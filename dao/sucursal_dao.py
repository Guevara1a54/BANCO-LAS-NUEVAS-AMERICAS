from mysql.connector import Error

from bd.conexion import Conexion
from modelos.sucursal import Sucursal

class SucursalDAO:
    _INSERTAR: str = """
        INSERT INTO SUCURSAL (idSucursal, nombre, direccion, telefono, estado)
        VALUES (%s, %s, %s, %s, %s);
    """

    _SELECCIONAR: str = """
        SELECT idSucursal, nombre, direccion, telefono, estado
        FROM SUCURSAL
        ORDER BY idSucursal ASC;
    """

    _BUSCAR_POR_ID: str = """
        SELECT idSucursal, nombre, direccion, telefono, estado
        FROM SUCURSAL
        WHERE idSucursal = %s;
    """

    _ACTUALIZAR: str = """
        UPDATE SUCURSAL
        SET nombre = %s, direccion = %s, telefono = %s, estado = %s
        WHERE idSucursal = %s;
    """

    _ELIMINAR: str = """
        DELETE FROM SUCURSAL
        WHERE idSucursal = %s;
    """

    @classmethod
    def insertar(cls, sucursal: Sucursal) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._INSERTAR, 
                    (
                        sucursal.idSucursal, 
                        sucursal.nombre, 
                        sucursal.direccion, 
                        sucursal.telefono, 
                        sucursal.estado
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar sucursal: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar(cls) -> list[Sucursal]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        sucursales: list[Sucursal] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    sucursales.append(Sucursal(reg[0], reg[1], reg[2], reg[3], reg[4]))
            except Error as e:
                print(f"Error al listar sucursales: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return sucursales

    @classmethod
    def buscar_por_id(cls, idSucursal: str) -> Sucursal | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        sucursal: Sucursal | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_ID, (idSucursal,))
                reg = cursor.fetchone()
                if reg is not None:
                    sucursal = Sucursal(reg[0], reg[1], reg[2], reg[3], reg[4])
            except Error as e:
                print(f"Error al buscar sucursal: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return sucursal

    @classmethod
    def actualizar(cls, sucursal: Sucursal) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._ACTUALIZAR, 
                    (
                        sucursal.nombre, 
                        sucursal.direccion, 
                        sucursal.telefono, 
                        sucursal.estado, 
                        sucursal.idSucursal
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar sucursal: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def eliminar(cls, idSucursal: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ELIMINAR, (idSucursal,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar sucursal: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas


    
