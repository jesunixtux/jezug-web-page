"""Build only the explicitly listed public pages. Never scan the documentary archive."""
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path

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
        skip = tag in {"script", "style", "svg", "nav", "noscript"} or attributes.get("aria-hidden") == "true"
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


def build():
    pages = json.loads((SOURCE / "pages.json").read_text(encoding="utf-8"))
    layout = (SOURCE / "layout.html").read_text(encoding="utf-8")
    by_id = {page["id"]: page for page in pages}
    if len(by_id) != len(pages) or len({page["route"] for page in pages}) != len(pages):
        raise ValueError("Page IDs and routes must be unique")
    index = []
    for page in pages:
        destination = (OUTPUT / page["route"]).resolve()
        source = (SOURCE / "pages" / page["source"]).resolve()
        if not destination.is_relative_to(OUTPUT.resolve()) or not source.is_relative_to((SOURCE / "pages").resolve()):
            raise ValueError("Page paths must remain inside the public site")
        prefix = "../" * (len(Path(page["route"]).parts) - 1)
        content = substitute(source.read_text(encoding="utf-8"), {"root": prefix})
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
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(output, encoding="utf-8", newline="\n")
        if page["id"] != "buscar":
            parser = PublicText()
            parser.feed(content)
            index.append({"title": page["title"], "url": page["route"], "text": " ".join("".join(parser.parts).split())})
    search_file = OUTPUT / "assets" / "search-index.js"
    search_file.parent.mkdir(parents=True, exist_ok=True)
    search_file.write_text("/* Generated from the explicit public page list; do not edit. */\nwindow.ALEJANDRIA_SEARCH_INDEX = " + json.dumps(index, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8", newline="\n")
    print(f"Built {len(pages)} public pages; indexed {len(index)} pages. No archive directories accessed.")


if __name__ == "__main__":
    build()
