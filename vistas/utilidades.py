def leer_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Debe ingresar un número válido.")


def leer_int(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero.")


def mostrar_lista(elementos: list) -> None:
    if len(elementos) == 0:
        print("No hay registros para mostrar.")
    else:
        for elemento in elementos:
            print(elemento)
