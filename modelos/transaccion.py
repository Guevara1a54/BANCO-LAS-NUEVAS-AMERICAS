from __future__ import annotations

from modelos.cuenta_bancaria import CuentaBancaria

class Transaccion:
    def __init__(
        self,
        idTransaccion: str,
        tipoTransaccion: str,  
        monto: float,          
        fecha: str,
        descripcion: str,
        cuenta,
        beneficiario = None  
    ) -> None:

        self.idTransaccion: str = idTransaccion
        self.tipoTransaccion: str = tipoTransaccion
        self.monto: float = monto
        self.fecha: str = fecha
        self.descripcion: str = descripcion

        self.cuenta: CuentaBancaria = cuenta
        self.cuenta.agregar_transaccion(self)

        self.beneficiario: CuentaBancaria | None = beneficiario
        if self.beneficiario is not None:
            self.beneficiario.agregar_transaccion(self)
            
    def mostrar_transaccion(self) -> None:
        print(f"--DATOS DE LA TRANSACCIÓN--")
        print(f"------------------------")
        print(f"ID: {self.idTransaccion} | Tipo: {self.tipoTransaccion}")
        print(f"Monto: S/. {self.monto:.2f}")
        print(f"Fecha: {self.fecha}")
        print(f"Descripción: {self.descripcion}")
        print(f"Cuenta Origen: {self.cuenta.numeroCuenta}")
        
        if self.beneficiario is not None:
            print(f"Cuenta Destino: {self.beneficiario.numeroCuenta}")
       
    def __str__(self) -> str:
        return f"Transacción {self.idTransaccion} ({self.tipoTransaccion}) ||| S/. {self.monto:.2f}"




    
