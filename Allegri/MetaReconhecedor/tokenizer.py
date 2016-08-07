import string
from Allegri.MetaReconhecedor import AutomatoFinito

num_estados = 15

def tokenizer(cadeia):
    estados = ['q'+str(i) for i in range(num_estados)]
    reconhecedor = AutomatoFinito(nome='reconhecedor', estados=estados, estadoInicial='q0', estadosFinais=['q3'] + ['q'+str(i) for i in range(5,num_estados)], alfabeto=list(string.ascii_lowercase + string.ascii_uppercase + string.digits + '=()[]}{|."'))

    reconhecedor['q0']['='] = reconhecedor['q13']
    reconhecedor['q0']['('] = reconhecedor['q5']
    reconhecedor['q0'][')'] = reconhecedor['q6']
    reconhecedor['q0']['['] = reconhecedor['q7']
    reconhecedor['q0'][']'] = reconhecedor['q8']
    reconhecedor['q0']['{'] = reconhecedor['q9']
    reconhecedor['q0']['}'] = reconhecedor['q10']
    reconhecedor['q0']['|'] = reconhecedor['q11']
    reconhecedor['q0']['.'] = reconhecedor['q12']
    # inicio de terminal
    reconhecedor['q0']['"'] = reconhecedor['q1']
    # caractere " do meio
    reconhecedor['q1']['"'] = reconhecedor['q2']
    # caractere " do fim
    reconhecedor['q2']['"'] = reconhecedor['q3']
    reconhecedor['q4']['"'] = reconhecedor['q3']

    # letras minusculas
    for caractere in string.ascii_lowercase:
        # não-terminais
        reconhecedor['q0'][caractere] = reconhecedor['q14']
        reconhecedor['q14'][caractere] = reconhecedor['q14']
        # terminais
        reconhecedor['q1'][caractere] = reconhecedor['q4']
        reconhecedor['q4'][caractere] = reconhecedor['q4']
    # letras maiusculas
    for caractere in string.ascii_uppercase:
        # não-terminais
        reconhecedor['q0'][caractere] = reconhecedor['q14']
        reconhecedor['q14'][caractere] = reconhecedor['q14']
        # terminais
        reconhecedor['q1'][caractere] = reconhecedor['q4']
        reconhecedor['q4'][caractere] = reconhecedor['q4']
    # digitos
    for caractere in string.digits:
        # não-terminais
        reconhecedor['q14'][caractere] = reconhecedor['q14']
        # terminais
        reconhecedor['q1'][caractere] = reconhecedor['q4']
        reconhecedor['q4'][caractere] = reconhecedor['q4']

    status = 'inicio'
    token = ''
    i = 0
    reconhecedor.inicializar()
    while i < len(cadeia):
        reconhecedor.atualizarSimbolo(cadeia[i])
        # estadoAnterior, _ = reconhecedor.mConfiguracao()
        if reconhecedor.fazerTransicao():
            estadoAtual, _ = reconhecedor.mConfiguracao()
            if status == 'inicio':
                token += cadeia[i]
                if estadoAtual.isFinal():
                    status = 'atingiu final'
                else:
                    status = 'transito'
            elif status == 'transito':
                token += cadeia[i]
                if estadoAtual.isFinal():
                    status = 'atingiu final'
            elif status == 'atingiu final':
                token += cadeia[i]
            i += 1
        else:
            # if estadoAnterior.isFinal():
            if status == 'atingiu final':
                    status = 'inicio'
                    reconhecedor.inicializar()
                    print(token)
                    token = ''
    if status == 'atingiu final':
            status = 'inicio'
            reconhecedor.inicializar()
            print(token)
            token = ''


if __name__ == '__main__':
    tokenizer('"abc"oi[({|.})]')
