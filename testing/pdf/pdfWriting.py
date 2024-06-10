import sqlite3
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registra una fuente TTF
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

# Conecta a la base de datos
conn = sqlite3.connect('mi_base_de_datos.db')
cursor = conn.cursor()

# Consulta los datos
cursor.execute("SELECT campo1, campo2, campo3 FROM mi_tabla")
datos = cursor.fetchall()

# Crea un nuevo PDF con ReportLab
c = canvas.Canvas("nuevo.pdf")

# Establece la fuente y el tamaño
c.setFont('Arial', 11)

# Asume que la tabla comienza en la posición y = 800
y = 800

# Escribe los datos en el PDF
for fila in datos:
    campo1, campo2, campo3 = fila
    c.drawString(50, y, str(campo1))
    c.drawString(200, y, str(campo2))
    c.drawString(350, y, str(campo3))
    y -= 20  # Mueve la posición y para la siguiente fila

# Guarda el PDF
c.save()
