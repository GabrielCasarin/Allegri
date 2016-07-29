# coding=utf-8
# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from Allegri import Estado


class AutomatoFinito(object):
    """implementa um Autômato Finito Determinístico"""
    def __init__(self, nome, **kwargs):
        super(AutomatoFinito, self).__init__()
        # nome do automato
        self.nome = nome
        # estados
        if 'estados' in kwargs and kwargs['estados'] is not None:
            self.estados = {
                nomeEstado: Estado(nomeEstado) for nomeEstado in kwargs['estados']
            }
        if 'estadoInicial' in kwargs and kwargs['estadoInicial'] is not None:
            self.__estadoInicial = self.estados[kwargs['estadoInicial']]
        if 'estadosFinais' in kwargs and kwargs['estadosFinais'] is not None:
            for nomeEstado in kwargs['estadosFinais']:
                estado = self.estados[nomeEstado]
                estado.setFinal()
        # alfabeto
        if 'alfabeto' in kwargs and kwargs['alfabeto'] is not None:
            self.alfabeto = kwargs['alfabeto']
        else:
            self.alfabeto = []
        # m-Configuração
        self.__estadoAtual = None
        self.__simboloAtual = None

    def inicializar(self, estadoInicial=None, simboloInicial=None):
        self.__estadoAtual = self.__estadoInicial if estadoInicial is None else estadoInicial
        self.__simboloAtual = None if simboloInicial is None else simboloInicial

    def atualizarSimbolo(self, simbolo):
        if simbolo in self.alfabeto:
            self.__simboloAtual = simbolo
        else:
            raise ValueError("Erro ao fazer transição: símbolo não pertence ao alfabeto")

    def fazerTransicao(self):
        if self.__simboloAtual != '#':   # se não se consumiu todos os caracteres
            if (self.__simboloAtual in self.alfabeto) or self.__simboloAtual == '':
                if self.__simboloAtual in self.__estadoAtual:  # verifica se há transição associada ao simboloAtual in estadoAtual
                    proxEst = self.__estadoAtual[self.__simboloAtual]
                    self.__estadoAtual = proxEst
                    return True
            else:
                raise ValueError("Erro ao fazer transição: símbolo não pertence ao alfabeto")

        # retorna False em dois casos:
        #    1) atigingiu-se o fim da cadeia; ou
        #    2) não havia regra associada ao par (estadoAtual, simboloAtual)
        return False

    def mConfiguracao(self):
        return self.__estadoAtual, self.__simboloAtual

    def __eq__(self, maq):
    	if isinstance(maq, AutomatoFinito):
    		return self == name.nome
    	else:
    		return self.nome == maq
