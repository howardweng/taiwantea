/**
 * ProductCard - Displays a single tea product
 *
 * Features:
 * - Product image with alt text
 * - Product name, category, description
 * - Price formatting
 * - Stock status indicator
 * - Responsive design
 * - Accessibility (ARIA labels, semantic HTML)
 */

import PropTypes from 'prop-types';
import styles from './ProductCard.module.css';

function ProductCard({ product }) {
  const { id, name, category, description, price, imageUrl, thumbnailUrl, inStock } = product;

  // Use thumbnail if available, fallback to main image
  const displayImage = thumbnailUrl || imageUrl;

  // Format price to 2 decimal places
  const formattedPrice = `NT$${price.toFixed(2)}`;

  return (
    <article
      className={`${styles.card} ${!inStock ? styles.outOfStock : ''}`}
      aria-label={`${name} - ${formattedPrice}`}
    >
      <div className={styles.imageContainer}>
        <img
          src={displayImage}
          alt={name}
          className={styles.image}
          loading="lazy"
        />
        {!inStock && (
          <div className={styles.stockBadge} aria-label="Out of stock">
            Out of Stock
          </div>
        )}
      </div>

      <div className={styles.content}>
        <h3 className={styles.name}>{name}</h3>

        <p className={styles.category} aria-label={`Category: ${category}`}>
          {category}
        </p>

        <p className={styles.description}>{description}</p>

        <div className={styles.footer}>
          <span className={styles.price} aria-label={`Price: ${formattedPrice}`}>
            {formattedPrice}
          </span>

          {inStock ? (
            <span className={styles.stockStatus} aria-label="In stock">
              In Stock
            </span>
          ) : (
            <span className={`${styles.stockStatus} ${styles.unavailable}`} aria-label="Out of stock">
              Unavailable
            </span>
          )}
        </div>
      </div>
    </article>
  );
}

ProductCard.propTypes = {
  product: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    category: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    price: PropTypes.number.isRequired,
    imageUrl: PropTypes.string.isRequired,
    thumbnailUrl: PropTypes.string,
    inStock: PropTypes.bool.isRequired,
  }).isRequired,
};

export default ProductCard;
