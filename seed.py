from app import create_app
from app.extensions import db
from app.models import Producto

app = create_app()

with app.app_context():
    datos = [
        {"nombre": "Ron Cartavio", "precio": 25, "imagen": "ron.jpg", "categoria": "ron"},
        {"nombre": "Whisky Blue Label", "precio": 80, "imagen": "whisky.jpg", "categoria": "whisky"},
        {"nombre": "Vodka Premium", "precio": 50, "imagen": "vodka.png", "categoria": "vodka"},
        {"nombre": "Hoja de coca", "precio": 3.00, "imagen": "coca.jpg", "categoria": "otros"},
        {"nombre": "Vino Tinto Reserva", "precio": 45, "imagen": "vino.jpg", "categoria": "vino"},
        {"nombre": "Tequila Gold", "precio": 60, "imagen": "tequila.jpg", "categoria": "tequila"}
    ]

    for d in datos:
        existe = Producto.query.filter_by(nombre=d["nombre"]).first()

        if not existe:
            nuevo = Producto(**d)
            db.session.add(nuevo)

    db.session.commit()
    print("Productos insertados ✅")