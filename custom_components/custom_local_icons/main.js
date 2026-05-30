const DOMAIN = "custom_local_icons";

const ICON_STORE = {};

const VALID_ICON_NAME = /^[a-zA-Z0-9_/-]+$/;

const preProcessIcon = async (iconName) => {
  const [icon, format] = iconName.split("#");

  // Prevent path traversal or malformed names
  if (
    !icon ||
    icon.includes("..") ||
    !VALID_ICON_NAME.test(icon)
  ) {
    console.warn(`[${DOMAIN}] Invalid icon name: ${icon}`);
    return {};
  }

  const response = await fetch(
    `/${DOMAIN}/icons/${icon}.svg`
  );

  if (!response.ok) {
    console.warn(
      `[${DOMAIN}] Failed to load icon: ${icon}`
    );
    return {};
  }

  const text = await response.text();

  // Parse strictly as SVG XML
  const parser = new DOMParser();
  const doc = parser.parseFromString(
    text,
    "image/svg+xml"
  );

  const svg = doc.querySelector("svg");

  if (!svg) {
    console.warn(
      `[${DOMAIN}] Invalid SVG icon: ${icon}`
    );
    return {};
  }

  // Reject embedded scripts
  if (svg.querySelector("script")) {
    console.warn(
      `[${DOMAIN}] Blocked scripted SVG: ${icon}`
    );
    return {};
  }

  // Reject inline event handlers (onclick, onload, etc.)
  const hasEventHandlers = Array.from(
    svg.querySelectorAll("*")
  ).some((el) =>
    Array.from(el.attributes).some((attr) =>
      attr.name.toLowerCase().startsWith("on")
    )
  );

  if (hasEventHandlers) {
    console.warn(
      `[${DOMAIN}] Blocked unsafe SVG: ${icon}`
    );
    return {};
  }

  const viewBox =
    svg.getAttribute("viewBox") || "0 0 24 24";

  let path = "";

  // Only extract safe <path d="">
  for (const pth of svg.querySelectorAll("path")) {
    const d = pth.getAttribute("d");

    if (d) {
      path += d;
    }
  }

  // Require actual path data
  if (!path) {
    console.warn(
      `[${DOMAIN}] SVG contains no usable paths: ${icon}`
    );
    return {};
  }

  return {
    viewBox,
    path,
    format,
  };
};

const getIcon = async (iconName) => {
  if (ICON_STORE[iconName]) {
    return ICON_STORE[iconName];
  }

  ICON_STORE[iconName] =
    preProcessIcon(iconName);

  return ICON_STORE[iconName];
};

const getIconList = async () => {
  const response = await fetch(
    `/${DOMAIN}/list`
  );

  if (!response.ok) {
    console.warn(
      `[${DOMAIN}] Failed to fetch icon list`
    );
    return [];
  }

  return response.json();
};

window.getIcon = getIcon;
window.getIconList = getIconList;

if (!("customIcons" in window)) {
  window.customIcons = {};
}

window.customIcons["cli"] = {
  getIcon,
  getIconList,
};
