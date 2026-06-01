const DOMAIN = "custom_local_icons";

const ICON_STORE = {};
const ICON_PROMISES = {};

const VALID_ICON_NAME = /^[a-zA-Z0-9_/-]+$/;

/**
 * Parse + sanitize SVG into CLI icon format
 * Async ONLY used for background warming
 */
const preProcessIcon = async (iconName) => {
  const [icon, format] = iconName.split("#");

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

  const viewBox = svg.getAttribute("viewBox") || "0 0 24 24";

  let path = "";
  for (const p of svg.querySelectorAll("path")) {
    const d = p.getAttribute("d");
    if (d) path += d;
  }

  if (!path) {
    console.warn(`[${DOMAIN}] SVG contains no usable paths: ${icon}`);
    return null;
  }

  return {
    viewBox,
    path,
    format,
  };
};

/**
 * CRITICAL: synchronous icon resolver (MDI-like behavior)
 * Never returns a Promise.
 */
const getIcon = (iconName) => {
  // 1. already ready → instant
  if (ICON_STORE[iconName]) {
    return ICON_STORE[iconName];
  }

  // 2. start background load (once only)
  if (!ICON_PROMISES[iconName]) {
    ICON_PROMISES[iconName] = preProcessIcon(iconName).then((icon) => {
      if (icon) {
        ICON_STORE[iconName] = icon;
      }
      return icon;
    });
  }

  // 3. ALWAYS return safe placeholder synchronously
  return {
    viewBox: "0 0 24 24",
    path: "",
    format: "mdi",
  };
};

/**
 * Icon list (used by picker)
 */
const getIconList = async () => {
  const response = await fetch(`/${DOMAIN}/list`);

  if (!response.ok) {
    console.warn(`[${DOMAIN}] Failed to fetch icon list`);
    return [];
  }

  return response.json();
};

/**
 * Warm cache at startup (removes Safari/UIX race entirely)
 */
getIconList().then((list) => {
  list.forEach(({ name }) => {
    getIcon(name);
  });
});

/**
 * Expose API globally
 */
window.getIcon = getIcon;
window.getIconList = getIconList;

/**
 * Register CLI icon set synchronously (CRITICAL)
 */
window.customIcons ??= {};

window.customIcons.cli = {
  getIcon,
  getIconList,
};
