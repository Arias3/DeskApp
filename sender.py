import json
from websocket import create_connection

ws = create_connection("ws://localhost:5000")
print("✅ Conectado al servidor WebSocket")

pedido = {
    "numero": "190601",
    "fecha": "2025-06-22",
    "hora": "15:30",
    "items": [
        {"nombre": "Copa Helada", "sabores": "Fresa - Mango", "notas": "Con salsa de chocolate y crema extra"},
        {"nombre": "Banana Split", "sabores": "Fresa - Vainilla - Chocolate", "notas": "Sin nuez, extra crema, para compartir"},
        {"nombre": "Helado Artesanal", "sabores": "Lulo - Mora", "notas": "Presentación en copa pequeña, bien frío"},
        {"nombre": "Brownie con Helado", "sabores": "Chocolate - Coco", "notas": "Brownie caliente, helado encima"},
        {"nombre": "Cono Doble", "sabores": "Fresa - Uva", "notas": "Cono crujiente, doble bola"},
        {"nombre": "Malteada Especial", "sabores": "Oreo - Vainilla", "notas": "Con leche deslactosada y topping de galletas"},
        {"nombre": "Paleta de Frutas", "sabores": "Piña - Maracuyá", "notas": "100% natural, sin azúcar"},
        {"nombre": "Sundae Clásico", "sabores": "Chocolate", "notas": "Con nueces y cereza roja"},
        {"nombre": "Milkshake XXL", "sabores": "Banano - Café", "notas": "Tamaño grande, vaso con tapa"},
        {"nombre": "Smoothie Tropical", "sabores": "Papaya - Mango - Coco", "notas": "Bebida fría, con pajilla ecológica"},
        {"nombre": "Helado Kids", "sabores": "Chicle - Algodón de Azúcar", "notas": "Con confites de colores y barquillo decorativo"},
        {"nombre": "Helado Vegano", "sabores": "Avena - Canela", "notas": "Sin leche, endulzado con panela"},
        {"nombre": "Creppe Helado", "sabores": "Vainilla - Nutella", "notas": "Enrollado, con topping de maní"},
        {"nombre": "Helado Premium", "sabores": "Ron con Pasas", "notas": "Para mayores de edad, servir con cuchara especial"},
        {"nombre": "Cono Mini", "sabores": "Menta - Chocolate", "notas": "Cono pequeño para niños"},
        {"nombre": "Copa Helada", "sabores": "Fresa - Mango", "notas": "Con salsa de chocolate y crema extra"},
        {"nombre": "Banana Split", "sabores": "Fresa - Vainilla - Chocolate", "notas": "Sin nuez, extra crema, para compartir"},
        {"nombre": "Helado Artesanal", "sabores": "Lulo - Mora", "notas": "Presentación en copa pequeña, bien frío"},
        {"nombre": "Brownie con Helado", "sabores": "Chocolate - Coco", "notas": "Brownie caliente, helado encima"},
        {"nombre": "Cono Doble", "sabores": "Fresa - Uva", "notas": "Cono crujiente, doble bola"},
        {"nombre": "Malteada Especial", "sabores": "Oreo - Vainilla", "notas": "Con leche deslactosada y topping de galletas"},
        {"nombre": "Paleta de Frutas", "sabores": "Piña - Maracuyá", "notas": "100% natural, sin azúcar"},
        {"nombre": "Sundae Clásico", "sabores": "Chocolate", "notas": "Con nueces y cereza roja"},
        {"nombre": "Milkshake XXL", "sabores": "Banano - Café", "notas": "Tamaño grande, vaso con tapa"},
        {"nombre": "Smoothie Tropical", "sabores": "Papaya - Mango - Coco", "notas": "Bebida fría, con pajilla ecológica"},
        {"nombre": "Helado Kids", "sabores": "Chicle - Algodón de Azúcar", "notas": "Con confites de colores y barquillo decorativo"},
        {"nombre": "Helado Vegano", "sabores": "Avena - Canela", "notas": "Sin leche, endulzado con panela"},
        {"nombre": "Creppe Helado", "sabores": "Vainilla - Nutella", "notas": "Enrollado, con topping de maní"},
        {"nombre": "Helado Premium", "sabores": "Ron con Pasas", "notas": "Para mayores de edad, servir con cuchara especial"},
        {"nombre": "Cono Mini", "sabores": "Menta - Chocolate", "notas": "Cono pequeño para niños"},
    ]
}


ws.send(json.dumps(pedido))
print("📤 Pedido enviado")
ws.close()
