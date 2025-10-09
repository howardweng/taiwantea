# Research: Tea Leaves E-Commerce Website

**Feature**: Tea Leaves E-Commerce Website
**Date**: 2025-10-08
**Phase**: 0 - Technical Research

## Technology Stack Research

### Frontend: React + Vite

**Decision**: React 18+ with Vite as build tool

**Rationale**:
- React is explicitly requested by user
- Vite provides fast development experience with HMR (Hot Module Replacement)
- Better performance than Create React App (faster builds, optimized bundling)
- Native ES modules support
- Built-in support for modern features (CSS modules, TypeScript, JSX)

**Alternatives Considered**:
- Create React App: Deprecated and slower build times
- Next.js: Overkill for single-page application, adds unnecessary complexity

### Backend: FastAPI + Motor

**Decision**: FastAPI with Motor (async MongoDB driver)

**Rationale**:
- FastAPI explicitly requested by user
- Async support via Motor for non-blocking MongoDB operations
- Built-in OpenAPI documentation generation
- Pydantic integration for data validation
- High performance (comparable to Node.js/Go)
- Type hints for better IDE support and runtime validation

**Alternatives Considered**:
- PyMongo (sync driver): Blocks I/O operations, lower throughput
- Flask: Lacks built-in async support and data validation

### Database: MongoDB

**Decision**: MongoDB with single database, multiple collections

**Rationale**:
- Explicitly requested by user
- Flexible schema suitable for product catalog (varying tea attributes)
- Good performance for read-heavy operations (customer browsing)
- Easy to scale horizontally
- Native support for storing binary data (GridFS for images if needed)

**Collections Structure**:
- `products`: Tea product documents
- `categories`: Tea category metadata
- `admins`: Admin user credentials and profiles

### Authentication: JWT with httpOnly Cookies

**Decision**: JWT tokens stored in httpOnly cookies

**Rationale**:
- Industry standard for stateless authentication
- httpOnly cookies prevent XSS attacks
- Secure flag ensures HTTPS-only transmission
- Refresh token rotation for enhanced security
- bcrypt for password hashing (industry standard, resistant to rainbow tables)

**Alternatives Considered**:
- Session-based auth: Requires server-side storage, harder to scale
- localStorage JWT: Vulnerable to XSS attacks
- OAuth2: Overkill for admin-only authentication

### Image Storage: File System + Future Cloud Migration

**Decision**: Local file system for development, designed for cloud storage migration

**Rationale**:
- Simple for initial development and testing
- Fast local access during development
- Architecture allows easy migration to cloud storage (S3, Cloudinary, etc.)
- Image service abstraction layer for future flexibility

**Image Processing**:
- Sharp library (Node.js) or Pillow (Python) for resizing/optimization
- Convert uploads to WebP format for better compression
- Generate multiple sizes (thumbnail, medium, full) for responsive images
- Maximum 5MB upload size enforced

**Alternatives Considered**:
- Immediate cloud storage: Adds complexity and cost for development
- GridFS: Slower than file system, harder to serve with CDN

### State Management: React Context + Custom Hooks

**Decision**: React Context API with custom hooks

**Rationale**:
- Built-in solution, no external dependencies
- Sufficient for this application's state complexity
- Custom hooks encapsulate data fetching logic
- Reduces bundle size compared to Redux

**State Domains**:
- Authentication state (useAuth hook)
- Product data (useProducts hook)
- Navigation state (useScrollNav hook)

**Alternatives Considered**:
- Redux/Redux Toolkit: Overkill for simple CRUD operations
- Zustand: Additional dependency, unnecessary for this scope

### API Communication: Axios

**Decision**: Axios for HTTP requests

**Rationale**:
- Automatic request/response transformation
- Interceptors for auth token injection
- Better error handling than fetch
- Request cancellation support
- Widespread community adoption

**Alternatives Considered**:
- Fetch API: Less feature-rich, requires more boilerplate
- React Query: Adds complexity, not needed for simple CRUD

### Styling: CSS Modules + Modern CSS

**Decision**: CSS Modules with CSS custom properties (variables)

**Rationale**:
- Scoped styles prevent conflicts
- No runtime overhead (unlike CSS-in-JS)
- Native CSS features (Grid, Flexbox, custom properties)
- Better performance (styles parsed at build time)
- WCAG 2.1 compliance easier with semantic CSS

**Design System**:
- CSS custom properties for theming (colors, spacing, typography)
- Mobile-first responsive design
- Flexbox/Grid for layouts
- Smooth scroll behavior via CSS or Intersection Observer API

**Alternatives Considered**:
- Tailwind CSS: Increases HTML complexity, larger bundle
- Styled Components: Runtime overhead, slower performance
- Material-UI: Heavy bundle size, opinionated design

### Testing Strategy

**Backend Testing**:
- pytest: Python standard, rich plugin ecosystem
- pytest-asyncio: Async test support for FastAPI
- httpx: Test client for FastAPI
- Coverage.py: Code coverage reporting

**Frontend Testing**:
- Vitest: Fast, Vite-native test runner
- React Testing Library: User-centric testing approach
- Happy DOM: Lightweight DOM implementation
- MSW (Mock Service Worker): API mocking for integration tests

**Test Pyramid**:
1. Unit tests: Business logic, utilities, pure functions
2. Integration tests: API endpoints, user flows
3. Contract tests: API schema validation
4. E2E tests (future): Playwright for critical paths

### Development Tools

**Linting & Formatting**:
- ESLint + Prettier (frontend): Code quality and consistency
- Black + Ruff (backend): Python formatting and linting
- Pre-commit hooks: Enforce standards before commits

**Development Environment**:
- Docker Compose: Local MongoDB + backend + frontend
- Hot reload: Vite (frontend), uvicorn --reload (backend)
- Environment variables: python-dotenv (backend), Vite env (frontend)

**Version Control**:
- Git with feature branch workflow
- Conventional commits format
- PR reviews required per constitution

## Best Practices Summary

### Performance Optimization
1. **Frontend**:
   - Lazy load admin routes
   - Image lazy loading (Intersection Observer)
   - Bundle size monitoring (Vite bundle analyzer)
   - Code splitting for routes

2. **Backend**:
   - Async handlers for all I/O operations
   - Database connection pooling
   - Index on category, createdAt fields
   - Response compression (GZip)

3. **Images**:
   - WebP format (70-80% quality)
   - Responsive images with srcset
   - CDN-ready architecture

### Security Best Practices
1. **Authentication**:
   - bcrypt with salt rounds 12
   - JWT expiry: 15 minutes (access), 7 days (refresh)
   - CSRF protection via SameSite cookie attribute

2. **Input Validation**:
   - Pydantic models for all API inputs
   - File type validation (magic number checking)
   - SQL/NoSQL injection prevention via parameterized queries
   - XSS prevention via output encoding

3. **CORS**:
   - Whitelist frontend origin only
   - Credentials allowed for cookie-based auth

4. **Rate Limiting**:
   - SlowAPI middleware for FastAPI
   - Limit admin endpoints to prevent brute force

### Accessibility (WCAG 2.1 Level AA)
1. Semantic HTML (nav, main, article, section)
2. ARIA labels for interactive elements
3. Keyboard navigation support (Tab, Enter, Escape)
4. Focus management (visible focus indicators)
5. Color contrast ratios (4.5:1 for text)
6. Alt text for all product images
7. Form labels and error announcements

### API Design Principles
1. RESTful conventions:
   - GET /api/products (list all)
   - GET /api/products/{id} (get one)
   - POST /api/admin/products (create)
   - PUT /api/admin/products/{id} (update)
   - DELETE /api/admin/products/{id} (delete)

2. Response format:
   ```json
   {
     "success": true,
     "data": {...},
     "message": "Operation successful"
   }
   ```

3. Error format:
   ```json
   {
     "success": false,
     "error": {
       "code": "VALIDATION_ERROR",
       "message": "User-friendly message",
       "details": [...]
     }
   }
   ```

## Architecture Decisions

### Separation of Concerns
- **Frontend**: Pure presentation layer, no business logic
- **Backend**: Business logic, data validation, persistence
- **Database**: Data storage only, minimal logic (indexes, constraints)

### Single-Page Application Flow
1. Initial load: HTML shell + JS bundle
2. React Router: Client-side routing (/, /admin)
3. Data fetching: Axios calls to FastAPI
4. State updates: Context API triggers re-renders
5. Smooth scroll: CSS scroll-behavior or JS scrollIntoView

### Image Upload Flow
1. User selects file in admin panel
2. Frontend validates size/type
3. FormData POST to /api/admin/upload
4. Backend validates, resizes, converts to WebP
5. Saves to filesystem, returns URL
6. Frontend updates product with image URL

### Deployment Considerations (Future)
- Frontend: Static hosting (Vercel, Netlify, S3 + CloudFront)
- Backend: Container deployment (Docker, Cloud Run, ECS)
- Database: MongoDB Atlas (managed service)
- Images: Cloud storage (S3, Cloudinary) with CDN
- Environment separation: dev, staging, production
