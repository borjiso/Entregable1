# -*- coding: utf-8 -*-
# Inteligencia Artificial. Universidad de La Rioja.
# Curso 2016-2017.
# Nombre y apellidos:

#======================================================================================
# Práctica 3. Búsqueda en espacios de estados
#======================================================================================

# -------------------------------------------------------------------------------------
# Auxiliar: colas y pilas
# -------------------------------------------------------------------------------------

class Cola:
    """Clase abstracta/interfaz para colas de dos tipos:
        PilaLIFO(): Pilas
        ColaFIFO(): Colas.
    Cualquiera de ellos soporta los siguientes métodos y funciones:
        q.append(item)  -- incluir un elemento en la cola q
        q.extend(items) -- equivalente a: for x in items: q.append(x)
        q.pop()         -- devuelve (y lo quita) el primero de la cola
        len(q)          -- número de elementos en q
        item in q       -- responde a la pregunta ¿item está en q?

    En el caso particular de PilaLIFO(), no será una instance de Cola, ya que
    directamente usaremos listas. La otra sí será definida como subclase
    de esta clase Cola."""

    def __init__(self):
        pass

    def extend(self, items):
        for item in items: self.append(item)


def PilaLIFO():
    """Devuelve la lista vacía, que tomaremos como una pila LIFO vacía."""
    return []


class ColaFIFO(Cola):
    """Definición de colas 'primero que entra, primero que sale'.  Se usan
    listas y la cola que representan es la que se forma si se recorre la lista
    de izquierda a derecha. Para eliminar un elemento de la cola, simplemente
    consideramos que el inicio de la cola cambia a la siguiente posición a la
    derecha. Para ello, llevamos un contador con el índice que indica el
    comienzo de la cola, y lo incrementaremos cuando se hace pop().  A partir de
    cinco, eliminamos la "basura" cuando más de la mitad de la lista esté
    eliminada (para ello, reemplazamos la lista por la sublista de los
    elementos "vivos")."""

    def __init__(self):
        self.A = []
        self.comienzo = 0

    def append(self, item):
        self.A.append(item)

    def __len__(self):
        return len(self.A) - self.comienzo

    def extend(self, items):
        self.A.extend(items)

    def pop(self):
        e = self.A[self.comienzo]
        self.comienzo += 1
        if self.comienzo > 5 and self.comienzo > len(self.A) / 2:
            self.A = self.A[self.comienzo:]
            self.comienzo = 0
        return e

    def __contains__(self, item):
        return item in self.A[self.comienzo:]

    def __str__(self):
        return str(self.A[self.comienzo:])


# -------------------------------------------------------------------------------------
# Nodos de búsqueda
# -------------------------------------------------------------------------------------

# Según lo visto en clase, la generación de los aŕboles de búsqueda en
# espacios de estado se hace a través de lo que llamamos nodo de búsqueda. La
# siguiente clase implementa los nodos de búsqueda:

class Nodo:
    """Nodos de un árbol de búsqueda. Un nodo se define como:
       - Un estado
       - Un puntero al estado desde el que viene (padre)
       - La acción que se ha aplicado al padre para que se obtenga el
         estado del nodo
       - Profundidad del nodo
       - Coste del camino desde el estado inicial hasta el nodo.

       Definimos además, entre otros, los siguientes métodos que se
       necesitarán para generar el aŕbol de búsqueda:
       - Sucesor y sucesores de un nodo (respesctivamente por una acción
         o por todas las acciones aplicables al estado del nodo). Estos
         métodos reciben como entrada un  problema de espacio de estados.
       - Camino (secuencia de nodos) que lleva del estado inicial al estado del
         nodo.
       - Solución (secuencia de acciones que llevan al estado) de un nodo.
       """

    def __init__(self, estado, padre=None, accion=None):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.profundidad = 0
        if padre:
            self.profundidad = padre.profundidad + 1

    def __repr__(self):
        return "<Nodo {0}>".format(self.estado)

    def sucesor(self, problema, accion):
        """Sucesor de un nodo por una acción aplicable"""
        estado_suc = problema.aplica(self.estado, accion)
        return Nodo(estado_suc, self, accion)

    def sucesores(self, problema):
        """Lista de los nodos sucesores por todas las acciones que le sean
           aplicables"""
        return [self.sucesor(problema, accion)
                for accion in problema.acciones(self.estado)]

    def camino(self):
        """Lista de nodos que forman el camino desde el inicial hasta el
           nodo."""
        nodo_aux, camino_inverso = self, []
        while nodo_aux:
            camino_inverso.append(nodo_aux)
            nodo_aux = nodo_aux.padre
        return list(reversed(camino_inverso))

    def solucion(self):
        """Secuencia de acciones desde el nodo inicial"""
        return [nodo.accion for nodo in self.camino()[1:]]

    def __eq__(self, other):
        """ Dos nodos son iguales si sus estados son iguales. Esto significa que
        cuando comprobemos pertenecia a una lista o a un conjunto (con"in"), sólo
        miramos los estados. Si hay que mirar, por ejemplo, algo del coste,
        habrá que hacerlo expresamente, como se hará en la
        buśqueda_con_prioridad"""

        return isinstance(other, Nodo) and self.estado == other.estado

    def __lt__(self, other):
        """La definición del menor entre nodos se necesita porque cuando se
        introduce un nodo en la cola de prioridad, con la misma valoración que
        uno ya existente, se van a comparar los nodos y por tanto es necesario que
        esté definido el operador <"""
        return True

    def __hash__(self):
        """Nótese que esta definición obliga a que los estados sean de un tipo
        de dato hashable"""
        return hash(self.estado)

# -------------------------------------------------------------------------------------
# Algoritmo genérico de búsqueda
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Ejercicio 3.1.
# -------------------------------------------------------------------------------------

# Completa el siguiente algoritmo utilizando lo que hemos
# visto en clase

def busqueda_generica(problema, abiertos):
    """Búsqueda genérica, tal y como se ha visto en clase; aquí
    abiertos es una cola que se puede gestionar de varias maneras.
    Cuando se llama a la función, el argumento abiertos debe ser la cola
    vacía. """

    # 1. Añade a abiertos un nodo con el estado_inicial de problema
    abiertos.append(Nodo(problema.estado_inicial))

    # 2. Inicializa cerrados como el conjunto vacío.
    cerrados = set()
    while abiertos:
        # 3. Hacer actual el primer nodo de abiertos
        actual = abiertos.pop()

        # 4. Comprobar si el estado actual es final
        if problema.es_estado_final(actual.estado):
            return actual

        # 5. Añadir a cerrados el estado actual
        cerrados.add(actual.estado)

        nuevos_sucesores=(sucesor for sucesor in actual.sucesores(problema)
                          if sucesor.estado not in cerrados
                          and sucesor not in abiertos)
        # 6. Extiende actual con los nuevos sucesores
        abiertos.extend(nuevos_sucesores)
    return None

# -------------------------------------------------------------------------------------
# Búsquedas en anchura y en profundidad
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Ejercicio 3.2.
# -------------------------------------------------------------------------------------

# Usando la búsqueda genérica, implementa los algoritmos
# de búsqueda_en_anchura y búsqueda_en_profundidad.


def busqueda_en_profundidad(problema):
    return busqueda_generica(problema, PilaLIFO())

def busqueda_en_anchura(problema):
    return busqueda_generica(problema, ColaFIFO())

# -------------------------------------------------------------------------------------
# Ejercicio 3.3.
# -------------------------------------------------------------------------------------

# Implementa las estrategias de búsqueda en profundidad
# acotada y la búsqueda en profundidad iterativa.

def busqueda_en_profundidad_acotada(problema,cota):
    # 1. Añade a abiertos un nodo con el estado_inicial de problema
    abiertos=PilaLIFO()
    abiertos.append(Nodo(problema.estado_inicial))

    # 2. Inicializa cerrados como el conjunto vacío.
    cerrados = set()

    while abiertos:
        # 3. Hacer actual el primer nodo de abiertos
        actual = abiertos.pop()

        # 4. Comprobar si el estado actual es final
        if problema.es_estado_final(actual.estado):
            return actual

        # 5. Añadir a cerrados el estado actual
        cerrados.add(actual.estado)
        if len(actual.camino())<cota:
            nuevos_sucesores = (sucesor for sucesor in actual.sucesores(problema)
                                if sucesor.estado not in cerrados
                                and sucesor not in abiertos)
            # 6. Extiende actual con los nuevos sucesores
            abiertos.extend(nuevos_sucesores)
    return None

def busqueda_en_profundidad_iterativa(problema,cota_inicial):
    n=cota_inicial
    terminado = False
    while not terminado:
        resultado=busqueda_en_profundidad_acotada(problema,n)
        if resultado is not None:
            return resultado
        n+=1
