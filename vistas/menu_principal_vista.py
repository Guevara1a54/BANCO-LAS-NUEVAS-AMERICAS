from vistas.sucursal_vista import SucursalVista
from vistas.empleado_vista import EmpleadoVista
from vistas.cliente_vista import ClienteVista
from vistas.cuenta_bancaria_vista import CuentaBancariaVista
from vistas.prestamo_vista import PrestamoVista
from vistas.beneficiario_vista import BeneficiarioVista
from vistas.tarjeta_vista import TarjetaVista

class MenuPrincipalVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("\n========== BANCO FINANCIERO - MENÚ PRINCIPAL ==========")
        print("1. Gestión de Sucursales")
        print("2. Gestión de Empleados")
        print("3. Gestión de Clientes")
        print("4. Cuentas Bancarias y Operaciones")
        print("5. Gestión de Préstamos")
        print("6. Agenda de Beneficiarios")
        print("7. Gestión de Tarjetas (Débito/Crédito)") 
        print("8. Salir del Sistema")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una sección: ").strip()

            if opcion == "1":
                SucursalVista.ejecutar()
            elif opcion == "2":
                EmpleadoVista.ejecutar()
            elif opcion == "3":
                ClienteVista.ejecutar()
            elif opcion == "4":
                CuentaBancariaVista.ejecutar()
            elif opcion == "5":
                PrestamoVista.ejecutar()
            elif opcion == "6":
                BeneficiarioVista.ejecutar()
            elif opcion == "7":
                TarjetaVista.ejecutar()    
            elif opcion == "8":
                print("\nGracias por usar el sistema bancario. ¡Hasta pronto!")
                break
            else:
                print("Opción inválida.")
