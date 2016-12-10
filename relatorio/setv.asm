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
K_FFFC	K /FFFC
K_000B	K /000B
; declaracao de FUNCOES
preencher	$ =1
LD K_0000
SC PUSH  ; var i
LD    FP
SC    PUSH
LD    K_0002
*     K_FFFF
SC    PUSH
LD    K_0000
SC    PUSH
SC    SET_TO_VECT
preencher_WHILE_1 + K_0000
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_FFFC
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD K_0000
SC PUSH
SC GET_LENGTH
SC MENOR
SC POP
JZ preencher_END_WHILE_1
LD    K_FFFC
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC    PUSHDOWN_SUM
LD    K_0002
SC    PUSH
SC    PUSHDOWN_MUL
LD    K_0002
SC    PUSH
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
SC PUSHDOWN_MUL
LD    K_0001
SC    PUSH
SC PUSHDOWN_SUM
SC    SET_TO_VECT
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
JP preencher_WHILE_1
preencher_END_WHILE_1 + K_0000
RET_preencher	LD  FP
-   WORD_TAM
MM  SP
RS	preencher
main	$ =1
LD K_000B
MM DIM_1
SC NEW_ARRAY
SC PUSH  ; var x
; espaco para valor de retorno
LD    K_0002
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
; par m1
LD main
SC PUSH
LD FP
SC PUSH
; troca o contexto
LD SP
+ WORD_TAM
MM FP
SC preencher
; volta ao contexto anterior
SC POP ; restaura FP
MM FP
SC POP ; restaura end. de retorno
MM main
SC POP
; termina de desempilhar os parametros passados aa funcao
; resta o valor de retorno no topo da pilha
RET_main	LD  FP
-   WORD_TAM
MM  SP
RS	main
# FIM
