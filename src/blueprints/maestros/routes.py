
from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)


def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


# GET: Listar maestros
@maestros_bp.route('/', methods=['GET'])
def listar_maestros():

    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM maestros")

        datos = cursor.fetchall()

        maestros = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': 'Error al consultar los maestros',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# GET: Consultar un maestro
@maestros_bp.route('/<int:idmaestro>', methods=['GET'])
def leer_maestro(idmaestro):

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM maestros WHERE idmaestro = %s",
            (idmaestro,)
        )

        fila = cursor.fetchone()

        if fila is None:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404

        maestro = fila_a_diccionario(cursor, fila)

        return jsonify({
            'maestro': maestro,
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': 'Error al consultar el maestro',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# POST: Registrar maestro
@maestros_bp.route('/', methods=['POST'])
def registrar_maestro():

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            'mensaje': 'Se requiere un objeto JSON',
            'exito': False
        }), 400

    campos = [
        'idmaestro',
        'nombre',
        'apaterno',
        'amaterno',
        'correo'
    ]

    if any(
        campo not in datos or
        datos[campo] is None or
        str(datos[campo]).strip() == ''
        for campo in campos
    ):
        return jsonify({
            'mensaje': 'Faltan campos obligatorios o son inválidos',
            'exito': False
        }), 400

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT idmaestro FROM maestros WHERE idmaestro = %s",
            (datos['idmaestro'],)
        )

        if cursor.fetchone() is not None:
            return jsonify({
                'mensaje': 'El ID del maestro ya existe',
                'exito': False
            }), 409

        cursor.execute("""
            INSERT INTO maestros
            (idmaestro, nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            datos['idmaestro'],
            datos['nombre'].strip(),
            datos['apaterno'].strip(),
            datos['amaterno'].strip(),
            datos['correo'].strip()
        ))

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro registrado correctamente',
            'exito': True
        }), 201

    except Exception as ex:
        mysql.connection.rollback()

        return jsonify({
            'mensaje': 'Error al registrar el maestro',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# PUT: Modificar maestro
@maestros_bp.route('/<int:idmaestro>', methods=['PUT'])
def modificar_maestro(idmaestro):

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            'mensaje': 'No se recibieron datos',
            'exito': False
        }), 400

    campos = ['nombre', 'apaterno', 'amaterno', 'correo']

    if any(
        not isinstance(datos.get(campo), str) or
        not datos[campo].strip()
        for campo in campos
    ):
        return jsonify({
            'mensaje': 'Todos los campos son obligatorios',
            'exito': False
        }), 400

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            "UPDATE maestros SET nombre=%s, apaterno=%s, amaterno=%s, correo=%s WHERE idmaestro=%s",
            (
                datos['nombre'].strip(),
                datos['apaterno'].strip(),
                datos['amaterno'].strip(),
                datos['correo'].strip(),
                idmaestro
            )
        )

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT idmaestro FROM maestros WHERE idmaestro=%s",
                (idmaestro,)
            )

            if cursor.fetchone() is None:
                return jsonify({
                    'mensaje': 'Maestro no encontrado',
                    'exito': False
                }), 404

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro modificado correctamente',
            'exito': True
        }), 200

    except Exception as ex:
        mysql.connection.rollback()

        return jsonify({
            'mensaje': 'Error al modificar el maestro',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# DELETE: Eliminar maestro
@maestros_bp.route('/<int:idmaestro>', methods=['DELETE'])
def eliminar_maestro(idmaestro):

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            "DELETE FROM maestros WHERE idmaestro = %s",
            (idmaestro,)
        )

        if cursor.rowcount == 0:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro eliminado correctamente',
            'exito': True
        }), 200

    except Exception as ex:
        mysql.connection.rollback()

        return jsonify({
            'mensaje': 'Error al eliminar el maestro',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()