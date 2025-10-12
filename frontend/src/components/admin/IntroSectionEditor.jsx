/**
 * IntroSectionEditor Component
 *
 * Admin interface for editing the intro section with rich HTML editor
 */

import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import api from '../../services/api';
import styles from './IntroSectionEditor.module.css';

function IntroSectionEditor({ toast }) {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    htmlContent: '',
    buttonText: '',
    buttonLink: '',
    active: true
  });

  useEffect(() => {
    fetchIntroSection();
  }, []);

  const fetchIntroSection = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/admin/intro-section');
      const data = response.data;
      setFormData({
        htmlContent: data.htmlContent || '',
        buttonText: data.buttonText || '',
        buttonLink: data.buttonLink || '',
        active: data.active !== undefined ? data.active : true
      });
    } catch (error) {
      if (error.response?.status === 404) {
        // Section doesn't exist yet, use defaults
        console.log('Intro section not found, using defaults');
      } else {
        toast.error('載入失敗');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setSaving(true);
      await api.put('/api/admin/intro-section', formData);
      toast.success('介紹區塊已更新');
    } catch (error) {
      console.error('Failed to update intro section:', error);
      toast.error('更新失敗');
    } finally {
      setSaving(false);
    }
  };

  // Quill editor modules configuration
  const modules = {
    toolbar: [
      [{ 'header': [1, 2, 3, false] }],
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'color': [] }, { 'background': [] }],
      [{ 'align': [] }],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      ['link'],
      ['clean']
    ],
  };

  const formats = [
    'header',
    'bold', 'italic', 'underline', 'strike',
    'color', 'background',
    'align',
    'list', 'bullet',
    'link'
  ];

  if (loading) {
    return <div className={styles.loading}>載入中...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>介紹區塊設定</h2>
        <p className={styles.description}>
          編輯首頁介紹區塊的內容、按鈕文字和連結
        </p>
      </div>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label className={styles.label}>HTML 內容 *</label>
          <ReactQuill
            theme="snow"
            value={formData.htmlContent}
            onChange={(content) => setFormData({ ...formData, htmlContent: content })}
            modules={modules}
            formats={formats}
            className={styles.editor}
            placeholder="輸入介紹區塊的內容..."
          />
          <span className={styles.helpText}>
            使用編輯器格式化文字、加入連結等
          </span>
        </div>

        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label className={styles.label}>按鈕文字 *</label>
            <input
              type="text"
              value={formData.buttonText}
              onChange={(e) => setFormData({ ...formData, buttonText: e.target.value })}
              className={styles.input}
              placeholder="例如：瀏覽全系列商品"
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>按鈕連結 *</label>
            <input
              type="text"
              value={formData.buttonLink}
              onChange={(e) => setFormData({ ...formData, buttonLink: e.target.value })}
              className={styles.input}
              placeholder="例如：https://shopee.tw/your-store"
              required
            />
            <span className={styles.helpText}>
              輸入完整網址（例如 Shopee 商店連結）
            </span>
          </div>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              checked={formData.active}
              onChange={(e) => setFormData({ ...formData, active: e.target.checked })}
            />
            <span>啟用介紹區塊</span>
          </label>
        </div>

        <div className={styles.actions}>
          <button
            type="submit"
            className={styles.saveButton}
            disabled={saving}
          >
            {saving ? '儲存中...' : '儲存變更'}
          </button>
        </div>
      </form>
    </div>
  );
}

IntroSectionEditor.propTypes = {
  toast: PropTypes.object.isRequired,
};

export default IntroSectionEditor;
