(function () {
  "use strict";

  const storageKey = "scouts-activity-library-theme";
  const media = window.matchMedia("(prefers-color-scheme: dark)");

  function savedTheme() {
    try {
      const value = window.localStorage.getItem(storageKey);
      return value === "light" || value === "dark" ? value : null;
    } catch (_error) {
      return null;
    }
  }

  function preferredTheme() {
    return savedTheme() || (media.matches ? "dark" : "light");
  }

  function setTheme(theme, remember) {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) themeColor.content = theme === "dark" ? "#19171c" : "#7413dc";
    if (remember) {
      try {
        window.localStorage.setItem(storageKey, theme);
      } catch (_error) {
        // Theme switching still works when storage is unavailable.
      }
    }
    document.querySelectorAll("[data-theme-choice]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.themeChoice === theme));
    });
  }

  function buildSelector(host) {
    host.classList.add("theme-switcher");
    host.setAttribute("role", "group");
    host.setAttribute("aria-label", "Colour theme");
    ["light", "dark"].forEach((theme) => {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.themeChoice = theme;
      button.textContent = theme[0].toUpperCase() + theme.slice(1);
      button.addEventListener("click", () => setTheme(theme, true));
      host.append(button);
    });
  }

  function initialiseSelectors() {
    let hosts = [...document.querySelectorAll("[data-theme-selector]")];
    if (!hosts.length) {
      const host = document.createElement("div");
      host.dataset.themeSelector = "";
      host.classList.add("theme-switcher--floating");
      document.body.prepend(host);
      hosts = [host];
    }
    hosts.forEach(buildSelector);
    setTheme(preferredTheme(), false);
  }

  setTheme(preferredTheme(), false);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialiseSelectors, { once: true });
  } else {
    initialiseSelectors();
  }
  media.addEventListener("change", () => {
    if (!savedTheme()) setTheme(preferredTheme(), false);
  });
})();
