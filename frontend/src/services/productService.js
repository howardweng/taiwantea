/**
 * Product Service
 *
 * API client for product and category endpoints
 */

import api from './api';

/**
 * Get all active categories
 *
 * @returns {Promise<Array>} Array of category objects
 * @throws {Error} If the request fails
 */
export async function getCategories() {
  try {
    const response = await api.get('/api/categories');

    if (response.data && response.data.categories) {
      // Transform _id to id for frontend components
      return response.data.categories.map(cat => ({
        ...cat,
        id: cat._id
      }));
    }

    throw new Error('Invalid response format');
  } catch (error) {
    console.error('getCategories error:', error);
    throw new Error(
      error.response?.data?.detail || 'Failed to fetch categories'
    );
  }
}

/**
 * Get all products with optional filters
 *
 * @param {Object} options - Query options
 * @param {string} [options.category] - Filter by category ID
 * @param {boolean} [options.inStockOnly=true] - Show only in-stock products
 * @param {number} [options.limit] - Limit number of results
 * @param {number} [options.skip=0] - Skip N results for pagination
 * @returns {Promise<Array>} Array of product objects
 * @throws {Error} If the request fails
 */
export async function getProducts(options = {}) {
  try {
    const { category, inStockOnly = true, limit, skip = 0 } = options;

    const params = new URLSearchParams();

    if (category) params.append('category', category);
    params.append('in_stock_only', inStockOnly);
    if (limit) params.append('limit', limit);
    if (skip) params.append('skip', skip);

    const response = await api.get(`/api/products?${params.toString()}`);

    if (response.data && response.data.products) {
      // Transform _id to id for frontend components
      return response.data.products.map(product => ({
        ...product,
        id: product._id
      }));
    }

    throw new Error('Invalid response format');
  } catch (error) {
    console.error('getProducts error:', error);
    throw new Error(
      error.response?.data?.detail || 'Failed to fetch products'
    );
  }
}

/**
 * Get single product by ID
 *
 * @param {string} productId - Product ID
 * @returns {Promise<Object>} Product object
 * @throws {Error} If the request fails
 */
export async function getProductById(productId) {
  try {
    const response = await api.get(`/api/products/${productId}`);

    if (response.data) {
      // Transform _id to id for frontend components
      return {
        ...response.data,
        id: response.data._id
      };
    }

    throw new Error('Invalid response format');
  } catch (error) {
    console.error('getProductById error:', error);

    if (error.response?.status === 404) {
      throw new Error('Product not found');
    }

    throw new Error(
      error.response?.data?.detail || 'Failed to fetch product'
    );
  }
}
