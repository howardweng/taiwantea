/**
 * ImageGallery Component
 *
 * Image gallery with main display and thumbnail navigation
 */

import { useState } from 'react';
import styles from './ImageGallery.module.css';

function ImageGallery({ images = [], productName = '' }) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  // Return placeholder if no images
  if (!images || images.length === 0) {
    return (
      <div className={styles.container}>
        <div className={styles.placeholder}>
          <span className={styles.placeholderIcon}>🍵</span>
          <p>No image available</p>
        </div>
      </div>
    );
  }

  const currentImage = images[selectedIndex];

  return (
    <div className={styles.container}>
      {/* Main Image Display */}
      <div className={styles.mainImageContainer}>
        <img
          src={currentImage.url}
          alt={currentImage.alt || `${productName} - 圖片 ${selectedIndex + 1}`}
          className={styles.mainImage}
        />
      </div>

      {/* Thumbnail Navigation */}
      {images.length > 1 && (
        <div className={styles.thumbnailContainer}>
          <div className={styles.thumbnailGrid}>
            {images.map((image, index) => (
              <button
                key={index}
                type="button"
                onClick={() => setSelectedIndex(index)}
                className={`${styles.thumbnail} ${
                  index === selectedIndex ? styles.thumbnailActive : ''
                }`}
                aria-label={`View image ${index + 1}`}
              >
                <img
                  src={image.thumbnailUrl || image.url}
                  alt={image.alt || `${productName} 縮圖 ${index + 1}`}
                  className={styles.thumbnailImage}
                />
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Image Counter */}
      {images.length > 1 && (
        <div className={styles.imageCounter}>
          {selectedIndex + 1} / {images.length}
        </div>
      )}
    </div>
  );
}

export default ImageGallery;
