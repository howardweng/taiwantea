/**
 * CategoryForm Component
 *
 * Form for creating/editing categories
 */

import { useState, useEffect } from 'react';
import styles from './CategoryForm.module.css';

function CategoryForm({ category, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    englishName: '',
    description: '',
    displayOrder: 999,
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  // Initialize form with category data if editing
  useEffect(() => {
    if (category) {
      setFormData({
        id: category.id || '',
        name: category.name || '',
        englishName: category.englishName || '',
        description: category.description || '',
        displayOrder: category.displayOrder || 999,
      });
    }
  }, [category]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'displayOrder' ? parseInt(value) || 0 : value,
    }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!category) {
      // ID is required for new categories
      if (!formData.id.trim()) {
        newErrors.id = '分類 ID 為必填';
      } else if (!/^[a-z0-9-]+$/.test(formData.id)) {
        newErrors.id = 'ID 只能包含小寫英文、數字和連字號';
      }
    }

    if (!formData.name.trim()) {
      newErrors.name = '分類名稱為必填';
    }

    if (!formData.description.trim() || formData.description.length < 10) {
      newErrors.description = '描述至少需要 10 個字元';
    }

    if (formData.displayOrder < 0) {
      newErrors.displayOrder = '顯示順序必須為 0 或更大';
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
    setSubmitError(null);

    try {
      // For editing, don't send the ID field
      const submitData = category
        ? { name: formData.name, englishName: formData.englishName, description: formData.description, displayOrder: formData.displayOrder }
        : formData;

      await onSubmit(submitData);
    } catch (error) {
      console.error('Failed to save category:', error);
      setSubmitError(error.response?.data?.detail || error.message || '儲存分類失敗');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.formContainer}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h2 className={styles.formTitle}>{category ? '編輯分類' : '新增分類'}</h2>

        {submitError && <div className={styles.errorMessage}>{submitError}</div>}

        <div className={styles.formGroup}>
          <label htmlFor="id" className={styles.label}>
            分類 ID *
          </label>
          <input
            type="text"
            id="id"
            name="id"
            value={formData.id}
            onChange={handleChange}
            disabled={!!category || isSubmitting}
            className={`${styles.input} ${errors.id ? styles.inputError : ''}`}
            placeholder="例如: green, black, oolong"
          />
          {errors.id && <span className={styles.fieldError}>{errors.id}</span>}
          {!category && (
            <small className={styles.helpText}>
              只能使用小寫英文、數字和連字號。建立後無法修改。
            </small>
          )}
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="name" className={styles.label}>
            分類名稱（中文）*
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            disabled={isSubmitting}
            className={`${styles.input} ${errors.name ? styles.inputError : ''}`}
            placeholder="例如: 優選綠茶"
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
            disabled={isSubmitting}
            className={styles.input}
            placeholder="e.g., Green Tea"
          />
          <small className={styles.helpText}>
            English translation of the category name (optional)
          </small>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="description" className={styles.label}>
            分類描述 *
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            disabled={isSubmitting}
            className={`${styles.textarea} ${errors.description ? styles.inputError : ''}`}
            placeholder="描述此茶葉分類..."
          />
          {errors.description && <span className={styles.fieldError}>{errors.description}</span>}
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
            disabled={isSubmitting}
            min="0"
            className={`${styles.input} ${errors.displayOrder ? styles.inputError : ''}`}
          />
          {errors.displayOrder && <span className={styles.fieldError}>{errors.displayOrder}</span>}
          <small className={styles.helpText}>分類依此數字排序 (0 = 第一個)</small>
        </div>

        <div className={styles.formActions}>
          <button type="button" onClick={onCancel} className={styles.cancelButton} disabled={isSubmitting}>
            取消
          </button>
          <button type="submit" className={styles.submitButton} disabled={isSubmitting}>
            {isSubmitting ? '儲存中...' : category ? '更新分類' : '建立分類'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default CategoryForm;
