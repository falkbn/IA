from py import problema_espacio_estados as pee
from py import búsqueda_espacio_estados as bee
from py import acciones as act
from time import time


matrices = open("C:/Users/falk/Desktop/hitoriNotes/txt/ejemplos_prueba.txt")
fichero = open("C:/Users/falk/Desktop/hitoriNotes/txt/ejemplos_reto_prueba_estrella.txt", "w")

for matrix_line in matrices:
    if matrix_line == " ":
        break
    matrix = eval(matrix_line)
    max_i = len(matrix)  # Row
    max_j = len(matrix[0])  # Column
    e = len(matrix) * len(matrix[0])  # Non-checked positions

    # States:
    pre_state_0 = (matrix, e)
    state_0 = act.par_inducido(pre_state_0)
    print(state_0)

    # Actions:
    acciones = [act.FijarCasilla(i, j) for i in range(0, max_i) for j in range(0, max_j)]
    acciones2 = [act.QuitarCasilla(i, j) for i in range(0, max_i) for j in range(0, max_j)]

    for a in acciones2:
        acciones.append(a)

    Hitori = pee.ProblemaEspacioEstados(acciones, state_0)


    def h(nodo):
        e = nodo.estado
        accs = []
        for acción in Hitori.acciones_aplicables(e):
            accs.append(acción.nombre)
        tmn = (len(accs) + 1)
        if e[1] < 0:
            return (max_i * max_j) ** (max_i * max_j)
        else:
            return e[1]*(10**(max(max_i, max_j))) + tmn * (10 ** (max(max_i, max_j)))

    b_estrella = bee.BúsquedaAEstrella(h, detallado=False)
    b_anchura = bee.BúsquedaEnAnchura(detallado=False)
    t1 = time()
    b_estrella.buscar(Hitori)
    t2 = time()

    fichero.write("Tiempo empleado en la respuesta: {}".format(t2 - t1) + "\n")
