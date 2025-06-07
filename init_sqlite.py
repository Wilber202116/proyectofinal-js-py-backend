import sqlite3
import os
import bcrypt

#ruta donde se guarda la base de datos
db_path = './backend/data/users.db'

#verifica si existe el archivo
os.makedirs('./data', exist_ok=True)

#conexion a sqlite

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
'''
#CREACION DE TABLA
cursor.execute(
    CREATE TABLE IF NOT EXISTS USERS(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    )'''

init_users = {
    ('calos', 'calve1223'), # id 1
    ('rodigo', '1223'), # id 2
    ('peldimo', 'peldimo123') # id 3
}
'''
#insertar usuarios a la base de datos
for username, password in init_users:

    #Esto lo guarda como tipo de dato byte
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute(
        INSERT OR IGNORE INTO users(username, password) VALUES (?,?)
    , (username, hashed_password.decode('utf-8')))
''' 

cursor.execute('DELETE FROM users WHERE id=7')
#resutados = cursor.fetchall()
#print(resutados)
#for fila in resutados:
#    print(fila[-1])

conn.commit()
conn.close()

print("Base de datos creada correctamente")
print("usuarios exitosamente agregados")