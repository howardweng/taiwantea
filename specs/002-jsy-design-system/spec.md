# Feature Specification: JSY Tea Design System Implementation

**Feature ID**: 002-jsy-design-system
**Status**: Planning
**Created**: 2025-10-12
**Based On**: Analysis of https://www.jsy-tea.com/

## 1. Overview

Redesign the TAIWANTEA e-commerce platform to match the professional, clean aesthetic of JSY Tea's website while maintaining our existing functionality and improving user experience.

## 2. Goals

### Primary Goals
- Implement JSY Tea's refined color palette and typography
- Adopt their proven product grid layout system
- Enhance mobile responsiveness with their breakpoint strategy
- Improve visual hierarchy and readability

### Success Metrics
- Maintain 100% feature parity with current platform
- Achieve similar visual aesthetic to JSY Tea
- Improve mobile conversion rate by 15%
- Maintain <3s page load time
- Keep accessibility at WCAG 2.1 AA level

## 3. Design System Analysis

### 3.1 Color Palette

**Primary Colors**:
```css
--primary-green: #008264;      /* CTAs, links, highlights */
--sale-red: #c0392b;          /* Sale prices, special tags */
--text-primary: #333333;      /* Body text */
--text-secondary: #666666;    /* Supporting text */
--bg-white: #ffffff;          /* Backgrounds, cards */
--bg-light: #f8f8f8;         /* Footer, sections */
--bg-secondary: #fafffe;     /* Dropdowns, panels */
--border-gray: #e0e0e0;      /* Borders, dividers */
```

**Migration Plan**:
- Current TAIWANTEA primary: `#2d5016` → New: `#008264`
- Update all CSS variables in `frontend/src/styles/variables.css`
- Update button backgrounds, link colors, hover states

### 3.2 Typography

**Font Stack**:
```css
font-family: 'Noto Sans TC', 'Source Sans Pro', 'Open Sans',
             'Helvetica Neue', Helvetica, Arial, sans-serif;
```

**Font Sizes**:
- Base: `16px`
- Small: `14px` (product prices, meta)
- Extra Small: `12px` (labels, tags)
- Large: `18px` (headings on mobile)
- Extra Large: `24px` - `32px` (page titles)

**Font Weights**:
- Regular: `400` (body text)
- Medium: `500` (labels)
- Semi-Bold: `600` (buttons, emphasis)
- Bold: `700` (headings)

**Line Heights**:
- Body: `1.5`
- Headings: `1.4`
- Tight: `1.2` (compact layouts)

### 3.3 Spacing System

**8-Point Grid**:
```css
--space-xs: 8px;
--space-sm: 16px;
--space-md: 24px;
--space-lg: 32px;
--space-xl: 48px;
--space-2xl: 64px;
```

**Component Spacing**:
- Product card padding: `15px` (desktop), `8px` (mobile)
- Section padding: `40px` vertical
- Container margins: `20px` bottom

### 3.4 Product Grid Layout

**Breakpoints & Columns**:
- Mobile (`< 480px`): 2 columns (50% width)
- Small Tablet (`480px - 750px`): 3 columns (33.33% width)
- Desktop (`> 750px`): 4 columns (25% width)

**Product Card Specs**:
- Aspect ratio: 1:1 square
- Image fit: `object-fit: contain`
- Title: 2-line clamp with ellipsis
- Info height: Fixed `60px`
- Hover: Show second image (if available)

### 3.5 Component Patterns

**Buttons**:
```css
.btn-primary {
  background: #008264;
  color: white;
  padding: 8px 24px;
  border-radius: 4px;
  font-weight: 600;
  min-width: 100px;
}
```

**Product Card**:
```jsx
<div className="product-card">
  <div className="product-image-wrapper"> {/* 1:1 aspect ratio */}
    <img src={thumbnailUrl} loading="lazy" />
    {badge && <span className="badge">{badge}</span>}
  </div>
  <div className="product-info"> {/* 60px height */}
    <h3 className="product-title">{name}</h3> {/* 2-line clamp */}
    <div className="product-price">
      {salePrice ? (
        <>
          <span className="price-sale">${salePrice}</span>
          <span className="price-regular">${price}</span>
        </>
      ) : (
        <span className="price">${price}</span>
      )}
    </div>
  </div>
</div>
```

**Navigation**:
- Fixed top navigation with white background
- Border bottom: `1px solid #e0e0e0`
- Logo: Left-aligned
- Menu: Center (desktop) / Hamburger (mobile)
- Cart/Account: Right-aligned

## 4. User Stories

### User Story 1: Enhanced Visual Design
**As a** customer
**I want** a clean, professional website design
**So that** I trust the brand and enjoy shopping

**Acceptance Criteria**:
- All pages use new color palette
- Typography is consistent throughout
- Spacing follows 8-point grid
- Mobile responsive at all breakpoints

### User Story 2: Improved Product Browsing
**As a** customer
**I want** clear, organized product displays
**So that** I can quickly find and compare teas

**Acceptance Criteria**:
- 4-column grid on desktop
- 2-column grid on mobile
- 1:1 aspect ratio product images
- 2-line product titles with ellipsis
- Clear pricing with sale indicators

### User Story 3: Better Mobile Experience
**As a** mobile user
**I want** optimized layouts and touch targets
**So that** I can easily browse on my phone

**Acceptance Criteria**:
- Touch targets minimum 44x44px
- Responsive breakpoints at 480px, 768px, 992px
- Mobile-optimized navigation
- Readable text at all sizes

### User Story 4: Professional Admin Interface
**As an** admin
**I want** the admin panel to match the new design
**So that** the experience is consistent

**Acceptance Criteria**:
- Admin uses same color palette
- Typography matches frontend
- Forms and inputs styled consistently
- Dashboard cards use new design system

## 5. Technical Requirements

### 5.1 Frontend Changes

**CSS Variables** (`frontend/src/styles/variables.css`):
```css
:root {
  /* Colors */
  --color-primary: #008264;
  --color-sale: #c0392b;
  --color-text-primary: #333333;
  --color-text-secondary: #666666;
  --color-bg-white: #ffffff;
  --color-bg-light: #f8f8f8;
  --color-bg-secondary: #fafffe;
  --color-border: #e0e0e0;

  /* Typography */
  --font-family-base: 'Noto Sans TC', 'Source Sans Pro', sans-serif;
  --font-size-base: 16px;
  --font-size-sm: 14px;
  --font-size-xs: 12px;
  --font-size-lg: 18px;
  --font-size-xl: 24px;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --line-height-base: 1.5;
  --line-height-heading: 1.4;

  /* Spacing */
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 24px;
  --space-lg: 32px;
  --space-xl: 48px;

  /* Borders */
  --border-radius-sm: 3px;
  --border-radius-md: 4px;
  --border-radius-lg: 6px;

  /* Breakpoints */
  --breakpoint-mobile: 480px;
  --breakpoint-tablet: 768px;
  --breakpoint-desktop: 992px;
}
```

**Components to Update**:
- `ProductCard.jsx` - Update layout to 1:1 aspect ratio, 2-line title
- `CategorySection.jsx` - Update grid to 4-column desktop
- `ProductGrid.module.css` - Implement new spacing
- `Navigation.jsx` - Update header design
- `HomePage.jsx` - Apply new section layouts
- All button components - Update to new button styles

### 5.2 Design System Documentation

**Create New Files**:
- `frontend/src/styles/design-system.css` - Core design tokens
- `docs/DESIGN_SYSTEM.md` - Design system documentation
- `frontend/src/components/design-system/` - Storybook components (optional)

### 5.3 Font Loading

**Add Google Fonts**:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 5.4 Image Optimization

**Product Images**:
- Aspect ratio: 1:1 (square)
- Minimum size: 600x600px
- Format: WebP with JPEG fallback
- Lazy loading: Enabled
- Alt text: Required for accessibility

## 6. Implementation Phases

### Phase 1: Foundation (Week 1)
**Goal**: Establish design system foundation

**Tasks**:
- Create new CSS variables file
- Update global styles
- Add Google Fonts
- Document design system
- Create component style guide

**Deliverables**:
- `frontend/src/styles/variables.css` (updated)
- `frontend/src/styles/design-system.css` (new)
- `docs/DESIGN_SYSTEM.md` (new)

### Phase 2: Components (Week 2)
**Goal**: Update all UI components

**Tasks**:
- Update ProductCard component
- Update button components
- Update form inputs
- Update navigation
- Update loading states

**Deliverables**:
- Updated component files
- Updated module CSS files
- Component screenshots for comparison

### Phase 3: Pages (Week 3)
**Goal**: Apply design system to all pages

**Tasks**:
- Update HomePage
- Update CategorySection
- Update ProductGrid
- Update ProductDetail page
- Update Admin pages

**Deliverables**:
- All pages using new design system
- Responsive at all breakpoints
- Visual regression tests passing

### Phase 4: Polish & Testing (Week 4)
**Goal**: Refine details and ensure quality

**Tasks**:
- Mobile optimization
- Performance testing
- Accessibility audit
- Cross-browser testing
- User acceptance testing

**Deliverables**:
- Performance report
- Accessibility report
- Bug fixes completed
- Production deployment

## 7. Testing Strategy

### 7.1 Visual Regression Testing
- Capture screenshots before/after
- Compare at all breakpoints
- Test hover/active states
- Verify color consistency

### 7.2 Responsive Testing
- Test at 320px, 375px, 768px, 1024px, 1920px
- Verify touch targets on mobile
- Test landscape/portrait orientations
- Verify navigation on all devices

### 7.3 Accessibility Testing
- Run axe DevTools audit
- Test keyboard navigation
- Verify color contrast (WCAG AA)
- Test with screen readers

### 7.4 Performance Testing
- Lighthouse score > 90
- First Contentful Paint < 1.5s
- Largest Contentful Paint < 2.5s
- Cumulative Layout Shift < 0.1

## 8. Rollout Plan

### Stage 1: Development (Internal)
- Implement on development branch
- Internal team review
- Fix critical issues

### Stage 2: Staging (Beta)
- Deploy to staging environment
- Beta user testing (10-20 users)
- Collect feedback
- Performance monitoring

### Stage 3: Production (Gradual)
- Deploy to production
- Monitor analytics
- Watch for errors/issues
- Iterate based on feedback

### Stage 4: Completion
- Full rollout complete
- Documentation updated
- Team training completed
- Celebrate! 🎉

## 9. Risks & Mitigations

### Risk 1: Breaking Changes
**Impact**: High
**Likelihood**: Medium
**Mitigation**:
- Comprehensive testing suite
- Feature flags for gradual rollout
- Quick rollback plan

### Risk 2: Performance Degradation
**Impact**: High
**Likelihood**: Low
**Mitigation**:
- Performance budgets
- Lazy loading
- Image optimization
- CDN for fonts

### Risk 3: User Confusion
**Impact**: Medium
**Likelihood**: Medium
**Mitigation**:
- Maintain familiar navigation patterns
- Keep key features in same locations
- Provide user feedback channels

### Risk 4: Timeline Slippage
**Impact**: Medium
**Likelihood**: Medium
**Mitigation**:
- Buffer time in schedule
- Prioritize must-have features
- Regular progress reviews

## 10. Success Criteria

### Design Quality
- [ ] All pages match JSY Tea aesthetic
- [ ] Color palette consistently applied
- [ ] Typography hierarchy clear
- [ ] Spacing follows 8-point grid

### Functionality
- [ ] All existing features work
- [ ] No regressions in functionality
- [ ] Admin panel fully functional
- [ ] Payment flow unaffected

### Performance
- [ ] Lighthouse score ≥ 90
- [ ] Page load < 3s
- [ ] No layout shifts
- [ ] Mobile performance optimal

### User Experience
- [ ] Mobile usability improved
- [ ] Product browsing enhanced
- [ ] Navigation intuitive
- [ ] Checkout flow smooth

### Accessibility
- [ ] WCAG 2.1 AA compliant
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast passes

## 11. Future Enhancements

### Phase 5: Advanced Features (Future)
- Product image zoom
- 360° product views
- Video product demos
- AR try-on features
- Product comparison tool
- Advanced filtering
- Wishlist sharing
- Social shopping features

### Phase 6: Personalization (Future)
- Personalized recommendations
- Recently viewed products
- Saved filters
- Custom product bundles
- Loyalty program integration

## 12. References

- JSY Tea Website: https://www.jsy-tea.com/
- Downloaded Files: `/home/datavan/METROPIA/TAIWANTEA/www.jsy_tea.com/`
- Design Analysis: [Design System Analysis Report]
- Current TAIWANTEA: http://localhost:5173

---

**Approved By**: [Pending]
**Start Date**: [TBD]
**Target Completion**: 4 weeks from start
