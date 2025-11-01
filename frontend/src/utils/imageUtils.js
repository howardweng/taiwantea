/**
 * Image utility functions
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8585';

/**
 * Get the full image URL by prepending API URL to relative paths
 * @param {string} imagePath - Image path (can be relative or absolute)
 * @returns {string} - Full image URL
 */
export const getImageUrl = (imagePath) => {
  if (!imagePath) return '';

  // If already an absolute URL (http:// or https://), return as is
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath;
  }

  // If it's a relative path starting with /, prepend API_URL
  if (imagePath.startsWith('/')) {
    return `${API_URL}${imagePath}`;
  }

  // Otherwise, return as is
  return imagePath;
};

/**
 * Get thumbnail URL from product data
 * @param {object} product - Product object with imageUrl and thumbnailUrl
 * @returns {string} - Full thumbnail URL
 */
export const getThumbnailUrl = (product) => {
  const imagePath = product.thumbnailUrl || product.imageUrl;
  return getImageUrl(imagePath);
};

/**
 * Get full image URL from product data
 * @param {object} product - Product object with imageUrl
 * @returns {string} - Full image URL
 */
export const getFullImageUrl = (product) => {
  return getImageUrl(product.imageUrl);
};
