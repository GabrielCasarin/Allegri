from util.mr2 import MetaReconhecedor
from util.minimizador import *
import string

mr = MetaReconhecedor(saida='automato_tokenizer.txt', log=False)

mr.add_evento(('<PartidaInicial>', ))
# submaquina NT
mr.add_evento(('<ChegadaSimbolo>', ('NT', 'NT')))
mr.add_evento(('<ChegadaSimbolo>', ('=', '=')))
mr.add_evento(('<ChegadaSimbolo>', ('Letra', 'TERM')))
mr.add_evento(('<ChegadaSimbolo>', ('{', '{')))
mr.add_evento(('<ChegadaSimbolo>', ('Letra', 'TERM')))
mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', ('Algarismo', 'TERM')))
mr.add_evento(('<ChegadaSimbolo>', ('}', '}')))
mr.add_evento(('<ChegadaSimbolo>', ('.', '.')))
# submaquina TERM
mr.add_evento(('<ChegadaSimbolo>', ('TERM', 'NT')))
mr.add_evento(('<ChegadaSimbolo>', ('=', '=')))
mr.add_evento(('<ChegadaSimbolo>', ('"', 'TERM')))
mr.add_evento(('<ChegadaSimbolo>', ('{', '{')))

mr.add_evento(('<ChegadaSimbolo>', ('Letra', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', ('Algarismo', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', ('(', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', (')', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', ('[', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', (']', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', ('{', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', ('}', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', ('|', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))
mr.add_evento(('<ChegadaSimbolo>', ('.', 'TERM')))
mr.add_evento(('<ChegadaSimbolo>', ('|', '|')))

mr.add_evento(('<ChegadaSimbolo>', ('"', 'TERM')))
mr.add_evento(('<ChegadaSimbolo>', ('"', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('}', '}')))

mr.add_evento(('<ChegadaSimbolo>', ('"', 'TERM')))

mr.add_evento(('<ChegadaSimbolo>', ('.', '.')))

mr.run()

# print('ANTES')
# for estado in mr.submaquinas['NT'].estados.values():
#     print('{}'.format('*' if estado.isFinal() else ''), estado.nome, '=', estado._transicoes)
for nome_da_submaq, submaquina in mr.submaquinas.items():
    print('Submaquina atual:', nome_da_submaq)
    eliminar_transicoes_em_vazio(submaquina)
    submaquina.gerar_alfabeto()
    eliminar_indeterminismos(submaquina)
    eliminar_estados_inacessiveis(submaquina)
    submaquina.gerar_alfabeto()
    print('alfabeto', submaquina.alfabeto)

    # print('\nDEPOIS')
    # for estado in submaquina.estados.values():
    #     print('{}'.format('*' if estado.isFinal() else ''), estado.nome, '=', estado._transicoes)

    particao = minimizador_de_Hopcroft(submaquina)
    # print('classes de equivalencia', particao)

    particao_para_automato_finito(particao)
