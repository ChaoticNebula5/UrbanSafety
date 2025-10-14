from typing import List, Dict
from datetime import datetime


class NotificationService:
    def __init__(self):
        self.sent_notifications = []  
    
    def send_emergency_alert(
        self, 
        incident_data: dict, 
        emergency_contacts: List[Dict[str, str]],
        user_name: str
    ) -> dict:
        timestamp = datetime.now().isoformat()
        notifications_sent = []
        
        message = f"""
EMERGENCY ALERT

{user_name} has reported an incident:
- {incident_data['title']}
- Severity: {incident_data.get('severity', 'UNKNOWN').upper()}
- Location: {incident_data['latitude']}, {incident_data['longitude']}
- Time: {timestamp}

Description: {incident_data['description']}

This is an automated safety alert from Urban Safety Platform.
        """
        
        for contact in emergency_contacts:
            print(f"\n[SMS] Sending to {contact['name']} ({contact['phone']}):")
            print(message)
            notifications_sent.append({
                "recipient": contact['name'],
                "phone": contact['phone'],
                "type": "emergency_contact",
                "status": "sent",
                "timestamp": timestamp
            })
        
        self._alert_authorities(incident_data, user_name, timestamp)
        notifications_sent.append({
            "recipient": "Local Police Station",
            "type": "authority",
            "status": "sent",
            "timestamp": timestamp
        })
        
        self.sent_notifications.extend(notifications_sent)
        
        return {
            "success": True,
            "notifications_sent": len(notifications_sent),
            "details": notifications_sent
        }
    
    def _alert_authorities(self, incident_data: dict, reporter: str, timestamp: str):
        """Mock alert to authorities"""
        print("\n[ALERT] Notifying MOCK AUTHORITIES (Police Control Room):")
        print(f"""
==========================================
INCIDENT REPORT - REQUIRES ATTENTION
==========================================

Incident: {incident_data['title']}
Category: {incident_data.get('category', 'OTHER').upper()}
Severity: {incident_data.get('severity', 'MEDIUM').upper()}

Location: 
  Lat: {incident_data['latitude']}
  Lng: {incident_data['longitude']}

Description:
{incident_data['description']}

Reporter: {reporter}
Time: {timestamp}

AI Summary: {incident_data.get('ai_summary', 'Processing...')}

==========================================
        """)
    
    def get_notification_history(self) -> List[dict]:
        """Get all sent notifications (for demo/debugging)"""
        return self.sent_notifications


notification_service = NotificationService()
