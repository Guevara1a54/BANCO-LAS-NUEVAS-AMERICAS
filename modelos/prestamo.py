from __future__ import annotations

from modelos.cliente import Cliente
from modelos.empleado import Empleado

class Prestamo:
    def __init__(
        self,
        idPrestamo: str,
        monto: float,          
        tasaInteres: float,  
        plazoMeses: int,       
        fechaPrestamo: str,
        estado: str,
        cliente: Cliente,
        empleado: Empleado
    ) -> None:

        self.idPrestamo: str = idPrestamo
        self.monto: float = monto
        self.tasaInteres: float = tasaInteres
        self.plazoMeses: int = plazoMeses
        self.fechaPrestamo: str = fechaPrestamo
        self.estado: str = estado

        self.cliente: Cliente = cliente
        self.cliente.agregar_prestamo(self)

        self.empleado: Empleado = empleado
        self.empleado.agregar_prestamo(self)


    def mostrar_prestamo(self) -> None:
        print(f"--DATOS DEL PRÉSTAMO--")
        print(f"------------------------")
        print(f"Código: {self.idPrestamo}")
        print(f"Monto: S/. {self.monto:.2f} ||| Interés: {self.tasaInteres}%")
        print(f"Plazo: {self.plazoMeses} meses")
        print(f"Fecha: {self.fechaPrestamo}")
        print(f"Estado: {self.estado}")
        print(f"Gestionado por: {self.empleado}")
        print(f"Solicitado por: {self.cliente}")


    def __str__(self) -> str:
        return f"Préstamo {self.idPrestamo} - S/ {self.monto:.2f}"






















