from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from datetime import datetime
import calendar
from ModuloMongodb.ManagerMongodb import managermongo
from ModuloMongodb.ManagerMongodb import Errores

import os

app = Flask(__name__)
app.secret_key = 'todoSuperSecreto'

errores = Errores()

""" LOGICA"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mensaje = ""
        return render_template('index.html')
    return render_template('index.html')


@app.route('/gastos', methods=['GET', 'POST'])
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
        print('fecha_convertida :', fecha_convertida)
        print('*' * 50)

        # provisional-------------
        valor_str = request.form.get('valor')
        # pasado a float para luego poder hacer calculos
        valor = float(valor_str)
        concepto = request.form.get('concepto')
        listado_conceptos = managermongo.getlistado_conceptos(
            "test_usuario")
        if fecha_convertida != "" and concepto != "" and valor != "":
            # mensaje = "Evento registrado con éxito"
            mensaje = managermongo.nuevo_registro("test_usuario", fecha_convertida, concepto, valor)
            return render_template('gastos.html', fecha_actual=datetime.today(), mensaje=mensaje,
                                   listado_conceptos=listado_conceptos)
        else:
            mensaje = "Debe rellenar los campos...."
            return render_template('gastos.html', fecha_actual=datetime.today(), mensaje=mensaje,
                                   listado_conceptos=listado_conceptos)
    else:
        listado_conceptos = managermongo.getlistado_conceptos("test_usuario")
        errores = None
        if "errorinsertadoconcepto" in session:
            errores = session.pop("errorinsertadoconcepto")

        return render_template('gastos.html', fecha_actual=datetime.today(), mensaje=mensaje,
                               listado_conceptos=listado_conceptos, errores=errores)


@app.route("/nuevoconcepto", methods=["post"])
def nuevo_concepto():
    if "txt_concepto" in request.form:
        if request.form["txt_concepto"] == "":
            return redirect(url_for("gastos"))

        resultado = managermongo.insertar_nuevo_concepto("test_usuario", request.form["txt_concepto"])
        if resultado == errores.correcto:
            return redirect(url_for("gastos"))
        elif resultado == errores.duplicado:
            session["errorinsertadoconcepto"] = "Concepto Duplicado"
        else:
            session["errorinsertadoconcepto"] = "Fallo db"

    return redirect(url_for("gastos"))


@app.route("/nuevoconcepto", methods=["get"])
def nuevo_concepto_get():
    return redirect(url_for("gastos"))


@app.route("/renombrarconcepto", methods=["post"])
def renombrar_concepto():
    if "txt_renombrar_concepto" in request.form:
        if request.form["txt_renombrar_concepto"] == "":
            return redirect(url_for("gastos"))

        resultado = managermongo.renombrar_concepto(
            "test_usuario", request.form["concepto"], request.form["txt_renombrar_concepto"])

    return redirect(url_for("gastos"))


@app.route("/renombrarconcepto", methods=["get"])
def renombrar_concepto_get():
    return redirect(url_for("gastos"))


@app.route('/informe', methods=['GET', 'POST'])
def informe():
    anoinfo = 0
    mensaje = ""
    if request.method == 'POST':
        mes_str = request.form.get('mesinfo')
        ano_str = request.form.get('anoinfo')
        mesinfo = int(mes_str)
        anoinfo = int(ano_str)

        fecha_inicio_informe = datetime(anoinfo, mesinfo, 1)
        # calendar.monthrange te devuelve numero de semanas del mes[0] y ultimo dia del mes[1]
        fecha_fin_informe = datetime(anoinfo, mesinfo, calendar.monthrange(anoinfo, mesinfo)[1])

        print('***** Fechas desde hasta :', fecha_inicio_informe, ' ** ', fecha_fin_informe)
        informes = managermongo.getinforme(
            fecha_inicio_informe, fecha_fin_informe)

        return render_template('informe.html', anoactual=datetime.utcnow().year, mesactual=datetime.utcnow().month,
                               mensaje=mensaje, informes=informes)
    else:
        return render_template('informe.html', anoactual=datetime.utcnow().year, mesactual=datetime.utcnow().month,
                               mensaje=mensaje)


# Run de la app
# HEROKU
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
