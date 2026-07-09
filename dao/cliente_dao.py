from mysql.connector import Error

from bd.conexion import Conexion
from modelos.cliente import Cliente
from dao.sucursal_dao import SucursalDAO  


class ClienteDAO:
    _INSERTAR: str = """
        INSERT INTO CLIENTE (idCliente, dni, nombres, apellidos, direccion, telefono, email, estado, idSucursal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    _SELECCIONAR: str = """
        SELECT idCliente, dni, nombres, apellidos, direccion, telefono, email, estado, idSucursal
        FROM CLIENTE
        ORDER BY apellidos, nombres;
    """

    _BUSCAR_POR_ID: str = """
        SELECT idCliente, dni, nombres, apellidos, direccion, telefono, email, estado, idSucursal
        FROM CLIENTE
        WHERE idCliente = %s;
    """

    _ACTUALIZAR: str = """
        UPDATE CLIENTE
        SET dni = %s, nombres = %s, apellidos = %s, direccion = %s, telefono = %s, email = %s, estado = %s, idSucursal = %s
        WHERE idCliente = %s;
    """

    _ELIMINAR: str = """
        DELETE FROM CLIENTE
        WHERE idCliente = %s;
    """

    @classmethod
    def insertar(cls, cliente: Cliente) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._INSERTAR,
                    (
                        cliente.idCliente,
                        cliente.dni,
                        cliente.nombres,
                        cliente.apellidos,
                        cliente.direccion,
                        cliente.telefono,
                        cliente.email,
                        cliente.estado,
                        cliente.sucursal.idSucursal
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar cliente: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar(cls) -> list[Cliente]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        clientes: list[Cliente] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    sucursal = SucursalDAO.buscar_por_id(reg[8])
                    if sucursal is not None:
                        clientes.append(
                            Cliente(reg[0], reg[1], reg[2], reg[3], reg[4], reg[5], reg[6], reg[7], sucursal)
                        )
            except Error as e:
                print(f"Error al listar clientes: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return clientes

    @classmethod
    def buscar_por_id(cls, idCliente: str) -> Cliente | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        cliente: Cliente | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_ID, (idCliente,))
                reg = cursor.fetchone()
                if reg is not None:
                    sucursal = SucursalDAO.buscar_por_id(reg[8])
                    if sucursal is not None:
                        cliente = Cliente(reg[0], reg[1], reg[2], reg[3], reg[4], reg[5], reg[6], reg[7], sucursal)
            except Error as e:
                print(f"Error al buscar cliente: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return cliente

    @classmethod
    def actualizar(cls, cliente: Cliente) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._ACTUALIZAR,
                    (
                        cliente.dni,
                        cliente.nombres,
                        cliente.apellidos,
                        cliente.direccion,
                        cliente.telefono,
                        cliente.email,
                        cliente.estado,
                        cliente.sucursal.idSucursal,
                        cliente.idCliente
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar cliente: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def eliminar(cls, idCliente: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ELIMINAR, (idCliente,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar cliente: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    
