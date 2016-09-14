# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


from analisador_lexico import decompoe_texto_fonte, analisador_lexico, analise_sintatica
from analisador_semantico import gerar_codigo_intermediario, otimizador, gerar_codigo_objeto

import re
from comum import TransdutorFinito


# class gerar_codigo_executavel:
#     def __init__(self):
#         super(gerar_codigo_executavel, self).__init__()
#
#     def __call__(self):
#         print('entrei na sub-rotina de geração de código executável...')
#
#         print('saí da sub-rotina de geração de código executável...')


with open('conf.txt') as arq_conf:
    log_decompoe_texto_fonte = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_imprimir_linhas = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_imprimir_caracteres = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_analise_lexica = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False
    log_analise_sintatica = True if arq_conf.readline().split(' = ')[1][:-1] == '1' else False

with open('tokenizer_wirth.maquina') as arq:
    match_automato = re.compile(r'<(?P<nome>\w+)>(.*)</(?P=nome)>', re.DOTALL | re.MULTILINE)
    match_transicoes = re.compile(r"\(([a-zA-Z]\w*)\s*,\s*'(.+)'\s*\)\s*->\s*([a-zA-Z]\w*)(?:\s*\\\s*(\w+))?")
    texto = arq.read()
    mo1 = match_automato.search(texto)
    nome_automato = mo1.group(1)
    linhas = mo1.group(2).split('\n')

    linha_atual = 0

    while linhas[linha_atual] == '':
        linha_atual += 1
    estados = linhas[linha_atual].split()
    linha_atual += 1

    while linhas[linha_atual] == '':
        linha_atual += 1
    inicial = linhas[linha_atual]
    linha_atual += 1

    while linhas[linha_atual] == '':
        linha_atual += 1
    finais = linhas[linha_atual].split()
    linha_atual += 1

    while linhas[linha_atual] == '':
        linha_atual += 1
    alfabeto = linhas[linha_atual].split()

    tf = TransdutorFinito(nome=nome_automato, estados=estados, estadoInicial=inicial, estadosFinais=finais, alfabeto=alfabeto)

    for mo2 in match_transicoes.finditer(mo1.group(2)):
        qi, s, qj, saida = mo2.groups()
        tf.add_transicao(de=qi, com=s, para=qj)
        if saida is not None:
            tf.add_saida(de=qi, com=s, saida=saida)

# front end
d = decompoe_texto_fonte(log_decompoe_texto_fonte, log_imprimir_linhas, log_imprimir_caracteres)
anal = analisador_lexico(tf, d, log_analise_lexica)
anal.add_evento(('<PartidaInicial>', ))
anal.run()
print()
print('TOKENS')
print(anal.tokens)
##analise_sintatica(log_analise_sintatica)

# código intermediário
##gerar_codigo_intermediario()()
##otimizador()()
##gerar_codigo_objeto()()

# back end
##gerar_codigo_executavel()()
