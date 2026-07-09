from __future__ import annotations

class Beneficiario:
    def __init__(
        self,
        idBeneficiario: str,
        nombres: str,
        apellidos: str,
        numeroCuenta: str,
        bancoDestino: str,  
    ) -> None:

        self.idBeneficiario: str = idBeneficiario
        self.nombres: str = nombres
        self.apellidos: str = apellidos
        self.numeroCuenta: str = numeroCuenta
        self.bancoDestino: str = bancoDestino

        self.transacciones_recibidas= []

    def agregar_transaccion(self, transaccion) -> None:
        self.transacciones_recibidas.append(transaccion)

    def mostrar_beneficiario(self) -> None:
        print(f"--DATOS DEL BENEFICIARIO--")
        print(f"------------------------")
        print(f"Código: {self.idBeneficiario}")
        print(f"Nombre: {self.nombres} {self.apellidos}")
        print(f"Cuenta Destino: {self.numeroCuenta}")
        print(f"Banco Destino: {self.bancoDestino}")
       
    def __str__(self) -> str:
        return f"{self.nombres} {self.apellidos} ({self.bancoDestino})"
