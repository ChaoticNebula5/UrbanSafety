import React, { useState } from 'react';
import { userService } from '../services/api';

const Home = () => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    password: '',
    email: '',
    emergency_contacts: [{ name: '', phone: '' }]
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleContactChange = (index, field, value) => {
    const newContacts = [...formData.emergency_contacts];
    newContacts[index] = {
      ...newContacts[index],
      [field]: value
    };
    setFormData(prev => ({
      ...prev,
      emergency_contacts: newContacts
    }));
  };

  const addContact = () => {
    setFormData(prev => ({
      ...prev,
      emergency_contacts: [...prev.emergency_contacts, { name: '', phone: '' }]
    }));
  };

  const removeContact = (indexToRemove) => {
    if (formData.emergency_contacts.length > 1) {
      setFormData(prev => ({
        ...prev,
        emergency_contacts: prev.emergency_contacts.filter((_, index) => index !== indexToRemove)
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    try {
      const response = await userService.register(formData);
      console.log('Registration successful:', response);
      setSuccess('✓ Registration Successful!');
      setFormData({
        name: '',
        phone: '',
        password: '',
        email: '',
        emergency_contacts: [{ name: '', phone: '' }]
      });
    } catch (err) {
      console.error('Registration error:', err);
      setError(typeof err === 'string' ? err : 'Registration failed. Please try again.');
    }
  };

  const styles = {
    container: {
      maxWidth: '500px',
      margin: '0 auto',
      padding: '20px',
    },
    form: {
      display: 'flex',
      flexDirection: 'column',
      gap: '15px',
    },
    input: {
      padding: '10px',
      border: '2px solid #1a365d',
      borderRadius: '4px',
      fontSize: '16px',
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
      backgroundColor: '#38a169',
      color: 'white',
      padding: '20px',
      borderRadius: '8px',
      marginTop: '20px',
      textAlign: 'center',
      animation: 'fadeIn 0.5s ease-in',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '10px',
    },
    successIcon: {
      fontSize: '48px',
      marginBottom: '10px',
    },
    contactsSection: {
      marginTop: '20px',
    },
    addButton: {
      marginTop: '10px',
      padding: '8px',
      backgroundColor: '#2c5282',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
    },
    removeButton: {
      padding: '8px',
      backgroundColor: '#e53e3e',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      marginLeft: '10px',
    },
    contactRow: {
      display: 'flex',
      alignItems: 'center',
      marginBottom: '10px',
    },
    contactInputs: {
      flex: 1,
      display: 'flex',
      gap: '10px',
    },
  };

  return (
    <div style={styles.container}>
      <h2>Register for Urban Safety</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={formData.name}
          onChange={handleInputChange}
          style={styles.input}
          required
          minLength="2"
          maxLength="100"
        />
        
        <input
          type="tel"
          name="phone"
          placeholder="Phone Number"
          value={formData.phone}
          onChange={handleInputChange}
          style={styles.input}
          required
          minLength="10"
          maxLength="15"
        />
        
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
          style={styles.input}
          required
          minLength="6"
        />
        
        <input
          type="email"
          name="email"
          placeholder="Email (optional)"
          value={formData.email}
          onChange={handleInputChange}
          style={styles.input}
        />

        <div style={styles.contactsSection}>
          <h3>Emergency Contacts</h3>
          {formData.emergency_contacts.map((contact, index) => (
            <div key={index} style={styles.contactRow}>
              <div style={styles.contactInputs}>
                <input
                  type="text"
                  placeholder="Contact Name"
                  value={contact.name}
                  onChange={(e) => handleContactChange(index, 'name', e.target.value)}
                  style={styles.input}
                  required
                  minLength="2"
                  maxLength="100"
                />
                <input
                  type="tel"
                  placeholder="Contact Phone"
                  value={contact.phone}
                  onChange={(e) => handleContactChange(index, 'phone', e.target.value)}
                  style={styles.input}
                  required
                  minLength="10"
                  maxLength="15"
                />
              </div>
              {index > 0 && (
                <button
                  type="button"
                  onClick={() => removeContact(index)}
                  style={styles.removeButton}
                  aria-label="Remove emergency contact"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <button type="button" onClick={addContact} style={styles.addButton}>
            Add Emergency Contact
          </button>
        </div>

        <button type="submit" style={styles.button}>
          Register
        </button>

        {error && <div style={styles.error}>{error}</div>}
        {success && (
          <div style={styles.success}>
            <span style={styles.successIcon}>✓</span>
            <h3 style={{ margin: 0 }}>{success}</h3>
            <p style={{ margin: '5px 0 0 0' }}>
              Thank you for joining SafeSphere! Your account has been created successfully.
            </p>
            <p style={{ margin: '5px 0 0 0', fontSize: '0.9em' }}>
              You can now login to access all SafeSphere features.
            </p>
          </div>
        )}
      </form>
    </div>
  );
};

export default Home;