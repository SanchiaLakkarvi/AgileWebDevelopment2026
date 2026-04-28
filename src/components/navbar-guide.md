# Navbar Component Guide

## Overview
The navbar is rendered by `src/components/navbar.js` and styled by `src/styles/global.css`.

Add one mount node in your page body:

```html
<div data-navbar data-active="forum"></div>
```

`navbar.js` will inject Bootstrap navbar markup into this node.

## Files
- `src/components/navbar.js`: navbar render logic
- `src/styles/global.css`: shared navbar styles

## Prerequisites
Include these assets in every page:

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
<link rel="stylesheet" href="/static/styles/global.css" />

<script src="/static/components/navbar.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

## Supported Attributes
### `data-navbar`
Required. Marks the mount target.

### `data-active`
Optional but recommended. Highlights active menu item.

Supported values:
- `home`
- `forum`
- `marketplace`
- `login`

## Current Links
`navbar.js` currently routes to Flask paths:
- `/`
- `/forum`
- `/marketplace`
- `/login`

If you change backend routes, update the `links` array in `navbar.js`.

## Troubleshooting
### Navbar does not render
- Check mount node exists.
- Check `navbar.js` path is correct.
- Check browser console for JS errors.

### Mobile toggler does not open
- Ensure Bootstrap bundle JS is loaded.

### Active tab not highlighted
- Ensure `data-active` matches a `links[].key`.
