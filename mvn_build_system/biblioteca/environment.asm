; exportacoes
GET_VECT 	>
SET_VECT 	>
GET_OFFSET  >
SET_OFFSET  >
BASE 	>
PUSHDOWN_SUM	>
PUSHDOWN_DIF 	>
PUSHDOWN_MUL 	>
PUSHDOWN_DIV 	>

; importacoes
PUSH 		<
POP  		<
K_MM 		<
K_LD 		<


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
				- 		OFFSET
				+ 		K_LD
				MM 		LOAD_OFFSET
LOAD_OFFSET 	K 		/0000
				RS 		GET_OFFSET



SET_OFFSET 		$ 		=1
				; OFFSET
				SC 		POP
				MM 		OFFSET
				; BASE
				SC 		POP
				MM 		BASE

				LD 		BASE
				- 		OFFSET
				+ 		K_MM
				MM 		MOVE_OFFSET
				; desempilha o valor a ser atribuido
				SC 		POP
MOVE_OFFSET 	K 		/0000
				RS 		SET_OFFSET


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
