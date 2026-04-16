# Esta parte de acá es la que se dio de base en el taller, está sin modificar ni nada

import threading
import random
import time
class Jarra:
    def init (self, capacidad):
        self.aguaDisponible = capacidad
        self.lock = threading.Lock() # Sección crítica protegida

    def beber(self, cantidad, nombre):
        with self.lock:
            if self.aguaDisponible >= cantidad:
                print(f"{nombre} está bebiendo {cantidad} ml de agua.")
                self.aguaDisponible -= cantidad
                print(f"Agua restante: {self.aguaDisponible} ml\n")
            else:
                print(f"{nombre} quiso beber {cantidad} ml, pero no hay
                suficiente agua.\n")


class Persona(threading.Thread):
    def init (self, nombre, jarra):
    super(). init ()
    self.nombre = nombre
    self.jarra = jarra

    def run(self):
        cantidad = random.randint(100, 300)
        time.sleep(random.uniform(0.1, 1.0)) # Simula tiempo de llegada
        self.jarra.beber(cantidad, self.nombre)

#Acá acaba el código base, solo lo copiamos y pegamos del enunciado del taller

#Punto 3
class Reabastecedor(threading.Thread):
    def __init__(self, jarra, agua_minima, cantidad_recarga): #uno le pasa la cantidad de agua minima con la cual activarse
        super().__init__()
        self.jarra = jarra
        self.ejecutando = True

    def run(self):
        while self.ejecutando:
            time.sleep(2)  #espera 2 segundos
            with self.jarra.lock: #adquirir el lock de la jarra antes de leer/modificar
                if self.jarra.aguaDisponible < agua_minima:
                    self.jarra.aguaDisponible += cantidad_recarga
                    print("Reabastecedor añadió {cantidad_recarga} ml. "
                          f"Nuevo nivel: {self.jarra.aguaDisponible} ml\n")

    def detener(self):
        self.ejecutando = False

# Simulación (del profe)
jarra = Jarra(1000)
personas = [Persona(f"Persona-{i+1}", jarra) for i in range(5)]

reabastecedor = Reabastecedor(jarra) #linea para el punto 3
reabastecedor.start() #linea para el punto 3

for p in personas:
p.start()
for p in personas:
p.join()

reabastecedor.detener()
reabastecedor.join()