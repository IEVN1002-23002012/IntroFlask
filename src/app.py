from flask import Flask, jsonify, request
from flask_cors import CORS
from database import mysql  # Importamos el mysql limpio desde database.py
from config import config

app = Flask(__name__)

# 1. PRIMERO cargamos la configuración de desarrollo
app.config.from_object(config['development'])

# 2. SEGUNDO inicializamos MySQL usando la app ya configurada (adiós a 'con = MySQL(app)')
mysql.init_app(app)

CORS(app)

# 3. TERCERO importamos y registramos los blueprints (cuando la app y la BD ya están listas)
from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp

app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404

app.register_error_handler(404, pagina_no_encontrada)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)