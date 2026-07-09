from mysql.connector import Error

from bd.conexion import Conexion
from modelos.prestamo import Prestamo
from dao.cliente_dao import ClienteDAO
from dao.empleado_dao import EmpleadoDAO


class PrestamoDAO:
    _INSERTAR: str = """
        INSERT INTO PRESTAMO (idPrestamo, monto, tasaInteres, plazoMeses, fechaPrestamo, estado, idCliente, idEmpleado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    _SELECCIONAR: str = """
        SELECT idPrestamo, monto, tasaInteres, plazoMeses, fechaPrestamo, estado, idCliente, idEmpleado
        FROM PRESTAMO
        ORDER BY idPrestamo;
    """

    _BUSCAR_POR_ID: str = """
        SELECT idPrestamo, monto, tasaInteres, plazoMeses, fechaPrestamo, estado, idCliente, idEmpleado
        FROM PRESTAMO
        WHERE idPrestamo = %s;
    """

    _ACTUALIZAR: str = """
        UPDATE PRESTAMO
        SET monto = %s, tasaInteres = %s, plazoMeses = %s, fechaPrestamo = %s, estado = %s, idCliente = %s, idEmpleado = %s
        WHERE idPrestamo = %s;
    """

    _ELIMINAR: str = """
        DELETE FROM PRESTAMO
        WHERE idPrestamo = %s;
    """

    @classmethod
    def insertar(cls, prestamo: Prestamo) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._INSERTAR,
                    (
                        prestamo.idPrestamo,
                        prestamo.monto,
                        prestamo.tasaInteres,
                        prestamo.plazoMeses,
                        prestamo.fechaPrestamo,
                        prestamo.estado,
                        prestamo.cliente.idCliente,
                        prestamo.empleado.idEmpleado
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar préstamo: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar(cls) -> list[Prestamo]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        prestamos: list[Prestamo] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    # 1. Recuperamos cliente y empleado usando los IDs de la fila
                    cliente = ClienteDAO.buscar_por_id(reg[6])
                    empleado = EmpleadoDAO.buscar_por_id(reg[7])
                    
                    # 2. Control de datos huérfanos para evitar que se oculte el préstamo
                    if cliente is None:
                        from modelos.cliente import Cliente
                        cliente = Cliente(idCliente=reg[6], nombres="CÓDIGO NO REGISTRADO", apellidos=f"({reg[6]})")
                        
                    if empleado is None:
                        from modelos.empleado import Empleado
                        empleado = Empleado(idEmpleado=reg[7], nombres="CÓDIGO NO REGISTRADO", apellidos=f"({reg[7]})")
                    
                    # 3. Agregamos el objeto a la lista (perfectamente alineado dentro del for)
                    prestamos.append(
                        Prestamo(reg[0], float(reg[1]), float(reg[2]), int(reg[3]), reg[4], reg[5], cliente, empleado)
                    )
            except Error as e:
                print(f"Error al listar préstamos en la base de datos: {e}")
            finally:
                # El bloque finally va exactamente al nivel del try original
                Conexion.cerrar_recursos(conexion, cursor)

        return prestamos

    @classmethod
    def buscar_por_id(cls, idPrestamo: str) -> Prestamo | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        prestamo: Prestamo | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_ID, (idPrestamo,))
                reg = cursor.fetchone()
                if reg is not None:
                    cliente = ClienteDAO.buscar_por_id(reg[6])
                    empleado = EmpleadoDAO.buscar_por_id(reg[7])
                    if cliente is not None and empleado is not None:
                        prestamo = Prestamo(reg[0], float(reg[1]), float(reg[2]), int(reg[3]), reg[4], reg[5], cliente, empleado)
            except Error as e:
                print(f"Error al buscar préstamo: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return prestamo

    @classmethod
    def actualizar(cls, prestamo: Prestamo) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._ACTUALIZAR,
                    (
                        prestamo.monto,
                        prestamo.tasaInteres,
                        prestamo.plazoMeses,
                        prestamo.fechaPrestamo,
                        prestamo.estado,
                        prestamo.cliente.idCliente,
                        prestamo.empleado.idEmpleado,
                        prestamo.idPrestamo
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar préstamo: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def eliminar(cls, idPrestamo: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ELIMINAR, (idPrestamo,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar préstamo: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas


    
