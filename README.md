# prorrateoClockify
Herramienta cuyo objetivo es prorratear las horas trabajadas por todos los colaboradores dentro de un rango de tiempo establecido. La herramienta genera un reporte en donde cada fila es el registro total de las horas asociadas a un proyecto de cada colaborador.
El reporte se guarda en Documentos. 

Ejemplo de reporte:

![image](https://github.com/pedeltasoftwares/prorrateoClockify/assets/144169025/981ab3ca-8a71-47b8-a19c-4b063fdecf89)

* Columna 1: Identificación del colaborador. Tiene ancho de columna de 15px.
* Columna 2: Identificación interna del proyecto. Tiene ancho de columna de 15px.
* Columna 3: Fecha de inicio de reporte. Tiene ancho de columna de 10px. Formato dd-mm-aaaa
* Columna 4: Fecha fin de reporte. Tiene ancho de columna de 10px. Formato dd-mm-aaaa
* Columna 5: Prorrateo. Tiene ancho de columna de 5px.
* Columna 6: Nombre del prorrateo. Después del guión bajo se añaden las tres primeras letras del mes al que corresponde el prorrateo.

  
**Explicación de herramienta**

La herramienta tienes dos funciones principales:
1. Generar reporte establecido un rango de fecha.
2. Agregar colaborador en llegado caso de que haya ingreso a la empresa. El objetivo de esta funcionalidad es mantener la herramienta actualizada sin necesidad de recurrir a Excel que la alimente.

**CONSIDERACIONES**

Para generar el reporte NO se debe tener instancias abiertas de MS Excel. De lo contrario, creará conflicto.
En llegado caso de olvidar esta consideración, se debe cerrar inmediatamente la herramienta. Posteriormente, se debe abrir el Administrador de Tareas del computador y finalizar la tarea asociada a Microsoft Excel.

Desarrollado por: KA
