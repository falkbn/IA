from py import problema_espacio_estados as pee
from scipy.ndimage import label as conex
import copy


def par_inducido(estado):
    evaluadas = 0
    estado = copy.deepcopy(estado)

    for valor in range(1, len(estado[0])):
        for fila in range(0, len(estado[0])):
            for columna in range(0, len(estado[0][0])):
                if columna + 1 <= len(estado[0][0]) - 1 and columna - 1 >= 0:
                    if (estado[0][fila][columna] == estado[0][fila][columna + 1]
                            and estado[0][fila][columna] != estado[0][fila][columna - 1]
                            and estado[0][fila][columna] == valor):
                        for j in range(0, len(estado[0][0])):
                            if (estado[0][fila][j] == valor
                                    and j != columna and j != columna + 1 and j != columna - 1):
                                evaluadas = evaluadas + 1
                                estado[0][fila][j] = 0
    transpuesta = [[estado[0][b][a] for b in range(len(estado[0]))] for a in range(len(estado[0][0]))]
    for valor in range(1, len(transpuesta)):
        for fila in range(0, len(transpuesta)):
            for columna in range(0, len(transpuesta[0])):
                if columna + 1 <= len(transpuesta[0]) - 1 and columna - 1 >= 0:
                    if (transpuesta[fila][columna] == transpuesta[fila][columna + 1]
                            and transpuesta[fila][columna] != transpuesta[fila][columna - 1]
                            and transpuesta[fila][columna] == valor):
                        for j in range(0, len(transpuesta[0])):
                            if (transpuesta[fila][j] == valor
                                    and j != columna and j != columna + 1):
                                evaluadas = evaluadas + 1
                                transpuesta[fila][j] = 0
    nueva_matriz = [[transpuesta[b][a] for b in range(len(transpuesta))] for a in range(len(transpuesta[0]))]
    return [nueva_matriz, estado[1] - int(evaluadas)]


def casilla_sin_evaluar(estado, i, j):
    valor_posicion = estado[0][i][j]
    return bool(valor_posicion != 0)


def contigua_no_tachada(estado, i, j):
    res = True
    if i + 1 < len(estado[0]) and estado[0][i + 1][j] == 0:
        return not res
    if i - 1 >= 0 and estado[0][i - 1][j] == 0:
        return not res
    if j + 1 < len(estado[0]) and estado[0][i][j + 1] == 0:
        return not res
    if j - 1 >= 0 and estado[0][i][j - 1] == 0:
        return not res
    else:
        return res


def quitar_casilla(estado, i, j):
    estado[0][i][j] = 0
    evaluadas = estado[1]
    nuevo_estado = [estado[0], evaluadas - 1]
    return nuevo_estado


def valor_repetido(estado, i, j):
    valor_casilla = estado[0][i][j]
    max_i = len(estado[0]) - 1
    max_j = len(estado[0][0]) - 1

    for fila in range(0, max_i):
        if i != fila and estado[0][fila][j] == valor_casilla and valor_casilla != 0:
            return True

    for columna in range(0, max_j):
        if j != columna and estado[0][i][columna] == valor_casilla and valor_casilla != 0:
            return True

    return False


def es_continuo(estado, i, j):
    nuevo_estado = copy.deepcopy(estado)
    nuevo_estado[0][i][j] = 0
    return conex(nuevo_estado[0])[1] == 1


class FijarCasilla(pee.Acción):

    def __init__(self, i, j):
        nombre = 'FIJAR:(Fila:{}, Columna:{})'.format(i, j)
        super().__init__(nombre)
        self.fila = i
        self.columna = j

    def coste_de_aplicar(self, estado):
        coste = 10**(len(estado[0])*len(estado[0][0]))
        if not es_continuo(estado, self.fila, self.columna):
            coste = 100  # *(len(estado[0])+len(estado[0]))
        if not contigua_no_tachada(estado, self.fila, self.columna):
            coste = 10  # *(len(estado[0])+len(estado[0]))
        if self.entre_pares(estado):
            coste = 1  # *(len(estado[0])+len(estado[0]))
        return coste

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

    def entre_pares(self, estado):
        return self.entre_pares_fila(estado) or self.entre_pares_columna(estado)

    def es_aplicable(self, estado):
        return (casilla_sin_evaluar(estado, self.fila, self.columna) and
                (self.entre_pares(estado) or
                 not contigua_no_tachada(estado, self.fila, self.columna)
                 or not es_continuo(estado, self.fila, self.columna)
                 ) and valor_repetido(estado, self.fila, self.columna))
        # probar aplicable si es valor unico en la fila y columna

    def quitar_valores_repetidos(self, estado):
        valor_casilla = estado[0][self.fila][self.columna]
        nuevo_estado = estado

        for fila in range(0, len(estado[0])):
            if fila != self.fila and estado[0][fila][self.columna] == valor_casilla:
                if contigua_no_tachada(estado, fila, self.columna):
                    nuevo_estado = quitar_casilla(nuevo_estado, fila, self.columna)

        for columna in range(0, len(estado[0])):
            if columna != self.columna and estado[0][self.fila][columna] == valor_casilla:
                if contigua_no_tachada(estado, self.fila, columna):
                    nuevo_estado = quitar_casilla(nuevo_estado, self.fila, columna)

        return nuevo_estado

    def fijar_casilla(self, estado):
        evaluadas = estado[1] - 1
        nuevo_estado = [estado[0], evaluadas - 1]
        return self.quitar_valores_repetidos(nuevo_estado)

    def aplicar(self, estado):
        nuevo_estado = copy.deepcopy(estado)
        return self.fijar_casilla(nuevo_estado)


class QuitarCasilla(pee.Acción):

    def __init__(self, i, j):
        nombre = 'QUITAR:(Fila:{}, Columna:{})'.format(i, j)
        super().__init__(nombre)
        self.fila = i
        self.columna = j

    def coste_de_aplicar(self, estado):
        return 1000

    def es_aplicable(self, estado):
        return (casilla_sin_evaluar(estado, self.fila, self.columna) and
                contigua_no_tachada(estado, self.fila, self.columna) and
                valor_repetido(estado, self.fila, self.columna) and
                es_continuo(estado, self.fila, self.columna))

    def aplicar(self, estado):
        nuevo_estado = copy.deepcopy(estado)
        return quitar_casilla(nuevo_estado, self.fila, self.columna)
