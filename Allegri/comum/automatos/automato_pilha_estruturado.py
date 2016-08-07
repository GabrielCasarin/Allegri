# coding=utf-8
# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from Allegri import Estado


class AutomatoPilhaEstruturado(object):
    """implementa um Autômato de Pilha Estruturado"""
    def __init__(self, nome, **kwargs):
        super(AutomatoPilhaEstruturado, self).__init__()
        ## nome do autômato
        self.nome = nome
        ## sub-máquinas
        if 'sub-maquinas' in kwargs and kwargs['sub-maquinas'] is not None:
            self.__subMaquinas = {
                submaq.nome: submaq for submaq in kwargs['sub-maquinas']
            }
            self.__transicoesSubmaquina = {
                submaq.nome: Estado(submaq.nome) for submaq in kwargs['sub-maquinas']
            }
        else:
            self.__subMaquinas = {}
        if 'automatoInicial' in kwargs and kwargs['automatoInicial'] is not None:
            self.__automatoInicial = kwargs['automatoInicial']
        ## configuração
        self.__maquinaAtual = None
        ## Pilha
        self.__pilha = []

    def inicializar(self):
        """põe o Automato de Pilha Estruturado no estado inicial e dá outras providências."""
        self.__maquinaAtual = self.__automatoInicial
        self.__maquinaAtual.inicializar()

    def chama(self):
        # pega a configuração atual do autômato
        estadoAtual, _ = self.__maquinaAtual.mConfiguracao()
        tag = self.__maquinaAtual.nome
        # Pega a próxima sub-máquina e o estado de retorno
        proxMaquina, estadoRetorno = self.__maquinaAtual[tag][estadoAtual]
        # Empilha a sub-máquina de retorno e o estado de retorno
        self._pilha.append((self.__maquinaAtual, estadoRetorno))

    def retorna(self):
        if self.__pilha:
            submaqRet, estadoRetorno = self.__pilha.pop()
            self.__maquinaAtual = submaqRet
            self.__maquinaAtual.inicializar(estadoRetorno)
