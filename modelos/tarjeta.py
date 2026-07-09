from __future__ import annotations

from modelos.cuenta_bancaria import CuentaBancaria

class Tarjeta:
    def __init__(
        self,
        idTarjeta: str,
        numeroTarjeta: str,
        tipoTarjeta: str,  
        fechaEmision: str,
        fechaVencimiento: str,
        estado: str,
        cuenta: CuentaBancaria
    ) -> None:

        self.idTarjeta: str = idTarjeta
        self.numeroTarjeta: str = numeroTarjeta
        self.tipoTarjeta: str = tipoTarjeta
        self.fechaEmision: str = fechaEmision
        self.fechaVencimiento: str = fechaVencimiento
        self.estado: str = estado

        self.cuenta: CuentaBancaria = cuenta
        self.cuenta.agregar_tarjeta(self)

    def mostrar_tarjeta(self) -> None:
        print(f"--DATOS DE LA TARJETA--")
        print(f"------------------------")
        print(f"Número de Tarjeta: {self.numeroTarjeta}")
        print(f"Tipo de Tarjeta: {self.tipoTarjeta}")  
        print(f"Fecha Emisión: {self.fechaEmision}")
        print(f"Fecha Vencimiento: {self.fechaVencimiento}")
        print(f"Estado: {self.estado}")
        print(f"Asociada a la cuenta: {self.cuenta.numeroCuenta}")
       
    def __str__(self) -> str:
        return f"Tarjeta {self.tipoTarjeta} - {self.numeroTarjeta}"


