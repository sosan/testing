from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from datetime import datetime
from ModuloMongodb.ManagerMongodb import managermongo

import os

app = Flask(__name__)
app.secret_key = 'todoSuperSecreto'


""" LOGICA"""
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        mensaje = ""
        return render_template('index.html')
    return render_template('index.html')


@app.route('/gastos', methods=['GET','POST'])
def gastos():
    fecha = ""
    concepto = ""
    valor = ""
    mensaje = ""
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        # provisional-------------
        print('*' * 50)
        print('fecha :', fecha)
        fecha_convertida = datetime(fecha.year, fecha.month, fecha.day)
        valor = request.form.get('valor')
        concepto = request.form.get('concepto')
        if fecha != "" and concepto != "" and valor != "":
            mensaje = "Evento registrado con éxito"
            managermongo.nuevo_registro(fecha_convertida, concepto, valor)
            return render_template('gastos.html', mensaje=mensaje)
        else:
            print('********** Dentro Gastos')
            mensaje = "Debe rellenar los campos...."  
            return render_template('gastos.html', mensaje=mensaje)  
    else:
        return render_template('gastos.html', mensaje=mensaje)  

    return render_template('index.html')


@app.route('/informe', methods=['GET','POST'])
def informe():
    mensaje = ""
    if request.method == 'POST':
        mesinfo= request.form.get('mesinfo')
        anoinfo= request.form.get('anoinfo')
        
        return render_template('informe.html', mensaje=mensaje)
    else:
        return render_template('informe.html', mensaje=mensaje)

        
    return render_template('informe.html')


# Run de la app
# HEROKU
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)