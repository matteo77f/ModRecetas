# ModRecetas - MVP en Azure

## Descripción
ModRecetas es un MVP para transformar recetas hacia versiones más saludables usando IA. El proyecto está alojado en Azure DevOps y el desarrollo principal se realiza en:

- Backend: Python
- Frontend: React
- Repositorio: Azure Repos `https://dev.azure.com/fmateo77/ModRecetas/_git/ModRecetas`
- Gestión de trabajo: Azure Boards

## Arquitectura del MVP

### Backend Python
- API REST en Python.
- Endpoint principal: `/api/recommend`.
- Entrada: receta original en texto estructurado o libre.
- Salida: recomendaciones de sustitución de ingredientes con cantidades adaptadas y pasos actualizados.
- IA: prompt especializado de chef experto que devuelve JSON uniforme.

### Frontend React
- Interfaz de una sola página.
- Secciones principales:
  - Entrada de receta: texto, archivo o imagen.
  - Resultado de IA: receta original vs receta modificada.
  - Copiar / descargar resultado.
- Diseño con colores verdes ligeros para transmitir una experiencia saludable.

### Diseño y UX
- Paleta: verdes suaves, blanco y grises claros.
- Enfoque: claridad, salud y legibilidad.
- Elementos clave:
  - Botones verdes suaves para acciones principales.
  - Tarjetas claras para recetas original y modificada.
  - Indicadores de carga y mensajes de error.

## Estado actual
- Backlog MVP documentado en `BACKLOG.md`.
- Azure Boards: tareas creadas para implementación del backend, IA, frontend, integración y validación.

## Próximos pasos
1. Desarrollar la API Python para generar recomendaciones de ingredientes.
2. Definir y probar el prompt de IA con salida JSON estructurada.
3. Construir la interfaz React con diseño verde saludable.
4. Conectar el frontend con la API y manejar errores.
5. Añadir validación de entrada y retroalimentación de usuario.
