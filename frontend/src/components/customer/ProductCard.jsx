/**
 * ProductCard - Displays a single tea product
 *
 * Features:
 * - Product image with alt text (click to view full-size)
 * - Product name, category, description
 * - Price formatting
 * - Stock status indicator
 * - Responsive design
 * - Accessibility (ARIA labels, semantic HTML)
 * - Image modal for full-size viewing
 */

import { useState } from 'react';
import PropTypes from 'prop-types';
import styles from './ProductCard.module.css';
import ImageModal from './ImageModal';
import ShopeeIcon from './ShopeeIcon';
import { getImageUrl } from '../../utils/imageUtils';

function ProductCard({ product, shopeeStoreUrl = 'https://shopee.tw/' }) {
  const { id, name, category, description, price, imageUrl, thumbnailUrl, inStock, badge } = product;
  const [showModal, setShowModal] = useState(false);

  // Use thumbnail for card display, full image for modal (with full backend URL)
  const displayImage = getImageUrl(thumbnailUrl || imageUrl);
  const fullImageUrl = getImageUrl(imageUrl);

  // Format price to 2 decimal places
  const formattedPrice = `NT$${price.toFixed(2)}`;

  // Translate badge to Chinese
  const getBadgeText = (badge) => {
    const badgeMap = {
      'HOT': '熱銷',
      'NEW': '新品',
      'SALE': '特價'
    };
    return badgeMap[badge] || badge;
  };

  const handleImageClick = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <>
      <article
        className={`${styles.card} ${!inStock ? styles.outOfStock : ''}`}
        aria-label={`${name} - ${formattedPrice}`}
      >
        <div
          className={styles.imageContainer}
          onClick={handleImageClick}
          onKeyPress={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              handleImageClick();
            }
          }}
          role="button"
          tabIndex={0}
          aria-label={`Click to view full-size image of ${name}`}
        >
          <img
            src={displayImage}
            alt={name}
            className={styles.image}
            loading="lazy"
          />
          <div className={styles.imageOverlay}>
            <span className={styles.zoomIcon}>🔍</span>
          </div>
          {/* Custom badge from admin (e.g., "HOT", "NEW", "SALE") */}
          {badge && inStock && (
            <div className={styles.productBadge} aria-label={`Badge: ${getBadgeText(badge)}`}>
              {getBadgeText(badge)}
            </div>
          )}
          {/* Out of stock badge takes priority */}
          {!inStock && (
            <div className={styles.stockBadge} aria-label="缺貨">
              缺貨
            </div>
          )}
        </div>

      <div className={styles.content}>
        <h3 className={styles.name} title={name}>{name}</h3>

        <p className={styles.category} aria-label={`Category: ${category}`} title={category}>
          {category}
        </p>

        <p className={styles.description} title={description}>{description}</p>

        <div className={styles.footer}>
          <span className={styles.price} aria-label={`Price: ${formattedPrice}`}>
            {formattedPrice}
          </span>

          {inStock && (
            <a
              href={shopeeStoreUrl || "https://shopee.tw/"}
              target="_blank"
              rel="noopener noreferrer"
              className={styles.shopeeButton}
              aria-label={`在蝦皮購買 ${name}`}
              title="在蝦皮購買"
              onClick={(e) => {
                e.stopPropagation();
              }}
            >
              <ShopeeIcon size={36} className={styles.shopeeIcon} />
            </a>
          )}
        </div>
      </div>
      </article>

      {showModal && (
        <ImageModal
          imageUrl={fullImageUrl}
          alt={name}
          onClose={handleCloseModal}
        />
      )}
    </>
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
    smImageUrl: PropTypes.string,  // Small image URL from media server
    inStock: PropTypes.bool.isRequired,
    badge: PropTypes.string,  // Optional badge text
  }).isRequired,
  shopeeStoreUrl: PropTypes.string,
};

export default ProductCard;
