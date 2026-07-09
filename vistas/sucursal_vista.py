from controladores.sucursal_controlador import SucursalControlador
from vistas.utilidades import mostrar_lista


class SucursalVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("========== GESTIÓN DE SUCURSALES ==========")
        print("1. Registrar sucursal.")
        print("2. Listar sucursales.")
        print("3. Buscar sucursal por ID.")
        print("4. Modificar sucursal.")
        print("5. Eliminar sucursal.")
        print("6. Ver empleados de una sucursal...")
        print("7. Volver")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idSucursal = input("ID Sucursal: ").strip()
                nombre = input("Nombre de sede: ").strip()
                direccion = input("Dirección: ").strip()
                telefono = input("Teléfono: ").strip()
                estado = input("Estado (Activo/Inactivo): ").strip()

                if SucursalControlador.registrar(idSucursal, nombre, direccion, telefono, estado):
                    print("Sucursal registrada correctamente.")
                else:
                    print("No se pudo registrar la sucursal.")

            elif opcion == "2":
                sucursales = SucursalControlador.listar()
                mostrar_lista(sucursales)

            elif opcion == "3":
                idSucursal = input("ID Sucursal: ").strip()
                sucursal = SucursalControlador.buscar(idSucursal)

                if sucursal is None:
                    print("Sucursal no encontrada.")
                else:
                    print(sucursal)

            elif opcion == "4":
                idSucursal = input("ID Sucursal a modificar: ").strip()
                sucursal = SucursalControlador.buscar(idSucursal)

                if sucursal is None:
                    print("Sucursal no encontrada.")
                else:
                    print("Sucursal actual:", sucursal)
                    nombre = input("Nuevo nombre de sede: ").strip()
                    direccion = input("Nueva dirección: ").strip()
                    telefono = input("Nuevo teléfono: ").strip()
                    estado = input("Nuevo estado: ").strip()

                    if SucursalControlador.modificar(idSucursal, nombre, direccion, telefono, estado):
                        print("Sucursal modificada correctamente.")
                    else:
                        print("No se pudo modificar la sucursal.")

            elif opcion == "5":
                idSucursal = input("ID Sucursal a eliminar: ").strip()
                confirmacion = input("¿Está seguro? (s/n): ").lower()

                if confirmacion == "s":
                    if SucursalControlador.eliminar(idSucursal):
                        print("Sucursal eliminada correctamente.")
                    else:
                        print("No se pudo eliminar la sucursal.")

            elif opcion == "6":
                idSucursal = input("ID Sucursal: ").strip()
                empleados = SucursalControlador.listar_empleados_sucursal(idSucursal)
                mostrar_lista(empleados)

            elif opcion == "7":
                break
            else:
                print("Opción inválida.")
