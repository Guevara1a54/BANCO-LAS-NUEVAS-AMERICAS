from __future__ import annotations

class Sucursal:
    def __init__(
        self,
        idSucursal: str,
        nombre: str,
        direccion: str,
        telefono: str,
        estado: str
    )->None:
        self.idSucursal: str = idSucursal
        self.nombre: str = nombre
        self.direccion: str = direccion
        self.telefono: str = telefono
        self.estado: str = estado

        self.empleados = []
        self.clientes= []

    def agregar_empleado(self,empleado)->None:
        self.empleados.append(empleado)

    def agregar_cliente(self,cliente)->None:
        self.clientes.append(cliente)

    def mostrar_sucursal(self)->None:
        print(f"--DATOS DE LA SUCURSAL--")
        print(f"------------------------")
        print(f"Código: {self.idSucursal}")
        print(f"Nombre: {self.nombre}")
        print(f"Estado: {self.estado}")

    def __str__(self)->str:
        return f"Sucursal {self.nombre}"
