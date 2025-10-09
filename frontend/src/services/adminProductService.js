/**
 * Admin Product Service
 *
 * API calls for admin product management
 */

import api from './api';

/**
 * Create a new product
 */
export async function createProduct(productData) {
  const response = await api.post('/api/admin/products', productData);
  if (response.data) {
    return {
      ...response.data,
      id: response.data._id,
    };
  }
  return response.data;
}

/**
 * Update an existing product
 */
export async function updateProduct(productId, productData) {
  const response = await api.put(`/api/admin/products/${productId}`, productData);
  if (response.data) {
    return {
      ...response.data,
      id: response.data._id,
    };
  }
  return response.data;
}

/**
 * Delete a product
 */
export async function deleteProduct(productId) {
  const response = await api.delete(`/api/admin/products/${productId}`);
  return response.data;
}

/**
 * Get all products (admin view - includes out of stock)
 */
export async function getAllProductsAdmin(categoryFilter = null) {
  const params = categoryFilter ? { category: categoryFilter } : {};
  const response = await api.get('/api/admin/products', { params });

  if (response.data && response.data.products) {
    return response.data.products.map((product) => ({
      ...product,
      id: product._id,
    }));
  }

  return [];
}
