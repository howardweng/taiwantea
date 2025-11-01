/**
 * Navigation Component
 *
 * Sticky navigation bar with category links and mobile menu
 */

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';
import api from '../../services/api';
import styles from './Navigation.module.css';

function Navigation({ categories }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [siteSettings, setSiteSettings] = useState(null);

  // Fetch site settings
  useEffect(() => {
    const fetchSiteSettings = async () => {
      try {
        const response = await api.get('/api/site-settings');
        setSiteSettings(response.data);
      } catch (error) {
        console.error('Failed to fetch site settings:', error);
        // Use default values if fetch fails
        setSiteSettings({
          logoType: 'text',
          logoIcon: '🍵',
          brandName: 'TAIWANTEA'
        });
      }
    };
    fetchSiteSettings();
  }, []);

  // Handle scroll to add shadow when scrolled
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Smooth scroll to category section
  const scrollToCategory = (categoryId) => {
    // Check if we're on the homepage
    if (location.pathname === '/') {
      // We're on homepage, scroll to section
      const element = document.getElementById(categoryId);
      if (element) {
        const offset = 80; // Height of sticky nav
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });

        // Close mobile menu after navigation
        setIsMenuOpen(false);
      }
    } else {
      // We're on another page, navigate to homepage with hash
      navigate(`/#${categoryId}`);
      setIsMenuOpen(false);
    }
  };

  // Scroll to top
  const scrollToTop = () => {
    // Check if we're on the homepage
    if (location.pathname === '/') {
      // We're on homepage, scroll to top
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    } else {
      // We're on another page, navigate to homepage
      navigate('/');
    }
    setIsMenuOpen(false);
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className={`${styles.nav} ${isScrolled ? styles.scrolled : ''}`}>
      <div className={styles.container}>
        {/* Logo/Brand */}
        <button
          onClick={scrollToTop}
          className={styles.brand}
          aria-label="回到頂部"
        >
          {siteSettings && (
            <>
              {siteSettings.logoType === 'image' ? (
                <>
                  <img
                    src={siteSettings.logoImageUrl}
                    alt={siteSettings.brandName}
                    className={styles.brandImage}
                  />
                  <div className={styles.brandTextContainer}>
                    <span className={styles.brandText}>{siteSettings.brandName}</span>
                    {siteSettings.logoText && (
                      <span className={styles.brandSubtext}>{siteSettings.logoText}</span>
                    )}
                  </div>
                </>
              ) : (
                <>
                  <span className={styles.brandIcon}>{siteSettings.logoIcon}</span>
                  <div className={styles.brandTextContainer}>
                    <span className={styles.brandText}>{siteSettings.brandName}</span>
                    {siteSettings.logoText && (
                      <span className={styles.brandSubtext}>{siteSettings.logoText}</span>
                    )}
                  </div>
                </>
              )}
            </>
          )}
        </button>

        {/* Desktop Navigation Links */}
        <ul className={styles.navLinks}>
          {categories.map((category) => (
            <li key={category.id}>
              <button
                onClick={() => scrollToCategory(category.id)}
                className={styles.navLink}
                aria-label={`Go to ${category.name} section`}
              >
                <span className={styles.navLinkChinese}>{category.name}</span>
                {category.englishName && <span className={styles.navLinkEnglish}>{category.englishName}</span>}
              </button>
            </li>
          ))}
        </ul>

        {/* Mobile Menu Toggle */}
        <button
          className={styles.menuToggle}
          onClick={toggleMenu}
          aria-label="切換選單"
          aria-expanded={isMenuOpen}
        >
          <span className={`${styles.hamburger} ${isMenuOpen ? styles.open : ''}`}>
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
      </div>

      {/* Mobile Menu Dropdown */}
      <div className={`${styles.mobileMenu} ${isMenuOpen ? styles.open : ''}`}>
        <ul className={styles.mobileNavLinks}>
          <li>
            <button
              onClick={scrollToTop}
              className={styles.mobileNavLink}
            >
              🏠 首頁
            </button>
          </li>
          {categories.map((category) => (
            <li key={category.id}>
              <button
                onClick={() => scrollToCategory(category.id)}
                className={styles.mobileNavLink}
              >
                {category.name}
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* Overlay for mobile menu */}
      {isMenuOpen && (
        <div
          className={styles.overlay}
          onClick={() => setIsMenuOpen(false)}
          aria-hidden="true"
        />
      )}
    </nav>
  );
}

Navigation.propTypes = {
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default Navigation;
