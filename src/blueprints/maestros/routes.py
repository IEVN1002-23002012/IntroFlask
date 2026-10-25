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


# GET: Listar todos los maestros
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


# GET: Consultar un maestro por matrícula
@maestros_bp.route('/<string:matricula>', methods=['GET'])
def leer_maestro(matricula):
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM maestros WHERE matricula = %s",
            (matricula,)
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


# POST: Registrar un maestro
@maestros_bp.route('/', methods=['POST'])
def registrar_maestro():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            'mensaje': 'Se requiere un objeto JSON',
            'exito': False
        }), 400

    campos = [
        'matricula', 'nombre', 'apaterno',
        'amaterno', 'correo'
    ]

    if any(
        campo not in datos
        or not isinstance(datos[campo], str)
        or not datos[campo].strip()
        for campo in campos
    ):
        return jsonify({
            'mensaje': 'Faltan campos obligatorios o son inválidos',
            'exito': False
        }), 400

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        # Comprobar si la matrícula ya existe
        cursor.execute(
            "SELECT matricula FROM maestros WHERE matricula = %s",
            (datos['matricula'].strip(),)
        )

        if cursor.fetchone() is not None:
            return jsonify({
                'mensaje': 'La matrícula ya existe',
                'exito': False
            }), 409

        # Insertar el maestro
        cursor.execute("""
            INSERT INTO maestros
                (matricula, nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s, %s)
        """, tuple(datos[campo].strip() for campo in campos))

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


# PUT: Modificar un maestro
@maestros_bp.route('/<string:matricula>', methods=['PUT'])
def modificar_maestro(matricula):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict) or not datos:
        return jsonify({
            'mensaje': 'No se recibieron datos para modificar',
            'exito': False
        }), 400

    nombre = datos.get('nombre')
    apaterno = datos.get('apaterno')
    amaterno = datos.get('amaterno')
    correo = datos.get('correo')

    if (
        not isinstance(nombre, str) or not nombre.strip()
        or not isinstance(apaterno, str) or not apaterno.strip()
        or not isinstance(correo, str) or not correo.strip()
        or not isinstance(amaterno, str)
    ):
        return jsonify({
            'mensaje': 'Nombre, apellido paterno, apellido materno y correo son obligatorios'
        }), 400

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT matricula FROM maestros WHERE matricula = %s",
            (matricula,)
        )

        maestro = cursor.fetchone()

        if not maestro:
            return jsonify({
                'mensaje': 'No existe un maestro con esa matrícula',
                'exito': False
            }), 404

        sql = """
            UPDATE maestros
            SET nombre = %s,
                apaterno = %s,
                amaterno = %s,
                correo = %s
            WHERE matricula = %s
        """

        cursor.execute(sql, (
            nombre.strip(),
            apaterno.strip(),
            amaterno.strip(),
            correo.strip(),
            matricula
        ))

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro modificado correctamente',
            'matricula': matricula,
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


# DELETE: Eliminar un maestro
@maestros_bp.route('/<string:matricula>', methods=['DELETE'])
def eliminar_maestro(matricula):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT matricula FROM maestros WHERE matricula = %s",
            (matricula,)
        )

        maestro = cursor.fetchone()

        if not maestro:
            return jsonify({
                'mensaje': 'No existe un maestro con esa matrícula',
                'exito': False
            }), 404

        cursor.execute(
            "DELETE FROM maestros WHERE matricula = %s",
            (matricula,)
        )

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro eliminado correctamente',
            'matricula': matricula,
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