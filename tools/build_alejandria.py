"""Build only the explicitly listed public pages. Never scan the documentary archive."""
from html import escape
from html.parser import HTMLParser
from hashlib import sha256
import json
from pathlib import Path
import re

from alejandria_content import load_dossiers, render_cases, render_dossier, render_timeline, safe_source, event_anchor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site-public"
OUTPUT = ROOT / "public-html"
NAV_IDS = ("inicio", "cronologia", "casos", "evidencias", "metodologia", "fuentes", "transparencia", "buscar")
ICONS = {
    "inicio": '<path d="m3 10 9-7 9 7v11h-7v-7h-4v7H3Z"/>',
    "cronologia": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "casos": '<path d="M3 5h7l2 3h9v12H3Z"/>',
    "evidencias": '<path d="M5 3h10l4 4v14H5ZM14 3v5h5M8 12h8M8 16h6"/>',
    "metodologia": '<circle cx="12" cy="4" r="2"/><circle cx="4" cy="19" r="2"/><circle cx="20" cy="19" r="2"/><path d="m11 6-6 11M13 6l6 11M6 19h12"/>',
    "fuentes": '<path d="M4 4h6c2 0 2 1 2 2v14c0-2-1-2-2-2H4ZM20 4h-6c-2 0-2 1-2 2v14c0-2 1-2 2-2h6Z"/>',
    "transparencia": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>',
    "buscar": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
}


class PublicText(HTMLParser):
    """Extract readable public content, excluding decoration and local navigation."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.ignored = 0
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        skip = tag in {"script", "style", "svg", "nav", "noscript", "form"} or attributes.get("aria-hidden") == "true" or "data-search-exclude" in attributes
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, skip))
            if skip:
                self.ignored += 1
        self.parts.append(" ")

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            _, skip = self.stack.pop()
            if skip:
                self.ignored -= 1
        self.parts.append(" ")

    def handle_data(self, data):
        if not self.ignored:
            self.parts.append(data)


def substitute(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    if "{{" in template:
        raise ValueError("Unresolved template token")
    return template


def render_site(source_dir=SOURCE):
    """Return deterministic output in memory; also used to detect outdated generated files."""
    configured = json.loads((source_dir / "pages.json").read_text(encoding="utf-8"))
    if not isinstance(configured, list):
        raise ValueError("pages.json must be a list")
    pages = []
    for page in configured:
        if type(page.get("public")) is not bool or type(page.get("search")) is not bool:
            raise ValueError("Every page needs explicit public/search boolean authorization")
        if page["public"]:
            pages.append(page)
    dossiers = load_dossiers(source_dir)
    pages.extend({"id": doc["id"], "nav": "casos", "title": doc["title"], "description": doc["description"], "route": doc["route"], "public": True, "search": doc["search"], "doc": doc} for doc in dossiers)
    settings = json.loads((source_dir / "settings.json").read_text(encoding="utf-8"))
    base_path = settings["base_path"]
    if not isinstance(base_path, str) or not re.fullmatch(r"/(?:[a-zA-Z0-9_-]+/)*", base_path):
        raise ValueError("base_path must be / or an absolute subfolder such as /alejandria/")
    layout = (source_dir / "layout.html").read_text(encoding="utf-8")
    dossier_template = (source_dir / "templates/expediente.html").read_text(encoding="utf-8")
    timeline_template = (source_dir / "templates/timeline.html").read_text(encoding="utf-8")
    by_id = {page["id"]: page for page in pages}
    routes = [route for page in pages for route in [page["route"], *page.get("aliases", [])]]
    if len(by_id) != len(pages) or len(set(routes)) != len(routes):
        raise ValueError("Page IDs and routes must be unique")
    if any(not isinstance(route, str) or not re.fullmatch(r"(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+\.html", route) for route in routes):
        raise ValueError("Routes must be relative HTML paths within the public site")
    index = []
    outputs = {}
    for page in pages:
        prefix = base_path if page["id"] == "404" else "../" * (len(Path(page["route"]).parts) - 1)
        if "doc" in page:
            content = render_dossier(page["doc"], dossier_template, substitute, prefix)
        else:
            source = safe_source(source_dir / "pages", page["source"], ".html")
            content = substitute(source.read_text(encoding="utf-8"), {
                "root": prefix, "cases": render_cases(dossiers, prefix),
                "timeline": render_timeline(dossiers, timeline_template, substitute, prefix),
            })
        navigation = []
        for key in NAV_IDS:
            target = by_id[key]
            current = ' aria-current="page"' if page["id"] == key else ""
            classes = []
            if key == "transparencia":
                classes.append("nav-separated")
            if page.get("nav") == key:
                classes.append("nav-parent")
            class_attr = ' class="' + " ".join(classes) + '"' if classes else ""
            navigation.append(f'<a href="{prefix}{escape(target["route"], quote=True)}"{current}{class_attr}><svg class="icon" viewBox="0 0 24 24" aria-hidden="true">{ICONS[key]}</svg>{escape(target["title"])}</a>')
        breadcrumbs = '<span aria-current="page">Inicio</span>'
        if page["id"] != "inicio":
            breadcrumbs = f'<a href="{prefix}index.html">Alejandría</a><span aria-hidden="true">/</span>'
            if page.get("nav"):
                parent = by_id[page["nav"]]
                breadcrumbs += f'<a href="{prefix}{parent["route"]}">{escape(parent["title"])}</a><span aria-hidden="true">/</span>'
            breadcrumbs += f'<span aria-current="page">{escape(page["title"])}</span>'
        output = substitute(layout, {
            "root": prefix, "page": escape(page["id"], quote=True),
            "title": escape(page["title"]), "description": escape(page["description"], quote=True),
            "navigation": "\n        ".join(navigation), "breadcrumbs": breadcrumbs, "content": content,
        })
        outputs[page["route"]] = output
        for alias in page.get("aliases", []):
            if page["id"] != "404":
                raise ValueError("Only the 404 page supports aliases")
            outputs[alias] = output
        if page["search"]:
            parser = PublicText()
            parser.feed(content)
            index.append({"title": page["title"], "url": page["route"], "kind": "Expediente" if "doc" in page else "Página", "text": " ".join("".join(parser.parts).split())})
    # Add individual authorized chronology entries, with stable deep links.
    if by_id["cronologia"]["search"]:
        for doc in dossiers:
            if not doc["search"]:
                continue
            for event in doc["events"]:
                index.append({"title": event["title"], "url": by_id["cronologia"]["route"] + "#" + event_anchor(doc, event), "kind": "Acontecimiento", "text": " ".join((doc["title"], event.get("date_label") or event["date"] or "Fecha sin determinar", event["summary"]))})
    outputs["assets/search-index.js"] = "/* Generated only from explicit public/search authorization; do not edit. */\nwindow.ALEJANDRIA_SEARCH_INDEX = " + json.dumps(index, ensure_ascii=False, indent=2) + ";\n"
    outputs["robots.txt"] = "# Sitio en preparación. Mantener fuera de los rastreadores.\nUser-agent: *\nDisallow: /\n"
    # Track only generated files, so revoking publication also removes old HTML safely.
    outputs["assets/generated-files.json"] = json.dumps({route: sha256(value.encode("utf-8")).hexdigest() for route, value in outputs.items()}, indent=2) + "\n"
    return outputs, pages, index


def build(source_dir=SOURCE, output_dir=OUTPUT):
    outputs, pages, index = render_site(source_dir)
    if any(not (output_dir / route).resolve().is_relative_to(output_dir.resolve()) for route in outputs):
        raise ValueError("Output paths must remain inside public-html, including symlinks")
    inventory = output_dir / "assets/generated-files.json"
    obsolete = []
    if inventory.is_file():
        previous = json.loads(inventory.read_text(encoding="utf-8"))
        if not isinstance(previous, dict):
            raise ValueError("Invalid generated file inventory")
        for route, digest in previous.items():
            candidate = output_dir / route
            if not candidate.resolve().is_relative_to(output_dir.resolve()) or not re.fullmatch(r"(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+\.html|assets/search-index\.js|robots\.txt", route):
                raise ValueError("Generated inventory contains an unsafe path")
            if route not in outputs and candidate.exists():
                if sha256(candidate.read_text(encoding="utf-8").encode("utf-8")).hexdigest() != digest:
                    raise ValueError(f"Previously generated file was edited; review before removing: {route}")
                obsolete.append(candidate)
    for route, output in outputs.items():
        destination = output_dir / route
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(output, encoding="utf-8", newline="\n")
    for candidate in obsolete:
        candidate.unlink()  # Only unchanged files recorded by a previous build, inside the output directory.
    print(f"Built {len(pages)} public pages and aliases; {len(index)} search entries. Only explicitly approved sources read.")


if __name__ == "__main__":
    build()
