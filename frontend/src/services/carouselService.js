/**
 * Carousel Service
 *
 * Handles API requests for carousel data
 */

import api from './api';

/**
 * Get all active carousel slides
 * @returns {Promise<Array>} Array of carousel slides
 */
export async function getCarouselSlides() {
  try {
    const response = await api.get('/api/carousel');
    return response.data.slides || [];
  } catch (error) {
    console.error('Error fetching carousel slides:', error);
    throw new Error(
      error.response?.data?.detail || 'Failed to load carousel slides'
    );
  }
}

/**
 * Admin: Get all carousel slides (including inactive)
 * @returns {Promise<Array>} Array of carousel slides
 */
export async function getAllCarouselSlides() {
  try {
    const response = await api.get('/api/admin/carousel');
    return response.data.slides || [];
  } catch (error) {
    console.error('Error fetching all carousel slides:', error);
    throw new Error(
      error.response?.data?.detail || 'Failed to load carousel slides'
    );
  }
}

/**
 * Admin: Create a new carousel slide
 * @param {Object} slideData - Slide data
 * @returns {Promise<Object>} Created slide
 */
export async function createCarouselSlide(slideData) {
  try {
    const response = await api.post('/api/admin/carousel', slideData);
    return response.data;
  } catch (error) {
    console.error('Error creating carousel slide:', error);
    throw new Error(
      error.response?.data?.detail || 'Failed to create carousel slide'
    );
  }
}

/**
 * Admin: Update a carousel slide
 * @param {string} slideId - Slide ID
 * @param {Object} updates - Fields to update
 * @returns {Promise<Object>} Updated slide
 */
export async function updateCarouselSlide(slideId, updates) {
  try {
    const response = await api.put(`/api/admin/carousel/${slideId}`, updates);
    return response.data;
  } catch (error) {
    console.error('Error updating carousel slide:', error);
    throw new Error(
      error.response?.data?.detail || 'Failed to update carousel slide'
    );
  }
}

/**
 * Admin: Delete a carousel slide
 * @param {string} slideId - Slide ID
 * @returns {Promise<Object>} Success message
 */
export async function deleteCarouselSlide(slideId) {
  try {
    const response = await api.delete(`/api/admin/carousel/${slideId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting carousel slide:', error);
    throw new Error(
      error.response?.data?.detail || 'Failed to delete carousel slide'
    );
  }
}
