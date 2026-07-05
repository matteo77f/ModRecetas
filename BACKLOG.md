# Backlog MVP - ModRecetas

## Épica 1: Ingesta de Recetas (Carga de Información)

### US1.1: Carga de receta por Texto, Documento o Imagen
**Como** usuario cocinero,

**Quiero** pegar el texto de una receta, subir un archivo o una foto con la receta,

**Para** poder iniciar el proceso de modificación de manera rápida y sin copiar manualmente.

- **Criterios de Aceptación:**
  - **Dado** que el usuario está en la pantalla principal, **cuando** introduce el texto de una receta en el campo de entrada y presiona "Enviar", **entonces** el sistema debe procesar el texto y reconocer los ingredientes y pasos de preparación.
  - **Dado** que el usuario selecciona "Subir Documento" o "Subir Imagen", **cuando** adjunta un archivo válido (.pdf, .docx, .txt, .jpg, .png) de hasta 5MB, **entonces** el sistema debe extraer el texto de la receta correctamente y mostrarlo para confirmación.
  - **Dado** que el usuario envía un texto vacío o adjunta un archivo no válido, **cuando** intenta enviar la receta, **entonces** el sistema debe mostrar un mensaje de error claro indicando que debe proporcionar una receta válida.

### US1.2: Carga de receta mediante Archivo (Doc/PDF)
**Como** usuario cocinero,

**Quiero** subir un archivo de documento (PDF, DOCX o TXT) con una receta,

**Para** no tener que copiar y pegar el texto manualmente.

- **Criterios de Aceptación:**
  - **Dado** que el usuario selecciona la opción de "Subir Documento", **cuando** adjunta un archivo válido (.pdf, .docx, .txt) de hasta 5MB, **entonces** el sistema debe extraer el texto de la receta correctamente.
  - **Dado** que el archivo supera el límite de tamaño o es de un formato no soportado, **cuando** el usuario intenta subirlo, **entonces** el sistema debe mostrar un mensaje de error claro.

### US1.3: Carga de receta mediante Imagen (OCR)
**Como** usuario cocinero,

**Quiero** subir una foto de una receta (de un libro o anotador),

**Para** que la IA la digitalice y pueda trabajar sobre ella.

- **Criterios de Aceptación:**
  - **Dado** que el usuario selecciona la opción de "Subir Imagen", **cuando** adjunta una foto (.jpg, .png), **entonces** el sistema debe procesar la imagen mediante OCR y mostrar el texto extraído al usuario para confirmar que es correcto.
  - **Dado** que la imagen es borrosa o el software no detecta texto, **cuando** finaliza el procesamiento, **entonces** el sistema debe solicitar al usuario que intente con otra foto o que edite el texto manualmente.

## Épica 2: Modificación de Ingredientes con IA

### US2.1: Reemplazo automático de ingredientes por Restricción/Preferencia
**Como** usuario cocinero,

**Quiero** indicarle a la IA qué tipo de modificación quiero (ej. "hacerla sin azúcar", "reemplazar manteca por aceite de coco", "hacerla vegana"),

**Para** obtener una versión adaptada de la receta que respete las proporciones culinarias correctas.

- **Criterios de Aceptación:**
  - **Dado** que el sistema ya procesó la receta original, **cuando** el usuario selecciona o escribe una regla de reemplazo, **entonces** la IA debe devolver la nueva lista de ingredientes con las cantidades recalculadas y adaptar los pasos de preparación si es necesario.
  - **Dado** que el reemplazo altera drásticamente la química de la receta (ej. sacar el huevo en un suflé), **cuando** la IA genera la respuesta, **entonces** debe incluir una breve advertencia o tip sobre el resultado esperado.

### US2.2: Ajuste interactivo por Chat (Refinamiento)
**Como** usuario cocinero,

**Quiero** chatear con la IA sobre la receta modificada (ej. pedirle que use miel en vez de edulcorante tras el primer cambio),

**Para** ajustar los detalles culinarios a mi gusto personal.

- **Criterios de Aceptación:**
  - **Dado** que ya se generó una primera modificación, **cuando** el usuario escribe una contrapropuesta o pregunta en el chat, **entonces** la IA debe responder manteniendo el contexto de la receta actual.

## Épica 3: Visualización y Salida

### US3.1: Visualización Comparativa (Antes vs. Después)
**Como** usuario cocinero,

**Quiero** ver la receta original y la modificada en paralelo o de forma claramente diferenciada,

**Para** entender exactamente qué cambió en las proporciones y procedimientos.

- **Criterios de Aceptación:**
  - **Dado** que la IA completó la modificación, **cuando** se renderiza el resultado, **entonces** la interfaz debe mostrar los ingredientes originales tachados o reemplazados visualmente por los nuevos (o una vista split-screen).

### US3.2: Copiado / Exportación del resultado
**Como** usuario cocinero,

**Quiero** poder copiar la nueva receta al portapapeles o descargarla,

**Para** tenerla a mano al momento de cocinar.

- **Criterios de Aceptación:**
  - **Dado** que el usuario está conforme con la receta final, **cuando** hace clic en "Copiar", **entonces** todo el texto estructurado (Ingredientes y Pasos) se guarda en el portapapeles y se muestra un aviso de "Copiado exitoso".

## Notas técnicas sugeridas para el backlog técnico (MVP)

- **Prompt Engineering:** Definir un system prompt estricto para que la IA actúe como un chef/pastelero experto y devuelva siempre la misma estructura de JSON (Ingredientes, Cantidades, Pasos).
- **UI simple:** Una sola pantalla dividida en: sección de carga/chat (izquierda) y receta resultante (derecha).
- **Carga de archivos:** Soportar PDF, DOCX, TXT y OCR para JPG/PNG.
- **Validación:** Manejar texto vacío, archivos inválidos y OCR con baja calidad.
- **Salida:** Copiar al portapapeles y descargar receta final.
