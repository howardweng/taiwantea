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

import useProducts from '../hooks/useProducts';
import useCarousel from '../hooks/useCarousel';
import Navigation from '../components/layout/Navigation';
import ProductGrid from '../components/customer/ProductGrid';
import BackToTop from '../components/layout/BackToTop';
import HeroCarousel from '../components/customer/HeroCarousel';
import IntroSection from '../components/customer/IntroSection';
import styles from './HomePage.module.css';

function HomePage() {
  const { categories, products, loading, error } = useProducts();
  const { slides: carouselSlides, loading: carouselLoading } = useCarousel();

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
    image: slide.imageUrl,
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
