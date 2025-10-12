/**
 * CategorySection - Displays products grouped by category
 *
 * Features:
 * - Category header with name and description
 * - Responsive product grid
 * - Smooth scroll anchor for navigation
 * - Accessible section structure
 */

import PropTypes from 'prop-types';
import ProductCard from './ProductCard';
import styles from './CategorySection.module.css';

function CategorySection({ category, products, isAlternate }) {
  const { id, name, description, imageUrl } = category;

  // Create anchor ID from category ID (e.g., "green-tea")
  const anchorId = id;

  return (
    <section
      id={anchorId}
      className={`${styles.section} ${isAlternate ? styles.alternate : ''}`}
      aria-labelledby={`${anchorId}-heading`}
    >
      <div className={styles.innerContainer}>
        <div className={styles.header}>
          {imageUrl && (
            <div className={styles.headerImageContainer}>
              <img
                src={imageUrl}
                alt={`${name} category`}
                className={styles.headerImage}
              />
            </div>
          )}

          <div className={styles.headerContent}>
            <h2 id={`${anchorId}-heading`} className={styles.title}>
              {name}
            </h2>

            {description && (
              <p className={styles.description}>{description}</p>
            )}
          </div>
        </div>

        {products.length > 0 ? (
          <div className={styles.grid} role="list">
            {products.map((product) => (
              <div key={product.id} role="listitem">
                <ProductCard product={product} />
              </div>
            ))}
          </div>
        ) : (
          <div className={styles.empty} role="status">
            <p>No products available in this category.</p>
          </div>
        )}
      </div>
    </section>
  );
}

CategorySection.propTypes = {
  category: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    description: PropTypes.string,
    imageUrl: PropTypes.string,
  }).isRequired,
  products: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      category: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
      price: PropTypes.number.isRequired,
      imageUrl: PropTypes.string.isRequired,
      thumbnailUrl: PropTypes.string,
      inStock: PropTypes.bool.isRequired,
    })
  ).isRequired,
  isAlternate: PropTypes.bool,
};

CategorySection.defaultProps = {
  isAlternate: false,
};

export default CategorySection;
