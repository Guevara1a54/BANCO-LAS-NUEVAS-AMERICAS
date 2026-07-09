from dao.cliente_dao import ClienteDAO
from dao.sucursal_dao import SucursalDAO
from dao.cuenta_bancaria_dao import CuentaBancariaDAO
from modelos.cliente import Cliente


class ClienteControlador:
    @classmethod
    def registrar(
        cls, idCliente: str, dni: str, nombres: str, apellidos: str, direccion: str, telefono: str, email: str, estado: str, idSucursal: str
    ) -> bool:
        sucursal = SucursalDAO.buscar_por_id(idSucursal)
        if sucursal is None:
            return False
            
        cliente = Cliente(idCliente, dni, nombres, apellidos, direccion, telefono, email, estado, sucursal)
        return ClienteDAO.insertar(cliente) > 0

    @classmethod
    def listar(cls) -> list[Cliente]:
        return ClienteDAO.seleccionar()

    @classmethod
    def buscar(cls, idCliente: str) -> Cliente | None:
        return ClienteDAO.buscar_por_id(idCliente)

    @classmethod
    def modificar(
        cls, idCliente: str, dni: str, nombres: str, apellidos: str, direccion: str, telefono: str, email: str, estado: str, idSucursal: str
    ) -> bool:
        sucursal = SucursalDAO.buscar_por_id(idSucursal)
        if sucursal is None:
            return False
            
        cliente = Cliente(idCliente, dni, nombres, apellidos, direccion, telefono, email, estado, sucursal)
        return ClienteDAO.actualizar(cliente) > 0

    @classmethod
    def eliminar(cls, idCliente: str) -> bool:
        return ClienteDAO.eliminar(idCliente) > 0

    @classmethod
    def listar_cuentas_cliente(cls, idCliente: str) -> list:
        cuentas = CuentaBancariaDAO.seleccionar()
        return [cta for cta in cuentas if cta.cliente.idCliente == idCliente]



    
