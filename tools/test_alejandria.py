"""Synthetic, isolated publishing tests. Never load or publish documentary archives."""
import copy
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from build_alejandria import SOURCE, render_site, build


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="alejandria-test-")
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name) / "site-public"
        # Only the web's authored source tree is copied into this isolated fixture.
        shutil.copytree(SOURCE, self.source)
        self.doc = json.loads((self.source / "expedientes/expediente-ejemplo.json").read_text(encoding="utf-8"))
        self.doc.update({"id": "prueba-ficticia", "title": "Expediente sintético de prueba (ficticio)", "introduction": "INTRO_TEST_ONLY", "events": [
            {"id": "entrada-uno", "public": True, "date": "2000-01-01", "title": "Entrada sintética ficticia A", "summary": "EVENT_TEST_ONLY", "type": "documento", "references": ["fuente-prueba"]},
            {"id": "entrada-dos", "public": True, "date": "2001", "title": "Entrada sintética ficticia B", "summary": "Otra entrada de prueba, sin valor histórico.", "type": "revision", "references": []},
        ], "references": [{"id": "fuente-prueba", "public": True, "title": "Referencia ficticia de prueba", "url": "https://example.org/prueba-ficticia", "context": "Referencia sintética, no se descarga."}]})

    def save(self, doc=None, search=True):
        (self.source / "expedientes/prueba.json").write_text(json.dumps(doc or self.doc), encoding="utf-8")
        (self.source / "expedientes.json").write_text(json.dumps([{"source": "prueba.json", "public": True, "search": search}]), encoding="utf-8")

    def build_fixture(self, output):
        with redirect_stdout(StringIO()):
            build(self.source, output)

    def test_future_dossier_updates_cases_timeline_search_and_deep_links(self):
        self.save()
        outputs, pages, index = render_site(self.source)
        self.assertIn("casos/prueba-ficticia/index.html", outputs)
        self.assertIn("prueba-ficticia/index.html", outputs["casos/index.html"])
        self.assertIn('data-year="2000"', outputs["cronologia/index.html"])
        self.assertIn('data-type="revision"', outputs["cronologia/index.html"])
        self.assertIn("#ref-fuente-prueba", outputs["cronologia/index.html"])
        events = [entry for entry in index if entry["kind"] == "Acontecimiento"]
        self.assertEqual(len(events), 2)
        for entry in events:
            fragment = entry["url"].split("#")[1]
            self.assertIn('id="' + fragment + '"', outputs["cronologia/index.html"])

    def test_unapproved_source_is_not_even_opened(self):
        catalog = [{"source": "../../evidence/NOT_A_REAL_SOURCE.json", "public": False, "search": False}]
        (self.source / "expedientes.json").write_text(json.dumps(catalog), encoding="utf-8")
        outputs, pages, index = render_site(self.source)
        self.assertFalse(any("doc" in page for page in pages))
        self.assertFalse(any(entry["kind"] == "Expediente" for entry in index))

    def test_search_authorization_excludes_body_and_events_from_all_index_entries(self):
        self.save(search=False)
        outputs, pages, index = render_site(self.source)
        self.assertIn("INTRO_TEST_ONLY", outputs["casos/prueba-ficticia/index.html"])
        self.assertIn("EVENT_TEST_ONLY", outputs["cronologia/index.html"])
        combined = json.dumps(index)
        self.assertNotIn("INTRO_TEST_ONLY", combined)
        self.assertNotIn("EVENT_TEST_ONLY", combined)
        self.assertFalse(any(entry["kind"] in {"Expediente", "Acontecimiento"} for entry in index))

    def test_unapproved_events_and_references_never_enter_output_or_index(self):
        self.doc["events"].append({**self.doc["events"][0], "id": "oculto", "public": False, "summary": "UNAPPROVED_EVENT_TEST"})
        self.doc["references"].append({**self.doc["references"][0], "id": "oculta", "public": False, "context": "UNAPPROVED_REF_TEST"})
        self.save()
        outputs, _, index = render_site(self.source)
        combined = " ".join(outputs.values()) + json.dumps(index)
        self.assertNotIn("UNAPPROVED_EVENT_TEST", combined)
        self.assertNotIn("UNAPPROVED_REF_TEST", combined)

    def test_rejects_private_reference_ids_invalid_categories_dates_and_urls(self):
        variants = []
        doc = copy.deepcopy(self.doc)
        doc["references"][0]["public"] = False
        variants.append(doc)
        doc = copy.deepcopy(self.doc)
        doc["events"][0]["date"] = "2000-02-31"
        variants.append(doc)
        doc = copy.deepcopy(self.doc)
        doc["references"][0]["url"] = "file:///private.txt"
        variants.append(doc)
        doc = copy.deepcopy(self.doc)
        doc["claims"] = [{"id": "prueba", "category": "inventada", "text": "Prueba sintética", "limits": "Sin contenido real", "references": []}]
        variants.append(doc)
        for doc in variants:
            with self.subTest(doc=doc), self.assertRaises(ValueError):
                self.save(doc)
                render_site(self.source)

    def test_source_traversal_and_implicit_authorization_are_rejected(self):
        for item in [
            {"source": "../../private-references/not-real.json", "public": True, "search": True},
            {"source": "prueba.json", "public": "yes", "search": True},
        ]:
            with self.subTest(item=item), self.assertRaises(ValueError):
                (self.source / "expedientes.json").write_text(json.dumps([item]), encoding="utf-8")
                render_site(self.source)

    def test_plain_text_is_escaped_and_categories_are_preserved(self):
        self.doc["title"] = '<script>alert("fixture")</script>'
        self.doc["claims"] = [{"id": "prueba", "category": "admision", "text": "Afirmación ficticia de prueba", "limits": "Sin valor histórico", "references": []}]
        self.save()
        outputs, _, _ = render_site(self.source)
        dossier = outputs["casos/prueba-ficticia/index.html"]
        self.assertNotIn('<script>alert("fixture")</script>', dossier)
        self.assertIn("&lt;script&gt;", dossier)
        self.assertIn("Admisión", dossier)

    def test_404_alias_is_deterministic_and_safe_at_arbitrary_depth(self):
        (self.source / "settings.json").write_text('{"base_path":"/alejandria/"}', encoding="utf-8")
        first, _, _ = render_site(self.source)
        second, _, _ = render_site(self.source)
        self.assertEqual(first, second)
        self.assertEqual(first["404.html"], first["404/404.html"])
        self.assertIn('src="/alejandria/assets/site.js"', first["404.html"])
        self.assertIn('href="/alejandria/index.html"', first["404.html"])

    def test_revoking_publication_removes_only_unchanged_generated_page(self):
        self.save()
        output = Path(self.temporary.name) / "public-html"
        self.build_fixture(output)
        manual = output / "unmanaged.html"
        manual.write_text("Manually authored fixture", encoding="utf-8")
        self.assertTrue((output / "casos/prueba-ficticia/index.html").exists())
        (self.source / "expedientes.json").write_text("[]", encoding="utf-8")
        self.build_fixture(output)
        self.assertFalse((output / "casos/prueba-ficticia/index.html").exists())
        self.assertTrue(manual.exists())

    def test_edited_generated_page_is_not_silently_removed_on_revocation(self):
        self.save()
        output = Path(self.temporary.name) / "public-html"
        self.build_fixture(output)
        page = output / "casos/prueba-ficticia/index.html"
        page.write_text("Manually edited fixture", encoding="utf-8")
        (self.source / "expedientes.json").write_text("[]", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.build_fixture(output)
        self.assertEqual(page.read_text(encoding="utf-8"), "Manually edited fixture")


if __name__ == "__main__":
    unittest.main(verbosity=2)
