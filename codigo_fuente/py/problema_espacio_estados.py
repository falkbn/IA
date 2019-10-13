from scipy.ndimage import label as conex
import numpy as np


class Acción:
    def __init__(self, nombre='', aplicabilidad=None, aplicación=None,
                 coste=None):
        self.nombre = nombre
        self.aplicabilidad = aplicabilidad
        self.aplicación = aplicación
        self.coste = coste

    def es_aplicable(self, estado):
        if self.aplicabilidad is None:
            raise NotImplementedError(
                'Aplicabilidad de la acción no implementada')
        else:
            return self.aplicabilidad(estado)

    def aplicar(self, estado):
        if self.aplicar is None:
            raise NotImplementedError(
                'Aplicación de la acción no implementada')
        else:
            return self.aplicación(estado)

    def coste_de_aplicar(self, estado):
        if self.coste is None:
            return 1
        else:
            return self.coste(estado)

    def __str__(self):
        return 'Acción: {}'.format(self.nombre)


def comprueba_estado_final(estado):
    max_i = len(estado[0])
    matriz = estado[0]
    matriz_transpuesta = np.transpose(matriz)

    if conex(estado[0])[1] != 1:
        return False
    for fila in range(0, max_i):
        lista = matriz[fila]
        for puntero_1 in range(0, len(lista)):
            for puntero_2 in range(puntero_1, len(lista)):
                if puntero_1 != puntero_2 and lista[puntero_1] != 0 and lista[puntero_1] == lista[puntero_2]:
                    return False
    for fila in range(0, max_i):
        lista = matriz_transpuesta[fila]
        for puntero_1 in range(0, len(lista)):
            for puntero_2 in range(puntero_1, len(lista)):
                if puntero_1 != puntero_2 and lista[puntero_1] != 0 and lista[puntero_1] == lista[puntero_2]:
                    return False
    return True


class ProblemaEspacioEstados:
    def __init__(self, acciones, estado=None):
        if not isinstance(acciones, list):
            raise TypeError('Debe proporcionarse una lista de acciones')
        self.acciones = acciones
        self.estado = estado

    def acciones_aplicables(self, estado):
        return (acción
                for acción in self.acciones
                if acción.es_aplicable(estado))

    def es_estado_final(self, estado):
        if comprueba_estado_final(estado):
            return estado
        else:
            return False


class ProblemaEspacioEstados_0:
    def __init__(self, acciones, estado_inicial=None, estados_finales=None):
        if not isinstance(acciones, list):
            raise TypeError('Debe proporcionarse una lista de acciones')
        self.acciones = acciones
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales

    def es_estado_final(self, estado):
        return estado in self.estados_finales

    def acciones_aplicables(self, estado):
        return (acción
                for acción in self.acciones
                if acción.es_aplicable(estado))
