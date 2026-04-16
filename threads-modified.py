import threading
import random
import time

# Puntos 2 y 3 con implementación del algoritmo del panadero para n hilos

class BakeryLock:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.choosing = [False] * num_threads
        self.number   = [0] * num_threads

    def acquire(self, thread_id):
        #obtención de número
        self.choosing[thread_id] = True
        self.number[thread_id] = max(self.number) + 1
        self.choosing[thread_id] = False

        #espera hasta que sea el turno del hilo
        for other in range(self.num_threads):
            # Espera si el otro hilo está eligiendo número
            while self.choosing[other]:
                pass
            #espera si el otro hilo tiene un número menor o igual con desempate por ID
            while (self.number[other] != 0 and
                   (self.number[other] < self.number[thread_id] or
                    (self.number[other] == self.number[thread_id] and other < thread_id))):
                pass

    def release(self, thread_id):
        self.number[thread_id] = 0


class Jarra:
    def __init__(self, capacidad, bakery_lock):
        self.aguaDisponible = capacidad
        self.bakery = bakery_lock

    def beber(self, cantidad, nombre, thread_id):
        self.bakery.acquire(thread_id)
        try:
            if self.aguaDisponible >= cantidad:
                print(f"{nombre} está bebiendo {cantidad} ml de agua.")
                self.aguaDisponible -= cantidad
                print(f"Agua restante: {self.aguaDisponible} ml\n")
                return True
            else:
                print(f"{nombre} quiso beber {cantidad} ml, pero no hay suficiente agua.\n")
                return False
        finally:
            self.bakery.release(thread_id)

    def recargar(self, cantidad, thread_id):
        self.bakery.acquire(thread_id)
        try:
            self.aguaDisponible += cantidad
            print(f"Reabastecedor añadió {cantidad} ml. Nuevo nivel: {self.aguaDisponible} ml\n")
        finally:
            self.bakery.release(thread_id)


class Persona(threading.Thread):
    def __init__(self, nombre, jarra, thread_id):
        super().__init__()
        self.nombre = nombre
        self.jarra = jarra
        self.thread_id = thread_id

    def run(self):
        cantidad = random.randint(100, 300)
        time.sleep(random.uniform(0.1, 1.0))   #simula tiempo de llegada
        self.jarra.beber(cantidad, self.nombre, self.thread_id)

class Reabastecedor(threading.Thread): #punto 3
    def __init__(self, jarra, agua_minima, cantidad_recarga, thread_id):
        super().__init__()
        self.jarra = jarra
        self.thread_id = thread_id
        self.agua_minima = agua_minima
        self.cantidad_recarga = cantidad_recarga        
        self.ejecutando = True

    def run(self):
        while self.ejecutando:
            time.sleep(2)  #espera 2 segundos
            if self.jarra.aguaDisponible < self.agua_minima:
                self.jarra.aguaDisponible += self.cantidad_recarga
                print(f"Reabastecedor añadió {self.cantidad_recarga} ml. "
                     f"Nuevo nivel: {self.jarra.aguaDisponible} ml\n")

    def detener(self):
        self.ejecutando = False

#Simulación principal

if __name__ == "__main__":
    NUM_PERSONAS = 5
    NUM_HILOS_TOTAL = NUM_PERSONAS + 1   #personas+reabastecedor

    #crear el lock del bakery para todos los hilos
    bakery = BakeryLock(NUM_HILOS_TOTAL)

    #crear la jarra compartida
    jarra = Jarra(1000, bakery)

    #crear los hilos de personas
    personas = []
    for i in range(NUM_PERSONAS):
        p = Persona(f"Persona-{i+1}", jarra, thread_id=i)
        personas.append(p)

    #crear el hilo reabastecedor (ID = NUM_PERSONAS)
    reabastecedor = Reabastecedor(jarra, 200, 150, thread_id=NUM_PERSONAS)

    #iniciar los hilos
    reabastecedor.start()
    for p in personas:
        p.start()

    #esperar a que todas las personas terminen
    for p in personas:
        p.join()

    #detener el reabastecedor pq sino se queda ahí camellando
    reabastecedor.detener()
    reabastecedor.join()

    print("Simulación finalizada")