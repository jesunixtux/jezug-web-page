"""Check generated public navigation and resources without reading the private archive."""
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = (ROOT / "public-html").resolve()
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.labels = []
        self.required_ids = []
        self.h1_count = 0
        self.main_count = 0
        self.nav_links = []
        self.stack = []
        self.errors = []
        self.in_nav = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for attribute in ("href", "src", "action"):
            if attribute in attrs:
                self.links.append(attrs[attribute])
        for attribute in ("aria-controls", "aria-labelledby", "aria-describedby"):
            self.required_ids.extend(attrs.get(attribute, "").split())
        if tag == "label" and "for" in attrs:
            self.labels.append(attrs["for"])
        self.h1_count += tag == "h1"
        self.main_count += tag == "main"
        if tag == "nav" and attrs.get("id") == "site-nav":
            self.in_nav = True
        if tag == "a" and self.in_nav:
            self.nav_links.append(attrs)
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_nav = False
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"Unbalanced closing tag: {tag}")
        else:
            self.stack.pop()


def check():
    pages = json.loads((ROOT / "site-public/pages.json").read_text(encoding="utf-8"))
    parsed = {}
    errors = []
    for entry in pages:
        path = (PUBLIC / entry["route"]).resolve()
        parser = Page()
        html = path.read_text(encoding="utf-8")
        parser.feed(html)
        parsed[path] = parser
        prefix = entry["route"] + ": "
        errors.extend(prefix + error for error in parser.errors)
        if parser.stack:
            errors.append(prefix + "Unclosed tags: " + repr(parser.stack))
        if parser.h1_count != 1 or parser.main_count != 1:
            errors.append(prefix + "Expected one h1 and one main")
        duplicates = [key for key, count in Counter(parser.ids).items() if count > 1]
        if duplicates:
            errors.append(prefix + "Duplicate IDs: " + repr(duplicates))
        for element_id in parser.required_ids + parser.labels:
            if element_id not in parser.ids:
                errors.append(prefix + "Unresolved accessible label/control: " + element_id)
        expected_routes = {other["route"] for other in pages if not other.get("nav")}
        actual_routes = {(path.parent / link["href"]).resolve().relative_to(PUBLIC).as_posix() for link in parser.nav_links}
        if actual_routes != expected_routes:
            errors.append(prefix + "Inconsistent global navigation")
        active = [link for link in parser.nav_links if link.get("aria-current") == "page"]
        if entry.get("nav"):
            if active or not any("nav-parent" in link.get("class", "") for link in parser.nav_links):
                errors.append(prefix + "Incorrect parent navigation state")
        elif len(active) != 1 or (path.parent / active[0]["href"]).resolve() != path:
            errors.append(prefix + "Incorrect active navigation state")
        if "{{" in html:
            errors.append(prefix + "Unresolved template")

    count = 0
    for path, parser in parsed.items():
        for link in parser.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                errors.append(str(path.relative_to(PUBLIC)) + ": External resource/link needs review: " + link)
                continue
            destination = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not destination.is_relative_to(PUBLIC):
                errors.append("Link escapes public folder: " + link)
                continue
            if not destination.is_file():
                errors.append("Missing target: " + link)
                continue
            # Never open arbitrary linked files: inspect anchors only in the explicit page list.
            if parts.fragment and (destination not in parsed or unquote(parts.fragment) not in parsed[destination].ids):
                errors.append("Missing or unreviewed fragment: " + link)
            if destination.suffix == ".html" and destination not in parsed:
                errors.append("HTML outside the explicit public page list: " + link)
            count += 1

    index_path = PUBLIC / "assets/search-index.js"
    raw = index_path.read_text(encoding="utf-8")
    index = json.loads(raw.split("window.ALEJANDRIA_SEARCH_INDEX = ", 1)[1].removesuffix(";\n"))
    expected = {entry["route"] for entry in pages if entry["id"] != "buscar"}
    if {entry["url"] for entry in index} != expected or len(index) != len(expected):
        errors.append("Search index must cover exactly the explicit public content pages")
    if any(not entry["text"].strip() for entry in index):
        errors.append("Empty searchable page")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: {len(pages)} pages, {count} local links/resources, {len(index)} indexed pages; valid fragments, labels and navigation.")


if __name__ == "__main__":
    check()
