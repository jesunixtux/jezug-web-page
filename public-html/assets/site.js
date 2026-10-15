(function () {
  "use strict";
  const root = document.documentElement;
  const themeButton = document.querySelector(".theme-toggle");
  const menuButton = document.querySelector(".menu-toggle");
  const navigation = document.getElementById("site-nav");
  const form = document.querySelector(".searchbar");
  const input = document.getElementById("site-search");
  const results = document.getElementById("search-results");
  const status = document.getElementById("search-status");
  const normalize = value => value.toLocaleLowerCase("es").normalize("NFD").replace(/[\u0300-\u036f]/g, "");

  function updateTheme() {
    const light = root.dataset.theme === "light";
    themeButton.setAttribute("aria-pressed", String(light));
    themeButton.setAttribute("aria-label", light ? "Activar modo oscuro" : "Activar modo claro");
    themeButton.title = themeButton.getAttribute("aria-label");
    document.querySelector('meta[name="theme-color"]').content = light ? "#f4f6fb" : "#10131c";
  }
  themeButton.hidden = false;
  updateTheme();
  themeButton.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "light" ? "dark" : "light";
    try { localStorage.setItem("alejandria-theme", root.dataset.theme); } catch (_) { /* Optional persistence. */ }
    updateTheme();
  });
  window.addEventListener("storage", event => {
    if (event.key === "alejandria-theme") {
      root.dataset.theme = event.newValue === "light" ? "light" : "dark";
      updateTheme();
    }
  });

  menuButton.hidden = false;
  const mobile = window.matchMedia("(max-width: 900px)");
  function closeMenu() {
    const restoreFocus = mobile.matches && navigation.contains(document.activeElement);
    navigation.classList.remove("is-open");
    menuButton.setAttribute("aria-expanded", "false");
    if (restoreFocus) menuButton.focus();
  }
  menuButton.addEventListener("click", () => {
    const open = navigation.classList.toggle("is-open");
    menuButton.setAttribute("aria-expanded", String(open));
  });
  navigation.addEventListener("click", event => {
    if (event.target.closest("a")) closeMenu();
  });
  mobile.addEventListener("change", () => {
    closeMenu();
    if (!mobile.matches && document.activeElement === menuButton) navigation.querySelector("a").focus();
  });
  document.addEventListener("click", event => {
    if (mobile.matches && !navigation.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
  });
  // Collapse navigation only after its controls are wired; it remains usable if this file fails to load.
  root.classList.add("js");
  document.addEventListener("keydown", event => {
    const editing = event.target.closest?.("input, textarea, select, [contenteditable]:not([contenteditable='false'])");
    if (event.key === "/" && !editing && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      input.focus();
    }
    if (event.key === "Escape") {
      if (navigation.classList.contains("is-open")) { closeMenu(); menuButton.focus(); }
      else if (document.activeElement === input) {
        input.value = "";
        if (results) renderSearch(true);
      }
    }
  });

  if (!results) return;
  const index = (window.ALEJANDRIA_SEARCH_INDEX || []).map(entry => ({
    ...entry, normalizedTitle: normalize(entry.title), normalizedText: normalize(entry.text)
  }));

  function excerpt(entry, terms) {
    const positions = terms.map(term => entry.normalizedText.indexOf(term)).filter(position => position >= 0);
    const position = positions.length ? Math.min(...positions) : 0;
    let start = Math.max(0, position - 65);
    if (start) {
      const space = entry.text.indexOf(" ", start);
      if (space >= 0 && space < position) start = space + 1;
    }
    const end = Math.min(entry.text.length, start + 240);
    return (start ? "…" : "") + entry.text.slice(start, end) + (end < entry.text.length ? "…" : "");
  }

  function renderSearch(updateUrl) {
    const query = input.value.trim().slice(0, 200);
    if (updateUrl) {
      const url = new URL(window.location.href);
      if (query) url.searchParams.set("q", query); else url.searchParams.delete("q");
      try { history.replaceState(null, "", url); } catch (_) { /* Some file:// browsers restrict history. */ }
    }
    results.replaceChildren();
    if (!query) {
      status.textContent = "Introduce una consulta en el buscador superior y pulsa Buscar.";
      return;
    }
    const terms = normalize(query).split(/\s+/).filter(Boolean);
    const matches = index.filter(entry => terms.every(term => (entry.normalizedTitle + " " + entry.normalizedText).includes(term)))
      .map(entry => ({ ...entry, score: terms.reduce((total, term) => total + (entry.normalizedTitle.includes(term) ? 3 : 0), 0) }))
      .sort((a, b) => b.score - a.score || a.title.localeCompare(b.title, "es"));
    status.textContent = matches.length
      ? matches.length + (matches.length === 1 ? " resultado encontrado" : " resultados encontrados") + " para «" + query + "»."
      : "Sin resultados para «" + query + "». Prueba con otra palabra, como metodología, fuentes o transparencia.";
    for (const entry of matches) {
      const article = document.createElement("article");
      article.className = "card search-result";
      const label = document.createElement("span");
      label.className = "result-path";
      label.textContent = (entry.kind || "Página") + " / " + entry.title;
      const heading = document.createElement("h3");
      const link = document.createElement("a");
      link.href = root.dataset.root + entry.url;
      link.textContent = entry.title;
      heading.append(link);
      const summary = document.createElement("p");
      summary.textContent = excerpt(entry, terms);
      article.append(label, heading, summary);
      results.append(article);
    }
  }

  function readQuery() {
    input.value = (new URLSearchParams(window.location.search).get("q") || "").slice(0, 200);
    renderSearch(false);
  }
  form.addEventListener("submit", event => { event.preventDefault(); renderSearch(true); });
  let pending;
  input.addEventListener("input", () => { clearTimeout(pending); pending = setTimeout(() => renderSearch(true), 180); });
  window.addEventListener("popstate", readQuery);
  readQuery();
}());
