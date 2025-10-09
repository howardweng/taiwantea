/**
 * Admin Category Service
 *
 * API calls for admin category management
 */

import api from './api';

/**
 * Create a new category
 */
export async function createCategory(categoryData) {
  const response = await api.post('/api/admin/categories', categoryData);
  if (response.data) {
    return {
      ...response.data,
      id: response.data._id,
    };
  }
  return response.data;
}

/**
 * Update an existing category
 */
export async function updateCategory(categoryId, categoryData) {
  const response = await api.put(`/api/admin/categories/${categoryId}`, categoryData);
  if (response.data) {
    return {
      ...response.data,
      id: response.data._id,
    };
  }
  return response.data;
}

/**
 * Delete a category
 */
export async function deleteCategory(categoryId) {
  const response = await api.delete(`/api/admin/categories/${categoryId}`);
  return response.data;
}
