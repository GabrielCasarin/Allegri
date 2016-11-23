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

        self.__fp_em_base = False

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
            "SET_VECT     <",
            "GET_OFFSET  <",
            "SET_OFFSET  <",
            "PUSHDOWN_SUM    <",
            "PUSHDOWN_DIF    <",
            "PUSHDOWN_MUL    <",
            "PUSHDOWN_DIV    <",
            "BASE    <",
            "K_0000  <",
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
            ST.SimboloConst("K_0000", "const", self.tipos["int"], 0)
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
        elif rotina == 'inicia_declaracao_parametros':
            self.inicia_declaracao_parametros()
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

        # CHAMADA DE FUNÇÃO
        elif rotina == 'iniciar_frame':
            self.iniciar_frame()
        elif rotina == 'chamar_funcao':
            self.chamar_funcao()
        # FIM CHAMADA DE FUNÇÃO

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
        const_existe = self.tabela_simbolos.existe(label)
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
    
    def load_val(self, operando):
        if (operando.especie == "var"
            or operando.especie == "par"):
                if not self.__fp_em_base:
                    self.codigo.append("LD FP")
                    self.codigo.append("MM BASE")
                self.codigo.append('LD {}'.format(self.get_const_num_repr(operando.posicao)))
                self.codigo.append('SC PUSH')
                self.codigo.append('SC GET_VECT')
        elif operando.especie == "const":
            self.codigo.append('LD {}'.format(operando.nome))
        self.codigo.append('SC PUSH')
    # FIM FUNÇÕES AUXILIARES

    # DECLARAÇÃO DE FUNÇÕES
    def declaracao_funcao(self, nome_func):
        func_existe = self.tabela_simbolos.existe(nome_func)
        if not func_existe:
            self.__func_atual = ST.SimboloFunc(nome_func, self.tipos["void"]) # toda função é procedimento até que se prove o contrário
            self.tabela_simbolos.inserir_simbolo(self.__func_atual)
            self.tabela_simbolos.novo_escopo()
            self.codigo.append("{}\t$ =1".format(self.__func_atual.nome))

    def definir_tipo_funcao(self, tipo_retorno):
        if tipo_retorno in self.tipos:
            self.__func_atual.tipo = self.tipos[tipo_retorno]
            self.__func_atual.pilha_offset += self.__func_atual.tipo.tamanho

    def inicia_declaracao_parametros(self):
        self.__lista_parametros = []

    def novo_par(self, nome_par):
        self.__lista_parametros.append(nome_par)

    def fecha_declaracao_parametro(self, tipo_par):
        for nome_par in self.__lista_parametros:
            parametro_existe = self.tabela_simbolos.existe(nome_par)
            if not parametro_existe:
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
            variavel_existe = self.tabela_simbolos.existe(nome_var)
            if not variavel_existe:
                var_simb = ST.Simbolo(nome_var, "var", self.tipos[tipo_var])
                var_simb.posicao = self.__func_atual.pilha_offset
                self.tabela_simbolos.inserir_simbolo(var_simb)
                self.__func_atual.pilha_offset += var_simb.tipo.tamanho
    # FIM DECLARAÇÃO DE FUNÇÕES

    # EXPRESSÕES MATEMÁTICAS
    def iniciar_expressao_mat(self):
        # self.pilha_operadores.append('LD')
        if not self.__fp_em_base:
            self.codigo.append("LD FP")
            self.codigo.append("MM BASE")
            self.__fp_em_base = True

    def mais_ou_menos(self, operador):
        if self.pilha_operadores:
            if (self.pilha_operadores[-1] == '*'
                or self.pilha_operadores[-1] =='/'):
                    self.sai_termo()
            if self.pilha_operadores and self.pilha_operadores[-1] != '(':
                operador_old = self.pilha_operadores.pop()
                if operador_old == '+':
                    self.codigo.append('SC PUSHDOWN_SUM')
                elif operador_old == '-':
                    self.codigo.append('SC PUSHDOWN_DIF')
        self.pilha_operadores.append(operador)

    def vezes_ou_dividir(self, operador):
        if self.pilha_operadores:
            operador_old = self.pilha_operadores[-1]
            if operador_old == '*':
                self.codigo.append('SC PUSHDOWN_MUL')
                self.pilha_operadores.pop()
            elif operador_old == '/':
                self.codigo.append('SC PUSHDOWN_DIV')
                self.pilha_operadores.pop()
        self.pilha_operadores.append(operador)

    def recebe_operando_var(self, operando):
        s = self.tabela_simbolos.procurar(operando)
        if s is not None:
            self.load_val(s)
            # self.pilha_operandos.append(s)

    def recebe_operando_num(self, num):
        label = self.get_const_num_repr(num)
        # self.pilha_operandos.append(self.tabela_simbolos.procurar(label))
        self.load_val(self.tabela_simbolos.procurar(label))

    def finalizar_expressao_mat(self):
        if self.pilha_operadores:
            if (self.pilha_operadores[-1] == '*'
                or self.pilha_operadores[-1] =='/'):
                    self.sai_termo()
            if self.pilha_operadores and self.pilha_operadores[-1] != '(':
                operador_old = self.pilha_operadores.pop()
                if operador_old == '+':
                    self.codigo.append('SC PUSHDOWN_SUM')
                elif operador_old == '-':
                    self.codigo.append('SC PUSHDOWN_DIF')
        # self.__fp_em_base = False

    def abre_parenteses(self):
        self.pilha_operadores.append('(')

    def fecha_parenteses(self):
        # finaliza a expressão interna
        while self.pilha_operadores[-1] != '(':
            self.finalizar_expressao_mat()
        self.pilha_operadores.pop() # retira o '('

    def sai_termo(self):
        # termina a operacap de * ou /
        operador = self.pilha_operadores.pop()
        if operador == '*':
            self.codigo.append('SC PUSHDOWN_MUL')
        elif operador == '/':
            self.codigo.append('SC PUSHDOWN_DIV')
    # FIM EXPRESSÕES MATEMÁTICAS

    # CHAMADA DE FUNÇÃO
    def iniciar_frame(self):
        zero = False
        for b in range(0, self.__identificador_atual.tipo.tamanho, 2):
            if not zero:
                self.codigo.append('LD K_0000')
                zero = True
            self.codigo.append('SC PUSH')

    def chamar_funcao(self):
        # empilha o endereço de retorno
        self.codigo.append("LD {}".format(self.__func_atual.nome))
        self.codigo.append("SC PUSH")
        # empilha o FP
        self.codigo.append("LD FP")
        self.codigo.append("SC PUSH")
        # atualiza FP com seu novo valor
        self.codigo.append("LD SP")
        self.codigo.append("MM FP")
    # FIM CHAMADA DE FUNÇÃO

    # COMANDO SIMPLES
    def inicia_comando_simples(self, identificador):
        # procura o identificador na tabela
        s = self.tabela_simbolos.procurar(identificador)
        # se encontrou em algum escopo
        if s is not None:
            self.__identificador_atual = s
            self.__identificador_atual.utilizado = True

    def comando_atribuicao(self):
        self.finalizar_expressao_mat()
        if not self.__fp_em_base:
            self.codigo.append("LD FP")
            self.codigo.append("MM BASE")
        self.codigo.append("LD {}".format(self.get_const_num_repr(self.__identificador_atual.posicao)))
        self.codigo.append("SC PUSH")
        self.codigo.append("SC SET_VECT")
    # FIM COMANDO SIMPLES

    # CHAMADA DE PROCEDIMENTOS
    def call_func(self, nome_func):
        f = self.tabela_simbolos.procurar(nome_func)
        if f is not None:
            # salva o estado atual no frame record da função chamadora
            self.codigo.append("LD {}".format(self.__func_atual.nome))
            self.codigo.append("SC PUSH")
            self.codigo.append("LD FP")
            self.codigo.append("SC PUSH")
            # cria um novo frame record para a função chamada
            self.codigo.append("LD SP")
            self.codigo.append("MM FP")
            # agora a pilha está pronta para receber os parâmetros
            # que devem ser passados para a função chamada via frame record

    # FIM CHAMADA DE PROCEDIMENTOS
