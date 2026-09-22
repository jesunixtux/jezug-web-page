# Bundle IA — el pepe / parte 01

Este directorio es **derivado**. Los PNG numéricos de `md-s/el pepe/` siguen siendo los originales y no se modifican.

## Objetivo

Reducir el costo visual/contextual cuando otra IA necesite revisar esta parte del grupo de Discord.

- Originales actuales: **31** archivos.
- Índices incluidos: **0–30**.
- `optimized/`: una copia WebP ligera por captura.
- `pages/`: páginas de revisión con hasta **3 capturas consecutivas**.
- `manifest.json`: relación exacta entre derivado y original, dimensiones y SHA-256.

## Cómo pasárselo a otra IA

1. Entregar primero este README y `manifest.json`.
2. Para una primera lectura, usar solo `pages/` en orden.
3. Si una frase, nombre, fecha o autoría resulta importante, abrir el archivo correspondiente en `optimized/`.
4. Para una cita o verificación definitiva, volver siempre al PNG original.
5. No inferir que un mensaje pertenece a una persona solo porque aparece cerca de otro.
6. Distinguir mensaje visible, reacción, meme compartido, interpretación y contexto aportado por el archivista.
7. No convertir la ausencia de spam en prueba de que no existían otros mensajes.

## Contexto aportado por el archivista

El archivista describe este grupo como un MD grupal donde varios participantes, incluido Jezu, se burlaban o insultaban a Danel / Montaña VHS.

Ese dato debe tratarse como **contexto aportado**, no como sustituto de leer las capturas. La atribución de cada mensaje debe hacerse imagen por imagen.

## Spam y omisiones

Se permite dejar fuera spam, stickers repetidos o contenido sin relación **solo cuando no cambie el sentido del intercambio**. Si existe un salto entre capturas, una IA debe tratarlo como un hueco y no inventar qué ocurrió ahí.

## Integridad

Los derivados pueden comprimirse o regenerarse. Los hashes de los originales están en `manifest.json`; cualquier conclusión documental importante debe poder trazarse de vuelta al PNG fuente.
