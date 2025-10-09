/**
 * Product Form Component
 *
 * Form for creating and editing products
 */

import { useState, useEffect } from 'react';
import ImageUpload from './ImageUpload';
import styles from './ProductForm.module.css';

function ProductForm({ product, categories, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    description: '',
    price: '',
    imageUrl: '',
    thumbnailUrl: '',
    inStock: true,
    displayOrder: 999,
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Populate form if editing existing product
  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name || '',
        category: product.category || '',
        description: product.description || '',
        price: product.price || '',
        imageUrl: product.imageUrl || '',
        thumbnailUrl: product.thumbnailUrl || '',
        inStock: product.inStock ?? true,
        displayOrder: product.displayOrder || 999,
      });
    }
  }, [product]);

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

    if (!formData.imageUrl.trim()) {
      newErrors.imageUrl = 'Image URL is required';
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
          {product ? 'Edit Product' : 'Add New Product'}
        </h2>

        {errors.submit && (
          <div className={styles.errorMessage} role="alert">
            {errors.submit}
          </div>
        )}

        <div className={styles.formGroup}>
          <label htmlFor="name" className={styles.label}>
            Product Name *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={`${styles.input} ${errors.name ? styles.inputError : ''}`}
            disabled={isSubmitting}
          />
          {errors.name && <span className={styles.fieldError}>{errors.name}</span>}
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="category" className={styles.label}>
            Category *
          </label>
          <select
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
            className={`${styles.select} ${errors.category ? styles.inputError : ''}`}
            disabled={isSubmitting}
          >
            <option value="">Select a category</option>
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
            Description *
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
              Price (NT$) *
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
              Display Order
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

        <ImageUpload
          label="Product Image *"
          value={formData.imageUrl}
          onChange={(url) => {
            setFormData((prev) => ({ ...prev, imageUrl: url }));
            if (errors.imageUrl) {
              setErrors((prev) => ({ ...prev, imageUrl: null }));
            }
          }}
          onThumbnailChange={(thumbUrl) => {
            setFormData((prev) => ({ ...prev, thumbnailUrl: thumbUrl }));
          }}
          placeholder="Upload product image (thumbnail will be generated automatically)"
        />
        {errors.imageUrl && <span className={styles.fieldError}>{errors.imageUrl}</span>}
        {formData.thumbnailUrl && (
          <p className={styles.helpText}>✓ Thumbnail generated automatically</p>
        )}

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
            <span>In Stock</span>
          </label>
        </div>

        <div className={styles.formActions}>
          <button
            type="button"
            onClick={onCancel}
            className={styles.cancelButton}
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button type="submit" className={styles.submitButton} disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : product ? 'Update Product' : 'Create Product'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default ProductForm;
