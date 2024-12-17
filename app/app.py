from flask import Flask, request, jsonify, render_template
import psycopg2
import requests

app = Flask(__name__)

# Conexión a las bases de datos
db1_conn = psycopg2.connect(
    host="db1",
    database="postgres",
    user="postgres",
    password="postgres"
)

db2_conn = psycopg2.connect(
    host="db2",
    database="postgres",
    user="postgres",
    password="postgres"
)

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para obtener usuarios y mostrar en el frontend
@app.route('/users/display', methods=['GET'])
def display_users():
    cur = db1_conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('users.html', users=users)

# Endpoint para obtener productos y mostrar en el frontend
@app.route('/products/display', methods=['GET'])
def display_products():
    cur = db2_conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('products.html', products=products)

# Endpoint para obtener IP pública y ubicación de AWS
@app.route('/aws-info', methods=['GET'])
def aws_info():
    try:
        # Obtener IP pública
        ip_info = requests.get("https://ipinfo.io").json()
        ip = ip_info.get("ip", "Unknown")
        location = ip_info.get("region", "Unknown") + ", " + ip_info.get("country", "Unknown")
        return render_template('aws_info.html', ip=ip, location=location)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
