from jinja2 import Environment, FileSystemLoader
from datetime import datetime

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('comanda.html')

html = template.render(
    numero="0005",
    fecha=datetime.now().strftime('%Y-%m-%d'),
    hora=datetime.now().strftime('%H:%M'),
    items=[
        {"nombre": "Café Americano", "sabores": "Sin azúcar", "notas": "Extra caliente"},
        {"nombre": "Croissant", "sabores": "Con mantequilla", "notas": "Tostado suave"}
    ]
)

with open("rendered_ticket.html", "w", encoding="utf-8") as f:
    f.write(html)
