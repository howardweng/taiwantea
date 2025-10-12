/**
 * useCarousel Hook
 *
 * Custom hook for fetching and managing carousel slides
 *
 * Features:
 * - Fetch active carousel slides
 * - Loading and error states
 * - Automatic data fetching on mount
 */

import { useState, useEffect, useCallback } from 'react';
import { getCarouselSlides } from '../services/carouselService';

export function useCarousel() {
  const [slides, setSlides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refetchTrigger, setRefetchTrigger] = useState(0);

  const fetchSlides = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const slidesData = await getCarouselSlides();
      setSlides(slidesData);
    } catch (err) {
      console.error('Failed to fetch carousel slides:', err);
      setError(err.message || 'Failed to load carousel slides. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSlides();
  }, [fetchSlides, refetchTrigger]);

  const refetch = useCallback(() => {
    setRefetchTrigger((prev) => prev + 1);
  }, []);

  return {
    slides,
    loading,
    error,
    refetch,
  };
}

export default useCarousel;
