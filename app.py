from flask import Flask, request, jsonify, send_file, redirect, url_for, flash, session
from flask import request
from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template
from os import listdir
from werkzeug.utils import secure_filename
from psycopg2 import connect, extras #Conectarse a postgresql
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_paginate import Pagination, get_page_parameter


from config import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1302@localhost/telemedicina'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#key = Fernet.generate_key()
db = SQLAlchemy(app)


host = 'localhost'
port = 5432
dbname = 'telemedicina'
user = 'postgres'
password = '1302'

def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
    return conn


# ******************************************************************
# LOGIN
# ****************************************************************




class User(db.Model):
    __tablename__ = 'usuarios'  # Puedes cambiar 'usuarios' por el nombre que desees
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String, nullable=False)
    rol = db.Column(db.String, nullable=False)

class Carrito(db.Model):
    __tablename__ = 'carrito'
    id_carrito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    name_servicio = db.Column(db.String(80), nullable=False)
    descripcion_servicio = db.Column(db.String, nullable=False)
    precio_servicio = db.Column(db.Float, nullable=False)

class Ordenes(db.Model):
    __tablename__= 'ordenes'
    id_orden = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_orden = db.Column(db.String(80), nullable=False)
    name_servicio = db.Column(db.String(80), nullable=False)
    precio_servicio = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


with app.app_context():
    db.create_all()



@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_session 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Login successful', 'success')
            session['user_id'] = user.id
            session['user_rol']= user.rol
            if user.rol == 'usuario':
                return redirect(url_for('inicio'))
            elif user.rol in ['administrador', 'superusuario']:
                return redirect(url_for('admin_examen'))
            else:
                flash('Rol desconocido', 'danger')

        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        rol = 'usuario'
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, lastname=lastname, password=hashed_password, email=email, rol=rol)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        username = request.form['username']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        rol = 'administrador'
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, lastname=lastname, password=hashed_password, email=email, rol=rol)
        db.session.add(new_user)
        db.session.commit()
        flash(f'¡Administrador {username} registrado correctamente!', 'success')
        return redirect(url_for('admin_admins'))
    return render_template('gestion_admin.html')


@app.route('/get_username/<int:user_id>')
def get_username(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    else:
        return 'Usuario no encontrado'
    
@app.route('/logout')
def logout():
    global user_session 
    # Elimina la información de la sesión
    session.pop('user_id', None)
    user_session = 2
    print("Sesion:", user_session)
    # Redirige a la página de inicio d  e sesión (o a donde desees)
    return redirect(url_for('inicio'))


# ******************************************************************
# Rutas
# *****************************************************************


@app.route('/inicio')
def inicio():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/medicos')
def medicos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute(
        "SELECT COUNT(*) AS total FROM especialidades ")
    count = cur.fetchone()['total']

    page_num = request.args.get('page', 1, type=int)
    per_page = 8

    # Calcular el índice del primer registro y limitar la consulta a un rango de registros
    start_index = (page_num - 1) * per_page + 1

    querySQL = (
        f"SELECT id_especialidad, nombre_especialidad, descripcion_especialidad, precio_especialidad "
        f"FROM especialidades WHERE id_especialidad >= 1 "
        f"ORDER BY id_especialidad DESC LIMIT {per_page} OFFSET {start_index}"
    )
    cur.execute(querySQL)
    especialidades = cur.fetchall()

    # Calcular el índice del último registro
    end_index = min(start_index + per_page, count)
    # end_index = start_index + per_page - 1
    if end_index > count:
        end_index = count

    # Crear objeto paginable
    pagination = Pagination(page=page_num, total=count, per_page=per_page,
                            display_msg=f"Mostrando registros {start_index} - {end_index} de un total de <strong>({count})</strong>")
    conn.commit()



    return render_template('medicos.html', especialidades=especialidades, pagination=pagination)


@app.route('/medicamentos')
def medicamentos():
   
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute(
        "SELECT COUNT(*) AS total FROM medicamentos ")
    count = cur.fetchone()['total']

    page_num = request.args.get('page', 1, type=int)
    per_page = 8

    # Calcular el índice del primer registro y limitar la consulta a un rango de registros
    start_index = (page_num - 1) * per_page + 1

    querySQL = (
        f"SELECT id_medicamento, nombre_medicamento, descripcion_medicamento, precio_medicamento "
        f"FROM medicamentos WHERE id_medicamento >= 1 "
        f"ORDER BY id_medicamento DESC LIMIT {per_page} OFFSET {start_index}"
    )
    cur.execute(querySQL)
    medicamentos = cur.fetchall()

    # Calcular el índice del último registro
    end_index = min(start_index + per_page, count)
    # end_index = start_index + per_page - 1
    if end_index > count:
        end_index = count

    # Crear objeto paginable
    pagination = Pagination(page=page_num, total=count, per_page=per_page,
                            display_msg=f"Mostrando registros {start_index} - {end_index} de un total de <strong>({count})</strong>")
    conn.commit()



    return render_template('medicamentos.html', medicamentos=medicamentos, pagination=pagination)

@app.route('/examenes')
def examenes():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute(
        "SELECT COUNT(*) AS total FROM examenes ")
    count = cur.fetchone()['total']

    page_num = request.args.get('page', 1, type=int)
    per_page = 8

    # Calcular el índice del primer registro y limitar la consulta a un rango de registros
    start_index = (page_num - 1) * per_page + 1

    querySQL = (
        f"SELECT id_examen, name_examen, description_examen, precio_examen "
        f"FROM examenes WHERE id_examen >= 1 "
        f"ORDER BY id_examen DESC LIMIT {per_page} OFFSET {start_index}"
    )
    cur.execute(querySQL)
    examenes = cur.fetchall()

    # Calcular el índice del último registro
    end_index = min(start_index + per_page, count)
    # end_index = start_index + per_page - 1
    if end_index > count:
        end_index = count

    # Crear objeto paginable
    pagination = Pagination(page=page_num, total=count, per_page=per_page,
                            display_msg=f"Mostrando registros {start_index} - {end_index} de un total de <strong>({count})</strong>")
    conn.commit()



    return render_template('examenes.html', examenes=examenes, pagination=pagination)

@app.route('/vacunas')
def vacunas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute(
        "SELECT COUNT(*) AS total FROM vacunas ")
    count = cur.fetchone()['total']

    page_num = request.args.get('page', 1, type=int)
    per_page = 8

    # Calcular el índice del primer registro y limitar la consulta a un rango de registros
    start_index = (page_num - 1) * per_page + 1

    querySQL = (
        f"SELECT id_vacuna, nombre_vacuna, descripcion_vacuna, precio_vacuna "
        f"FROM vacunas WHERE id_vacuna >= 1 "
        f"ORDER BY id_vacuna DESC LIMIT {per_page} OFFSET {start_index}"
    )
    cur.execute(querySQL)
    vacunas = cur.fetchall()

    # Calcular el índice del último registro
    end_index = min(start_index + per_page, count)
    # end_index = start_index + per_page - 1
    if end_index > count:
        end_index = count

    # Crear objeto paginable
    pagination = Pagination(page=page_num, total=count, per_page=per_page,
                            display_msg=f"Mostrando registros {start_index} - {end_index} de un total de <strong>({count})</strong>")
    conn.commit()



    return render_template('vacunas.html', vacunas=vacunas, pagination=pagination)

@app.route('/admin/examenes')
def admin_examen():
    return render_template('admin_examenes.html')

@app.route('/admin/vacunas')
def admin_vacuna():
    return render_template('admin_vacunas.html')

@app.route('/admin/medicamentos')
def admin_medicamento():
    return render_template('admin_medicamentos.html')

@app.route('/admin/especialidades')
def admin_especialidad():
    return render_template('admin_especialidades.html')


@app.route('/admin/ordenes')
def admin_orden():
    return render_template('ordenes.html')

@app.route('/admin/admins')
def admin_admins():
    return render_template('gestion_admin.html')

@app.route('/admin/users')
def admin_users():
    return render_template('admin_user.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/loginPage')
def login_page():
    return render_template('login.html')

@app.route('/registerPage')
def register_page():
    return render_template('register.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito_page.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return redirect(url_for('inicio'))





# ******************************************************************
# Rutas RESTApi
# *****************************************************************


# ******EXAMENES*********
@app.get('/api/examenes')
def get_examenes():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM  examenes')
    examenes =cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(examenes)

@app.post('/api/examenes')
def create_examenes():
    new_examen = request.get_json()
    id_examen = new_examen['id_examen']
    name_examen = new_examen['name_examen']
    description_examen = new_examen['description_examen']
    precio_examen = new_examen['precio_examen']

    #password = Fernet(key).encrypt(bytes(new_examen['password'], 'utf8'))

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO examenes (id_examen, name_examen, description_examen, precio_examen) VALUES (%s, %s, %s, %s) RETURNING *',
                (id_examen, name_examen, description_examen, precio_examen))
    new_examen = cur.fetchone()
    print(new_examen)
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_examen)

@app.delete('/api/examenes/<id_examen>')
def delete_examenes(id_examen):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)


    cur.execute('DELETE FROM examenes WHERE id_examen = %s RETURNING *', (id_examen, ))
    examen = cur.fetchone()

    print(examen)

    conn.commit()

    conn.close()
    cur.close()


    if examen is None:
        return jsonify({'message': 'Examen not found'}), 404
    
    return jsonify(examen)

@app.put('/api/examenes/<id_examen>')
def update_examenes(id_examen):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_examen = request.get_json()
    name_examen =new_examen['name_examen']
    description_examen = new_examen['description_examen']
    precio_examen = new_examen['precio_examen']

    cur.execute(
        'UPDATE examenes SET name_examen = %s, description_examen = %s, precio_examen = %s WHERE id_examen = %s RETURNING *',
        (name_examen, description_examen, precio_examen, id_examen))
    
    updated_examen = cur.fetchone()
    cur.close()
    conn.commit()
    
    conn.close()
    

    if updated_examen is None:
        return jsonify({'message': 'Examen not found'}), 404

    return jsonify(updated_examen)

@app.get('/api/examenes/<id_examen>')
def get_examen(id_examen):
    
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM examenes WHERE id_examen= %s', (id_examen,))
    examen= cur.fetchone()

    if examen is None:
        return jsonify({'message':'Exam not found'}), 404

    return jsonify(examen)


# *********MEDICAMENTOS********
@app.route('/api/medicamentos')
def get_medicamentos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM medicamentos')
    medicamentos = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(medicamentos)


@app.post('/api/medicamentos')
def create_medicamentos():
    new_medicamento = request.get_json()
    id_medicamento = new_medicamento['id_medicamento']
    nombre_medicamento = new_medicamento['nombre_medicamento']
    descripcion_medicamento = new_medicamento['descripcion_medicamento']
    precio_medicamento = new_medicamento['precio_medicamento']


    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO medicamentos(id_medicamento, nombre_medicamento, descripcion_medicamento,precio_medicamento) VALUES(%s,%s,%s,%s) RETURNING *',
                (id_medicamento, nombre_medicamento, descripcion_medicamento, precio_medicamento))
    new_medicamento = cur.fetchone()
    print(new_medicamento)
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_medicamento)

@app.delete('/api/medicamentos/<id_medicamento>')
def delete_medicamento(id_medicamento):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('DELETE FROM medicamentos WHERE id_medicamento = %s RETURNING *', (id_medicamento, ))
    medicamento = cur.fetchone()
    print(medicamento)

    conn.commit()

    conn.close()
    cur.close()

    if medicamento is None:
        return jsonify({'message':'Medicamento not found'}), 404
    
    return jsonify(medicamento)

@app.put('/api/medicamentos/<id_medicamento>')
def update_medicamento(id_medicamento):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_medicamento = request.get_json()
    nombre_medicamento =new_medicamento['nombre_medicamento']
    descripcion_medicamento = new_medicamento['descripcion_medicamento']
    precio_medicamento = new_medicamento['precio_medicamento']

    cur.execute(
        'UPDATE medicamentos SET nombre_medicamento= %s, descripcion_medicamento= %s, precio_medicamento= %s WHERE id_medicamento = %s RETURNING *',
        (nombre_medicamento,descripcion_medicamento,precio_medicamento,id_medicamento))

    updated_medicamento=cur.fetchone()

    cur.close()
    conn.commit()
    conn.close()

    if updated_medicamento is None:
        return jsonify({'message': 'Medicamento not found'}),404
    
    return jsonify(updated_medicamento)

@app.get('/api/medicamentos/<id_medicamento>')
def get_medicamento(id_medicamento):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM medicamentos WHERE id_medicamento= %s', (id_medicamento, ))
    medicamento = cur.fetchone()

    if medicamento is None:
        return jsonify({'message': 'Medicamento not found'}), 404
    
    return jsonify(medicamento)


# **********VACUNAS********

@app.get('/api/vacunas')
def get_vacunas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM vacunas')
    vacunas = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(vacunas)
                
@app.post('/api/vacunas')
def create_vacunas():
    new_vacuna = request.get_json()
    id_vacuna = new_vacuna['id_vacuna']
    nombre_vacuna = new_vacuna['nombre_vacuna']
    descripcion_vacuna = new_vacuna['descripcion_vacuna']
    precio_vacuna = new_vacuna['precio_vacuna']


    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO vacunas (id_vacuna, nombre_vacuna, descripcion_vacuna, precio_vacuna) VALUES(%s, %s, %s,%s) RETURNING *',
                (id_vacuna, nombre_vacuna, descripcion_vacuna, precio_vacuna))
    
    new_vacuna = cur.fetchone()
    print(new_vacuna)
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_vacuna)

@app.delete('/api/vacunas/<id_vacuna>')
def delete_vacunas(id_vacuna):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('DELETE FROM vacunas WHERE id_vacuna = %s RETURNING *', (id_vacuna, ))
    vacuna = cur.fetchone()

    print(vacuna)

    conn.commit()
    conn.close()
    cur.close()

    if vacuna is None:
        return jsonify({'message': 'Vacuna not found'}), 404
    
    return jsonify(vacuna)

@app.put('/api/vacunas/<id_vacuna>')
def update_vacuna(id_vacuna):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_vacuna = request.get_json()
    nombre_vacuna = new_vacuna['nombre_vacuna']
    descripcion_vacuna = new_vacuna['descripcion_vacuna']
    precio_vacuna = new_vacuna['precio_vacuna']

    cur.execute('UPDATE vacunas SET nombre_vacuna =%s, descripcion_vacuna =%s, precio_vacuna =%s WHERE id_vacuna = %s RETURNING *',
                (nombre_vacuna, descripcion_vacuna, precio_vacuna, id_vacuna))
    
    updated_examen = cur.fetchone()
    cur.close()
    conn.commit()

    conn.close()

    if updated_examen is None:
        return jsonify({'message': 'Vacuna not found'}),404
    
    return jsonify(updated_examen)

@app.get('/api/vacunas/<id_vacuna>')
def get_vacuna(id_vacuna):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM vacunas WHERE id_vacuna =%s', (id_vacuna, ))
    vacuna = cur.fetchone()

    if vacuna is None:
        return jsonify({'message': 'Vacunas not found'}),404
    
    return jsonify(vacuna)


# ********ESPECIALIDADES******

@app.get('/api/especialidades')
def get_especialidades():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM especialidades')
    especialidades = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(especialidades)

@app.post('/api/especialidades')
def create_especialidades():
    new_especialidad = request.get_json()
    id_especialidad = new_especialidad['id_especialidad']
    nombre_especialidad = new_especialidad['nombre_especialidad']
    descripcion_especialidad = new_especialidad['descripcion_especialidad']
    precio_especialidad = new_especialidad['precio_especialidad']


    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO especialidades (id_especialidad,nombre_especialidad, descripcion_especialidad, precio_especialidad) VALUES (%s, %s, %s, %s) RETURNING *',
                (id_especialidad, nombre_especialidad, descripcion_especialidad, precio_especialidad))
    
    new_especialidad = cur.fetchone()
    print(new_especialidad)
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_especialidad)

@app.delete('/api/especialidades/<id_especialidad>')
def delete_especialidad(id_especialidad):

    conn= get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('DELETE FROM especialidades WHERE id_especialidad =%s RETURNING *' (id_especialidad))
    especialidad = cur.fetchone()

    print(especialidad)

    conn.commit()
    conn.close()
    cur.close()

    if especialidad is None:
        return jsonify({'message' : 'Especialidad not found'}),404
    
    return jsonify(especialidad)

@app.put('/api/especialidades/<id_especialidad>')
def update_especialidad(id_especialidad):
    
    conn=get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_especialidad = request.get_json()
    nombre_especialidad = new_especialidad['nombre_especialidad']
    descripcion_especialidad = new_especialidad['descripcion_especialidad']
    precio_especialidad = new_especialidad['precio_especialidad']

    cur.execute('UPDATE especialidad SET nombre_especialidad = %s, descripcion_especialidad = %s, precio_especialidad = %s WHERE id_especialidad = %s RETURNING*',
                (nombre_especialidad, descripcion_especialidad, precio_especialidad, id_especialidad))
    
    updated_especialidad = cur.fetchone()
    cur.close()
    conn.commit()

    conn.close()

    if updated_especialidad is None: 
        return jsonify({'message': 'Especialidad not found'}), 404
    
    return jsonify(update_especialidad)

@app.get('/api/especialidades/<id_especialidad>')
def get_especialidad(id_especialidad):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM especialidades WHERE id_especialidad= %s', (id_especialidad, ))
    especialidad = cur.fetchone()

    if especialidad is None:
        return jsonify({'message': 'Especialidad not found'}), 404
    
    return jsonify(especialidad)

# ********USUARIOS******

@app.get('/api/usuarios')
def get_usuarios():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM usuarios WHERE rol= %s',('usuario', ))
    usuarios = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(usuarios)


# ********ADMINISTRADORE******

@app.get('/api/administradores')
def get_administradores():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM usuarios WHERE rol= %s',('administrador', ))
    administradores = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(administradores)

#****************************************************
# Ruta para manejar la solicitud de agregar al carrito
#****************************************************
@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    if request.method == 'POST':
        data = request.json
        id_vacuna = data.get('id_vacuna')

        # Obtén información de la vacuna desde la base de datos
        conn = get_connection()
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute('SELECT * FROM vacunas WHERE id_vacuna = %s', (id_vacuna,))
        vacuna = cur.fetchone()
        conn.close()

        if vacuna:
            # Obtén el username del usuario actual (asegúrate de que la sesión esté configurada)
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            username = user.username if user else 'Usuario Desconocido'

            # Crea una nueva entrada en la tabla Carrito
            nueva_entrada_carrito = Carrito(
                username=username,
                name_servicio=vacuna['nombre_vacuna'],
                descripcion_servicio=vacuna['descripcion_vacuna'],
                precio_servicio=vacuna['precio_vacuna']
            )

            # Agrega la nueva entrada al carrito y guarda en la base de datos
            db.session.add(nueva_entrada_carrito)
            db.session.commit()

            return jsonify({'message': 'Vacuna agregada al carrito exitosamente'})
        else:
            return jsonify({'message': 'Vacuna no encontrada'}), 404
        
@app.route('/agregar_al_carrito_medicamentos', methods=['POST'])
def agregar_al_carrito_medicamentos():
    if request.method == 'POST':
        data = request.json
        id_medicamento = data.get('id_medicamento')

        # Obtén información de la vacuna desde la base de datos
        conn = get_connection()
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute('SELECT * FROM medicamentos WHERE id_medicamento = %s', (id_medicamento,))
        medicamento = cur.fetchone()
        conn.close()

        if medicamento:
            # Obtén el username del usuario actual (asegúrate de que la sesión esté configurada)
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            username = user.username if user else 'Usuario Desconocido'

            # Crea una nueva entrada en la tabla Carrito
            nueva_entrada_carrito = Carrito(
                username=username,
                name_servicio=medicamento['nombre_medicamento'],
                descripcion_servicio=medicamento['descripcion_medicamento'],
                precio_servicio=medicamento['precio_medicamento']
            )

            # Agrega la nueva entrada al carrito y guarda en la base de datos
            db.session.add(nueva_entrada_carrito)
            db.session.commit()

            return jsonify({'message': 'Medicamento agregada al carrito exitosamente'})
        else:
            return jsonify({'message': 'Medicamento no encontrada'}), 404
        
@app.route('/agregar_al_carrito_examenes', methods=['POST'])
def agregar_al_carrito_examenes():
    if request.method == 'POST':
        data = request.json
        id_examen = data.get('id_examen')

        # Obtén información de la vacuna desde la base de datos
        conn = get_connection()
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute('SELECT * FROM examenes WHERE id_examen = %s', (id_examen,))
        examen = cur.fetchone()
        print('examen: %s', examen)
        conn.close()

        if examen:
            # Obtén el username del usuario actual (asegúrate de que la sesión esté configurada)
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            username = user.username if user else 'Usuario Desconocido'

            # Crea una nueva entrada en la tabla Carrito
            nueva_entrada_carrito = Carrito(
                username=username,
                name_servicio=examen['name_examen'],
                descripcion_servicio=examen['description_examen'],
                precio_servicio=examen['precio_examen']
            )

            # Agrega la nueva entrada al carrito y guarda en la base de datos
            db.session.add(nueva_entrada_carrito)
            db.session.commit()

            return jsonify({'message': 'Examen agregada al carrito exitosamente'})
        else:
            return jsonify({'message': 'Examen no encontrada'}), 404

@app.route('/agregar_al_carrito_especialidades', methods=['POST'])
def agregar_al_carrito_especialidades():
    if request.method == 'POST':
        data = request.json
        id_especialidad = data.get('id_especialidad')

        # Obtén información de la vacuna desde la base de datos
        conn = get_connection()
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute('SELECT * FROM especialidades WHERE id_especialidad = %s', (id_especialidad,))
        especialidad = cur.fetchone()
        print('examen: %s', especialidad)
        conn.close()

        if especialidad:
            # Obtén el username del usuario actual (asegúrate de que la sesión esté configurada)
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            username = user.username if user else 'Usuario Desconocido'

            # Crea una nueva entrada en la tabla Carrito
            nueva_entrada_carrito = Carrito(
                username=username,
                name_servicio=especialidad['nombre_especialidad'],
                descripcion_servicio=especialidad['descripcion_especialidad'],
                precio_servicio=especialidad['precio_especialidad']
            )

            # Agrega la nueva entrada al carrito y guarda en la base de datos
            db.session.add(nueva_entrada_carrito)
            db.session.commit()

            return jsonify({'message': 'Examen agregada al carrito exitosamente'})
        else:
            return jsonify({'message': 'Examen no encontrada'}), 404

@app.get('/api/carrito')
def get_carrito():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM carrito')
    carrito = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(carrito)


@app.delete('/api/carrito/<id_carrito>')
def delete_carrito(id_carrito):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('DELETE FROM carrito WHERE id_carrito = %s RETURNING *', (id_carrito, ))
    carrito = cur.fetchone()

    print(carrito)

    conn.commit()
    conn.close()
    cur.close()

    return jsonify(carrito)

@app.route('/comprar', methods=['POST'])
def comprar():
     if request.method == 'POST':
        data = request.json
        id_carrito = data.get('id_carrito')

        conn = get_connection()
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute('SELECT * FROM carrito WHERE id_carrito = %s', (id_carrito,))
        carrito = cur.fetchone()

        if carrito:
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            username = user.username if user else 'Usuario Desconocido'

            nueva_orden = Ordenes(
                username_orden=username,
                name_servicio=carrito['name_servicio'],
                precio_servicio=carrito['precio_servicio'],
                fecha_creacion=datetime.utcnow()
            )

            db.session.add(nueva_orden)
            db.session.commit()

            cur.execute('DELETE FROM carrito WHERE id_carrito = %s', (id_carrito,))
            conn.commit()
            conn.close()

            return jsonify({'message': 'Orden agregada al carrito exitosamente'})
        else:
            return jsonify({'message': 'Orden no encontrada'}), 404
        

@app.get('/api/ordenes')
def get_comprar():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM ordenes')
    ordenes = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(ordenes)

if __name__ == '__main__':

    app.run(port=5000, debug=True)