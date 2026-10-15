# Alejandría — inventario y mapa maestro (15-10-2026)

**Estado:** privado, documento de coordinación. Nada en este archivo constituye dictamen jurídico ni verdad histórica exhaustiva. Este archivo es producido por una parte interesada.

## 1. Principios editoriales

El corpus distingue (a) hecho observable, (b) declaración/admisión del autor, (c) alegación externa, (d) inferencia, (e) no determinado. Conservar material que perjudique al autor con igual visibilidad; no confundir capturas, comentarios y datos de plataforma con verificación independiente.

## 2. Fuentes conservadas

| ID | Fuente | Ruta | Nivel / límite |
| --- | --- | --- | --- |
| PRI-G01 | «el pepe» export completo: 5.979 mensajes | `evidence/menores/originales/el-pepe-completo.json` | Primaria textual de mensajes conservados, **no todo el universo de interacciones**. Prohibido acceder a multimedia y enlaces de adjuntos. |
| DER-G01 | «el pepe» consulta HTML | `evidence/menores/originales/el-pepe-transcript.html` | Derivado, incluye avatares incrustados; no sustituye a PRI-G01. |
| PRI-D01 | Ángel, cuenta exportada 1 | `evidence/menores/originales/[DiscordKit] Angel_DirectMessages_20261014_233252.html` | DM histórico preservado. |
| PRI-D02 | Ángel, cuenta exportada 2 | `evidence/menores/originales/[DiscordKit] 💎ANGEL💎_DirectMessages_20261015_000105.html` | DM histórico preservado. |
| PRI-D03 | Sprout/Tord | `evidence/menores/originales/[DiscordKit] 𓂀 𝕊𝕡𝕣𝕠𝕦𝕥🍓 𓂀_DirectMessages_20261015_000741.html` | DM histórico preservado. |
| EXT-B01 | Documento Los Brígidos, parte 1 | `docs/drive-downloads/2026-09-06_drive_documento-jezug-parte-1.docx` | Documento acusatorio, no todas sus inferencias están probadas. |
| EXT-B02 | Documento Los Brígidos, parte 2 | `docs/drive-downloads/2026-09-06_drive_documento-jezug-parte-2.docx` | Documento acusatorio, no todas sus inferencias están probadas. |
| SEC-V01 | Imágenes catalogadas | `evidence/manifest.json` — campo `files` | 105 piezas auditadas en septiembre; **no hay nueva auditoría visual**. |
| SEC-C01 | Matriz argumental | `data/fase3_claim_matrix.json` | Síntesis revisable, actualmente C01–C11. |
| SEC-T01 | Inventario de videos | `transcripts/manifest.json` | 6 entradas; varios originales/timestamps incompletos. |

Todos los archivos con datos personales se mantienen privados. Los SHA de blob Git y tamaños de las cinco exportaciones textuales están en `evidence/manifest.json` bajo `textual_exports`.

## 3. Casos — nunca fusionar sujetos ni episodios por asociación

- **Danel**: amenazas, publicación de IP atribuida, declaración de Grindr; consultar `docs/fase4_casos_2022_2023.md`.
- **Guillermo/The Loud Channel**: conflicto de 2022, Kirmo y alegación de implicación de tres menores; diferenciar iniciativa, sugerencias y supuesta dirección.
- **Ruitzo/Ray/Wildo**: episodios y destinatarios propios; la propuesta del 03-01-2023 dirigida a Ruitzo y su pareja no era una instrucción contra Guillermo.
- **Leniloq/Menita**: distinguir invitación/acceso a recursos, usos posteriores, relato de muerte y correcciones.
- **Fan de Lucky**: no atribuir control de cuenta sin cadena verificable.
- **2026 / Los Brígidos / búsquedas y reclamaciones**: separar de responsabilidades históricas, índice en `acoso/`.

## 4. Itinerario hasta el public-html

1. Cerrar matriz caso por caso con ID de mensaje, autor, fecha, enlace interno y texto redactado/anónimo.
2. Completar verificación de fuentes ausentes y marcar hallazgos inverificables de manera explícita.
3. Revisar privacidad y seguridad; nadie debe acceder desde la web a los originales privados.
4. Aprobar personalmente la parte de disculpas/responsabilidad.
5. **Solo entonces** construir o sustituir `public-html/`, que ya contiene elementos preparatorios no modificados por esta fase.

## 5. Estado técnico de preservación

El corpus conserva fuentes primarias y derivados en distintas carpetas; se evitan cambios de nombre o traslados destructivos para no romper referencias. Los cinco exportados textuales añadidos en octubre están preservados. Ninguna revisión de este hito ha abierto multimedia de «el pepe».
