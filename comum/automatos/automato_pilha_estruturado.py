# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from . import TransdutorFinito


class AutomatoPilhaEstruturado:
    """implementa um Autômato de Pilha Estruturado"""
    def __init__(self, nome, **kwargs):
        super(AutomatoPilhaEstruturado, self).__init__()
        # nome do autômato
        self.nome = nome
        # sub-máquinas
        if 'sub_maquinas' in kwargs and kwargs['sub_maquinas'] is not None:
            self.__automatos = {
                submaq: TransdutorFinito(nome=submaq) for submaq in kwargs['sub_maquinas']
            }
            if 'automatoInicial' in kwargs and kwargs['automatoInicial'] is not None:
                self.__maquinaInicial = kwargs['automatoInicial']
        else:
            self.__automatos = {}
        # configuração
        self.__maquinaAtual = None
        # Pilha
        self.__pilha = []

        # alfabeto
        self.alfabeto = set()
        self.__simboloAtual = None

    def gerar_alfabeto(self):
        for S in self.__automatos.values():
            self.alfabeto.update(S.alfabeto)

    def set_submaquina_inicial(self, sub_maq):
        self.__maquinaInicial = self.__automatos[sub_maq]

    def inicializar(self):
        """põe o Automato de Pilha Estruturado no estado inicial e dá outras providências."""
        self.__maquinaAtual = self.__maquinaInicial
        self.__maquinaAtual.inicializar()

    def atualizar_simbolo(self, simbolo):
        if simbolo in self.alfabeto:
            self.__simboloAtual = simbolo
        else:
            raise ValueError("Erro ao atualizar símbolo: '{}' não pertence ao alfabeto".format(simbolo))
        self.__maquinaAtual.atualizar_simbolo(simbolo)

    def fazer_transicao(self):
        # tenta fazer uma transição dentro da sub-máquina atual
        return self.__maquinaAtual.fazer_transicao()

    def chama(self):
        # pega a configuração atual do autômato
        estadoAtual, simboloAtual = self.__maquinaAtual.mConfiguracao()
        # Pega a próxima sub-máquina e o estado de retorno
        proxMaquina, estadoRetorno = estadoAtual['']
        # Empilha a sub-máquina de retorno e o estado de retorno
        self.__pilha.append((self.__maquinaAtual, estadoRetorno))
        # Troca de sub-máquina e a inicializa
        self.__maquinaAtual = proxMaquina
        self.__maquinaAtual.inicializar()
        # self.__maquinaAtual.atualizar_simbolo(simboloAtual)

    def retorna(self):
        if self.__pilha:
            submaqRet, estadoRetorno = self.__pilha.pop()
            _, simboloAtual = self.__maquinaAtual.mConfiguracao()
            self.__maquinaAtual = submaqRet
            self.__maquinaAtual.inicializar(estadoRetorno)
            # self.__maquinaAtual.atualizar_simbolo(simboloAtual)

    def mConfiguracao(self):
        temp1, temp2 = self.__maquinaAtual.mConfiguracao()
        return self.__maquinaAtual, temp1, temp2

    def __getitem__(self, sub_maq):
        if sub_maq in self.__automatos:
            return self.__automatos[sub_maq]
        else:
            return None
