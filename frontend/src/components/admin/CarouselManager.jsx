/**
 * CarouselManager Component
 *
 * Admin interface for managing carousel slides with drag-and-drop reordering
 */

import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import {
  getAllCarouselSlides,
  createCarouselSlide,
  updateCarouselSlide,
  deleteCarouselSlide
} from '../../services/carouselService';
import ImageUpload from './ImageUpload';
import { getImageUrl } from '../../utils/imageUtils';
import styles from './CarouselManager.module.css';

function CarouselManager({ toast }) {
  const [slides, setSlides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    subtitle: '',
    imageUrl: '',
    ctaLabel: '',
    ctaLink: '',
    displayOrder: 0,
    active: true
  });

  useEffect(() => {
    fetchSlides();
  }, []);

  const fetchSlides = async () => {
    try {
      setLoading(true);
      const data = await getAllCarouselSlides();
      setSlides(data);
    } catch (error) {
      toast.error('載入輪播圖失敗');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditing(null);
    setFormData({
      title: '',
      subtitle: '',
      imageUrl: '',
      displayOrder: slides.length,
      active: true
    });
    setShowForm(true);
  };

  const handleEdit = (slide) => {
    setEditing({ ...slide, id: slide._id }); // Ensure id field exists
    setFormData({
      title: slide.title,
      subtitle: slide.subtitle || '',
      imageUrl: slide.imageUrl,
      displayOrder: slide.displayOrder,
      active: slide.active
    });
    setShowForm(true);
  };

  const handleDelete = async (slideId) => {
    if (!window.confirm('確定要刪除此輪播圖嗎？')) return;

    try {
      await deleteCarouselSlide(slideId);
      toast.success('輪播圖已刪除');
      fetchSlides();
    } catch (error) {
      toast.error('刪除失敗');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editing) {
        await updateCarouselSlide(editing.id, formData);
        toast.success('輪播圖已更新');
      } else {
        await createCarouselSlide(formData);
        toast.success('輪播圖已新增');
      }
      setShowForm(false);
      fetchSlides();
    } catch (error) {
      toast.error(editing ? '更新失敗' : '新增失敗');
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditing(null);
  };

  const handleDragEnd = async (result) => {
    if (!result.destination) {
      return;
    }

    if (result.destination.index === result.source.index) {
      return;
    }

    const items = Array.from(slides);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    // Update display order for all affected slides
    const updatedSlides = items.map((slide, index) => ({
      ...slide,
      displayOrder: index
    }));

    setSlides(updatedSlides);

    // Update the backend for changed slides
    try {
      const updatePromises = updatedSlides
        .filter((slide, index) => slide.displayOrder !== slides[index]?.displayOrder)
        .map(slide => updateCarouselSlide(slide._id, { displayOrder: slide.displayOrder }));

      await Promise.all(updatePromises);
      toast.success('順序已更新');
    } catch (error) {
      console.error('Failed to update order:', error);
      toast.error('更新順序失敗');
      fetchSlides(); // Revert on error
    }
  };

  if (loading) {
    return <div className={styles.loading}>載入中...</div>;
  }

  if (showForm) {
    return (
      <div className={styles.formContainer}>
        <h2>{editing ? '編輯輪播圖' : '新增輪播圖'}</h2>
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label>標題 *</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
              maxLength={200}
            />
          </div>

          <div className={styles.formGroup}>
            <label>副標題</label>
            <input
              type="text"
              value={formData.subtitle}
              onChange={(e) => setFormData({ ...formData, subtitle: e.target.value })}
              maxLength={500}
            />
          </div>

          <ImageUpload
            label="輪播圖片 *"
            value={formData.imageUrl}
            onChange={(url) => setFormData({ ...formData, imageUrl: url })}
            placeholder="點擊上傳輪播圖片 (最大 5MB)"
            hideUrlInput={true}
          />

          <div className={styles.formGroup}>
            <label>顯示順序</label>
            <input
              type="number"
              value={formData.displayOrder}
              onChange={(e) => setFormData({ ...formData, displayOrder: parseInt(e.target.value) })}
              min={0}
            />
          </div>

          <div className={styles.formGroup}>
            <label>
              <input
                type="checkbox"
                checked={formData.active}
                onChange={(e) => setFormData({ ...formData, active: e.target.checked })}
              />
              啟用
            </label>
          </div>

          <div className={styles.formActions}>
            <button type="submit" className={styles.primaryButton}>
              {editing ? '更新' : '新增'}
            </button>
            <button type="button" onClick={handleCancel} className={styles.secondaryButton}>
              取消
            </button>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>輪播圖管理</h2>
        <button onClick={handleAdd} className={styles.primaryButton}>
          ➕ 新增輪播圖
        </button>
      </div>

      <div className={styles.slidesContainer}>
        {slides.length === 0 ? (
          <p className={styles.empty}>尚無輪播圖，請新增第一個</p>
        ) : (
          <DragDropContext onDragEnd={handleDragEnd}>
            <Droppable droppableId="carousel-slides">
              {(provided, snapshot) => (
                <div
                  className={styles.slidesList}
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                  style={{
                    backgroundColor: snapshot.isDraggingOver ? '#f0f4ff' : 'transparent',
                  }}
                >
                  {slides.map((slide, index) => (
                    <Draggable key={slide._id} draggableId={String(slide._id)} index={index}>
                      {(provided, snapshot) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          className={`${styles.slideCard} ${snapshot.isDragging ? styles.dragging : ''}`}
                          style={{
                            ...provided.draggableProps.style,
                          }}
                        >
                          <div
                            className={styles.dragHandle}
                            {...provided.dragHandleProps}
                            title="拖曳以重新排序"
                          >
                            ☰
                          </div>
                          <img src={getImageUrl(slide.imageUrl)} alt={slide.title} className={styles.slideImage} />
                          <div className={styles.slideInfo}>
                            <h3>{slide.title}</h3>
                            <p>{slide.subtitle}</p>
                            <div className={styles.slideMeta}>
                              <span>順序: {slide.displayOrder}</span>
                              <span className={slide.active ? styles.active : styles.inactive}>
                                {slide.active ? '✓ 啟用' : '✗ 停用'}
                              </span>
                            </div>
                          </div>
                          <div className={styles.slideActions}>
                            <button onClick={() => handleEdit(slide)} className={styles.editButton}>
                              編輯
                            </button>
                            <button onClick={() => handleDelete(slide._id)} className={styles.deleteButton}>
                              刪除
                            </button>
                          </div>
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          </DragDropContext>
        )}
      </div>
    </div>
  );
}

CarouselManager.propTypes = {
  toast: PropTypes.object.isRequired,
};

export default CarouselManager;
