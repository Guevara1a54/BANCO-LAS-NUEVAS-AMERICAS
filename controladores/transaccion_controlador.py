from datetime import datetime
from dao.transaccion_dao import TransaccionDAO
from dao.cuenta_bancaria_dao import CuentaBancariaDAO

class TransaccionControlador:
    @classmethod
    def registrar_movimiento(cls, idCuenta: str, tipo: str, monto: float, fraude: float, veredicto: str) -> bool:
        """
        Registra de manera automática una auditoría de movimiento bancario
        guardando los indicadores analizados por el Machine Learning.
        """
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return TransaccionDAO.insertar(idCuenta, tipo, monto, fecha_actual, fraude, veredicto) > 0

    @classmethod
    def obtener_historial(cls, idCuenta: str) -> list[dict]:
        """
        Devuelve el récord histórico de operaciones de una cuenta específica ordenado cronológicamente.
        """
        cuenta = CuentaBancariaDAO.buscar_por_id(idCuenta)
        if cuenta is None:
            return []
        return TransaccionDAO.seleccionar_por_cuenta(idCuenta)