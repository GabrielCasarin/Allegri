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

    submaquinas_geradas = {}
    for nome_da_submaq, submaquina in mr.submaquinas.items():
        # print('Submaquina atual:', nome_da_submaq)
        submaquina.gerar_alfabeto()
        # print('ANTES')
        # for estado in submaquina.estados.values():
        #     print('{}'.format('*' if estado.final else ''), estado.nome, '=', estado.transicoes)

        eliminar_transicoes_em_vazio(submaquina)
        # print('\nDEPOIS de eliminar transições em vazio')
        # for estado in submaquina.estados.values():
        #     print('{}'.format('*' if estado.final else ''), estado.nome, '=', estado.transicoes)

        eliminar_indeterminismos(submaquina)
        # print('\nDEPOIS de eliminar indeterminismos')
        # for estado in submaquina.estados.values():
        #     print('{}'.format('*' if estado.final else ''), estado.nome, '=', estado.transicoes)

        eliminar_estados_inacessiveis(submaquina)
        # print('\nDEPOIS de eliminar estados inacessiveis')
        # for estado in submaquina.estados.values():
        #     print('{}'.format('*' if estado.final else ''), estado.nome, '=', estado.transicoes)

        particao = minimizador_de_Hopcroft(submaquina)
        # print()
        # print('particao:', particao)

        # print()
        # print('alfabeto', submaquina.alfabeto)
        # print('classes de equivalencia')
        af = particao_para_automato_finito(particao, nome=nome_da_submaq, alfabeto=submaquina.alfabeto)
        submaquinas_geradas[nome_da_submaq] = af


    with open(os.path.join(ROOT_DIR, 'saida', arquivo_saida), 'w') as f:
        if mr.eh_ape:
            f.write('<S>\n')
            f.write(' '.join(submaquinas_geradas.keys()) + '\n')
            f.write('{}\n'.format(list(submaquinas_geradas.keys())[0]))

        for af in submaquinas_geradas.values():
            f.write('<{}>\n'.format(af.nome))

            # estados
            f.write(' '.join(af.estados.keys()) + '\n')

            # estado inicial
            f.write('{}\n'.format(af._estadoInicial.nome))

            # estados finais
            f.write(' '.join(af.finais()) + '\n')

            # alfabeto
            f.write(' '.join(af.alfabeto_sem_chamada_de_submaquina) + '\n')

            # transicoes
            for estado_atual in af.estados.values():
                for s in af.alfabeto:
                    if s in estado_atual.submaquinas_chamadas:
                        f.write("{} => ({}, {})\n".format(estado_atual.nome, s, estado_atual[s]))
                    elif estado_atual[s] is not None:
                        f.write("({}, '{}') -> {}\n".format(estado_atual.nome, s, estado_atual[s]))

            f.write('</{}>\n'.format(af.nome))

        if mr.eh_ape:
            f.write('</S>\n')