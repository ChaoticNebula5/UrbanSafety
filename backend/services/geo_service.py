from typing import List, Dict
import json
from pathlib import Path
from math import radians, cos, sin, asin, sqrt

from sklearn.cluster import DBSCAN
import numpy as np


class GeoService:
    
    def __init__(self):
        landmarks_path = Path(__file__).parent.parent / "data" / "patiala_landmarks.json"
        
        with open(landmarks_path, 'r', encoding='utf-8') as f:
            self.landmarks_data = json.load(f)
    
    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
     
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return round(km, 2)
    
    def find_nearest_landmark(self, lat: float, lng: float, landmark_type: str = "police_stations") -> Dict:

        landmarks = self.landmarks_data.get(landmark_type, [])
        
        if not landmarks:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for landmark in landmarks:
            distance = self.haversine_distance(
                lat, lng,
                landmark['lat'], landmark['lng']
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest = {
                    "name": landmark['name'],
                    "distance_km": distance,
                    "coordinates": {"lat": landmark['lat'], "lng": landmark['lng']}
                }
                if 'phone' in landmark:
                    nearest['phone'] = landmark['phone']
                if 'emergency' in landmark:
                    nearest['emergency'] = landmark['emergency']
        
        return nearest
    
    def get_spatial_context(self, lat: float, lng: float) -> Dict:
        return {
            "nearest_police_station": self.find_nearest_landmark(lat, lng, "police_stations"),
            "nearest_hospital": self.find_nearest_landmark(lat, lng, "hospitals"),
            "nearby_landmark": self.find_nearest_landmark(lat, lng, "landmarks")
        }
    
    def cluster_incidents(self, incidents: List[Dict], eps_km: float = 0.5) -> List[Dict]:
        if len(incidents) < 2:
            return []
        
        coords = np.array([[inc['latitude'], inc['longitude']] for inc in incidents])
        
        eps_degrees = eps_km / 111.0  
        clustering = DBSCAN(eps=eps_degrees, min_samples=2).fit(coords)
        
        clusters = {}
        for idx, label in enumerate(clustering.labels_):
            if label == -1:  
                continue
            
            if label not in clusters:
                clusters[label] = []
            
            clusters[label].append(incidents[idx])
        
        cluster_summaries = []
        for label, cluster_incidents in clusters.items():
            lats = [inc['latitude'] for inc in cluster_incidents]
            lngs = [inc['longitude'] for inc in cluster_incidents]
            center_lat = sum(lats) / len(lats)
            center_lng = sum(lngs) / len(lngs)
            
            severity_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
            severities = [severity_map.get(inc.get('severity', 'medium'), 2) for inc in cluster_incidents]
            avg_severity = sum(severities) / len(severities)
            
            nearest_police = self.find_nearest_landmark(center_lat, center_lng, "police_stations")
            
            cluster_summaries.append({
                "cluster_id": int(label),
                "center": {"lat": round(center_lat, 4), "lng": round(center_lng, 4)},
                "incident_count": len(cluster_incidents),
                "severity_score": round(avg_severity, 2),
                "radius_km": eps_km,
                "nearest_police_station": nearest_police,
                "incident_ids": [inc.get('id') for inc in cluster_incidents if 'id' in inc]
            })
        
        return sorted(cluster_summaries, key=lambda x: x['severity_score'], reverse=True)
    
    def generate_heatmap_data(self, incidents: List[Dict]) -> Dict:
        severity_weights = {
            'low': 0.25,
            'medium': 0.5,
            'high': 0.75,
            'critical': 1.0
        }
        
        points = []
        for inc in incidents:
            weight = severity_weights.get(inc.get('severity', 'medium'), 0.5)
            points.append({
                "lat": inc['latitude'],
                "lng": inc['longitude'],
                "weight": weight,
                "category": inc.get('category', 'other')
            })
        
        return {
            "total_incidents": len(incidents),
            "points": points,
            "legend": {
                "low": "Minor incidents",
                "medium": "Moderate concern",
                "high": "Requires attention",
                "critical": "Immediate danger"
            }
        }
    
    def identify_danger_zones(self, incidents: List[Dict], threshold: int = 3) -> List[Dict]:
        clusters = self.cluster_incidents(incidents, eps_km=1.0)
        
        danger_zones = []
        for cluster in clusters:
            if cluster['incident_count'] >= threshold:
                cluster_incidents = [inc for inc in incidents if inc.get('id') in cluster['incident_ids']]
                categories = [inc.get('category', 'other') for inc in cluster_incidents]
                dominant_category = max(set(categories), key=categories.count)
                
                danger_zones.append({
                    "zone_id": cluster['cluster_id'],
                    "center": cluster['center'],
                    "radius_km": 1.0,
                    "incident_count": cluster['incident_count'],
                    "severity_score": cluster['severity_score'],
                    "dominant_category": dominant_category,
                    "nearest_police_station": cluster['nearest_police_station'],
                    "risk_level": "high" if cluster['severity_score'] >= 3 else "medium"
                })
        
        return danger_zones


geo_service = GeoService()
