/**
 * useProducts Hook
 *
 * Custom hook for fetching and managing products and categories
 *
 * Features:
 * - Fetch all categories
 * - Fetch all products (with optional category filter)
 * - Loading and error states
 * - Automatic data fetching on mount
 */

import { useState, useEffect, useCallback } from 'react';
import { getCategories, getProducts } from '../services/productService';

export function useProducts(categoryFilter = null) {
  const [categories, setCategories] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refetchTrigger, setRefetchTrigger] = useState(0);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch categories and products in parallel
      const [categoriesData, productsData] = await Promise.all([
        getCategories(),
        getProducts({ category: categoryFilter, inStockOnly: false }), // Admin needs to see all
      ]);

      setCategories(categoriesData);
      setProducts(productsData);
    } catch (err) {
      console.error('Failed to fetch products:', err);
      setError(err.message || 'Failed to load products. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, [categoryFilter]);

  useEffect(() => {
    fetchData();
  }, [fetchData, refetchTrigger]);

  const refetch = useCallback(() => {
    setRefetchTrigger((prev) => prev + 1);
  }, []);

  return {
    categories,
    products,
    loading,
    error,
    refetch,
  };
}

export default useProducts;
