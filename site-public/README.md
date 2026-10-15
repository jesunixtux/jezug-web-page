# Alejandría: sitio público

Sitio estático sin dependencias de terceros, cuentas, analítica ni servicios externos.
El contenido de ejemplo está separado del archivo documental. No se configura ningún despliegue.

## Editar y comprobar

Desde la raíz del repositorio, con Python 3.10 o superior:

```powershell
python tools/build_alejandria.py
python tools/check_alejandria.py
python -m http.server 8765 --bind 127.0.0.1 --directory public-html
```

Abre `http://127.0.0.1:8765/index.html`. El servidor es local y no publica el sitio.
Las páginas generadas también se pueden abrir como archivos; la persistencia del tema depende del almacenamiento que permita el navegador para `file://`.

- `pages.json`: lista explícita de páginas, rutas y metadatos.
- `layout.html`: navegación, cabecera y pie compartidos.
- `pages/*.html`: contenido público editable.
- `../public-html/assets/site.css`: estilos y adaptación a móvil.
- `../public-html/assets/theme.js`: recuperación del tema antes de cargar estilos.
- `../public-html/assets/site.js`: tema, menú móvil y búsqueda.
- `../public-html/assets/search-index.js`: índice generado; no editar directamente.

Edita las fuentes y ejecuta el generador; no edites los HTML generados en `public-html/`.
El generador solo lee los archivos indicados en `pages.json` y la plantilla. No busca ni importa documentos desde otras carpetas.

## Agregar un expediente

1. Copia `pages/expediente-ejemplo.html` a un nuevo archivo dentro de `pages/`.
2. Completa únicamente contenido público revisado. Elimina el aviso de ejemplo solo cuando corresponda.
3. Agrega una entrada en `pages.json` con un `id` único, `nav: "casos"`, título, descripción, `source` y una ruta como `casos/nombre-del-expediente/index.html`.
4. Añade un enlace en `pages/casos.html`, usando `{{root}}` delante de la ruta. Usa también este prefijo en enlaces y recursos del contenido para permitir rutas anidadas.
5. Conserva los apartados de alcance, cronología, afirmaciones, referencias, límites y revisiones. Aplica los criterios documentales existentes; no completes lagunas con hechos ficticios.
6. Ejecuta el generador y el verificador. Revisa el cambio de Git antes de incorporar contenido al historial.

La búsqueda se actualiza al generar el sitio y solo incluye el texto de las páginas explícitas, sin menús ni recursos decorativos. Admite varias palabras, mayúsculas y consultas sin tildes. Las consultas no salen del sitio.

## Decisiones editoriales de esta versión

- Las cifras y los años de la portada anterior se retiraron de la interfaz porque no se verificaron dentro del contenido público autorizado. No se alteraron sus materiales de origen.
- Cronología, Casos, Evidencias y Fuentes presentan estados pendientes en lugar de contenido documental sin revisar.
- El ejemplo de expediente es una estructura vacía, sin personas, acontecimientos ni testimonios ficticios.
- Metodología traslada el criterio y las categorías de la portada y los cuatro principios de lectura de Transparencia, conservando su redacción.
- Se conserva el texto de las secciones de Transparencia y sus identificadores. La revisión del contenido original sigue fechada el 15 de octubre de 2026.
- Se conservan las directivas `noindex`, `nofollow`, `noarchive` existentes. No son un control de acceso: todo archivo que se incluya en el sitio debe ser apto para acceso público.
- Los archivos locales preexistentes en `public-html/404/` y `public-html/Informacion/Sobre-la-pagina/` no forman parte del generador y no se modifican.

## Pendiente antes de incorporar documentación real

Revisión editorial de los expedientes, referencias públicas precisas, registro documental de correcciones y mecanismos de consulta. La búsqueda no verifica las fuentes ni consulta el archivo privado.
