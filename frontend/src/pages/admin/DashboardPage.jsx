/**
 * Admin Dashboard Page
 *
 * Main admin interface with product management
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.jsx';
import { useToast } from '../../components/common/ToastContainer.jsx';
import useProducts from '../../hooks/useProducts';
import ProductForm from '../../components/admin/ProductForm';
import CategoryForm from '../../components/admin/CategoryForm';
import CarouselManager from '../../components/admin/CarouselManager';
import IntroSectionEditor from '../../components/admin/IntroSectionEditor';
import { createProduct, updateProduct, deleteProduct } from '../../services/adminProductService';
import { createCategory, updateCategory, deleteCategory } from '../../services/adminCategoryService';
import styles from './DashboardPage.module.css';

function DashboardPage() {
  const { user, logout } = useAuth();
  const toast = useToast();
  const { categories, products, loading, refetch } = useProducts();
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState('products');
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [showCategoryForm, setShowCategoryForm] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);

  const handleLogout = async () => {
    await logout();
    navigate('/admin/login');
  };

  const handleAddProduct = () => {
    setEditingProduct(null);
    setShowForm(true);
  };

  const handleEditProduct = (product) => {
    setEditingProduct(product);
    setShowForm(true);
  };

  const handleDeleteProduct = async (productId) => {
    if (!window.confirm('確定要刪除此商品嗎？')) {
      return;
    }

    try {
      await deleteProduct(productId);
      toast.success('商品已成功刪除');
      refetch(); // Refresh product list
    } catch (error) {
      console.error('Failed to delete product:', error);
      toast.error('刪除商品失敗，請重試。');
    }
  };

  const handleFormSubmit = async (formData) => {
    try {
      if (editingProduct) {
        await updateProduct(editingProduct.id, formData);
        toast.success('商品已成功更新');
      } else {
        await createProduct(formData);
        toast.success('商品已成功建立');
      }
      setShowForm(false);
      setEditingProduct(null);
      refetch(); // Refresh product list
    } catch (error) {
      console.error('Failed to save product:', error);
      throw error; // Re-throw to let form handle it
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingProduct(null);
  };

  const handleAddCategory = () => {
    setEditingCategory(null);
    setShowCategoryForm(true);
  };

  const handleEditCategory = (category) => {
    setEditingCategory(category);
    setShowCategoryForm(true);
  };

  const handleDeleteCategory = async (categoryId) => {
    if (!window.confirm('確定要刪除此分類嗎？')) {
      return;
    }

    try {
      await deleteCategory(categoryId);
      toast.success('分類已成功刪除');
      refetch(); // Refresh categories list
    } catch (error) {
      console.error('Failed to delete category:', error);
      toast.error('刪除分類失敗，請重試。');
    }
  };

  const handleCategoryFormSubmit = async (formData) => {
    try {
      if (editingCategory) {
        await updateCategory(editingCategory.id, formData);
        toast.success('分類已成功更新');
      } else {
        await createCategory(formData);
        toast.success('分類已成功建立');
      }
      setShowCategoryForm(false);
      setEditingCategory(null);
      refetch(); // Refresh categories list
    } catch (error) {
      console.error('Failed to save category:', error);
      throw error; // Re-throw to let form handle it
    }
  };

  const handleCategoryFormCancel = () => {
    setShowCategoryForm(false);
    setEditingCategory(null);
  };

  // Group products by category
  const productsByCategory = products.reduce((acc, product) => {
    const cat = product.category;
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(product);
    return acc;
  }, {});

  return (
    <div className={styles.container}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.sidebarHeader}>
          <div className={styles.logo}>🍵</div>
          <h2 className={styles.brandName}>TAIWANTEA</h2>
          <p className={styles.adminLabel}>管理後台</p>
        </div>

        <nav className={styles.nav}>
          <button
            className={`${styles.navItem} ${activeTab === 'products' ? styles.active : ''}`}
            onClick={() => setActiveTab('products')}
          >
            📦 商品管理
          </button>
          <button
            className={`${styles.navItem} ${activeTab === 'categories' ? styles.active : ''}`}
            onClick={() => setActiveTab('categories')}
          >
            🏷️ 分類管理
          </button>
          <button
            className={`${styles.navItem} ${activeTab === 'carousel' ? styles.active : ''}`}
            onClick={() => setActiveTab('carousel')}
          >
            🎠 輪播圖管理
          </button>
          <button
            className={`${styles.navItem} ${activeTab === 'intro' ? styles.active : ''}`}
            onClick={() => setActiveTab('intro')}
          >
            📝 介紹區塊
          </button>
          <button
            className={`${styles.navItem} ${activeTab === 'settings' ? styles.active : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            ⚙️ 系統設定
          </button>
        </nav>

        <div className={styles.sidebarFooter}>
          <div className={styles.userInfo}>
            <div className={styles.userAvatar}>👤</div>
            <div>
              <div className={styles.userName}>{user?.name || 'Admin'}</div>
              <div className={styles.userEmail}>{user?.email}</div>
            </div>
          </div>
          <button onClick={handleLogout} className={styles.logoutButton}>
            🚪 登出
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className={styles.main}>
        {/* Header */}
        <header className={styles.header}>
          <h1 className={styles.pageTitle}>
            {activeTab === 'products' && '📦 商品管理'}
            {activeTab === 'categories' && '🏷️ 分類管理'}
            {activeTab === 'carousel' && '🎠 輪播圖管理'}
            {activeTab === 'intro' && '📝 介紹區塊'}
            {activeTab === 'settings' && '⚙️ 系統設定'}
          </h1>
        </header>

        {/* Content */}
        <div className={styles.content}>
          {activeTab === 'products' && (
            <div className={styles.productsTab}>
              <div className={styles.stats}>
                <div className={styles.statCard}>
                  <div className={styles.statValue}>{products.length}</div>
                  <div className={styles.statLabel}>商品總數</div>
                </div>
                <div className={styles.statCard}>
                  <div className={styles.statValue}>{categories.length}</div>
                  <div className={styles.statLabel}>分類總數</div>
                </div>
                <div className={styles.statCard}>
                  <div className={styles.statValue}>
                    {products.filter(p => p.inStock).length}
                  </div>
                  <div className={styles.statLabel}>庫存商品</div>
                </div>
              </div>

              <div className={styles.actions}>
                <button className={styles.primaryButton} onClick={handleAddProduct}>
                  ➕ 新增商品
                </button>
              </div>

              {loading ? (
                <div className={styles.loading}>載入商品中...</div>
              ) : (
                <div className={styles.productsList}>
                  {categories.map((category) => {
                    const categoryProducts = productsByCategory[category.id] || [];

                    return (
                      <div key={category.id} className={styles.categoryGroup}>
                        <h3 className={styles.categoryTitle}>
                          {category.name} ({categoryProducts.length})
                        </h3>
                        <div className={styles.productTable}>
                          {categoryProducts.map((product) => (
                            <div key={product.id} className={styles.productRow}>
                              <div className={styles.productInfo}>
                                <img
                                  src={product.thumbnailUrl || product.imageUrl}
                                  alt={product.name}
                                  className={styles.productImage}
                                />
                                <div>
                                  <div className={styles.productName}>{product.name}</div>
                                  <div className={styles.productCategory}>{category.name}</div>
                                </div>
                              </div>
                              <div className={styles.productPrice}>NT${product.price}</div>
                              <div className={styles.productBadge}>
                                {product.badge ? (
                                  <span className={styles.badgeTag}>{product.badge}</span>
                                ) : (
                                  <span className={styles.noBadge}>—</span>
                                )}
                              </div>
                              <div className={styles.productStock}>
                                <span className={product.inStock ? styles.inStock : styles.outOfStock}>
                                  {product.inStock ? '✓ 有庫存' : '✗ 缺貨'}
                                </span>
                              </div>
                              <div className={styles.productActions}>
                                <button
                                  className={styles.editButton}
                                  onClick={() => handleEditProduct(product)}
                                >
                                  編輯
                                </button>
                                <button
                                  className={styles.deleteButton}
                                  onClick={() => handleDeleteProduct(product.id)}
                                >
                                  刪除
                                </button>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {activeTab === 'categories' && (
            <div className={styles.categoriesTab}>
              <div className={styles.actions}>
                <button className={styles.primaryButton} onClick={handleAddCategory}>
                  ➕ 新增分類
                </button>
              </div>

              <div className={styles.categoryList}>
                {categories.map((category) => (
                  <div key={category.id} className={styles.categoryCard}>
                    <div className={styles.categoryCardContent}>
                      <h3>{category.name}</h3>
                      <p>{category.description}</p>
                      <div className={styles.categoryMeta}>
                        顯示順序: {category.displayOrder} |
                        商品數量: {productsByCategory[category.id]?.length || 0}
                      </div>
                    </div>
                    <div className={styles.categoryCardActions}>
                      <button
                        className={styles.editButton}
                        onClick={() => handleEditCategory(category)}
                      >
                        編輯
                      </button>
                      <button
                        className={styles.deleteButton}
                        onClick={() => handleDeleteCategory(category.id)}
                      >
                        刪除
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'carousel' && (
            <CarouselManager toast={toast} />
          )}

          {activeTab === 'intro' && (
            <IntroSectionEditor toast={toast} />
          )}

          {activeTab === 'settings' && (
            <div className={styles.settingsTab}>
              <div className={styles.settingSection}>
                <h3>管理員資訊</h3>
                <p><strong>名稱:</strong> {user?.name}</p>
                <p><strong>電子郵件:</strong> {user?.email}</p>
              </div>

              <div className={styles.settingSection}>
                <h3>系統狀態</h3>
                <p>✅ API 已連接</p>
                <p>✅ 資料庫已連接</p>
                <p>✅ 已載入 {products.length} 項商品</p>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Product Form Modal */}
      {showForm && (
        <ProductForm
          product={editingProduct}
          categories={categories}
          onSubmit={handleFormSubmit}
          onCancel={handleFormCancel}
        />
      )}

      {/* Category Form Modal */}
      {showCategoryForm && (
        <CategoryForm
          category={editingCategory}
          onSubmit={handleCategoryFormSubmit}
          onCancel={handleCategoryFormCancel}
        />
      )}
    </div>
  );
}

export default DashboardPage;
