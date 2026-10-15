"""Structured public dossiers. Read only explicit, approved files under site-public."""
from datetime import date
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

CATEGORIES = {
    "hecho-observable": "Hecho observable", "admision": "Admisión",
    "alegacion-externa": "Alegación externa", "inferencia": "Inferencia",
    "no-determinado": "No determinado",
}
EVENT_TYPES = {
    "acontecimiento": "Acontecimiento", "documento": "Registro documental",
    "publicacion": "Publicación", "revision": "Revisión",
}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def text(value, label, allow_empty=False):
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ValueError(f"{label}: expected {'possibly empty ' if allow_empty else ''}text")
    return value


def slug(value, label):
    if not isinstance(value, str) or not SLUG.fullmatch(value):
        raise ValueError(f"{label}: use a lowercase slug")
    return value


def fields(record, required, optional=()):
    if not isinstance(record, dict) or not set(required).issubset(record) or set(record) - set(required) - set(optional):
        raise ValueError(f"Expected fields {required}, optional {optional}")


def date_label(value):
    if value is None:
        return "Fecha sin determinar"
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}(?:-[0-9]{2}(?:-[0-9]{2})?)?", value):
        raise ValueError("Date must be YYYY, YYYY-MM, YYYY-MM-DD or null")
    date.fromisoformat(value + ("-01-01" if len(value) == 4 else "-01" if len(value) == 7 else ""))
    return value


def safe_source(folder, name, suffix):
    text(name, "source")
    path = (folder / name).resolve()
    if not path.is_relative_to(folder.resolve()) or path.suffix != suffix:
        raise ValueError("Source must stay within its authorized public folder")
    return path


def public_url(value):
    text(value, "reference URL")
    parts = urlsplit(value)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password or any(c.isspace() for c in value):
        raise ValueError("Public references require an explicit HTTPS URL without credentials")
    return value


def validate_references(ids, approved):
    if not isinstance(ids, list) or any(not isinstance(key, str) or key not in approved for key in ids):
        raise ValueError("Reference IDs must identify explicitly public references in this dossier")


def load_dossiers(source):
    catalog = json.loads((source / "expedientes.json").read_text(encoding="utf-8"))
    if not isinstance(catalog, list):
        raise ValueError("expedientes.json must be a list")
    dossiers = []
    for item in catalog:
        fields(item, ("source", "public", "search"))
        if type(item["public"]) is not bool or type(item["search"]) is not bool:
            raise ValueError("Publication and search authorization must be explicit booleans")
        if not item["public"]:
            continue  # Do not even open unapproved sources.
        path = safe_source(source / "expedientes", item["source"], ".json")
        doc = json.loads(path.read_text(encoding="utf-8"))
        fields(doc, ("id", "title", "description", "example", "period", "introduction", "context", "scope", "events", "claims", "references", "contradictions", "undetermined", "conclusions", "updates"))
        slug(doc["id"], "dossier id")
        for key in ("title", "description", "period"):
            text(doc[key], key)
        for key in ("introduction", "context", "scope"):
            text(doc[key], key, allow_empty=True)
        if type(doc["example"]) is not bool:
            raise ValueError("example must be a boolean")
        for key in ("events", "claims", "references", "contradictions", "undetermined", "conclusions", "updates"):
            if not isinstance(doc[key], list):
                raise ValueError(f"{key} must be a list")
        approved = {}
        for ref in doc["references"]:
            fields(ref, ("id", "public", "title", "url", "context"))
            if type(ref["public"]) is not bool:
                raise ValueError("Reference publication must be explicitly authorized")
            if not ref["public"]:
                continue
            slug(ref["id"], "reference id")
            if ref["id"] in approved:
                raise ValueError("Duplicate reference ID")
            text(ref["title"], "reference title")
            text(ref["context"], "reference context", allow_empty=True)
            public_url(ref["url"])
            approved[ref["id"]] = ref
        events = []
        for event in doc["events"]:
            fields(event, ("id", "public", "date", "title", "summary", "type", "references"), ("date_label",))
            if type(event["public"]) is not bool:
                raise ValueError("Event publication must be explicitly authorized")
            if not event["public"]:
                continue
            slug(event["id"], "event id")
            date_label(event["date"])
            for key in ("title", "summary"):
                text(event[key], key)
            if "date_label" in event:
                text(event["date_label"], "date label")
            if event["type"] not in EVENT_TYPES:
                raise ValueError("Unknown event type")
            validate_references(event["references"], approved)
            events.append(event)
        if len({event["id"] for event in events}) != len(events):
            raise ValueError("Duplicate event ID")
        for claim in doc["claims"]:
            fields(claim, ("id", "category", "text", "limits", "references"))
            slug(claim["id"], "claim id")
            if claim["category"] not in CATEGORIES:
                raise ValueError("Unknown documentary category")
            text(claim["text"], "claim text")
            text(claim["limits"], "claim limits")
            validate_references(claim["references"], approved)
        if len({claim["id"] for claim in doc["claims"]}) != len(doc["claims"]):
            raise ValueError("Duplicate claim ID")
        for key in ("contradictions", "undetermined", "conclusions"):
            for value in doc[key]:
                text(value, key)
        for update in doc["updates"]:
            fields(update, ("date", "change", "reason", "references"))
            date_label(update["date"])
            text(update["change"], "update change")
            text(update["reason"], "update reason")
            validate_references(update["references"], approved)
        doc = {**doc, "references": list(approved.values()), "events": sorted(events, key=lambda e: (e["date"] or "9999", e["id"])), "search": item["search"], "route": f'casos/{doc["id"]}/index.html'}
        dossiers.append(doc)
    if len({doc["id"] for doc in dossiers}) != len(dossiers):
        raise ValueError("Duplicate dossier ID")
    return dossiers


def paragraphs(value, empty):
    return "".join(f"<p>{escape(part)}</p>" for part in value.splitlines() if part.strip()) if value.strip() else f'<p class="pending-text">{escape(empty)}</p>'


def items(values, empty):
    return '<ul class="document-list">' + "".join(f"<li>{escape(value)}</li>" for value in values) + "</ul>" if values else f'<p class="pending-text">{escape(empty)}</p>'


def reference_links(ids, doc, prefix):
    refs = {ref["id"]: ref for ref in doc["references"]}
    return '<div class="reference-links">' + " ".join(f'<a href="{prefix}{doc["route"]}#ref-{key}">{escape(refs[key]["title"])}</a>' for key in ids) + "</div>" if ids else '<p class="pending-text">Sin referencias públicas asociadas.</p>'


def event_anchor(doc, event):
    return f'evento-{doc["id"]}-{event["id"]}'


def render_event(doc, event, prefix):
    label = event.get("date_label", date_label(event["date"]))
    stamp = f'<time datetime="{event["date"]}">{escape(label)}</time>' if event["date"] else escape(label)
    kind = EVENT_TYPES[event["type"]]
    example = '<span class="status-pill">Ejemplo ficticio</span>' if doc["example"] else ""
    return f'''<li class="timeline-entry" id="{event_anchor(doc, event)}" data-year="{event['date'][:4] if event['date'] else 'sin-fecha'}" data-case="{doc['id']}" data-case-label="{escape(doc['title'], quote=True)}" data-type="{event['type']}" data-type-label="{escape(kind, quote=True)}"><div class="timeline-date">{stamp}</div><article class="timeline-card">{example}<span class="card-index">{escape(kind)}</span><h3>{escape(event['title'])}</h3><p>{escape(event['summary'])}</p><a class="text-link" href="{prefix}{doc['route']}#cronologia">{escape(doc['title'])} →</a>{reference_links(event['references'], doc, prefix)}</article></li>'''


def render_dossier(doc, template, substitute, prefix):
    claims = []
    for claim in doc["claims"]:
        claims.append(f'<article class="claim" id="afirmacion-{claim["id"]}"><span class="status-pill">{CATEGORIES[claim["category"]]}</span><h3>{escape(claim["text"])}</h3><p><strong>Límites:</strong> {escape(claim["limits"])}</p>{reference_links(claim["references"], doc, prefix)}</article>')
    references = [f'<li id="ref-{ref["id"]}"><a href="{escape(ref["url"], quote=True)}" rel="noreferrer">{escape(ref["title"])}</a>{paragraphs(ref["context"], "Contexto pendiente de documentar.")}</li>' for ref in doc["references"]]
    updates = [f'<li><span class="card-index">{escape(date_label(update["date"]))}</span><h3>{escape(update["change"])}</h3><p>{escape(update["reason"])}</p>{reference_links(update["references"], doc, prefix)}</li>' for update in doc["updates"]]
    return substitute(template, {
        "title": escape(doc["title"]), "description": escape(doc["description"]), "root": prefix,
        "status": "Ejemplo sin contenido documental" if doc["example"] else "Expediente en revisión",
        "example_notice": '<aside class="notice section"><span class="notice-mark" aria-hidden="true">i</span><div><strong>Ejemplo de organización, sin contenido documental real.</strong><p>Los apartados vacíos indican qué información pública deberá revisarse antes de redactar un expediente.</p></div></aside>' if doc["example"] else "",
        "period": escape(doc["period"]),
        "introduction": paragraphs(doc["introduction"], "Pendiente de definir la pregunta del expediente."),
        "context": paragraphs(doc["context"], "Pendiente de contextualización pública."),
        "scope": paragraphs(doc["scope"], "Pendiente de delimitar qué se examina y qué queda fuera."),
        "events": '<ol class="timeline-list">' + "".join(render_event(doc, event, prefix) for event in doc["events"]) + "</ol>" if doc["events"] else '<p class="pending-text">Sin acontecimientos públicos registrados.</p>',
        "claims": "".join(claims) or '<p class="pending-text">Sin afirmaciones examinadas.</p>',
        "references": '<ol class="document-list">' + "".join(references) + "</ol>" if references else '<p class="pending-text">Sin evidencias ni referencias públicas asociadas.</p>',
        "contradictions": items(doc["contradictions"], "Sin contradicciones examinadas en esta estructura."),
        "undetermined": items(doc["undetermined"], "Pendiente de registrar vacíos, límites y puntos no determinados."),
        "conclusions": items(doc["conclusions"], "No se presentan conclusiones provisionales."),
        "updates": '<ol class="document-list">' + "".join(updates) + "</ol>" if updates else '<p class="pending-text">Sin correcciones documentales registradas.</p>',
    })


def render_cases(dossiers, prefix):
    cards = []
    for doc in dossiers:
        status = "Ejemplo de estructura" if doc["example"] else "Expediente en revisión"
        cards.append(f'<a class="card linked-card" href="{prefix}{doc["route"]}"><span class="status-pill">{status}</span><h3>{escape(doc["title"])} <span aria-hidden="true">↗</span></h3><p>{escape(doc["description"])}</p><span class="card-foot">Abrir expediente →</span></a>')
    empty = '<p class="reading-note section">No hay casos documentales reales publicados en esta versión. La estructura de ejemplo no presenta hechos sobre personas.</p>' if not any(not doc["example"] for doc in dossiers) else ""
    return empty + '<div class="cards section">' + "".join(cards) + "</div>"


def render_timeline(dossiers, template, substitute, prefix):
    rows = [(doc, event) for doc in dossiers for event in doc["events"]]
    rows.sort(key=lambda row: (row[1]["date"] or "9999", row[0]["id"], row[1]["id"]))
    return substitute(template, {
        "entries": "".join(render_event(doc, event, prefix) for doc, event in rows),
        "status": f"{len(rows)} acontecimientos públicos disponibles." if rows else "No hay acontecimientos públicos registrados. Los filtros se activarán cuando existan entradas.",
        "empty_hidden": "hidden" if rows else "",
        "empty_label": "Sin coincidencias" if rows else "Cronología en preparación",
        "empty_title": "No hay entradas con estos filtros." if rows else "La cronología está lista para incorporar entradas revisadas.",
        "empty_text": "Prueba otra combinación o limpia los filtros." if rows else "Esta versión no publica acontecimientos fechados. Las futuras entradas enlazarán a su expediente y a sus referencias públicas.",
    })
