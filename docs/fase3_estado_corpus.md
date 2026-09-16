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
