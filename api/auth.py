from flask import Flask, Blueprint, current_app, request,jsonify
import json
import bcrypt, base64
from db_sqlite import query_db, get_data_from_database,modify_db

auth_bp = Blueprint('auth', __name__)

#carga el archivo json
def load_db():
    with open(current_app.config['DATABASE_FILE']) as f:
        return json.load(f)

def save_db(data):
    with open(current_app.config['DATABASE_FILE'], 'w') as file:
        json.dump(data, file, indent=2)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json #datos que vienen desde postman
    #print(data)
    #db = load_db() #datos almacenas en el servidor
    
    #for user in db["users"]:
    #    if user["username"] == data["username"] and user["password"] == data["password"]:
    #        return jsonify({'mensaje': 'login exitoso', 'user_id': user["id"]}), 200
    
    user = query_db(
        'SELECT * FROM users WHERE username = ?',
        (data['username'], ), one=True
    )

    if user:
        store_hash = user['password']
        # contraseñas: 1: mada el cliente, 2: en base de datos
        password_bytes = data['password'].encode('utf-8')
        stored_hasd_bytes = store_hash.encode('utf-8')
    
    if bcrypt.checkpw(password_bytes,stored_hasd_bytes):
        return jsonify({'mensaje': 'login exitoso', 'user_id':user['id']}), 200
    
    return jsonify({'Error': 'Credenciales invalidas'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    profilePicture = request.files['profilePicture']
    recivied_password_bytes = password.encode('utf-8')
    
    db = get_data_from_database('SELECT * FROM users')

    for u in db:
        hased_password = u["password"]
        hased_password_bytes = hased_password.encode('utf8')
        if bcrypt.checkpw(recivied_password_bytes, hased_password_bytes) and u["username"] == username:
            return jsonify({'Error': 'El usuario ya existe'}), 400 

    #if any(u[1] == data["username"] and bcrypt.checkpw(u[-1], recivied_password) for u in db):
    #    return jsonify({'Error' : 'El usuario ya existe'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    userid = modify_db('INSERT OR IGNORE INTO users(username, password) VALUES (?, ?)', (username, hashed_password.decode('utf-8')))

    jsondb = load_db()

    file = profilePicture.read()
    encoded_Data = base64.b64encode(file).decode('utf-8')

    newPictureProfile = {
        "id": len(jsondb["profilePicture"]) + 1,
        "user_Id": userid,
        "profilePicture": encoded_Data
    }

    jsondb["profilePicture"].append(newPictureProfile)
    save_db(jsondb)

    return jsonify({'mensaje': 'Usuario registrado correctamente'}), 201


@auth_bp.route('/users', methods=["GET"])
def get_users():
    db = query_db(
        'SELECT id, username FROM users'
    )
    return jsonify([dict(user) for user in db]), 200

