from controladores.beneficiario_controlador import BeneficiarioControlador
from vistas.utilidades import mostrar_lista


class BeneficiarioVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("========== AGENDA DE BENEFICIARIOS ==========")
        print("1. Agregar beneficiario frecuente.")
        print("2. Listar mis beneficiarios.")
        print("3. Buscar beneficiario por ID.")
        print("4. Modificar datos de beneficiario.")
        print("5. Eliminar beneficiario de la agenda.")
        print("6. Volver.")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idBeneficiario = input("ID Beneficiario: ").strip()
                nombres = input("Nombres: ").strip()
                apellidos = input("Apellidos: ").strip()
                numeroCuenta = input("Número de Cuenta Externa: ").strip()
                bancoDestino = input("Banco (BCP, BBVA, Interbank, etc.): ").strip()

                if BeneficiarioControlador.registrar(idBeneficiario, nombres, apellidos, numeroCuenta, bancoDestino):
                    print("Beneficiario añadido a tu agenda con éxito.")
                else:
                    print("No se pudo añadir al beneficiario.")

            elif opcion == "2":
                beneficiarios = BeneficiarioControlador.listar()
                mostrar_lista(beneficiarios)

            elif opcion == "3":
                idBeneficiario = input("ID Beneficiario: ").strip()
                beneficiario = BeneficiarioControlador.buscar(idBeneficiario)
                if beneficiario is None:
                    print("Beneficiario no encontrado.")
                else:
                    beneficiario.mostrar_beneficiario()

            elif opcion == "4":
                idBeneficiario = input("ID Beneficiario a modificar: ").strip()
                beneficiario = BeneficiarioControlador.buscar(idBeneficiario)
                
                if beneficiario is None:
                    print("Beneficiario no encontrado.")
                else:
                    nombres = input("Nuevos nombres: ").strip()
                    apellidos = input("Nuevos apellidos: ").strip()
                    numeroCuenta = input("Nuevo número de cuenta: ").strip()
                    bancoDestino = input("Nuevo banco destino: ").strip()

                    if BeneficiarioControlador.modificar(idBeneficiario, nombres, apellidos, numeroCuenta, bancoDestino):
                        print("Datos actualizados correctamente.")
                    else:
                        print("No se pudo actualizar.")

            elif opcion == "5":
                idBeneficiario = input("ID Beneficiario a eliminar: ").strip()
                if BeneficiarioControlador.eliminar(idBeneficiario):
                    print("Beneficiario eliminado de la agenda.")
                else:
                    print("No se pudo eliminar.")

            elif opcion == "6":
                break
            else:
                print("Opción inválida.")

                
