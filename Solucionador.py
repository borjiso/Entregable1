from entregable1 import*
from busqueda import*
if __name__ == "__main__":
    print "Introduzca los ficheros que contienen los mapas"
    ficheros = "espacio1.txt"
    listaFicheros = ficheros.split(" ")
    for fichero in listaFicheros:
        problema = lee_espacio(fichero)
        for algoritmo in [busqueda_primero_el_mejor,busqueda_a_estrella]:
            for heuristica in[h1_viaje_espacial(Viaje_Espacial(problema)),h2_viaje_espacial(Viaje_Espacial(problema))]:
                recorridoYcoste(problema,algoritmo,heuristica)
