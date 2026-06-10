import psycopg2 as db
from psycopg2 import pool
from logger_base import log

class Conexion:
    _DATABASE = 'test_bd'
    _USERNAME = 'postgres'
    _PASSWORD = 'admin'
    _PORT = '5432'
    _HOST = 'localhost'
    _MIN_CON = 1
    _MAX_CON = 5
    _pool = None
    _conexion = None
    _cursor = None

    @classmethod
    def obtenerConexion(cls):
        conexion = cls.obtenerPool().getconn()
        log.debug(f"Conexión obtenida del pool: {conexion}")
        return conexion

        """if cls._conexion is None:
            try:
                cls._conexion = db.connect(
                    host = cls._HOST,
                    user = cls._USERNAME,
                    password = cls._PASSWORD,
                    port = cls._PORT,
                    database = cls._DATABASE
                )

                log.debug(f"Conexión exitosa: {cls._conexion}")
                
                return cls._conexion
            except Exception as e:
                log.error(f"Ocurrió un error: {e}")
                sys.exit()
        else:
            return cls._conexion"""

    @classmethod
    def obtenerCursor(cls):
        pass 

        """if cls._cursor is None:
            try:
                cls._cursor = cls._obtenerConexion().cursor()
                log.debug(f"Se abrió correctamente el cursor: {cls._cursor}")

                return cls._cursor
            except Exception as e:
                log.error(f"Ocurrió un error: {e}")
                sys.exit()
        else:
            return cls._cursor"""

    @classmethod
    def obtenerPool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(
                    cls._MIN_CON,
                    cls._MAX_CON,
                    host = cls._HOST,
                    user = cls._USERNAME,
                    password = cls._PASSWORD,
                    port = cls._PORT,
                    database = cls._DATABASE
                )
            
                log.debug(f"Creación del pool exitosa: {cls._pool}")

                return cls._pool
            except Exception as e:
                log.error(f"Ocurrió un error: {e}")
        else:
            return cls._pool

    @classmethod
    def liberarConexion(cls, conexion):
        cls.obtenerPool().putconn(conexion)
        
        log.debug(f"Regresamos la conexión del pool: {conexion}")

    @classmethod
    def cerrarConexiones(cls):
        cls.obtenerPool().closeall()

# -------- Prueba --------
if __name__ == "__main__":
    conexion1 = Conexion.obtenerConexion()
    Conexion.liberarConexion(conexion1)
    conexion2 = Conexion.obtenerConexion()
    Conexion.liberarConexion(conexion2)