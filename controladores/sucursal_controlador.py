from dao.sucursal_dao import SucursalDAO
from dao.empleado_dao import EmpleadoDAO
from modelos.sucursal import Sucursal


class SucursalControlador:
    @classmethod
    def registrar(cls, idSucursal: str, nombre: str, direccion: str, telefono: str, estado: str) -> bool:
        sucursal = Sucursal(idSucursal, nombre, direccion, telefono, estado)
        return SucursalDAO.insertar(sucursal) > 0

    @classmethod
    def listar(cls) -> list[Sucursal]:
        return SucursalDAO.seleccionar()

    @classmethod
    def buscar(cls, idSucursal: str) -> Sucursal | None:
        return SucursalDAO.buscar_por_id(idSucursal)

    @classmethod
    def modificar(cls, idSucursal: str, nombre: str, direccion: str, telefono: str, estado: str) -> bool:
        sucursal = Sucursal(idSucursal, nombre, direccion, telefono, estado)
        return SucursalDAO.actualizar(sucursal) > 0

    @classmethod
    def eliminar(cls, idSucursal: str) -> bool:
        return SucursalDAO.eliminar(idSucursal) > 0

    @classmethod
    def listar_empleados_sucursal(cls, idSucursal: str) -> list:
        empleados = EmpleadoDAO.seleccionar()
        return [emp for emp in empleados if emp.sucursal.idSucursal == idSucursal]
