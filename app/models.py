from app.extensions import db
from datetime import datetime

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    imagen = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(50), nullable=False)


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    apellidos = db.Column(
        db.String(100)
    )

    usuario = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    correo = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    codigo_verificacion = db.Column(
        db.String(10)
    )

    correo_verificado = db.Column(
        db.Boolean,
        default=False
    )

    rol = db.Column(
        db.String(20),
        default="cliente"
    )


class Venta(db.Model):

    __tablename__ = "venta"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer)

    nombre = db.Column(db.String(100))

    nombre_completo = db.Column(db.String(200))

    telefono = db.Column(db.String(20))

    direccion = db.Column(db.String(200))

    total = db.Column(db.Float)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    tipo_documento = db.Column(db.String(10))

    numero_documento = db.Column(db.String(15))

    # RELACION
    detalles = db.relationship(
        'DetalleVenta',
        backref='venta',
        lazy=True
    )

    estado = db.Column(
    db.String(30),
    default="Pendiente"
    )

class Envio(db.Model):

    __tablename__ = "envios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    venta_id = db.Column(
        db.Integer
    )

    departamento = db.Column(
        db.String(100)
    )

    provincia = db.Column(
        db.String(100)
    )

    distrito = db.Column(
        db.String(100)
    )

    direccion = db.Column(
        db.String(200)
    )

    numero = db.Column(
        db.String(50)
    )

    piso = db.Column(
        db.String(50)
    )

    referencia = db.Column(
        db.String(200)
    )

class DetalleVenta(db.Model):

    __tablename__ = "detalle_venta"

    id = db.Column(db.Integer, primary_key=True)

    venta_id = db.Column(
        db.Integer,
        db.ForeignKey('venta.id')
    )

    producto = db.Column(db.String(100))

    cantidad = db.Column(db.Integer)

    precio = db.Column(db.Float)

class IpBloqueada(db.Model):

    __tablename__ = "ips_bloqueadas"

    id = db.Column(db.Integer, primary_key=True)

    ip = db.Column(db.String(100), nullable=False)

    intentos = db.Column(db.Integer, default=0)

    bloqueado_hasta = db.Column(db.DateTime)

    creado_en = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )