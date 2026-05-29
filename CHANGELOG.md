# Changelog

## [0.2.1] - 2026-05-29

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
