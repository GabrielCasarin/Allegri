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
K_0015	K /0015
K_002D	K /002D
K_0004	K /0004
K_0006	K /0006
; declaracao de FUNCOES
main	$ =1
LD K_0000
SC PUSH  ; var b
LD K_0000
SC PUSH  ; var c
LD K_0015
MM DIM_1
LD K_002D
MM DIM_2
SC NEW_MATRIX
SC PUSH  ; var a
LD    FP
SC    PUSH
LD    K_0004
*     K_FFFF
SC    PUSH
LD    K_0006
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0000
SC    PUSH
SC GET_LENGTH
SC    SET_TO_VECT
LD    FP
SC    PUSH
LD    K_0002
*     K_FFFF
SC    PUSH
LD    K_0006
SC    PUSH
SC    GET_FROM_FRAME
SC    PUSH
LD    K_0001
SC    PUSH
SC GET_LENGTH
SC    SET_TO_VECT
RET_main	LD  FP
-   WORD_TAM
MM  SP
RS	main
# FIM
