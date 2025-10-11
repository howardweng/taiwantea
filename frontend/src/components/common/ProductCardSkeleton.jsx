/**
 * ProductCardSkeleton - Loading placeholder for ProductCard
 *
 * Provides visual feedback while products are loading
 */

import styles from './ProductCardSkeleton.module.css';

function ProductCardSkeleton() {
  return (
    <div className={styles.skeleton} aria-busy="true" aria-label="Loading product">
      <div className={styles.imageContainer}>
        <div className={styles.imagePlaceholder}></div>
      </div>
      <div className={styles.content}>
        <div className={styles.namePlaceholder}></div>
        <div className={styles.categoryPlaceholder}></div>
        <div className={styles.descriptionPlaceholder}></div>
        <div className={styles.descriptionPlaceholder}></div>
        <div className={styles.footer}>
          <div className={styles.pricePlaceholder}></div>
          <div className={styles.stockPlaceholder}></div>
        </div>
      </div>
    </div>
  );
}

export default ProductCardSkeleton;
