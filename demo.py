import os
import sys
import cx_Oracle
from flask import Flask, render_template, abort,request, redirect, url_for, session
from flask import Flask

# alterar la sesion
def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("""
        ALTER SESSION SET
          TIME_ZONE = 'UTC'
          NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI'""")

# Función para establecer la conexión con la base de datos
def start_pool():
    pool_min = 4
    pool_max = 4
    pool_inc = 0
    pool_gmd = cx_Oracle.SPOOL_ATTRVAL_WAIT
    print("Connecting to", os.environ.get("PYTHON_CONNECTSTRING"))
    pool = cx_Oracle.SessionPool(user=os.environ.get("PYTHON_USERNAME"),
                                 password=os.environ.get("PYTHON_PASSWORD"),
                                 dsn=os.environ.get("PYTHON_CONNECTSTRING"),
                                 min=pool_min,
                                 max=pool_max,
                                 increment=pool_inc,
                                 threaded=True,
                                 getmode=pool_gmd,
                                 sessionCallback=init_session)

    return pool

# Definimos el nombre de la aplicación para flask
app = Flask(__name__)

# Muestra la página principal con su correspondiente plantilla
@app.route('/',methods=["GET","POST"])
def inicio():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("select table_name from user_tables")
    res = cursor.fetchall()
    return render_template("inicio.html",tablas=[res])

#mostrar registro
#@app.route('/tabla/<str:nombre>', methods=["GET","POST"])
#def verregistro(nombre):
#        connection = pool.acquire()
#        cursor = connection.cursor()
#        select_p = "SELECT * FROM %s"
#        dato = (int(nombre))
#        cursor.execute(select_p,dato)
#        for tabla in res:
#                if tabla == int(nombre):
#

# Intento de login, no funciona

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    username = request.form['username']
#    password = request.form['password']
#    user_ora = os.environ.get("PYTHON_USERNAME")
#    psswd_ora = os.environ.get("PYTHON_PASSWORD")
#    if username == user_ora and password == psswd_ora:
#         msg = 'Has iniciado sesion correctamente'
#         pool = start_pool()
#         return redirect('index.html', msg=msg)
#    else:
#         msg = 'ERROR'
#    return render_template('login.html')


# Este código funciona si se ha ejecutado previamente como usuario startup en la base de datos.
if __name__ == '__main__':

    # Iniciar la conexión a la base de datos 
    pool = start_pool()
    # Iniciar la aplicación web
    app.run(port=int(os.environ.get('PORT', '8080')))

