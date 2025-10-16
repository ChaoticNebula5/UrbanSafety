import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const userService = {
  register: async (userData) => {
    try {
      const response = await api.post('/api/users/register', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  login: async (credentials) => {
    try {
      const response = await api.post('/api/users/login', credentials);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};

export const incidentService = {
  reportIncident: async (incidentData) => {
    try {
      const response = await api.post('/api/incidents', incidentData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  getIncidents: async () => {
    try {
      const response = await api.get('/api/incidents');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};

export default api;