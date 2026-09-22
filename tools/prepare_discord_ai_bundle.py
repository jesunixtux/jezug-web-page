#!/usr/bin/env python3
"""Build AI-friendly derivatives for the private Discord archive.

The numeric PNG files in the source directory are treated as immutable originals.
This script creates:
  - compressed WebP copies for lightweight review;
  - vertical review pages containing up to three consecutive screenshots;
  - a JSON manifest with hashes, dimensions and mapping back to originals;
  - a README explaining how another AI should consume the bundle.

No OCR or semantic interpretation is performed here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps

NUMERIC_PNG = re.compile(r"^(\d+)\.png$", re.IGNORECASE)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def numeric_sources(source_dir: Path) -> list[Path]:
    files: list[tuple[int, Path]] = []
    for path in source_dir.iterdir():
        if not path.is_file():
            continue
        m = NUMERIC_PNG.match(path.name)
        if m:
            files.append((int(m.group(1)), path))
    return [p for _, p in sorted(files, key=lambda x: x[0])]


def flatten_rgb(img: Image.Image) -> Image.Image:
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        rgba = img.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, "white")
        bg.alpha_composite(rgba)
        return bg.convert("RGB")
    return img.convert("RGB")


def fit_width(img: Image.Image, max_width: int) -> Image.Image:
    if img.width <= max_width:
        return img.copy()
    height = round(img.height * (max_width / img.width))
    return img.resize((max_width, height), Image.Resampling.LANCZOS)


def save_webp(src: Path, dst: Path, max_width: int, quality: int) -> tuple[int, int]:
    with Image.open(src) as im:
        rgb = flatten_rgb(im)
        out = fit_width(rgb, max_width)
        dst.parent.mkdir(parents=True, exist_ok=True)
        out.save(dst, "WEBP", quality=quality, method=6, optimize=True)
        return out.size


def chunks(seq: list[Path], size: int) -> Iterable[list[Path]]:
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def make_review_page(
    files: list[Path],
    dst: Path,
    max_width: int,
    quality: int,
) -> dict:
    font = ImageFont.load_default()
    margin = 24
    label_h = 34
    gap = 20

    rendered: list[tuple[Path, Image.Image]] = []
    for path in files:
        with Image.open(path) as im:
            img = fit_width(flatten_rgb(im), max_width)
            rendered.append((path, img))

    canvas_w = max(img.width for _, img in rendered) + margin * 2
    canvas_h = margin
    for _, img in rendered:
        canvas_h += label_h + img.height + gap
    canvas_h += margin - gap

    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(canvas)
    y = margin

    for path, img in rendered:
        label = f"ORIGINAL: {path.name}"
        draw.text((margin, y + 8), label, fill="black", font=font)
        y += label_h
        x = margin + (canvas_w - margin * 2 - img.width) // 2
        canvas.paste(img, (x, y))
        y += img.height + gap

    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst, "WEBP", quality=quality, method=6, optimize=True)

    return {
        "path": dst.as_posix(),
        "sources": [p.name for p in files],
        "width": canvas.width,
        "height": canvas.height,
        "bytes": dst.stat().st_size,
        "sha256": sha256(dst),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="md-s/el pepe")
    ap.add_argument("--output", default="md-s/el pepe/ai")
    ap.add_argument("--individual-width", type=int, default=1440)
    ap.add_argument("--page-width", type=int, default=1600)
    ap.add_argument("--page-size", type=int, default=3)
    ap.add_argument("--quality", type=int, default=82)
    args = ap.parse_args()

    source_dir = Path(args.source)
    output_dir = Path(args.output)
    optimized_dir = output_dir / "optimized"
    pages_dir = output_dir / "pages"

    sources = numeric_sources(source_dir)
    if not sources:
        raise SystemExit(f"No numeric PNG originals found in {source_dir}")

    # Generated derivatives are disposable; originals are never touched.
    if output_dir.exists():
        shutil.rmtree(output_dir)
    optimized_dir.mkdir(parents=True, exist_ok=True)
    pages_dir.mkdir(parents=True, exist_ok=True)

    manifest_files = []
    original_total = 0
    optimized_total = 0

    for src in sources:
        idx = int(src.stem)
        dst = optimized_dir / f"{idx:04d}.webp"
        out_w, out_h = save_webp(src, dst, args.individual_width, args.quality)
        original_total += src.stat().st_size
        optimized_total += dst.stat().st_size
        with Image.open(src) as im:
            src_w, src_h = im.size
        manifest_files.append(
            {
                "index": idx,
                "original": src.as_posix(),
                "original_bytes": src.stat().st_size,
                "original_sha256": sha256(src),
                "original_width": src_w,
                "original_height": src_h,
                "optimized": dst.as_posix(),
                "optimized_bytes": dst.stat().st_size,
                "optimized_sha256": sha256(dst),
                "optimized_width": out_w,
                "optimized_height": out_h,
            }
        )

    review_pages = []
    for page_no, group in enumerate(chunks(sources, args.page_size), start=1):
        first = int(group[0].stem)
        last = int(group[-1].stem)
        dst = pages_dir / f"part-01-page-{page_no:03d}__{first:03d}-{last:03d}.webp"
        entry = make_review_page(group, dst, args.page_width, args.quality)
        entry["page"] = page_no
        review_pages.append(entry)

    pages_total = sum(p["bytes"] for p in review_pages)

    manifest = {
        "schema_version": "1.0",
        "collection": "discord-el-pepe",
        "bundle": "part-01",
        "status": "derived_for_ai_review",
        "source_policy": "Numeric PNG files in md-s/el pepe/ are immutable originals. Everything under ai/ is derived and may be regenerated.",
        "semantic_policy": "This bundle performs no OCR and makes no factual conclusions. It only reduces image weight and groups consecutive screenshots.",
        "context_from_archivist": {
            "description": "Grupo de MD en el que varios participantes, incluido Jezu, se burlaban o insultaban a Danel / Montaña VHS.",
            "warning": "Este contexto es aportado por el archivista y no sustituye la verificación mensaje por mensaje."
        },
        "selection_policy": {
            "spam": "El archivista indicó que spam y contenido repetitivo no relevante puede quedar fuera de la selección documental.",
            "caution": "Una omisión por spam no debe ocultar mensajes que cambien el sentido, autoría, secuencia o contexto de una interacción."
        },
        "source_count": len(sources),
        "source_indices": [int(p.stem) for p in sources],
        "files": manifest_files,
        "review_pages": review_pages,
        "totals": {
            "original_bytes": original_total,
            "optimized_individual_bytes": optimized_total,
            "review_pages_bytes": pages_total,
            "optimized_individual_ratio": round(optimized_total / original_total, 4) if original_total else None,
        },
    }

    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readme = f"""# Bundle IA — el pepe / parte 01

Este directorio es **derivado**. Los PNG numéricos de `md-s/el pepe/` siguen siendo los originales y no se modifican.

## Objetivo

Reducir el costo visual/contextual cuando otra IA necesite revisar esta parte del grupo de Discord.

- Originales actuales: **{len(sources)}** archivos.
- Índices incluidos: **{int(sources[0].stem)}–{int(sources[-1].stem)}**.
- `optimized/`: una copia WebP ligera por captura.
- `pages/`: páginas de revisión con hasta **{args.page_size} capturas consecutivas**.
- `manifest.json`: relación exacta entre derivado y original, dimensiones y SHA-256.

## Cómo pasárselo a otra IA

1. Entregar primero este README y `manifest.json`.
2. Para una primera lectura, usar solo `pages/` en orden.
3. Si una frase, nombre, fecha o autoría resulta importante, abrir el archivo correspondiente en `optimized/`.
4. Para una cita o verificación definitiva, volver siempre al PNG original.
5. No inferir que un mensaje pertenece a una persona solo porque aparece cerca de otro.
6. Distinguir mensaje visible, reacción, meme compartido, interpretación y contexto aportado por el archivista.
7. No convertir la ausencia de spam en prueba de que no existían otros mensajes.

## Contexto aportado por el archivista

El archivista describe este grupo como un MD grupal donde varios participantes, incluido Jezu, se burlaban o insultaban a Danel / Montaña VHS.

Ese dato debe tratarse como **contexto aportado**, no como sustituto de leer las capturas. La atribución de cada mensaje debe hacerse imagen por imagen.

## Spam y omisiones

Se permite dejar fuera spam, stickers repetidos o contenido sin relación **solo cuando no cambie el sentido del intercambio**. Si existe un salto entre capturas, una IA debe tratarlo como un hueco y no inventar qué ocurrió ahí.

## Integridad

Los derivados pueden comprimirse o regenerarse. Los hashes de los originales están en `manifest.json`; cualquier conclusión documental importante debe poder trazarse de vuelta al PNG fuente.
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
