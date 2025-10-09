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
import Navigation from '../components/layout/Navigation';
import ProductGrid from '../components/customer/ProductGrid';
import BackToTop from '../components/layout/BackToTop';
import styles from './HomePage.module.css';

function HomePage() {
  const { categories, products, loading, error } = useProducts();

  return (
    <div className={styles.page}>
      {/* Sticky Navigation Bar */}
      {categories.length > 0 && <Navigation categories={categories} />}

      {/* Hero Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <h1 className={styles.title}>TAIWANTEA</h1>
          <p className={styles.subtitle}>Premium Taiwan Tea Leaves</p>
          <p className={styles.description}>
            Discover the finest selection of authentic Taiwanese teas.
            From delicate green teas to robust pu-erh, find your perfect brew.
          </p>
        </div>
      </header>

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
          <p>&copy; 2025 TAIWANTEA. All rights reserved.</p>
          <p className={styles.footerLinks}>
            <a href="#top">Privacy Policy</a>
            {' | '}
            <a href="#top">Terms of Service</a>
            {' | '}
            <a href="#top">Contact</a>
          </p>
        </div>
      </footer>

      {/* Back to Top Button */}
      <BackToTop />
    </div>
  );
}

export default HomePage;
