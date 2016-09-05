# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from . import Estado, AbstractAutomato


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
                self._estadoInicial = self.estados[kwargs['estadoInicial']]
            if 'estadosFinais' in kwargs and kwargs['estadosFinais'] is not None:
                for nomeEstado in kwargs['estadosFinais']:
                    estado = self.estados[nomeEstado]
                    estado.setFinal()
        # alfabeto
        if 'alfabeto' in kwargs and kwargs['alfabeto'] is not None:
            self.alfabeto = kwargs['alfabeto']
        # m-Configuração
        self._estadoAtual = None
        self._simboloAtual = None

    def set_inicial(self, estado):
        self._estadoInicial = self.estados[estado]

    def inicializar(self, estadoInicial=None, simboloInicial=None):
        # por padrão, inicia no estado inicial constante no arquivo de especificação do autômato,
        # porém, é possível,nos casos de retorno de sub-máquina, iniciar o autômato em outro estado (estado de retorno, nesse caso)
        self._estadoAtual = self._estadoInicial if estadoInicial is None else estadoInicial
        self._simboloAtual = None if simboloInicial is None else simboloInicial

    def atualizar_simbolo(self, simbolo):
        if simbolo in self.alfabeto:
            self._simboloAtual = simbolo
        else:
            raise ValueError("Erro ao atualizar símbolo: '{}' não pertence ao alfabeto".format(simbolo))

    def fazer_transicao(self):
        if self._simboloAtual in self.alfabeto:
            if self._simboloAtual in self._estadoAtual:  # verifica se há transição associada ao simboloAtual in estadoAtual
                proxEst = self._estadoAtual[self._simboloAtual]
                if proxEst is not None:
                    self._estadoAtual = proxEst
                    return True
            return False

        else:
            raise ValueError("Erro ao fazer transição: símbolo não pertence ao alfabeto")

    def mConfiguracao(self):
        return self._estadoAtual, self._simboloAtual

    def __getitem__(self, nome_estado):
        if nome_estado in self.estados:
            return self.estados[nome_estado]
        else:
            return None

    def __eq__(self, maq):
        if isinstance(maq, AutomatoFinito):
            return self == self.nome
        else:
            return self.nome == maq


class TransdutorFinito(AutomatoFinito):
    def __init__(self, nome, **kwargs):
        super(TransdutorFinito, self).__init__(nome, **kwargs)
        self.saidas = {}

    def add_saida(self, de, com, saida):
        self.saidas[(de, com)] = saida

    def traduzir(self):
        return self.saidas[(self._estadoAtual.nome, self._simboloAtual)]
