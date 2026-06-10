const DOMAIN = "custom_local_icons";

const ICON_STORE = {};
const ICON_PROMISES = {};

const VALID_ICON_NAME = /^[a-zA-Z0-9_/-]+$/;

const VIEWBOX = "0 0 24 24";

const EMPTY_ICON = {
  viewBox: VIEWBOX,
  path: "",
};

let DEBUG = false;

/**
 * Integration info
 */
async function logIntegrationInfo() {
  const badgeStyle =
    "color: white; background: linear-gradient(90deg, #41BDF5, #2C6ECB);" +
    "padding: 2px 8px; font-weight: bold; border-radius: 0px;";

  const errorStyle =
    "color:#ef4444;font-weight:700;";

  const fallbackStyle =
    "background:#374151;color:white;padding:2px 8px;border-radius:4px;";

  try {
    const res = await fetch(`/${DOMAIN}/info`);

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const info = await res.json();

    DEBUG = info?.debug === true;

    const { name, version, description, url, path, svg_count } = info;

    console.groupCollapsed(
      `%c🏠🎨 ${name} is installed %c✨${version}`,
      badgeStyle,
      badgeStyle
    );

    console.log("💬", description);
    console.log("📄 Readme: %s", url);
    console.log("🐞 Frontend debug mode:", DEBUG);

    if (DEBUG) {
      const base = window.location.origin;

      console.log("📁 Path:", path);
      console.log("📦 Icons:", svg_count);
      console.log("ℹ️ Integration info: %s", `${base}/${DOMAIN}/info`);
      console.log("📋 Icon list: %s", `${base}/${DOMAIN}/list`);
    }
    console.groupEnd();

    return info;
  } catch (err) {
    console.groupCollapsed(
      `%c⚠️ ${DOMAIN} - Failed to load integration info`,
      errorStyle
    );

    console.error(err);
    console.groupEnd();

    console.info(
      `%c🧩 ${DOMAIN} loaded (no metadata available)`,
      fallbackStyle
    );

    return null;
  }
}

/**
 * Cached integration info
 */
const INFO_PROMISE = logIntegrationInfo();

/**
 * Parse + sanitize SVG into CLI icon format
 */
const preProcessIcon = async (iconName) => {
  const [icon] = iconName.split("#");

  if (!icon || icon.includes("..") || !VALID_ICON_NAME.test(icon)) {
    console.warn(`[${DOMAIN}] Invalid icon name: ${icon}`);
    return null;
  }

  const response = await fetch(`/${DOMAIN}/icons/${icon}.svg`);
  if (!response.ok) {
    console.warn(`[${DOMAIN}] Failed to load icon: ${icon}`);
    return null;
  }

  const text = await response.text();
  const doc = new DOMParser().parseFromString(text, "image/svg+xml");
  const svg = doc.querySelector("svg");

  if (!svg) {
    console.warn(`[${DOMAIN}] Invalid SVG icon: ${icon}`);
    return null;
  }

  if (svg.querySelector("script")) {
    console.warn(`[${DOMAIN}] Blocked scripted SVG: ${icon}`);
    return null;
  }

  const hasEventHandlers = Array.from(svg.querySelectorAll("*")).some((el) =>
    Array.from(el.attributes).some((attr) =>
      attr.name.toLowerCase().startsWith("on")
    )
  );

  if (hasEventHandlers) {
    console.warn(`[${DOMAIN}] Blocked unsafe SVG: ${icon}`);
    return null;
  }

  /**
   * ViewBox deviation logging in debug
   */
  const viewBox = svg.getAttribute("viewBox") || VIEWBOX;

  let path = "";
  for (const p of svg.querySelectorAll("path")) {
    const d = p.getAttribute("d");
    if (d) path += d;
  }

  if (!path) {
    console.warn(`[${DOMAIN}] SVG contains no usable paths: ${icon}`);
    return null;
  }

  if (DEBUG && viewBox !== VIEWBOX) {

    console.debug(
      `[${DOMAIN}] viewBox deviation in ${icon}: ${viewBox} (expected ${VIEWBOX}) | path length: ${path.length}`
    );
  }


  return { viewBox, path };
};

/**
 * Cache-first icon resolver.
 */
const getIcon = (iconName) => {
  // 1. fast path: already ready
  const cached = ICON_STORE[iconName];
  if (cached) return cached;

  // 2. if already loading, just return EMPTY_ICON
  const pending = ICON_PROMISES[iconName];
  if (pending) return EMPTY_ICON;

  // 3. start load exactly once
  ICON_PROMISES[iconName] = preProcessIcon(iconName)
    .then((icon) => {
      if (icon) {
        ICON_STORE[iconName] = icon;
      }
      return icon;
    })
    .finally(() => {
      // cleanup so future reload attempts are possible if needed
      delete ICON_PROMISES[iconName];
    });

  return EMPTY_ICON;
};

/**
 * Icon list
 */
const getIconList = async () => {
  const response = await fetch(`/${DOMAIN}/list`);

  if (!response.ok) {
    console.warn(`[${DOMAIN}] Failed to fetch icon list`);
    return [];
  }

  const info = (await INFO_PROMISE) || {};
  const { svg_count, path } = info;

  const icons = await response.json();

  console.info(
    `[${DOMAIN}] Loaded ${svg_count} icons from ${path}`
  );

  return icons;
};

/**
 * Warm cache
 */
getIconList().then((list) => {
  list.forEach(({ name }) => getIcon(name));
});

/**
 * Expose API
 */
window.getIcon = getIcon;
window.getIconList = getIconList;

window.customIcons ??= {};
window.customIcons.cli = {
  getIcon,
  getIconList,
};
