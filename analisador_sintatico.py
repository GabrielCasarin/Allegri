# Copyright (c) 2016 Gabriel Casarin da Silva, All Rights Reserved.


class analise_sintatica(Simulador):
    def __init__(self, log_analise_sintatica=False):
        super(analise_sintatica, self).__init__()

    def __call__(self):
        if self.log_analise_sintatica:
            print('entrei na sub-rotina de análise sintática...')

        if self.log_analise_sintatica:
            print('saí da sub-rotina de análise sintática.')
