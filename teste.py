from util.mr2 import MetaReconhecedor
from util.minimizador import *

mr = MetaReconhecedor()
mr.add_evento(('regra', 'id'))
mr.add_evento(('sinal', '='))
mr.add_evento(('terminal', '0'))
mr.add_evento(('terminal', 'x'))
mr.add_evento(('terminal', 'F'))
mr.add_evento(('sinal', '{'))
mr.add_evento(('terminal', 'F'))
mr.add_evento(('sinal', '}'))
mr.add_evento(('sinal', '.'))

mr.run()

tabela = gera_tabela(mr.transicoes)
estados = list(tabela.values())
alfabeto = ['0', 'x', 'F']
for q in estados:
    print(q.nome, q._transicoes)
eliminar_transicoes_em_vazio(estados, alfabeto)
estados2 = eliminar_indeterminismos(estados)
estados3 = eliminar_estados_inacessiveis(estados2, tabela['q0'])
