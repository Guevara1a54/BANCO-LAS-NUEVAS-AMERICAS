from controladores.cuenta_controlador import CuentaControlador
from vistas.utilidades import mostrar_lista


class CuentaBancariaVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("========== OPERACIONES Y CUENTAS BANCARIAS ==========")
        print("1. Abrir cuenta bancaria.")
        print("2. Listar todas las cuentas.")
        print("3. Consultar cuenta por ID (Ver saldo).")
        print("4. Realizar Depósito.")
        print("5. Realizar Retiro.")
        print("6. Realizar Transferencia")
        print("7. Ver historial de transacciones de la cuenta...")
        print("8. Cancelar/Eliminar cuenta.")
        print("9. Volver.")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idCuenta = input("ID de Cuenta: ").strip()
                numeroCuenta = input("Número de Cuenta Único: ").strip()
                tipoCuenta = input("Tipo (Ahorros/Corriente): ").strip()
                saldo_inicial = float(input("Depósito de Apertura: ").strip() or 0)
                fechaApertura = input("Fecha: ").strip()
                estado = input("Estado (Activo): ").strip()
                idCliente = input("ID del Cliente Titular: ").strip()

                if CuentaControlador.registrar(idCuenta, numeroCuenta, tipoCuenta, saldo_inicial, fechaApertura, estado, idCliente):
                    print("Cuenta bancaria abierta con éxito.")
                else:
                    print("No se pudo abrir la cuenta.")

            elif opcion == "2":
                cuentas = CuentaControlador.listar()
                mostrar_lista(cuentas)

            elif opcion == "3":
                idCuenta = input("ID de Cuenta: ").strip()
                cuenta = CuentaControlador.buscar(idCuenta)
                if cuenta is None:
                    print("Cuenta no encontrada.")
                else:
                    cuenta.mostrar_cuenta()

            elif opcion == "4":
                idCuenta = input("ID de tu Cuenta: ").strip()
                monto = float(input("Monto a depositar: $").strip() or 0)
                if CuentaControlador.depositar(idCuenta, monto):
                    print("Depósito exitoso.")
                else:
                    print("Operación rechazada.")

            elif opcion == "5":
                idCuenta = input("ID de tu Cuenta: ").strip()
                monto = float(input("Monto a retirar: $").strip() or 0)
                if CuentaControlador.retirar(idCuenta, monto):
                    print("Retiro exitoso.")
                else:
                    print("Fondos insuficientes o cuenta inactiva.")

            elif opcion == "6":
                idCuentaOrigen = input("ID de tu Cuenta: ").strip()
                idDestino = input("ID de Cuenta Destino o Beneficiario: ").strip()
                monto = float(input("Monto a transferir: $").strip() or 0)
                
                if CuentaControlador.transferir(idCuentaOrigen, idDestino, monto):
                    print("Transferencia procesada correctamente.")
                else:
                    print("No se pudo completar la transferencia.")

            elif opcion == "7":
                idCuenta = input("ID de Cuenta: ").strip()
                transacciones = CuentaControlador.obtener_historial(idCuenta)
                mostrar_lista(transacciones)

            elif opcion == "8":
                idCuenta = input("ID de Cuenta a cancelar: ").strip()
                confirmacion = input("¿Seguro que desea cerrar esta cuenta? (s/n): ").lower()
                if confirmacion == "s":
                    if CuentaControlador.eliminar(idCuenta):
                        print("Cuenta eliminada del sistema bancario.")
                    else:
                        print("No se pudo eliminar la cuenta.")

            elif opcion == "9":
                break
            else:
                print("Opción inválida.")

                
