# Revisión externa por modelo — 2026-09-21

Estado: nota metodológica interna. No constituye evidencia sobre los hechos.

Se probó el repositorio con un modelo externo (Grok) usando dos tipos de instrucciones.

## Primera pasada

La primera consulta pedía opinión, pros/contras y cambios para que el repositorio no pareciera una “lavada de manos”.

Resultado: produjo observaciones útiles, pero también lenguaje evaluativo y presuposiciones inducidas por el propio prompt.

Problemas detectados:

- lenguaje moralizante;
- atribución implícita de intención;
- uso de expresiones absolutas como “siempre”;
- afirmaciones sobre impacto en terceros sin identificar evidencia del impacto;
- confusión entre cautela probatoria y sesgo favorable.

## Segunda pasada

Se pidió una auditoría documental independiente:

- sin asumir que el repo era una defensa honesta ni una lavada de manos;
- sin asumir que las acusaciones externas eran correctas o exageradas;
- distinguiendo hecho, admisión, alegación e inferencia;
- señalando límites del material.

Resultado: la respuesta fue sustancialmente más útil y neutral.

Puntos adoptados:

- declarar expresamente que el archivo es mantenido por una parte interesada;
- usar categorías epistemológicas explícitas;
- separar el expediente de hostigamiento 2026 del historial anterior;
- desarrollar una capa personal de responsabilidad sin convertirla en defensa técnica;
- describir impacto solo cuando esté documentado;
- mantener material desfavorable dentro del corpus;
- reconocer puntos no determinados.

Puntos no adoptados literalmente:

- tratar toda limitación de evidencia como “sesgo favorable”;
- eliminar frases de alcance probatorio como “no determinado”;
- usar una auditoría de IA como prueba de culpabilidad, inocencia o neutralidad.

## Regla resultante

Un modelo externo puede auditar la organización y consistencia del corpus, pero no convierte el repositorio en una fuente independiente de los hechos.

La futura web/agente debe poder cuestionar tanto la versión de Jezu como una acusación externa cuando la evidencia no alcance.
