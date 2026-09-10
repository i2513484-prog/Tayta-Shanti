from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
import os
from werkzeug.utils import secure_filename
from app.models import Producto, Venta, Usuario
from app.models import Venta, DetalleVenta

UPLOAD_FOLDER = "app/static/img"

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/ventas')
def ventas():

    page = request.args.get(

        'page',

        1,

        type=int

    )

    fecha = request.args.get('fecha')

    query = Venta.query

    # FILTRO FECHA
    if fecha:

        query = query.filter(

            db.func.date(Venta.fecha) == fecha

        )

    # PAGINACION
    ventas = query.order_by(

        Venta.fecha.desc()

    ).paginate(

        page=page,

        per_page=10

    )

    data = []

    for venta in ventas.items:

        detalles = DetalleVenta.query.filter_by(

            venta_id=venta.id

        ).all()

        data.append({

            "venta": venta,

            "detalles": detalles

        })

    return render_template(

        "admin/ventas.html",

        data=data,

        ventas=ventas

    )


# ===== CAMBIAR ESTADO =====

@admin_bp.route(
    '/ventas/estado/<int:id>',
    methods=['POST']
)

def cambiar_estado(id):

    venta = Venta.query.get_or_404(id)

    nuevo_estado = request.form.get(
        'estado'
    )

    venta.estado = nuevo_estado

    db.session.commit()

    flash(
        "Estado actualizado"
    )

    return redirect(
        url_for('admin.dashboard')
    )

@admin_bp.route('/ventas/eliminar/<int:id>')
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)

    # borrar detalles primero
    DetalleVenta.query.filter_by(venta_id=venta.id).delete()

    # borrar venta
    db.session.delete(venta)
    db.session.commit()

    return redirect(url_for('admin.ventas'))

# DASHBOARD
# DASHBOARD
@admin_bp.route('/')
def dashboard():

    total_productos = Producto.query.count()

    total_ventas = Venta.query.count()

    total_usuarios = Usuario.query.count()

    # ===== INGRESOS TOTALES =====

    ingresos_totales = db.session.query(

        db.func.sum(Venta.total)

    ).scalar() or 0

    # ===== PEDIDOS PENDIENTES =====

    pedidos_pendientes = Venta.query.filter(
        Venta.estado == "Pendiente"
    ).count()

    # ===== ULTIMAS VENTAS =====

    ultimas_ventas = Venta.query.order_by(

        Venta.fecha.desc()

    ).limit(5).all()

    return render_template(

        'admin/dashboard.html',

        total_productos=total_productos,

        total_ventas=total_ventas,

        total_usuarios=total_usuarios,

        ingresos_totales=ingresos_totales,

        pedidos_pendientes=pedidos_pendientes,

        ultimas_ventas=ultimas_ventas

    )

# LISTAR PRODUCTOS
@admin_bp.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('admin/list_productos.html', productos=productos)


# CREAR PRODUCTO
@admin_bp.route('/productos/crear', methods=['GET', 'POST'])
def crear_producto():

    if request.method == 'POST':

        nombre = request.form['nombre']

        precio = float(
            request.form['precio']
        )

        stock = int(
            request.form['stock']
        )

        descripcion = request.form.get(
            'descripcion'
        )

        categoria = request.form.get(
            'categoria'
        )

        imagen = request.files.get(
            'imagen'
        )

        filename = None

        if imagen and imagen.filename != "":

            filename = secure_filename(
                imagen.filename
            )

            ruta = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            imagen.save(ruta)

        nuevo_producto = Producto(

            nombre=nombre,

            precio=precio,

            stock=stock,

            descripcion=descripcion,

            categoria=categoria,

            imagen=filename

        )

        db.session.add(
            nuevo_producto
        )

        db.session.commit()

        return redirect(
            url_for('main.home')
        )

    return render_template(
        'admin/crear_producto.html'
    )

# ELIMINAR PRODUCTO
@admin_bp.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()

    flash("Producto eliminado ❌")
    return redirect(url_for('admin.productos'))

# EDITAR PRODUCTO
@admin_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    producto = Producto.query.get_or_404(id)  # 🔥 aquí se define

    if request.method == 'POST':

        producto.nombre = request.form.get('nombre')
        producto.precio = request.form.get('precio')
        producto.descripcion = request.form.get('descripcion')
        producto.categoria = request.form.get('categoria')
        producto.precio = float(
            request.form['precio']
        )
        producto.stock = int(
            request.form['stock']
        )

        imagen = request.files.get('imagen')

        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            ruta = os.path.join(UPLOAD_FOLDER, filename)
            imagen.save(ruta)

            producto.imagen = filename  # ✔ ahora sí funciona

        db.session.commit()

        return redirect(
    url_for(
        'admin.editar_producto',
        id=producto.id
    )
)
    return render_template(
    'admin/editar_producto.html',
    producto=producto
)
