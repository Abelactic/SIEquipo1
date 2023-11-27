from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password1'
app.config['MYSQL_DB'] = 'citas_vet'

mysql = MySQL(app)

app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/citas')
def Citas():
    return render_template('citas.html')


@app.route('/login')
def Login():
    return render_template('login.html')


@app.route('/main')
def Main():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM datosdecita')
    data = cur.fetchall()
    return render_template('mainvet.html', citas=data)


@app.route('/agendar_cita', methods=['POST'])
def agendar_cita():
    if request.method == 'POST':
        nomapellido = request.form['nomapellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        mascota = request.form['mascota']
        motivo = request.form['motivo']
        fecha = request.form['fecha']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO datosdecita (nomapellido,telefono,correo,mascota,motivo,fecha) VALUES (%s,%s,%s,%s,%s,%s)',
                    (nomapellido, telefono, correo, mascota, motivo, fecha))
        mysql.connection.commit()
        flash('Datos guardados!')
        return redirect(url_for('Citas'))


@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM datosdecita WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Cita Eliminada')
    return redirect(url_for('Main'))


@app.route('/editarcita/<id>')
def get_cita(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM datosdecita WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('mainedit.html', cita=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_cita(id):
    if request.method == 'POST':
        nomapellido = request.form['nomapellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        mascota = request.form['mascota']
        motivo = request.form['motivo']
        fecha = request.form['fecha']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE datosdecita
            SET nomapellido = %s,
                telefono = %s,
                correo = %s,
                mascota = %s,
                motivo = %s,
                fecha = %s
            WHERE id = %s
            """, (nomapellido, telefono, correo, mascota, motivo, fecha, id))
        mysql.connection.commit()
        flash('Cita actualizada con éxito')
        return redirect(url_for('Main'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
