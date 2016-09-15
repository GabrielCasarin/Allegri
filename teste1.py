from comum.automatos.AbstractAutomato import *
from util.minimizador import minimizador_Hopcroft

af = AbstractAutomato()
af['A']['0'] = 'B'
af['A']['1'] = 'F'

af['B']['0'] = 'G'
af['B']['1'] = 'C'

af['C']['0'] = 'A'
af['C']['1'] = 'C'

af['D']['0'] = 'D'
af['D']['1'] = 'E'

af['E']['0'] = 'H'
af['E']['1'] = 'F'

af['F']['0'] = 'C'
af['F']['1'] = 'G'

af['G']['0'] = 'G'
af['G']['1'] = 'E'

af['H']['0'] = 'G'
af['H']['1'] = 'C'

af['C'].setFinal()
af.gerar_alfabeto()

print(minimizador_Hopcroft(af))
