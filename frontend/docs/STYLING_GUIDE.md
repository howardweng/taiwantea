# Styling Guide for TAIWANTEA Frontend

## Architecture Overview

This project uses **CSS Modules + CSS Variables** for styling:

- **CSS Variables** (`variables.css`) - Centralized theme tokens
- **CSS Modules** (`*.module.css`) - Scoped component styles
- **Global Styles** (`global.css`) - App-wide base styles

### Benefits

✅ **Centralized theming** - Change colors/spacing in one place
✅ **No style conflicts** - CSS Modules automatically scope styles
✅ **Type-safe** - Works seamlessly with TypeScript
✅ **Fast development** - Vite hot-reloads changes instantly
✅ **Maintainable** - Clear separation between global and local styles

---

## File Structure

```
src/styles/
├── variables.css          # Theme tokens (colors, spacing, fonts)
└── global.css            # Global styles and resets

src/components/
└── ComponentName/
    ├── ComponentName.jsx
    └── ComponentName.module.css  # Component-specific styles
```

---

## How to Change Styles

### Scenario 1: Change Theme Colors

**Where:** `/src/styles/variables.css`

**Example: Make primary color darker**

```css
:root {
  /* OLD */
  --color-primary: #2d5016;

  /* NEW */
  --color-primary: #1a3009;
}
```

**Effect:** Updates automatically across:
- All buttons using `var(--color-primary)`
- All links, badges, highlights
- ProductCard prices
- Navigation active states
- 15+ components instantly

✅ **One file change = entire app updates**

---

### Scenario 2: Change Global Spacing

**Where:** `/src/styles/variables.css`

**Example: Increase padding everywhere**

```css
:root {
  /* OLD */
  --spacing-md: 1rem;      /* 16px */

  /* NEW */
  --spacing-md: 1.5rem;    /* 24px */
}
```

**Effect:** All components using `padding: var(--spacing-md)` get updated automatically

✅ **Consistent spacing maintained automatically**

---

### Scenario 3: Change One Component Style

**Where:** `/src/components/customer/ProductCard.module.css`

**Example: Make ProductCard corners more rounded**

```css
/* OLD */
.card {
  border-radius: var(--border-radius);  /* 8px */
}

/* NEW */
.card {
  border-radius: var(--border-radius-lg);  /* 12px */
}
```

**Effect:** Only ProductCard changes, nothing else affected

✅ **Scoped change, no side effects**

---

### Scenario 4: Change Hover Effect

**Option A: Change globally** (affects all components)

**Where:** `/src/styles/variables.css`
```css
:root {
  /* OLD */
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

  /* NEW */
  --shadow-lg: 0 20px 30px -5px rgba(0, 0, 0, 0.2);
}
```

**Option B: Change specific component** (affects only ProductCard)

**Where:** `/src/components/customer/ProductCard.module.css`
```css
.card:hover {
  /* OLD */
  box-shadow: var(--shadow-lg);

  /* NEW */
  box-shadow: 0 30px 40px -10px rgba(0, 0, 0, 0.3);
}
```

✅ **You control scope: global or local**

---

### Scenario 5: Responsive Changes

**Where:** `/src/styles/variables.css`

**Example: Make all text bigger on mobile**

```css
:root {
  --font-size-base: 1rem;     /* 16px */
}

@media (max-width: 768px) {
  :root {
    --font-size-base: 1.125rem;  /* 18px */
  }
}
```

**Effect:** All text using `font-size: var(--font-size-base)` grows on mobile

✅ **Responsive changes centralized**

---

### Scenario 6: Create Reusable Button Styles

**Where:** `/src/styles/global.css`

**Add utility class:**

```css
.btn-primary {
  background: var(--color-primary);
  color: var(--color-white);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  font-weight: var(--font-weight-semibold);
  transition: var(--transition-base);
}

.btn-primary:hover {
  background: var(--color-primary-dark);
}
```

**Usage in any component:**
```jsx
<button className="btn-primary">Click Me</button>
```

✅ **Consistent buttons without repeating code**

---

## Style Change Workflow

```
User wants to change primary color
    ↓
Edit variables.css (1 file)
    ↓
All CSS files using var(--color-primary) update
    ↓
Vite hot-reloads (no page refresh needed)
    ↓
Changes appear instantly in browser
```

**Time:** 10 seconds

---

## Quick Reference Table

| What to Change | File | Scope | Example |
|----------------|------|-------|---------|
| Colors | `variables.css` | Global | `--color-primary: #1a3009;` |
| Spacing | `variables.css` | Global | `--spacing-md: 1.5rem;` |
| Fonts | `variables.css` | Global | `--font-size-base: 1.125rem;` |
| Shadows | `variables.css` | Global | `--shadow-lg: 0 20px 30px...` |
| Component style | `ComponentName.module.css` | Local | `.card { ... }` |
| Utility classes | `global.css` | Global | `.btn-primary { ... }` |
| Reset/normalize | `global.css` | Global | `body { margin: 0; }` |

---

## Best Practices

### ✅ DO:

**1. Use CSS variables for reusable values**
```css
/* GOOD */
.card {
  padding: var(--spacing-md);
  color: var(--color-text);
  border-radius: var(--border-radius);
}
```

**2. Keep component-specific styles in module files**
```css
/* ProductCard.module.css */
.specialBadge {
  /* Only used in ProductCard */
  position: absolute;
  top: 10px;
  right: 10px;
}
```

**3. Use global classes for common patterns**
```css
/* global.css */
.container {
  max-width: var(--max-width-xl);
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}
```

**4. Follow naming conventions**
```css
/* Component-specific classes use camelCase */
.productCard { }
.imageContainer { }
.priceLabel { }

/* Utility classes use kebab-case */
.btn-primary { }
.text-center { }
.mt-4 { }
```

---

### ❌ DON'T:

**1. Hardcode values**
```css
/* BAD */
.card {
  padding: 16px;
  color: #2d5016;
  border-radius: 8px;
}

/* GOOD */
.card {
  padding: var(--spacing-md);
  color: var(--color-primary);
  border-radius: var(--border-radius);
}
```

**2. Duplicate common styles**
```css
/* BAD - repeated in multiple files */
.card { border-radius: 8px; }
.button { border-radius: 8px; }
.modal { border-radius: 8px; }

/* GOOD - use variable */
.card { border-radius: var(--border-radius); }
.button { border-radius: var(--border-radius); }
.modal { border-radius: var(--border-radius); }
```

**3. Use global styles for component-specific needs**
```css
/* BAD - in global.css */
.productCardPrice {
  font-size: 1.25rem;
}

/* GOOD - in ProductCard.module.css */
.price {
  font-size: var(--font-size-xl);
}
```

---

## Available Design Tokens

### Colors

```css
/* Primary colors */
--color-primary: #2d5016;
--color-primary-light: #5a9436;
--color-primary-dark: #1a3009;

/* Secondary colors */
--color-secondary: #8b4513;
--color-accent: #d4af37;

/* Text colors */
--color-text: #1a1a1a;
--color-text-secondary: #4a4a4a;
--color-text-light: #666666;
--color-text-inverse: #ffffff;

/* Background colors */
--color-background: #ffffff;
--color-background-alt: #f8f9fa;
--color-border: #e0e0e0;

/* Grayscale */
--color-gray-100: #f5f5f5;
--color-gray-200: #e5e5e5;
--color-gray-300: #d4d4d4;
--color-gray-600: #737373;

/* Status colors */
--color-success: #16a34a;
--color-error: #dc2626;
--color-warning: #ea580c;
```

### Typography

```css
/* Font families */
--font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto'...;
--font-family-heading: 'Georgia', serif;

/* Font sizes */
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */

/* Font weights */
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

/* Line heights */
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;
```

### Spacing

```css
--spacing-xs: 0.25rem;   /* 4px */
--spacing-sm: 0.5rem;    /* 8px */
--spacing-md: 1rem;      /* 16px */
--spacing-lg: 1.5rem;    /* 24px */
--spacing-xl: 2rem;      /* 32px */
--spacing-2xl: 3rem;     /* 48px */
--spacing-3xl: 4rem;     /* 64px */
```

### Border Radius

```css
--border-radius-sm: 4px;
--border-radius: 8px;
--border-radius-lg: 12px;
--border-radius-full: 9999px;
```

### Shadows

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1)...;
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)...;
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1)...;
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1)...;
```

### Transitions

```css
--transition-fast: 150ms ease-in-out;
--transition-base: 250ms ease-in-out;
--transition-slow: 350ms ease-in-out;
```

### Breakpoints

```css
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
--breakpoint-2xl: 1536px;
```

---

## Common Patterns

### Container

```jsx
<div className="container">
  {/* Max-width, centered, padded */}
</div>
```

### Grid Layout

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}
```

### Card

```css
.card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  padding: var(--spacing-md);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-base);
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
```

### Button

```css
.button {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  font-weight: var(--font-weight-semibold);
  transition: var(--transition-fast);
  cursor: pointer;
}

.button:hover {
  transform: translateY(-1px);
}
```

---

## Example: Full Rebrand

**Task:** Change entire site to new brand colors

**Step 1:** Update theme colors (2 minutes)
```css
/* variables.css */
:root {
  --color-primary: #new-color;
  --color-secondary: #new-color-2;
  --color-accent: #new-color-3;
}
```

**Step 2:** View changes instantly in browser

**Step 3:** Adjust individual components if needed
```css
/* ProductCard.module.css - if primary is too bright */
.price {
  color: var(--color-primary-dark); /* use darker variant */
}
```

**Total time:** 5-10 minutes for full rebrand

---

## Troubleshooting

### Styles not updating?

1. Check browser DevTools for CSS variable value
2. Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)
3. Check if CSS Module is imported: `import styles from './Component.module.css'`

### Styles conflicting?

- CSS Modules prevent this automatically
- If using global classes, check `global.css` for duplicates

### Variable not working?

```css
/* Make sure variable is defined in :root */
:root {
  --my-variable: value;
}

/* Then use with var() */
.element {
  property: var(--my-variable);
}
```

---

## Further Reading

- [CSS Modules Documentation](https://github.com/css-modules/css-modules)
- [CSS Custom Properties (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Vite CSS Documentation](https://vitejs.dev/guide/features.html#css)

---

## Summary

**Your styling architecture is well-designed and follows industry best practices.**

✅ **Theme changes:** 1 file (`variables.css`)
✅ **Component changes:** 1 file (`ComponentName.module.css`)
✅ **No conflicts:** CSS Modules scope everything
✅ **Fast:** Vite hot-reloads instantly
✅ **Maintainable:** Clear separation of concerns

**Keep using this pattern - it works!**
