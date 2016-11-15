; exportacoes
GET_VECT 	>
SET_VET 	>
GET_OFFSET  >
SET_OFFSET  >
ACC_AUX 	>

; importacoes
PUSH 		<
POP  		<
K_MM 		<
K_LD 		<


			& 		/0000


ACC_AUX		$		=1

BASE 		$ 		=1
OFFSET 		$		=1
TAM			$ 		=1


GET_VECT  	$ 		=1
			; desempilha os parametros
			; TAM
			SC		POP
			MM 		TAM
			; OFFSET
			SC 		POP
			MM 		OFFSET
			; BASE
			SC 		POP
			MM 		BASE

			; corpo da função
			LD 		OFFSET
			*		TAM
			MM 		ACC_AUX
			LD		BASE
			-		ACC_AUX
			+		K_LD
			MM		LOAD
LOAD		K 		/0000
			RS 		GET_VECT



SET_VET 	$		=1
			; desempilha os parametros
			; TAM
			SC		POP
			MM 		TAM
			; OFFSET
			SC 		POP
			MM 		OFFSET
			; BASE
			SC 		POP
			MM 		BASE

			LD 		OFFSET
			*		TAM
			MM 		ACC_AUX
			LD		BASE
			- 		ACC_AUX
			+		K_MM
			MM 		MOVE
			; desempilha o valor a ser atribuido
			SC 		POP
MOVE 		K 		/0000
			RS 		SET_VET


GET_OFFSET 	$ 		=1
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
LOAD_OFFSET K 		/0000
			RS 		GET_OFFSET


SET_OFFSET 	$ 		=1
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
MOVE_OFFSET K 		/0000
			RS 		SET_OFFSET

# ENV
