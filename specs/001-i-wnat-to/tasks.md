# Tasks: Tea Leaves E-Commerce Website

**Input**: Design documents from `/specs/001-i-wnat-to/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD approach required per constitution - tests MUST be written first and verified to fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below follow plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project root structure (backend/, frontend/, .env.example, docker-compose.yml, README.md)
- [x] T002 [P] Initialize backend Python project (backend/requirements.txt with FastAPI, Motor, Pydantic, pytest, bcrypt, python-jose)
- [x] T003 [P] Initialize frontend React project with Vite (frontend/package.json with React 18, React Router, Axios, Vitest)
- [x] T004 [P] Configure backend linting tools (backend/.flake8, backend/pyproject.toml for Black + Ruff)
- [x] T005 [P] Configure frontend linting tools (frontend/.eslintrc.json, frontend/.prettierrc)
- [x] T006 Create Docker Compose configuration (docker-compose.yml with MongoDB, backend, frontend services)
- [x] T007 [P] Create backend environment template (backend/.env.example with MongoDB URL, JWT secret, CORS origins)
- [x] T008 [P] Create frontend environment template (frontend/.env.example with API URL)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create backend source structure (backend/src/__init__.py, models/, schemas/, routers/, services/, middleware/)
- [x] T010 Create frontend source structure (frontend/src/main.jsx, App.jsx, components/, pages/, services/, hooks/, utils/, styles/)
- [x] T011 Implement MongoDB database connection (backend/src/database.py with Motor async client and connection pooling)
- [x] T012 Create MongoDB indexes and seed script (backend/src/scripts/seed_data.py for categories and initial admin user)
- [x] T013 Implement FastAPI application setup (backend/src/main.py with CORS, routers, error handlers)
- [x] T014 Implement backend configuration management (backend/src/config.py using Pydantic Settings)
- [x] T015 [P] Create Pydantic schemas for Admin entity (backend/src/schemas/admin.py with AdminCreate, AdminLogin, AdminProfile)
- [x] T016 [P] Create MongoDB model for Admin entity (backend/src/models/admin.py with CRUD operations)
- [x] T017 Implement authentication service (backend/src/services/auth_service.py with bcrypt password hashing, JWT creation/verification)
- [x] T018 Implement authentication middleware (backend/src/middleware/auth.py for JWT cookie validation)
- [x] T019 [P] Create authentication router (backend/src/routers/auth.py with /api/auth/login, /api/auth/logout, /api/auth/me endpoints)
- [x] T020 [P] Create React Router setup (frontend/src/App.jsx with routes for /, /admin)
- [x] T021 [P] Create Axios API client (frontend/src/services/api.js with base URL, interceptors for auth cookies)
- [x] T022 [P] Create authentication context and hook (frontend/src/hooks/useAuth.js for login, logout, current user state)
- [x] T023 [P] Create common UI components (frontend/src/components/common/LoadingSpinner.jsx, ErrorMessage.jsx)
- [x] T024 [P] Create global CSS variables and base styles (frontend/src/styles/variables.css, global.css with design tokens)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Browse and View Tea Products (Priority: P1) 🎯 MVP

**Goal**: Customers can view all tea products organized by category on a single scrollable page

**Independent Test**: Visit homepage and scroll through all categories - all products visible with complete information

### Tests for User Story 1 (TDD - Write First)

**NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T025 [P] [US1] Contract test for GET /api/categories in backend/tests/contract/test_products_api.py
- [ ] T026 [P] [US1] Contract test for GET /api/products in backend/tests/contract/test_products_api.py
- [ ] T027 [P] [US1] Contract test for GET /api/products/{id} in backend/tests/contract/test_products_api.py
- [ ] T028 [P] [US1] Integration test for public product browsing flow in backend/tests/integration/test_product_flow.py
- [ ] T029 [P] [US1] Unit test for ProductCard component in frontend/tests/components/ProductCard.test.jsx
- [ ] T030 [P] [US1] Integration test for homepage product display in frontend/tests/integration/userFlows.test.jsx

### Implementation for User Story 1

- [ ] T031 [P] [US1] Create Pydantic schemas for Category entity (backend/src/schemas/product.py with CategoryResponse)
- [ ] T032 [P] [US1] Create Pydantic schemas for Product entity (backend/src/schemas/product.py with ProductResponse, ProductList)
- [ ] T033 [P] [US1] Create MongoDB model for Category entity (backend/src/models/category.py with get_all_active, get_by_id)
- [ ] T034 [P] [US1] Create MongoDB model for Product entity (backend/src/models/product.py with get_all, get_by_id, filter_by_category)
- [ ] T035 [US1] Implement product service layer (backend/src/services/product_service.py with business logic for fetching products)
- [ ] T036 [US1] Create public products router (backend/src/routers/products.py with GET /api/products, GET /api/products/{id}, GET /api/categories)
- [ ] T037 [P] [US1] Create ProductCard component (frontend/src/components/customer/ProductCard.jsx displaying image, name, price, description)
- [ ] T038 [P] [US1] Create CategorySection component (frontend/src/components/customer/CategorySection.jsx with category header and product grid)
- [ ] T039 [P] [US1] Create ProductGrid component (frontend/src/components/customer/ProductGrid.jsx organizing products in responsive grid)
- [ ] T040 [US1] Create useProducts hook (frontend/src/hooks/useProducts.js fetching categories and products from API)
- [ ] T041 [US1] Create product service (frontend/src/services/productService.js with API calls for getProducts, getCategories)
- [ ] T042 [US1] Implement HomePage component (frontend/src/pages/HomePage.jsx rendering all category sections)
- [ ] T043 [P] [US1] Add responsive CSS for product display (frontend/src/components/customer/ProductCard.module.css, CategorySection.module.css)
- [ ] T044 [US1] Add ARIA labels and semantic HTML for accessibility (update ProductCard, CategorySection with proper roles, labels)

**Checkpoint**: At this point, User Story 1 should be fully functional - customers can view all products organized by category

---

## Phase 4: User Story 2 - Navigate Between Tea Categories (Priority: P2)

**Goal**: Customers can quickly jump to specific tea categories using smooth-scroll navigation

**Independent Test**: Click navigation menu items and verify smooth scroll to correct category sections

### Tests for User Story 2 (TDD - Write First)

- [ ] T045 [P] [US2] Unit test for Navigation component in frontend/tests/components/Navigation.test.jsx
- [ ] T046 [P] [US2] Integration test for smooth scroll navigation in frontend/tests/integration/userFlows.test.jsx

### Implementation for User Story 2

- [ ] T047 [P] [US2] Create Navigation component (frontend/src/components/customer/Navigation.jsx with category links)
- [ ] T048 [US2] Create useScrollNav hook (frontend/src/hooks/useScrollNav.js with smooth scroll to section logic)
- [ ] T049 [US2] Implement sticky navigation behavior (frontend/src/components/customer/Navigation.module.css with fixed positioning)
- [ ] T050 [US2] Integrate Navigation into HomePage (update frontend/src/pages/HomePage.jsx to include Navigation component)
- [ ] T051 [US2] Add scroll-to-section anchors (update CategorySection with id attributes matching navigation links)
- [ ] T052 [US2] Add active section highlighting (update useScrollNav to track current visible section, update Navigation styling)
- [ ] T053 [US2] Add keyboard navigation support (update Navigation component with Tab, Enter key handlers for accessibility)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - customers can browse products AND navigate quickly between categories

---

## Phase 5: User Story 3 - Admin Content Management (Priority: P1)

**Goal**: Administrators can manage tea products (create, edit, delete) via secure admin panel

**Independent Test**: Login to admin panel, create/edit/delete products, verify changes appear on public site immediately

### Tests for User Story 3 (TDD - Write First)

- [ ] T054 [P] [US3] Contract test for POST /api/admin/products in backend/tests/contract/test_admin_api.py
- [ ] T055 [P] [US3] Contract test for PUT /api/admin/products/{id} in backend/tests/contract/test_admin_api.py
- [ ] T056 [P] [US3] Contract test for DELETE /api/admin/products/{id} in backend/tests/contract/test_admin_api.py
- [ ] T057 [P] [US3] Contract test for POST /api/admin/upload in backend/tests/contract/test_admin_api.py
- [ ] T058 [P] [US3] Integration test for admin product CRUD flow in backend/tests/integration/test_admin_flow.py
- [ ] T059 [P] [US3] Integration test for admin authentication flow in backend/tests/integration/test_admin_flow.py
- [ ] T060 [P] [US3] Unit test for ProductForm component in frontend/tests/components/ProductForm.test.jsx
- [ ] T061 [P] [US3] Unit test for AdminLogin component in frontend/tests/components/AdminLogin.test.jsx

### Implementation for User Story 3

- [ ] T062 [P] [US3] Create Pydantic schemas for admin product operations (backend/src/schemas/product.py with ProductCreate, ProductUpdate, ProductAdmin)
- [ ] T063 [P] [US3] Add product CRUD methods to Product model (backend/src/models/product.py with create, update, delete, admin queries)
- [ ] T064 [US3] Implement image upload service (backend/src/services/image_service.py with file validation, resize, WebP conversion, storage)
- [ ] T065 [US3] Update product service with admin operations (backend/src/services/product_service.py with create_product, update_product, delete_product)
- [ ] T066 [US3] Create admin products router (backend/src/routers/admin.py with POST, PUT, DELETE /api/admin/products endpoints, protected by auth middleware)
- [ ] T067 [US3] Create image upload endpoint (add POST /api/admin/upload to backend/src/routers/admin.py with multipart form handling)
- [ ] T068 [P] [US3] Create AdminLogin component (frontend/src/components/admin/AdminLogin.jsx with email/password form)
- [ ] T069 [P] [US3] Create AdminDashboard component (frontend/src/components/admin/AdminDashboard.jsx with product list and actions)
- [ ] T070 [P] [US3] Create ProductList component (frontend/src/components/admin/ProductList.jsx displaying all products with edit/delete buttons)
- [ ] T071 [P] [US3] Create ProductForm component (frontend/src/components/admin/ProductForm.jsx for create/edit with all fields)
- [ ] T072 [P] [US3] Create ImageUpload component (frontend/src/components/admin/ImageUpload.jsx with drag-drop, preview, validation)
- [ ] T073 [US3] Create auth service for frontend (frontend/src/services/authService.js with login, logout, getCurrentUser API calls)
- [ ] T074 [US3] Update product service with admin methods (frontend/src/services/productService.js add createProduct, updateProduct, deleteProduct, uploadImage)
- [ ] T075 [US3] Implement AdminPage component (frontend/src/pages/AdminPage.jsx with login gate, dashboard, product management)
- [ ] T076 [US3] Add form validation utilities (frontend/src/utils/validators.js for product name, price, description, image validation)
- [ ] T077 [P] [US3] Add admin panel CSS styling (frontend/src/components/admin/*.module.css for all admin components)
- [ ] T078 [US3] Implement protected route wrapper (update frontend/src/App.jsx to require authentication for /admin route)
- [ ] T079 [US3] Add loading and error states to admin forms (update ProductForm, ImageUpload with LoadingSpinner, ErrorMessage)
- [ ] T080 [US3] Add success notifications for admin actions (create toast/notification component, integrate into admin workflows)

**Checkpoint**: All three user stories should now be independently functional - customers can browse/navigate, admins can manage content

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T081 [P] Create Header component (frontend/src/components/common/Header.jsx with site title, responsive design)
- [ ] T082 [P] Create Footer component (frontend/src/components/common/Footer.jsx with copyright, links)
- [ ] T083 [P] Implement image lazy loading (update ProductCard to use Intersection Observer for images)
- [ ] T084 [P] Add loading skeletons for product grid (create skeleton components for better perceived performance)
- [ ] T085 [P] Optimize images on upload (ensure backend/src/services/image_service.py creates multiple sizes: thumbnail, medium, full)
- [ ] T086 [P] Add MongoDB indexes (verify backend/src/scripts/seed_data.py creates indexes on category, displayOrder, createdAt)
- [ ] T087 [P] Implement error boundary (frontend/src/components/ErrorBoundary.jsx for React error handling)
- [ ] T088 [P] Add request logging (backend/src/main.py add middleware for request/response logging)
- [ ] T089 [P] Configure CORS properly (update backend/src/main.py with production CORS settings)
- [ ] T090 [P] Add rate limiting to admin endpoints (backend/src/middleware/rate_limit.py using SlowAPI)
- [ ] T091 [P] Create comprehensive README (README.md at project root with setup, architecture, deployment instructions)
- [ ] T092 [P] Add API health check endpoint (backend/src/routers/health.py with GET /api/health)
- [ ] T093 Run full test suite and ensure 80% coverage (pytest --cov=backend/src for backend, npm run test:coverage for frontend)
- [ ] T094 Validate WCAG 2.1 Level AA compliance (use axe-core or Lighthouse to audit, fix accessibility issues)
- [ ] T095 Performance testing and optimization (verify <3s page load, <200ms API p95, optimize as needed)
- [ ] T096 Run quickstart.md validation (follow quickstart guide end-to-end, update any outdated steps)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3, 4, 5)**: All depend on Foundational phase completion
  - US1 (Browse Products): Can start after Foundational - No dependencies on other stories
  - US2 (Navigation): Depends on US1 completion (needs product display to navigate)
  - US3 (Admin): Can start after Foundational - Parallel to US1, independent testing possible
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Browse Products)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2 - Navigation)**: Depends on US1 (needs CategorySection components with IDs)
- **User Story 3 (P1 - Admin)**: Can start after Foundational (Phase 2) - Independent of US1/US2 for implementation, but needs US1 complete to verify changes appear

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- Schemas before models (Pydantic schemas define model structure)
- Models before services (services use models)
- Services before routers (routers call services)
- Backend API before frontend integration
- Components before pages (pages compose components)
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes:
  - US1 tests can all run in parallel (T025-T030)
  - US1 backend tasks can run in parallel: Schemas (T031-T032), Models (T033-T034)
  - US1 frontend components can run in parallel: ProductCard (T037), CategorySection (T038), ProductGrid (T039)
  - US3 can start in parallel with US1 (independent admin functionality)
- Within US3: Tests (T054-T061) can run in parallel, then schemas/components can run in parallel
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch all tests for User Story 1 together:
Task: "Contract test for GET /api/categories in backend/tests/contract/test_products_api.py"
Task: "Contract test for GET /api/products in backend/tests/contract/test_products_api.py"
Task: "Contract test for GET /api/products/{id} in backend/tests/contract/test_products_api.py"
Task: "Integration test for public product browsing flow in backend/tests/integration/test_product_flow.py"
Task: "Unit test for ProductCard component in frontend/tests/components/ProductCard.test.jsx"
Task: "Integration test for homepage product display in frontend/tests/integration/userFlows.test.jsx"

# Then launch all schemas in parallel:
Task: "Create Pydantic schemas for Category entity in backend/src/schemas/product.py"
Task: "Create Pydantic schemas for Product entity in backend/src/schemas/product.py"

# Then launch all models in parallel:
Task: "Create MongoDB model for Category entity in backend/src/models/category.py"
Task: "Create MongoDB model for Product entity in backend/src/models/product.py"

# After models complete, launch frontend components in parallel:
Task: "Create ProductCard component in frontend/src/components/customer/ProductCard.jsx"
Task: "Create CategorySection component in frontend/src/components/customer/CategorySection.jsx"
Task: "Create ProductGrid component in frontend/src/components/customer/ProductGrid.jsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Browse Products)
4. **STOP and VALIDATE**: Test User Story 1 independently - customers can view all products
5. Deploy/demo if ready (read-only catalog)

This gives you a working tea catalog website that customers can browse.

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - browsing catalog!)
3. Add User Story 2 → Test independently → Deploy/Demo (navigation enhancement)
4. Add User Story 3 → Test independently → Deploy/Demo (admin can manage content)
5. Add Polish (Phase 6) → Final QA → Production release
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (CRITICAL BLOCKING PHASE)
2. Once Foundational is done:
   - **Developer A**: User Story 1 (Browse Products) - Backend + Frontend
   - **Developer B**: User Story 3 (Admin Panel) - Can work in parallel with US1
3. After US1 complete:
   - **Developer C**: User Story 2 (Navigation) - Depends on US1
4. Stories complete and integrate independently

**Important**: US3 (Admin) can be developed in parallel with US1, but final validation requires US1 to be complete (to verify admin changes appear on public site).

---

## Notes

- [P] tasks = different files, no dependencies - can be executed in parallel
- [Story] label maps task to specific user story for traceability (US1, US2, US3)
- Each user story should be independently completable and testable
- **TDD is mandatory per constitution**: Write tests first, verify they fail, then implement
- Stop at any checkpoint to validate story independently
- Verify tests fail before implementing (Red-Green-Refactor cycle)
- Commit after each task or logical group
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Total tasks: 96 (8 setup, 16 foundational, 20 US1, 9 US2, 27 US3, 16 polish)
