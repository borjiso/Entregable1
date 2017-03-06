# -*- coding: utf-8 -*-
# Inteligencia Artificial. Universidad de La Rioja.
# Curso 2016-2017.
# Nombre y apellidos:

#=========================================================
# Práctica 3. Búsqueda en espacios de estados
#=========================================================

#---------------------------------------------------------
# Representación de un problema de espacio de estados
#---------------------------------------------------------

# Recuérdese que según lo que se ha visto en clase, la
# implementación de la representación de un problema de
# espacio de estados consiste en:
# * Representar estados y acciones mediante una estructura
#   de datos.
# * Definir: estado_inicial, es_estado_final(_), acciones(_),
#   y aplica(_,_).

# La siguiente clase Problema representa este esquema general
# de cualquier problema de espacio de estados. Un problema
# concreto será una subclase de Problema, y requerirá
# implementar acciones, aplica y eventualmente __init__, y
# es_estado_final.

class Problema(object):
    """Clase abstracta para un problema de espacio de estados.
     Los problemas concretos habría que definirlos como
     subclases de Problema, implementando acciones, aplica
     y eventualmente __init__, y es_estado_final. Una vez
     hecho esto, se han de crear instancias de dicha subclase,
     que serán la entrada a los distintos algoritmos de
     resolución mediante búsqueda."""

    def __init__(self, estado_inicial, estado_final=None):
        """El constructor de la clase especifica el estado
         inicial y puede que un estado_final, si es que es
         único. Las subclases podrían añadir otros argumentos"""

        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

    def acciones(self, estado):
        """Devuelve las acciones aplicables a un estado dado.
         Lo normal es que aquí se devuelva una lista, pero si
         hay muchas se podría devolver un iterador, ya que
         sería más eficiente."""
        pass

    def aplica(self, estado, accion):
        """ Devuelve el estado resultante de aplicar accion a
         estado. Se supone que accion es aplicable a estado (es
         decir, debe ser una de las acciones de
         self.acciones(estado)."""
        pass

    def es_estado_final(self, estado):
        """Devuelve True cuando estado es final. Por defecto,
        compara con el estado final, si éste se hubiera especificado
        al constructor. Si se da el caso de que no hubiera un único
        estado final, o se definiera mediante otro tipo de comprobación,
        habría que redefinir este método en la subclase."""
        return estado == self.estado_final

    def coste_de_aplicar_accion(self, estado, accion):
        return 1