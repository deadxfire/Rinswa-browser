# Rinswa UI Architecture

## UI Architecture
Rinswa's user interface is built on top of Firefox's `browser.html` and XUL/WebComponent foundations. Instead of completely rewriting the DOM structure—which would cause massive merge conflicts with upstream Gecko—Rinswa heavily leverages a CSS-first customization approach alongside built-in Theme API manifests. This ensures we inherit all of Gecko's accessibility, keyboard navigation, tab rendering, and security indicators while presenting a completely original, modern visual language.

## Components Modified
To achieve Rinswa's minimalist aesthetic, we modify the styling and visibility of the following components in the main browser window using our custom CSS layer:
- **Tab Bar (`#TabsToolbar`)**: Padded, borderless tabs with clear active/inactive states. Supports pinned and private tabs natively. Prepared for future vertical tabs via CSS grid restructuring (currently hidden).
- **Navigation Bar (`#nav-bar`)**: Re-spaced to provide a cleaner layout for Back/Forward, URL bar, Home, and extensions. Unnecessary borders and drop shadows are removed.
- **Address Bar (`#urlbar`)**: Custom floating design that expands smoothly on focus. Retains all Gecko security/permission indicators, search suggestions, and reader mode natively.
- **Main Menu / Profile (`#PanelUI-button`)**: Re-styled to fit the modern typographic hierarchy.
- **Downloads & Bookmarks**: Cleaner icon rendering and padded dropdown panels.
- **Window Controls**: Spaced appropriately for Windows, macOS, and Linux native window management.

## Styling System
Rinswa's CSS overrides (`rinswa.css`) rely on CSS variables mapped to our custom color palette and spacing tokens.
- We inject `rinswa.css` directly into `browser.html` during the build process, taking precedence over default Firefox styles.
- Unnecessary visual clutter (e.g., separating lines, excessive drop shadows, old XUL gradient remnants) is stripped via `display: none` or `border: none`.

## Theme Architecture
Rinswa includes built-in Light and Dark themes defined via WebExtension `theme` manifests (located in `ui/themes/`). 
- **Light Theme**: High-contrast, clean white/gray aesthetic with subtle borders.
- **Dark Theme**: Deep grays (not pure black) to reduce eye strain, with soft highlighted active elements.
- **System**: Respects OS-level preferences and toggles the internal theme accordingly.

## Accessibility Considerations
- **Keyboard/Mouse**: We rely on Mozilla's built-in focus management. Focus rings are customized to match Rinswa's accent color but are always visible for keyboard navigation. Hitboxes for mouse users are padded generously.
- **Contrast**: Theme colors strictly adhere to WCAG AA contrast standards.
- **Responsive Layout**: Designed to be highly usable on small screens (1280x720) up to 4K resolutions, maintaining proper padding and font scaling.

## Performance Considerations
- **Animations**: Kept to an absolute minimum. Only critical state changes (e.g., URL bar focus, tab hover) feature subtle micro-animations (e.g., `transition: 150ms ease`).
- **Memory/Startup**: By avoiding heavy JS-based UI frameworks and sticking to pure CSS overrides and native WebComponents, Rinswa adds zero overhead to the browser's startup time or memory footprint. We explicitly do not alter Gecko rendering behavior.
