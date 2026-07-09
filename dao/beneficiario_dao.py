from mysql.connector import Error

from bd.conexion import Conexion
from modelos.beneficiario import Beneficiario


class BeneficiarioDAO:
    _INSERTAR: str = """
        INSERT INTO BENEFICIARIO (idBeneficiario, nombres, apellidos, numeroCuenta, bancoDestino)
        VALUES (%s, %s, %s, %s, %s);
    """

    _SELECCIONAR: str = """
        SELECT idBeneficiario, nombres, apellidos, numeroCuenta, bancoDestino
        FROM BENEFICIARIO
        ORDER BY apellidos, nombres;
    """

    _BUSCAR_POR_ID: str = """
        SELECT idBeneficiario, nombres, apellidos, numeroCuenta, bancoDestino
        FROM BENEFICIARIO
        WHERE idBeneficiario = %s;
    """

    _ACTUALIZAR: str = """
        UPDATE BENEFICIARIO
        SET nombres = %s, apellidos = %s, numeroCuenta = %s, bancoDestino = %s
        WHERE idBeneficiario = %s;
    """

    _ELIMINAR: str = """
        DELETE FROM BENEFICIARIO
        WHERE idBeneficiario = %s;
    """

    @classmethod
    def insertar(cls, beneficiario: Beneficiario) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._INSERTAR,
                    (
                        beneficiario.idBeneficiario,
                        beneficiario.nombres,
                        beneficiario.apellidos,
                        beneficiario.numeroCuenta,
                        beneficiario.bancoDestino
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar beneficiario: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar(cls) -> list[Beneficiario]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        beneficiarios: list[Beneficiario] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    beneficiarios.append(
                        Beneficiario(reg[0], reg[1], reg[2], reg[3], reg[4])
                    )
            except Error as e:
                print(f"Error al listar beneficiarios: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return beneficiarios

    @classmethod
    def buscar_por_id(cls, idBeneficiario: str) -> Beneficiario | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        beneficiario: Beneficiario | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_ID, (idBeneficiario,))
                reg = cursor.fetchone()
                if reg is not None:
                    beneficiario = Beneficiario(reg[0], reg[1], reg[2], reg[3], reg[4])
            except Error as e:
                print(f"Error al buscar beneficiario: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return beneficiario

    @classmethod
    def actualizar(cls, beneficiario: Beneficiario) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._ACTUALIZAR,
                    (
                        beneficiario.nombres,
                        beneficiario.apellidos,
                        beneficiario.numeroCuenta,
                        beneficiario.bancoDestino,
                        beneficiario.idBeneficiario
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar beneficiario: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def eliminar(cls, idBeneficiario: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ELIMINAR, (idBeneficiario,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar beneficiario: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas
