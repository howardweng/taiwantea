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
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }

    try {
      await deleteProduct(productId);
      toast.success('Product deleted successfully');
      refetch(); // Refresh product list
    } catch (error) {
      console.error('Failed to delete product:', error);
      toast.error('Failed to delete product. Please try again.');
    }
  };

  const handleFormSubmit = async (formData) => {
    try {
      if (editingProduct) {
        await updateProduct(editingProduct.id, formData);
        toast.success('Product updated successfully');
      } else {
        await createProduct(formData);
        toast.success('Product created successfully');
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
    if (!window.confirm('Are you sure you want to delete this category?')) {
      return;
    }

    try {
      await deleteCategory(categoryId);
      toast.success('Category deleted successfully');
      refetch(); // Refresh categories list
    } catch (error) {
      console.error('Failed to delete category:', error);
      toast.error('Failed to delete category. Please try again.');
    }
  };

  const handleCategoryFormSubmit = async (formData) => {
    try {
      if (editingCategory) {
        await updateCategory(editingCategory.id, formData);
        toast.success('Category updated successfully');
      } else {
        await createCategory(formData);
        toast.success('Category created successfully');
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
          <p className={styles.adminLabel}>Admin Panel</p>
        </div>

        <nav className={styles.nav}>
          <button
            className={`${styles.navItem} ${activeTab === 'products' ? styles.active : ''}`}
            onClick={() => setActiveTab('products')}
          >
            📦 Products
          </button>
          <button
            className={`${styles.navItem} ${activeTab === 'categories' ? styles.active : ''}`}
            onClick={() => setActiveTab('categories')}
          >
            🏷️ Categories
          </button>
          <button
            className={`${styles.navItem} ${activeTab === 'settings' ? styles.active : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            ⚙️ Settings
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
            🚪 Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className={styles.main}>
        {/* Header */}
        <header className={styles.header}>
          <h1 className={styles.pageTitle}>
            {activeTab === 'products' && '📦 Product Management'}
            {activeTab === 'categories' && '🏷️ Category Management'}
            {activeTab === 'settings' && '⚙️ Settings'}
          </h1>
        </header>

        {/* Content */}
        <div className={styles.content}>
          {activeTab === 'products' && (
            <div className={styles.productsTab}>
              <div className={styles.stats}>
                <div className={styles.statCard}>
                  <div className={styles.statValue}>{products.length}</div>
                  <div className={styles.statLabel}>Total Products</div>
                </div>
                <div className={styles.statCard}>
                  <div className={styles.statValue}>{categories.length}</div>
                  <div className={styles.statLabel}>Categories</div>
                </div>
                <div className={styles.statCard}>
                  <div className={styles.statValue}>
                    {products.filter(p => p.inStock).length}
                  </div>
                  <div className={styles.statLabel}>In Stock</div>
                </div>
              </div>

              <div className={styles.actions}>
                <button className={styles.primaryButton} onClick={handleAddProduct}>
                  ➕ Add New Product
                </button>
              </div>

              {loading ? (
                <div className={styles.loading}>Loading products...</div>
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
                              <div className={styles.productStock}>
                                <span className={product.inStock ? styles.inStock : styles.outOfStock}>
                                  {product.inStock ? '✓ In Stock' : '✗ Out of Stock'}
                                </span>
                              </div>
                              <div className={styles.productActions}>
                                <button
                                  className={styles.editButton}
                                  onClick={() => handleEditProduct(product)}
                                >
                                  Edit
                                </button>
                                <button
                                  className={styles.deleteButton}
                                  onClick={() => handleDeleteProduct(product.id)}
                                >
                                  Delete
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
                  ➕ Add New Category
                </button>
              </div>

              <div className={styles.categoryList}>
                {categories.map((category) => (
                  <div key={category.id} className={styles.categoryCard}>
                    <div className={styles.categoryCardContent}>
                      <h3>{category.name}</h3>
                      <p>{category.description}</p>
                      <div className={styles.categoryMeta}>
                        Order: {category.displayOrder} |
                        Products: {productsByCategory[category.id]?.length || 0}
                      </div>
                    </div>
                    <div className={styles.categoryCardActions}>
                      <button
                        className={styles.editButton}
                        onClick={() => handleEditCategory(category)}
                      >
                        Edit
                      </button>
                      <button
                        className={styles.deleteButton}
                        onClick={() => handleDeleteCategory(category.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className={styles.settingsTab}>
              <div className={styles.settingSection}>
                <h3>Admin Information</h3>
                <p><strong>Name:</strong> {user?.name}</p>
                <p><strong>Email:</strong> {user?.email}</p>
              </div>

              <div className={styles.settingSection}>
                <h3>System Status</h3>
                <p>✅ API Connected</p>
                <p>✅ Database Connected</p>
                <p>✅ {products.length} Products Loaded</p>
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
