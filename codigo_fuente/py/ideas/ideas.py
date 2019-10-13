from py import problema_espacio_estados as pee
import copy


class SombrearCasilla(pee.Acción):
    def __init__(self, i, j):
        nombre = 'Sombrear(F:{},C:{})'.format(i, j)
        super().__init__(nombre)
        self.fila = i
        self.columna = j

    def casilla_sin_evaluar(self, estado):
        posicion = estado[0][self.fila][self.columna]
        return bool(posicion != 'X' or posicion)

    def es_aplicable(self, estado):
        return self.casilla_sin_evaluar(estado)

    def fijar_casillas(self, estado):
        matriz = estado[0]
        valor_casilla = matriz[self.fila][self.columna]

        contador = 0
        for fila in range(0, len(matriz)):
            if matriz[fila][self.columna] == valor_casilla:
                contador = contador + 1
                matriz[fila][self.columna] = 0
                matriz[self.fila][self.columna] = 'X'

        for columna in range(0, len(matriz[0])):
            if matriz[self.fila][columna] == valor_casilla:
                contador = contador + 1
                matriz[self.fila][columna] = 0
                matriz[self.fila][self.columna] = 'X'
        estado[1] - contador

        return estado

    def sombrear_casilla(self, estado):
        matriz = estado[0]
        mayor_fila = len(matriz)
        mayor_columna = len(matriz[0])

        estado[1] - 1
        matriz[self.fila][self.columna] = 0
        if self.fila+1 <= mayor_fila:
            self.fila+1
            self.fijar_casillas(estado)
            self.fila-1
        if self.fila-1 >= 0:
            self.fila-1
            self.fijar_casillas(estado)
            self.fila+1
        if self.columna+1 <= mayor_columna:
            self.columna+1
            self.fijar_casillas(estado)
            self.columna-1
        if self.columna-1 >= 0:
            self.columna-1
            self.fijar_casillas(estado)
            self.columna+1

        return estado

    def aplicar(self, estado):
        nuevo_estado = copy.deepcopy(estado)
        return self.sombrear_casilla(nuevo_estado)