"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, current_app as app
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        print("Request data:", data)

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            print("Missing email or password")
            return jsonify({"error": "Correo y contraseña son requeridos"}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print("Usuario ya existe")
            return jsonify({"error": "El usuario ya existe"}), 409

        new_user = User(
            email=email,
            password=generate_password_hash(password),
            is_active=True  # ⚠️ Asegúrate de establecer esto si es obligatorio en tu modelo
        )

        db.session.add(new_user)
        db.session.commit()

        print("Usuario creado exitosamente")
        return jsonify({"message": "Usuario creado correctamente"}), 201

    except Exception as e:
        print("Error en el backend:", str(e))
        return jsonify({"error": "Error interno del servidor"}), 500

# ✅ Nuevo endpoint: Login
@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"msg": "Faltan datos"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Contraseña incorrecta"}), 401

        # Generar token JWT válido por 1 hora
        token = jwt.encode({
            "sub": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['FLASK_APP_KEY'], algorithm="HS256")

        return jsonify({"token": token, "user": user.serialize()}), 200

    except Exception as e:
        print("Error al intentar iniciar sesión:", str(e))
        return jsonify({"error": "Error interno al iniciar sesión"}), 500

