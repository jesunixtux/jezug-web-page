/* Run before the stylesheet to restore the selected theme without a flash. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");
  let theme = "dark";
  try {
    if (localStorage.getItem("alejandria-theme") === "light") theme = "light";
  } catch (_) { /* The site also works when browser storage is unavailable. */ }
  document.documentElement.dataset.theme = theme;
}());
