# Metodología documental

Estado: interno. Aplicable a Fase 3 y a cualquier futura web/agente.

## 1. Unidad básica: afirmación, no relato

Cada punto debe analizarse como una afirmación concreta. Evitar que una narrativa larga convierta por acumulación una inferencia en hecho.

Para cada afirmación registrar:

- texto o formulación original;
- fuente y fecha;
- evidencia primaria relacionada;
- admisiones relevantes;
- evidencia que contradice o limita;
- impacto documentado, si existe;
- estado epistemológico;
- huecos pendientes.

## 2. Estados epistemológicos

### Hecho observable
Visible directamente en una fuente preservada.

### Admisión
Declaración atribuible a la propia persona sobre su conducta. Una admisión puede probar que esa declaración se realizó; su alcance debe leerse literalmente y en contexto.

### Alegación externa
Afirmación de un tercero. No se convierte en hecho por repetición.

### Inferencia
Conclusión construida a partir de hechos, admisiones o testimonios. Debe identificarse como inferencia y explicar sus premisas.

### No determinado
El corpus disponible no permite resolver el punto con seguridad suficiente.

## 3. Simetría de revisión

El mismo estándar debe aplicarse a inferencias favorables y desfavorables a Jezu.

Ejemplo:

- Si una captura no basta para atribuir a Jezu la autoría total de un plan, decirlo.
- Si una captura tampoco basta para afirmar que Jezu no tuvo influencia previa fuera del fragmento preservado, decirlo también.

No usar “no se puede concluir” como muletilla defensiva. Usarlo únicamente cuando exista una pregunta concreta que la fuente no resuelva.

## 4. Responsabilidad y contexto

Contextualizar no significa minimizar.

Cuando una conducta esté reconocida o bien documentada:

- describirla directamente;
- explicar por qué se considera indebida cuando sea una admisión explícita o una evaluación claramente identificada;
- no convertir matices probatorios en un atenuante general.

En episodios con menores, la iniciativa de la persona menor no elimina la responsabilidad distinta de un adulto. Al mismo tiempo, esa responsabilidad no autoriza a atribuir hechos adicionales sin evidencia.

## 5. Impacto en terceros

No asumir consecuencias psicológicas, sociales, económicas o reputacionales.

Usar tres niveles:

- **impacto observable:** consecuencia directamente documentada;
- **impacto declarado:** consecuencia descrita por la persona afectada;
- **impacto no determinado:** no existe evidencia suficiente para describir consecuencias concretas.

## 6. Separación de expedientes

El registro `acoso/` de 2026 debe mantenerse separado del historial previo.

Que Jezu haya cometido o reconocido conductas anteriores no invalida un reclamo posterior de privacidad/hostigamiento.

Que Jezu haya recibido hostigamiento posterior no reduce su responsabilidad por hechos anteriores.

## 7. Fuentes de parte interesada

Este repositorio es mantenido por Jezu y, por tanto, tiene un interés evidente.

La forma de compensarlo no es declararlo “neutral”, sino:

- preservar evidencia adversa;
- enlazar fuentes acusatorias originales;
- marcar huecos;
- conservar el historial de cambios;
- permitir auditoría externa;
- corregir errores de forma visible.

## 8. Correcciones

Los cambios materiales deben dejar rastro en Git.

Para una corrección factual, el commit debería indicar:

- qué decía la versión anterior;
- qué se corrigió;
- qué fuente motivó la corrección;
- si cambia o no una conclusión anterior.

No hacer force-push ni reescritura destructiva del historial cuando el repositorio se use públicamente como archivo.

## 9. Uso por agentes de IA

Un agente que consulte el archivo deberá:

- citar IDs/rutas de evidencia;
- distinguir las cinco categorías epistemológicas;
- presentar fuentes en conflicto;
- no decidir culpabilidad o inocencia a partir del repo;
- no atribuir intención sin evidencia;
- no usar una ausencia de evidencia como prueba de inexistencia;
- señalar explícitamente cuando una respuesta dependa de material pendiente.
