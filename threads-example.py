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


# Simulación
jarra = Jarra(1000)
personas = [Persona(f"Persona-{i+1}", jarra) for i in range(5)]
for p in personas:
p.start()
for p in personas:
p.join()

#Acá acaba el código base, solo lo copiamos y pegamos del enunciado del taller
