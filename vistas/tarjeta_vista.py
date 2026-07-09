from controladores.tarjeta_controlador import TarjetaControlador
from vistas.utilidades import mostrar_lista


class TarjetaVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("========== GESTIÓN DE TARJETAS ==========")
        print("1. Emitir / Registrar tarjeta")
        print("2. Listar todas las tarjetas")
        print("3. Consultar tarjeta por ID (Ver detalles)")
        print("4. Modificar datos de tarjeta")
        print("5. Bloquear / Eliminar tarjeta")
        print("6. Volver")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idTarjeta = input("ID Tarjeta: ").strip()
                numeroTarjeta = input("Número de Tarjeta (16 dígitos): ").strip()
                tipoTarjeta = input("Tipo (Débito/Crédito): ").strip()
                fechaEmision = input("Fecha Emision (AAAA-MM-DD): ").strip()
                fechaVencimiento = input("Fecha Vencimiento (AAAA-MM-DD): ").strip()
                estado = input("Estado (Activo/Bloqueado): ").strip()
                idCuenta = input("ID de Cuenta Bancaria asociada: ").strip()

                if TarjetaControlador.registrar(idTarjeta, numeroTarjeta, tipoTarjeta, fechaEmision, fechaVencimiento, estado, idCuenta):
                    print("Tarjeta emitida con éxito.")
                else:
                    print("No se pudo emitir la tarjeta. Verifique el ID de la cuenta.")

            elif opcion == "2":
                tarjetas = TarjetaControlador.listar()
                mostrar_lista(tarjetas)

            elif opcion == "3":
                idTarjeta = input("Ingrese el ID de la Tarjeta a consultar: ").strip()
                tarjeta = TarjetaControlador.buscar(idTarjeta)

                if tarjeta is None:
                    print("Tarjeta no encontrada en el sistema.")
                else:
                    print("\n--- DETALLES DE LA TARJETA ---")
                    tarjeta.mostrar_tarjeta()

            elif opcion == "4":
                idTarjeta = input("ID Tarjeta a modificar: ").strip()
                tarjeta = TarjetaControlador.buscar(idTarjeta)

                if tarjeta is None:
                    print("Tarjeta no encontrada.")
                else:
                    print("Datos actuales:", tarjeta)
                    numeroTarjeta = input("Nuevo número: ").strip()
                    tipoTarjeta = input("Nuevo tipo: ").strip()
                    fechaEmision = input("Nueva fecha vencimiento: ").strip()
                    fechaVencimiento = input("Nuevo CVV: ").strip()
                    estado = input("Nuevo estado: ").strip()
                    idCuenta = input("Nueva ID Cuenta: ").strip()

                    if TarjetaControlador.modificar(idTarjeta, numeroTarjeta, tipoTarjeta, fechaEmision, fechaVencimiento, estado, idCuenta):
                        print("Tarjeta modificada correctamente.")
                    else:
                        print("No se pudo modificar la tarjeta.")

            elif opcion == "5":
                idTarjeta = input("ID Tarjeta a dar de baja/bloquear: ").strip()
                confirmacion = input("¿Está seguro? (s/n): ").lower()

                if confirmacion == "s":
                    if TarjetaControlador.eliminar(idTarjeta):
                        print("Tarjeta dada de baja en el sistema.")
                    else:
                        print("No se pudo eliminar la tarjeta.")

            elif opcion == "6":
                break
            else:
                print("Opción inválida.")