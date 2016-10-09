# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import os
import sys
import string
from configuracoes import *

from analisador_lexico import decompoe_texto_fonte, classificador_lexico
from util.automatos_loaders import transdutor_finito
from util.meta_reconhecedor import MetaReconhecedor
from util.minimizador import *


# leitor e classificador de caracteres do arquivo fonte
decompositor = decompoe_texto_fonte(log_decompoe_texto_fonte, log_imprimir_linhas, log_imprimir_caracteres)
# define as categorias possíveis em que os caracteres poderão ser classificados
decompositor.add_categoria('enter', ['\n'])
decompositor.add_categoria('espaco', ['\t', ' '])
decompositor.add_categoria('Letra', string.ascii_letters)
decompositor.add_categoria('Algarismo', string.digits)
for el in string.punctuation:
    decompositor.add_categoria(el, [el])

# cria o automato que reconhece os diversos tokens da linguagem
automato_transdutor_tokenizador_de_wirth = transdutor_finito(os.path.join(ROOT_DIR, 'Wirth', 'tokenizer_wirth.maquina'))

# analisador léxico
tokenizer = classificador_lexico(automato_transdutor_tokenizador_de_wirth, decompositor, log_analise_lexica)
tokenizer.add_classificacao('NT', 'NT')
tokenizer.add_classificacao('TERM', 'TERM')

# meta-reconhecedor, ou analisador sintático
mr = MetaReconhecedor(tokenizer, log=log_analise_sintatica)

# rotina MAIN
if __name__ == '__main__':
    arquivo_saida = 'out.maquina'
    if len(sys.argv) > 1:
        mr(os.path.join('.', sys.argv[1]))
    else:
        nome_input = input('Arquivo da Gramática: ')
        mr(nome_input)

    af = AutomatoFinito(nome='tokenizer')
    id_estados = 0
    canditados_a_inicial = []
    substituicoes = []
    submaquinas_geradas = {}

    for nome_da_submaq, submaquina in mr.submaquinas.items():
        submaquina.gerar_alfabeto()

        eliminar_transicoes_em_vazio(submaquina)

        eliminar_indeterminismos(submaquina)

        eliminar_estados_inacessiveis(submaquina)

        particao = minimizador_de_Hopcroft(submaquina)

        canditados_a_inicial.append('q' + str(id_estados))
        id_estados, transicoes_chamada, finais = particao_para_automato_finito(particao, inicial=id_estados, apendice=af)
        id_estados += 1
        submaquinas_geradas[nome_da_submaq] = (canditados_a_inicial[-1], finais)
        if transicoes_chamada: substituicoes += transicoes_chamada

    for qi_old, maq, qj_old in substituicoes:
        if qi_old in canditados_a_inicial:
            qi_novo, qjs_novos = submaquinas_geradas[maq]
            for qj_novo in qjs_novos:
                for s, qk in af[qj_old].transicoes.items():
                    if qk is not None:
                        af.add_transicao(qj_novo, s, qk.nome)
            canditados_a_inicial.remove(qi_old)
            del af.estados[qi_old]

    inicial = canditados_a_inicial.pop()

    for qi in canditados_a_inicial:
        for s, qk in af[qi].transicoes.items():
            if qk is not None:
                af.add_transicao(inicial, s, qk.nome)
        del af.estados[qi]

    af.set_inicial(inicial)
    af.alfabeto = set()
    af.gerar_alfabeto()

    with open(os.path.join(ROOT_DIR, 'saida', arquivo_saida), 'w') as f:

        f.write('<{}>\n'.format(af.nome))

        # estados
        f.write('    ' + ' '.join(af.estados.keys()) + '\n\n')

        # estado inicial
        f.write('    ' + '{}\n\n'.format(af._estadoInicial.nome))

        # estados finais
        f.write('    ' + ' '.join(af.finais()) + '\n\n')

        # alfabeto
        f.write('    ' + ' '.join(af.alfabeto_sem_chamada_de_submaquina) + '\n\n')

        # transicoes
        for estado_atual in af.estados.values():
            for s in af.alfabeto:
                if s in estado_atual.submaquinas_chamadas:
                    f.write('    ' + "{} => ({}, {})\n".format(estado_atual.nome, s, estado_atual[s]))
                elif estado_atual[s] is not None:
                    f.write('    ' + "({}, '{}') -> {}\n".format(estado_atual.nome, s, estado_atual[s]))

        f.write('</{}>\n'.format(af.nome))
