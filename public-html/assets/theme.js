/* Run before the stylesheet to restore the selected theme without a flash. */
(function () {
  "use strict";
  let theme = "dark";
  try {
    if (localStorage.getItem("alejandria-theme") === "light") theme = "light";
  } catch (_) { /* The site also works when browser storage is unavailable. */ }
  document.documentElement.dataset.theme = theme;
  document.querySelector('meta[name="theme-color"]').content = theme === "light" ? "#f4f6fb" : "#10131c";
}());
