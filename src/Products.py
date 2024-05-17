from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="Integracion2",
    password="Integracion2",
    database="Integracion2"
)
cursor = conn.cursor()

# Ruta para obtener todos los datos de la tabla product con sus precios
@app.route('/', methods=['GET'])
def obtener_productos_con_precios():
    cursor.execute("""
        SELECT 
            product.Código_del_producto AS Codigo_del_producto,
            product.Marca,
            product.Código AS Codigo,
            product.Nombre,
            precio.Fecha AS Fecha,
            precio.valor AS Valor
        FROM 
            product
        JOIN 
            precio ON product.id_Precio = precio.id
    """)
    rows = cursor.fetchall()
    
    # Lista para almacenar productos con sus precios
    productos_con_precios = []
    for row in rows:
        codigo_producto, marca, codigo, nombre, fecha, valor = row
        precio = {
            'Fecha': fecha.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            'Valor': float(valor)
        }
        
        codigo_producto, marca, codigo, nombre, fecha, valor = row
        producto = {
            'Codigo_del_producto': codigo_producto,
            'Marca': marca,
            'Codigo': codigo,
            'Nombre': nombre,
            'Precio': [precio]
        }
        productos_con_precios.append(producto)
    
    return render_template('hola.html', productos=productos_con_precios)

if __name__ == '__main__':
    app.run(debug=True)
