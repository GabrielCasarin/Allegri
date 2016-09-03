# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from . import Estado
from .AbstractAutomato import AbstractAutomato


class AutomatoFinito(AbstractAutomato):
    """implementa um Autômato Finito Determinístico"""
    def __init__(self, nome, **kwargs):
        super(AutomatoFinito, self).__init__(deterministico=True)
        # nome do automato
        self.nome = nome
        # estados
        if 'estados' in kwargs and kwargs['estados'] is not None:
            self.estados = {
                nome_estado: Estado(nome_estado) for nome_estado in kwargs['estados']
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
        # m-Configuração
        self.__estadoAtual = None
        self.__simboloAtual = None

    def inicializar(self, estadoInicial=None, simboloInicial=None):
        # por padrão, inicia no estado inicial constante no arquivo de especificação do autômato,
        # porém, é possível,nos casos de retorno de sub-máquina, iniciar o autômato em outro estado (estado de retorno, nesse caso)
        self.__estadoAtual = self.__estadoInicial if estadoInicial is None else estadoInicial
        self.__simboloAtual = None if simboloInicial is None else simboloInicial

    def atualizarSimbolo(self, simbolo):
        if simbolo in self.alfabeto:
            self.__simboloAtual = simbolo
        else:
            raise ValueError("Erro ao atualizar símbolo: não pertence ao alfabeto")

    def fazerTransicao(self):
        if self.__simboloAtual in self.alfabeto:
            # or self.__simboloAtual == ''): qual a necessidade disso?
                if self.__simboloAtual in self.__estadoAtual:  # verifica se há transição associada ao simboloAtual in estadoAtual
                    proxEst = self.__estadoAtual[self.__simboloAtual]
                    if proxEst is not None:
                        self.__estadoAtual = proxEst
                        return True
                return False

        else:
            raise ValueError("Erro ao fazer transição: símbolo não pertence ao alfabeto")

    def mConfiguracao(self):
        return self.__estadoAtual, self.__simboloAtual

    def __eq__(self, maq):
    	if isinstance(maq, AutomatoFinito):
    		return self == name.nome
    	else:
    		return self.nome == maq

    def __getitem__(self, nome_estado):
        if nome_estado in self.estados:
            return self.estados[nome_estado]
        else:
            return None
