/**
 * Product Form Component
 *
 * Form for creating and editing products
 */

import { useState, useEffect, useCallback } from 'react';
import ImageUpload from './ImageUpload';
import styles from './ProductForm.module.css';

function ProductForm({ product, categories, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: '',
    englishName: '',
    category: '',
    description: '',
    price: '',
    imageUrl: '',
    thumbnailUrl: '',
    inStock: true,
    displayOrder: 999,
    badge: '',  // Badge text field
    images: [],  // Multi-image support (max 6)
    detailContent: '',  // Rich text HTML content
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [uploadingImage, setUploadingImage] = useState({ url: '', thumbnailUrl: '' });

  // Populate form if editing existing product
  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name || '',
        englishName: product.englishName || '',
        category: product.category || '',
        description: product.description || '',
        price: product.price || '',
        imageUrl: product.imageUrl || '',
        thumbnailUrl: product.thumbnailUrl || '',
        inStock: product.inStock ?? true,
        displayOrder: product.displayOrder || 999,
        badge: product.badge || '',  // Load existing badge
        images: product.images || [],  // Load existing images array
        detailContent: product.detailContent || '',  // Load rich text content
      });
    }
  }, [product]);

  // Handle image upload completion
  useEffect(() => {
    if (uploadingImage.url && uploadingImage.thumbnailUrl) {
      handleAddImage(uploadingImage.url, uploadingImage.thumbnailUrl);
      setUploadingImage({ url: '', thumbnailUrl: '' }); // Reset
    }
  }, [uploadingImage]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));

    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  // Multi-image management functions
  const handleAddImage = useCallback((url, thumbnailUrl) => {
    setFormData(prev => {
      if (prev.images.length >= 6) {
        alert('最多只能上傳 6 張圖片');
        return prev;
      }

      const newImage = {
        url,
        thumbnailUrl: thumbnailUrl || null,
        displayOrder: prev.images.length,
        alt: `${prev.name || '商品'} 圖片 ${prev.images.length + 1}`
      };

      const newImages = [...prev.images, newImage];
      const updatedData = {
        ...prev,
        images: newImages
      };

      // Update main image if this is the first image
      if (prev.images.length === 0) {
        updatedData.imageUrl = url;
        updatedData.thumbnailUrl = thumbnailUrl || null;
      }

      return updatedData;
    });
  }, []);

  const handleRemoveImage = (index) => {
    const newImages = formData.images.filter((_, i) => i !== index);
    // Re-index displayOrder
    const reindexedImages = newImages.map((img, i) => ({
      ...img,
      displayOrder: i
    }));

    setFormData(prev => ({
      ...prev,
      images: reindexedImages
    }));

    // Update main image if first image was removed
    if (index === 0 && reindexedImages.length > 0) {
      setFormData(prev => ({
        ...prev,
        imageUrl: reindexedImages[0].url,
        thumbnailUrl: reindexedImages[0].thumbnailUrl || null
      }));
    } else if (reindexedImages.length === 0) {
      setFormData(prev => ({
        ...prev,
        imageUrl: '',
        thumbnailUrl: ''
      }));
    }
  };

  const handleMoveImage = (fromIndex, toIndex) => {
    if (toIndex < 0 || toIndex >= formData.images.length) return;

    const newImages = [...formData.images];
    const [movedImage] = newImages.splice(fromIndex, 1);
    newImages.splice(toIndex, 0, movedImage);

    // Re-index displayOrder
    const reindexedImages = newImages.map((img, i) => ({
      ...img,
      displayOrder: i
    }));

    setFormData(prev => ({
      ...prev,
      images: reindexedImages
    }));

    // Update main image if first image changed
    if (fromIndex === 0 || toIndex === 0) {
      setFormData(prev => ({
        ...prev,
        imageUrl: reindexedImages[0].url,
        thumbnailUrl: reindexedImages[0].thumbnailUrl || null
      }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Product name is required';
    }

    if (!formData.category) {
      newErrors.category = 'Category is required';
    }

    if (!formData.description.trim() || formData.description.length < 10) {
      newErrors.description = 'Description must be at least 10 characters';
    }

    if (!formData.price || parseFloat(formData.price) <= 0) {
      newErrors.price = 'Price must be greater than 0';
    }

    if (!formData.images || formData.images.length === 0) {
      newErrors.imageUrl = '請至少上傳一張商品圖片';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);

    try {
      // Convert price to number
      const submitData = {
        ...formData,
        price: parseFloat(formData.price),
        displayOrder: parseInt(formData.displayOrder) || 999,
      };

      await onSubmit(submitData);
    } catch (error) {
      console.error('Form submission error:', error);
      setErrors({ submit: error.message || 'Failed to save product' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.formContainer}>
      <form onSubmit={handleSubmit} className={styles.form}>
        <h2 className={styles.formTitle}>
          {product ? '編輯商品' : '新增商品'}
        </h2>

        {errors.submit && (
          <div className={styles.errorMessage} role="alert">
            {errors.submit}
          </div>
        )}

        <div className={styles.formGroup}>
          <label htmlFor="name" className={styles.label}>
            商品名稱（中文）*
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={`${styles.input} ${errors.name ? styles.inputError : ''}`}
            disabled={isSubmitting}
            placeholder="例如: 龍井綠茶(珍品量少)"
          />
          {errors.name && <span className={styles.fieldError}>{errors.name}</span>}
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="englishName" className={styles.label}>
            English Name (Optional)
          </label>
          <input
            type="text"
            id="englishName"
            name="englishName"
            value={formData.englishName}
            onChange={handleChange}
            className={styles.input}
            disabled={isSubmitting}
            placeholder="e.g., Taiwan Longjing Green Tea"
          />
          <small className={styles.helpText}>
            English translation of the product name (optional)
          </small>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="category" className={styles.label}>
            商品分類 *
          </label>
          <select
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
            className={`${styles.select} ${errors.category ? styles.inputError : ''}`}
            disabled={isSubmitting}
          >
            <option value="">請選擇分類</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
          {errors.category && <span className={styles.fieldError}>{errors.category}</span>}
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="description" className={styles.label}>
            商品描述 *
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={4}
            className={`${styles.textarea} ${errors.description ? styles.inputError : ''}`}
            disabled={isSubmitting}
          />
          {errors.description && <span className={styles.fieldError}>{errors.description}</span>}
        </div>

        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label htmlFor="price" className={styles.label}>
              價格 (NT$) *
            </label>
            <input
              type="number"
              id="price"
              name="price"
              value={formData.price}
              onChange={handleChange}
              step="0.01"
              min="0"
              className={`${styles.input} ${errors.price ? styles.inputError : ''}`}
              disabled={isSubmitting}
            />
            {errors.price && <span className={styles.fieldError}>{errors.price}</span>}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="displayOrder" className={styles.label}>
              顯示順序
            </label>
            <input
              type="number"
              id="displayOrder"
              name="displayOrder"
              value={formData.displayOrder}
              onChange={handleChange}
              min="0"
              className={styles.input}
              disabled={isSubmitting}
            />
          </div>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="badge" className={styles.label}>
            標籤 (選填)
          </label>
          <select
            id="badge"
            name="badge"
            value={formData.badge || ''}
            onChange={handleChange}
            className={styles.select}
            disabled={isSubmitting}
          >
            <option value="">無標籤</option>
            <option value="HOT">HOT 熱門</option>
            <option value="NEW">NEW 新品</option>
            <option value="SALE">SALE 特價</option>
          </select>
          <span className={styles.helpText}>
            選擇要在商品卡片上顯示的標籤
          </span>
        </div>

        {/* Multi-Image Management Section */}
        <div className={styles.formGroup}>
          <label className={styles.label}>
            商品圖片 * (最多 6 張)
          </label>

          <div className={styles.imagesContainer}>
            {/* Existing Images Display */}
            {formData.images.length > 0 && (
              <div className={styles.imagesGrid}>
                {formData.images.map((image, index) => (
                  <div key={index} className={styles.imageItem}>
                    <img
                      src={image.thumbnailUrl || image.url}
                      alt={image.alt || `圖片 ${index + 1}`}
                      className={styles.imagePreview}
                    />
                    <div className={styles.imageOverlay}>
                      <span className={styles.imageIndex}>
                        {index === 0 ? '主圖' : `${index + 1}`}
                      </span>
                    </div>
                    <div className={styles.imageActions}>
                      {index > 0 && (
                        <button
                          type="button"
                          onClick={() => handleMoveImage(index, index - 1)}
                          className={styles.iconButton}
                          title="往前移"
                        >
                          ←
                        </button>
                      )}
                      {index < formData.images.length - 1 && (
                        <button
                          type="button"
                          onClick={() => handleMoveImage(index, index + 1)}
                          className={styles.iconButton}
                          title="往後移"
                        >
                          →
                        </button>
                      )}
                      <button
                        type="button"
                        onClick={() => handleRemoveImage(index)}
                        className={styles.deleteButton}
                        title="刪除"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                ))}

                {/* Add New Image Card - Inside Grid */}
                {formData.images.length < 6 && (
                  <div className={styles.uploadCard}>
                    <ImageUpload
                      key={formData.images.length}
                      label=""
                      value=""
                      onChange={(url) => {
                        setUploadingImage(prev => ({ ...prev, url }));
                      }}
                      onThumbnailChange={(thumbUrl) => {
                        setUploadingImage(prev => ({ ...prev, thumbnailUrl: thumbUrl }));
                      }}
                      placeholder={`➕ 新增\n第 ${formData.images.length + 1} 張圖片`}
                      hideUrlInput={true}
                    />
                  </div>
                )}
              </div>
            )}

            {/* Show upload area when no images */}
            {formData.images.length === 0 && (
              <ImageUpload
                label="上傳第一張圖片（主圖）"
                value=""
                onChange={(url) => {
                  setUploadingImage(prev => ({ ...prev, url }));
                }}
                onThumbnailChange={(thumbUrl) => {
                  setUploadingImage(prev => ({ ...prev, thumbnailUrl: thumbUrl }));
                }}
                placeholder="點擊上傳圖片 (縮圖將自動生成)"
                hideUrlInput={true}
              />
            )}
          </div>

          {errors.imageUrl && <span className={styles.fieldError}>{errors.imageUrl}</span>}

          <p className={styles.helpText}>
            ℹ️ 第一張圖片將作為主圖顯示在商品列表中。可上傳最多 6 張圖片。
          </p>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              name="inStock"
              checked={formData.inStock}
              onChange={handleChange}
              className={styles.checkbox}
              disabled={isSubmitting}
            />
            <span>顯示於首頁</span>
          </label>
        </div>

        <div className={styles.formActions}>
          <button
            type="button"
            onClick={onCancel}
            className={styles.cancelButton}
            disabled={isSubmitting}
          >
            取消
          </button>
          <button type="submit" className={styles.submitButton} disabled={isSubmitting}>
            {isSubmitting ? '儲存中...' : product ? '更新商品' : '建立商品'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default ProductForm;
