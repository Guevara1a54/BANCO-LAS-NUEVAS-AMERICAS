from __future__ import annotations

from modelos.sucursal import Sucursal

class Cliente:
    def __init__(
        self,
        idCliente: str,
        dni: str,
        nombres: str,
        apellidos: str,
        direccion: str,
        telefono: str,
        email: str,
        estado: str,
        sucursal: Sucursal
    ) -> None:

        self.idCliente: str = idCliente
        self.dni: str = dni
        self.nombres: str = nombres
        self.apellidos: str = apellidos
        self.direccion: str = direccion
        self.telefono: str = telefono
        self.email: str = email
        self.estado: str = estado

        self.sucursal: Sucursal = sucursal
        self.sucursal.agregar_cliente(self)

        self.cuentas= []
        self.prestamos = []

    def agregar_cuenta(self, cuenta) -> None:
        self.cuentas.append(cuenta)

    def agregar_prestamo(self, prestamo) -> None:
        self.prestamos.append(prestamo)

    def mostrar_cliente(self) -> None:
        print(f"--DATOS DEL CLIENTE--")
        print(f"------------------------")
        print(f"Código: {self.idCliente}")
        print(f"Cliente: {self.nombres} {self.apellidos}")
        print(f"Email: {self.email}")
        print(f"Sede Asignada: {self.sucursal.nombre}")
        
    def __str__(self) -> str:
        return f"{self.nombres} {self.apellidos}"


