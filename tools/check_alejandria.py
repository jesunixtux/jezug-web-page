"""Check generated public navigation and resources without reading the private archive."""
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
from build_alejandria import render_site, NAV_IDS
from alejandria_content import public_url

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
                self.links.append((tag, attribute, attrs[attribute]))
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
    outputs, pages, expected_index = render_site()
    base_path = json.loads((ROOT / "site-public/settings.json").read_text(encoding="utf-8"))["base_path"]
    parsed = {}
    errors = []
    for route, expected_text in outputs.items():
        path = PUBLIC / route
        if not path.is_file() or path.read_text(encoding="utf-8") != expected_text:
            errors.append(route + ": generated output differs from approved sources; run the generator")
    by_route = {route: entry for entry in pages for route in [entry["route"], *entry.get("aliases", [])]}

    def local_target(path, url):
        parts = urlsplit(url)
        local = unquote(parts.path)
        if local.startswith("/"):
            if not local.startswith(base_path):
                raise ValueError("Root URL lies outside configured base_path")
            return (PUBLIC / local[len(base_path):]).resolve()
        return (path.parent / local).resolve() if local else path

    for route, entry in by_route.items():
        path = (PUBLIC / route).resolve()
        if not path.is_file():
            continue
        parser = Page()
        html = path.read_text(encoding="utf-8")
        parser.feed(html)
        parsed[path] = parser
        prefix = route + ": "
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
        expected_routes = {other["route"] for other in pages if other["id"] in NAV_IDS}
        actual_routes = {local_target(path, link["href"]).relative_to(PUBLIC).as_posix() for link in parser.nav_links}
        if actual_routes != expected_routes:
            errors.append(prefix + "Inconsistent global navigation")
        active = [link for link in parser.nav_links if link.get("aria-current") == "page"]
        if entry.get("nav"):
            if active or not any("nav-parent" in link.get("class", "") for link in parser.nav_links):
                errors.append(prefix + "Incorrect parent navigation state")
        elif entry["id"] not in NAV_IDS:
            if active:
                errors.append(prefix + "This page must not mark an unrelated navigation item as current")
        elif len(active) != 1 or local_target(path, active[0]["href"]) != path:
            errors.append(prefix + "Incorrect active navigation state")
        if "{{" in html:
            errors.append(prefix + "Unresolved template")

    count = 0
    external_count = 0
    allowed_files = {(PUBLIC / route).resolve() for route in outputs} | {(PUBLIC / "assets" / name).resolve() for name in ("site.css", "site.js", "theme.js", "timeline.js")}
    approved_urls = {ref["url"] for entry in pages if "doc" in entry for ref in entry["doc"]["references"]}
    for path, parser in parsed.items():
        for tag, attribute, link in parser.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                try:
                    public_url(link)
                    if tag != "a" or attribute != "href" or link not in approved_urls:
                        raise ValueError("External links must be explicitly approved public references; remote resources are forbidden")
                except ValueError as error:
                    errors.append(str(path.relative_to(PUBLIC)) + ": " + str(error))
                external_count += 1
                continue
            try:
                destination = local_target(path, link)
            except ValueError as error:
                errors.append(str(error))
                continue
            if not destination.is_relative_to(PUBLIC):
                errors.append("Link escapes public folder: " + link)
                continue
            if not destination.is_file():
                errors.append("Missing target: " + link)
                continue
            if destination not in allowed_files:
                errors.append("Local file is outside the explicitly authorized site output: " + link)
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
    if index != expected_index:
        errors.append("Search index differs from explicit publication/search authorization")
    for entry in index:
        destination = local_target(PUBLIC / "index.html", entry["url"])
        fragment = unquote(urlsplit(entry["url"]).fragment)
        if destination not in parsed or (fragment and fragment not in parsed[destination].ids):
            errors.append("Invalid search result target: " + entry["url"])
    if any(not entry["text"].strip() for entry in index):
        errors.append("Empty searchable page")
    if (PUBLIC / "robot.txt").exists():
        errors.append("Obsolete robot.txt must be removed")
    if "User-agent: *\nDisallow: /" not in (PUBLIC / "robots.txt").read_text(encoding="utf-8"):
        errors.append("Preparation robots policy must disallow crawling")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: {len(parsed)} HTML outputs, {count} local links/resources, {len(index)} search entries; templates, authorization, fragments, labels, navigation and robots match.")
    if external_count:
        print(f"{external_count} approved HTTPS references checked for format only; no remote sources fetched.")


if __name__ == "__main__":
    check()
