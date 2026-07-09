import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

# CONSEJO: Instalar librería scikit-learn con pip install scikit-learn
class FiltroAntifraude:
    # MACHINE LEARNING
    _PaquitoNuevasAmericasBank_ia = None  

    @classmethod
    def entrenar_cerebro(cls):
        """
        Entrena el modelo de IA con el historial del banco
        """
        if cls._PaquitoNuevasAmericasBank_ia is not None:
            return

        datos_historicos = [
            [100.00, 1, 1500.00, 10], [50.00,  0, 1600.00, 14],
            [300.00, 2, 2500.00, 11], [20.00,  1, 1200.00, 16],
            [150.00, 2, 4000.00, 9],  [80.00,  1, 850.00,  12],
            [500.00, 0, 5000.00, 15],
            [4500.00, 2, 4700.00, 3], [8000.00, 1, 8200.00, 2],
            [3500.00, 2, 3600.00, 4]
        ]
        etiquetas = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

        X_train = pd.DataFrame(datos_historicos, columns=['monto', 'tipo', 'saldo', 'hora'])
        y_train = etiquetas

        # Nombre propio para el algoritmo
        cls._PaquitoNuevasAmericasBank_ia = RandomForestClassifier(n_estimators=10, random_state=42)
        cls._PaquitoNuevasAmericasBank_ia.fit(X_train, y_train)

    @classmethod
    def es_operacion_sospechosa(cls, monto: float, tipo_texto: str, saldo_cuenta: float) -> tuple[float, str]:
        """
        Analiza el comportamiento financiero y define si se bloquea o no.
        """
        cls.entrenar_cerebro()
        hora_actual = datetime.now().hour

        tipo_codificado = 0
        if tipo_texto == 'Retiro':
            tipo_codificado = 1
        elif tipo_texto == 'Transferencia':
            tipo_codificado = 2

        nueva_transaccion = pd.DataFrame([[monto, tipo_codificado, saldo_cuenta, hora_actual]], 
                                         columns=['monto', 'tipo', 'saldo', 'hora'])
        
        probabilidades = cls._PaquitoNuevasAmericasBank_ia.predict_proba(nueva_transaccion)[0]
        probabilidad_fraude = float(probabilidades[1] * 100)

        veredicto = "BLOQUEADO" if probabilidad_fraude >= 75.0 else "APROBADO"
        return probabilidad_fraude, veredicto



    
