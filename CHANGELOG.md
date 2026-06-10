# Changelog

## Version [1.4.0] - 2026-06-10

### Added

* Added a new **Frontend Debug Logging** option in the integration options flow.
* Added frontend debug state to the `/custom_local_icons/info` endpoint.
* Added configurable frontend debug logging in `main.js`.
* Added browser console visibility for current frontend debug status.

### Changed

* Refactored folder validation into a shared helper function.
* Improved options flow logging to only report actual configuration changes.
* Added separate logging for folder changes and frontend debug changes.
* Renamed debug option constants to clearly distinguish frontend debugging from Home Assistant integration log levels.
* Updated runtime storage to expose frontend debug configuration to the frontend.
* Improved integration metadata reporting and diagnostics.

### Translations

* Added translation support for the new frontend debug option.
* Added Dutch translations.
* Migrated to a modern translation structure using dedicated translation files.

### Internal

* Cleaned up configuration flow implementation.
* Reduced duplicated validation logic.
* Improved runtime data handling in `__init__.py`.
* Improved consistency of logging and configuration management.
* Refactored path handling to consistently use the resolved icon base path.

## [1.3.1] - 2026-06-09

### ✨ Added
- Clear separation between icon discovery (/list) and rendering pipeline
- Improved troubleshooting documentation for icon picker vs rendering mismatch
- Optional frontend DEBUG mode for SVG parsing diagnostics
- Enhanced logging guidance for backend and frontend

### 🐛 Fixed
- Icons appearing in list but failing to render now properly documented and explained
- Clarified handling of complex SVGs (Inkscape / Illustrator exports)
- Improved consistency in invalid icon name reporting

### ⚠️ Changed
- `/list` endpoint now explicitly considered discovery-only (no render guarantees)
- Rendering pipeline remains best-effort and does not filter discovery results
- SVG rendering limited to `<path>` extraction only (no full SVG feature support)
- Console logs are now explicitly diagnostic-only
  
# [1.2.0] - 2026-06-03

## Added

* Frontend icon preloading to improve icon picker responsiveness.
* Frontend and backend informational logging for icon discovery and troubleshooting.
* Documentation for refreshing icon lists after filesystem changes.
* UIX cache-clear workflow documentation as an alternative to a full browser reload.

## Changed

* Reworked frontend icon loading and caching behavior for improved reliability.
* Icon lists are now always generated from the current filesystem state.
* Updated README with expanded installation, usage, performance, security, and troubleshooting documentation.
* Improved icon picker synchronization after frontend cache refreshes.

## Security

* Continued validation of SVG content before rendering.
* Maintained protection against unsupported SVG scripts and inline event handlers.

## Notes

* Icon additions, removals, and modifications require a browser reload or frontend cache clear before becoming visible in the UI.
* Icons with unsupported names may appear in the icon list but will not render; browser console warnings identify affected files.


## [1.0.0] - 2026-05-29

### Initial Release

**Features:**
- 🎨 Custom Local Icons component for Home Assistant
- Support for loading custom SVG icons from local filesystem
- Web-based icon listing and browsing
- Config flow for easy setup and reconfiguration
- Security-focused SVG parsing with:
  - Script injection prevention
  - Event handler blocking
  - Path traversal protection
  - Strict SVG XML validation

**Components:**
- `__init__.py` - Core async setup/unload with static path configuration
- `config_flow.py` - User configuration interface supporting icon folder paths
- `main.js` - Frontend loader with icon caching and safe SVG processing
- `manifest.json` - Integration metadata (v0.2.1, local_polling)
- `translations/en.json` - English language strings

**Installation:**
1. Copy the `custom_local_icons` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Navigate to Settings > Devices & Services > Create Automation
4. Search for "Custom local icons" and configure your icon folder path (default: `www/custom_local_icons`)

**Security Notes:**
- All SVGs are parsed and validated before use
- Embedded scripts and event handlers are automatically blocked
- Only safe path data is extracted and rendered

**Known Requirements:**
- Home Assistant with frontend and HTTP components
- Valid SVG files in the configured icon folder
