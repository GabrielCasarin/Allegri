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

    def __eq__(self, maq):
        if isinstance(maq, AutomatoFinito):
            return self == self.nome
        else:
            return self.nome == maq


class TransdutorFinito(AutomatoFinito):
    def __init__(self, nome, **kwargs):
        super(TransdutorFinito, self).__init__(nome, **kwargs)
        self.saidas = {}
        self.saida_gerada = None
        self.transicoes_para_submaquinas = {}

    def fazer_transicao(self):
        # A lógica aqui é meio confusa :-(
        # Antes, verificamos se, para dados símbolo e estado atuais, existe
        # alguma saida (transdução) associada a esse par
        if (self._estadoAtual.nome, self._simboloAtual) in self.saidas:
            self.saida_gerada = self.saidas[(self._estadoAtual.nome, self._simboloAtual)]
        else:
            self.saida_gerada = None
        # assumindo-se que só exista saída para uma transição válida,
        # então estára tudo sempre ok.
        # A lógica parece estar invertida, mas fiz isso por dois motivos:
        # 1. Sempre que há transição possível, o estado atual muda e,
        #    dado que a saída está sempre associada ao estado anterior,
        #    teríamos que guardar o estado anterior para fazer a verificação posteriormente à transição,
        #    de modo que evita-se acrescentar mais variáveis e mais código/lógica à sub-rotina
        # 2. Reaproveita-se código fazendo desse modo (evita-se ter que alterar a fazer_transicao para acomodar a verficicação de saída)
        # Tenta fazer a transição
        return super(TransdutorFinito, self).fazer_transicao()

    def tem_transicao_para_submaquina(self):
        if self._estadoAtual.nome in self.transicoes_para_submaquinas:
            return True
        return False

    def add_saida(self, de, com, saida):
        self.saidas[(de, com)] = saida

    def add_chamada_para_submaquina(self, de, para, retorno):
        self.add_estado(de)
        self.add_estado(retorno)
        self.transicoes_para_submaquinas[de] = (para, self.estados[retorno])

    def get_parametros_de_chamada(self):
        if self._estadoAtual.nome in self.transicoes_para_submaquinas:
            prox_maq, _ = self.transicoes_para_submaquinas[self._estadoAtual.nome]
            if (self._estadoAtual.nome, prox_maq.nome) in self.saidas:
                self.saida_gerada = self.saidas[(self._estadoAtual.nome, prox_maq.nome)]
            else:
                self.saida_gerada = None
            return self.transicoes_para_submaquinas[self._estadoAtual.nome]
        else:
            return (None, None)
