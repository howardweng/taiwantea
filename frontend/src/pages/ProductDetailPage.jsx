/**
 * Product Detail Page
 *
 * Displays full product information with image gallery
 */

import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import DOMPurify from 'dompurify';
import ImageGallery from '../components/customer/ImageGallery';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Navigation from '../components/layout/Navigation';
import { getCategories } from '../services/productService';
import styles from './ProductDetailPage.module.css';

function ProductDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProduct();
    fetchCategories();
  }, [id]);

  // Add structured data (Schema.org) for SEO
  useEffect(() => {
    if (!product) return;

    // Create structured data for product
    const structuredData = {
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": product.name,
      "image": product.images || [],
      "description": product.description || product.name,
      "brand": {
        "@type": "Brand",
        "name": "台灣茗茶大師 TeaMaster"
      },
      "offers": {
        "@type": "Offer",
        "url": `https://taiwantea.frrut.com/products/${product._id}`,
        "priceCurrency": "TWD",
        "price": product.price,
        "availability": product.inStock
          ? "https://schema.org/InStock"
          : "https://schema.org/OutOfStock"
      }
    };

    // Create script tag and add to head
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(structuredData);
    script.id = 'product-structured-data';
    document.head.appendChild(script);

    // Update page title and meta description
    document.title = `${product.name} - 台灣茗茶大師 TeaMaster`;

    // Update or create meta description
    let metaDescription = document.querySelector('meta[name="description"]');
    if (!metaDescription) {
      metaDescription = document.createElement('meta');
      metaDescription.name = 'description';
      document.head.appendChild(metaDescription);
    }
    metaDescription.content = `${product.description || product.name} - NT$ ${product.price.toLocaleString()}。100%台灣高山茶葉，手工採摘，天然無添加。`;

    // Cleanup function to remove script when component unmounts
    return () => {
      const oldScript = document.getElementById('product-structured-data');
      if (oldScript) {
        document.head.removeChild(oldScript);
      }
      // Reset title to default
      document.title = '台灣茗茶大師 TeaMaster - 精選台灣高山茶｜烏龍茶、紅茶、綠茶';
    };
  }, [product]);

  const fetchCategories = async () => {
    try {
      const categoriesData = await getCategories();
      setCategories(categoriesData || []);
    } catch (err) {
      console.error('Error fetching categories:', err);
      setCategories([]);
    }
  };

  const fetchProduct = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/products/${id}`);

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Product not found');
        }
        throw new Error('Failed to load product');
      }

      const data = await response.json();
      setProduct(data);
    } catch (err) {
      console.error('Error fetching product:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.errorContainer}>
        <div className={styles.errorCard}>
          <h2>Oops!</h2>
          <p>{error}</p>
          <button onClick={() => navigate('/')} className={styles.backButton}>
            ← Back to Home
          </button>
        </div>
      </div>
    );
  }

  if (!product) {
    return null;
  }

  const badgeText = {
    HOT: '熱門',
    NEW: '新品',
    SALE: '特價'
  };

  return (
    <>
      {/* Navigation Header */}
      <Navigation categories={categories} />

      <div className={styles.container}>
        {/* Breadcrumb */}
        <nav className={styles.breadcrumb} aria-label="Breadcrumb">
        <Link to="/" className={styles.breadcrumbLink}>
          首頁
        </Link>
        <span className={styles.breadcrumbSeparator}>/</span>
        <span className={styles.breadcrumbCurrent}>{product.name}</span>
      </nav>

      {/* Product Content */}
      <div className={styles.productContent}>
        {/* Left Column - Image Gallery */}
        <div className={styles.imageColumn}>
          <ImageGallery images={product.images} productName={product.name} />
        </div>

        {/* Right Column - Product Info */}
        <div className={styles.infoColumn}>
          {/* Product Name */}
          <h1 className={styles.productName}>
            {product.name}
            {product.badge && (
              <span className={`${styles.badge} ${styles[`badge${product.badge}`]}`}>
                {badgeText[product.badge] || product.badge}
              </span>
            )}
          </h1>

          {/* English Name */}
          {product.englishName && (
            <p className={styles.englishName}>{product.englishName}</p>
          )}

          {/* Price */}
          <div className={styles.priceSection}>
            <span className={styles.priceLabel}>價格：</span>
            <span className={styles.price}>NT$ {product.price.toLocaleString()}</span>
          </div>

          {/* Divider */}
          <hr className={styles.divider} />

          {/* Description */}
          <div className={styles.descriptionSection}>
            <h2 className={styles.sectionTitle}>商品描述</h2>
            <p className={styles.description}>{product.description}</p>
          </div>

          {/* Stock Status */}
          <div className={styles.stockSection}>
            {product.inStock ? (
              <span className={styles.inStock}>✓ 現貨供應中</span>
            ) : (
              <span className={styles.outOfStock}>✗ 目前缺貨</span>
            )}
          </div>

          {/* Action Buttons */}
          <div className={styles.actions}>
            <button onClick={() => navigate('/')} className={styles.backButton}>
              ← 返回商品列表
            </button>
          </div>
        </div>
      </div>

      {/* Rich Text Detail Content - Full Width Below Product Info */}
      {product.detailContent && product.detailContent.trim() !== '' && product.detailContent !== '<p><br></p>' && (
        <div className={styles.detailContentSection}>
          <h2 className={styles.sectionTitle}>詳細介紹</h2>
          <div
            className={styles.richTextContent}
            dangerouslySetInnerHTML={{
              __html: DOMPurify.sanitize(product.detailContent, {
                ALLOWED_TAGS: ['h2', 'h3', 'p', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'a', 'img', 'br'],
                ALLOWED_ATTR: ['href', 'src', 'alt', 'target', 'rel', 'style', 'class']
              })
            }}
          />
        </div>
      )}
      </div>
    </>
  );
}

export default ProductDetailPage;
