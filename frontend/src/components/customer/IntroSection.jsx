/**
 * IntroSection Component
 *
 * Introduction section with HTML content and CTA button (content from backend)
 */

import { useState, useEffect } from 'react';
import api from '../../services/api';
import styles from './IntroSection.module.css';

function IntroSection() {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchContent();
  }, []);

  const fetchContent = async () => {
    try {
      const response = await api.get('/api/intro-section');
      setContent(response.data);
    } catch (error) {
      console.error('Failed to fetch intro section:', error);
      // Don't show error to user, just don't render the section
    } finally {
      setLoading(false);
    }
  };

  const handleButtonClick = () => {
    if (content?.buttonLink) {
      window.open(content.buttonLink, '_blank', 'noopener,noreferrer');
    }
  };

  // Don't render if loading, no content, or inactive
  if (loading || !content || !content.active) {
    return null;
  }

  return (
    <section className={styles.introSection}>
      <div className={styles.content}>
        {/* Render HTML content from backend */}
        <div
          className={styles.htmlContent}
          dangerouslySetInnerHTML={{ __html: content.htmlContent }}
        />

        <button
          className={styles.ctaButton}
          onClick={handleButtonClick}
          aria-label={content.buttonText}
        >
          <svg className={styles.shopeeIcon} viewBox="0 0 24 24" fill="currentColor">
            <path d="M19.5 7h-15A1.5 1.5 0 003 8.5v10A1.5 1.5 0 004.5 20h15a1.5 1.5 0 001.5-1.5v-10A1.5 1.5 0 0019.5 7zM12 2.5c-1.5 0-2.7 1.2-2.7 2.7 0 1.5 1.2 2.7 2.7 2.7s2.7-1.2 2.7-2.7c0-1.5-1.2-2.7-2.7-2.7z"/>
          </svg>
          <span>{content.buttonText}</span>
          <span className={styles.arrow}>→</span>
        </button>
      </div>
    </section>
  );
}

export default IntroSection;
