from mysql.connector import Error
from bd.conexion import Conexion


class TransaccionDAO:
    _INSERTAR: str = """
        INSERT INTO TRANSACCION (idCuenta, tipo, monto, fecha, porcentajeFraude, descripcion)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    
    _BUSCAR_POR_CUENTA: str = """
        SELECT T.idTransaccion, T.tipoTransaccion, T.monto, T.fecha, T.descripcion, B.nombres, B.apellidos
        FROM TRANSACCION T
        LEFT JOIN BENEFICIARIO B ON T.idBeneficiario = B.idBeneficiario
        WHERE T.idCuenta = %s 
        ORDER BY T.fecha DESC;
    """

    @classmethod
    def insertar(cls, idCuenta: str, tipo: str, monto: float, fecha: str, fraude: float, descripcion: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._INSERTAR, 
                    (idCuenta, tipo, monto, fecha, fraude, descripcion)
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al registrar transacción en BD: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)
        return filas

    @classmethod
    def seleccionar_por_cuenta(cls, idCuenta: str) -> list[dict]:
        conexion = Conexion.obtainer_conexion() if hasattr(Conexion, 'obtener_conexion') else Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        resultados: list[dict] = []

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_CUENTA, (idCuenta,))
                for reg in cursor.fetchall():
                    # Formateamos la fecha si es un objeto datetime/date
                    fecha_str = reg[3].strftime("%Y-%m-%d") if hasattr(reg[3], "strftime") else str(reg[3])
                    
                    # Armamos el nombre completo del beneficiario si existe
                    beneficiario_txt = f"{reg[5]} {reg[6]}" if reg[5] else "N/A (Mismo Titular)"

                    resultados.append({
                        "idTransaccion": reg[0],
                        "tipoTransaccion": reg[1],
                        "monto": float(reg[2]),
                        "fecha": fecha_str,
                        "descripcion": reg[4],
                        "idBeneficiario": beneficiario_txt
                    })
            except Error as e:
                print(f"❌ Error real en BD al listar transacciones de la cuenta {idCuenta}: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)
        return resultados