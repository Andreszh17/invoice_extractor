# Prueba técnica: extracción de datos de facturas con LLM
## Objetivo
Desarrollar una aplicación que permita al usuario cargar una factura de servicios (imagen o PDF),
extraer información clave mediante un modelo de lenguaje (LLM) y visualizar los datos extraídos en una
interfaz.
## Descripción general
El candidato deberá construir una solución funcional end to end que integre un LLM para el
procesamiento inteligente de documentos. La aplicación debe recibir una factura como entrada,
procesarla y presentar la información estructurada al usuario.
Requerimientos funcionales
1. Carga de documento: El usuario debe poder cargar una factura de servicios en formato imegn o
pdf.
2. Extracción de información: Mediante un LLM, la aplicación deera extraer como mínimo los
siguientes campos:
  a. Fecha de emisión de la factura en formato YYYY-MM-dd
  b. Valor total a pagar
3. Visualización: Los datos extraídos deben presentarse de forma clara y estructurada en una
interfaz de usuario en una página web.
Requerimientos técnicos
1. Lenguaje principal: Python
2. Uso de al menos un LLM a traes de una API (OpenAI, Antrhopic u otro)
3. El modelo utilizado debe ser capaz de procesar imágenes o documentos, o en su defecto, el
candidato debe justificar y manejar la extracción de texto previa al llamado al LLM
4. integración de bases de datos (Sql)
## Entregables
1. Código fuente del proyecto en un repositorio (GitHub o similar)
2. Mínimo un ejemplo de factura utilizado para pruebas
Plazo de entrega: Una vez recibido este correo, el candidato tendrá 5 días calendario para desarrollar y enviar la solución.
