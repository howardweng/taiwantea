/**
 * ImageModal - Full-screen modal to view product images at full resolution
 *
 * Features:
 * - Click outside or ESC key to close
 * - Shows full-size image
 * - Smooth fade-in animation
 * - Prevents body scroll when open
 * - Accessible keyboard navigation
 */

import { useEffect } from 'react';
import PropTypes from 'prop-types';
import styles from './ImageModal.module.css';

function ImageModal({ imageUrl, alt, onClose }) {
  useEffect(() => {
    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';

    // Handle ESC key to close
    const handleEscKey = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscKey);

    return () => {
      document.body.style.overflow = 'unset';
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [onClose]);

  // Close on backdrop click
  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      className={styles.backdrop}
      onClick={handleBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-label="Product image viewer"
    >
      <div className={styles.container}>
        <button
          className={styles.closeButton}
          onClick={onClose}
          aria-label="Close image viewer"
          type="button"
        >
          ✕
        </button>

        <img
          src={imageUrl}
          alt={alt}
          className={styles.image}
        />

        <p className={styles.hint}>
          Click outside or press ESC to close
        </p>
      </div>
    </div>
  );
}

ImageModal.propTypes = {
  imageUrl: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default ImageModal;
