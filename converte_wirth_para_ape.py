# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


import os
import string
from configuracoes import *

from util.meta_reconhecedor import MetaReconhecedor
from util.minimizador import *

from analisador_lexico import decompoe_texto_fonte, classificador_lexico
from util.automatos_loaders import transdutor_finito

arquivo_saida = 'out.maquina'

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
print(automato_transdutor_tokenizador_de_wirth.saidas)

# analisador léxico
tokenizer = classificador_lexico(automato_transdutor_tokenizador_de_wirth, decompositor, log_analise_lexica)
tokenizer.add_classificacao('NT', 'NT')
tokenizer.add_classificacao('TERM', 'TERM')

# meta-reconhecedor, ou analisador sintático
mr = MetaReconhecedor(tokenizer, log=log_analise_sintatica)

mr('id.txt')

print(mr.chamadas_entre_submaquinas)

for nome_da_submaq, submaquina in mr.submaquinas.items():
    print('Submaquina atual:', nome_da_submaq)
    # print('ANTES')
    # for estado in submaquina.estados.values():
    #     print('{}'.format('*' if estado.isFinal() else ''), estado.nome, '=', estado._transicoes)
    eliminar_transicoes_em_vazio(submaquina)
    submaquina.gerar_alfabeto()
    eliminar_indeterminismos(submaquina)
    eliminar_estados_inacessiveis(submaquina)
    # print('\nDEPOIS')
    # for estado in submaquina.estados.values():
    #     print('{}'.format('*' if estado.isFinal() else ''), estado.nome, '=', estado._transicoes)
    submaquina.gerar_alfabeto()

    particao = minimizador_de_Hopcroft(submaquina)
    # print()
    # print('particao:', particao)

    # print()
    # print('alfabeto', submaquina.alfabeto)
    # print('classes de equivalencia')
    af = particao_para_automato_finito(nome_da_submaq, submaquina.alfabeto, particao)

    with open(os.path.join(ROOT_DIR, 'saida', arquivo_saida), 'w') as f:
        f.write('<{}>\n'.format(af.nome))

        # estados
        f.write(' '.join(af.estados.keys()) + '\n')

        # estado inicial
        f.write('{}\n'.format(af._estadoInicial.nome))

        # estados finais
        f.write(' '.join(af.finais()) + '\n')

        # alfabeto
        f.write(' '.join(af.alfabeto) + '\n')

        # transicoes
        for estado_atual in af.estados.values():
            for s in af.alfabeto:
                if estado_atual[s] is not None:
                    f.write("({}, '{}') -> {}\n".format(estado_atual.nome, s, estado_atual[s]))

        f.write('</{}>\n'.format(af.nome))
