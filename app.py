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
    return render_template('mainvet.html')


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


if __name__ == '__main__':
    app.run(port=3000, debug=True)
