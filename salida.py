from os import path

class Salida: 
    def __init__(self, mensaje):
        with open(path.join("datos", "salida.csv"), mode="a+") as file:
            file.write(str(mensaje) + '\n')

if __name__ == "__main__":
    l = Salida("Hola.. estamos en septiembre 2024")