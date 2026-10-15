# jezug-web-page

Archivo documental privado en construcción.

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

## Estado

El corpus sigue abierto. Una ausencia de evidencia no demuestra que un hecho no ocurriera; del mismo modo, una acusación no queda demostrada por el solo hecho de aparecer repetida en varias fuentes derivadas.

Antes de cualquier publicación pública deben existir copias redactadas de material con datos personales, menores o terceros innecesarios.

## Alejandría — consolidación documental (2026-10-15)

Estado: **archivo privado en consolidación; no apto aún para publicación pública**.

Punto de entrada actualizado: [inventario y mapa de fuentes](docs/fase4_inventario_alejandria.md) y [expediente cronológico 2022–2023](docs/fase4_casos_2022_2023.md). Se conservan los análisis de fases anteriores como historial, incluso cuando la actualización posterior corrige sus pendientes.

Fuentes añadidas recientemente: exportación JSON completa del grupo «el pepe» (5.979 mensajes), versión HTML de consulta y tres conversaciones directas de Discord. Las fuentes originales están en `evidence/menores/originales/`. **El JSON es la copia de referencia para el historial grupal; el HTML es un derivado de lectura**.

- [Registro de límites, privacidad y preparación para futura web](docs/fase4_preparacion_public_html.md)
- [Correcciones y procedencia](docs/fase4_bitacora_correcciones.md)
- [Matriz de afirmaciones](data/fase3_claim_matrix.json), ahora con adendas de octubre.
- [Notas de recuperación pendientes](notes/fase3_huecos_pendientes.md).

**Regla especial:** no abrir, procesar, descargar ni previsualizar imágenes, videos, audio, adjuntos o enlaces multimedia del grupo «el pepe», incluidos derivados PNG/WebP ya presentes en el repositorio. Solo análisis textual del JSON/HTML sin cargar recursos remotos. El workflow anterior de generación visual queda suspendido. No se autoriza publicación automática.

La carpeta `public-html/` ya existe en la rama, pero queda expresamente **fuera de la fase actual**: no asumir que sus archivos actuales constituyen una web publicada ni editarla antes de completar el expediente, anonimización y revisión final.
