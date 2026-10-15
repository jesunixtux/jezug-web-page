# Alejandría — verificación de la fase 2

Fecha: 15 de octubre de 2026. Alcance: código web, fuentes públicas de ejemplo, herramientas de generación y README. Se amplió la arquitectura existente; no se configuró publicación ni despliegue.

## Cambios

- `layout.html` y `public-html/assets/site.css`, `site.js`, `theme.js`: navegación compartida, nombre accesible de la marca, enlaces integrados en párrafos subrayados, foco del menú móvil, controles táctiles y transiciones discretas que respetan movimiento reducido. Tema oscuro predeterminado y modo claro persistente.
- `expedientes.json`, `expedientes/expediente-ejemplo.json`, `templates/expediente.html` y `tools/alejandria_content.py`: expedientes estructurados, categorías documentales existentes, referencias públicas, contradicciones, incertidumbre, conclusiones provisionales y correcciones. El antiguo HTML específico del ejemplo se sustituyó por la plantilla común.
- `pages/casos.html`, `pages/cronologia.html`, `templates/timeline.html` y `public-html/assets/timeline.js`: listado automático de expedientes, cronología generada desde acontecimientos públicos y filtros combinables por año, caso y tipo.
- `pages.json`, `settings.json`, `pages/404.html`, `tools/build_alejandria.py`: autorizaciones explícitas de publicación y búsqueda, 404 canónica y alias, generación determinista e inventario con huellas de salidas. La revocación de una publicación retira únicamente salidas generadas que no fueron editadas manualmente.
- `tools/check_alejandria.py`: comparación con plantillas y datos autorizados, navegación, enlaces, fragmentos, etiquetas accesibles, robots y contenido exacto del índice.
- `tools/test_alejandria.py`: diez pruebas con datos sintéticos aislados. No se incorporan al sitio.
- `tools/serve_alejandria.py`: vista previa exclusiva en localhost, 404 con estado HTTP correcto, sin listados de directorios ni rutas que salgan de la carpeta pública.
- `README.md` y `site-public/README.md`: estado real del repositorio público, instrucciones de autoría, autorizaciones, filtros, búsqueda y verificación.

## Salidas generadas

Se regeneraron `public-html/index.html`, `Informacion/index.html`, `buscar/index.html`, `casos/index.html`, `casos/expediente-ejemplo/index.html`, `cronologia/index.html`, `evidencias/index.html`, `fuentes/index.html` y `metodologia/index.html`.

Se completó `public-html/404/404.html`, se añadió `public-html/404.html` y se sustituyó el archivo vacío `robot.txt` por `robots.txt`. También se actualizaron `assets/search-index.js` y el inventario `assets/generated-files.json`.

La declaración fuente `site-public/pages/transparencia.html` y la fuente de Metodología permanecen intactas. En las páginas generales solo cambian la cabecera compartida y la carga del recurso de cronología, salvo Casos y Cronología, que incorporan sus nuevas interfaces.

## Resultados

| Comprobación | Resultado |
| --- | --- |
| Generador | 10 páginas canónicas; 11 archivos HTML contando el alias de la 404 |
| Verificador | 248 enlaces/recursos locales válidos; fragmentos, navegación, etiquetas, robots y salidas consistentes con sus fuentes |
| Índice público | 8 entradas: páginas generales y expediente de estructura; cero acontecimientos históricos |
| Pruebas automatizadas | 10 correctas: nueva publicación, enlaces, autorizaciones, exclusiones, revocación, conservación de archivos manuales, categorías, fechas, escape y 404 |
| Responsive | 110 combinaciones: 11 salidas × anchos de 320, 375, 768, 1024 y 1440 px × temas claro y oscuro; sin desbordamiento horizontal |
| Sin JavaScript | Las 11 salidas conservan navegación visible a 320 px, sin desbordamiento |
| Teclado | Menú móvil, cierre con Escape y retorno de foco, acceso al buscador con `/` y enlace para saltar al contenido comprobados |
| Tema | Oscuro inicial, cambio a claro, preferencia conservada entre páginas y funcionamiento con almacenamiento bloqueado |
| Búsqueda | Mayúsculas, tildes, varias palabras, consulta vacía, sin resultados y HTML introducido como texto; sin inyección |
| Filtros | Datos sintéticos en un iframe temporal: año, caso, tipo, combinaciones sin coincidencias, limpieza, restauración desde URL y valores inválidos |
| 404 HTTP | Ruta inexistente profunda devuelve 404 y la interfaz propia, con recursos y enlaces correctos |
| Lighthouse móvil | Accesibilidad 100/100 y buenas prácticas 100/100 en Cronología y expediente de ejemplo |
| JavaScript | Los cuatro recursos JavaScript pasan `node --check`; sin errores de ejecución observados en páginas normales |
| Integridad editorial | Fuentes de Transparencia y Metodología idénticas a las anteriores; originales y carpetas documentales sin cambios |

La solicitud intencional de una ruta inexistente produce el aviso de red 404 esperado en la consola; no es un error de JavaScript. El indicador SEO de Lighthouse refleja el bloqueo deliberado de indexación durante la preparación y no se ha habilitado el rastreo para mejorar esa puntuación.

## Límites y pendientes

- La verificación automatizada no sustituye una auditoría completa con lectores de pantalla ni la revisión editorial de los futuros expedientes.
- La cronología de producción permanece vacía. El ejemplo no contiene hechos, testimonios ni conclusiones reales.
- Las futuras referencias HTTPS deberán revisarse editorialmente. La herramienta valida su formato y autorización, sin descargar documentos ni comprobar disponibilidad remota.
- La asociación de `404.html` con rutas inexistentes en un alojamiento futuro dependerá del servidor elegido. La vista previa local ya la implementa.
- Quedan la redacción histórica, las referencias públicas precisas, la anonimización necesaria y el registro documental de correcciones. No requieren cambiar la estructura principal del sitio.
- No se añadieron fuentes privadas al índice ni se importó contenido automáticamente desde carpetas documentales. No se accedió a multimedia restringida, no se configuraron despliegues y no se crearon commits durante esta fase.
