from py import problema_espacio_estados as pee
from scipy.ndimage import label as conex
import copy


def casilla_sin_evaluar(estado, i, j):
    valor_posicion = estado[0][i][j]
    return bool(valor_posicion != 0)


def quitar_valores_repetidos(estado, i, j):
    valor_original_fijada = estado[0][i][j]
    max_i = len(estado[0]) - 1
    max_j = len(estado[0][0]) - 1
    contador = -1
    evaluadas = estado[1]

    for fila in range(0, max_i):
        if estado[0][fila][j] == valor_original_fijada:
            contador = contador + 1
            #estado[0][fila][j] = 0
            QuitarCasilla(fila, j).aplicar(estado)

    for columna in range(0, max_j):
        if estado[0][i][columna] == valor_original_fijada:
            contador = contador + 1
            estado[0][i][columna] = 0
            QuitarCasilla(i, columna).aplicar(estado)

    estado[0][i][j] = valor_original_fijada

    nuevo_estado = [estado[0], evaluadas - contador]
    return nuevo_estado


class QuitarCasilla(pee.Acción):

    def __init__(self, i, j):
        nombre = 'QUITAR:(Fila:{}, Columna:{})'.format(i, j)
        super().__init__(nombre)
        self.fila = i
        self.columna = j

    def coste_de_aplicar(self, estado):
        return 10

    def contigua_tachada(self, estado):
        res = True
        if self.fila + 1 < len(estado[0]) and estado[0][self.fila + 1][self.columna] == 0:
            return not res
        if self.fila - 1 >= 0 and estado[0][self.fila - 1][self.columna] == 0:
            return not res
        if self.columna + 1 < len(estado[0]) and estado[0][self.fila][self.columna + 1] == 0:
            return not res
        if self.columna - 1 >= 0 and estado[0][self.fila][self.columna - 1] == 0:
            return not res
        else:
            return res

    def valor_repetido(self, estado):
        valor_casilla = estado[0][self.fila][self.columna]
        max_i = len(estado[0]) - 1
        max_j = len(estado[0][0]) - 1

        for fila in range(0, max_i):
            if estado[0][fila][self.columna] == valor_casilla:
                return True

        for columna in range(0, max_j):
            if estado[0][self.fila][columna] == valor_casilla:
                return True

        return False

    def es_continuo(self, estado):
        nuevo_estado = copy.deepcopy(estado)
        nuevo_estado[0][self.fila][self.columna] = 0
        return conex(nuevo_estado[0])[1] == 1

    def es_aplicable(self, estado):
        return (casilla_sin_evaluar(estado, self.fila, self.columna) and
                self.contigua_tachada(estado) and
                self.valor_repetido(estado) and
                self.es_continuo(estado))

    def quitar_casilla(self, estado):
        estado[0][self.fila][self.columna] = 0
        evaluadas = estado[1]
        nuevo_estado = [estado[0], evaluadas - 1]
        # self.fijar_casillas_contiguas(estado)
        return nuevo_estado

    def fijar_casillas_contiguas(self, estado):
        contador = 0
        if self.fila + 1 < len(estado[0]):
            contador = contador + 1
            quitar_valores_repetidos(estado, self.fila + 1, self.columna)
        if self.columna + 1 < len(estado[0][0]):
            contador = contador + 1
            quitar_valores_repetidos(estado, self.fila, self.columna + 1)
        if self.fila - 1 >= 0:
            contador = contador + 1
            quitar_valores_repetidos(estado, self.fila - 1, self.columna)
        if self.columna - 1 >= 0:
            contador = contador + 1
            quitar_valores_repetidos(estado, self.fila, self.columna - 1)

        evaluadas = estado[1] - contador
        nuevo_estado = [estado[0], evaluadas]
        return nuevo_estado

    def aplicar(self, estado):
        nuevo_estado = copy.deepcopy(estado)
        return self.quitar_casilla(nuevo_estado)


class FijarCasilla(pee.Acción):

    def __init__(self, i, j):
        nombre = 'FIJAR:(Fila:{}, Columna:{})'.format(i, j)
        super().__init__(nombre)
        self.fila = i
        self.columna = j

    def coste_de_aplicar(self, estado):
        return 1

    def triplete_fila(self, estado):
        if self.columna == 0 or self.columna == (len(estado[0][0]) - 1):
            return False

        if (estado[0][self.fila][self.columna] != estado[0][self.fila][self.columna - 1]
                or estado[0][self.fila][self.columna] != estado[0][self.fila][self.columna + 1]):
            return False
        else:
            return True

    def triplete_columna(self, estado):
        if self.fila == 0 or self.fila == (len(estado[0]) - 1):
            return False
        if (estado[0][self.fila][self.columna] != estado[0][self.fila - 1][self.columna]
                or estado[0][self.fila][self.columna] != estado[0][self.fila + 1][self.columna]):
            return False
        else:
            return True

    def entre_pares_fila(self, estado):
        if self.columna == 0 or self.columna == (len(estado[0][0]) - 1):
            return False
        if estado[0][self.fila][self.columna + 1] == 0:
            return False
        if estado[0][self.fila][self.columna + 1] != estado[0][self.fila][self.columna - 1]:
            return False
        else:
            return True

    def entre_pares_columna(self, estado):
        if self.fila == 0 or self.fila == (len(estado[0]) - 1):
            return False
        if estado[0][self.fila + 1][self.columna] == 0:
            return False
        if estado[0][self.fila + 1][self.columna] != estado[0][self.fila - 1][self.columna]:
            return False
        else:
            return True

    def es_aplicable(self, estado):
        return (casilla_sin_evaluar(estado, self.fila, self.columna) and
                ((self.triplete_columna(estado) or self.triplete_fila(estado)) or
                (self.entre_pares_columna(estado) or self.entre_pares_fila(estado))))

    def fijar_casilla(self, estado):
        evaluadas = estado[1] - 1
        nuevo_estado = [estado[0], evaluadas - 1]
        quitar_valores_repetidos(nuevo_estado, self.fila, self.columna)
        return nuevo_estado

    def aplicar(self, estado):
        nuevo_estado = copy.deepcopy(estado)
        return self.fijar_casilla(nuevo_estado)
