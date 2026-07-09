from dao.empleado_dao import EmpleadoDAO
from dao.sucursal_dao import SucursalDAO
from modelos.empleado import Empleado


class EmpleadoControlador:
    @classmethod
    def registrar(
        cls, idEmpleado: str, dni: str, nombres: str, apellidos: str, cargo: str, salario: float, telefono: str, estado: str, idSucursal: str
    ) -> bool:
        sucursal = SucursalDAO.buscar_por_id(idSucursal)
        if sucursal is None:
            return False
        
        empleado = Empleado(idEmpleado, dni, nombres, apellidos, cargo, salario, telefono, estado, sucursal)
        return EmpleadoDAO.insertar(empleado) > 0

    @classmethod
    def listar(cls) -> list[Empleado]:
        return EmpleadoDAO.seleccionar()

    @classmethod
    def buscar(cls, idEmpleado: str) -> Empleado | None:
        return EmpleadoDAO.buscar_por_id(idEmpleado)

    @classmethod
    def modificar(
        cls, idEmpleado: str, dni: str, nombres: str, apellidos: str, cargo: str, salario: float, telefono: str, estado: str, idSucursal: str
    ) -> bool:
        sucursal = SucursalDAO.buscar_por_id(idSucursal)
        if sucursal is None:
            return False
            
        empleado = Empleado(idEmpleado, dni, nombres, apellidos, cargo, salario, telefono, estado, sucursal)
        return EmpleadoDAO.actualizar(empleado) > 0

    @classmethod
    def eliminar(cls, idEmpleado: str) -> bool:
        return EmpleadoDAO.eliminar(idEmpleado) > 0

    @classmethod
    def obtener_por_sucursal(cls, idSucursal: str) -> list:
        """
        Método intermediario que solicita al DAO la lista de empleados
        asociados a una sucursal específica.
        """
        id_limpio = idSucursal.strip()
        
        return EmpleadoDAO.seleccionar_por_sucursal(id_limpio)

    
