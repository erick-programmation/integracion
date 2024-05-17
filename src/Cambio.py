from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import bcchapi

app = Flask(__name__)

# Inicializar bcchapi con credenciales de Bancocentral
siete = bcchapi.Siete("ER.MUNOZC@DUOCUC.CL", "INTEGRACION2")

def obtener_tipo_cambio_hoy():
    # Obtener la fecha y hora actual
    hoy = datetime.now().strftime('%Y-%m-%d')

    # Obtener el tipo de cambio CLP a USD de hoy
    serie = siete.get("F073.TCO.PRE.Z.D", hoy, hoy)

    # Verificar si hay datos en la lista de observaciones
    if serie.Series.get('Obs'):
        # Obtener el tipo de cambio CLP a USD de hoy
        clp_to_usd = float(serie.Series['Obs'][0]['value'])
        return clp_to_usd
    else:
        return None

def obtener_ultimo_tipo_cambio():
    # Obtener la fecha y hora actual
    ahora = datetime.now()

    # Inicializar la fecha de inicio de la búsqueda
    fecha_inicio = ahora - timedelta(days=1)  # Retroceder un día

    # Buscar el último valor disponible que no sea del fin de semana
    while fecha_inicio.weekday() in [5, 6]:  # 5: sábado, 6: domingo
        fecha_inicio -= timedelta(days=1)

    # Convertir la fecha de inicio a formato YYYY-MM-DD
    fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')

    # Obtener el último valor disponible de la serie de tipo de cambio CLP a USD
    serie = siete.get("F073.TCO.PRE.Z.D", fecha_inicio_str, fecha_inicio_str)

    # Verificar si hay datos en la lista de observaciones
    if serie.Series.get('Obs'):
        # Obtener el último tipo de cambio CLP a USD
        clp_to_usd = float(serie.Series['Obs'][-1]['value'])
        return clp_to_usd
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def obtener_tipo_cambio():
    if request.method == 'POST':
        # Obtener el valor ingresado en pesos chilenos
        clp_amount = float(request.form['clp_amount'])

        # Intentar obtener el valor del dólar para el día de hoy
        clp_to_usd = obtener_tipo_cambio_hoy()

        # Si no hay datos disponibles para el día de hoy, obtener el último valor disponible
        if clp_to_usd is None:
            clp_to_usd = obtener_ultimo_tipo_cambio()

        if clp_to_usd is not None:
            # Calcular el valor en dólares
            usd_amount = clp_amount / clp_to_usd

            # Formatear el valor en dólares con el símbolo de la unidad monetaria y dos decimales
            formatted_usd_amount = "${:.2f}".format(usd_amount)

            # Obtener el valor del dólar actual
            current_usd_value = f"Valor actual del Dolar: {clp_to_usd:.2f} CLP"

            # Devolver el valor en dólares formateado como respuesta en formato JSON
            return jsonify({"Monto en Dolar": formatted_usd_amount, "Dolar actual": current_usd_value})
        else:
            # Manejar el caso donde no se encuentran datos de la serie
            return jsonify({"error": "No se encontraron datos de la serie para la fecha actual ni datos disponibles en la serie."}), 404
    else:
        # Renderizar el formulario para ingresar el valor en pesos chilenos
        return '''
            <form method="post">
                <label for="clp_amount">Ingrese el valor en pesos chilenos sin puntos:</label><br>
                <input type="text" id="clp_amount" name="clp_amount"><br>
                <input type="submit" value="Convertir a USD">
            </form>
            '''

if __name__ == '__main__':
    app.run(debug=True)
