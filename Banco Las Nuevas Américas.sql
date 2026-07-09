-- Banco "Las Nuevas Américas"
-- POO - CIBERSEGURIDAD V

CREATE DATABASE BDBANCO_LAS_NUEVAS_AMERICAS;
USE BDBANCO_LAS_NUEVAS_AMERICAS;

-- TABLAS:

-- SUCURSAL
CREATE TABLE SUCURSAL(
	idSucursal CHAR(5) NOT NULL,
	nombre VARCHAR(60) NOT NULL,
	direccion VARCHAR(100) NOT NULL,
	telefono VARCHAR(20) NOT NULL,
	estado VARCHAR(20) NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo','Remodelacion','Cerrado')),
	PRIMARY KEY(idSucursal)
);

-- SUCURSAL: Estado.- Activo, Remodelacion, Cerrado
INSERT INTO SUCURSAL 
VALUES
	('S0001','Sucursal Mall','Av. América 566','080135402','Activo'),
	('S0002','Sucursal Loreto','Jr. Shinca 122','080014600','Activo'),
	('S0003','Sucursal Trujillo','Av. Larco 357','980198787','Activo'),
	('S0004','Sucursal Lima','Av. Javier Prado','615610222','Activo'),
	('S0005','Sucursal Sur','Av. Joaquín Olmedo','622080991','Remodelacion'),
	('S0006','Sucursal Cusco','Av. Sol del Inca','403221806','Activo'),
	('S0007','Sucursal Puno','Jr. Huaylas','607114505','Cerrado');    

SELECT * FROM SUCURSAL;

-- EMPLEADO
CREATE TABLE EMPLEADO(
	idEmpleado CHAR(5) NOT NULL,
	dni CHAR(8) NOT NULL UNIQUE,
	nombres VARCHAR(50) NOT NULL,
	apellidos VARCHAR(50) NOT NULL,
	cargo VARCHAR(40) NOT NULL,
	salario DOUBLE NOT NULL CHECK (salario >= 2000),
	telefono VARCHAR(20) NOT NULL,
	estado VARCHAR(20) NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo','Suspendido', 'Cesado')),
	idSucursal CHAR(5) NOT NULL,
	PRIMARY KEY(idEmpleado),
	FOREIGN KEY(idSucursal) REFERENCES SUCURSAL(idSucursal)
);
-- EMPLEADO: Estado.- Activo, Suspendido, Cesado
INSERT INTO EMPLEADO 
VALUES
	('E0001','40149930','Marcelo Luis','Gastañal Meza','Gerente',4500,'991305224','Activo','S0001'),
	('E0002','60842023','Sandra Ximena','Perez Urtado','Asesora',2500,'990867401','Activo','S0001'),
	('E0003','15902434','Miguel Ángel','Rojas Saldaña','Asesor',3000,'924576888','Activo','S0003'),
	('E0004','60994570','Patricia Judith','Vega Burgos','Gerente',5000,'910301446','Activo','S0004'),
	('E0005','58904032','Ricardo Mateo','Arjona Palacios','Cajero',2400,'992701884','Activo','S0005'),
	('E0006','60994510','Lucas Leonardo','Escobedo Ponte','Cajero',2400,'901334710','Cesado','S0007'),
	('E0007','71803352','Alma Mía','Salas Pretell','Asesora',3200,'934002616','Activo','S0006');

SELECT * FROM EMPLEADO;


-- CLIENTE
CREATE TABLE CLIENTE(
	idCliente CHAR(5) NOT NULL,
	dni CHAR(8) NOT NULL UNIQUE,
	nombres VARCHAR(50) NOT NULL,
	apellidos VARCHAR(50) NOT NULL,
	direccion VARCHAR(100) NOT NULL,
	telefono VARCHAR(20) NOT NULL,
	email VARCHAR(100) UNIQUE,
	estado VARCHAR(20) NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo','Inactivo', 'Bloqueado')),
	idSucursal CHAR(5) NOT NULL,
	PRIMARY KEY(idCliente),
	FOREIGN KEY(idSucursal) REFERENCES SUCURSAL(idSucursal)
);

-- CLIENTE: Estado.- Activo, Inactivo, Bloqueado
INSERT INTO CLIENTE 
VALUES
	('C0001','70349056','Jorge Mateo','Espinoza Vásquez','Trujillo','925800123','jorespinoza@gmail.com','Activo','S0003'),
	('C0002','60204500','Maria Mia','Carmona Requejo','Trujillo','920145009','marimiacar@gmail.com','Activo','S0003'),
	('C0003','18158073','Carlos Francisco','Zambrano Usquiza','Lima','987654323','carloszambra@gmail.com','Activo','S0004'),
	('C0004','80157430','Ana Paola','Llauri Flores','Cusco','992701465','anallauri@gmail.com','Activo','S0006'),
	('C0005','63245508','Salvatore Marco','Castilla Zepia','Tumbes','940756331','salvatocasti@gmail.com','Activo','S0001'),
	('C0006','16490245','Martha Liza','López Córdova','Loreto','911503254','marthalopez@gmail.com','Bloqueado','S0002'),
	('C0007','15809924','Darío José','Castañeda Lápiz','Tumbes','932777140','dariocasta@gmail.com','Activo','S0001');

SELECT * FROM CLIENTE;

-- PRESTAMO
CREATE TABLE PRESTAMO(
	idPrestamo CHAR(6) NOT NULL,
	monto DOUBLE NOT NULL CHECK(monto > 500), -- 500 MONTO MINIMO, SI SE GANA EL SUELDO MINIMO QUE ES 1130 
	tasaInteres DOUBLE NOT NULL CHECK(tasaInteres > 0),
	plazoMeses INT NOT NULL,
	fechaPrestamo DATE NOT NULL,
	estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente' CHECK(estado IN ('Pendiente', 'Aprobado','Rechazado','Vigente','Pagado')),
	idCliente CHAR(5) NOT NULL,
    idEmpleado CHAR(5) NOT NULL,
	PRIMARY KEY(idPrestamo),
	FOREIGN KEY(idCliente) REFERENCES CLIENTE(idCliente),
	FOREIGN KEY(idEmpleado) REFERENCES EMPLEADO(idEmpleado)
);
-- PRESTAMO: Estado.- Pendiente, Aprobado, Rechazado, Vigente, Pagado
INSERT INTO PRESTAMO 
VALUES
	('P00001',10000,12.5,24,'2025-02-10','Aprobado','C0001','E0007'),
	('P00002',5000,10.5,12,'2026-03-05','Aprobado','C0002','E0002'),
	('P00003',7000,11.0,18,'2026-06-19','Pendiente','C0003','E0003'),
	('P00004',15000,13.5,36,'2024-05-20','Vigente','C0004','E0003'),
	('P00005',3000,9.5,10,'2026-04-30','Pendiente','C0005','E0002'),
	('P00006',3000,9.5,10,'2026-06-10','Pendiente','C0005','E0007'),
	('P00007',12000,12.0,24,'2025-07-21','Pagado','C0007','E0002');

SELECT * FROM PRESTAMO;


-- CUENTA BANCARIA
CREATE TABLE CUENTA_BANCARIA(
	idCuenta CHAR(6) NOT NULL,
	numeroCuenta VARCHAR(20) NOT NULL UNIQUE,
	tipoCuenta VARCHAR(30) NOT NULL CHECK(tipoCuenta IN ('Ahorros','Corriente')),
	saldo DOUBLE NOT NULL CHECK(saldo >= 0),
	fechaApertura DATE NOT NULL,
	estado VARCHAR(20) NOT NULL DEFAULT 'Activa' CHECK(estado IN ('Activa','Congelada','Cerrada')),
	idCliente CHAR(5) NOT NULL,
	PRIMARY KEY(idCuenta),
	FOREIGN KEY(idCliente) REFERENCES CLIENTE(idCliente)	
);

-- CUENTA BANCARIA: Estado.- Activa, Congelada, Cerrada
INSERT INTO CUENTA_BANCARIA 
VALUES
	('CB0001','19134567890012','Ahorros',3500,'2024-01-10','Activa','C0001'),
	('CB0002','19178901234155','Corriente',8500,'2025-02-19','Activa','C0004'),
	('CB0003','19451234567089','Ahorros',4200,'2023-03-20','Activa','C0003'),
	('CB0004','19101234567011','Corriente',9800,'2024-04-14','Activa','C0002'),
	('CB0005','19398765432145','Ahorros',2600,'2024-05-10','Activa','C0005'),
	('CB0006','19623456789123','Ahorros',2600,'2024-09-08','Congelada','C0006'),
	('CB0007','19345678901022','Corriente',7100,'2024-06-01','Activa','C0007');

SELECT * FROM CUENTA_BANCARIA;


-- TARJETA
CREATE TABLE TARJETA(
	idTarjeta CHAR(6) NOT NULL,
	numeroTarjeta VARCHAR(20) NOT NULL UNIQUE,
	tipoTarjeta VARCHAR(20) NOT NULL CHECK(tipoTarjeta IN ('Débito', 'Crédito')),
	fechaEmision DATE NOT NULL,
	fechaVencimiento DATE NOT NULL,
	estado VARCHAR(20) NOT NULL DEFAULT 'Activa' CHECK(estado IN ('Activa','Bloqueada','Vencida','Cancelada')),
	idCuenta CHAR(6) NOT NULL,
	PRIMARY KEY(idTarjeta),
    CHECK(fechaVencimiento > fechaEmision),
	FOREIGN KEY(idCuenta) REFERENCES CUENTA_BANCARIA(idCuenta)
);

-- TARJETA BANCARIA: Estado.- Activa, Bloqueada, Vencida, Cancelada
INSERT INTO TARJETA 
VALUES
	('T00001','4026111234567819','Débito','2024-01-08','2029-01-08','Activa','CB0001'),
	('T00002','4532751234567812','Débito','2024-04-13','2029-04-13','Activa','CB0002'),
	('T00003','4916123456789017','Crédito','2023-03-29','2027-03-29','Activa','CB0003'),
	('T00004','5412751234123456','Crédito','2025-02-20','2030-02-20','Activa','CB0004'),
	('T00005','6759123456789010','Crédito','2025-06-15','2030-06-15','Activa','CB0005'),
	('T00006','4929111234567814','Débito','2024-05-09','2029-05-09','Activa','CB0005'),
	('T00007','4929444234767910','Débito','2024-05-29','2029-05-29','Activa','CB0007');

SELECT * FROM TARJETA;


-- BENEFICIARIO
CREATE TABLE BENEFICIARIO(
	idBeneficiario CHAR(6) NOT NULL,
	nombres VARCHAR(50) NOT NULL,
	apellidos VARCHAR(50) NOT NULL,
	numeroCuenta VARCHAR(20) NOT NULL UNIQUE,
	bancoDestino VARCHAR(60) NOT NULL,
	PRIMARY KEY(idBeneficiario)
);

INSERT INTO BENEFICIARIO 
VALUES
	('BF0001','Marcos Manolo','Ruiz Gutierrez','00000123456','Banco Nación'),
	('BF0002','Daphne Helena','Guevara Carmona','2003001234567','Interbank'),
	('BF0003','Luis Jorge','Abanato Ludez','001101230200456789','BBVA'),
	('BF0004','Andrea Jimena','Llosa Contreras','0123456789','Scotiabank'),
	('BF0005','Diego Alejandro','Herrera Sánchez','04015987654','Banco Nación'),
	('BF0006','Paola Joaquina','Ríos Profundos','001103450100987654','BBVA'),
	('BF0007','William Joseph','Guevara Carmona','4503109876543','Interbank');

SELECT * FROM BENEFICIARIO;


-- TRANSACCION
-- TIPO DE TRANSACCION: Depósito, Retiro, Transferencia
CREATE TABLE TRANSACCION(
	idTransaccion CHAR(6) NOT NULL,
	tipoTransaccion VARCHAR(30) NOT NULL CHECK(tipoTransaccion IN ('Depósito', 'Retiro', 'Transferencia')),
	monto DOUBLE NOT NULL CHECK(monto > 0),
	fecha DATE NOT NULL,
	descripcion VARCHAR(150),
	idCuenta CHAR(6) NOT NULL,
    idBeneficiario CHAR(6) NULL, -- Null para Depósitos y Retiros
	PRIMARY KEY(idTransaccion),
	FOREIGN KEY(idCuenta) REFERENCES CUENTA_BANCARIA(idCuenta),
    FOREIGN KEY(idBeneficiario) REFERENCES BENEFICIARIO(idBeneficiario)
);

INSERT INTO TRANSACCION 
VALUES
	('TR0001','Retiro',500,'2025-06-01','Depósito en efectivo','CB0001', NULL),
	('TR0002','Depósito',300,'2026-02-26','Retiro por ventanilla','CB0002', NULL),
	('TR0003','Transferencia',800,'2025-06-03','Transferencia bancaria','CB0003','BF0003'),
	('TR0004','Depósito',1200,'2025-06-04','Depósito por agente','CB0004', NULL),
	('TR0005','Retiro',600,'2025-06-05','Retiro en cajero','CB0005', NULL),
	('TR0006','Retiro',600,'2025-06-05','Retiro en cajero','CB0005', NULL),
	('TR0007','Transferencia',950,'2025-06-06','Transferencia interbancaria','CB0007','BF0002');

SELECT * FROM TRANSACCION;






