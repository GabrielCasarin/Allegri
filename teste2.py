from comum import AutomatoPilhaEstruturado


# af = AutomatoFinito(nome='grammar', estados=['q0', 'q2', 'q3', 'q4', 'q5'], estadoInicial='q0', estadosFinais=['q5'])
# af['q0']['NT'] = af['q2']
# af['q2']['='] = af['q3']
# af['q4']['.'] = af['q5']
# af['q5']['NT'] = af['q2']


ap = AutomatoPilhaEstruturado(nome='wirth', sub_maquinas=['grammar', 'exp'])
ap['grammar'].add_transicao('q0', 'NT', 'q2')
ap['grammar'].add_transicao('q2', '=',  'q3')
ap['grammar'].add_transicao('q4', '.',  'q5')
ap['grammar'].add_transicao('q5', 'NT', 'q2')
ap['grammar']['q3'][''] = (ap['exp'], ap['grammar']['q4'])
ap['grammar'].set_inicial('q0')
ap['grammar']['q5'].setFinal()

ap['exp'].add_transicao('q0', '(', 'q5')
ap['exp'].add_transicao('q0', '[', 'q8')
ap['exp'].add_transicao('q0', '{', 'q11')
ap['exp'].add_transicao('q1', '(', 'q5')
ap['exp'].add_transicao('q1', '[', 'q8')
ap['exp'].add_transicao('q1', '{', 'q11')
ap['exp'].add_transicao('q6', ')', 'q1')
ap['exp'].add_transicao('q6', ']', 'q1')
ap['exp'].add_transicao('q6', '}', 'q1')
ap['exp'].add_transicao('q0', 'NT', 'q1')
ap['exp'].add_transicao('q0', 'TERM', 'q1')
ap['exp'].add_transicao('q1', 'NT', 'q1')
ap['exp'].add_transicao('q1', 'TERM', 'q1')
ap['exp'].add_transicao('q1', '|', 'q0')

ap['exp']['q5'][''] = (ap['exp'], ap['exp']['q6'])
ap['exp']['q8'][''] = (ap['exp'], ap['exp']['q9'])
ap['exp']['q11'][''] = (ap['exp'], ap['exp']['q12'])
ap['exp'].set_inicial('q0')
ap['exp']['q1'].setFinal()

ap.set_submaquina_inicial('grammar')
ap.inicializar()
ap._AutomatoPilhaEstruturado__maquinaAtual.atualizarSimbolo('NT')
ap._AutomatoPilhaEstruturado__maquinaAtual.fazerTransicao()
ap._AutomatoPilhaEstruturado__maquinaAtual.atualizarSimbolo('=')
ap._AutomatoPilhaEstruturado__maquinaAtual.fazerTransicao()