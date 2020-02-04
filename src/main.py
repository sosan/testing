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
        pass
        return render_template('index.html')
    return render_template('index.html')



@app.route('/gastos', methods=['GET','POST'])
def gastos():
    fecha = ""
    concepto = ""
    valor = ""
    if request.method == 'POST':
        mensaje = ""
        fecha = request.form.get('fecha')
        concepto = request.form.get('concepto')
        valor = request.form.get('valor')
        # if fecha != "" and concepto != "" and valor != "":
        managermongo.nuevo_registro(fecha, concepto, valor)
        return render_template('/gastos.html')
    else:
        mensaje = "Debe rellenar los campos...."  
        return render_template('/gastos.html', mensaje=mensaje)  

    return render_template('index.html')



# Run de la app
# HEROKU
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# if __name__ == "__main__":
#     app.run('0.0.0.0', 5000, debug=True)