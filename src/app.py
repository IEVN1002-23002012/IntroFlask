from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
 
from config import config
 
app = Flask(__name__)
 
CORS(app)
 
@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = "select * from alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno = {"matricula": fila[0], "nombre": fila[1],
                      "apaterno": fila[2], "amaterno": fila[3],
                      "correo": fila[4]}
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Lista de alumnos',
                        'exito': True})
 
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False})
 
con = MySQL(app)
 
def leer_alumnos_bd(matricula):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM alumnos WHERE matricula = %s"
        cursor.execute(sql, (matricula,))
        datos = cursor.fetchall()
 
        if datos:
            alumno = {"matricula": datos[0][0], "nombre": datos[0][1],
                      "apaterno": datos[0][2], "amaterno": datos[0][3],
                      "correo": datos[0][4]}
            return alumno
 
        else:
            return None
    except Exception as ex:
        raise ex
 
@app.route("/alumnos/<mat>", methods=['GET'])
def leer_alumnos(mat):
    try:
        alumno = leer_alumnos_bd(mat)
        if alumno is not None:
            return jsonify({'alumnos': alumno, 'mensaje': 'Alumno encontrado', 'exito': True})
        else:
            return jsonify({'alumnos': alumno, 'mensaje': 'Alumno no encontrado', 'exito': False})
 
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False})
 
 
@app.route("/alumnos", methods=['POST'])
def registro_alumnos():
    try:
        alumno = leer_alumnos_bd(request.json['matricula'])
        if alumno is not None:
            return jsonify({"message": "Alumno ya Existe", 'exito': False})
        else:
            cursor = con.connection.cursor()
            sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (request.json['matricula'],
                                 request.json['nombre'],
                                 request.json['apaterno'],
                                 request.json['amaterno'],
                                 request.json['correo']))
            con.connection.commit()
            return jsonify({"message": "Ya quedo perro", 'exito': True})
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False})
 
@app.route("/alumnos/<mat>", methods=['PUT'])
def actualizar_curso(mat):
    try:
        alumno = leer_alumnos_bd(mat)
        if alumno != None:
            cursor = con.connection.cursor()
            sql = """UPDATE alumnos SET nombre=%s,
            apaterno=%s, amaterno=%s, correo=%s WHERE matricula=%s"""
            cursor.execute(sql, (
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo'],from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
 
from config import config
 
app = Flask(__name__)
 
CORS(app)
 
@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = "select * from alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno = {"matricula": fila[0], "nombre": fila[1],
                      "apaterno": fila[2], "amaterno": fila[3],
                      "correo": fila[4]}
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Lista de alumnos',
                        'exito': True})
 
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False})
 
con = MySQL(app)
 
def leer_alumnos_bd(matricula):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM alumnos WHERE matricula = %s"
        cursor.execute(sql, (matricula,))
        datos = cursor.fetchall()
 
        if datos:
            alumno = {"matricula": datos[0][0], "nombre": datos[0][1],
                      "apaterno": datos[0][2], "amaterno": datos[0][3],
                      "correo": datos[0][4]}
            return alumno
 
        else:
            return None
    except Exception as ex:
        raise ex
 
@app.route("/alumnos/<mat>", methods=['GET'])
def leer_alumnos(mat):
    try:
        alumno = leer_alumnos_bd(mat)
        if alumno is not None:
            return jsonify({'alumnos': alumno, 'mensaje': 'Alumno encontrado', 'exito': True})
        else:
            return jsonify({'alumnos': alumno, 'mensaje': 'Alumno no encontrado', 'exito': False})
 
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False})
 
 
@app.route("/alumnos", methods=['POST'])
def registro_alumnos():
    try:
        alumno = leer_alumnos_bd(request.json['matricula'])
        if alumno is not None:
            return jsonify({"message": "Alumno ya Existe", 'exito': False})
        else:
            cursor = con.connection.cursor()
            sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (request.json['matricula'],
                                 request.json['nombre'],
                                 request.json['apaterno'],
                                 request.json['amaterno'],
                                 request.json['correo']))
            con.connection.commit()
            return jsonify({"message": "Ya quedo perro", 'exito': True})
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False})
 
@app.route("/alumnos/<mat>", methods=['PUT'])
def actualizar_curso(mat):
    try:
        alumno = leer_alumnos_bd(mat)
        if alumno != None:
            cursor = con.connection.cursor()
            sql = """UPDATE alumnos SET nombre=%s,
            apaterno=%s, amaterno=%s, correo=%s WHERE matricula=%s"""
            cursor.execute(sql, (
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo'],
                mat
            ))
            con.connection.commit()
            return jsonify({"message": "Alumno Actualizado, mi perrito", 'exito': True})
        except Exception as ex:
            return jsonify({"message": "error {}".format(ex), 'exito': False})
 
def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>"
 
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)
                mat
            ))
            con.connection.commit()
            return jsonify({"message": "Alumno Actualizado, mi perrito", 'exito': True})
        except Exception as ex:
            return jsonify({"message": "error {}".format(ex), 'exito': False})
 
def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>"
 
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)
 