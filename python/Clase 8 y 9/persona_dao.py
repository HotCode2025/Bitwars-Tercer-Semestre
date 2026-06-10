from logger_base import log
from persona import Persona
from conexion import Conexion

class PersonaDAO:
    """
    DAO: Data Access Object
    CRUD:
            CREATE
            READ
            UPDATE
            DELETE
    """

    _SELECCIONAR = 'SELECT * FROM persona ORDER BY persona_id'
    _INSERTAR = 'INSERT INTO persona(nombre, apellido, email) VALUES (%s, %s, %s)'
    _ACTUALIZAR = 'UPDATE persona SET nombre=%s, apellido=%s, email=%s WHERE id_persona=%s'
    _ELIMINAR = 'DELETE FROM persona WHERE id_persona=%s'

    # Definimos los métodos de la clase
    @classmethod
    def seleccionar(cls):
        with Conexion.obtenerConexion():
            with Conexion.obtenerCursor() as cursor:
                cursor.execute(cls._SELECCIONAR)

                registros = cursor.fetchall()

                personas = []

                for registro in registros:
                    # Un registro por columna
                    persona = Persona(registro[0], registro[1], registro[2], registro[3])
                    personas.append(persona)

        return personas

if __name__ == '__main__':
    personas = PersonaDAO.seleccionar()

    for persona in personas:
        log.debug(persona)