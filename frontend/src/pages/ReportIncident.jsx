import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents, useMap as useLeafletMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import '../styles/map.css';
import { incidentService } from '../services/api';

// Create custom marker icon
// Custom marker with bounce animation
const customMarker = L.icon({
  iconUrl: 'data:image/svg+xml;base64,' + btoa(`
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="30" height="40">
      <path fill="#e53e3e" d="M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0zM192 272c44.183 0 80-35.817 80-80s-35.817-80-80-80-80 35.817-80 80 35.817 80 80 80z"/>
    </svg>
  `),
  iconSize: [30, 40],
  iconAnchor: [15, 40],
  popupAnchor: [0, -40],
  className: 'bounce-marker' // Add class for animation
});

const LocationPicker = ({ onLocationSelect }) => {
  const map = useMapEvents({
    click(e) {
      onLocationSelect([e.latlng.lat, e.latlng.lng]);
      map.flyTo(e.latlng, map.getZoom(), {
        animate: true,
        duration: 0.5
      });
    },
  });
  return null;
};

// Marker component with fly-to functionality
const MarkerWithFlyTo = ({ position, icon }) => {
  const map = useLeafletMap();
  
  return (
    <Marker 
      position={position} 
      icon={icon}
      eventHandlers={{
        click: () => {
          map.flyTo(position, map.getZoom(), {
            animate: true,
            duration: 0.5
          });
        }
      }}
    />
  );
};

const ReportIncident = () => {
  const [formData, setFormData] = useState({
    type: 'harassment',
    customType: '',
    location: null,
    description: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showCustomType, setShowCustomType] = useState(false);
  const [showThankYou, setShowThankYou] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLocationSelect = (coordinates) => {
    setFormData(prev => ({
      ...prev,
      location: coordinates
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!formData.location) {
      setError('Please select a location on the map');
      return;
    }

    try {
      const incidentType = formData.type === 'other' ? formData.customType : formData.type;
      const response = await incidentService.reportIncident({
        ...formData,
        type: incidentType,
        latitude: formData.location[0],
        longitude: formData.location[1],
      });
      console.log('Incident reported:', response);
      setSuccess('Incident reported successfully');
      setShowThankYou(true);
      setFormData({
        type: 'harassment',
        customType: '',
        location: null,
        description: '',
      });
    } catch (err) {
      console.error('Reporting error:', err);
      setError(typeof err === 'string' ? err : 'Failed to report incident. Please try again.');
    }
  };

  const styles = {
    container: {
      maxWidth: '800px',
      margin: '0 auto',
      padding: '20px',
    },
    locationInstruction: {
      marginBottom: '15px',
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      color: '#1a365d',
    },
    locationIcon: {
      color: '#e53e3e',
      fontSize: '24px',
    },
    locationText: {
      margin: 0,
      fontSize: '1rem',
    },
    locationConfirm: {
      backgroundColor: '#38a169',
      color: 'white',
      padding: '12px 20px',
      borderRadius: '4px',
      marginBottom: '15px',
      display: formData.location ? 'block' : 'none',
      animation: 'fadeIn 0.5s ease-in',
      textAlign: 'center',
    },
    form: {
      display: 'flex',
      flexDirection: 'column',
      gap: '15px',
    },
    select: {
      padding: '10px',
      border: '2px solid #1a365d',
      borderRadius: '4px',
      fontSize: '16px',
    },
    textarea: {
      padding: '10px',
      border: '2px solid #1a365d',
      borderRadius: '4px',
      fontSize: '16px',
      minHeight: '100px',
    },
    mapContainer: {
      height: '400px',
      marginBottom: '20px',
      border: '2px solid #1a365d',
      borderRadius: '4px',
    },
    button: {
      padding: '12px',
      backgroundColor: '#1a365d',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      fontSize: '16px',
    },
    error: {
      color: '#e53e3e',
      marginTop: '10px',
    },
    success: {
      color: '#38a169',
      marginTop: '10px',
    },
  };

  if (showThankYou) {
    return (
      <div style={styles.container}>
        <div style={{
          textAlign: 'center',
          padding: '40px 20px',
          backgroundColor: '#f7fafc',
          borderRadius: '8px',
          border: '2px solid #1a365d',
        }}>
          <h2 style={{ color: '#1a365d', marginBottom: '20px' }}>Thank You for Your Report</h2>
          <p style={{ fontSize: '1.1rem', color: '#4a5568', marginBottom: '20px' }}>
            Your incident has been successfully reported. We take every report seriously and will take appropriate action.
          </p>
          <div style={{ marginTop: '30px' }}>
            <h3 style={{ color: '#1a365d', marginBottom: '15px' }}>Important Emergency Numbers:</h3>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', flexWrap: 'wrap' }}>
              <div style={{ padding: '10px', backgroundColor: '#fff', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                <strong>Police:</strong> 100
              </div>
              <div style={{ padding: '10px', backgroundColor: '#fff', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                <strong>Ambulance:</strong> 108
              </div>
              <div style={{ padding: '10px', backgroundColor: '#fff', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                <strong>Fire:</strong> 101
              </div>
            </div>
          </div>
          <div style={{ marginTop: '30px' }}>
            <a
              href="/emergency-contacts"
              style={{
                padding: '12px 24px',
                backgroundColor: '#1a365d',
                color: 'white',
                textDecoration: 'none',
                borderRadius: '4px',
                display: 'inline-block',
              }}
            >
              View All Emergency Contacts
            </a>
          </div>
          <button
            onClick={() => setShowThankYou(false)}
            style={{
              marginTop: '20px',
              padding: '12px 24px',
              backgroundColor: '#2c5282',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Report Another Incident
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2>Report an Incident</h2>
      <blockquote style={{
        borderLeft: '4px solid #1a365d',
        paddingLeft: '20px',
        marginBottom: '20px',
        color: '#4a5568',
        fontStyle: 'italic'
      }}>
        "The near miss reported today is the accident that doesn't happen tomorrow"
      </blockquote>
      <form onSubmit={handleSubmit} style={styles.form}>
        <select
          name="type"
          value={formData.type}
          onChange={(e) => {
            const value = e.target.value;
            setShowCustomType(value === 'other');
            handleInputChange(e);
            if (value !== 'other') {
              setFormData(prev => ({ ...prev, customType: '' }));
            }
          }}
          style={styles.select}
          required
        >
          <option value="harassment">Harassment</option>
          <option value="fire">Fire</option>
          <option value="accident">Accident</option>
          <option value="theft">Theft</option>
          <option value="vandalism">Vandalism</option>
          <option value="suspicious_activity">Suspicious Activity</option>
          <option value="medical_emergency">Medical Emergency</option>
          <option value="traffic_violation">Traffic Violation</option>
          <option value="noise_complaint">Noise Complaint</option>
          <option value="other">Other (Specify)</option>
        </select>
        
        {showCustomType && (
          <input
            type="text"
            name="customType"
            placeholder="Specify incident type"
            value={formData.customType}
            onChange={handleInputChange}
            style={styles.input}
            required
          />
        )}

        <textarea
          name="description"
          placeholder="Describe the incident..."
          value={formData.description}
          onChange={handleInputChange}
          style={styles.textarea}
          required
        />

        <div style={styles.locationInstruction}>
          <span style={styles.locationIcon}>📍</span>
          <p style={styles.locationText}>
            Mark the location on the map by clicking where the incident occurred
          </p>
        </div>

        {formData.location && (
          <div style={styles.locationConfirm}>
            ✓ Location marked successfully! You can click elsewhere on the map to change the location.
          </div>
        )}

        <div style={styles.mapContainer}>
          <MapContainer
            center={[30.3398, 76.3869]} // Patiala coordinates
            zoom={13}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            <LocationPicker onLocationSelect={handleLocationSelect} />
            {formData.location && (
              <MarkerWithFlyTo 
                position={formData.location} 
                icon={customMarker}
              />
            )}
          </MapContainer>
        </div>

        <button type="submit" style={styles.button}>
          Report Incident
        </button>

        {error && <div style={styles.error}>{error}</div>}
        {success && <div style={styles.success}>{success}</div>}
      </form>
    </div>
  );
};

export default ReportIncident;