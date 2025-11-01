/**
 * SiteSettingsEditor Component
 *
 * Admin interface for managing site settings (logo, brand name, etc.)
 */

import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import api from '../../services/api';
import ImageUpload from './ImageUpload';
import styles from './SiteSettingsEditor.module.css';

function SiteSettingsEditor({ toast }) {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [settings, setSettings] = useState(null);

  const [formData, setFormData] = useState({
    logoType: 'text',
    logoImageUrl: '',
    logoText: '',
    logoIcon: '🍵',
    brandName: 'TAIWANTEA',
    shopeeStoreUrl: 'https://shopee.tw/'
  });

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await api.get('/api/admin/site-settings', { timeout: 5000 });
      setSettings(response.data);
      setFormData({
        logoType: response.data.logoType,
        logoImageUrl: response.data.logoImageUrl || '',
        logoText: response.data.logoText || '',
        logoIcon: response.data.logoIcon || '🍵',
        brandName: response.data.brandName,
        shopeeStoreUrl: response.data.shopeeStoreUrl || 'https://shopee.tw/'
      });
    } catch (error) {
      console.error('Failed to fetch site settings:', error);
      toast.error('載入網站設定失敗: ' + (error.message || '未知錯誤'));
      // Set default values so user can still use the form
      setFormData({
        logoType: 'text',
        logoImageUrl: '',
        logoText: '',
        logoIcon: '🍵',
        brandName: 'TAIWANTEA',
        shopeeStoreUrl: 'https://shopee.tw/'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLogoTypeChange = (e) => {
    setFormData(prev => ({
      ...prev,
      logoType: e.target.value
    }));
  };

  const handleImageUpload = (imageUrl) => {
    setFormData(prev => ({
      ...prev,
      logoImageUrl: imageUrl
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      // Validate based on logo type
      if (formData.logoType === 'image' && !formData.logoImageUrl) {
        toast.error('請上傳 Logo 圖片');
        return;
      }
      if (formData.logoType === 'text' && !formData.logoIcon) {
        toast.error('請輸入 Logo 圖示');
        return;
      }

      await api.put('/api/admin/site-settings', formData);
      toast.success('網站設定已更新');
      fetchSettings(); // Refresh
    } catch (error) {
      console.error('Failed to update site settings:', error);
      toast.error('更新網站設定失敗');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className={styles.loading}>載入中...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>網站設定</h2>
        <p className={styles.description}>管理網站 Logo、品牌名稱和蝦皮商店連結</p>
      </div>

      <form className={styles.form} onSubmit={handleSubmit}>
        {/* Logo Type Selection */}
        <div className={styles.formGroup}>
          <label className={styles.label}>Logo 類型</label>
          <div className={styles.radioGroup}>
            <label className={styles.radioLabel}>
              <input
                type="radio"
                name="logoType"
                value="text"
                checked={formData.logoType === 'text'}
                onChange={handleLogoTypeChange}
              />
              <span>文字 + 圖示</span>
            </label>
            <label className={styles.radioLabel}>
              <input
                type="radio"
                name="logoType"
                value="image"
                checked={formData.logoType === 'image'}
                onChange={handleLogoTypeChange}
              />
              <span>圖片</span>
            </label>
          </div>
        </div>

        {/* Text Logo Fields */}
        {formData.logoType === 'text' && (
          <>
            <div className={styles.formGroup}>
              <label className={styles.label} htmlFor="logoIcon">
                Logo 圖示 (Emoji 或文字)
              </label>
              <input
                type="text"
                id="logoIcon"
                name="logoIcon"
                value={formData.logoIcon}
                onChange={handleInputChange}
                className={styles.input}
                placeholder="例如: 🍵"
                maxLength={10}
              />
              <span className={styles.helpText}>
                可使用 Emoji 或簡短文字
              </span>
            </div>

            <div className={styles.formGroup}>
              <label className={styles.label} htmlFor="logoText">
                Logo 文字 (選填)
              </label>
              <input
                type="text"
                id="logoText"
                name="logoText"
                value={formData.logoText}
                onChange={handleInputChange}
                className={styles.input}
                placeholder="例如: 精選好茶"
              />
              <span className={styles.helpText}>
                顯示在圖示旁邊的文字，留空則不顯示
              </span>
            </div>
          </>
        )}

        {/* Image Logo Field */}
        {formData.logoType === 'image' && (
          <div className={styles.formGroup}>
            <label className={styles.label}>Logo 圖片</label>
            <ImageUpload
              onChange={handleImageUpload}
              value={formData.logoImageUrl}
              hideUrlInput={true}
            />
            <span className={styles.helpText}>
              建議尺寸: 200x60 像素，支援 PNG、JPG 格式
            </span>
          </div>
        )}

        {/* Brand Name */}
        <div className={styles.formGroup}>
          <label className={styles.label} htmlFor="brandName">
            品牌名稱 *
          </label>
          <input
            type="text"
            id="brandName"
            name="brandName"
            value={formData.brandName}
            onChange={handleInputChange}
            className={styles.input}
            required
            maxLength={100}
          />
          <span className={styles.helpText}>
            顯示在導航列的品牌名稱
          </span>
        </div>

        {/* Shopee Store URL */}
        <div className={styles.formGroup}>
          <label className={styles.label} htmlFor="shopeeStoreUrl">
            蝦皮商店網址 *
          </label>
          <input
            type="url"
            id="shopeeStoreUrl"
            name="shopeeStoreUrl"
            value={formData.shopeeStoreUrl}
            onChange={handleInputChange}
            className={styles.input}
            required
            placeholder="https://shopee.tw/your-store"
          />
          <span className={styles.helpText}>
            此網址將用於所有商品卡片和介紹區塊的購買按鈕
          </span>
        </div>

        {/* Preview */}
        <div className={styles.preview}>
          <h3>預覽</h3>
          <div className={styles.previewContent}>
            {formData.logoType === 'text' ? (
              <>
                <span className={styles.previewIcon}>{formData.logoIcon}</span>
                <span className={styles.previewBrand}>{formData.brandName}</span>
              </>
            ) : (
              <>
                {formData.logoImageUrl && (
                  <img
                    src={formData.logoImageUrl}
                    alt="Logo preview"
                    className={styles.previewImage}
                  />
                )}
                <span className={styles.previewBrand}>{formData.brandName}</span>
              </>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className={styles.actions}>
          <button
            type="submit"
            className={styles.saveButton}
            disabled={saving}
          >
            {saving ? '儲存中...' : '儲存設定'}
          </button>
        </div>
      </form>
    </div>
  );
}

SiteSettingsEditor.propTypes = {
  toast: PropTypes.object.isRequired
};

export default SiteSettingsEditor;
