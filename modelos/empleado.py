from __future__ import annotations
from modelos.sucursal import Sucursal

class Empleado:
    def __init__(
        self,
        idEmpleado: str,
        dni: str,
        nombres: str,
        apellidos: str,
        cargo: str,
        salario: float,  
        telefono: str,
        estado: str,
        sucursal: Sucursal
    ) -> None:
        
        self.idEmpleado: str = idEmpleado
        self.dni: str = dni
        self.nombres: str = nombres
        self.apellidos: str = apellidos
        self.cargo: str = cargo
        self.salario: float = salario
        self.telefono: str = telefono
        self.estado: str = estado

        self.sucursal: Sucursal = sucursal
        self.sucursal.aggregate_empleado(self) if hasattr(self.sucursal, 'aggregate_empleado') else self.sucursal.agregar_empleado(self)

        self.prestamos = []        
    def agregar_prestamo(self, prestamo) -> None:
        self.prestamos.append(prestamo)

    def mostrar_empleado(self):
        print(f"--DATOS DEL EMPLEADO--")
        print(f"------------------------")
        print(f"Empleado: {self.nombres} {self.apellidos}")
        print(f"Cargo: {self.cargo}")
        print(f"Sede: {self.sucursal.nombre}")
        print(f"Salario: S/. {self.salario:.2f}")
        
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - Cargo: {self.cargo}"

    
