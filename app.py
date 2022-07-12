from flask import Flask
from flask import flash, render_template, request, redirect, send_from_directory, url_for
from flaskext.mysql import MySQL
from datetime import datetime
from forms import SignupForm


import os #operating sistem

# instanciando un objeto de tipo Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_BD'] = 'crud_codo'
app.config['MYSQL_DATABASE_PORT'] = 3307

UPLOADS = os.path.join('uploads')
app.config['UPLOADS'] = UPLOADS #Guardamos la ruta como un valor en la app

mysql.init_app(app)

@app.route('/uploads/<nombreFoto>') 
def uploads(nombreFoto): 
    return send_from_directory(app.config['UPLOADS'], nombreFoto)

@app.route('/team')
def index():
    sql = "SELECT * FROM `crud_codo`.`players` ORDER BY `number`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    # fetch all recupera todas las filas de la consulta y las devuelve en forma de tuplas
    players = cursor.fetchall()
    conn.commit()
    return render_template('players/team.html', players=players)

@app.route('/create')
def create():
    form = SignupForm()
    sql = "SELECT * FROM `crud_codo`.`players` ORDER BY `number`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    players = cursor.fetchall()
    conn.commit()
    return render_template('players/create.html', players=players, form=form)

@app.route("/destroy/<int:id>")
def destroy(id):
    conn = mysql.connect() 
    cursor = conn.cursor()
    cursor.execute("SELECT foto FROM `crud_codo`.`players` WHERE id=%s", id) 
    #al borrar elimina la foto del empleado
    fila= cursor.fetchall() 
    os.remove(os.path.join(app.config['UPLOADS'], fila[0][0]))
    cursor.execute("DELETE FROM `crud_codo`.`players` WHERE id=%s", (id)) 
    conn.commit() 
    return redirect('/team')

@app.route("/edit/<int:id>")
def edit(id):
    form = SignupForm()
    conn = mysql.connect() 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `crud_codo`.`players` WHERE id=%s", (id)) 
    players = cursor.fetchall()
    conn.commit() 
    sql = "SELECT * FROM `crud_codo`.`players` ORDER BY `number`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    players_list = cursor.fetchall()
    return render_template('players/edit.html', players=players, players_list=players_list, form=form)

@app.route('/update', methods=['POST']) 
def update():
    form = SignupForm()
    if not form.validate_on_submit():
        txtNombre = form.txtNombre.data
        flash('All fields are required')
        return redirect(url_for('edit', id = id)) 
    
    id=request.form['txtID'] 
    _nombre=request.form['txtNombre'] 
    _position = request.form['txtPosition'] 
    _num=request.form['txtNum']
    _foto=request.files['txtFoto']

    sql = "UPDATE `crud_codo`.`players` SET `name`=%s, `position`=%s, `number`=%s WHERE id=%s;" 
    datos=(_nombre, _position, _num, id)

    conn = mysql.connect() 
    cursor = conn.cursor() 

    now = datetime.now().strftime("%Y%H%M%S")
    if _foto.filename != '':
        newFotoName = now + _foto.filename
        _foto.save("uploads/"+ newFotoName)

        cursor.execute("SELECT foto FROM `crud_codo`.`players` WHERE id=%s", id) 
        fila= cursor.fetchall()

        os.remove(os.path.join(app.config['UPLOADS'], fila[0][0])) 
        cursor.execute("UPDATE `crud_codo`.`players` SET foto=%s WHERE id=%s;", (newFotoName, id)) 
        conn.commit()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/team')

@app.route('/store', methods=['POST'])
def storage():
    form = SignupForm()
    if not form.validate_on_submit():
        txtNombre = form.txtNombre.data
        return redirect(url_for('create', form = form))
    # creo variables para almacenar los datos enviados por el form
    _nombre = request.form['txtNombre']
    _position = request.form['txtPosition'] 
    _num=request.form['txtNum']
    _foto = request.files['txtFoto']
    now = datetime.now().strftime("%Y%H%M%S")
    
    if _foto.filename != '':
        newFotoName = now + _foto.filename
        _foto.save("uploads/"+ newFotoName)

    sql = "INSERT INTO `crud_codo`.`players` (`id`, `name`, `position`,`number`, `foto`) VALUES (NULL, %s, %s, %s, %s);"
    datos = (_nombre, _position, _num, newFotoName) 
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/team')

@app.route('/')
def team():
    return render_template('players/index.html')

# Esta linea de codigo es para que el programa no se rompa si existe un error
if __name__ == '__main__':
    app.run(debug=True)