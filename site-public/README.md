# Alejandría: sitio estático y expedientes

La fase 2 amplía el generador existente. Conserva la interfaz gris carbón e índigo, el menú lateral, la declaración de Transparencia y los criterios documentales. El tema predeterminado es oscuro; el modo claro se guarda en el navegador. No hay cuentas, analítica, dependencias de terceros, servicios de búsqueda externos ni despliegues automáticos.

La web contiene un expediente de estructura vacío. No hay acontecimientos, acusaciones, evidencias ni conclusiones históricas reales publicadas en esta versión.

## Generar, verificar y previsualizar

Requiere Python 3.10 o superior. Desde la raíz del repositorio:

```powershell
python -B tools/build_alejandria.py
python -B tools/check_alejandria.py
python -B tools/test_alejandria.py
python -B tools/serve_alejandria.py
```

Abre `http://127.0.0.1:8765/index.html`. La vista previa escucha solo en `127.0.0.1`, sirve `public-html/`, bloquea los listados de directorios y rutas que salgan de esa carpeta, y responde con la página propia y código HTTP 404 ante rutas inexistentes. Usa `--port 8766` si el puerto predeterminado está ocupado. Detén el servidor con Ctrl+C.

Los enlaces ordinarios son relativos y permiten abrir las páginas como archivos. La 404 utiliza rutas absolutas desde la raíz web para funcionar incluso al solicitar una ruta inexistente profundamente anidada. Su aspecto completo debe comprobarse a través del servidor local.

## Fuentes y salida

| Archivo o carpeta | Responsabilidad |
| --- | --- |
| `pages.json` | Lista explícita de páginas HTML, con autorización `public` y `search` |
| `layout.html` | Cabecera, navegación lateral, buscador y pie compartidos |
| `pages/*.html` | Contenido público de las páginas generales |
| `expedientes.json` | Lista explícita de expedientes y sus autorizaciones |
| `expedientes/*.json` | Datos públicos redactados para cada expediente |
| `templates/expediente.html` | Estructura común de todos los expedientes |
| `templates/timeline.html` | Cronología global y controles de filtrado |
| `settings.json` | `base_path` de la instalación, `/` por defecto, utilizado por la 404 |
| `../public-html/assets/site.css` | Estilos, contraste, foco, responsive y transiciones discretas |
| `../public-html/assets/theme.js` | Tema guardado antes de cargar los estilos |
| `../public-html/assets/site.js` | Menú móvil, tema y búsqueda |
| `../public-html/assets/timeline.js` | Filtros locales de cronología y estado en la URL |
| `../public-html/assets/search-index.js` | Índice generado; no editar directamente |
| `../public-html/assets/generated-files.json` | Inventario y huellas de las salidas generadas; no editar directamente |

Edita las fuentes y vuelve a generar. Los HTML, el índice y `robots.txt` son salidas del generador. Los recursos CSS/JS compartidos se editan directamente en `public-html/assets/`.

El generador no recorre el repositorio ni copia documentos: lee únicamente las plantillas, las páginas con `public: true` y los JSON de expedientes expresamente autorizados. Rechaza rutas que salgan de las carpetas de fuentes permitidas y enlaces de referencias que no sean HTTPS. No descarga fuentes ni abre multimedia.

## Crear un expediente sin duplicar HTML

1. Copia `expedientes/expediente-ejemplo.json` dentro de la misma carpeta y asigna un `id` único con minúsculas, números y guiones.
2. Redacta título, descripción, introducción, contexto, alcance y período; completa las listas documentales cuando haya contenido revisado. Los valores de texto son texto plano: el generador escapa HTML automáticamente.
3. Mantén `example: true` si sigue siendo una estructura o demostración. Para un expediente real revisado, usa `example: false`; la interfaz lo marcará «Expediente en revisión».
4. Añade en `expedientes.json` una entrada como `{ "source": "nombre.json", "public": true, "search": true }` cuando el archivo esté expresamente autorizado para la web y el buscador.
5. Ejecuta el generador, el verificador y las pruebas. Revisa el diff antes de incorporar contenido al historial.

La ruta será `casos/<id>/index.html`. El caso aparece automáticamente en Casos, su cronología pública aparece en Cronología y su contenido autorizado se añade al buscador. No hay que editar el menú, copiar una página HTML ni registrar cada expediente en `pages.json`.

`public: false` impide incluso abrir el JSON durante la generación. `search: false` permite presentar el expediente aprobado, pero excluye su cuerpo y sus acontecimientos del índice. El título y la descripción siguen siendo visibles en el listado público de Casos y pueden aparecer como texto de ese listado.

Al revocar la publicación o cambiar una ruta, el siguiente build retira el HTML anterior solo si está registrado en el inventario y conserva el contenido generado. No elimina archivos ajenos al generador. Si se editó manualmente una salida obsoleta, la generación se detiene para que se revise, sin borrarla silenciosamente. Los cambios de saltos de línea de Git no se consideran una edición de contenido.

Estas banderas solo controlan la salida web. **El repositorio es público:** no deben guardarse borradores sensibles, datos personales, conversaciones completas ni originales privados en estas carpetas, aunque sus banderas estén desactivadas.

### Campos del expediente

Todos los campos del ejemplo son obligatorios; se admiten textos vacíos y listas vacías para documentar lo pendiente. La validación señala claves desconocidas o faltantes.

| Campo | Contenido |
| --- | --- |
| `id`, `title`, `description`, `example`, `period` | Identidad, presentación y estado del expediente |
| `introduction`, `context`, `scope` | Introducción, contexto y alcance; los saltos de línea separan párrafos |
| `events` | Acontecimientos públicos o lista vacía |
| `claims` | Afirmaciones examinadas con categoría, límites y referencias |
| `references` | Referencias públicas redactadas y autorizadas |
| `contradictions` | Lista de contradicciones que requieren contraste |
| `undetermined` | Lista de vacíos y puntos no determinados |
| `conclusions` | Lista de conclusiones expresamente provisionales |
| `updates` | Registro de cambios, motivos y fuentes que los sustentan |

Cada referencia tiene `id`, `public`, `title`, `url` y `context`. `public` debe ser `true` para que pueda mostrarse o enlazarse; `url` debe ser una URL HTTPS pública expresamente revisada, sin credenciales. No se copian sus documentos ni se comprueba su contenido automáticamente. Las referencias no autorizadas se excluyen y no pueden ser utilizadas por acontecimientos, afirmaciones o correcciones publicados.

Cada afirmación tiene `id`, `category`, `text`, `limits` y `references` (lista de identificadores de referencias públicas del propio expediente). Las categorías conservan los criterios existentes:

| Clave | Categoría documental |
| --- | --- |
| `hecho-observable` | Hecho observable |
| `admision` | Admisión |
| `alegacion-externa` | Alegación externa |
| `inferencia` | Inferencia |
| `no-determinado` | No determinado |

Cada corrección tiene `date`, `change`, `reason` y `references`: qué cambió, cuándo, por qué y qué referencias públicas motivaron la revisión. No hay registros inventados para rellenar el ejemplo.

### Acontecimientos y filtros

Cada acontecimiento tiene `id`, `public`, `date`, `title`, `summary`, `type` y `references`, con `date_label` opcional para expresar una fecha incierta. El identificador es único dentro de su expediente.

- `date`: `YYYY`, `YYYY-MM`, `YYYY-MM-DD` o `null` si permanece sin determinar. La validación comprueba que las fechas existan.
- `type`: `acontecimiento`, `documento`, `publicacion` o `revision`. El tipo de entrada no reemplaza la categoría documental de una afirmación.
- `references`: lista de identificadores de referencias públicas del expediente. Puede estar vacía; la interfaz lo indica expresamente.
- `public: false`: excluye la entrada de las páginas y la búsqueda.

La cronología se ordena de forma ascendente; las fechas sin determinar aparecen al final. Los filtros por año, caso y tipo se derivan de las entradas públicas, se combinan y se conservan en los parámetros `year`, `case` y `type` de la URL. Hay estado sin resultados y botón para limpiar. Sin JavaScript se muestran todas las entradas. Con una cronología vacía los controles se presentan desactivados, sin inventar opciones.

Cada entrada enlaza a su expediente y a sus referencias. Sus enlaces estables usan `#evento-<id-expediente>-<id-entrada>`. El buscador añade resultados individuales para los acontecimientos autorizados y enlaza a esos fragmentos.

## Búsqueda y privacidad de la salida

La búsqueda compara el texto local de las páginas expresamente autorizadas, admite varias palabras, mayúsculas y consultas sin tildes. Las consultas no se envían a servicios externos. Los menús, formularios y elementos decorativos no se indexan. La cronología se indexa por entrada autorizada para respetar también `search: false` en un expediente.

La generación no consulta `docs/`, `evidence/`, `md-s/` ni `private-references/`. La autorización de una fuente web debe seguir a su revisión editorial; ninguna validación técnica certifica que un texto esté anonimizado o que una afirmación sea verdadera.

## 404 y rastreadores

Se generan `404.html` y el alias existente `404/404.html` desde una única fuente. El servidor local ya responde con código 404. Al escoger un alojamiento en el futuro habrá que asociar allí `404.html` con las rutas inexistentes; no se ha configurado alojamiento ni despliegue. Si se sirve bajo una subcarpeta, se ajustará `base_path` y el punto de montaje del servidor.

Se sustituyó el archivo vacío `robot.txt` por `robots.txt`, con `User-agent: *` y `Disallow: /` mientras el sitio esté en preparación. Se conservan los metadatos `noindex, nofollow, noarchive`. Son instrucciones para rastreadores; no proporcionan privacidad ni control de acceso.

La declaración de Transparencia y los criterios de Metodología permanecen intactos. El archivo vacío preexistente `public-html/Informacion/Sobre-la-pagina/index.html` se conserva fuera del generador; no está enlazado ni indexado.

## Alcance de la verificación

El verificador compara todas las salidas generadas con las fuentes autorizadas, comprueba enlaces y fragmentos locales, navegación, identificadores y etiquetas accesibles, 404, robots y contenido del índice. Los enlaces HTTPS aprobados se validan por formato; no se descargan ni se certifica su disponibilidad.

Las pruebas utilizan exclusivamente datos sintéticos en una carpeta temporal. Comprueban publicación y búsqueda por autorización explícita, exclusión de fuentes/entradas/referencias no aprobadas, nuevas rutas y enlaces, categorías, fechas, escape de HTML y consistencia de la 404. Los datos de prueba no se incorporan al sitio generado.

Antes de añadir documentación histórica real quedan la revisión editorial, las referencias públicas precisas, la anonimización que corresponda y la redacción del registro de correcciones. La arquitectura web está preparada para esos contenidos.
