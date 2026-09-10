from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy import or_
from flask_login import login_user
import os
from werkzeug.utils import secure_filename
from app.models import Producto, Usuario
from app.extensions import db
import requests
import mercadopago
from app.models import Venta, DetalleVenta
import time
from datetime import datetime, timedelta
from app.models import IpBloqueada
from app.models import Envio
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.utils.pdf import generar_pdf
import random
from flask_mail import Message
from app.extensions import mail
from app.extensions import csrf, limiter


ips_baneadas = {}
tiempo_ban = 60
limite_intentos = 3
intentos_ip = {}

def obtener_ip():

    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]

    return request.remote_addr

def obtener_ip():

    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr

    return ip.lower()

def registrar_intento_ip(ip):

    ahora = time.time()

    if ip not in ips_baneadas:
        ips_baneadas[ip] = []

    ips_baneadas[ip].append(ahora)

    # limpiar intentos viejos
    ips_baneadas[ip] = [
        t for t in ips_baneadas[ip]
        if ahora - t < tiempo_ban
    ]

    baneada = len(ips_baneadas[ip]) >= limite_intentos

    intentos_restantes = max(
        0,
        limite_intentos - len(ips_baneadas[ip])
    )

    return baneada, intentos_restantes

main_bp = Blueprint('main', __name__)

@main_bp.before_app_request
def verificar_baneo():

    ip = obtener_ip()

    if ip in ips_baneadas and len(ips_baneadas[ip]) >= limite_intentos:
        return "🚫 IP bloqueada temporalmente", 403
UPLOAD_FOLDER = "app/static/img"

sdk = mercadopago.SDK("TEST-6366574855887010-041601-e22298b2235c7932282b3b9418c6449b-3339472073")

main_bp = Blueprint('main', __name__)

@main_bp.route(
    '/verificar_correo',
    methods=['GET', 'POST']
)

def verificar_correo():

    correo = request.args.get('correo')

    usuario = Usuario.query.filter_by(
        correo=correo
    ).first()

    # ===== SI NO EXISTE =====

    if not usuario:

        flash(
            "Usuario no encontrado"
        )

        return redirect(
            url_for('main.login')
        )

    if request.method == 'POST':

        codigo = request.form.get('codigo')

        # ===== CODIGO CORRECTO =====

        if usuario.codigo_verificacion == codigo:

            usuario.correo_verificado = True

            usuario.codigo_verificacion = None

            db.session.commit()

            # ===== CORREO BIENVENIDA =====

            msg_bienvenida = Message(

                "Bienvenido a LICORERÍA TAYTA SHANTI",

                sender="johnsuasnabar23@gmail.com",

                recipients=[usuario.correo]

            )

            msg_bienvenida.body = f"""

Hola {usuario.nombre}

Tu cuenta fue verificada correctamente.

Bienvenido a LICORERÍA TAYTA SHANTI 🍃

Ahora ya puedes iniciar sesión y comprar en nuestra tienda.

Gracias por confiar en nosotros.

"""

            mail.send(msg_bienvenida)

            # ===== CREAR SESION =====

            session['usuario_id'] = usuario.id

            session['usuario_nombre'] = usuario.nombre

            flash(
                f"✅ Código verificado, bienvenido {usuario.nombre}"
            )

            return redirect(
                url_for('main.home')
            )

        else:

            flash(
                "❌ Código incorrecto"
            )

    return render_template(
        'verificar.html'
    )

@main_bp.before_request
def verificar_baneo():
        ip = obtener_ip()
        if ip in intentos_ip and len(intentos_ip[ip]) > limite_intentos:
            return "Tu IP está temporalmente bloqueada", 403

@main_bp.route("/api/dni", methods=["POST"])
@csrf.exempt
def api_dni():
    data = request.get_json(silent=True) or {}
    dni = data.get("dni")

    if not dni or len(dni) != 8:
        return jsonify({"error": "DNI inválido"}), 400

    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImkyNTEzNDg0QGNvbnRpbmVudGFsLmVkdS5wZSJ9.XCSuqw2XahjZCfagIcEbGJjoNOh2Eww9escjyK4lygw"

    url = f"https://dniruc.apisperu.com/api/v1/dni/{dni}?token={token}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        resultado = response.json()

    except requests.RequestException:
        return jsonify({"error": "No se pudo consultar el DNI"}), 502

    except ValueError:
        return jsonify({"error": "Respuesta inválida de la API DNI"}), 502

    return jsonify(resultado)


@main_bp.route("/api/ruc", methods=["POST"])
@csrf.exempt
def api_ruc():
    data = request.get_json(silent=True) or {}
    ruc = data.get("ruc")

    if not ruc or len(ruc) != 11:
        return jsonify({"error": "RUC inválido"}), 400

    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImkyNTEzNDg0QGNvbnRpbmVudGFsLmVkdS5wZSJ9.XCSuqw2XahjZCfagIcEbGJjoNOh2Eww9escjyK4lygw"

    url = f"https://dniruc.apisperu.com/api/v1/ruc/{ruc}?token={token}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        resultado = response.json()

    except requests.RequestException:
        return jsonify({"error": "No se pudo consultar el RUC"}), 502

    except ValueError:
        return jsonify({"error": "Respuesta inválida de la API RUC"}), 502

    return jsonify(resultado)

@main_bp.route("/")
def home():
    productos = Producto.query.all()
    return render_template("index.html", productos=productos, categoria_actual=None)

@main_bp.route("/categoria/<string:categoria>")
def categoria(categoria):
    productos = Producto.query.filter_by(categoria=categoria).all()
    return render_template("index.html", productos=productos, categoria_actual=categoria)

@main_bp.route("/producto/<int:id>")
def producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template("producto.html", producto=producto)

@main_bp.route("/agregar_carrito/<int:id>")
def agregar_carrito(id):
    producto = Producto.query.get_or_404(id)

    if 'carrito' not in session:
        session['carrito'] = {}

    carrito = session['carrito']
    id_str = str(producto.id)

    if id_str in carrito:
        carrito[id_str] += 1
    else:
        carrito[id_str] = 1

    session['carrito'] = carrito
    session.modified = True

    flash(f'¡{producto.nombre} añadido al carrito!')
    return redirect(request.referrer or url_for('main.home'))

@main_bp.route('/envios', methods=['GET', 'POST'])
def envios():

    carrito = session.get('carrito', {})

    productos = []

    total = 0

    for id_producto, cantidad in carrito.items():

        producto = Producto.query.get(
            int(id_producto)
        )

        subtotal = producto.precio * cantidad

        total += subtotal

        productos.append({

            'producto': producto,

            'cantidad': cantidad,

            'subtotal': subtotal

        })

    if request.method == 'POST':

        session['envio'] = {

            'departamento':
            request.form.get('departamento'),

            'provincia':
            request.form.get('provincia'),

            'distrito':
            request.form.get('distrito'),

            'direccion':
            request.form.get('direccion'),

            'numero':
            request.form.get('numero'),

            'piso':
            request.form.get('piso'),

            'referencia':
            request.form.get('referencia')

        }

        return redirect(
            url_for('main.checkout')
        )

    return render_template(

        'envios.html',

        productos=productos,

        total=total
    )

@main_bp.route('/carrito')
def carrito():
    carrito_session = session.get('carrito', {})
    productos_carrito = []
    total = 0

    for id_str, cantidad in carrito_session.items():
        producto = Producto.query.get(int(id_str))

        if producto:
            subtotal = producto.precio * cantidad
            total += subtotal

            productos_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })

    return render_template('carrito.html', productos=productos_carrito, total=total)

@main_bp.route('/sumar_carrito/<int:id>')
def sumar_carrito(id):
    carrito = session.get('carrito', {})
    id_str = str(id)

    if id_str in carrito:
        carrito[id_str] += 1
        session['carrito'] = carrito
        session.modified = True

    return redirect(url_for('main.carrito'))

@main_bp.route('/restar_carrito/<int:id>')
def restar_carrito(id):
    carrito = session.get('carrito', {})
    id_str = str(id)

    if id_str in carrito:
        carrito[id_str] -= 1

        if carrito[id_str] <= 0:
            del carrito[id_str]

        session['carrito'] = carrito
        session.modified = True

    return redirect(url_for('main.carrito'))

@main_bp.route('/eliminar_carrito/<int:id>')
def eliminar_carrito(id):
    carrito = session.get('carrito', {})
    id_str = str(id)

    if id_str in carrito:
        del carrito[id_str]
        session['carrito'] = carrito
        session.modified = True

    return redirect(url_for('main.carrito'))

@main_bp.route('/vaciar_carrito')
def vaciar_carrito():
    session.pop('carrito', None)
    return redirect(url_for('main.carrito'))

@main_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():

    ip = obtener_ip()

    bloqueo = IpBloqueada.query.filter_by(
        ip=ip
    ).first()

    # ===== VERIFICAR BLOQUEO =====

    if bloqueo and bloqueo.bloqueado_hasta:

        if bloqueo.bloqueado_hasta > datetime.utcnow():

            tiempo_restante = int(

                (
                    bloqueo.bloqueado_hasta - datetime.utcnow()
                ).total_seconds()

            )

            return render_template(

                'login.html',

                error="🚫 IP bloqueada temporalmente",

                tiempo_restante=tiempo_restante,

                intentos_restantes=0

            )

        else:

            bloqueo.intentos = 0

            bloqueo.bloqueado_hasta = None

            db.session.commit()

    # ===== LOGIN =====

    if request.method == 'POST':

        identificador = request.form.get(
            'identificador'
        )

        password = request.form.get(
            'password'
        )

        usuario = Usuario.query.filter(

            or_(

                Usuario.correo == identificador,

                Usuario.usuario == identificador

            )

        ).first()

        # ===== LOGIN CORRECTO =====

        if usuario and check_password_hash(
            usuario.password,
            password
        ):

            # ===== VERIFICAR CORREO =====

            if not usuario.correo_verificado and usuario.rol != "admin":

                # ===== GENERAR CODIGO =====

                codigo = str(

                    random.randint(100000, 999999)

                )

                usuario.codigo_verificacion = codigo

                db.session.commit()

                # ===== ENVIAR GMAIL =====

                msg = Message(

                    "Código de verificación",

                    sender="johnsuasnabar23@gmail.com",

                    recipients=[usuario.correo]

                )

                msg.body = f"""

Hola {usuario.nombre}

Tu código de verificación es:

{codigo}

LICORERÍA TAYTA SHANTI

"""

                mail.send(msg)

                flash(
                    "Te enviamos un código de verificación"
                )

                return redirect(

                    url_for(

                        'main.verificar_correo',

                        correo=usuario.correo

                    )

                )

            # ===== RESETEAR BLOQUEO =====

            if bloqueo:

                bloqueo.intentos = 0

                bloqueo.bloqueado_hasta = None

                db.session.commit()

            # ===== CREAR SESION =====

            session['usuario_id'] = usuario.id

            session['usuario_nombre'] = usuario.nombre

            session['usuario_rol'] = usuario.rol

            return redirect(
                url_for('main.home')
            )

        # ===== LOGIN INCORRECTO =====

        if not bloqueo:

            bloqueo = IpBloqueada(

                ip=ip,

                intentos=1

            )

            db.session.add(bloqueo)

        else:

            bloqueo.intentos += 1

        intentos_restantes = max(

            0,

            5 - bloqueo.intentos

        )

        # ===== BLOQUEAR =====

        if bloqueo.intentos >= 5:

            bloqueo.bloqueado_hasta = (

                datetime.utcnow()

                + timedelta(minutes=1)

            )

        db.session.commit()

        return render_template(

            'login.html',

            error="Datos incorrectos",

            intentos_restantes=intentos_restantes,

            tiempo_restante=60 if bloqueo.intentos >= 5 else 0

        )

    return render_template(

        'login.html',

        tiempo_restante=0,

        intentos_restantes=0

    )


@main_bp.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':

        nombre = request.form.get('nombre')

        apellidos = request.form.get('apellidos')

        correo = request.form.get('correo')

        usuario = request.form.get('usuario')

        password = generate_password_hash(
            request.form.get('password')
        )

        # ===== VALIDAR =====

        existe = Usuario.query.filter_by(
            correo=correo
        ).first()

        if existe:

            return render_template(

                'registro.html',

                error='Ese correo ya está registrado'

            )

        # ===== CREAR USUARIO =====

        nuevo_usuario = Usuario(

            nombre=nombre,

            apellidos=apellidos,

            correo=correo,

            password=password,

            usuario=usuario,

            correo_verificado=False

        )

        db.session.add(nuevo_usuario)

        db.session.commit()

        flash(
            "Cuenta creada correctamente"
        )

        return redirect(
            url_for('main.login')
        )

    return render_template('registro.html')

@main_bp.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nombre', None)
    return redirect(url_for('main.home'))

@main_bp.route('/checkout')
def checkout():
    # Si Mercado Pago devuelve información del pago
    if request.args.get('payment_id') or request.args.get('collection_id'):

        return redirect(
            url_for(
                'main.pago_exitoso',
                **request.args
            )
        )
    # Verificar sesión
    if 'usuario_id' not in session:

        session['next_url'] = url_for('main.checkout')

        return redirect(
            url_for('main.login')
        )
    # Obtener carrito
    carrito_session = session.get('carrito', {})
    productos_carrito = []
    subtotal = 0
    # Si el carrito está vacío
    if not carrito_session:
        return redirect(
            url_for('main.carrito')
        )
    # Recorrer productos
    for id_str, cantidad in carrito_session.items():
        producto = Producto.query.get(int(id_str))
        if producto:
            cantidad = int(cantidad)
            subtotal_producto = (
                float(producto.precio) * cantidad
            )
            subtotal += subtotal_producto
            productos_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal_producto
            })
    # Obtener usuario
    usuario = Usuario.query.get(
        session['usuario_id']
    )
    # ==============================
    # TIPO DE ENTREGA
    # ==============================
    tipo_entrega = session.get(
        'tipo_entrega',
        'recojo'
    )
    # ==============================
    # COSTO DELIVERY
    # ==============================
    if tipo_entrega == 'delivery':
        costo_delivery = float(
            session.get(
                'costo_delivery',
                0
            )
        )
    else:
        costo_delivery = 0
    # ==============================
    # TOTAL FINAL
    # ==============================
    total_final = (
        subtotal + costo_delivery
    )
    # ==============================
    # MOSTRAR CHECKOUT
    # ==============================
    return render_template(
        'checkout.html',
        productos=productos_carrito,
        subtotal=subtotal,
        costo_delivery=costo_delivery,
        total_final=total_final,
        tipo_entrega=tipo_entrega,
        # Se mantiene por compatibilidad
        total=total_final,
        usuario=usuario
    )

@main_bp.route('/procesar_compra', methods=['POST'])
def procesar_compra():

    # ==========================================
    # 1. VERIFICAR USUARIO
    # ==========================================

    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para realizar la compra.")
        return redirect(url_for('main.login'))


    # ==========================================
    # 2. OBTENER DATOS DEL CLIENTE
    # ==========================================

    datos = {
        "nombre": request.form.get('nombre') or request.form.get('nombre_completo'),
        "telefono": request.form.get('telefono'),
        "direccion": request.form.get('direccion')
    }


    # ==========================================
    # 3. VALIDAR CARRITO
    # ==========================================

    carrito_session = session.get('carrito', {})

    if not carrito_session:
        flash("Tu carrito está vacío.")
        return redirect(url_for('main.carrito'))


    # ==========================================
    # 4. RECORRER PRODUCTOS Y CALCULAR TOTAL
    # ==========================================

    productos_carrito = []
    total = 0

    for id_str, cantidad in carrito_session.items():

        producto = Producto.query.get(int(id_str))

        if producto:

            cantidad = int(cantidad)

            subtotal = producto.precio * cantidad

            total += subtotal

            productos_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })


    # ==========================================
    # 5. VALIDAR TOTAL
    # ==========================================

    if not productos_carrito or total <= 0:
        flash("No se encontraron productos válidos en el carrito.")
        return redirect(url_for('main.carrito'))


    # ==========================================
    # 6. VALIDAR DOCUMENTO
    # ==========================================

    tipo_doc = request.form.get("tipo_doc")
    numero_doc = request.form.get("numero_doc", "").strip()


    if tipo_doc == "dni":

        if not numero_doc.isdigit() or len(numero_doc) != 8:

            flash("El DNI debe tener exactamente 8 dígitos.")
            return redirect(url_for('main.checkout'))

        tipo_comprobante = "BOLETA"


    elif tipo_doc == "ruc":

        if not numero_doc.isdigit() or len(numero_doc) != 11:

            flash("El RUC debe tener exactamente 11 dígitos.")
            return redirect(url_for('main.checkout'))

        tipo_comprobante = "FACTURA"


    else:

        flash("Selecciona un tipo de documento válido.")
        return redirect(url_for('main.checkout'))


    # ==========================================
    # 7. CREAR LA VENTA
    # ==========================================

    nueva_venta = Venta(

        nombre=datos["nombre"],

        nombre_completo=request.form.get("nombre_completo") or datos["nombre"],

        telefono=datos["telefono"],

        direccion=datos["direccion"],

        total=total,

        tipo_documento=tipo_doc,

        numero_documento=numero_doc
    )

    db.session.add(nueva_venta)

    db.session.commit()


    # ==========================================
    # 8. GUARDAR ENVÍO
    # ==========================================

    envio = session.get('envio')


    if envio:

        nuevo_envio = Envio(

            venta_id=nueva_venta.id,

            departamento=envio.get('departamento'),

            provincia=envio.get('provincia'),

            distrito=envio.get('distrito'),

            direccion=envio.get('direccion'),

            numero=envio.get('numero'),

            piso=envio.get('piso'),

            referencia=envio.get('referencia')
        )

        db.session.add(nuevo_envio)


    # ==========================================
    # 9. GUARDAR DETALLE DE VENTA
    # ==========================================

    for item in productos_carrito:

        detalle = DetalleVenta(

            venta_id=nueva_venta.id,

            producto=item['producto'].nombre,

            cantidad=item['cantidad'],

            precio=item['producto'].precio
        )

        db.session.add(detalle)


    # Guardar envío y detalles

    db.session.commit()


    # ==========================================
    # 10. GENERAR PDF
    # ==========================================

    pdf_generado = generar_pdf(
        nueva_venta,
        nueva_venta.detalles
    )


    # ==========================================
    # 11. LIMPIAR CARRITO
    # ==========================================

    session.pop('carrito', None)


    # ==========================================
    # 12. MOSTRAR CONFIRMACIÓN
    # ==========================================

    return render_template(

        'confirmacion.html',

        productos=productos_carrito,

        total=total,

        mensaje="✅ Pedido confirmado",

        nombre=datos["nombre"],

        telefono=datos["telefono"],

        direccion=datos["direccion"],

        metodo_pago=request.form.get("metodo_pago"),

        tipo_documento=tipo_doc,

        numero_documento=numero_doc,

        tipo_comprobante=tipo_comprobante,

        pdf=pdf_generado
    )

@main_bp.route('/crear_pago', methods=['POST'])
def crear_pago():

    # ==============================
    # VALIDAR SESIÓN
    # ==============================

    if 'usuario_id' not in session:

        return redirect(
            url_for('main.login')
        )

    # ==============================
    # OBTENER DATOS DEL FORMULARIO
    # ==============================

    tipo_doc = request.form.get(
        'tipo_doc',
        'dni'
    )

    numero_doc = request.form.get(
        'numero_doc',
        ''
    ).strip()

    nombre = request.form.get(
        'nombre',
        ''
    ).strip()

    telefono = request.form.get(
        'telefono',
        ''
    ).strip()

    # ==============================
    # VALIDAR DNI
    # ==============================

    if tipo_doc == 'dni':

        if not (
            numero_doc.isdigit()
            and len(numero_doc) == 8
        ):

            flash(
                'El DNI debe tener exactamente 8 dígitos.'
            )

            return redirect(
                url_for('main.checkout')
            )

    # ==============================
    # VALIDAR RUC
    # ==============================

    elif tipo_doc == 'ruc':

        if not (
            numero_doc.isdigit()
            and len(numero_doc) == 11
        ):

            flash(
                'El RUC debe tener exactamente 11 dígitos.'
            )

            return redirect(
                url_for('main.checkout')
            )

    # ==============================
    # VALIDAR NOMBRE
    # ==============================

    if len(nombre) < 3:

        flash(
            'Ingresa un nombre o razón social válido.'
        )

        return redirect(
            url_for('main.checkout')
        )

    # ==============================
    # OBTENER CARRITO
    # ==============================

    carrito_session = session.get(
        'carrito',
        {}
    )

    if not carrito_session:

        flash(
            'Tu carrito está vacío.'
        )

        return redirect(
            url_for('main.carrito')
        )

    # ==============================
    # GUARDAR DATOS DEL CLIENTE
    # ==============================

    session['datos_cliente'] = {

        'tipo_doc': tipo_doc,

        'numero_doc': numero_doc,

        'nombre': nombre,

        'telefono': telefono,

        'metodo_pago': 'mercado'
    }

    # ==============================
    # CREAR ITEMS MERCADO PAGO
    # ==============================

    items = []

    for id_str, cantidad in carrito_session.items():

        producto = Producto.query.get(
            int(id_str)
        )

        if producto:

            items.append({

                'title': producto.nombre,

                'quantity': int(cantidad),

                'unit_price': float(
                    producto.precio
                ),

                'currency_id': 'PEN'

            })

    # ==============================
    # VALIDAR PRODUCTOS
    # ==============================

    if not items:

        flash(
            'No hay productos válidos para procesar.'
        )

        return redirect(
            url_for('main.carrito')
        )

    # ==============================
    # CREAR PREFERENCIA
    # ==============================

    preference_data = {

        'items': items,

        'back_urls': {

            'success':
                'http://127.0.0.1:5000/pago_exitoso',

            'failure':
                'http://127.0.0.1:5000/pago_exitoso',

            'pending':
                'http://127.0.0.1:5000/pago_exitoso'

        }

    }

    # ==============================
    # ENVIAR A MERCADO PAGO
    # ==============================

    preference_response = (
        sdk.preference().create(
            preference_data
        )
    )

    print(
        'RESPUESTA MERCADO PAGO:',
        preference_response
    )

    # ==============================
    # VALIDAR RESPUESTA
    # ==============================

    if preference_response.get(
        'status'
    ) not in [200, 201]:

        print(
            'ERROR MERCADO PAGO:',
            preference_response
        )

        flash(
            'No se pudo iniciar el pago con Mercado Pago.'
        )

        return redirect(
            url_for('main.checkout')
        )

    preference = preference_response.get(
        'response',
        {}
    )

    init_point = preference.get(
        'init_point'
    )

    if not init_point:

        flash(
            'Mercado Pago no devolvió un enlace de pago.'
        )

        return redirect(
            url_for('main.checkout')
        )

    # ==============================
    # REDIRIGIR A MERCADO PAGO
    # ==============================

    return redirect(init_point)


@main_bp.route('/pago_exitoso')
def pago_exitoso():

    datos = session.get(
        'datos_cliente',
        {}
    )

    carrito_session = session.get(
        'carrito',
        {}
    )

    productos_carrito = []

    total = 0

    for id_str, cantidad in carrito_session.items():

        producto = Producto.query.get(
            int(id_str)
        )

        if producto:

            cantidad = int(cantidad)

            subtotal = (
                float(producto.precio)
                * cantidad
            )

            total += subtotal

            productos_carrito.append({

                'producto': producto,

                'cantidad': cantidad,

                'subtotal': subtotal

            })

    # Vaciar carrito después de mostrar
    # la compra confirmada
    session.pop(
        'carrito',
        None
    )

    return render_template(

        'confirmacion.html',

        productos=productos_carrito,

        total=total,

        mensaje='✅ Compra realizada con éxito',

        nombre=datos.get('nombre'),

        telefono=datos.get('telefono'),

        direccion=datos.get(
            'direccion'
        )
    )

@main_bp.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':

        producto.nombre = request.form.get('nombre')
        producto.precio = request.form.get('precio')
        producto.descripcion = request.form.get('descripcion')
        producto.categoria = request.form.get('categoria')

        # 🔥 MANEJO DE IMAGEN
        imagen = request.files.get('imagen')

        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            ruta = os.path.join(UPLOAD_FOLDER, filename)
            imagen.save(ruta)

            producto.imagen = filename

        db.session.commit()

        return redirect(url_for('main.home'))

    return render_template('admin/editar_producto.html', producto=producto)

    
@main_bp.route("/buscar")
def buscar():
    termino = request.args.get("q", "").strip()

    if termino:
        productos = Producto.query.filter(
            Producto.nombre.ilike(f"%{termino}%")
        ).all()
    else:
        productos = Producto.query.all()

    return render_template(
        "index.html",
        productos=productos,
        categoria_actual=None,
        termino_busqueda=termino
    )

@main_bp.route('/agregar_favorito/<int:id>')
def agregar_favorito(id):
    producto = Producto.query.get_or_404(id)

    if 'favoritos' not in session:
        session['favoritos'] = {}

    favoritos = session['favoritos']
    id_str = str(producto.id)

    if id_str not in favoritos:
        favoritos[id_str] = 1

    session['favoritos'] = favoritos
    session.modified = True

    flash(f'{producto.nombre} añadido a favoritos')
    return redirect(request.referrer or url_for('main.home'))

@main_bp.route('/favoritos')
def favoritos():
    favoritos_session = session.get('favoritos', {})
    productos_favoritos = []

    for id_str in favoritos_session.keys():
        producto = Producto.query.get(int(id_str))

        if producto:
            productos_favoritos.append(producto)

    return render_template(
        'favoritos.html',
        productos=productos_favoritos
    )

@main_bp.route('/mis-pedidos')
def mis_pedidos():

    # VERIFICAR LOGIN
    if 'usuario_id' not in session:

        return redirect(
            url_for('main.login')
        )

    pedidos = Venta.query.filter_by(

        usuario_id=session['usuario_id']

    ).order_by(

        Venta.fecha.desc()

    ).all()

    return render_template(

        'mis_pedidos.html',

        pedidos=pedidos

    )
