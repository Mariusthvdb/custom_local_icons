[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![GH-release](https://img.shields.io/github/v/release/Mariusthvdb/custom_local_icons.svg?style=flat-square)](https://github.com/Mariusthvdb/custom_local_icons/releases)
[![GH-downloads](https://img.shields.io/github/downloads/Mariusthvdb/custom_local_icons/total?style=flat-square)](https://github.com/Mariusthvdb/custom_local_icons/releases)
[![GH-last-commit](https://img.shields.io/github/last-commit/Mariusthvdb/custom_local_icons.svg?style=flat-square)](https://github.com/Mariusthvdb/custom_local_icons/commits/master)
[![GH-code-size](https://img.shields.io/github/languages/code-size/Mariusthvdb/custom_local_icons.svg?color=red&style=flat-square)](https://github.com/Mariusthvdb/custom_local_icons)

![icon](https://github.com/user-attachments/assets/45507839-3aef-4682-9957-f27501ba883e)

# Custom Local Icons

A Home Assistant custom component for loading and displaying custom SVG icons from your local filesystem. Perfect for adding organization-specific, branded, or personalized icons to your Home Assistant UI.

## Features

- 🎨 **Custom SVG Icons** - Load any SVG icons from your local filesystem
- 🔒 **Security First** - Strict SVG validation prevents script injection and malicious content
- ⚡ **Caching** - Icons are cached in memory for optimal performance
- 🎯 **Easy Setup** - Simple config flow with folder path configuration
- 🌐 **Frontend Integration** - Seamlessly integrated with Home Assistant's icon system
- 📱 **Responsive** - Works across all Home Assistant interfaces

## Installation

### Via HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Mariusthvdb&repository=custom_local_icons)

or:
1. Open HACS in your Home Assistant instance
2. Click on "Custom repositories"
3. Add `https://github.com/Mariusthvdb/custom_local_icons` as a custom repository with category "Integration"
4. Search for "Custom Local Icons" and click Install
5. Restart Home Assistant

### Manual Installation
1. Download the latest release
2. Copy the `custom_local_icons` folder to your Home Assistant `custom_components` directory:
   ```
   /config/custom_components/custom_local_icons
   ```
3. Restart Home Assistant

## Configuration

### Setup
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=custom_local_icons)

or:
1. Go to **Settings → Devices & Services**
2. Click **Add Integration** (or search for "Custom Local Icons")
3. Select "Custom Local Icons"
4. Enter your icon folder path (default: `www/custom_local_icons`)
5. Click **Create Entry**

### Icon Folder Structure

Create your icon folder in your Home Assistant config directory:

```
/config/www/custom_local_icons/
├── icon1.svg
├── icon2.svg
├── subfolder/
│   ├── icon3.svg
│   └── icon4.svg
```

Icons are referenced using the following naming convention:
- `icon1` for `/config/www/custom_local_icons/icon1.svg`
- `subfolder/icon3` for `/config/www/custom_local_icons/subfolder/icon3.svg`

## Usage

### In YAML
```yaml
lovelace:
  dashboards:
    ui-cctv:
      mode: yaml
      filename: ui-cctv.yaml
      title: Cameras
      icon: cli:home-video
```

### Icon Format
Use the prefix `cli:` followed by your icon name:
```
cli:icon_name
cli:subfolder/icon_name
```

## SVG Requirements

Your SVG files should follow these guidelines:

1. **Valid SVG Format** - Must be valid XML
2. **Viewbox Attribute** - Should include a `viewBox` attribute (defaults to `0 0 24 24`)
3. **Path Elements** - Use `<path>` elements for icon shapes
4. **No Scripts** - Embedded `<script>` tags are blocked for security
5. **No Event Handlers** - Event handlers (`onclick`, `onload`, etc.) are blocked
6. **Safe Content** - Only path data is extracted and rendered

### Example SVG
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
</svg>
```

## Security

This component includes multiple layers of security:

- **Path Traversal Prevention** - Icon names are validated to prevent directory traversal
- **Script Blocking** - Embedded JavaScript is detected and blocked
- **Event Handler Blocking** - Inline event handlers are removed
- **Strict XML Parsing** - SVGs are parsed as strict XML to prevent injection
- **Safe Path Extraction** - Only `<path>` element data is used

All validation happens on both the backend (Python) and frontend (JavaScript).

## Troubleshooting

### Icons Not Appearing
1. **Check the folder path** - Verify the path in the config entry matches your icon folder
2. **Check file names** - Use lowercase names without spaces
3. **Verify SVG format** - Ensure SVG files are valid XML
4. **Check Home Assistant logs** - Look for error messages in Settings → System → Logs

### Error: "Invalid icon name"
- Icon names can only contain alphanumeric characters, underscores, hyphens, and forward slashes
- Example valid names: `my_icon`, `icon-1`, `folder/icon`

### Error: "Failed to load icon"
- Check that the SVG file exists in the configured folder
- Verify file permissions (Home Assistant must be able to read the file)

### Error: "Blocked scripted SVG"
- Your SVG contains embedded JavaScript or event handlers
- Remove these elements from your SVG file

## Performance

- **Caching** - Icons are cached in the browser to minimize file transfers
- **Lazy Loading** - Icons are only loaded when needed
- **Optimized Parsing** - Efficient SVG processing to extract only necessary data

## Limitations

- SVG icons only (PNG, JPG, and other formats not supported)
- Icons must be located in the specified folder
- File size recommendations: Keep SVG files under 10KB for optimal performance

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

See the LICENSE file for details.

## Support

For issues, questions, or feature requests, please open an issue on [GitHub](https://github.com/Mariusthvdb/custom_local_icons/issues).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history and version information.

---

**Custom Local Icons** - Making Home Assistant icons personal and secure. 🚀
