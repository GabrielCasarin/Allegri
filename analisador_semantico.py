# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from comum import AbstractSimulador
import tabela_simbolos as ST


class gerar_codigo_assembly(AbstractSimulador):
    def __init__(self, log=False):
        super(gerar_codigo_assembly, self).__init__()
        self.tabela_simbolos = ST.TabelaSimbolos()
        self.tipos = {
                "int": ST.TipoBasico("int", 2),
                "char": ST.TipoBasico("char", 2),
                "bool": ST.TipoBasico("bool", 2),
                "void": ST.TipoBasico("void", 0),
        }
        self.pilha_operandos = []
        self.pilha_operadores = []
        self.__func_atual = None

        # código necessário a todos os programas compilados
        self.preambulo = [
            "PUSH    <",
            "POP     <",
            "SP      <",
            "TRUE    <",
            "FALSE   <",
            "AND   <",
            "OR    <",
            "NOT   <",
            "OP1   <",
            "OP2   <",
            "GET_VECT    <",
            "SET_VET     <",
            "GET_OFFSET  <",
            "SET_OFFSET  <",
            "K_0  <",
            "WORD_TAM <",
            "&    /0000",
            "LD   SP",
            "MM   FP",
            "SC main",
            "FIM HM FIM",
            "FP    $ =1",
        ]

        # insere na tabela de símbolos todos os imports
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("PUSH", "func", self.tipos["void"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("POP", "func", self.tipos["int"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.SimboloConst("TRUE", "const", self.tipos["bool"], 1)
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.SimboloConst("FALSE", "const", self.tipos["bool"], 0)
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("AND", "func", self.tipos["bool"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("NOT", "func", self.tipos["bool"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("OR", "func", self.tipos["bool"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("ACESSO_VET", "func", self.tipos["int"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.Simbolo("ATTR_VET", "func", self.tipos["void"])
        )
        self.tabela_simbolos.inserir_simbolo(
            ST.SimboloConst("K_0", "const", self.tipos["int"], 0)
        )

        # armazena o código referente a declarações de constantes 
        self.constantes = []
        # armazena todo o código gerado
        self.codigo = []
        
        self.__log = log

    def __call__(self, rotina, token=None):
        if self.__log:
            print('entrei na sub-rotina de geração de código objeto...')

        # EXPRESSÕES MATEMÁTICAS
        if rotina == 'iniciar_expressao_mat':
            self.iniciar_expressao_mat()
        elif rotina == 'recebe_operador_normal':
            self.recebe_operador_normal(token)
        elif rotina == 'mais_ou_menos':
            self.mais_ou_menos(token)
        elif rotina == 'vezes_ou_dividir':
            self.vezes_ou_dividir(token)
        elif rotina == 'recebe_operando_var':
            self.recebe_operando_var(token)
        elif rotina == 'recebe_operando_num':
            self.recebe_operando_num(token)
        elif rotina == 'finalizar_expressao_mat':
            self.finalizar_expressao_mat()
        elif rotina == 'abre_parenteses':
            self.abre_parenteses()
        elif rotina == 'fecha_parenteses':
            self.fecha_parenteses()
        elif rotina == 'sai_termo':
            self.sai_termo()
        # FIM EXPRESSÕES MATEMÁTICAS

        # DECLARAÇÃO DE FUNÇÕES
        elif rotina == 'declaracao_funcao':
            self.declaracao_funcao(token)
        elif rotina == 'definir_tipo_funcao':
            self.definir_tipo_funcao(token)
        elif rotina == 'inicia_declaracao_parametro':
            self.inicia_declaracao_parametro()
        elif rotina == 'novo_par':
            self.novo_par(token)
        elif rotina == 'fecha_declaracao_parametro':
            self.fecha_declaracao_parametro(token)        
        elif rotina == 'inicia_declaracao_variavel':
            self.inicia_declaracao_variavel()
        elif rotina == 'nova_var':
            self.nova_var(token)
        elif rotina == 'fecha_declaracao_variavel':
            self.fecha_declaracao_variavel(token)
        elif rotina == 'encerra_funcao':
            self.encerra_funcao()
        # DECLARAÇÃO DE FUNÇÕES

        # ACESSO A VARIÁVEIS
        elif rotina == 'ref_var_01':
            self.ref_var_01(token)
        elif rotina == 'ref_var_02':
            self.ref_var_02()
        elif rotina == 'ref_var_03':
            self.ref_var_03()
        # FIM ACESSO A VARIÁVEIS

        # COMANDO SIMPLES
        elif rotina == 'inicia_comando_simples':
            self.inicia_comando_simples(token)
        elif rotina == 'comando_atribuicao':
            self.comando_atribuicao()
        # FIM COMANDO SIMPLES

        if self.__log:
            print('saí da sub-rotina de geração de código objeto...')

    # FUNÇÕES AUXILIARES
    def hex_repr(num):
        if num < 0:
            return hex(((abs(num) ^ 0xffff) + 1) & 0xffff)[-4:]
        else:
            return "{:0>4X}".format(num)

    def get_const_num_repr(self, num):
        label = "K_" + gerar_codigo_assembly.hex_repr(int(num))
        const_existe = self.tabela_simbolos.procurar_const(label)
        if not const_existe:
            nova_const = ST.SimboloConst(label, "const", self.tipos["int"], num)
            nova_const.referenciado = True
            nova_const.utilizado = True
            self.tabela_simbolos.inserir_const(nova_const)
            self.constantes.append("{nome}\tK /{val:04X}".format(nome=nova_const.nome, val=nova_const.valor))
        return label

    def log_tabela(self):
        escopo = self.tabela_simbolos.escopo_atual
        while escopo is not None:
            print()
            for s in escopo.simbolos:
                print("{0.nome}    {0.tipo.s}    {0.especie}    {0.posicao}".format(s))
            print()
            escopo = escopo.pai
    # FIM FUNÇÕES AUXILIARES

    # DECLARAÇÃO DE FUNÇÕES
    def declaracao_funcao(self, nome_func):
        _, simb = self.tabela_simbolos.procurar(nome_func)
        if simb is None:
            self.__func_atual = ST.SimboloFunc(nome_func, self.tipos["void"]) # toda função é procedimento até que se prove o contrário
            self.tabela_simbolos.inserir_simbolo(self.__func_atual)
            self.tabela_simbolos.novo_escopo()
            self.codigo.append("{}\t$ =1".format(self.__func_atual.nome))

    def definir_tipo_funcao(self, tipo_retorno):
        if tipo_retorno in self.tipos:
            self.__func_atual.tipo = self.tipos[tipo_retorno]

    def inicia_declaracao_parametro(self):
        self.__lista_parametros = []

    def novo_par(self, nome_par):
        self.__lista_parametros.append(nome_par)

    def fecha_declaracao_parametro(self, tipo_par):
        for nome_par in self.__lista_parametros:
            _, simb = self.tabela_simbolos.procurar(nome_par)
            if simb is None:
                par_simb = ST.Simbolo(nome_par, "par", self.tipos[tipo_par])
                par_simb.posicao = self.__func_atual.pilha_offset
                self.__func_atual.pilha_offset += par_simb.tipo.tamanho
                self.tabela_simbolos.inserir_simbolo(par_simb)

    def encerra_funcao(self):
        escopo = self.tabela_simbolos.escopo_atual
        print()
        for s in escopo.simbolos:
            print("{0.nome}    {0.tipo.s}    {0.especie}    {0.posicao}".format(s))
        print()
        self.tabela_simbolos.remover_escopo()
        self.codigo.append("RET_{0}\tRS\t{0}".format(self.__func_atual.nome))
        self.__func_atual = None

    def inicia_declaracao_variavel(self):
        self.__lista_variaveis_a_declarar = []

    def nova_var(self, nome_var):
        self.__lista_variaveis_a_declarar.append(nome_var)
        # print(self.__lista_variaveis_a_declarar)

    def fecha_declaracao_variavel(self, tipo_var):
        for nome_var in self.__lista_variaveis_a_declarar:
            _, simb = self.tabela_simbolos.procurar(nome_var)
            if simb is None:
                var_simb = ST.Simbolo(nome_var, "var", self.tipos[tipo_var])
                var_simb.posicao = self.__func_atual.pilha_offset
                self.tabela_simbolos.inserir_simbolo(var_simb)
                self.__func_atual.pilha_offset += var_simb.tipo.tamanho
    # FIM DECLARAÇÃO DE FUNÇÕES

    # EXPRESSÕES MATEMÁTICAS
    def iniciar_expressao_mat(self):
        self.pilha_operadores.append('LD')

    def recebe_operador_normal(self, operador):
        print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
        self.pilha_operadores.append(operador)

    def vezes_ou_dividir(self, operador):
        self.pilha_operadores.append(operador)
        print('SC PUSH')
        self.pilha_operadores.append('LD')
        print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
        self.pilha_operandos.append('ACC_AUX')

    def recebe_operando_var(self, operando):
        self.pilha_operandos.append(operando)

    def recebe_operando_num(self, num):
        label = self.get_const_num_repr(num)
        print(label, 'oiaqui')
        self.pilha_operandos.append(label)

    def finalizar_expressao_mat(self):
        while len(self.pilha_operandos) > 1:
            # termina a operacap de * ou /
            print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
            # guarda em X
            print('MM ACC_AUX')
            print('SC POP')
            # entrega tudo bonitinho no acc
        print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))

    def abre_parenteses(self):
        self.pilha_operandos.append('ACC_AUX')
        self.pilha_operadores.append('(')
        print('SC PUSH')

    def fecha_parenteses(self):
        # finaliza a expressão interna
        while self.pilha_operadores[-1] != '(':
            print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
            # restaura o estado anterior
            print('MM ACC_AUX')
            print('SC POP')
        self.pilha_operadores.pop() # retira o '('

    def sai_termo(self):
        # termina a operacap de * ou /
        print('{} {}'.format(self.pilha_operadores.pop(), self.pilha_operandos.pop()))
        # guarda em X
        print('MM ACC_AUX')
        print('SC POP')
    # FIM EXPRESSÕES MATEMÁTICAS

    # ACESSO A VARIÁVEIS
    def ref_var_01(self, nome_var):
        escopo, pos = self.tabela_simbolos.procurar(nome_var)
        if pos is not None:
            self.codigo.append('LD FP')
            self.codigo.append('SC PUSH')
            self.codigo.append('LD K_{}'.format(escopo[pos].posicao))
            self.codigo.append('SC PUSH')
            self.codigo.append('LD K_{}'.format(escopo[pos].tipo.tamanho))
            self.codigo.append('SC PUSH')
            self.codigo.append('SC ACESSO_VET')

    def ref_var_02(self):
        print('MM BASE')

    def ref_var_03(self):
        print('MM OFFSET')
        print('SC ACESSO_VET')
    # FIM ACESSO A VARIÁVEIS

    # COMANDO SIMPLES
    def inicia_comando_simples(self, identificador):
        # procura o identificador na tabela
        escopo, indice = self.tabela_simbolos.procurar(identificador)
        # se encontrou em algum escopo
        if escopo is not None and indice is not None:
            self.__identificador_atual = escopo[indice]
            self.__identificador_atual.utilizado = True

    def comando_atribuicao(self):
        self.codigo.append("LD K_0028")
        self.codigo.append("SC PUSH")
        self.codigo.append("LD FP")
        self.codigo.append("SC PUSH")
        self.codigo.append("LD {}".format(self.get_const_num_repr(self.__identificador_atual.posicao)))
        self.codigo.append("SC PUSH")
        self.codigo.append("SC SET_OFFSET")


    # FIM COMANDO SIMPLES