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
        # fecha = request.form.get('fecha')
        fecha_str = request.form["fecha"]
        print('*' * 50)
        print('fecha :', fecha_str)
        # formato fecha_str: 2020-2-6
        trozos_fecha = fecha_str.split("-")
        ano = int(trozos_fecha[0])
        mes = int(trozos_fecha[1])
        dia = int(trozos_fecha[2])
        fecha_convertida = datetime(ano, mes, dia)
        
        # provisional-------------
        valor_str = request.form.get('valor')
        # pasado a float para luego poder hacer calculos
        valor = float(valor_str)
        concepto = request.form.get('concepto')
        if fecha_convertida != "" and concepto != "" and valor != "":
            # mensaje = "Evento registrado con éxito"
            mensaje = managermongo.nuevo_registro(fecha_convertida, concepto, valor)
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
        return render_template('informe.html', anoactual=datetime.utcnow().year, mesactual=datetime.utcnow().month,
                                mensaje=mensaje)

        
    return render_template('informe.html')


# Run de la app
# HEROKU
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
