import React from 'react';

const EmergencyContacts = () => {
  const styles = {
    container: {
      maxWidth: '800px',
      margin: '0 auto',
      padding: '20px',
    },
    heading: {
      color: '#1a365d',
      marginBottom: '20px',
    },
    grid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: '20px',
      marginTop: '20px',
    },
    card: {
      border: '2px solid #1a365d',
      borderRadius: '8px',
      padding: '20px',
      backgroundColor: '#fff',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    },
    cardTitle: {
      color: '#1a365d',
      marginBottom: '10px',
      fontSize: '1.2rem',
      fontWeight: 'bold',
    },
    contact: {
      marginBottom: '8px',
    },
    phone: {
      color: '#2c5282',
      fontWeight: 'bold',
      fontSize: '1.1rem',
    },
    description: {
      color: '#4a5568',
      fontSize: '0.9rem',
      marginTop: '5px',
    },
    note: {
      backgroundColor: '#e2e8f0',
      padding: '15px',
      borderRadius: '6px',
      marginTop: '20px',
      color: '#4a5568',
      fontSize: '0.9rem',
    },
  };

  const emergencyContacts = [
    {
      category: 'Police Emergency',
      contacts: [
        { number: '100', description: 'Police Control Room' },
        { number: '112', description: 'National Emergency Number' },
        { number: '1091', description: 'Women Helpline' },
      ]
    },
    {
      category: 'Medical Emergency',
      contacts: [
        { number: '108', description: 'Ambulance Services' },
        { number: '102', description: 'Pregnancy Medical Van' },
        { number: '104', description: 'Health Helpline' },
      ]
    },
    {
      category: 'Fire Emergency',
      contacts: [
        { number: '101', description: 'Fire Control Room' },
      ]
    },
    {
      category: 'Disaster Management',
      contacts: [
        { number: '1078', description: 'District Emergency Operation Center' },
        { number: '1070', description: 'State Emergency Operation Center' },
      ]
    },
    {
      category: 'Local Helplines',
      contacts: [
        { number: '1098', description: 'Child Helpline' },
        { number: '181', description: 'Women Helpline' },
        { number: '1363', description: 'Tourist Helpline' },
      ]
    },
    {
      category: 'Patiala Emergency',
      contacts: [
        { number: '+91-175-2212223', description: 'Patiala Police Control Room' },
        { number: '+91-175-2212368', description: 'Rajindra Hospital' },
        { number: '+91-175-2970349', description: 'Civil Hospital' },
      ]
    }
  ];

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Emergency Contact Numbers</h1>
      
      <div style={styles.note}>
        <strong>Important Note:</strong> In case of any emergency, please don't hesitate to call these numbers. 
        These services are available 24/7 and are free of charge. If one number doesn't work, please try the 
        alternative numbers provided.
      </div>

      <div style={styles.grid}>
        {emergencyContacts.map((category, index) => (
          <div key={index} style={styles.card}>
            <h2 style={styles.cardTitle}>{category.category}</h2>
            {category.contacts.map((contact, contactIndex) => (
              <div key={contactIndex} style={styles.contact}>
                <div style={styles.phone}>{contact.number}</div>
                <div style={styles.description}>{contact.description}</div>
              </div>
            ))}
          </div>
        ))}
      </div>

      <div style={styles.note}>
        <strong>Save these numbers:</strong> We recommend saving these emergency numbers in your phone. 
        In an emergency situation, every second counts, and having these numbers readily available could 
        make a crucial difference.
      </div>
    </div>
  );
};

export default EmergencyContacts;