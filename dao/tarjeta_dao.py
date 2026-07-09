from bd.conexion import Conexion
from mysql.connector import Error
from modelos.tarjeta import Tarjeta
from dao.cuenta_bancaria_dao import CuentaBancariaDAO

class TarjetaDAO:

    @classmethod
    def seleccionar(cls) -> list[Tarjeta]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        lista_tarjetas = []
        
        if conexion and cursor:
            try:
                sql = "SELECT idTarjeta, numeroTarjeta, tipoTarjeta, fechaEmision, fechaVencimiento, estado, idCuenta FROM TARJETA"
                cursor.execute(sql)
                registros = cursor.fetchall()
                
                for reg in registros:
                    cuenta = CuentaBancariaDAO.buscar_por_id(reg[6])
                    
                    tarjeta = Tarjeta(
                        idTarjeta=reg[0],
                        numeroTarjeta=reg[1],
                        tipoTarjeta=reg[2],
                        fechaEmision=reg[3],
                        fechaVencimiento=reg[4],
                        estado=reg[5],
                        cuenta=cuenta
                    )
                    lista_tarjetas.append(tarjeta)
                    
            except Error as e:
                print(f"Error al seleccionar tarjetas: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)
                
        return lista_tarjetas

    @classmethod
    def buscar_por_id(cls, idTarjeta: str) -> Tarjeta | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        tarjeta = None
        
        if conexion and cursor:
            try:
                sql = "SELECT idTarjeta, numeroTarjeta, tipoTarjeta, fechaEmision, fechaVencimiento, estado, idCuenta FROM TARJETA WHERE idTarjeta = %s"
                cursor.execute(sql, (idTarjeta,))
                reg = cursor.fetchone()
                
                if reg:
                    cuenta = CuentaBancariaDAO.buscar_por_id(reg[6])
                    
                    tarjeta = Tarjeta(
                        idTarjeta=reg[0],
                        numeroTarjeta=reg[1],
                        tipoTarjeta=reg[2],
                        fechaEmision=reg[3],
                        fechaVencimiento=reg[4],
                        estado=reg[5],
                        cuenta=cuenta
                    )
            except Error as e:
                print(f"Error al buscar tarjeta por ID: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)
                
        return tarjeta

    @classmethod
    def insertar(cls, tarjeta: Tarjeta) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas = 0
        
        if conexion and cursor:
            try:
                sql = """INSERT INTO TARJETA (idTarjeta, numeroTarjeta, tipoTarjeta, fechaEmision, fechaVencimiento, estado, idCuenta) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                valores = (
                    tarjeta.idTarjeta,
                    tarjeta.numeroTarjeta,
                    tarjeta.tipoTarjeta,
                    tarjeta.fechaEmision,
                    tarjeta.fechaVencimiento,
                    tarjeta.estado,
                    tarjeta.cuenta.idCuenta
                )
                cursor.execute(sql, valores)
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar tarjeta: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)
                
        return filas
    


    @classmethod
    def actualizar(cls, tarjeta: Tarjeta) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas = 0
        
        if conexion and cursor:
            try:
                sql = """UPDATE TARJETA 
                         SET numeroTarjeta = %s, tipoTarjeta = %s, fechaEmision = %s, 
                             fechaVencimiento = %s, estado = %s, idCuenta = %s 
                         WHERE idTarjeta = %s"""
                valores = (
                    tarjeta.numeroTarjeta,
                    tarjeta.tipoTarjeta,
                    tarjeta.fechaEmision,
                    tarjeta.fechaVencimiento,
                    tarjeta.estado,
                    tarjeta.cuenta.idCuenta,
                    tarjeta.idTarjeta
                )
                cursor.execute(sql, valores)
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar tarjeta: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)
                
        return filas
    

    @classmethod
    def eliminar(cls, idTarjeta: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas = 0
        
        if conexion and cursor:
            try:
                sql = "DELETE FROM TARJETA WHERE idTarjeta = %s"
                cursor.execute(sql, (idTarjeta,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar tarjeta: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)
                
        return filas