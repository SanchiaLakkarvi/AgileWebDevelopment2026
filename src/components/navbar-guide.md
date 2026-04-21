# Navbar Component Guide

## Overview
The navbar is a reusable client-side component rendered by `src/components/navbar.js` and styled via global styles in `src/styles/global.css`.

Instead of hardcoding navbar HTML in each page, pages provide a mount point:

```html
<div data-navbar data-active="forum"></div>
```

The component script finds that element and injects the navbar markup.

## Files
- `src/components/navbar.js`: component logic and HTML rendering
- `src/styles/global.css`: shared project styles (includes navbar styles)

## Prerequisites
Each page that uses the component must include:

1. Bootstrap CSS
2. Global project CSS
3. Navbar component JS
4. Bootstrap JS bundle (for collapse/toggler behavior)

Example:

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
<link rel="stylesheet" href="../../styles/global.css" />

<script src="../../components/navbar.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

## Basic Usage
Add this in the page body where the navbar should appear:

```html
<div data-navbar data-active="home"></div>
```

## Supported Attributes
### `data-navbar`
Required. Marks the mount target for navbar injection.

### `data-active`
Optional but recommended. Controls which nav item appears active.

Supported values in current implementation:
- `home`
- `forum`
- `marketplace`
- `login`

If omitted or invalid, no item will be highlighted as active.

## Current Path Assumption
In `navbar.js`, links are built with a fixed base:

```js
const base = "../";
```

This assumes pages live one level below `src/pages/` (for example `src/pages/Forum/forum.html`).

If you move pages to deeper or different directories, update `base` in `navbar.js`.

## Adding Navbar to a New Page
1. Add Bootstrap CSS link in `<head>`.
2. Add `../../styles/global.css` in `<head>`.
3. Add mount node in `<body>`:
   ```html
   <div data-navbar data-active="home"></div>
   ```
4. Add scripts before `</body>`:
   ```html
   <script src="../../components/navbar.js"></script>
   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
   ```
5. Set correct `data-active` value for that page.

## Updating Links
Navbar links are defined in `navbar.js`:

```js
const links = [ ... ];
```

To update navigation items:
1. Add or edit objects in `links`.
2. Ensure each item has:
   - `key`: unique identifier used by `data-active`
   - `label`: visible text
   - `href`: target URL
3. Update this guide if supported `data-active` values change.

## Troubleshooting
### Navbar does not render
- Check that the page has `<div data-navbar ...></div>`.
- Check `navbar.js` script path is correct.
- Confirm there is no JavaScript error in the console.

### Toggler button does not open menu
- Ensure Bootstrap JS bundle is included.
- Ensure script load order keeps Bootstrap JS available on page.

### Active tab not highlighted
- Check `data-active` exactly matches a `links[].key` value.

### Broken links
- Verify `base` value and page directory structure.

## Maintenance Notes
- Keep component logic in `navbar.js` and shared styles in `global.css`.
- Avoid duplicating navbar markup in individual pages.
- When changing nav structure, test on all pages that mount the component.
