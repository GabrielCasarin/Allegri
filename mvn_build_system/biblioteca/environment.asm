; exportacoes
GET_VECT 	>
SET_VECT 	>
GET_OFFSET  >
SET_OFFSET  >
BASE 		>
PUSHDOWN_SUM	>
PUSHDOWN_DIF 	>
PUSHDOWN_MUL 	>
PUSHDOWN_DIV 	>
GET_LENGTH 		>
ACC_AUX 		>

; importacoes
PUSH 		<
POP  		<
K_MM 		<
K_LD 		<
WORD_TAM 	<


			& 		/0000


ACC_AUX		$		=1

BASE 		$ 		=1
OFFSET 		$		=1



; =====================================
;  OPERACOES SOBRE POSICOES DE MEMORIA
; =====================================

GET_VECT	  	$ 		=1
				; desempilha o parametro
				; OFFSET
				SC 		POP
				MM 		OFFSET

				; corpo da função
				LD		BASE
				-		OFFSET
				+		K_LD
				MM		LOAD
LOAD			K 		/0000
				RS 		GET_VECT



SET_VECT 		$		=1
				; desempilha os parametros
				; OFFSET
				SC 		POP
				MM 		OFFSET

				LD		BASE
				- 		OFFSET
				+		K_MM
				MM 		MOVE
				; desempilha o valor a ser atribuido
				SC 		POP
MOVE 			K 		/0000
				RS 		SET_VECT



GET_OFFSET 		$ 		=1
				; OFFSET
				SC 		POP
				MM 		OFFSET
				; BASE
				SC 		POP
				MM 		BASE

				LD 		BASE
				+ 		OFFSET
				+ 		K_LD
				MM 		LOAD_OFFSET
LOAD_OFFSET 	K 		/0000
				RS 		GET_OFFSET



SET_OFFSET 		$ 		=1
				; BASE
				SC 		POP
				MM 		BASE
				; desempilha o valor a ser atribuido
				SC 		POP
				MM 		ACC_AUX
				; OFFSET
				SC 		POP
				* 		WORD_TAM
				MM 		OFFSET

				LD 		BASE
				+ 		OFFSET
				+ 		K_MM
				MM 		MOVE_OFFSET
				LD 		ACC_AUX
MOVE_OFFSET 	K 		/0000
				RS 		SET_OFFSET



GET_LENGTH      $       =1
				; dim
				LD 		WORD_TAM
				SC 		PUSH
				SC 		PUSHDOWN_MUL
				; calcula a instrucao
				SC 		PUSHDOWN_SUM
				SC 		POP
				+ 		K_LD
				MM 		LOAD_GET_LENGTH
LOAD_GET_LENGTH $ 		=1
				SC 		PUSH
				RS 		GET_LENGTH


; =====================================
;  OPERACOES SOBRE OPERANDOS NA PILHA
; =====================================

PUSHDOWN_SUM 	$ 		=1
				SC 		POP
				MM 		ACC_AUX
				SC 		POP
				+ 		ACC_AUX
				SC 		PUSH
				RS 		PUSHDOWN_SUM

PUSHDOWN_DIF 	$ 		=1
				SC 		POP
				MM 		ACC_AUX
				SC 		POP
				- 		ACC_AUX
				SC 		PUSH
				RS 		PUSHDOWN_DIF

PUSHDOWN_MUL 	$ 		=1
				SC 		POP
				MM 		ACC_AUX
				SC 		POP
				* 		ACC_AUX
				SC 		PUSH
				RS 		PUSHDOWN_MUL

PUSHDOWN_DIV 	$ 		=1
				SC 		POP
				MM 		ACC_AUX
				SC 		POP
				/ 		ACC_AUX
				SC 		PUSH
				RS 		PUSHDOWN_DIV


# ENV
