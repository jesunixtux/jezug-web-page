# Registro de cambios de transcripciones

Crear un archivo por cada versión editada.

Formato recomendado:

```md
# <título>

Original: ../original/<archivo>
Editado: ../edited/<archivo>
Video original: <URL o PENDIENTE>

## Cambios

- [00:12:31] "X" -> "Y"
  - Tipo: corrección de reconocimiento automático
  - Motivo: el audio permite identificar claramente "Y"

- [00:22:05] dato personal -> [REDACTADO]
  - Tipo: privacidad
  - Motivo: tercero no necesario para comprender el hecho

- [00:30:11] frase conservada literalmente
  - Nota editorial: la versión resumida usa una formulación menos dramática, pero el original no fue alterado.
```

No borrar entradas antiguas: si una corrección posterior demuestra que una edición estaba mal, añadir una nueva corrección y dejar Git como historial.
