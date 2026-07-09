from mysql.connector import Error

from bd.conexion import Conexion
from modelos.empleado import Empleado
from modelos.prestamo import Prestamo
from dao.sucursal_dao import SucursalDAO  


class EmpleadoDAO:
    _INSERTAR: str = """
        INSERT INTO EMPLEADO (idEmpleado, dni, nombres, apellidos, cargo, salario, telefono, estado, idSucursal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    _SELECCIONAR: str = """
        SELECT idEmpleado, dni, nombres, apellidos, cargo, salario, telefono, estado, idSucursal
        FROM EMPLEADO
        ORDER BY apellidos, nombres;
    """

    _BUSCAR_POR_ID: str = """
        SELECT idEmpleado, dni, nombres, apellidos, cargo, salario, telefono, estado, idSucursal
        FROM EMPLEADO
        WHERE idEmpleado = %s;
    """

    _ACTUALIZAR: str = """
        UPDATE EMPLEADO
        SET dni = %s, nombres = %s, apellidos = %s, cargo = %s, salario = %s, telefono = %s, estado = %s, idSucursal = %s
        WHERE idEmpleado = %s;
    """

    _ELIMINAR: str = """
        DELETE FROM EMPLEADO
        WHERE idEmpleado = %s;
    """
    _BUSCAR_POR_SUCURSAL = """
        SELECT idEmpleado, dni, nombres, apellidos, cargo, salario
        FROM EMPLEADO 
        WHERE idSucursal = %s;
    """


    @classmethod
    def insertar(cls, empleado: Empleado) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._INSERTAR,
                    (
                        empleado.idEmpleado,
                        empleado.dni,
                        empleado.nombres,
                        empleado.apellidos,
                        empleado.cargo,
                        empleado.salario,
                        empleado.telefono,
                        empleado.estado,
                        empleado.sucursal.idSucursal
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar empleado: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar(cls) -> list[Empleado]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        empleados: list[Empleado] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    sucursal = SucursalDAO.buscar_por_id(reg[8])
                    if sucursal is not None:
                        empleados.append(
                            Empleado(reg[0], reg[1], reg[2], reg[3], reg[4], float(reg[5]), reg[6], reg[7], sucursal)
                        )
            except Error as e:
                print(f"Error al listar empleados: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return empleados

    @classmethod
    def buscar_por_id(cls, idEmpleado: str) -> Empleado | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        empleado: Empleado | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_ID, (idEmpleado,))
                reg = cursor.fetchone()
                if reg is not None:
                    sucursal = SucursalDAO.buscar_por_id(reg[8])
                    if sucursal is not None:
                        empleado = Empleado(reg[0], reg[1], reg[2], reg[3], reg[4], float(reg[5]), reg[6], reg[7], sucursal)
            except Error as e:
                print(f"Error al buscar empleado: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return empleado

    @classmethod
    def actualizar(cls, empleado: Empleado) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(
                    cls._ACTUALIZAR,
                    (
                        empleado.dni,
                        empleado.nombres,
                        empleado.apellidos,
                        empleado.cargo,
                        empleado.salario,
                        empleado.telefono,
                        empleado.estado,
                        empleado.sucursal.idSucursal,
                        empleado.idEmpleado
                    )
                )
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar empleado: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def eliminar(cls, idEmpleado: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ELIMINAR, (idEmpleado,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar empleado: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar_por_sucursal(cls, idSucursal: str) -> list:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        lista_empleados = []
        
        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_SUCURSAL, (idSucursal,))
                for reg in cursor.fetchall():
                    # Guardamos los registros como diccionarios limpios para Pandas
                    lista_empleados.append({
                        "idEmpleado": reg[0],
                        "dni": reg[1],
                        "nombres": reg[2],
                        "apellidos": reg[3],
                        "cargo": reg[4],
                        "salario": float(reg[5]) if reg[5] is not None else 0.0
                    })
            except Error as e:
                print(f"Error en EmpleadoDAO.seleccionar_por_sucursal: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)
                
        return lista_empleados