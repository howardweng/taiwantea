import axios from 'axios';

// Use empty string for production (relative URLs) or fallback to localhost for dev
const API_URL = import.meta.env.VITE_API_URL !== undefined
  ? import.meta.env.VITE_API_URL
  : 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Important for cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle errors globally
    if (error.response?.status === 401) {
      // Ignore 401 errors from /auth/me (it's just checking login status)
      if (!error.config?.url?.includes('/auth/me')) {
        console.error('Unauthorized access');
      }
    }
    return Promise.reject(error);
  }
);

export default api;
