from dao.tarjeta_dao import TarjetaDAO
from dao.cuenta_bancaria_dao import CuentaBancariaDAO
from modelos.tarjeta import Tarjeta


class TarjetaControlador:
    @classmethod
    def registrar(cls, idTarjeta: str, numeroTarjeta: str, tipoTarjeta: str, fechaEmision: str, fechaVencimiento: str, estado: str, idCuenta: str) -> bool:
        cuenta = CuentaBancariaDAO.buscar_por_id(idCuenta)
        if cuenta is None:
            return False
            
        tarjeta = Tarjeta(idTarjeta, numeroTarjeta, tipoTarjeta, fechaEmision, fechaVencimiento, estado, cuenta)
        return TarjetaDAO.insertar(tarjeta) > 0

    @classmethod
    def listar(cls) -> list:
        return TarjetaDAO.seleccionar()

    @classmethod
    def buscar(cls, idTarjeta: str):
        return TarjetaDAO.buscar_por_id(idTarjeta)

    @classmethod
    def modificar(cls, idTarjeta: str, numeroTarjeta: str, tipoTarjeta: str, fechaEmision: str, fechaVencimiento: str, estado: str, idCuenta: str) -> bool:
        cuenta = CuentaBancariaDAO.buscar_por_id(idCuenta)
        if cuenta is None:
            return False
            
        tarjeta = Tarjeta(idTarjeta, numeroTarjeta, tipoTarjeta, fechaEmision, fechaVencimiento, estado, cuenta)
        return TarjetaDAO.actualizar(tarjeta) > 0

    @classmethod
    def eliminar(cls, idTarjeta: str) -> bool:
        return TarjetaDAO.eliminar(idTarjeta) > 0