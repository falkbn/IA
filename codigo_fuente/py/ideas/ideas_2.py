from py import problema_espacio_estados as pee
import copy


# When placing a white square, all matching numbers in row/column are black.
def white(state, i, j):
    matrix = state[0]
    value = matrix[i][j]
    e = state[1]

    count = 0
    for row in range(0, len(matrix)):
        if matrix[row][j] == value:
            count = count + 1
            matrix[row][j] = 0
            matrix[i][j] = 'X'

    for column in range(0, len(matrix[0])):
        if matrix[i][column] == value:
            count = count + 1
            matrix[i][column] = 0
            matrix[i][j] = 'X'
    e = e - count
    return state


# When shading a square, all neighboring squares are white.
def shade(state, i, j):
    matrix = state[0]
    max_i = len(matrix)
    max_j = len(matrix[0])

    matrix[i][j] = 0
    if i + 1 <= max_i:
        white(state, i + 1, j)
    if i - 1 >= 0:
        white(state, i - 1, j)
    if j + 1 <= max_j:
        white(state, i, j + 1)
    if j - 1 >= 0:
        white(state, i, j - 1)
    return state


# I will define applicability here:
def position_unchecked(state, i, j):
    position = state[0][i][j]
    return bool(position != 'X' and position != 0)


# Actions:
class ToBlack(pee.Acción):

    def __init__(self, i, j):
        nombre = '(Row:{}, Column:{}) has been shaded'.format(i, j)
        super().__init__(nombre)
        self.row = i
        self.column = j

    def es_aplicable(self, state):
        return position_unchecked(state, self.row, self.column)

    def aplicar(self, state):
        new_state = copy.deepcopy(state)
        return shade(new_state, self.row, self.column)
