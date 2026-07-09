from __future__ import annotations

from modelos.cliente import Cliente


class CuentaBancaria:
    def __init__(
        self,
        idCuenta: str,
        numeroCuenta: str,
        tipoCuenta: str,
        saldo: float,          
        fechaApertura: str,
        estado: str,
        cliente: Cliente
    ) -> None:

        self.idCuenta: str = idCuenta
        self.numeroCuenta: str = numeroCuenta
        self.tipoCuenta: str = tipoCuenta
        self.saldo: float = saldo
        self.fechaApertura: str = fechaApertura
        self.estado: str = estado

        self.cliente: Cliente = cliente
        self.cliente.agregar_cuenta(self)

        self.tarjetas = []
        self.transacciones = []

    def agregar_tarjeta(self, tarjeta) -> None:
        self.tarjetas.append(tarjeta)

    def agregar_transaccion(self, transaccion) -> None:
        self.transacciones.append(transaccion)
    def mostrar_cuenta(self) -> None:
        
        print(f"--DATOS DE LA CUENTA--")
        print(f"------------------------")
        print(f"Número de Cuenta: {self.numeroCuenta}")
        print(f"Tipo de Cuenta: {self.tipoCuenta}")
        print(f"Saldo actual: S/ {self.saldo:.2f}")
        print(f"Fecha de Apertura: {self.fechaApertura}")
        print(f"Estado: {self.estado}")
        print(f"Titular: {self.cliente}")
       
    def __str__(self) -> str:
        return f"Cuenta {self.tipoCuenta} - {self.numeroCuenta}"


    
