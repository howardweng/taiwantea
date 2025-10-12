/**
 * ImageUpload Component
 *
 * Reusable image upload component with preview
 */

import { useState, useRef, useEffect } from 'react';
import api from '../../services/api';
import styles from './ImageUpload.module.css';

function ImageUpload({ value, onChange, onThumbnailChange, label, placeholder, hideUrlInput = false }) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(value || '');
  const fileInputRef = useRef(null);

  // Update preview when value prop changes (important for editing mode)
  useEffect(() => {
    setPreviewUrl(value || '');
  }, [value]);

  const handleFileSelect = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file');
      return;
    }

    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('Image size must be less than 5MB');
      return;
    }

    setError(null);
    setUploading(true);

    try {
      // Create FormData for upload
      const formData = new FormData();
      formData.append('file', file);

      // Upload image
      const response = await api.post('/api/upload/image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const { imageUrl, thumbnailUrl } = response.data;

      // Update preview and notify parent
      setPreviewUrl(imageUrl);
      onChange(imageUrl);

      // Also update thumbnail if callback provided
      if (onThumbnailChange && thumbnailUrl) {
        onThumbnailChange(thumbnailUrl);
      }
    } catch (err) {
      console.error('Upload failed:', err);
      setError(err.response?.data?.detail || 'Failed to upload image');
    } finally {
      setUploading(false);
    }
  };

  const handleUrlChange = (e) => {
    const url = e.target.value;
    setPreviewUrl(url);
    onChange(url);
    setError(null);
  };

  const handleRemove = () => {
    setPreviewUrl('');
    onChange('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleBrowse = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className={styles.container}>
      {label && <label className={styles.label}>{label}</label>}

      <div className={styles.uploadArea}>
        {/* Preview */}
        {previewUrl && (
          <div className={styles.preview}>
            <img src={previewUrl} alt="Preview" className={styles.previewImage} />
            <button
              type="button"
              onClick={handleRemove}
              className={styles.removeButton}
              disabled={uploading}
            >
              ✕
            </button>
          </div>
        )}

        {/* Upload Button */}
        {!previewUrl && (
          <div className={styles.uploadPrompt}>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className={styles.fileInput}
              disabled={uploading}
            />
            <button
              type="button"
              onClick={handleBrowse}
              className={styles.browseButton}
              disabled={uploading}
            >
              {uploading ? '⏳ Uploading...' : '📁 Choose Image'}
            </button>
            <p className={styles.uploadHint}>
              {placeholder || 'Click to upload or enter URL below (Max 5MB)'}
            </p>
          </div>
        )}
      </div>

      {/* URL Input */}
      {!hideUrlInput && (
        <div className={styles.urlInput}>
          <input
            type="url"
            value={previewUrl}
            onChange={handleUrlChange}
            placeholder="Or enter image URL..."
            className={styles.input}
            disabled={uploading}
          />
        </div>
      )}

      {/* Error Message */}
      {error && <div className={styles.error}>{error}</div>}

      {/* File Info */}
      <p className={styles.info}>Supported: JPG, PNG, WebP, GIF (max 5MB)</p>
    </div>
  );
}

export default ImageUpload;
