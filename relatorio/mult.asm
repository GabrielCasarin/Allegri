PUSH    <
POP     <
SP      <
FP      <
TRUE    <
FALSE   <
AND     <
OR      <
NOT     <
GET_FROM_FRAME  <
SET_TO_FRAME    <
GET_FROM_VECT   <
SET_TO_VECT     <
PUSHDOWN_SUM    <
PUSHDOWN_DIF    <
PUSHDOWN_MUL    <
PUSHDOWN_DIV    <
GET_LENGTH      <
IGUAL           <
DIFERENTE       <
MAIOR           <
MAIOR_OU_IGUAL  <
MENOR           <
MENOR_OU_IGUAL  <
K_0000    <
K_0001    <
K_0002    <
K_FFFF    <
WORD_TAM  <
DIM_1     <
DIM_2     <
INIT_HEAP      <
NEW_ARRAY      <
NEW_MATRIX     <

; inicio do codigo
&     /0000
SC    INIT_HEAP
LD    SP
+     WORD_TAM
MM    FP
SC    main
FIM   HM FIM
; declaracao de CONSTANTES
K_0004	K /0004
K_0006	K /0006
K_0008	K /0008
K_FFF8	K /FFF8
K_FFFA	K /FFFA
K_FFFC	K /FFFC
K_000B	K /000B
K_000C	K /000C
K_000E	K /000E
K_0005	K /0005
; declaracao de FUNCOES
mult	$ =1
LD K_0000
SC PUSH  ; var i
LD K_0000
SC PUSH  ; var j
LD K_0000
SC PUSH  ; var k
LD K_0000
SC PUSH  ; var temp
LD    FP
SC    PUSH
LD    K_0002
*     K_FFFF
SC    PUSH
LD    K_0000
SC    PUSH
SC    SET_TO_VECT
mult_WHILE_1 + K_0000
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0002
SC    PUSH
SC MENOR
SC POP
JZ mult_END_WHILE_1
LD    FP
SC    PUSH
LD    K_0004
*     K_FFFF
SC    PUSH
LD    K_0000
SC    PUSH
SC    SET_TO_VECT
mult_WHILE_2 + K_0000
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC MENOR
SC POP
JZ mult_END_WHILE_2
LD    FP
SC    PUSH
LD    K_0006
*     K_FFFF
SC    PUSH
LD    K_0000
SC    PUSH
SC    SET_TO_VECT
LD    FP
SC    PUSH
LD    K_0008
*     K_FFFF
SC    PUSH
LD    K_0000
SC    PUSH
SC    SET_TO_VECT
mult_WHILE_3 + K_0000
LD    K_0006
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0002
SC    PUSH
SC MENOR
SC POP
JZ mult_END_WHILE_3
LD    FP
SC    PUSH
LD    K_0008
*     K_FFFF
SC    PUSH
LD    K_0008
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_FFF8
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_FFF8
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    GET_LENGTH
SC    PUSHDOWN_MUL
LD    K_0006
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0002
SC    PUSH
SC    PUSHDOWN_SUM
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
SC  GET_FROM_VECT
SC  PUSH
LD    K_FFFA
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0006
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_FFFA
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    GET_LENGTH
SC    PUSHDOWN_MUL
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0002
SC    PUSH
SC    PUSHDOWN_SUM
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
SC  GET_FROM_VECT
SC  PUSH
SC PUSHDOWN_MUL
SC PUSHDOWN_SUM
SC    SET_TO_VECT
LD    FP
SC    PUSH
LD    K_0006
*     K_FFFF
SC    PUSH
LD    K_0006
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC PUSHDOWN_SUM
SC    SET_TO_VECT
JP mult_WHILE_3
mult_END_WHILE_3 + K_0000
LD    K_FFFC
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_FFFC
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    GET_LENGTH
SC    PUSHDOWN_MUL
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0002
SC    PUSH
SC    PUSHDOWN_SUM
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
LD    K_0008
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
SC    SET_TO_VECT
LD    FP
SC    PUSH
LD    K_0004
*     K_FFFF
SC    PUSH
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC PUSHDOWN_SUM
SC    SET_TO_VECT
JP mult_WHILE_2
mult_END_WHILE_2 + K_0000
LD    FP
SC    PUSH
LD    K_0002
*     K_FFFF
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC PUSHDOWN_SUM
SC    SET_TO_VECT
JP mult_WHILE_1
mult_END_WHILE_1 + K_0000
RET_mult	LD  FP
-   WORD_TAM
MM  SP
RS	mult
main	$ =1
LD K_0002
MM DIM_1
LD K_0002
MM DIM_2
SC NEW_MATRIX
SC PUSH  ; var x
LD K_0002
MM DIM_1
LD K_0001
MM DIM_2
SC NEW_MATRIX
SC PUSH  ; var y
LD K_0002
MM DIM_1
LD K_0001
MM DIM_2
SC NEW_MATRIX
SC PUSH  ; var z
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0000
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    GET_LENGTH
SC    PUSHDOWN_MUL
LD    K_0000
SC    PUSH
LD    K_0002
SC    PUSH
SC    PUSHDOWN_SUM
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
LD    K_000B
SC    PUSH
SC    SET_TO_VECT
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0000
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    GET_LENGTH
SC    PUSHDOWN_MUL
LD    K_0001
SC    PUSH
LD    K_0002
SC    PUSH
SC    PUSHDOWN_SUM
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
LD    K_0001
SC    PUSH
SC    SET_TO_VECT
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    GET_LENGTH
SC    PUSHDOWN_MUL
LD    K_0000
SC    PUSH
LD    K_0002
SC    PUSH
SC    PUSHDOWN_SUM
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
LD    K_000C
SC    PUSH
SC    SET_TO_VECT
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    GET_LENGTH
SC    PUSHDOWN_MUL
LD    K_0001
SC    PUSH
LD    K_0002
SC    PUSH
SC    PUSHDOWN_SUM
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
LD    K_0008
SC    PUSH
SC    SET_TO_VECT
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0000
SC    PUSH
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    GET_LENGTH
SC    PUSHDOWN_MUL
LD    K_0000
SC    PUSH
LD    K_0002
SC    PUSH
SC    PUSHDOWN_SUM
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
LD    K_000E
SC    PUSH
SC    SET_TO_VECT
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    GET_LENGTH
SC    PUSHDOWN_MUL
LD    K_0000
SC    PUSH
LD    K_0002
SC    PUSH
SC    PUSHDOWN_SUM
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
LD    K_0005
SC    PUSH
SC    SET_TO_VECT
; espaco para valor de retorno
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
; par m1
LD    K_0004
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
; par m2
LD    K_0006
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
; par mr
LD main
SC PUSH
LD FP
SC PUSH
; troca o contexto
LD SP
+ WORD_TAM
MM FP
SC mult
; volta ao contexto anterior
SC POP ; restaura FP
MM FP
SC POP ; restaura end. de retorno
MM main
SC POP
SC POP
SC POP
; termina de desempilhar os parametros passados aa funcao
; resta o valor de retorno no topo da pilha
RET_main	LD  FP
-   WORD_TAM
MM  SP
RS	main
# FIM
