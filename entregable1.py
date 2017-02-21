# -*- coding: utf-8 -*-
# ============================================================================
# Inteligencia Artificial. Universidad de La Rioja.
# Curso 2016-2017.
# Nombre y apellidos: Borja Jimeno Soto
# =============================================================================

# ==============================================================================
# Entregable 1. Búsqueda en espacios de estados
# ==============================================================================

# Escribir el código Python de las funciones que se piden en el
# espacio que se indica en cada ejercicio.

# IMPORTANTE: NO CAMBIAR EL NOMBRE NI A ESTE ARCHIVO NI A LAS FUNCIONES QUE SE
# PIDEN (aquellas funciones con un nombre distinto al que se pide en el
# ejercicio NO se corregirán).


# ==============================================================================
# DESCRIPCIÓN DEL PROBLEMA
# ==============================================================================

# La tripulación de la nave Planet Express ha realizado con exito la entrega
# en el planeta Omicron Persei 8, y ahora debes ayudar a Leela, Fry y Bender
# a volver sanos y salvos a casa. Para ello deberás emplear técnicas de
# búsqueda en espacio de estados, el llamado problema de "viaje espacial".
# En este problema, Leela introduce en el ordenador de la nave una configuración
# del espacio, formado por una rejilla de casillas, algunas de ellas ocupadas
# por un asteroide. Inicialmente, en una de las casillas libres está situada
# la nave de Planet Expre99ss que tiene tres posibles movimientos: avanzar, girar
# a la derecha, y girar a la izquierda (aunque al movernos por el espacio podríamos
# avanzar en tres dimensiones, aquí simplificamos el viaje a dos). Por supuesto
# la nave sólo puede moverse a casillas que no tengan asteroides y al girar se
# mantiene en la misma casilla.
# La nave tiene 4 posibles orientaciones U,D,L,R que corresponden a
# (Up, Down, Left y Right). El coste de girar a derecha o izquierda es de una
# unidad de materia oscura y el de avanzar es de dos unidades de materia oscura.
# El objetivo final es encontrar una secuencia de movimientos para la nave,
# de manera que llegue a la tierra (la orientación al llegar a la tierra de la nave
# no es relevante).

# Por ejemplo, un espacio podría ser algo así, siendo "D" la posición de
# la nave indicado su orientación, H la posición de la tierra, y "*" las
# casillas con asteroide:

# ********
# *      *
# *   D  *
# * **** *
# * *    *
# * * ****
# *H*    *
# ********

# Una posible solución sería:

# Girar Derecha -> Avanzar -> Avanzar -> Avanzar -> Girar Izquierda ->
# Avanzar -> Avanzar -> Avanzar -> Avanzar

# -------------------------------------------------------------------------
# PROBLEMAS DE ESPACIOS DE ESTADO Y BÚSQUEDA
# -------------------------------------------------------------------------

# Como primer paso debes cargar los módulos busqueda.py y problema.py
# desarrollados en las prácticas 3 y 4.

import busqueda
import problema as p


# -------------------------------------------------------------------------
# LECTURA DE ESPACIOS EN FICHEROS
# -------------------------------------------------------------------------

# Los ficheros espaciox.txt, con x=1,...,5, contienen una representación
# gráfica de cinco espacios de ejemplo. Estos ficheros de texto contienen
# una primera línea con las dimensiones del espacio (en la dimensión no
# contamos los bordes del espacio) y en las siguientes líneas se incluye la
# representación gráfica.

# Define la siguiente función para leer un espacio de un fichero y cargar
# toda la información en una estructura de datos:


def lee_espacio(fichero):
    """
    Lee de un fichero de texto en el que está representado
           el espacio y devuelve una tupla (dim,mat,posI,posF) donde:
           - dim es una tupla (n,m) donde n es el número de filas del espacio
             y m el número de columnas (sin contar los bordes).
           - mat es una matriz nxm (en forma de lista de listas) en la que su
             componente mat[i][j] es 0 si en la casilla (i,j) no hay obstáculo
             y 1 si hay obstáculo.
           - posI es una tupla ((x,y),O), donde (x,y) son las coordenadas de la posición
             inicial de la nave (las coordenadas empiezan a contar en el 0) y O es
             la orientación de la nave.
            - posF es una tupla (x,y) con las coordenadas de la posición de casa
    """
    with open(fichero) as ficheroAbierto:
        componentes = ficheroAbierto.readline().split()
        dim = (componentes[0], componentes[1])
        mat = []
        i = -1
        encontrado = False
        for line in ficheroAbierto:
            print line
            l = [1 if x == '*' else 0 for x in line]
            mat.append(l[1:-2])
            if not encontrado:
                if line.find("H") > -1:
                    posF = (line.find("H")-1, i)
                for x in ["U", "D", "L", "R"]:
                    if line.find(x) > -1:
                        posI = ((line.find(x)-1, i), x)
            i += 1
    return tuple(dim, mat[1:-1], posI, posF)


# Ejemplo de uso (en espacio1.txt está el laberinto del ejemplo anterior):
# >>> esp1=lee_espacio("espacio1.txt")
# >>> esp1
# ((6, 6),
# [[0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0],
#  [0, 1, 1, 1, 1, 0],
#  [0, 1, 0, 0, 0, 0],
#  [0, 1, 0, 1, 1, 1],
#  [0, 1, 0, 0, 0, 0]],
# ((5, 0), 'L'),
# (5, 5))


# -------------------------------------------------------------------------
# IMPLEMENTACIÓN DEL PROBLEMA
# -------------------------------------------------------------------------

# Implementar una clase Viaje_Espacial (¡ojo, con ese nombre!), que
# represente el problema de "viaje espacial".
# Esta clase DEBE SER SUBCLASE de la clase Problema y su constructor recibe
# como argumento una estructura de las que se obtienen al leer el espacio de
# un fichero (por ejemplo, como la variable esp1 del ejemplo anterior).

class Viaje_Espacial(p.Problema):
    def __init__(self, espacio):
        super(Viaje_Espacial, self).__init__(estado_inicial=espacio.index(2), estado_final=espacio[3])
        self.mapa = espacio.index(1)


    def acciones(self, estado):
        x = estado.index(2).index(0).index(0)
        y = estado.index(2).index(0).index(1)
        o = estado.index(2).index(1)
        xmax = estado.index(0).index(0)
        ymax = estado.index(0).index(1)
        accs = list()
        accs.add("GirarDerecha")
        accs.add("GirarIzquierda")
        if o == "U":
            if y < ymax and self.mapa[x][y+1] == 0:
                accs.add("Avanzar")
        elif o == "D":
            if y > 0 and self.mapa[x][y-1] == 0:
                accs.add("Avanzar")
        elif o == "R":
            if x < xmax and self.mapa[x+1][y] == 0:
                accs.add("Avanzar")
        else:  # o == "L"
            if x > 0 and self.mapa[x-1][y] == 0:
                accs.add("Avanzar")
        return accs

    def aplica(self, estado, accion):
        pos = [x for x in estado.index(0)]
        o = estado.index(1)
        if accion == "GirarDerecha":
            if o == "U":
                o = "R"
            elif o == "R":
                o = "D"
            elif o == "D":
                o = "L"
            else:  # o == "L"
                o = "U"
        elif accion == "GirarIzquierda":
            if o == "U":
                o = "L"
            elif o == "L":
                o = "D"
            elif o == "D":
                o = "R"
            else:  # o == "R"
                o = "U"
        elif accion == "Avanzar":
            if o == "U":
                pos[1] += 1
            elif o == "R":
                pos[0] += 1
            elif o == "D":
                pos[1] -= 1
            else:  # o == "L"
                pos[0] -= 1

    def es_estado_final(self, estado):
        return estado.index(0) == self.estado_final.index(0)


# -------------------------------------------------------------------------
# Heurísticas
# -------------------------------------------------------------------------

# Definir dos heurísticas para este problema. Las dos funciones heurísticas
# deben de llamarse, respectivamente h1_viaje_espacial y h2_viaje_espacial
# y pueden depender del problema concreto.

def h1_viaje_espacial(problema):
    pass


def h2_viaje_espacial(problema):
    pass


# -------------------------------------------------------------------------
# Experimentando
# -------------------------------------------------------------------------

# Define una función que dado un espacio (con la estructura de datos vista
# anteriormente), un algoritmo y una heurística (sólo si esta es necesaria
# para el algoritmo de búsqueda) calcule la solución para el espacio dado
# utilizando el algoritmo de búsqueda y la heuristica dadas. Para este
# ejercicio puede ser útil que recuperes la clase Problema_con_Analizados
# vista en las prácticas 3 y 4.

def recorridoYcoste(espacio, algoritmo, h=None):
    pass

# Utilizando la función anterior busca soluciones a los distintos laberintos
# de los ejemplos, usando para ello las implementaciones de los distintos
# algoritmos de búsqueda.

# IMPORTANTE:
# * Se valorará que las soluciones obtenidas sean de longitud mínima
#   (suponemos que mordisquitos no se encuentra en la nave en este momento,
#   y por lo tanto el combustible a nuestra disposición es limitado),
#   que se encuentren analizando cuantos menos nodos mejor y que tengan
#   el menor coste posible.

# Indica a continuación los resultados que has obtenido para cada uno de los
# espacios.

# Espacio 1:
#   - Longitud solución:
#   - Nodos analizados:
#   - Coste:
#   - Algoritmo empleado (y heurística):

# Espacio 2:
#   - Longitud solución:
#   - Nodos analizados:
#   - Coste:
#   - Algoritmo empleado (y heurística):

# Espacio 3:
#   - Longitud solución:
#   - Nodos analizados:
#   - Coste:
#   - Algoritmo empleado (y heurística):

# Espacio 4:
#   - Longitud solución:
#   - Nodos analizados:
#   - Coste:
#   - Algoritmo empleado (y heurística):

# Espacio 5:
#   - Longitud solución:
#   - Nodos analizados:
#   - Coste:
#   - Algoritmo empleado (y heurística):

# -------------------------------------------------------------------------
# Comprobando tus soluciones
# -------------------------------------------------------------------------

# Al igual que en las prácticas dispones en el aula virtual de un fichero
# llamado testEntregable1.py para comprobar si has realizado correctamente
# los distintos apartados.

# -------------------------------------------------------------------------
# Extensiones
# -------------------------------------------------------------------------

# Se proponen las siguientes extensiones a este trabajo para subir nota:
# - Añadir nuevos tests.
# - Generador de mapas aleatorio.
# - Incluir otros mapas.
# - Añadir otras heurísticas.
# - Visualizador gráfico de las soluciones encontradas. 
# - Crear una pequeña interfaz de línea de comandos para interactuar
#   con este programa.
# - Usar Python Qt (u otra herramienta similar) para crear una interfaz
#   gráfica.
# - Cualquier otra mejora que se te pueda ocurrir.
#
# Todas las mejoras que introduzcas, deben ser documentadas a continuación.




# ==========================================================================
# Entregable
# ==========================================================================

# Guarda este fichero con tus soluciones a los distintos apartados,
# introduciendo tu nombre al principio del mismo. Deberás entregar en un zip
# este fichero junto a los ficheros problema.py, testEntregable1.py y
# busqueda.py. Si has introducido alguna extensión en tu programa que haya
# supuesto desarrollar nuevos ficheros, dichos ficheros deberán también ir
# incluidos en el fichero zip. 


# ==========================================================================
