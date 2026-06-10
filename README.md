# Custom Local Icons

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![GH-release](https://img.shields.io/github/v/release/Mariusthvdb/custom_local_icons.svg?style=flat-square)](https://github.com/Mariusthvdb/custom_local_icons/releases)
[![GH-downloads](https://img.shields.io/github/downloads/Mariusthvdb/custom_local_icons/total)](https://github.com/Mariusthvdb/custom_local_icons/releases)
[![GH-last-commit](https://img.shields.io/github/last-commit/Mariusthvdb/custom_local_icons.svg?style=flat-square)](https://github.com/Mariusthvdb/custom_local_icons/commits/master)
[![GH-code-size](https://img.shields.io/github/languages/code-size/Mariusthvdb/custom_local_icons.svg?color=red&style=flat-square)](https://github.com/Mariusthvdb/custom_local_icons)

![icon](https://github.com/user-attachments/assets/45507839-3aef-4682-9957-f27501ba883e)

## ✨ Summary
A Home Assistant custom component for loading and displaying custom SVG icons from your local filesystem. Perfect for adding organization-specific, branded, or personalized icons to your Home Assistant UI.


## ⚡ Features

* 🔍 Icon picker integration for UI selection
* 📂 Load SVG icons from a configurable local folder
* 🔄 Automatic icon discovery
* ⚡ Optimized frontend rendering
* 🛡 Secure SVG parsing


## 📦 Installation

### HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Mariusthvdb&repository=custom_local_icons&category=integration)

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


## ⚙️ Configuration

### Setup
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=custom_local_icons)

or:
1. Go to **Settings → Devices & Services**
2. Click **Add Integration** (or search for "Custom Local Icons")
3. Select "Custom Local Icons"
4. Enter your icon folder path (default: `www/custom_local_icons`)
5. Click **Create Entry**

> The folder can later be changed through the integration's Options menu.

### 📁 Icon Folder Structure

Create your icon folder in your Home Assistant config directory:

```
/config/www/custom_local_icons/
├── icon1.svg
├── icon2.svg
├── subfolder/
│   ├── icon3.svg
│   └── icon4.svg
```

### Icon Format
Use the prefix `cli:` followed by your icon name:
```
cli:icon_name
cli:subfolder/icon_name
```

## 🧭 Usage

### In UI

<img width="598" height="555" alt="icon-picker" src="https://github.com/user-attachments/assets/7ced88e1-ccc0-4c4a-97db-35dd0bb055ad" />


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
on the most versatile card of all, [custom:button-card](https://github.com/custom-cards/button-card)
```
type: custom:button-card
icon: >
  [[[ return states['binary_sensor.rook_co_lekkage'].state === 'off'
      ? 'cli:home-check' : 'mdi:home-alert'; ]]]
```
in a stock entities card:
```
type: entities
title: Custom local icons
entities:
  - entity: switch.light
    name: Light switch
    icon: cli:light-switch
```
or eg in a glance card with [UIX](https://uix.lf.technology/using/entities/) templates

```
type: glance
entities:
  - entity: device_tracker.philips_hue_1
    style: |
      :host {
        --uix-icon:
          {% set con = states(config.entity) %}
          cli:hue-bridge-v2{{'-off' if con == 'not_home'}};
      }
```

## 🔄 Updating Icons
When icons are added, removed, or modified in the filesystem, the changes are **not** automatically reflected in an active Home Assistant session.
To apply updates, use one of the following methods:

### Recommended
Reload the Home Assistant browser tab.
This ensures the icon list and frontend cache are fully re-initialized.

> No Home Assistant restart or integration reload is required.

### Alternative (UIX)
If your setup includes [UIX](https://uix.lf.technology/debugging/cache/?h=clear) support, you can use the `clear_cache` action:
```yaml
action: fire-dom-event
uix:
  action: clear_cache
```

In a [badge](https://www.home-assistant.io/dashboards/badges/):

<img width="189" height="42" alt="clear frontend cache" src="https://github.com/user-attachments/assets/2632d80e-2501-44b0-92f6-025bcbd51995" />

This clears the frontend cache, causing the icon list to be requested again.

```yaml
entity: input_select.theme
show_name: true
show_state: false
icon: mdi:broom
name: Clear Frontend Cache
tap_action: none
hold_action:
  action: fire-dom-event
  uix:
    action: clear_cache
```
### ⚠️ Notes

The backend always reflects the latest filesystem state when /list is requested.
The frontend caches icons for performance and does not continuously poll for changes.
Icon updates are therefore only visible after a view reload or cache clear action.

## ⚡ Performance

* **Frontend caching**
  Icons are cached in memory after first load for instant reuse.
  
* **Loading strategy**
  Icons load asynchronously and render with a safe fallback until available. Frequently used icons are preloaded after initial list retrieval.

## 📄 SVG Requirements

Your SVG files should follow these guidelines:

* **Valid SVG Format** - Must be valid XML
* **Viewbox Attribute** - Used as-is when present. If missing or empty, defaults to 0 0 24 24
* **Path Elements** - Use `<path>` elements for icon shapes
* **No Scripts** - Embedded `<script>` tags are blocked for security
* **No Event Handlers** - Event handlers (`onclick`, `onload`, etc.) are blocked
* **Safe Content** - Only path data is extracted and rendered

### Example SVG

<img width="24" height="24" alt="smile" src="https://github.com/user-attachments/assets/605199e7-9416-449a-8ce5-fe40466ea395" />

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#44739e">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
</svg>
```

## 🛡 Security

SVG content is validated before rendering:

* Blocks `<script>` elements
* Blocks inline event handlers (`on*`)
* Requires valid SVG structure
* Extracts only path data for rendering


## ⚠️ Limitations

* No real-time updates (reload required)
* SVG format only
* Large icon sets may increase initial load time
* Icons must be stored in the configured folder
* Invalid or unsupported icons may appear in the icon list but will not render

## 🧠 Logging & Debugging
Custom Local Icons provides lightweight logging in both backend and frontend.

### Backend logs 🧱
* file access
* API responses
* integration-level issues

### Frontend Debug Logging 🐞

If icons are not loading as expected, enable **Frontend debug logging** in the integration options and open your browser developer console.

Additional information will be displayed, including:

* Integration metadata
* Icon count
* Icon list endpoint
* Integration info endpoint
* SVG viewBox deviations
* Icon loading diagnostics

When disabled:
* only warnings/errors are shown

> Logging is for debugging only and does not reflect final render behavior.

## 🧰 Troubleshooting

### Icons Not Appearing

### 🔍 Icon not showing in picker
Check:
* file is in correct folder
* valid filename (no spaces)
* /list endpoint includes it

### 🎨 Icon appears but does not render
Common causes:
* Complex SVG features (transforms, masks, filters, grouped elements) may render differently because only <path> geometry is extracted.
* complex editor exports (Inkscape / Illustrator)
* missing or unusual viewBox (usually non-fatal)

> Note: Icons may preview correctly in file managers, but frontend rendering depends on simplified SVG path extraction.

### 🚫 Invalid icon name
Allowed:
a-z A-Z 0-9 _ - /

Not allowed:
* spaces
* special characters

### 🔍 Verify Icon Discovery

To view all icons currently detected by the integration, open:

```text
http://<home-assistant>/custom_local_icons/list
```

> The `/custom_local_icons/list` endpoint is provided by the integration and is independent of the configured icon folder.

Example response:

```json
[
  { "name": "home" },
  { "name": "light-switch" },
  { "name": "devices/sensor" }
]
```

Icons can then be referenced as:

```yaml
icon: cli:home
icon: cli:light-switch
icon: cli:devices/sensor
```

### Error: "Invalid icon name"
- Icon names can only contain alphanumeric characters, underscores, hyphens, and forward slashes
- Icon names containing spaces are not supported
- Example valid names: `my_icon`, `icon-1`, `folder/icon`

### Error: "Failed to load icon"
- Check that the SVG file exists in the configured folder
- Verify file permissions (Home Assistant must be able to read the file)

### Error: "Blocked scripted SVG"
- Your SVG contains embedded JavaScript or event handlers
- Remove these elements from your SVG file

> Invalid or unsupported icons may appear in the backend icon /list but will not render in the frontend icon picker or view; a warning is logged in the browser console.
<img width="435" height="47" alt="icon with spaces in name" src="https://github.com/user-attachments/assets/efd3226f-c7dd-42b4-bb16-842d43afcf27" />

In other words:
> The icon list reflects filesystem discovery and may include icons that fail validation or rendering at runtime.

## 🔧 Design notes
This system intentionally separates:
* discovery (backend)
* rendering (frontend)
* validation (runtime best-effort)
This avoids blocking icons from appearing while still protecting rendering stability.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## ⚖️ License

See the [LICENSE](LICENSE) file for details.

## 💬 Support

For issues, questions, or feature requests, please open an issue on [GitHub](https://github.com/Mariusthvdb/custom_local_icons/issues).

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history and version information.

---

**Custom Local Icons** - Making Home Assistant icons personal and secure. 🚀
