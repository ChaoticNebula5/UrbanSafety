import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, HeatmapLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { incidentService } from '../services/api';

const Dashboard = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchIncidents = async () => {
    try {
      const data = await incidentService.getIncidents();
      setIncidents(data);
      setError('');
    } catch (err) {
      console.error('Error fetching incidents:', err);
      setError('Failed to load incidents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIncidents();
    // Set up auto-refresh every 30 seconds
    const interval = setInterval(fetchIncidents, 30000);
    return () => clearInterval(interval);
  }, []);

  const styles = {
    container: {
      display: 'flex',
      gap: '20px',
      padding: '20px',
      maxWidth: '1200px',
      margin: '0 auto',
    },
    mapContainer: {
      flex: '1',
      height: '600px',
      border: '2px solid #1a365d',
      borderRadius: '4px',
    },
    sidebar: {
      width: '300px',
      padding: '20px',
      backgroundColor: '#f8f9fa',
      border: '2px solid #1a365d',
      borderRadius: '4px',
    },
    header: {
      color: '#1a365d',
      marginBottom: '20px',
    },
    list: {
      listStyle: 'none',
      padding: 0,
      margin: 0,
    },
    listItem: {
      padding: '10px',
      borderBottom: '1px solid #dee2e6',
      fontSize: '14px',
    },
    error: {
      color: '#e53e3e',
      padding: '10px',
      marginBottom: '10px',
      backgroundColor: '#fff5f5',
      borderRadius: '4px',
    },
    loading: {
      color: '#718096',
      textAlign: 'center',
      padding: '20px',
    },
  };

  if (loading) {
    return <div style={styles.loading}>Loading dashboard...</div>;
  }

  return (
    <div style={styles.container}>
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
          {/* Heatmap layer will be added here once we have real data */}
        </MapContainer>
      </div>

      <div style={styles.sidebar}>
        <h2 style={styles.header}>Recent Reports</h2>
        {error && <div style={styles.error}>{error}</div>}
        <ul style={styles.list}>
          {incidents.slice(0, 10).map((incident, index) => (
            <li key={index} style={styles.listItem}>
              <strong>{incident.type}</strong>
              <br />
              <small>
                {new Date(incident.timestamp).toLocaleDateString()} at{' '}
                {new Date(incident.timestamp).toLocaleTimeString()}
              </small>
              <p>{incident.description}</p>
            </li>
          ))}
          {incidents.length === 0 && (
            <li style={styles.listItem}>No incidents reported yet</li>
          )}
        </ul>

        <h2 style={styles.header}>Hotspots</h2>
        <ul style={styles.list}>
          {/* This will be populated once we have clustering logic */}
          <li style={styles.listItem}>Coming soon...</li>
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;