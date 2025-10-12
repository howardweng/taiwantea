/**
 * HeroCarousel - Full-screen image carousel
 *
 * Features:
 * - Full-screen immersive slides
 * - Smooth fade transitions
 * - Auto-play with pause on hover
 * - Navigation dots and arrows
 * - Responsive design
 */

import { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import styles from './HeroCarousel.module.css';

function HeroCarousel({ slides, autoPlayInterval = 5000 }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Go to next slide
  const goToNext = useCallback(() => {
    if (isTransitioning) return;
    setIsTransitioning(true);
    setCurrentIndex((prevIndex) => (prevIndex + 1) % slides.length);
    setTimeout(() => setIsTransitioning(false), 1000);
  }, [slides.length, isTransitioning]);

  // Go to previous slide
  const goToPrevious = useCallback(() => {
    if (isTransitioning) return;
    setIsTransitioning(true);
    setCurrentIndex((prevIndex) =>
      prevIndex === 0 ? slides.length - 1 : prevIndex - 1
    );
    setTimeout(() => setIsTransitioning(false), 1000);
  }, [slides.length, isTransitioning]);

  // Go to specific slide
  const goToSlide = (index) => {
    if (isTransitioning || index === currentIndex) return;
    setIsTransitioning(true);
    setCurrentIndex(index);
    setTimeout(() => setIsTransitioning(false), 1000);
  };

  // Auto-play
  useEffect(() => {
    if (isPaused || slides.length <= 1) return;

    const interval = setInterval(goToNext, autoPlayInterval);
    return () => clearInterval(interval);
  }, [isPaused, slides.length, autoPlayInterval, goToNext]);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowLeft') goToPrevious();
      if (e.key === 'ArrowRight') goToNext();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [goToNext, goToPrevious]);

  if (!slides || slides.length === 0) {
    return null;
  }

  return (
    <div
      className={styles.carousel}
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
      role="region"
      aria-label="圖片輪播"
    >
      {/* Slides */}
      <div className={styles.slidesContainer}>
        {slides.map((slide, index) => (
          <div
            key={index}
            className={`${styles.slide} ${
              index === currentIndex ? styles.active : ''
            }`}
            style={{ backgroundImage: `url(${slide.image})` }}
            aria-hidden={index !== currentIndex}
          >
            <div className={styles.overlay} />
            <div className={styles.content}>
              {slide.title && (
                <h2 className={styles.title}>{slide.title}</h2>
              )}
              {slide.subtitle && (
                <p className={styles.subtitle}>{slide.subtitle}</p>
              )}
              {slide.cta && (
                <button
                  className={styles.ctaButton}
                  onClick={slide.cta.onClick}
                  aria-label={slide.cta.label}
                >
                  {slide.cta.label}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Navigation Arrows */}
      {slides.length > 1 && (
        <>
          <button
            className={`${styles.arrow} ${styles.arrowLeft}`}
            onClick={goToPrevious}
            aria-label="上一張"
            disabled={isTransitioning}
          >
            ‹
          </button>
          <button
            className={`${styles.arrow} ${styles.arrowRight}`}
            onClick={goToNext}
            aria-label="下一張"
            disabled={isTransitioning}
          >
            ›
          </button>
        </>
      )}

      {/* Navigation Dots */}
      {slides.length > 1 && (
        <div className={styles.dots}>
          {slides.map((_, index) => (
            <button
              key={index}
              className={`${styles.dot} ${
                index === currentIndex ? styles.dotActive : ''
              }`}
              onClick={() => goToSlide(index)}
              aria-label={`前往第 ${index + 1} 張`}
              aria-current={index === currentIndex}
              disabled={isTransitioning}
            />
          ))}
        </div>
      )}

      {/* Pause/Play indicator (optional) */}
      {isPaused && (
        <div className={styles.pauseIndicator}>
          ⏸
        </div>
      )}
    </div>
  );
}

HeroCarousel.propTypes = {
  slides: PropTypes.arrayOf(
    PropTypes.shape({
      image: PropTypes.string.isRequired,
      title: PropTypes.string,
      subtitle: PropTypes.string,
      cta: PropTypes.shape({
        label: PropTypes.string.isRequired,
        onClick: PropTypes.func.isRequired,
      }),
    })
  ).isRequired,
  autoPlayInterval: PropTypes.number,
};

export default HeroCarousel;
