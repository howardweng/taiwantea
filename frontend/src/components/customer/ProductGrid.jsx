/**
 * ProductGrid - Main container for all category sections
 *
 * Features:
 * - Groups products by category
 * - Renders CategorySection components
 * - Loading and error states
 * - Responsive container
 */

import PropTypes from 'prop-types';
import CategorySection from './CategorySection';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';
import styles from './ProductGrid.module.css';

function ProductGrid({ categories, products, loading, error }) {
  if (loading) {
    return (
      <div className={styles.container}>
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <ErrorMessage message={error} />
      </div>
    );
  }

  if (!categories || categories.length === 0) {
    return (
      <div className={styles.container}>
        <div className={styles.empty}>
          <h2>No Categories Available</h2>
          <p>Please check back later for our tea selection.</p>
        </div>
      </div>
    );
  }

  // Group products by category
  const productsByCategory = products.reduce((acc, product) => {
    const categoryId = product.category;
    if (!acc[categoryId]) {
      acc[categoryId] = [];
    }
    acc[categoryId].push(product);
    return acc;
  }, {});

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        {categories.map((category) => {
          const categoryProducts = productsByCategory[category.id] || [];

          return (
            <CategorySection
              key={category.id}
              category={category}
              products={categoryProducts}
            />
          );
        })}
      </main>
    </div>
  );
}

ProductGrid.propTypes = {
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      description: PropTypes.string,
      imageUrl: PropTypes.string,
    })
  ),
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
  ),
  loading: PropTypes.bool,
  error: PropTypes.string,
};

ProductGrid.defaultProps = {
  categories: [],
  products: [],
  loading: false,
  error: null,
};

export default ProductGrid;
