from dao.prestamo_dao import PrestamoDAO
from dao.cliente_dao import ClienteDAO
from dao.empleado_dao import EmpleadoDAO
from modelos.prestamo import Prestamo


class PrestamoControlador:
    @classmethod
    def registrar(cls, idPrestamo: str, monto: float, tasaInteres: float, plazoMeses: int, fechaPrestamo: str, estado: str, idCliente: str, idEmpleado: str) -> bool:
        cliente = ClienteDAO.buscar_por_id(idCliente)
        empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
        
        if cliente is None or empleado is None:
            return False
            
        prestamo = Prestamo(idPrestamo, monto, tasaInteres, plazoMeses, fechaPrestamo, estado, cliente, empleado)
        return PrestamoDAO.insertar(prestamo) > 0

    @classmethod
    def listar(cls) -> list[Prestamo]:
        return PrestamoDAO.seleccionar()

    @classmethod
    def buscar(cls, idPrestamo: str) -> Prestamo | None:
        return PrestamoDAO.buscar_por_id(idPrestamo)

    @classmethod
    def actualizar_estado(cls, idPrestamo: str, nuevo_estado: str) -> bool:
        prestamo = PrestamoDAO.buscar_por_id(idPrestamo)
        if prestamo is None:
            return False
            
        prestamo.estado = nuevo_estado
        return PrestamoDAO.actualizar(prestamo) > 0

    @classmethod
    def eliminar(cls, idPrestamo: str) -> bool:
        return PrestamoDAO.eliminar(idPrestamo) > 0


    
