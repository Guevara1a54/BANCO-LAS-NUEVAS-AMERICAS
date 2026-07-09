from controladores.cliente_controlador import ClienteControlador
from vistas.utilidades import mostrar_lista


class ClienteVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("========== GESTIÓN DE CLIENTES ==========")
        print("1. Registrar cliente.")
        print("2. Listar clientes.")
        print("3. Buscar cliente por ID.")
        print("4. Modificar cliente.")
        print("5. Eliminar cliente.")
        print("6. Ver cuentas bancarias de un cliente.")
        print("7. Volver.")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idCliente = input("ID cliente: ").strip()
                dni = input("DNI: ").strip()
                nombres = input("Nombres: ").strip()
                apellidos = input("Apellidos: ").strip()
                direccion = input("Dirección: ").strip()
                telefono = input("Teléfono: ").strip()
                email = input("Email: ").strip()
                estado = input("Estado (Activo/Baneado): ").strip()
                idSucursal = input("ID Sucursal a la que pertenece: ").strip()

                if ClienteControlador.registrar(idCliente, dni, nombres, apellidos, direccion, telefono, email, estado, idSucursal):
                    print("Cliente registrado correctamente.")
                else:
                    print("No se pudo registrar el cliente.")

            elif opcion == "2":
                clientes = ClienteControlador.listar()
                mostrar_lista(clientes)

            elif opcion == "3":
                idCliente = input("ID cliente: ").strip()
                cliente = ClienteControlador.buscar(idCliente)

                if cliente is None:
                    print("Cliente no encontrado.")
                else:
                    print(cliente)

            elif opcion == "4":
                idCliente = input("ID cliente a modificar: ").strip()
                cliente = ClienteControlador.buscar(idCliente)

                if cliente is None:
                    print("Cliente no encontrado.")
                else:
                    print("Cliente actual:", cliente)
                    dni = input("Nuevo DNI: ").strip()
                    nombres = input("Nuevos nombres: ").strip()
                    apellidos = input("Nuevos apellidos: ").strip()
                    direccion = input("Nueva dirección: ").strip()
                    telefono = input("Nuevo teléfono: ").strip()
                    email = input("Nuevo email: ").strip()
                    estado = input("Nuevo estado: ").strip()
                    idSucursal = input("Nueva ID Sucursal: ").strip()

                    if ClienteControlador.modificar(idCliente, dni, nombres, apellidos, direccion, telefono, email, estado, idSucursal):
                        print("Cliente modificado correctamente.")
                    else:
                        print("No se pudo modificar el cliente.")

            elif opcion == "5":
                idCliente = input("ID cliente a eliminar: ").strip()
                confirmacion = input("¿Está seguro? (s/n): ").lower()

                if confirmacion == "s":
                    if ClienteControlador.eliminar(idCliente):
                        print("Cliente eliminado correctamente.")
                    else:
                        print("No se pudo eliminar el cliente.")

            elif opcion == "6":
                idCliente = input("ID cliente: ").strip()
                cuentas = ClienteControlador.listar_cuentas_cliente(idCliente)
                mostrar_lista(cuentas)

            elif opcion == "7":
                break
            else:
                print("Opción inválida.")

                
