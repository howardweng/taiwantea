/**
 * HomePage - Main customer-facing page
 *
 * Features:
 * - Sticky navigation bar with category links
 * - Displays all tea categories
 * - Shows products grouped by category
 * - Smooth scroll navigation
 * - Back-to-top button
 * - Responsive design
 */

import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import useProducts from '../hooks/useProducts';
import useCarousel from '../hooks/useCarousel';
import Navigation from '../components/layout/Navigation';
import ProductGrid from '../components/customer/ProductGrid';
import BackToTop from '../components/layout/BackToTop';
import HeroCarousel from '../components/customer/HeroCarousel';
import IntroSection from '../components/customer/IntroSection';
import api from '../services/api';
import { getImageUrl } from '../utils/imageUtils';
import styles from './HomePage.module.css';

function HomePage() {
  const location = useLocation();
  const { categories, products, loading, error } = useProducts();
  const { slides: carouselSlides, loading: carouselLoading } = useCarousel();
  const [siteSettings, setSiteSettings] = useState(null);

  // Fetch site settings
  useEffect(() => {
    const fetchSiteSettings = async () => {
      try {
        const response = await api.get('/api/site-settings');
        setSiteSettings(response.data);
      } catch (error) {
        console.error('Failed to fetch site settings:', error);
        // Use default if fetch fails
        setSiteSettings({ shopeeStoreUrl: 'https://shopee.tw/' });
      }
    };
    fetchSiteSettings();
  }, []);

  // Add organization structured data (Schema.org) for SEO
  useEffect(() => {
    const organizationData = {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "台灣茗茶大師 TeaMaster",
      "url": "https://taiwantea.frrut.com",
      "logo": "https://taiwantea.frrut.com/tea-logo.png",
      "description": "提供100%台灣高山茶葉，包括烏龍茶、紅茶、白茶、綠茶及茶葉禮盒。手工採摘，天然無添加，品質保證。",
      "address": {
        "@type": "PostalAddress",
        "addressCountry": "TW",
        "addressLocality": "台灣"
      },
      "sameAs": []
    };

    // Create script tag and add to head
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(organizationData);
    script.id = 'organization-structured-data';
    document.head.appendChild(script);

    // Cleanup function
    return () => {
      const oldScript = document.getElementById('organization-structured-data');
      if (oldScript) {
        document.head.removeChild(oldScript);
      }
    };
  }, []);

  // Handle hash navigation from other pages
  useEffect(() => {
    // Wait for content to load before scrolling
    if (loading || categories.length === 0) return;

    const hash = location.hash;
    if (hash) {
      // Remove the # to get the category ID
      const categoryId = hash.substring(1);

      // Use setTimeout to ensure DOM is ready
      setTimeout(() => {
        const element = document.getElementById(categoryId);
        if (element) {
          const offset = 80; // Height of sticky nav
          const elementPosition = element.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - offset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      }, 100);
    }
  }, [location.hash, loading, categories]);

  // Scroll to products section
  const scrollToProducts = () => {
    const element = document.getElementById('products');
    if (element) {
      const offset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;
      window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    }
  };

  const heroSlides = carouselSlides.map(slide => ({
    image: getImageUrl(slide.imageUrl),
    title: slide.title,
    subtitle: slide.subtitle,
    cta: {
      label: '立即選購',
      onClick: scrollToProducts
    }
  }));

  return (
    <div className={styles.page}>
      {/* Sticky Navigation Bar */}
      {categories.length > 0 && <Navigation categories={categories} />}

      {/* Hero Carousel */}
      {!carouselLoading && heroSlides.length > 0 && (
        <HeroCarousel slides={heroSlides} autoPlayInterval={5000} />
      )}

      {/* Intro Section */}
      <IntroSection />

      {/* Product Grid */}
      <ProductGrid
        categories={categories}
        products={products}
        loading={loading}
        error={error}
        shopeeStoreUrl={siteSettings?.shopeeStoreUrl || 'https://shopee.tw/'}
      />

      {/* Footer */}
      <footer className={styles.footer}>
        <div className={styles.footerContent}>
          <p>&copy; 2025 TAIWANTEA. 版權所有。</p>
          <p className={styles.footerLinks}>
            <a href="#top">隱私權政策</a>
            {' | '}
            <a href="#top">服務條款</a>
            {' | '}
            <a href="#top">聯絡我們</a>
          </p>
        </div>
      </footer>

      {/* Back to Top Button */}
      <BackToTop />
    </div>
  );
}

export default HomePage;
