from controladores.empleado_controlador import EmpleadoControlador
from vistas.utilidades import mostrar_lista


class EmpleadoVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("========== GESTIÓN DE EMPLEADOS ==========")
        print("1. Registrar empleado.")
        print("2. Listar empleados.")
        print("3. Buscar empleado por ID.")
        print("4. Modificar empleado.")
        print("5. Eliminar empleado.")
        print("6. Volver.")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idEmpleado = input("ID empleado: ").strip()
                dni = input("DNI: ").strip()
                nombres = input("Nombres: ").strip()
                apellidos = input("Apellidos: ").strip()
                cargo = input("Cargo: ").strip()
                salario = float(input("Salario: ").strip() or 0)
                telefono = input("Teléfono: ").strip()
                estado = input("Estado (Activo/Inactivo): ").strip()
                idSucursal = input("ID Sucursal de trabajo: ").strip()

                if EmpleadoControlador.registrar(idEmpleado, dni, nombres, apellidos, cargo, salario, telefono, estado, idSucursal):
                    print("Empleado registrado correctamente.")
                else:
                    print("No se pudo registrar el empleado.")

            elif opcion == "2":
                empleados = EmpleadoControlador.listar()
                mostrar_lista(empleados)

            elif opcion == "3":
                idEmpleado = input("ID empleado: ").strip()
                empleado = EmpleadoControlador.buscar(idEmpleado)

                if empleado is None:
                    print("Empleado no encontrado.")
                else:
                    print(empleado)

            elif opcion == "4":
                idEmpleado = input("ID empleado a modificar: ").strip()
                empleado = EmpleadoControlador.buscar(idEmpleado)

                if empleado is None:
                    print("Empleado no encontrado.")
                else:
                    print("Empleado actual:", empleado)
                    dni = input("Nuevo DNI: ").strip()
                    nombres = input("Nuevos nombres: ").strip()
                    apellidos = input("Nuevos apellidos: ").strip()
                    cargo = input("Nuevo cargo: ").strip()
                    salario = float(input("Nuevo salario: ").strip() or 0)
                    telefono = input("Nuevo teléfono: ").strip()
                    estado = input("Nuevo estado: ").strip()
                    idSucursal = input("Nueva ID Sucursal: ").strip()

                    if EmpleadoControlador.modificar(idEmpleado, dni, nombres, apellidos, cargo, salario, telefono, estado, idSucursal):
                        print("Empleado modificado correctamente.")
                    else:
                        print("No se pudo modificar el empleado.")

            elif opcion == "5":
                idEmpleado = input("ID empleado a eliminar: ").strip()
                confirmacion = input("¿Está seguro? (s/n): ").lower()

                if confirmacion == "s":
                    if EmpleadoControlador.eliminar(idEmpleado):
                        print("Empleado eliminado correctamente.")
                    else:
                        print("No se pudo eliminar el empleado.")

            elif opcion == "6":
                break
            else:
                print("Opción inválida.")
