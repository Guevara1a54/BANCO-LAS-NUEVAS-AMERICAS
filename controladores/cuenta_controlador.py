from dao.cuenta_bancaria_dao import CuentaBancariaDAO
from dao.cliente_dao import ClienteDAO
from modelos.cuenta_bancaria import CuentaBancaria


class CuentaControlador:
    @classmethod
    def registrar(cls, idCuenta: str, numeroCuenta: str, tipoCuenta: str, saldo: float, fechaApertura: str, estado: str, idCliente: str) -> bool:
        cliente = ClienteDAO.buscar_por_id(idCliente)
        if cliente is None:
            return False
        
        cuenta = CuentaBancaria(idCuenta, numeroCuenta, tipoCuenta, saldo, fechaApertura, estado, cliente)
        return CuentaBancariaDAO.insertar(cuenta) > 0

    @classmethod
    def listar(cls) -> list[CuentaBancaria]:
        return CuentaBancariaDAO.seleccionar()

    @classmethod
    def buscar(cls, idCuenta: str) -> CuentaBancaria | None:
        return CuentaBancariaDAO.buscar_por_id(idCuenta)

    @classmethod
    def modificar(cls, idCuenta: str, numeroCuenta: str, tipoCuenta: str, saldo: float, fechaApertura: str, estado: str, idCliente: str) -> bool:
        cliente = ClienteDAO.buscar_por_id(idCliente)
        if cliente is None:
            return False
            
        cuenta = CuentaBancaria(idCuenta, numeroCuenta, tipoCuenta, saldo, fechaApertura, estado, cliente)
        return CuentaBancariaDAO.actualizar(cuenta) > 0

    @classmethod
    def eliminar(cls, idCuenta: str) -> bool:
        return CuentaBancariaDAO.eliminar(idCuenta) > 0

    @classmethod
    def depositar(cls, idCuenta: str, monto: float) -> bool:
        if monto <= 0:
            return False
        cuenta = CuentaBancariaDAO.buscar_por_id(idCuenta)
        if cuenta is None or cuenta.estado.lower() != "Activo":
            return False
            
        cuenta.saldo += monto
        return CuentaBancariaDAO.actualizar(cuenta) > 0

    @classmethod
    def retirar(cls, idCuenta: str, monto: float) -> bool:
        if monto <= 0:
            return False
        cuenta = CuentaBancariaDAO.buscar_por_id(idCuenta)
        if cuenta is None or cuenta.estado.lower() != "Activo" or cuenta.saldo < monto:
            return False
            
        cuenta.saldo -= monto
        return CuentaBancariaDAO.actualizar(cuenta) > 0

    @classmethod
    def transferir(cls, idCuentaOrigen: str, idDestino: str, monto: float) -> bool:
        if monto <= 0:
            return False
            
        cuenta_origen = CuentaBancariaDAO.buscar_por_id(idCuentaOrigen)
        if cuenta_origen is None or cuenta_origen.saldo < monto:
            return False
            
        # Intentamos buscar si la cuenta destino es interna del banco
        cuenta_destino = CuentaBancariaDAO.buscar_por_id(idDestino)
        
        if cuenta_destino is not None:
            # Transferencia interna 
            cuenta_origen.saldo -= monto
            cuenta_destino.saldo += monto
            # Actualizaciones en la BD
            res1 = CuentaBancariaDAO.actualizar(cuenta_origen) > 0
            res2 = CuentaBancariaDAO.actualizar(cuenta_destino) > 0
            return res1 and res2
        else:
            # Si no es cuenta interna, verificamos si es un beneficiario externo registrado
            from dao.beneficiario_dao import BeneficiarioDAO
            beneficiario = BeneficiarioDAO.buscar_por_id(idDestino)
            if beneficiario is not None:
                # Se debita de la cuenta de origen (Simulación interbancaria)
                cuenta_origen.saldo -= monto
                return CuentaBancariaDAO.actualizar(cuenta_origen) > 0
                
        return False

    @classmethod
    def obtener_historial(cls, idCuenta: str) -> list:
        return []

    @classmethod
    def procesar_operacion_segura(cls, idCuenta: str, tipo_operacion: str, monto: float) -> tuple[bool, str, float]:
        """
        Método de negocio avanzado. Evalúa con Inteligencia Artificial antes de operar en la BD.
        Retorna: (OperacionExitosa, MensajeEstado, PorcentajeFraude)
        """
        from controladores.guardian_fraudes import IAFraudDetector

        cuenta = CuentaBancariaDAO.buscar_por_id(idCuenta)
        if cuenta is None:
            return False, "Cuenta no encontrada.", 0.0
        if cuenta.estado.strip().capitalize() != "Activo":
            return False, f"Operación rechazada. La cuenta está: {cuenta.estado}.", 0.0

        # 1. PASAR POR EL FILTRO DE LA INTELIGENCIA ARTIFICIAL
        prob_fraude, veredicto = IAFraudDetector.evaluar_transaccion(monto, tipo_operacion, cuenta.saldo)

        if veredicto == "BLOQUEADO":
            # CIBERSEGURIDAD: Bloqueo inmediato y congelamiento en BD
            cuenta.estado = "Congelada"
            CuentaBancariaDAO.actualizar(cuenta)
            return False, "ESTA TRANSACCIÓN HA SIDO BLOQUEADA POR FRAUDE. Tu cuenta ha sido congelada por seguridad.", prob_fraude

        # 2. SI ES SEGURO, CONTINUAR CON LA LÓGICA DE NEGOCIO EN BD
        if tipo_operacion == "Depósito":
            cuenta.saldo += monto
        elif tipo_operacion == "Retiro" or tipo_operacion == "Transferencia":
            if cuenta.saldo < monto:
                return False, "Fondos insuficientes.", prob_fraude
            cuenta.saldo -= monto

        # Salvar cambios reales en MySQL
        exito = CuentaBancariaDAO.actualizar(cuenta) > 0
        return exito, "Transacción aprobada y procesada con éxito.", prob_fraude
    
