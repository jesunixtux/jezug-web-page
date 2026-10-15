# Alejandría — bitácora de cambios y precisión documental

Estado: interno, 15-10-2026. Este archivo documenta **correcciones de descripción y procedencia**, no resuelve culpabilidad ni veracidad absoluta.

| Tema | Antes / riesgo de interpretación | Corrección / estado | Base |
| --- | --- | --- | --- |
| «el pepe» | Pendiente de recuperar MD grupal completo en documento de septiembre | JSON completo (5.979 mensajes) y HTML derivados presentes; el historial recuperado no garantiza mensajes borrados ni cobertura de otros canales | `evidence/menores/originales/` |
| DMs de menores | Fragmentos seleccionados en capturas | Se añadieron dos exportaciones de Ángel y una de Sprout/Tord; dar prioridad al contexto textual y al carácter privado | `evidence/menores/originales/` |
| Grindr / Danel | Riesgo de tratar frase «lo suscribi» como registro consumado | Frase documentada; ejecución no verificada. El autor sostiene en octubre que no lo realizó; testimonio retrospectivo no constituye prueba independiente | `EXT-B01`, matriz C04 |
| Fuente documental Grindr | C04 remitía a la parte 2 | El pasaje examinado está en la **parte 1**, páginas 4–5; se corrigió C04 | `EXT-B01` |
| «Saqué tu cell» | Riesgo de confundir modelo con número de teléfono | Según recuerdo actual del autor, «cell» significaba modelo mostrado en recuperación de Google; sin prueba independiente del mecanismo | declaración actual del autor, `PRI-G01` |
| IP / Danel | Riesgo de confundir obtener, compartir y amenazar | Publicación y amenazas visibles; origen de IP atribuido a Cris únicamente por declaración posterior, sin corroboración | `PRI-G01`, matriz C10 |
| Ángel / Ruitzo | Riesgo de utilizar ataque verbal documentado como prueba dirigida a Guillermo | Mensaje del 03-01-2023 dirigido a **Ruitzo y su pareja**; muestra participación inapropiada de Jezu, no una orden en contra de Guillermo | `PRI-D01`/`PRI-D02` |
| Tres menores | Riesgo de inferir dirección conjunta desde participación dispersa | Textos revisados no muestran instrucción expresa al grupo de tres; existencia fuera del corpus no puede excluirse | `PRI-G01`, `PRI-D01`, `PRI-D02`, `PRI-D03` |
| Evidencia visual | Matriz de septiembre cubría 105 piezas | Se mantienen 105 imágenes con procedencia histórica y 5 exportaciones textuales en sección nueva; no atribuir inspección visual nueva | `evidence/manifest.json` |
| Pipeline multimedia | Workflow anterior podía procesar capturas del grupo | Workflow desactivado por la restricción actual; no reactivarlo sin permiso expreso | `.github/workflows/prepare-el-pepe-ai-bundle.yml` |
| public-html | Carpeta ya creada en otra revisión/commit | **No se modifica en esta fase**; ninguna publicación derivada se considera aprobada hasta pasar redacción y privacidad | `docs/fase4_preparacion_public_html.md` |

**Nota editorial:** preservar siempre diferencias entre hechos de 2022–2023, testimonios retrospectivos de 2026 y afirmaciones externas; corregir errores con commits visibles, nunca mediante reescritura destructiva del historial.
