import pandas as pd
from openpyxl import load_workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black

# Cargar el archivo Excel
excel_file = "asistentes.xlsx"
wb = load_workbook(excel_file)
hoja = wb.active

# Extraer los datos del encabezado
asignatura = hoja["A1"].value
fecha = hoja["A2"].value
semana_docencia = hoja["A3"].value
tema = hoja["A4"].value

# Cargar datos ignorando las primeras 4 filas del encabezado
df = pd.read_excel(excel_file, skiprows=5)  # Cambiado de 4 a 5 para saltar la fila extra

# Renombrar las columnas correctamente
df.columns = ["Nombre", "Apellido", "", "Nombre", "Apellido"]

# Eliminar la columna vacía (posición 2)
df = df.drop(columns=df.columns[2])

# Reemplazar valores NaN con cadena vacía
df = df.fillna("")

# Nombre del archivo de salida
pdf_file = "asistentes.pdf"

# Configurar el PDF
c = canvas.Canvas(pdf_file, pagesize=landscape(letter))
width, height = landscape(letter)

# Dibujar el encabezado
c.setFont("Helvetica-Bold", 14)
c.drawString(30, height - 40, asignatura)
c.drawString(30, height - 60, fecha)
c.drawString(30, height - 80, semana_docencia)
c.drawString(30, height - 100, tema)

# Posicionamiento inicial para la tabla
x_offset = 30
y_offset = height - 140
row_height = 20
col_width = 150

# Escribir encabezados de la tabla en negrita
c.setFont("Helvetica-Bold", 12)
for col_num, column_name in enumerate(df.columns):
    c.drawString(x_offset + col_num * col_width, y_offset, column_name)
    c.rect(x_offset + col_num * col_width, y_offset - row_height, col_width, row_height, stroke=1, fill=0)

# Escribir datos
c.setFont("Helvetica", 10)
y_offset -= row_height

for _, row in df.iterrows():
    if any(row):  # Evita filas vacías
        for col_num, value in enumerate(row):
            c.drawString(x_offset + col_num * col_width, y_offset, str(value))
            c.rect(x_offset + col_num * col_width, y_offset - row_height, col_width, row_height, stroke=1, fill=0)
        y_offset -= row_height

    # Agregar nueva página si se acaba el espacio
    if y_offset < 50:
        c.showPage()
        y_offset = height - 50

# Guardar PDF
c.save()
print(f"Archivo PDF generado: {pdf_file}")
