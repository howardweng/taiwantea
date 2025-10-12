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

function ProductGrid({ categories, products, loading, error, shopeeStoreUrl }) {
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
          <h2>目前無可用分類</h2>
          <p>請稍後再查看我們的茶品選擇。</p>
        </div>
      </div>
    );
  }

  // Filter only visible products (inStock = true) and group by category
  const productsByCategory = products
    .filter(product => product.inStock)
    .reduce((acc, product) => {
      const categoryId = product.category;
      if (!acc[categoryId]) {
        acc[categoryId] = [];
      }
      acc[categoryId].push(product);
      return acc;
    }, {});

  return (
    <div id="products" className={styles.container}>
      {categories.map((category, index) => {
        const categoryProducts = productsByCategory[category.id] || [];

        return (
          <CategorySection
            key={category.id}
            category={category}
            products={categoryProducts}
            isAlternate={index % 2 === 0}
            shopeeStoreUrl={shopeeStoreUrl}
          />
        );
      })}
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
  shopeeStoreUrl: PropTypes.string,
};

ProductGrid.defaultProps = {
  categories: [],
  products: [],
  loading: false,
  error: null,
  shopeeStoreUrl: 'https://shopee.tw/',
};

export default ProductGrid;
