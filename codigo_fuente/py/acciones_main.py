from py import problema_espacio_estados as pee
from py import búsqueda_espacio_estados as bee
from py import acciones as act
from time import time


# Parameters:
matrix = [[7,6,4,4,5,5,1,8,3],[5,5,1,8,6,9,7,3,7],[6,8,4,7,1,8,3,5,5],[9,1,5,3,7,2,4,6,6],[1,7,7,2,3,8,6,5,8],[2,2,7,7,5,4,8,1,3],[4,2,8,1,2,6,5,3,9],[1,2,6,4,4,2,8,9,1],[1,5,2,7,8,1,9,4,6]]

max_i = len(matrix)                 # Row
max_j = len(matrix[0])              # Column
e = len(matrix) * len(matrix[0])    # Non-checked positions

# States:
pre_state_0 = (matrix, e)
state_0 = act.par_inducido(pre_state_0)

# Actions:
acciones = [act.FijarCasilla(i, j) for i in range(0, max_i) for j in range(0, max_j)]
acciones2 = [act.QuitarCasilla(i, j) for i in range(0, max_i) for j in range(0, max_j)]

for a in acciones2:
    acciones.append(a)

# Definition:
Hitori = pee.ProblemaEspacioEstados(acciones, state_0)

print("==============================================")
print("Estado inicial:")
print(state_0)
print("==============================================")
print("Acciones posibles en el estado inicial:")
for acción in Hitori.acciones_aplicables(state_0):
    print(acción.nombre)
print("==============================================")
print("Nodos:")
b_anchura = bee.BúsquedaEnAnchura(detallado=True)

b_profundidad = bee.BúsquedaEnProfundidad(detallado=True)  # Cota: pasos maximos en profundidad (altura del arbol)
b_profundidad_acotada = bee.BúsquedaEnProfundidadAcotada(cota=5, detallado=True)  # Búsqueda acotada cota:inicial-final.
b_profundidad_iterativa = bee.BúsquedaEnProfundidadIterativa(cota_final=7, cota_inicial=4, detallado=True)


def h(nodo):
    e = nodo.estado
    accs = []
    for acción in Hitori.acciones_aplicables(e):
        accs.append(acción.nombre)
    tmn = (len(accs)+1)
    if e[1] < 0:
        return (max_i*max_j)**(max_i*max_j)
    else:
        return e[1]*(10**(max(max_i, max_j))) + tmn*(10**(max(max_i, max_j)))


b_estrella = bee.BúsquedaAEstrella(h, detallado=True)


t1 = time()
print(b_estrella.buscar(Hitori))
t2 = time()
print("Tiempo empleado en la respuesta: {}".format(t2 - t1))
print("==============================================")
print("Espacio para pruebas:")
t1 = time()
print(act.par_inducido(pre_state_0))
t2 = time()
print("Tiempo empleado en induccion: {}".format(t2 - t1))
print("==============================================")


