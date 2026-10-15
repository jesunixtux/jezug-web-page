# Archivo físico de evidencias

Estado: interno, no publicar.

Esta carpeta conserva evidencias primarias y referencias de trabajo. Los originales no deben alterarse a nivel binario. La Fase 3 solo reclasificó y renombró archivos para que el archivo sea auditable.

## Carpetas canónicas

- `guillermo/`
- `kirmo/`
- `leniloq-menita/`
- `wildo-ray/`
- `fan-de-lucky/`
- `menores/`
- `brigidos/`
- `md-grupal/`
- `otros/`

Las carpetas antiguas o alternativas pueden permanecer por historial, pero el manifest actualizado usa las carpetas canónicas anteriores.

## Fase 3 auditoría visual

- Imágenes revisadas: 105
- Movidas o renombradas: 100
- Duplicados exactos por SHA-256: 0
- Requieren redacción antes de publicación: 104

## Importación directa desde Library

El 2026-09-16 se intentó localizar por nombre exacto las capturas directas indicadas en la conversación de trabajo. No aparecieron los binarios UUID en las rutas locales revisadas, por lo que no se copiaron archivos que no estuvieran realmente disponibles.

El detalle queda en:

- `private-references/library_direct_import_audit.json`
- campo `direct_library_import_audit` de `evidence/manifest.json`

Algunas piezas ya existen como equivalentes preservados desde documentos o extracciones previas, pero no como el binario directo original de Library. Mantener esa distinción para no mezclar "evidencia ya preservada" con "original directo recuperado".

## Reglas

- No publicar contenido íntimo ni datos personales sensibles.
- No publicar datos identificatorios de menores.
- No convertir declaraciones, acusaciones, memes, miniaturas o textos de wiki en hechos probados.
- Antes de redacción pública, crear copias censuradas en una ruta separada; no modificar los originales.

## Exportaciones de Discord añadidas el 15-10-2026

Directorio privado `evidence/menores/originales/`:
- `el-pepe-completo.json` — fuente primaria de mensajes y metadatos del grupo (5.979 mensajes).
- `el-pepe-transcript.html` — derivado de consulta; no sustituye al JSON fuente.
- Tres HTML [DiscordKit] preservados de conversaciones con Ángel (dos) y Sprout/Tord.

El inventario visual de septiembre (`files`: 105) **no incluye estos cinco exportados**. Sus SHA de blob Git, tamaños y rutas se registran en la nueva sección `textual_exports` del `evidence/manifest.json`. No afirmar que son parte de la auditoría visual ni que todos los adjuntos fueron verificados.

**Regla vigente para «el pepe»: está prohibido abrir, visualizar, descargar o procesar sus archivos multimedia, incluyendo capturas/derivados ya existentes y enlaces externos en el JSON o HTML.** No generar previews, thumbnails ni indexaciones multimedia. Para trabajar usar solo contenido textual y metadatos. La futura publicación web no deberá exponer enlaces de adjuntos, correos, IP, nombres reales ni información identificatoria de menores.
