# jezug-web-page

Repositorio público en construcción: archivo documental y sitio estático Alejandría. Que un archivo esté en este repositorio no autoriza su incorporación al sitio web.

## Alejandría — desarrollo web

La web estática se mantiene en `public-html/` y se genera desde `site-public/`. Tiene navegación compartida, tema oscuro predeterminado y modo claro persistente, búsqueda local, una cronología con filtros preparada para recibir entradas y un sistema de expedientes estructurados. Solo incluye contenido público de ejemplo y estados vacíos; todavía no presenta expedientes históricos reales.

```powershell
python -B tools/build_alejandria.py
python -B tools/check_alejandria.py
python -B tools/test_alejandria.py
python -B tools/serve_alejandria.py
```

Consulta [la guía web](site-public/README.md) para redactar expedientes, autorizar su publicación y búsqueda, y revisar las pruebas. El servidor de vista previa escucha únicamente en `127.0.0.1:8765` y sirve solo `public-html/`, incluyendo una respuesta 404 propia. No hay despliegue automático ni dominio configurado. El estado de la web es independiente del estado de revisión del archivo documental descrito a continuación.

Este repositorio preserva material relacionado con la historia pública de “Jezu G”, respuestas a acusaciones, evidencia primaria y secundaria, correcciones, y un registro separado de publicaciones/hostigamiento posteriores.

## Qué es este repositorio

Es un archivo preparado por una **parte interesada**. No debe presentarse como una fuente neutral o como una versión definitiva de los hechos.

Su objetivo es que cada afirmación importante pueda rastrearse hasta una fuente y que un tercero pueda distinguir entre:

1. **hecho observable** — algo visible directamente en una fuente preservada;
2. **admisión** — algo reconocido expresamente por Jezu;
3. **alegación externa** — afirmación realizada por un tercero;
4. **inferencia** — conclusión que va más allá de lo directamente visible;
5. **no determinado** — punto que el corpus actual no permite resolver.

## Principios

- Conservar también evidencia desfavorable a Jezu.
- No convertir testimonios, acusaciones, memes, títulos o documentos de terceros en hechos probados.
- No usar “contexto” como sustituto de responsabilidad por conductas reconocidas.
- No usar el hostigamiento recibido en 2026 para reducir el peso de hechos anteriores: son expedientes distintos.
- Describir impacto sobre terceros solo cuando esté documentado por fuente o admisión; no inventarlo.
- Mantener correcciones visibles en Git. No reescribir silenciosamente errores materiales.
- Proteger datos sensibles, especialmente información de menores.

## Estructura

- `evidence/` — evidencia preservada y manifest.
- `docs/` — cronologías, respuestas y metodología.
- `data/` — matrices y datos estructurados.
- `acoso/` — registro separado de publicaciones, reclamos y hostigamiento de 2026.
- `private-references/` — auditorías internas, huecos y procedencia.
- `notes/` — notas auxiliares.
- `site-public/` — plantillas, páginas y expedientes autorizados para la web.
- `public-html/` — salida estática del generador y recursos compartidos.
- `tools/build_alejandria.py`, `tools/check_alejandria.py`, `tools/test_alejandria.py`, `tools/serve_alejandria.py` — generación, verificación, pruebas y vista previa local.

## Estado

El corpus sigue abierto. Una ausencia de evidencia no demuestra que un hecho no ocurriera; del mismo modo, una acusación no queda demostrada por el solo hecho de aparecer repetida en varias fuentes derivadas.

Antes de cualquier publicación pública deben existir copias redactadas de material con datos personales, menores o terceros innecesarios.

## Alejandría — consolidación documental (2026-10-15)

Estado documental: **material en consolidación; su incorporación a la web requiere revisión y autorización explícitas**. El repositorio es público; la expresión «archivo privado» de fases anteriores no describe su visibilidad actual.

Punto de entrada actualizado: [inventario y mapa de fuentes](docs/fase4_inventario_alejandria.md) y [expediente cronológico 2022–2023](docs/fase4_casos_2022_2023.md). Se conservan los análisis de fases anteriores como historial, incluso cuando la actualización posterior corrige sus pendientes.

Fuentes añadidas recientemente: exportación JSON completa del grupo «el pepe» (5.979 mensajes), versión HTML de consulta y tres conversaciones directas de Discord. Las fuentes originales están en `evidence/menores/originales/`. **El JSON es la copia de referencia para el historial grupal; el HTML es un derivado de lectura**.

- [Registro de límites, privacidad y preparación para futura web](docs/fase4_preparacion_public_html.md)
- [Correcciones y procedencia](docs/fase4_bitacora_correcciones.md)
- [Matriz de afirmaciones](data/fase3_claim_matrix.json), ahora con adendas de octubre.
- [Notas de recuperación pendientes](notes/fase3_huecos_pendientes.md).

**Regla especial:** no abrir, procesar, descargar ni previsualizar imágenes, videos, audio, adjuntos o enlaces multimedia del grupo «el pepe», incluidos derivados PNG/WebP ya presentes en el repositorio. Solo análisis textual del JSON/HTML sin cargar recursos remotos. El workflow anterior de generación visual queda suspendido. No se autoriza publicación automática.

La fase de desarrollo web está autorizada sobre código y contenido público de ejemplo. Esto no autoriza a trasladar originales, conversaciones completas o datos personales a `public-html/`. El generador no recorre `docs/`, `evidence/`, `md-s/` ni `private-references/`; solo lee las fuentes web expresamente autorizadas. La revisión documental, anonimización y autorización de cada expediente real siguen pendientes. Una web generada localmente no equivale a un sitio publicado.
