# Transcripciones de videos y directos

Esta carpeta preserva transcripciones y subtítulos vinculados al expediente.

> Nota de formato: **SRT**, no “STR”. Un archivo `.srt` contiene bloques de subtítulos con marcas de tiempo. Algunos materiales recuperados solo existen como `.txt` generado por servicios de subtítulos; esos archivos se conservan con su extensión real y no se renombran falsamente a SRT.

## Regla principal: original y edición nunca se mezclan

`original/`
: copia preservada tal como fue recuperada. No corregir ortografía, nombres, timestamps ni frases aunque la transcripción automática esté equivocada.

`edited/`
: versión revisada/anotada para lectura. Puede corregir errores de transcripción, anonimizar datos, quitar elementos innecesariamente dramáticos o añadir contexto, pero **nunca debe presentarse como cita literal del video original**.

`changes/`
: registro de cambios entre el original y la versión editada.

## Qué debe acompañar a cada video/directo

Cada entrada del `manifest.json` debería incluir, cuando sea posible:

- título exacto;
- canal/autor;
- fecha;
- URL original de YouTube;
- ID del video;
- si el enlace sigue disponible o solo es histórico;
- formato del archivo recuperado (`srt`, `txt`, etc.);
- origen de la transcripción (YouTube auto-generated, DownSub, manual...);
- ruta del original;
- ruta de la versión editada;
- motivo de las modificaciones;
- estado de verificación contra el audio/video.

## Etiquetas obligatorias para versiones editadas

Toda versión modificada debe comenzar con algo equivalente a:

> **VERSIÓN EDITADA / ANOTADA.** Esta no es la transcripción original. Se han realizado correcciones, redacciones o cambios editoriales. Consulte la copia preservada en `../original/` y el registro en `../changes/`.

Si se modifica una frase por claridad o para reducir lenguaje dramático, el cambio debe quedar registrado. No se debe sustituir silenciosamente una afirmación del hablante por una formulación más favorable o desfavorable.

## Citas

Para una cita textual importante:

1. preferir el audio/video original;
2. usar el SRT/TXT como ayuda de localización;
3. señalar si el subtítulo es automático;
4. no tratar un error de reconocimiento de voz como palabras reales del hablante.

## Privacidad

Las versiones públicas deben anonimizar menores y datos personales innecesarios. El original privado puede conservarse para integridad documental, pero no debe exponerse automáticamente en una futura web pública.
