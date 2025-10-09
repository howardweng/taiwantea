# Data Model: Tea Leaves E-Commerce Website

**Feature**: Tea Leaves E-Commerce Website
**Date**: 2025-10-08
**Phase**: 1 - Data Design

## Overview

The data model consists of three primary entities stored in MongoDB collections. The design supports the core functionality of browsing tea products (customer-facing) and managing content (admin-facing).

## Entities

### 1. Product

Represents a tea product in the catalog.

**Collection**: `products`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `_id` | ObjectId | Yes | MongoDB auto-generated unique identifier | Auto-generated |
| `name` | String | Yes | Product name (e.g., "Dragon Well Green Tea") | 1-200 characters |
| `category` | String | Yes | Tea category (references Category entity) | Must exist in categories collection |
| `description` | String | Yes | Full product description including origin, flavor profile, brewing instructions | 10-5000 characters |
| `price` | Decimal | Yes | Product price in USD | >= 0, max 2 decimal places |
| `imageUrl` | String | Yes | URL/path to product image | Valid URL or file path |
| `thumbnailUrl` | String | No | URL/path to thumbnail image (auto-generated) | Valid URL or file path |
| `inStock` | Boolean | Yes | Product availability | Default: true |
| `displayOrder` | Integer | No | Sort order within category | >= 0, default: 999 |
| `createdAt` | DateTime | Yes | Product creation timestamp | ISO 8601 format, auto-set |
| `updatedAt` | DateTime | Yes | Last update timestamp | ISO 8601 format, auto-updated |
| `createdBy` | ObjectId | No | Admin user who created the product | References Admin._id |

**Indexes**:
- `category` (ascending) - for filtering by category
- `displayOrder` (ascending) - for sorting within categories
- `createdAt` (descending) - for "newest products" queries

**Example Document**:
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "Dragon Well Green Tea",
  "category": "green-tea",
  "description": "Premium Dragon Well (Longjing) green tea from Hangzhou, China. Renowned for its jade color, delicate aroma, and sweet aftertaste. Hand-picked leaves from high mountain gardens. Brewing: 175°F (80°C), 2-3 minutes, multiple infusions.",
  "price": 24.99,
  "imageUrl": "/uploads/products/dragon-well-001.webp",
  "thumbnailUrl": "/uploads/products/thumbs/dragon-well-001.webp",
  "inStock": true,
  "displayOrder": 1,
  "createdAt": "2025-10-08T12:00:00Z",
  "updatedAt": "2025-10-08T12:00:00Z",
  "createdBy": "507f1f77bcf86cd799439012"
}
```

**State Transitions**:
- Create: All required fields must be provided, timestamps auto-set
- Update: `updatedAt` automatically refreshed, partial updates allowed
- Delete: Soft delete option (add `deletedAt` field) or hard delete

---

### 2. Category

Represents a tea category for organizing products.

**Collection**: `categories`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `_id` | String | Yes | URL-friendly category identifier (e.g., "green-tea") | Lowercase, hyphens only, unique |
| `name` | String | Yes | Display name (e.g., "Green Tea") | 1-100 characters |
| `description` | String | No | Category description for SEO and display | 0-1000 characters |
| `displayOrder` | Integer | Yes | Sort order on homepage | >= 0, unique |
| `imageUrl` | String | No | Category hero/banner image | Valid URL or file path |
| `isActive` | Boolean | Yes | Whether category is visible | Default: true |
| `createdAt` | DateTime | Yes | Category creation timestamp | ISO 8601 format, auto-set |

**Indexes**:
- `displayOrder` (ascending) - for homepage section ordering
- `isActive` (ascending) - for filtering active categories

**Example Document**:
```json
{
  "_id": "green-tea",
  "name": "Green Tea",
  "description": "Fresh, delicate green teas from China and Japan. Rich in antioxidants with vegetal, grassy notes.",
  "displayOrder": 1,
  "imageUrl": "/uploads/categories/green-tea-banner.webp",
  "isActive": true,
  "createdAt": "2025-10-08T10:00:00Z"
}
```

**Predefined Categories** (Initial seed data):
1. Green Tea
2. Black Tea
3. Oolong Tea
4. White Tea
5. Herbal Tea
6. Pu-erh Tea

---

### 3. Admin

Represents an administrator user with content management permissions.

**Collection**: `admins`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `_id` | ObjectId | Yes | MongoDB auto-generated unique identifier | Auto-generated |
| `email` | String | Yes | Admin email (login identifier) | Valid email format, unique |
| `passwordHash` | String | Yes | bcrypt hashed password | bcrypt hash (never store plaintext) |
| `name` | String | Yes | Admin display name | 1-100 characters |
| `isActive` | Boolean | Yes | Account status | Default: true |
| `lastLoginAt` | DateTime | No | Last successful login timestamp | ISO 8601 format |
| `createdAt` | DateTime | Yes | Account creation timestamp | ISO 8601 format, auto-set |
| `updatedAt` | DateTime | Yes | Last update timestamp | ISO 8601 format, auto-updated |

**Indexes**:
- `email` (unique) - for login lookups
- `isActive` (ascending) - for filtering active admins

**Example Document**:
```json
{
  "_id": "507f1f77bcf86cd799439012",
  "email": "admin@taiwantea.com",
  "passwordHash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLhJ5u3G",
  "name": "Tea Admin",
  "isActive": true,
  "lastLoginAt": "2025-10-08T14:30:00Z",
  "createdAt": "2025-10-08T09:00:00Z",
  "updatedAt": "2025-10-08T14:30:00Z"
}
```

**Security Notes**:
- Never expose `passwordHash` in API responses
- Password requirements: min 8 characters, 1 uppercase, 1 lowercase, 1 number
- Account lockout after 5 failed login attempts (add `loginAttempts` field if needed)

---

## Relationships

### Product → Category
- **Type**: Many-to-One
- **Implementation**: `Product.category` stores Category ID (string reference)
- **Enforcement**: Application-level validation (ensure category exists before creating product)
- **Cascade**: If category deleted/deactivated, products remain but should show "Uncategorized" or be hidden

### Product → Admin
- **Type**: Many-to-One
- **Implementation**: `Product.createdBy` stores Admin ObjectId (optional)
- **Enforcement**: Application-level (store authenticated admin's ID on create)
- **Cascade**: If admin deleted, products remain (createdBy becomes null or references deleted admin)

---

## Validation Rules

### Product Validation
1. **Name**: Required, unique per category (case-insensitive check)
2. **Price**: Required, must be >= 0, max 2 decimal places
3. **Description**: Required, min 10 characters (ensure meaningful content)
4. **Image**: Required on create, must be valid image file (JPG/PNG/WebP), max 5MB
5. **Category**: Must reference an active category

### Category Validation
1. **ID**: Must be URL-friendly (lowercase, hyphens, no spaces)
2. **Display Order**: Must be unique across all active categories
3. **Cannot delete**: If category has products, prevent deletion or require reassignment

### Admin Validation
1. **Email**: Must be unique, valid email format
2. **Password**: Min 8 chars, complexity requirements (enforced on create/update)
3. **Cannot delete**: Must have at least one active admin in system

---

## Data Access Patterns

### Customer-Facing (Public API)

**Browse all products (homepage)**:
```javascript
// Query all active categories with their products
db.categories.find({ isActive: true }).sort({ displayOrder: 1 })
db.products.find({ category: "green-tea", inStock: true }).sort({ displayOrder: 1 })
```

**Get single product**:
```javascript
db.products.findOne({ _id: ObjectId("...") })
```

**Filter by category**:
```javascript
db.products.find({ category: "black-tea", inStock: true }).sort({ displayOrder: 1 })
```

### Admin-Facing (Protected API)

**List all products (admin dashboard)**:
```javascript
db.products.find({}).sort({ createdAt: -1 })
```

**Create product**:
```javascript
db.products.insertOne({
  name: "...",
  category: "...",
  // ... other fields
  createdAt: new Date(),
  updatedAt: new Date(),
  createdBy: adminId
})
```

**Update product**:
```javascript
db.products.updateOne(
  { _id: ObjectId("...") },
  { $set: { ...updates, updatedAt: new Date() } }
)
```

**Delete product**:
```javascript
db.products.deleteOne({ _id: ObjectId("...") })
// OR soft delete
db.products.updateOne(
  { _id: ObjectId("...") },
  { $set: { deletedAt: new Date(), isActive: false } }
)
```

**Admin authentication**:
```javascript
db.admins.findOne({ email: "admin@example.com", isActive: true })
// Then verify passwordHash with bcrypt
```

---

## Migration Strategy

### Initial Setup
1. Create collections with validation schemas
2. Create indexes for performance
3. Seed initial categories (6 predefined tea types)
4. Create initial admin account

### Schema Changes (Future)
- Add fields with default values to avoid breaking existing documents
- Use MongoDB schema validation for data integrity
- Version control migration scripts
- Test migrations on copy of production data

---

## Performance Considerations

1. **Indexes**: Already defined on high-query fields (category, displayOrder, createdAt)
2. **Document Size**: Product descriptions capped at 5000 chars to keep docs small
3. **Image Storage**: URLs only, actual images stored on filesystem/CDN
4. **Pagination**: Implement for admin product list (50 products per page)
5. **Caching**: Cache category list (rarely changes, frequently accessed)

---

## Compliance with Constitution

### Data Quality (Principle I)
- Clear field types and validation rules
- Consistent naming conventions (camelCase)
- Documented relationships and constraints

### Security (Principle V)
- Password hashing (bcrypt)
- No sensitive data in logs
- Input validation at model level
- Principle of least privilege (separate admin/customer access)

### Performance (Principle IV)
- Indexed fields for common queries
- Lightweight document structure
- Ready for pagination and caching
