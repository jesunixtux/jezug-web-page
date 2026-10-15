# Fase 3 - estado del corpus

Estado: interno. No publicar.

## Ya preservado

- Documentos de Drive preservados como snapshots en `docs/drive-downloads/`.
- Auditoria visual de 105 imagenes extraidas, con reclasificacion en carpetas canonicas y hashes en `evidence/manifest.json`.
- Capturas clave de Kirmo del 18/02/2023.
- Varias piezas sobre Leniloq/Menita, incluida invitacion de Leny preservada como captura extraida.
- Varias piezas sobre Wildo/Ray, incluido comentario de Ray Mioda y capturas contextuales.
- Capturas de Fan de Lucky y materiales relacionados con el documento reciente.
- Matriz inicial de afirmaciones en `data/fase3_claim_matrix.json`.

## Importacion directa desde Library

Se intento localizar por nombre exacto los UUID indicados en la conversacion previa. No aparecieron como binarios recuperables en las rutas locales revisadas. Por eso no se duplicaron archivos ni se afirmo una importacion directa inexistente.

Quedo registrado:

- `private-references/library_direct_import_audit.json`
- `evidence/manifest.json` campo `direct_library_import_audit`

Algunas capturas tienen equivalentes ya preservados en el repo, pero no el binario directo con UUID de Library. Las mas importantes son:

- Invitacion "Leny": preservada como `evidence/leniloq-menita/fecha-desconocida_fase3-053_correo-invitacion-propietario-leny.png`.
- Comentario Ray Mioda/Leniloq: preservado como `evidence/wildo-ray/fecha-desconocida_fase3-084_comentario-ray-mioda-leniloq-acoso.png`.
- Comentario Leniloq/Menita: preservado como `evidence/leniloq-menita/fecha-desconocida_fase3-070_comentarios-leniloq-original.png`.
- Respuesta publica de Jezu: preservada parcialmente como `evidence/brigidos/fecha-desconocida_fase3-001_youtube-respuesta-publica-jezu.png`.

## Recuperación desde ChatGPT Library — 2026-09-21

Una nueva búsqueda sobre archivos conservados en conversaciones anteriores localizó varios binarios directos que la auditoría del 16/09 había marcado como no encontrados. Entre ellos hay material de:

- Menita/Leniloq;
- conversaciones con Eyden;
- hilo de X y disculpas públicas de abril de 2026;
- conversaciones Puck/Neo-Brigidos y Hector/Puck;
- capturas de videos previamente registradas solo por referencia.

La existencia de estos archivos en Library ya está registrada en `private-references/library_direct_import_audit.json` con sus identificadores persistentes. **Aún debe distinguirse entre “localizado en Library” y “copiado físicamente al repositorio”**; no afirmar lo segundo hasta incorporar el binario y registrar su hash en `evidence/manifest.json`.

## Sigue faltando

- Binario directo de `cf4fb209-e0da-46bd-a9b0-8a88fcd13cad.png` sobre Menita/Jesus del 21/12/2025.
- Capturas directas de Eyden: malentendido, postura neutral, directo Ray/Leniloq, diferencia de edad y reflexion sobre Leni/Menita.
- Capturas del hilo de X del 20/04/2026 y continuaciones.
- Capturas directas de disculpas publicas y mencion explicita del uso de cuenta de Leniloq.
- Conversaciones directas Puck/Neo-Brigidos y Hector/Puck por UUID.
- Captura de que Wildo/Ray ya habia publicado su rostro en 2021.
- Conversacion con supercole del 18/04/2023 donde corrige/retracta acusacion.
- Transcripcion completa con timestamps del video "Jezu G Lo que quiso ocultar".
- MD grupal completo donde agregaron a Jezu para debatir/discutir la funa.

## Privacidad

No se copiaron contenidos intimos ni capturas de autolesiones a carpetas normales. Si aparecen luego, deben registrarse solo como referencia privada o `never_publish=true`, sin redistribuir el contenido.

## Cierre provisional

El corpus es suficiente para empezar una redaccion interna de cronologia y respuestas graves, pero no debe considerarse cerrado para publicacion. La publicacion requiere, como minimo:

- transcripcion del video reciente;
- materializacion de las capturas directas mas importantes que hoy solo existen como referencias;
- copias redactadas para cualquier evidencia con menores, datos personales o terceros innecesarios;
- revision final afirmacion por afirmacion.

## Adenda de corpus — 2026-10-15

**Actualización posterior que prevalece sobre los pendientes de septiembre sin borrar el registro histórico.**

- Se incorporó la exportación completa de texto/metadatos del MD grupal «el pepe» en `evidence/menores/originales/el-pepe-completo.json` (5.979 mensajes, 19 cuentas según exportación). Su HTML de consulta está en la misma carpeta, como derivado.
- Hay tres exportaciones privadas de conversaciones directas: Ángel (dos cuentas) y Sprout/Tord (una cuenta). Su inclusión permite contrastar fragmentos de capturas con conversaciones más extensas; **no garantiza recuperación de mensajes eliminados ni de otras plataformas**.
- Los 105 ítems de `evidence/manifest.json` siguen siendo el inventario visual de septiembre. Los cinco archivos textuales nuevos se registran en `textual_exports`, aparte y sin fingir que recibieron la auditoría visual de septiembre.
- Los dos documentos de Los Brígidos siguen preservados en `docs/drive-downloads/`. En la comprobación de metadatos de Google Drive de 2026-10-15 sus últimas modificaciones constaban ambas el 6 de septiembre de 2026. Esto se refiere solo a esos dos archivos, no a otras publicaciones.
- Los borradores `fase3_capa1_cronologia.md`, `fase3_capa2_respuestas_graves.md` y la matriz cuentan con adendas de octubre. Consultar también `docs/fase4_casos_2022_2023.md` para separar los conflictos de Danel, Guillermo y Ruitzo.
- Por restricción expresa del titular del archivo, **está prohibido examinar o transformar cualquier multimedia o adjunto del grupo «el pepe»**, incluso archivos locales en `md-s/el pepe/`; la revisión se limita a texto y metadatos sin acceder a enlaces.
- Estado editorial: suficiente para **trabajo interno** y reconstrucción provisional, **insuficiente para publicación pública** hasta comprobar fuentes, anonimizar identidades y contar con la revisión de privacidad.

Esta adenda no transforma recuerdos retrospectivos en hechos comprobados ni convierte la ausencia de una orden en los textos supervivientes en prueba de que nunca existiera en otros canales.
