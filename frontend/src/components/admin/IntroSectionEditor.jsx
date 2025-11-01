/**
 * IntroSectionEditor Component
 *
 * Admin interface for editing the intro section with rich HTML editor
 */

import { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import PropTypes from 'prop-types';
import ReactQuill, { Quill } from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import ImageResize from 'quill-image-resize-module-react';
import api from '../../services/api';
import styles from './IntroSectionEditor.module.css';

// Register the image resize module
Quill.register('modules/imageResize', ImageResize);

// Suppress react-quill deprecation warnings
const originalError = console.error;
const originalWarn = console.warn;

console.error = (...args) => {
  if (
    typeof args[0] === 'string' &&
    (args[0].includes('findDOMNode') || args[0].includes('DOMNodeInserted'))
  ) {
    return;
  }
  originalError.call(console, ...args);
};

console.warn = (...args) => {
  if (
    typeof args[0] === 'string' &&
    args[0].includes('DOMNodeInserted')
  ) {
    return;
  }
  originalWarn.call(console, ...args);
};

function IntroSectionEditor({ toast }) {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    htmlContent: '',
    buttonText: '',
    buttonLink: '',
    active: true
  });
  const quillRef = useRef(null);
  const uploadImageRef = useRef(null);

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

      // Keep the current form data, don't refetch
    } catch (error) {
      console.error('Failed to update intro section:', error);
      toast.error('更新失敗: ' + (error.response?.data?.message || error.message));
    } finally {
      setSaving(false);
    }
  };

  // Upload image file and insert into editor
  const uploadImage = useCallback(async (file) => {
    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('圖片大小不能超過 5MB');
      return null;
    }

    try {
      const formData = new FormData();
      formData.append('image', file);

      const response = await api.post('/api/upload/image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success('圖片已上傳');
      return response.data.imageUrl;
    } catch (error) {
      console.error('Image upload failed:', error);
      toast.error('圖片上傳失敗');
      return null;
    }
  }, [toast]);

  // Keep uploadImage ref updated
  useEffect(() => {
    uploadImageRef.current = uploadImage;
  }, [uploadImage]);

  // Image upload handler for toolbar button
  const imageHandler = useCallback(async () => {
    const input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');
    input.click();

    input.onchange = async () => {
      const file = input.files[0];
      if (!file) return;

      const imageUrl = await uploadImageRef.current(file);
      if (imageUrl && quillRef.current) {
        const quill = quillRef.current.getEditor();
        const range = quill.getSelection(true);
        quill.insertEmbed(range.index, 'image', imageUrl);
        quill.setSelection(range.index + 1);
      }
    };
  }, []); // No dependencies - stable function

  // Handle pasted images
  const handlePaste = useCallback(async (e) => {
    const clipboardData = e.clipboardData || window.clipboardData;
    if (!clipboardData) {
      return;
    }

    const items = clipboardData.items;

    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf('image') !== -1) {
        e.preventDefault();
        e.stopPropagation();

        const file = items[i].getAsFile();

        const imageUrl = await uploadImageRef.current(file);

        if (imageUrl && quillRef.current) {
          const quill = quillRef.current.getEditor();
          const range = quill.getSelection(true);
          quill.insertEmbed(range.index, 'image', imageUrl);
          quill.setSelection(range.index + 1);
        }
        break;
      }
    }
  }, []); // No dependencies - stable function

  // Attach paste handler and enable image deletion
  useEffect(() => {
    if (quillRef.current) {
      const editor = quillRef.current.getEditor();
      const editorElement = editor.root;

      // Add paste handler
      editorElement.addEventListener('paste', handlePaste);

      // Add keyboard handler for image deletion
      const handleKeyDown = (e) => {
        if (e.key === 'Delete' || e.key === 'Backspace') {
          const selection = editor.getSelection();
          if (selection) {
            const [blot] = editor.getLeaf(selection.index);
            if (blot && blot.domNode && blot.domNode.tagName === 'IMG') {
              // Allow default deletion behavior
              return;
            }
          }
        }
      };

      editorElement.addEventListener('keydown', handleKeyDown);

      return () => {
        editorElement.removeEventListener('paste', handlePaste);
        editorElement.removeEventListener('keydown', handleKeyDown);
      };
    }
  }, []); // Empty dependency - only run once when editor mounts

  // Quill editor modules configuration
  const modules = useMemo(() => ({
    toolbar: {
      container: [
        [{ 'header': [1, 2, 3, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'align': [] }],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        ['link'],
        ['clean']
      ]
    },
    imageResize: {
      parchment: Quill.import('parchment'),
      modules: ['Resize', 'DisplaySize', 'Toolbar']
    }
  }), []); // Remove imageHandler dependency to prevent remounting

  const formats = [
    'header',
    'bold', 'italic', 'underline', 'strike',
    'color', 'background',
    'align',
    'list', 'bullet',
    'link',
    'image',
    'width',
    'height',
    'style'
  ];

  if (loading) {
    return <div className={styles.loading}>載入中...</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>介紹區塊設定</h2>
        <p className={styles.description}>
          編輯首頁介紹區塊的內容和按鈕文字（按鈕連結會自動使用網站設定中的蝦皮商店網址）
        </p>
      </div>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label className={styles.label}>HTML 內容 *</label>
          <ReactQuill
            key="intro-editor"
            ref={quillRef}
            theme="snow"
            value={formData.htmlContent}
            onChange={(content) => setFormData({ ...formData, htmlContent: content })}
            modules={modules}
            formats={formats}
            className={styles.editor}
            placeholder="輸入介紹區塊的內容..."
          />
          <span className={styles.helpText}>
            使用編輯器格式化文字、加入連結等。按 Ctrl+V 貼上圖片，點擊圖片可拖曳調整大小，使用對齊按鈕調整圖片位置
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
              placeholder="例如：於蝦皮賣場購買"
              required
            />
            <span className={styles.helpText}>
              按鈕連結會自動使用「網站設定」中的「蝦皮商店網址」
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
