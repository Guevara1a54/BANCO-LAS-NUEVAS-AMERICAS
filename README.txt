PROYECTO: BANCO LAS NUEVAS AMÉRICAS - Python + MySQL + POO + DAO + MVC

1. DESCRIPCIÓN
Este proyecto implementa el sistema informático del Banco Las Nuevas Américas usando:
- Python
- MySQL
- Programación Orientada a Objetos
- Patrón DAO
- Patrón MVC

La carpeta modelos contiene las entidades financieras:

- Sucursal
- Empleado
- Cliente
- Prestamo
- CuentaBancaria
- Tarjeta
- Beneficiario
- Transaccion

El código SQL está separado en la carpeta dao.
Las vistas de consola están separadas en la carpeta vistas.
Los controladores de la lógica de negocio están separados en la carpeta controladores.


banco_las_nuevas_americas/
│
├── main.py
├── script_bd_banco.sql
├── README.txt
│
├── bd/
│   └── conexion.py
│
├── modelos/
│   ├── sucursal.py
│   ├── empleado.py
│   ├── cliente.py
│   ├── prestamo.py
│   ├── cuenta_bancaria.py
│   └── tarjeta.py
│   └── beneficiario.py
│   └── transaccion.py
│
├── dao/
│   ├── sucursal_dao.py
│   ├── empleado_dao.py
│   ├── cliente_dao.py
│   ├── cuenta_bancaria_dao.py
│   ├── prestamo_dao.py
│   └── beneficiario_dao.py
│
├── controladores/
│   ├── sucursal_controlador.py
│   ├── empleado_controlador.py
│   ├── cliente_controlador.py
│   ├── cuenta_controlador.py
│   ├── prestamo_controlador.py
│   └── beneficiario_controlador.py
│   └── guardian_fraudes.py
│
└── vistas/
    ├── menu_principal_vista.py
    ├── sucursal_vista.py
    ├── empleado_vista.py
    ├── cliente_vista.py
    ├── cuenta_bancaria_vista.py
    ├── prestamo_vista.py
    └── beneficiario_vista.py

3. INSTALACIÓN DEL CONECTOR
Ejecutar en la terminal:

python -m pip install mysql-connector-python

4. CREAR BASE DE DATOS
Ejecutar en MySQL Workbench el archivo:

BDBANCO_LAS_NUEVAS_AMERICAS

5. CONFIGURAR CONEXIÓN
Abrir el archivo:

bd/conexion.py

Modificar si es necesario:

_HOST = "localhost"
_USER = "root"
_PASSWORD = "123456"
_DATABASE = "BDBANCO_LAS_NUEVAS_AMERICAS"
_PORT = 3306
# IMPORTANTE: Uso del Puerto 33061 en Computadoras de la Universidad César Vallejo.

6. EJECUTAR EL PROGRAMA
Desde la carpeta del proyecto ejecutar:

python main.py

7. FLUJO DE USO RECOMENDADO
1. Gestión de Sucursales.
2. Gestión de Empleados.
3. Gestión de Clientes.
4. Cuentas Bancarias y Operaciones.
5. Gestión de Préstamos.
6. Agenda de Beneficiarios.
7. Salir del Sistema

7. DESARROLLO CON STREAMLIT:
El uso de esta biblioteca fue crucial para desarrollarla de una manera más visual. Para ello creamos un archivo "app.py" en el cual se 
coloco el código necesario para configurar colores, patrones, figuras, imagenes, entre otros objetos.

Recalcar el uso del comando "streamlit run app.py" para ingresar en la página web de Banco Las Nuevas Americas.




