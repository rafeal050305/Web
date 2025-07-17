from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

import io

app = Flask(__name__)
app.secret_key = '050305'

DATABASE = 'baseDatos.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY,
                nombres VARCHAR(100),
                apellidos VARCHAR(100),
                dni VARCHAR(100),
                password VARCHAR(100),
                correo VARCHAR(100),
                telefono VARCHAR(100),
                genero VARCHAR(100),
                fecha_nacimiento VARCHAR(100)
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS citas_usuario (
                id_cita INTEGER PRIMARY KEY,
                id_usuario INTEGER NOT NULL,
                fecha VARCHAR(100),
                turno VARCHAR(100),
                horario VARCHAR(100),
                FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS resultados_usuario (
                id_resultado INTEGER PRIMARY KEY,
                id_usuario INTEGER NOT NULL,
                fecha_envio VARCHAR(100),
                hora_envio VARCHAR(100),
                glucosa VARCHAR(100),
                colesterol VARCHAR(100),
                rbc VARCHAR(100),
                hemoglobina VARCHAR(100),
                hematocrito VARCHAR(100),
                wbd VARCHAR(100),
                rpl VARCHAR(100),
                grupo_sanguineo VARCHAR(100),
                eco TEXT,
                parasitalogico_simple TEXT,
                parasitalogico_seriado TEXT,
                pr_dengue TEXT,
                pr_helicobacter TEXT,
                link_drive TEXT,
                FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        ''')
        
    
        conn.commit()
        conn.close()

def registrar_usuario():
    conn = sqlite3.connect(DATABASE)

    #*Insertar Registros de Usuarios, NOTA: SOLO HAY UN ADMINISTRADOR
    #* ADMIN:  72931578  PASSWORD: 123
    #* USER:   87654321  PASSWORD: 123
    conn.execute('''
        INSERT INTO usuario (nombres, apellidos, dni, password, correo, telefono, genero, fecha_nacimiento) VALUES
        ('Giovanni', 'Santiago', '12345678', 'pass123', 'giovanni1@mail.com', '999111222', 'Masculino', '12-05-1995'),
        ('Lucía', 'Mendoza', '87654321', '123', 'lucia2@mail.com', '988111222', 'Femenino', '03-10-1992'),
        ('Carlos', 'Ramírez', '13579246', 'carlos789', 'carlos3@mail.com', '977111222', 'Masculino', '22-03-1990'),
        ('Valeria', 'Torres', '24681357', 'valeria123', 'valeria4@mail.com', '966111222', 'Femenino', '19-07-1998'),
        ('Andrés', 'Morales', '19283746', 'andres456', 'andres5@mail.com', '955111222', 'Masculino', '09-01-1993'),
        ('Marta', 'Salazar', '91827364', 'marta789', 'marta6@mail.com', '944111222', 'Femenino', '11-12-1991'),
        ('Pedro', 'García', '10293847', 'pedro123', 'pedro7@mail.com', '933111222', 'Masculino', '30-09-1997'),
        ('Julia', 'Rojas', '56473829', 'julia456', 'julia8@mail.com', '922111222', 'Femenino', '05-06-1994'),
        ('Alonso', 'López', '11122233', 'alonso789', 'alonso9@mail.com', '911111222', 'Masculino', '25-11-1989'),
        ('Rosa', 'Castillo', '44455566', 'rosa123', 'rosa10@mail.com', '900111222', 'Femenino', '15-08-1996'),
        ('Marco', 'Espinoza', '123', '123', 'mk@mail.com', '900111222', 'Masculino', '15-08-1996'),
        ('Mauricio', 'Velazco', '72931578', '123', 'mauricio@gmail.com', '987456963', 'Masculino', '05-02-2000')
    ''')
    
    conn.execute('''
        INSERT INTO citas_usuario (id_usuario, fecha, turno, horario) VALUES

        (1, '01-07-2025', 'Mañana', '08:00'),
        (1, '10-07-2025', 'Tarde', '15:00'),
        (1, '15-07-2025', 'Mañana', '10:30'),
        (1, '20-07-2025', 'Tarde', '14:00'),
        (1, '25-07-2025', 'Mañana', '09:00'),

        (2, '02-07-2025', 'Mañana', '08:00'),
        (2, '11-07-2025', 'Tarde', '16:30'),
        (2, '16-07-2025', 'Mañana', '10:30'),
        (2, '21-07-2025', 'Tarde', '15:00'),
        (2, '26-07-2025', 'Mañana', '09:00'),

        (3, '03-07-2025', 'Mañana', '08:00'),
        (3, '12-07-2025', 'Tarde', '14:00'),
        (3, '17-07-2025', 'Mañana', '10:30'),
        (3, '22-07-2025', 'Tarde', '16:30'),
        (3, '27-07-2025', 'Mañana', '09:00'),

        (4, '04-07-2025', 'Mañana', '08:00'),
        (4, '13-07-2025', 'Tarde', '15:00'),
        (4, '18-07-2025', 'Mañana', '10:30'),
        (4, '23-07-2025', 'Tarde', '14:00'),
        (4, '28-07-2025', 'Mañana', '09:00'),

        (5, '05-07-2025', 'Mañana', '08:00'),
        (5, '14-07-2025', 'Tarde', '16:30'),
        (5, '19-07-2025', 'Mañana', '10:30'),
        (5, '24-07-2025', 'Tarde', '15:00'),
        (5, '29-07-2025', 'Mañana', '09:00'),

        (6, '06-07-2025', 'Mañana', '08:00'),
        (6, '15-07-2025', 'Tarde', '14:00'),
        (6, '20-07-2025', 'Mañana', '10:30'),
        (6, '25-07-2025', 'Tarde', '16:30'),
        (6, '30-07-2025', 'Mañana', '09:00'),

        (7, '07-07-2025', 'Mañana', '08:00'),
        (7, '16-07-2025', 'Tarde', '15:00'),
        (7, '21-07-2025', 'Mañana', '10:30'),
        (7, '26-07-2025', 'Tarde', '14:00'),
        (7, '31-07-2025', 'Mañana', '09:00'),

        (8, '08-07-2025', 'Mañana', '08:00'),
        (8, '17-07-2025', 'Tarde', '16:30'),
        (8, '22-07-2025', 'Mañana', '10:30'),
        (8, '27-07-2025', 'Tarde', '15:00'),
        (8, '01-08-2025', 'Mañana', '09:00'),

        (9, '09-07-2025', 'Mañana', '08:00'),
        (9, '18-07-2025', 'Tarde', '14:00'),
        (9, '23-07-2025', 'Mañana', '10:30'),
        (9, '28-07-2025', 'Tarde', '16:30'),
        (9, '02-08-2025', 'Mañana', '09:00'),

        (10, '10-07-2025', 'Mañana', '08:00'),
        (10, '19-07-2025', 'Tarde', '15:00'),
        (10, '24-07-2025', 'Mañana', '10:30'),
        (10, '29-07-2025', 'Tarde', '14:00'),
        (10, '03-08-2025', 'Mañana', '09:00')
    ''')
    
    conn.execute('''
        INSERT INTO resultados_usuario (
        id_usuario, fecha_envio, hora_envio,
        glucosa, colesterol, rbc, hemoglobina, hematocrito,
        wbd, rpl, grupo_sanguineo,
        eco, parasitalogico_simple, parasitalogico_seriado,
        pr_dengue, pr_helicobacter, link_drive
        ) VALUES

        -- Usuario 1
        (1,'2025-07-05','09:00','85','180','4.5','14.1','42','7.0','200k','O+',
        'Normal. No hay alteraciones.', 'Sin hallazgos', '3 muestras negativas',
        'NS1 positivo, IgM negativo', 'IgG positivo', 'https://drive.com/doc1'),
        (1,'2025-07-12','09:10','92','190','4.6','14.3','43','6.8','210k','O+',
        'Sombra renal visible', 'Quistes benignos', '1 muestra con Blastocystis',
        'IgM positivo', 'C y T presentes', 'https://drive.com/doc2'),
        (1,'2025-07-19','09:20','88','185','4.4','14.0','41','7.2','205k','O+',
        'Todo normal', 'Sin parásitos', 'Negativo en las 3 muestras',
        'Negativo NS1, IgM e IgG', 'Sólo línea C presente', 'https://drive.com/doc3'),

        (2,'2025-07-22','14:10','98.8','198.7','4.5','13.8','41.4','6.8','222k','B+','Sombra renal visible','Leve concentración de protozoarios','1 muestra positiva para Blastocystis','IgM positivo','Sólo línea C presente','https://drive.com/doc_u2_720'),
        (2,'2025-07-21','10:00','84.1','186.8','4.6','13.7','43.7','6.6','205k','B+','Sin alteraciones significativas','Presencia de quistes benignos','Negativo en las 3 muestras','NS1 positivo, IgM negativo','C y T presentes','https://drive.com/doc_u2_834'),
        (2,'2025-07-13','17:10','83.0','166.9','4.8','13.4','41.8','6.8','198k','B+','Todo normal','Presencia de quistes benignos','1 muestra positiva para Blastocystis','Negativo NS1, IgM e IgG','C y T presentes','https://drive.com/doc_u2_837'),

        (3,'2025-07-25','17:30','88.4','165.8','4.8','13.4','42.2','6.7','230k','B+','Sin alteraciones significativas','Leve concentración de protozoarios','2 muestras negativas, 1 indeterminada','IgM positivo','Sólo línea C presente','https://drive.com/doc_u3_498'),
        (3,'2025-07-25','16:50','81.9','181.3','4.7','13.0','42.7','7.2','201k','B+','Sombra renal visible','Presencia de quistes benignos','2 muestras negativas, 1 indeterminada','IgM positivo','Línea T débil, requiere confirmación','https://drive.com/doc_u3_969'),
        (3,'2025-07-09','09:00','89.1','173.5','4.3','14.1','42.3','7.2','196k','B+','Sin alteraciones significativas','Sin hallazgos','Negativo en las 3 muestras','NS1 positivo, IgM negativo','Línea T débil, requiere confirmación','https://drive.com/doc_u3_934'),

        (4,'2025-07-23','15:50','96.2','189.6','4.8','13.1','41.6','6.9','229k','B-','Todo normal','Sin hallazgos','Negativo en las 3 muestras','IgM positivo','Sólo línea C presente','https://drive.com/doc_u4_164'),
        (4,'2025-07-16','11:50','81.6','184.0','4.2','13.4','41.4','6.6','225k','B-','Ligero engrosamiento vesical','Presencia de quistes benignos','Negativo en las 3 muestras','Negativo NS1, IgM e IgG','Sólo línea C presente','https://drive.com/doc_u4_992'),
        (4,'2025-07-25','13:50','82.0','190.1','4.2','13.9','40.6','6.8','241k','B-','Sombra renal visible','Leve concentración de protozoarios','Negativo en las 3 muestras','IgM positivo','C y T presentes','https://drive.com/doc_u4_124'),

        (5,'2025-07-14','11:20','92.4','177.0','4.8','14.7','43.7','6.7','194k','O-','Todo normal','Sin hallazgos','2 muestras negativas, 1 indeterminada','NS1 positivo, IgM negativo','Línea T débil, requiere confirmación','https://drive.com/doc_u5_627'),
        (5,'2025-07-22','08:40','87.6','194.0','4.2','14.6','41.0','6.8','213k','O-','Ligero engrosamiento vesical','Sin hallazgos','Negativo en las 3 muestras','IgM positivo','C y T presentes','https://drive.com/doc_u5_267'),
        (5,'2025-07-10','12:10','88.2','196.8','4.2','14.3','40.6','7.2','217k','O-','Todo normal','Sin hallazgos','Negativo en las 3 muestras','NS1 positivo, IgM negativo','C y T presentes','https://drive.com/doc_u5_797'),

        (6,'2025-07-20','13:40','86.7','162.0','4.5','13.5','41.0','6.8','230k','AB+','Sin alteraciones significativas','Sin hallazgos','2 muestras negativas, 1 indeterminada','IgM positivo','Sólo línea C presente','https://drive.com/doc_u6_327'),
        (6,'2025-07-25','14:30','98.8','187.8','4.6','13.1','42.2','6.8','217k','AB+','Ligero engrosamiento vesical','Presencia de quistes benignos','Negativo en las 3 muestras','NS1 positivo, IgM negativo','Sólo línea C presente','https://drive.com/doc_u6_685'),
        (6,'2025-07-07','12:00','95.8','174.8','4.3','14.6','40.9','6.9','240k','AB+','Todo normal','Presencia de quistes benignos','Negativo en las 3 muestras','Negativo NS1, IgM e IgG','C y T presentes','https://drive.com/doc_u6_222'),

        (7,'2025-07-20','08:00','90.6','174.1','4.6','13.1','43.3','6.5','215k','B+','Todo normal','Presencia de quistes benignos','2 muestras negativas, 1 indeterminada','Negativo NS1, IgM e IgG','C y T presentes','https://drive.com/doc_u7_666'),
        (7,'2025-07-10','09:00','91.2','165.0','4.2','13.9','41.4','6.6','207k','B+','Sombra renal visible','Presencia de quistes benignos','2 muestras negativas, 1 indeterminada','IgM positivo','C y T presentes','https://drive.com/doc_u7_312'),
        (7,'2025-07-21','17:00','89.7','183.1','4.4','14.8','41.3','6.7','204k','B+','Sin alteraciones significativas','Presencia de quistes benignos','Negativo en las 3 muestras','Negativo NS1, IgM e IgG','Línea T débil, requiere confirmación','https://drive.com/doc_u7_115'),

        (8,'2025-07-17','12:00','95.5','194.1','4.4','13.9','43.1','6.5','207k','AB+','Todo normal','Sin hallazgos','1 muestra positiva para Blastocystis','NS1 positivo, IgM negativo','Línea T débil, requiere confirmación','https://drive.com/doc_u8_218'),
        (8,'2025-07-09','10:30','84.7','188.2','4.6','13.5','41.5','6.9','211k','AB+','Sin alteraciones significativas','Leve concentración de protozoarios','Negativo en las 3 muestras','NS1 positivo, IgM negativo','C y T presentes','https://drive.com/doc_u8_111'),
        (8,'2025-07-20','13:30','91.5','174.5','4.7','13.1','40.4','7.0','203k','AB+','Ligero engrosamiento vesical','Presencia de quistes benignos','2 muestras negativas, 1 indeterminada','NS1 positivo, IgM negativo','Sólo línea C presente','https://drive.com/doc_u8_295'),

        (9,'2025-07-27','16:20','95.7','188.8','4.3','13.4','42.3','7.0','247k','O+','Ligero engrosamiento vesical','Leve concentración de protozoarios','1 muestra positiva para Blastocystis','IgM positivo','Línea T débil, requiere confirmación','https://drive.com/doc_u9_755'),
        (9,'2025-07-19','08:50','82.7','195.6','4.2','14.1','43.3','6.7','202k','O+','Sombra renal visible','Presencia de quistes benignos','Negativo en las 3 muestras','Negativo NS1, IgM e IgG','C y T presentes','https://drive.com/doc_u9_958'),
        (9,'2025-07-22','10:00','85.8','193.9','4.5','14.7','42.4','6.7','217k','O+','Sin alteraciones significativas','Presencia de quistes benignos','Negativo en las 3 muestras','IgM positivo','C y T presentes','https://drive.com/doc_u9_108'),

        (10,'2025-07-13','16:30','95.1','170.1','4.5','13.4','40.8','6.5','230k','A+','Todo normal','Presencia de quistes benignos','Negativo en las 3 muestras','IgM positivo','Sólo línea C presente','https://drive.com/doc_u10_634'),
        (10,'2025-07-11','14:20','90.2','185.1','4.3','13.5','42.5','6.7','245k','A+','Todo normal','Sin hallazgos','Negativo en las 3 muestras','IgM positivo','Sólo línea C presente','https://drive.com/doc_u10_437'),
        (10,'2025-07-19','09:20','96.0','185.6','4.3','13.3','40.3','6.5','200k','A+','Sombra renal visible','Leve concentración de protozoarios','Negativo en las 3 muestras','Negativo NS1, IgM e IgG','C y T presentes','https://drive.com/doc_u10_929')
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/landing')
def landing():
    # Forzamos user=None para que el navbar muestre solo Home/Login/Registro
    return render_template('landing.html', user=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        dni = request.form['dni']
        password = request.form['password']
        correo = request.form['correo']
        telefono = request.form['telefono']
        fecha_raw = request.form['fecha_nacimiento']
        fecha_nacimiento = datetime.strptime(fecha_raw, '%Y-%m-%d').strftime('%d-%m-%Y')

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuario (nombres, apellidos, dni, password, correo, telefono, fecha_nacimiento) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (nombres, apellidos, dni, password, correo, telefono, fecha_nacimiento))
        conn.commit()
        # Obtener el usuario recién creado
        cur.execute("SELECT * FROM usuario WHERE dni = ?", (dni,))
        user = cur.fetchone()
        conn.close()
        # Autenticar automáticamente
        session['user_id'] = user['id_usuario']
        session['user_name'] = f"{user['nombres']} {user['apellidos']}"
        # Verificar si es admin
        if user['dni'] == '72931578':
            session['is_admin'] = True
            return redirect(url_for('home_admin'))
        else:
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dni = request.form['dni']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE dni = ?", (dni,))
        user = cur.fetchone()
        conn.close()

        # Comparación directa de contraseña SIN hash
        if user and user['password'] == password:
            session['user_id'] = user['id_usuario']
            session['user_name'] = f"{user['nombres']} {user['apellidos']}"

            # Verificamos si es admin por su DNI específico
            if user['dni'] == '72931578':
                session['is_admin'] = True
                return redirect(url_for('home_admin'))
            else:
                return redirect(url_for('home'))
        else:
            flash('DNI o contraseña incorrecta.', 'danger')

    return render_template('login.html')


@app.route('/citas')
def citas():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('citas.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/crear_cita', methods=['GET', 'POST'])
def crear_cita():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        fecha_raw = request.form['fecha']
        fecha = datetime.strptime(fecha_raw, '%Y-%m-%d').strftime('%d-%m-%Y')
        turno = request.form['turno']
        horario = request.form['horario']
        id_usuario = session['user_id']

        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO citas_usuario (id_usuario, fecha, turno, horario) VALUES (?, ?, ?, ?)',
                    (id_usuario, fecha, turno, horario))
        conn.commit()
        conn.close()

        flash('Cita agendada exitosamente.', 'success')
        return redirect(url_for('citas'))

    return render_template('crear_cita.html')

@app.route('/historial_citas')
def historial_citas():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT fecha, turno, horario FROM citas_usuario WHERE id_usuario = ?', (session['user_id'],))
    citas = cur.fetchall()
    conn.close()

    return render_template('historial_citas.html', citas=citas)

@app.route('/historial_resultados')
def historial_resultados():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()
    user_id = session['user_id']

    cur.execute("""
        SELECT id_resultado, id_usuario, fecha_envio, hora_envio
        FROM resultados_usuario
        WHERE id_usuario = ?
        ORDER BY id_resultado DESC
    """, (user_id,))
    
    resultados = cur.fetchall()
    conn.close()

    return render_template('historial_resultados.html', resultados=resultados)

@app.route('/ver_resultado/<int:id_resultado>')
def ver_resultados_especifico(id_resultado):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM resultados_usuario
        WHERE id_resultado = ? AND id_usuario = ?
    """, (id_resultado, session['user_id']))

    fila = cur.fetchone()
    conn.close()

    if not fila:
        return "Resultado no encontrado o no autorizado", 404

    resultado = dict(fila)  

    return render_template('ver_resultado_usuario.html', resultado=resultado)






#*==============================================================
#*  SECCION ADMINISTRADOR DE RESULTADOS DEL USUARIO
#*==============================================================

@app.route('/admin')
def home_admin():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin/home_admin.html')

@app.route('/admin/resultados')
def admin_resultados():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin/resultados_admin.html')

@app.route('/admin/usuarios_resultado')
def tabla_usuarios_resultado():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    # Excluir usuarios con nombres 'ADMIN'
    cur.execute("""
        SELECT id_usuario, nombres, apellidos, correo, telefono
        FROM usuario
        WHERE UPPER(nombres) != 'ADMIN'
    """)
    usuarios = cur.fetchall()
    conn.close()

    return render_template('admin/tabla_usuarios_resultado.html', usuarios=usuarios)


@app.route('/admin/crear_resultado/<int:user_id>', methods=['GET', 'POST'])
def crear_resultado(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Obtener los datos del formulario
        glucosa = request.form['glucosa']
        colesterol = request.form['colesterol']
        rbc = request.form['rbc']
        hemoglobina = request.form['hemoglobina']
        hematocrito = request.form['hematocrito']
        wbc = request.form['wbd']
        rpl = request.form['rpl']
        grupo_sanguineo = request.form['grupo_sanguineo']
        eco = request.form['eco']
        parasitalogico_simple = request.form['parasitalogico_simple']
        parasitalogico_seriado = request.form['parasitalogico_seriado']
        pr_dengue = request.form['pr_dengue']
        pr_helicobacter = request.form['pr_helicobacter']
        link_drive = request.form['link_drive']
        
        # Fecha
        fecha_envio_raw = request.form['fecha_envio']
        try:
            fecha_dt = datetime.strptime(fecha_envio_raw, "%Y-%m-%d")
            fecha_envio = fecha_dt.strftime("%d-%m-%Y")
        except ValueError:
            flash("Fecha inválida.", "danger")
            return render_template('admi/crear_resultado.html')

        # Hora
        hora_envio = request.form['hora_envio']

        # Guardar en la base de datos
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO resultados_usuario (
                id_usuario, fecha_envio, hora_envio, glucosa, colesterol, rbc,
                hemoglobina, hematocrito, wbd, rpl, grupo_sanguineo, eco,
                parasitalogico_simple, parasitalogico_seriado, pr_dengue, pr_helicobacter, link_drive
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, fecha_envio, hora_envio, glucosa, colesterol, rbc,
            hemoglobina, hematocrito, wbc, rpl, grupo_sanguineo, eco,
            parasitalogico_simple, parasitalogico_seriado, pr_dengue, pr_helicobacter, link_drive
        ))


        conn.commit()
        conn.close()

        flash('Resultado registrado exitosamente.', 'success')
        return redirect(url_for('admin_resultados'))

    return render_template('admin/crear_resultado.html', user_id=user_id)


@app.route('/admin/usuarios_consulta')
def tabla_edicion():
  
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    # Solo los campos existentes, sin 'sexo'
    cur.execute("""
        SELECT id_usuario, dni, nombres, apellidos, correo, telefono
        FROM usuario
        WHERE UPPER(nombres) != 'ADMIN'
    """)
    usuarios = cur.fetchall()
    conn.close()

    return render_template('admin/tabla_consulta.html', usuarios=usuarios)


    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    # Elimina el resultado relacionado al usuario
    cur.execute("DELETE FROM resultado WHERE usuario_id = %s", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('tabla_edicion'))

@app.route('/admin/resultados_usuario/<int:user_id>')
def ver_resultados_usuario(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    # Obtener resultados
    cur.execute("""
        SELECT id_resultado, fecha_envio, hora_envio
        FROM resultados_usuario
        WHERE id_usuario = ?
        ORDER BY id_resultado DESC
    """, (user_id,))
    resultados = cur.fetchall()

    # Obtener nombres y apellidos del usuario
    cur.execute("SELECT nombres, apellidos FROM usuario WHERE id_usuario = ?", (user_id,))
    usuario = cur.fetchone()

    conn.close()

    return render_template(
        'admin/multiples_resultados_por_usuario.html',
        resultados=resultados,
        usuario=usuario
    )

@app.route('/admin/editar_resultado/<int:id_resultado>', methods=['GET', 'POST'])
def editar_resultado(id_resultado):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        # Captura de los campos desde el formulario
        glucosa = request.form['glucosa']
        colesterol = request.form['colesterol']
        hemoglobina = request.form['hemoglobina']
        rbc = request.form['rbc']
        hematocrito = request.form['hematocrito']
        wbd = request.form['wbd']
        rpl = request.form['rpl']
        grupo_sanguineo = request.form['grupo_sanguineo']
        eco = request.form['eco']
        parasitalogico_simple = request.form['parasitalogico_simple']
        parasitalogico_seriado = request.form['parasitalogico_seriado']
        pr_dengue = request.form['pr_dengue']
        pr_helicobacter = request.form['pr_helicobacter']
        link_drive = request.form['link_drive']

        # Actualizar los datos
        cur.execute("""
            UPDATE resultados_usuario
            SET glucosa = ?, colesterol = ?, hemoglobina = ?, rbc = ?, hematocrito = ?, wbd = ?, rpl = ?, 
                grupo_sanguineo = ?, eco = ?, parasitalogico_simple = ?, parasitalogico_seriado = ?, 
                pr_dengue = ?, pr_helicobacter = ?, link_drive = ?
            WHERE id_resultado = ?
        """, (
            glucosa, colesterol, hemoglobina, rbc, hematocrito, wbd, rpl,
            grupo_sanguineo, eco, parasitalogico_simple, parasitalogico_seriado,
            pr_dengue, pr_helicobacter, link_drive, id_resultado
        ))

        conn.commit()
        conn.close()
        return redirect(url_for('admin_resultados'))  # o a donde quieras redirigir

    # Si es GET, obtener los datos actuales del resultado
    cur.execute("SELECT * FROM resultados_usuario WHERE id_resultado = ?", (id_resultado,))
    resultado = cur.fetchone()
    conn.close()

    return render_template('admin/editar_resultado.html', resultado=resultado)

@app.route('/admin/eliminar_resultado/<int:id_resultado>')
def eliminar_resultado(id_resultado):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM resultados_usuario WHERE id_resultado = ?", (id_resultado,))
    conn.commit()
    conn.close()

    flash("Resultado eliminado correctamente.")
    return redirect(request.referrer or url_for('admin_resultados'))

#*==============================================================
#* SECCION ADMINISTRADOR DE CITAS DEL USUARIO

@app.route('/admin/citas_usuario/<int:user_id>')
def detalle_citas_usuario(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    # Obtener nombre completo del usuario
    cur.execute("SELECT nombres, apellidos FROM usuario WHERE id_usuario = ?", (user_id,))
    usuario = cur.fetchone()
    nombre_completo = f"{usuario['nombres']} {usuario['apellidos']}" if usuario else "Usuario"

    # Obtener citas del usuario
    cur.execute("""
        SELECT id_cita, fecha, turno, horario
        FROM citas_usuario
        WHERE id_usuario = ?
    """, (user_id,))
    citas_usuario = cur.fetchall()
    conn.close()

    return render_template('admin/detalle_citas_usuario.html', citas_usuario=citas_usuario, nombre_completo=nombre_completo)

@app.route('/admin/citas_general')
def citas_general():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT id_usuario, nombres, apellidos, dni, correo, telefono
    FROM usuario
    WHERE UPPER(nombres) != 'ADMIN'
    """)

    citas = cur.fetchall()
    conn.close()

    return render_template('admin/citas_general_usuarios.html', citas=citas)

@app.route('/admin/editar_cita/<int:id_cita>', methods=['GET', 'POST'])
def editar_cita(id_cita):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        nueva_fecha = request.form['fecha']
        nuevo_turno = request.form['turno']
        nuevo_horario = request.form['horario']


        cur.execute("SELECT id_usuario FROM citas_usuario WHERE id_cita = ?", (id_cita,))
        resultado = cur.fetchone()
        if not resultado:
            conn.close()
            return "Usuario no encontrado", 404

        user_id = resultado['id_usuario']


        cur.execute("""
            UPDATE citas_usuario
            SET fecha = ?, turno = ?, horario = ?
            WHERE id_cita = ?
        """, (nueva_fecha, nuevo_turno, nuevo_horario, id_cita))

        conn.commit()
        conn.close()


        return redirect(url_for('detalle_citas_usuario', user_id=user_id))


    cur.execute("SELECT * FROM citas_usuario WHERE id_cita = ?", (id_cita,))
    cita = cur.fetchone()
    conn.close()

    if not cita:
        return "Cita no encontrada", 404

    cita = dict(cita)


    if 'turno' in cita:
        cita['turno'] = cita['turno'].strip().capitalize()


    if 'fecha' in cita:
        from datetime import datetime
        try:
            fecha_obj = datetime.strptime(cita['fecha'], '%d-%m-%Y')
            cita['fecha'] = fecha_obj.strftime('%Y-%m-%d')
        except ValueError:
            pass

    return render_template('admin/editar_cita.html', cita=cita)

@app.route('/noticias/<int:noticia_id>')
def noticia_detalle(noticia_id):
    return render_template(f'noticias/{noticia_id}.html')

@app.route('/admin/eliminar_cita/<int:id_cita>', methods=['GET'])
def eliminar_cita(id_cita):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    # Obtener el ID del usuario antes de eliminar la cita
    cur.execute("SELECT id_usuario FROM citas_usuario WHERE id_cita = ?", (id_cita,))
    result = cur.fetchone()

    if not result:
        conn.close()
        flash('La cita no existe o ya fue eliminada', 'danger')
        return redirect(url_for('citas_general'))

    user_id = result['id_usuario']

    # Eliminar la cita
    cur.execute("DELETE FROM citas_usuario WHERE id_cita = ?", (id_cita,))
    conn.commit()
    conn.close()

    flash('Cita eliminada correctamente', 'success')
    return redirect(url_for('detalle_citas_usuario', user_id=user_id))

#*==============================================================
#* REPORTE DE DATOS DE USUARIO
#*==============================================================




@app.route('/descargar_pdf/<int:id_resultado>')
def descargar_pdf(id_resultado):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM resultados_usuario
        WHERE id_resultado = ? AND id_usuario = ?
    """, (id_resultado, session['user_id']))
    fila = cur.fetchone()
    conn.close()

    if not fila:
        return "Resultado no encontrado", 404

    resultado = dict(fila)

    # Renderizar la plantilla HTML
    html = render_template("pdf_resultado.html", resultado=resultado)

    # Convertir a PDF
    pdf_stream = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_stream)

    if pisa_status.err:
        return "Error al generar el PDF", 500

    response = make_response(pdf_stream.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=resultado.pdf'
    return response

@app.context_processor
def inject_user():
    return dict(user=session.get('user_name'))

if __name__ == '__main__':
    init_db()
    registrar_usuario()
    app.run(debug=True)
