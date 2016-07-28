# coding=utf-8
# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from Allegri import Estado

class EstadoContainer(Estado):
    """docstring for EstadoContainer"""
    def __init__(self, conjunto_estados):
        # inicializa-se o objeto como um estado sem nome e não-final
        super(EstadoContainer, self).__init__('', False)
        # a idéia aqui é encontrar os estados-raiz de cada elemento de conjunto_estados
        self.conjunto_estados = []
        for el in conjunto_estados:
            if isinstance(el, EstadoContainer):
                for estado in el.conjunto_estados:
                    if estado not in self.conjunto_estados:
                        self.conjunto_estados.append(estado)
            elif isinstance(el, Estado):
                if el not in self.conjunto_estados:
                    self.conjunto_estados.append(el)

        self.conjunto_estados = sorted(self.conjunto_estados, key=lambda e: e.nome)

        for estado in self.conjunto_estados:
            self.nome += estado.nome
            # self._final |= estado.isFinal()
            self.merge(estado, True)

    def compara_conjunto(self, conjunto_estados):
        temp = list(conjunto_estados)
        for el in conjunto_estados:
            if isinstance(el, EstadoContainer):
                temp.remove(el)
                for estado in el.conjunto_estados:
                    if estado not in temp:
                        temp.append(estado)
        # print('nome:', self.nome, 'conjunto_estados:', temp)
        if len(self.conjunto_estados) == len(temp):
            for el in self.conjunto_estados:
                if el not in temp:
                    return False
            return True
        else:
            return False
