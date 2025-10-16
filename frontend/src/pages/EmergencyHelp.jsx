import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const EmergencyHelp = () => {
  const [pressCount, setPressCount] = useState(0);
  const [isActivated, setIsActivated] = useState(false);
  const [countdown, setCountdown] = useState(5);
  const navigate = useNavigate();

  const styles = {
    container: {
      maxWidth: '800px',
      margin: '0 auto',
      padding: '20px',
      textAlign: 'center',
    },
    heading: {
      color: '#1a365d',
      marginBottom: '20px',
    },
    instructionsCard: {
      backgroundColor: '#f8f9fa',
      border: '2px solid #1a365d',
      borderRadius: '8px',
      padding: '20px',
      marginBottom: '30px',
      textAlign: 'left',
    },
    instructionsList: {
      listStyle: 'decimal',
      paddingLeft: '20px',
      marginTop: '10px',
    },
    listItem: {
      marginBottom: '10px',
      lineHeight: '1.5',
    },
    emergencyButton: {
      width: '200px',
      height: '200px',
      borderRadius: '50%',
      backgroundColor: isActivated ? '#38a169' : '#e53e3e',
      border: 'none',
      color: 'white',
      fontSize: '1.5rem',
      fontWeight: 'bold',
      cursor: 'pointer',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      transition: 'transform 0.2s, box-shadow 0.2s',
      margin: '20px auto',
      display: 'block',
      position: 'relative',
      animation: isActivated ? 'none' : 'pulse 2s infinite',
    },
    warningText: {
      color: '#e53e3e',
      fontWeight: 'bold',
      marginTop: '20px',
    },
    activatedMessage: {
      backgroundColor: '#38a169',
      color: 'white',
      padding: '20px',
      borderRadius: '8px',
      marginTop: '20px',
      animation: 'fadeIn 0.5s',
    },
    noteCard: {
      backgroundColor: '#fff3cd',
      border: '1px solid #ffeeba',
      borderRadius: '4px',
      padding: '15px',
      marginTop: '20px',
      color: '#856404',
    },
    '@keyframes pulse': {
      '0%': {
        transform: 'scale(1)',
        boxShadow: '0 0 0 0 rgba(229, 62, 62, 0.4)',
      },
      '70%': {
        transform: 'scale(1.05)',
        boxShadow: '0 0 0 20px rgba(229, 62, 62, 0)',
      },
      '100%': {
        transform: 'scale(1)',
        boxShadow: '0 0 0 0 rgba(229, 62, 62, 0)',
      },
    },
  };

  useEffect(() => {
    if (isActivated && countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    } else if (isActivated && countdown === 0) {
      // Here you would typically:
      // 1. Send emergency alert to backend
      // 2. Notify emergency contacts
      // 3. Share location with authorities
      navigate('/emergency-contacts');
    }
  }, [isActivated, countdown, navigate]);

  const handleEmergencyPress = () => {
    if (isActivated) return;
    
    const newCount = pressCount + 1;
    setPressCount(newCount);
    
    if (newCount === 3) {
      setIsActivated(true);
      // Add vibration if supported by the device
      if ('vibrate' in navigator) {
        navigator.vibrate(1000);
      }
    }

    // Reset count if not pressed again within 2 seconds
    setTimeout(() => {
      if (!isActivated) {
        setPressCount(0);
      }
    }, 2000);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Emergency Help Button</h1>
      
      <div style={styles.instructionsCard}>
        <h2>How This Works:</h2>
        <ol style={styles.instructionsList}>
          <li style={styles.listItem}>
            Press the red emergency button 3 times quickly to activate emergency response.
          </li>
          <li style={styles.listItem}>
            Once activated, the system will:
            <ul>
              <li>Alert nearby law enforcement and emergency services</li>
              <li>Send your current location to authorities</li>
              <li>Notify your registered emergency contacts</li>
              <li>Record an audio snippet of your surroundings (if permitted)</li>
            </ul>
          </li>
          <li style={styles.listItem}>
            You'll have a 5-second countdown before the alert is sent, allowing you to cancel if activated by mistake.
          </li>
        </ol>
      </div>

      <div style={styles.noteCard}>
        <strong>Important Note:</strong> Only use this button in genuine emergency situations. False alarms may result in 
        unnecessary deployment of emergency services and could affect response times for real emergencies.
      </div>

      <button
        onClick={handleEmergencyPress}
        style={styles.emergencyButton}
        aria-label="Emergency Help Button"
      >
        {isActivated ? 'ACTIVATED' : 'EMERGENCY'}
        {!isActivated && pressCount > 0 && (
          <div style={{ fontSize: '0.8rem', marginTop: '5px' }}>
            Press {3 - pressCount} more times
          </div>
        )}
      </button>

      {isActivated && (
        <div style={styles.activatedMessage}>
          <h2>Emergency Help Activated!</h2>
          <p>Sending alert in {countdown} seconds...</p>
          <p>Emergency services will be notified of your location.</p>
        </div>
      )}

      {!isActivated && pressCount > 0 && (
        <div style={styles.warningText}>
          Press {3 - pressCount} more times quickly to activate emergency response
        </div>
      )}
    </div>
  );
};

export default EmergencyHelp;