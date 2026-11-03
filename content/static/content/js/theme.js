(function () {
    const root = document.documentElement;
    const toggle = document.getElementById("themeToggle");
    const choices = document.querySelectorAll("[data-theme-choice]");
    let savedTheme = null;
    try { savedTheme = localStorage.getItem("tcs-theme"); } catch (error) { /* Browser storage may be unavailable. */ }
    const preferred = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";

    function applyTheme(theme, save) {
        const next = theme === "dark" ? "dark" : "light";
        root.setAttribute("data-theme", next);
        if (toggle) {
            toggle.setAttribute("aria-label", next === "dark" ? "Switch to light mode" : "Switch to dark mode");
            toggle.setAttribute("aria-pressed", next === "dark" ? "true" : "false");
        }
        document.querySelectorAll("[data-theme-choice]").forEach(function (button) {
            button.setAttribute("aria-pressed", button.getAttribute("data-theme-choice") === next ? "true" : "false");
        });
        if (save) { try { localStorage.setItem("tcs-theme", next); } catch (error) { /* Keep the theme for this page view. */ } }
    }

    applyTheme(savedTheme === "light" || savedTheme === "dark" ? savedTheme : preferred, false);
    if (toggle) toggle.addEventListener("click", function () {
        applyTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark", true);
    });
    choices.forEach(function (button) {
        button.addEventListener("click", function () { applyTheme(button.getAttribute("data-theme-choice"), true); });
    });
})();
