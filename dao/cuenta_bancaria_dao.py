from mysql.connector import Error

from bd.conexion import Conexion
from modelos.cuenta_bancaria import CuentaBancaria
from dao.cliente_dao import ClienteDAO


class CuentaBancariaDAO:
    _INSERTAR: str = """
        INSERT INTO CUENTA_BANCARIA (idCuenta, numeroCuenta, tipoCuenta, saldo, fechaApertura, estado, idCliente)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    _SELECCIONAR: str = """
        SELECT idCuenta, numeroCuenta, tipoCuenta, saldo, fechaApertura, estado, idCliente
        FROM CUENTA_BANCARIA
        ORDER BY numeroCuenta;
    """

    _BUSCAR_POR_ID: str = """
        SELECT idCuenta, numeroCuenta, tipoCuenta, saldo, fechaApertura, estado, idCliente
        FROM CUENTA_BANCARIA
        WHERE idCuenta = %s;
    """

    _ACTUALIZAR: str = """
        UPDATE CUENTA_BANCARIA
        SET numeroCuenta = %s, tipoCuenta = %s, saldo = %s, fechaApertura = %s, estado = %s, idCliente = %s
        WHERE idCuenta = %s;
    """

    _ELIMINAR: str = """
        DELETE FROM CUENTA_BANCARIA
        WHERE idCuenta = %s;
    """

    @classmethod
    def insertar(cls, cuenta: CuentaBancaria) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._INSERTAR,
                    (
                        cuenta.idCuenta,
                        cuenta.numeroCuenta,
                        cuenta.tipoCuenta,
                        cuenta.saldo,
                        cuenta.fechaApertura,
                        cuenta.estado,
                        cuenta.cliente.idCliente
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar cuenta bancaria: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar(cls) -> list[CuentaBancaria]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        cuentas: list[CuentaBancaria] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    cliente = ClienteDAO.buscar_por_id(reg[6])
                    if cliente is not None:
                        cuentas.append(
                            CuentaBancaria(reg[0], reg[1], reg[2], float(reg[3]), reg[4], reg[5], cliente)
                        )
            except Error as e:
                print(f"Error al listar cuentas bancarias: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return cuentas

    @classmethod
    def buscar_por_id(cls, idCuenta: str) -> CuentaBancaria | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        cuenta: CuentaBancaria | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_ID, (idCuenta,))
                reg = cursor.fetchone()
                if reg is not None:
                    cliente = ClienteDAO.buscar_por_id(reg[6])
                    if cliente is not None:
                        cuenta = CuentaBancaria(reg[0], reg[1], reg[2], float(reg[3]), reg[4], reg[5], cliente)
            except Error as e:
                print(f"Error al buscar cuenta bancaria: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return cuenta

    @classmethod
    def actualizar(cls, cuenta: CuentaBancaria) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._ACTUALIZAR,
                    (
                        cuenta.numeroCuenta,
                        cuenta.tipoCuenta,
                        cuenta.saldo,
                        cuenta.fechaApertura,
                        cuenta.estado,
                        cuenta.cliente.idCliente,
                        cuenta.idCuenta
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar cuenta bancaria: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def eliminar(cls, idCuenta: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ELIMINAR, (idCuenta,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar cuenta bancaria: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    
