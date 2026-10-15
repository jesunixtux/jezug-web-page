(function () {
  "use strict";
  const form = document.getElementById("timeline-filters");
  if (!form) return;
  const entries = Array.from(document.querySelectorAll("#timeline-entries .timeline-entry"));
  const status = document.getElementById("timeline-status");
  const empty = document.getElementById("timeline-empty");
  const controls = {year: form.elements.year, case: form.elements.case, type: form.elements.type};
  for (const [key, select] of Object.entries(controls)) {
    const values = new Map(entries.map(entry => [entry.dataset[key], entry.dataset[key + "Label"] || (entry.dataset[key] === "sin-fecha" ? "Sin fecha determinada" : entry.dataset[key])]));
    const sorted = Array.from(values).sort((a, b) => a[1].localeCompare(b[1], "es", {numeric: true}));
    for (const [value, label] of sorted) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      select.append(option);
    }
  }
  form.hidden = false;
  if (!entries.length) {
    form.querySelector("fieldset").disabled = true;
    return;
  }

  function filter(updateUrl) {
    let count = 0;
    for (const entry of entries) {
      const visible = Object.entries(controls).every(([key, select]) => !select.value || entry.dataset[key] === select.value);
      entry.hidden = !visible;
      if (visible) count++;
    }
    status.textContent = count + (count === 1 ? " acontecimiento visible" : " acontecimientos visibles") + " de " + entries.length + ".";
    empty.hidden = count > 0;
    if (updateUrl) {
      const url = new URL(window.location.href);
      for (const [key, select] of Object.entries(controls)) {
        if (select.value) url.searchParams.set(key, select.value); else url.searchParams.delete(key);
      }
      // Avoid keeping an anchor to an event hidden by the selected filters.
      let anchor = url.hash.slice(1);
      try { anchor = decodeURIComponent(anchor); } catch (_) { /* Ignore malformed URL encoding. */ }
      const target = document.getElementById(anchor);
      if (target?.classList.contains("timeline-entry") && target.hidden) url.hash = "";
      try { history.replaceState(null, "", url); } catch (_) { /* file:// may restrict history. */ }
    }
  }
  function readFilters() {
    const params = new URLSearchParams(window.location.search);
    for (const [key, select] of Object.entries(controls)) {
      const value = params.get(key) || "";
      select.value = Array.from(select.options).some(option => option.value === value) ? value : "";
    }
    filter(false);
  }
  form.addEventListener("change", () => filter(true));
  form.addEventListener("reset", event => {
    event.preventDefault();
    Object.values(controls).forEach(select => { select.value = ""; });
    filter(true);
  });
  window.addEventListener("popstate", readFilters);
  readFilters();
}());
