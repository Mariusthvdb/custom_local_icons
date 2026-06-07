const DOMAIN = "custom_local_icons";

const ICON_STORE = {};
const ICON_PROMISES = {};

const VALID_ICON_NAME = /^[a-zA-Z0-9_/-]+$/;

/**
 * Integration info
 */
async function logIntegrationInfo() {
  const badgeStyle =
    "color: white; background: linear-gradient(90deg, #41BDF5, #2C6ECB);" +
    "padding: 2px 8px; font-weight: bold; border-radius: 0px;";

  const errorStyle = "color:#ef4444;font-weight:700;";

  const fallbackStyle =
    "background:#374151;color:white;padding:2px 8px;border-radius:4px;";

  try {
    const res = await fetch(`/${DOMAIN}/info`);

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const { name, version, description, url } = await res.json();

    console.groupCollapsed(
      `%c🏠🎨 ${name} is installed %c✨${version}`,
      badgeStyle,
      badgeStyle
    );

    console.log("💬", description);
    console.log("📄 Readme:", url);

    console.groupEnd();

    return { name, version, description, url };
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
 * Parse + sanitize SVG into CLI icon format
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

  return { viewBox, path, format };
};

/**
 * Sync resolver
 */
const getIcon = (iconName) => {
  if (ICON_STORE[iconName]) {
    return ICON_STORE[iconName];
  }

  if (!ICON_PROMISES[iconName]) {
    ICON_PROMISES[iconName] = preProcessIcon(iconName).then((icon) => {
      if (icon) ICON_STORE[iconName] = icon;
      return icon;
    });
  }

  return {
    viewBox: "0 0 24 24",
    path: "",
    format: "mdi",
  };
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

  const icons = await response.json();

  console.info(
    `[${DOMAIN}] Loaded ${icons.length} icons from /${DOMAIN}/list`
  );

  return icons;
};

/**
 * Startup
 */
logIntegrationInfo();

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
window.logIntegrationInfo = logIntegrationInfo;

window.customIcons ??= {};
window.customIcons.cli = {
  getIcon,
  getIconList,
};
