from controladores.prestamo_controlador import PrestamoControlador
from vistas.utilidades import mostrar_lista


class PrestamoVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("========== GESTIÓN DE PRÉSTAMOS ==========")
        print("1. Solicitar/Registrar préstamo.")
        print("2. Listar todos los préstamos.")
        print("3. Buscar préstamo por ID.")
        print("4. Cambiar estado de préstamo (Aprobar/Liquidar).")
        print("5. Eliminar registro de préstamo.")
        print("6. Volver.")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idPrestamo = input("ID Préstamo: ").strip()
                monto = float(input("Monto Solicitado: $").strip() or 0)
                tasaInteres = float(input("Tasa de Interés (%): ").strip() or 0)
                plazoMeses = int(input("Plazo (en meses): ").strip() or 0)
                fechaPrestamo = input("Fecha : ").strip()
                estado = input("Estado Inicial (Pendiente/Aprobado): ").strip()
                idCliente = input("ID del Cliente Solicitante: ").strip()
                idEmpleado = input("ID del Empleado Evaluador: ").strip()

                if PrestamoControlador.registrar(idPrestamo, monto, tasaInteres, plazoMeses, fechaPrestamo, estado, idCliente, idEmpleado):
                    print("Préstamo registrado en el sistema.")
                else:
                    print("No se pudo registrar la solicitud.")

            elif opcion == "2":
                prestamos = PrestamoControlador.listar()
                mostrar_lista(prestamos)

            elif opcion == "3":
                idPrestamo = input("ID Préstamo: ").strip()
                prestamo = PrestamoControlador.buscar(idPrestamo)
                if prestamo is None:
                    print("Préstamo no encontrado.")
                else:
                    print(prestamo)

            elif opcion == "4":
                idPrestamo = input("ID Préstamo: ").strip()
                nuevo_estado = input("Nuevo Estado (Aprobado/Rechazado/Pagado/Vigente): ").strip()
                if PrestamoControlador.actualizar_estado(idPrestamo, nuevo_estado):
                    print("Estado actualizado con éxito.")
                else:
                    print("No se pudo cambiar el estado.")

            elif opcion == "5":
                idPrestamo = input("ID Préstamo a borrar: ").strip()
                if PrestamoControlador.eliminar(idPrestamo):
                    print("Registro eliminado correctamente.")
                else:
                    print("No se pudo eliminar.")

            elif opcion == "6":
                break
            else:
                print("Opción inválida.")

                
