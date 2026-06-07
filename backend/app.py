from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones_aracnidas'

CORS(app, resources={r"/api/*": {"origins": "*"}})

DATABASE = 'database.db'

def consultar_db(query, args=(), fetchone=False):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    resultado = cursor.fetchone() if fetchone else cursor.fetchall()
    conn.close()
    return resultado

@app.route('/api/login', methods=['POST'])
def login():
    datos = request.get_json()
    if not datos:
        return jsonify({"success": False, "error": "No se recibieron datos"}), 400
        
    username = datos.get('username')
    password = datos.get('password')
    
    usuario = consultar_db(
        "SELECT username, nombre FROM usuarios WHERE username = ? AND password = ?", 
        (username, password), 
        fetchone=True
    )
    
    if usuario:
        return jsonify({
            "success": True,
            "username": usuario[0],
            "nombre": usuario[1]
        }), 200
    else:
        return jsonify({
            "success": False, 
            "error": "Credenciales incorrectas. Intente de nuevo."
        }), 401

@app.route('/api/buscar_producto', methods=['POST'])
def buscar_producto():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Petición inválida"}), 400
        
    codigo = datos.get('codigo', '').upper()
    
    prod = consultar_db(
        "SELECT codigo, nombre, descripcion, precio, stock, categoria FROM productos WHERE codigo = ?", 
        (codigo,), 
        fetchone=True
    )
    
    if prod:
        return jsonify({
            "codigo": prod[0],
            "nombre": prod[1],
            "descripcion": prod[2],
            "precio": prod[3],
            "stock": prod[4],
            "categoria": prod[5]
        }), 200
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)