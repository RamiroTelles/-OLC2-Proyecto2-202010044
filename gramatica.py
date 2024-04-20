
from errores import error
listaErrores =[]

reservadas = {
    'console':'CONSOLE',
    'log':'LOG',
    'true':'TRUE',
    'false':'FALSE',
    'null':'NULL',
    'var':'VAR',
    'const':'CONST',
    'number': 'NUMBER',
    'float':'FLOAT',
    'string': 'STRING',
    'boolean':'BOOLEAN',
    'char': 'CHAR',
    'if':'IF',
    'else' : 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': "DEFAULT",
    'continue': 'CONTINUE',
    'break': 'BREAK',
    'return': 'RETURN',
    'function': 'FUNCTION',
    'interface': 'INTERFACE',
    'typeof': 'TYPEOF'
}

# Lista de tokens
tokens = [
   
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAVIZQ',
    'LLAVDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'EQUIVALENTE',
    'DISTINTO',
    'NOT',
    'OR',
    'AND',
    'PUNTO',
    'PUNTOCOMA',
    'DOSPUNTOS',
    'INTERROGACION',
    'COMA',
    'ID',
    'CADENA',
    'ENTERO',
    'DECIMAL',
    'CARACTER',
    'COMMENTBLOCK'
 ] + list(reservadas.values())

#t_CONSOLE   = r'console'
#t_LOG       = r'log'
#t_TRUE      = r'true'
#t_FALSE     = r'false'
#t_VAR       = r'var'
#t_NUMBER    = r'number'
#t_FLOAT     = r'float'
#t_STRING    = r'string'
#t_BOOLEAN   = r'boolean'
#t_CHAR      = r'char'
t_IGUAL     = r'='
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_LLAVIZQ   = r'{'
t_LLAVDER   = r'}'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_MODULO    = r'%'
t_MAYOR     = r'>'
t_MENOR     = r'<'
t_MAYORIGUAL    = r'>='
t_MENORIGUAL    = r'<='
t_EQUIVALENTE   = r'=='
t_DISTINTO  = r'!='
t_NOT       = r'!'
t_OR        = r'\|\|'
t_AND       = r'&&' 
t_PUNTO    = r'\.'
t_PUNTOCOMA     = r';'
t_DOSPUNTOS     = r':'
t_INTERROGACION = r'\?'
t_COMA          = r','

def t_CADENA(t):
    r'\"([^\"]*)\"'
    try:
        t.value = str(t.value)
    except ValueError:
        print("Error %d", t.value)
        t.value = ''
    return t

def t_CARACTER(t):
    r'\'(.?)\''
    try:
        t.value = str(t.value)
    except ValueError:
        print("Error %d", t.value)
        t.value = ''
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t



def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*' 
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t

t_ignore = " \t"

t_ignore_COMMENTLINE = r'\/\/.*'

def t_ignore_COMMENTBLOCK(t):
    r'\/\*[^*]*\*+(?:[^/*][^*]*\*+)*\/'
    t.lexer.lineno += t.value.count('\n')  


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

    

def t_error(t):
    listaErrores.append(error("Error lexico del valor" + str(t.value[0]),t.lexer.lineno,t.lexer.lexpos,"lexico"))
    print("Error Léxico '%s'" % t.value[0])
    t.lexer.skip(1)


from instrucciones import *
from expresiones import *
#Gramatica ------------------------------------------------------------------


def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t):
    '''instrucciones    : instrucciones instruccion'''
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_instruccion(t) :
    '''instruccion      : imprimir_instr
                        | declaracion
                        | asignacion PUNTOCOMA
                        | sIf
                        | sWhile
                        | sFor
                        | sContinue
                        | sBreak
                        | sReturn
                        | sSwitch
                        | declaracion_Funcion
                        | callFuncion PUNTOCOMA
                        | argumento_Funcion PUNTOCOMA'''
    t[0] = t[1]

def p_callArgumento_Funcion(t):
    '''argumento_Funcion    : ID PUNTO ID PARIZQ venir_Expresiones'''
    if t[3]== "push":
        t[0] = funcionPush(t[1],t[5])
    elif t[3]== "pop":
        t[0] = funcionPop(t[1])
    elif t[3]== "indexOf":
        t[0] = funcionIndexOf(t[1],t[5])
    elif t[3]== "join":
        t[0] = funcionJoin(t[1])
    elif t[3]== "toString":
        t[0] = funcionToString(ExpresionID(t[1]))
    elif t[3]== "toLowerCase":
        t[0] = funcionToLowerCase(ExpresionID(t[1]))
    elif t[3]== "toUpperCase":
        t[0] = funcionToUpperCase(ExpresionID(t[1]))
    
    
def p_accesoArgumento(t):
    '''accesoArgumento  : ID PUNTO ID'''
    if t[3]== "length":
        t[0] = funcionLength(t[1])


def p_callFuncion(t):
    '''callFuncion  : ID PARIZQ venir_Expresiones'''
    if t[1]== "parseInt":
        t[0] = funcionParseInt(t[3])
    elif t[1]== "parseFloat":
        t[0] = funcionParseFloat(t[3])
    else:
        t[0]= call_func(t[1],t[3])

def p_venir_Expresiones1(t):
    '''venir_Expresiones    : lista_Expresiones PARDER'''
    t[0]= t[1]

def p_venir_Expresiones2(t):
    '''venir_Expresiones    : PARDER'''
    t[0]=[]



def p_lista_Expresiones1(t):
    '''lista_Expresiones    : lista_Expresiones COMA op_Ternario'''
    t[1].append(t[3])
    t[0]=t[1]

def p_lista_Expresiones2(t):
    '''lista_Expresiones    : op_Ternario'''
    t[0] = [t[1]]

def p_declaracion_funcion(t):
    '''declaracion_Funcion  : FUNCTION ID PARIZQ parametros tipoFuncion instrucciones LLAVDER'''
    t[0] = guardar_func(t[2],t[4],t[5],t[6])

def p_parametros1(t):
    '''parametros   : PARDER '''
    t[0]=[]

def p_parametros2(t):
    '''parametros   : lista_Parametros PARDER'''
    t[0] = t[1]

def p_lista_Parametros1(t):
    '''lista_Parametros : lista_Parametros COMA ID DOSPUNTOS tipo
                        | ID DOSPUNTOS tipo'''
    if len(t)==6:
        t[1].append(DeclaracionExplicita(t[3],ExpresionNull(),t[5]))
        t[0] = t[1]
    elif len(t)==4:   
        t[0] = [DeclaracionExplicita(t[1],ExpresionNull(),t[3])]
    

def p_lista_Parametros2(t):
    '''lista_Parametros : lista_Parametros COMA ID DOSPUNTOS tipo CORIZQ CORDER
                        | ID DOSPUNTOS tipo CORIZQ CORDER'''
    if len(t)==6:
        t[0] = [DeclaracionExplicita(t[1],ExpresionNull(),t[3],False,1)]
        
    elif len(t)==8:   
        t[1].append(DeclaracionExplicita(t[3],ExpresionNull(),t[5],False,1))
        t[0] = t[1]
    
def p_tipoFuncion(t):
    '''tipoFuncion  : DOSPUNTOS tipo LLAVIZQ
                    | LLAVIZQ'''
    if len(t)==4:
        t[0]=t[2]
    elif len(t)==2:
        t[0]= TIPOS_P.VOID



def p_sSwitch(t):
    '''sSwitch  : SWITCH PARIZQ op_Ternario PARDER LLAVIZQ listCases LLAVDER'''
    t[0]= inst_switch(t[3],t[6][0],t[6][1])

def p_listCases1(t):
    '''listCases    : listCases CASE op_Ternario DOSPUNTOS instrucciones'''
    t[1][0].append(t[3])
    t[1][1].append(t[5])
    t[0]=t[1]


def p_listCases2(t):
    '''listCases    : listCases DEFAULT DOSPUNTOS instrucciones'''
    t[1][0].append(None)
    t[1][1].append(t[4])
    t[0]=t[1]
    

def p_listCases3(t):
    '''listCases    : CASE op_Ternario DOSPUNTOS instrucciones
                    | DEFAULT DOSPUNTOS instrucciones'''
    if len(t)==5:
        t[0] = [[t[2]],[t[4]]]
    elif len(t)==4:
        t[0] = [[ExpresionNull()],[t[3]]]

    

    

def p_sContinue(t):
    '''sContinue    : CONTINUE PUNTOCOMA'''
    t[0]= inst_Continue()

def p_sBreak(t):
    '''sBreak    : BREAK PUNTOCOMA'''
    t[0]= inst_Break()

def p_sReturn1(t):
    '''sReturn    : RETURN PUNTOCOMA'''
    t[0]= inst_Return(ExpresionNull())

def p_sReturn2(t):
    '''sReturn    : RETURN op_Ternario PUNTOCOMA'''
    t[0]= inst_Return(t[2])

def p_sFor(t):
    '''sFor : FOR PARIZQ declaracion op_Ternario PUNTOCOMA asignacion PARDER LLAVIZQ instrucciones LLAVDER'''
    t[0]= inst_for([t[3]],t[4],[t[6]],t[9])

def p_sWhile(t):
    '''sWhile   : WHILE PARIZQ op_Ternario PARDER LLAVIZQ instrucciones LLAVDER'''
    t[0] = inst_while(t[3],t[6])

def p_sIf1(t):
    '''sIf  : IF PARIZQ op_Ternario PARDER LLAVIZQ instrucciones sIf2'''
    t[0] = inst_if(t[3],t[6],t[7])

def p_sIf2_1(t):
    '''sIf2  : LLAVDER ELSE sElse'''
    t[0]=t[3]

def p_sIf2_2(t):
    '''sIf2  : LLAVDER'''
    t[0]= []

def p_sElse1(t):
    '''sElse    : LLAVIZQ instrucciones LLAVDER'''
    t[0]= t[2]

def p_sElse2(t):
    '''sElse    : sIf'''
    t[0]=[t[1]]

def p_asignacion1(t):
    '''asignacion   : ID IGUAL op_Ternario
                    | ID MAS IGUAL op_Ternario
                    | ID MENOS IGUAL op_Ternario
                    | ID CORIZQ op_Ternario CORDER IGUAL op_Ternario'''
    
    if t[2]=='=':
        t[0] = Asignacion(t[1],t[3])
    elif t[2]=='+':
        t[0]=Asignacion( t[1],ExpresionBinaria(ExpresionID(t[1]),t[4],OPERACION_ARITMETICA.MAS))
    elif t[2]=='-':
        t[0]=Asignacion( t[1],ExpresionBinaria(ExpresionID(t[1]),t[4],OPERACION_ARITMETICA.MENOS))
    elif t[2]== '[':
        t[0]= AsignacionArray(t[1],t[3],t[6])

def p_asignacion3(t):
    '''asignacion   : ID CORIZQ op_Ternario CORDER listaAccesos IGUAL op_Ternario'''
    lista=[t[3]]
    lista.extend(t[5])
    t[0] = AsignacionMatriz(t[1],lista,t[7])

def p_listaAccesos1(t):
    '''listaAccesos : listaAccesos CORIZQ op_Ternario CORDER'''
    t[1].append(t[3])
    t[0]=t[1]

def p_listaAccesos2(t):
    '''listaAccesos : CORIZQ op_Ternario CORDER'''
    t[0]= [t[2]]

def p_asignacion2(t):
    '''asignacion   : ID MAS MAS
                    | ID MENOS MENOS'''
    if t[3]=='+':
        t[0]= Asignacion(t[1],ExpresionBinaria(ExpresionID(t[1]),ExpresionEntero(1),OPERACION_ARITMETICA.MAS))
    elif t[3]=='-':
        t[0]= Asignacion(t[1],ExpresionBinaria(ExpresionID(t[1]),ExpresionEntero(1),OPERACION_ARITMETICA.MENOS))  


def p_declaracion1(t):
    '''declaracion  : tipoVar ID DOSPUNTOS tipo declaracion_explicita'''
    

    if t[1]=='const':
        t[0]= DeclaracionExplicita(t[2],t[5],t[4],True)
    else:
        t[0]= DeclaracionExplicita(t[2],t[5],t[4])
    
def p_declaracion2(t):
    '''declaracion  : tipoVar ID DOSPUNTOS tipo lista_Corchetes declaracion_explicita'''
    
    if t[1]=='const':
        t[0]= DeclaracionExplicita(t[2],t[6],t[4],True,t[5])
    else:
        t[0]= DeclaracionExplicita(t[2],t[6],t[4],False,t[5])

def p_declaracion3(t):
    '''declaracion  : tipoVar ID declaracion_implicita'''
    if t[1]=='const':
        t[0]= DeclaracionImplicita(t[2],t[3],True)
    else:
        t[0]= DeclaracionImplicita(t[2],t[3])

def p_Lista_Corchetes1(t):
    '''lista_Corchetes  : lista_Corchetes CORIZQ CORDER'''
    t[0] = t[1] +1

def p_Lista_Corchetes2(t):
    '''lista_Corchetes  : CORIZQ CORDER'''
    t[0] = 1
    
def p_declaracion_explicita1(t):
    '''declaracion_explicita    : PUNTOCOMA'''
    t[0] = None

def p_declaracion_explicita2(t):
    '''declaracion_explicita    : IGUAL op_Ternario PUNTOCOMA'''
    t[0]= t[2]
    

def p_declaracion_implicita(t):
    '''declaracion_implicita    : IGUAL op_Ternario PUNTOCOMA'''
    t[0] = t[2]

def p_tipoVar(t):
    '''tipoVar  : VAR
                | CONST'''
    t[0]=t[1]


def p_tipoNumber(t):
    '''tipo : NUMBER'''
    t[0]=TIPOS_P.ENTERO

def p_tipoFloat(t):
    '''tipo : FLOAT'''
    t[0]=TIPOS_P.FLOAT

def p_tipoString(t):
    '''tipo : STRING'''
    t[0]=TIPOS_P.CADENA

def p_tipoBoolean(t):
    '''tipo : BOOLEAN'''
    t[0]=TIPOS_P.BOOLEAN

def p_tipoChar(t):
    '''tipo : CHAR'''
    t[0]=TIPOS_P.CHAR



def p_instruccion_console(t):
    '''imprimir_instr : CONSOLE PUNTO LOG PARIZQ lista_exp PARDER PUNTOCOMA'''
    t[0] = Imprimir(t[5])

def p_lista_exp1(t):
    '''lista_exp    : lista_exp COMA op_Ternario'''
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_exp2(t):
    '''lista_exp    : op_Ternario'''
    t[0]=[t[1]]

def p_op_Ternario1(t):
    '''op_Ternario  : exp_Or INTERROGACION exp_Or DOSPUNTOS exp_Or'''
    t[0] = ExpresionTernaria(t[1],t[3],t[5])

def p_op_Ternario2(t):
    '''op_Ternario  : exp_Or'''
    t[0] = t[1]

def p_op_Ternario3(t):
    '''op_Ternario  : TYPEOF op_Ternario'''
    t[0] = funcionTypeOf(t[2])

def p_exp_Or1(t):
    '''exp_Or   : exp_Or OR exp_And'''
    t[0] = ExpresionLogica(t[1],t[3],OPERACION_LOGICA.OR)


def p_exp_Or2(t):
    '''exp_Or   : exp_And'''
    t[0] = t[1]

def p_exp_And1(t):
    '''exp_And   : exp_And AND exp_Not'''
    t[0] = ExpresionLogica(t[1],t[3],OPERACION_LOGICA.AND)

def p_exp_And2(t):
    '''exp_And   : exp_Not'''
    t[0]=t[1]



def p_exp_Not1(t):
    '''exp_Not  : lNot exp_Comp'''
    if t[1]%2==0:
        t[0] = t[2]
    else:
        t[0]= ExpresionNot(t[2])

def p_expNot2(t):
    '''exp_Not  : exp_Comp'''
    t[0]=t[1]

def p_listaNot1(t):
    '''lNot : lNot NOT'''
    t[0]= t[1]+1

def p_listaNot2(t):
    '''lNot : NOT'''
    t[0]=1

def p_exp_Comp1(t):
    '''exp_Comp : exp_Sum_Menos EQUIVALENTE exp_Sum_Menos
                | exp_Sum_Menos DISTINTO exp_Sum_Menos'''
    if t[2] == '=='  : t[0] = ExpresionRelacional(t[1], t[3], OPERACION_REL.IGUAL)
    elif t[2] == '!=': t[0] = ExpresionRelacional(t[1], t[3], OPERACION_REL.NO_IGUAL)
    
def p_exp_Comp2(t):
    '''exp_Comp    : exp_rel'''
    t[0]=t[1]

def p_exp_rel1(t):
    '''exp_rel  : exp_Sum_Menos MAYOR exp_Sum_Menos
                | exp_Sum_Menos MENOR exp_Sum_Menos
                | exp_Sum_Menos MAYORIGUAL exp_Sum_Menos
                | exp_Sum_Menos MENORIGUAL exp_Sum_Menos'''
    if t[2] == '>'  : t[0] = ExpresionRelacional(t[1], t[3], OPERACION_REL.MAYOR_QUE)
    elif t[2] == '<': t[0] = ExpresionRelacional(t[1], t[3], OPERACION_REL.MENOR_QUE)
    elif t[2] == '>=': t[0] = ExpresionRelacional(t[1], t[3], OPERACION_REL.MAYORIGUAL)
    elif t[2] == '<=': t[0] = ExpresionRelacional(t[1], t[3], OPERACION_REL.MENORIGUAL)
    
def p_exp_rel2(t):
    '''exp_rel    : exp_Sum_Menos'''
    t[0]=t[1]

def p_exp_sum_menos1(t):
    '''exp_Sum_Menos    : exp_Sum_Menos MAS exp_Mul_Div
                        | exp_Sum_Menos MENOS exp_Mul_Div'''
    
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)
    elif t[2] == '-': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS)
    
def p_exp_Sum_Menos2(t):
    '''exp_Sum_Menos    : exp_Mul_Div'''
    t[0]=t[1]


def p_exp_Mul_Div1(t):
    '''exp_Mul_Div  : exp_Mul_Div POR exp_Parentesis
                    | exp_Mul_Div DIVIDIDO exp_Parentesis
                    | exp_Mul_Div MODULO exp_Parentesis'''
    if t[2] == '*'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR)
    elif t[2] == '/': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)
    elif t[2] == '%': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MODULO)
    
def p_exp_Mul_Div2(t):
    '''exp_Mul_Div    : exp_Parentesis'''
    t[0]=t[1]

def p_exp_Parentesis1(t):
    '''exp_Parentesis   : PARIZQ op_Ternario PARDER'''
    t[0] = t[2]

def p_exp_Parentesis2(t):
    '''exp_Parentesis   : exp_Negativo'''
    t[0]=t[1]

def p_exp_Negativo1(t):
    '''exp_Negativo : MENOS valor'''
    t[0]= ExpresionNegativa(t[2])

def p_exp_Negativo2(t):
    '''exp_Negativo : valor'''
    t[0]= t[1]


def p_valorEntero(t):
    '''valor    : ENTERO'''
    t[0]=ExpresionEntero(t[1])

def p_valorCadena(t):
    '''valor    : CADENA'''
    t[0]=ExpresionDobleComilla(t[1])

def p_valorDecimal(t):
    '''valor    : DECIMAL'''
    t[0]=ExpresionDecimal(t[1])

def p_valorCaracter(t):
    '''valor    : CARACTER'''
    t[0]=ExpresionComillaSimple(t[1])

def p_valorBooleanToString(t):
    '''valor    : TRUE PUNTO ID PARIZQ PARDER
                | FALSE PUNTO ID PARIZQ PARDER'''
    if t[3]=="toString":
        t[0]=ExpresionDobleComilla("\"" + t[1] + "\"")


def p_valorBoolean(t):
    '''valor    : TRUE
                | FALSE'''
    t[0]=Expresion_True_False(t[1])

def p_valorNull(t):
    '''valor    : NULL'''
    t[0]=ExpresionNull()

def p_valorId(t):
    '''valor    : ID'''
    t[0]=ExpresionID(t[1])

def p_valorCallFuncion(t):
    '''valor    : callFuncion'''
    t[0]=t[1]
    
def p_valorArrayList(t):
    '''valor    : CORIZQ lista_Expresiones CORDER
                | CORIZQ CORDER'''
    if len(t) ==4:
        t[0] = ExpresionArray(t[2])
    elif len(t)==3:
        t[0] = ExpresionArray([])

def p_valorAccesoArray(t):
    '''valor    : ID CORIZQ op_Ternario CORDER''' 
    t[0] = Expresion_AccesoArray(t[1],t[3])

def p_valorAccesoMatriz(t):
    '''valor    : ID CORIZQ op_Ternario CORDER listaAccesos'''
    lista = []
    lista.append(t[3])
    lista.extend(t[5])
    t[0] = Expresion_AccesoMatriz(t[1],lista)
    

def p_valorCallArgumento_Funcion(t):
    '''valor    : argumento_Funcion'''
    t[0] = t[1]

def p_valorAccesoArgumento(t):
    '''valor    : accesoArgumento'''
    t[0] = t[1]

# def p_valorTypeOf(t):
#     '''valor    : TYPEOF op_Ternario'''
#     t[0] = funcionTypeOf(t[2])





def p_error(p):
    if p:
        listaErrores.append(error("Token inesperado "+ str(p.value),p.lineno,p.lexpos,'sintactico'))
        print(f"Error de sintaxis en línea {p.lineno}, columna {p.lexpos}: Token inesperado '{p.value}'")
    else:
        #listaErrores.append(error("Token inesperado "+ str(p.value),p.lineno,p.lexpos,'sintactico'))
        print("Error de sintaxis")

import ply.lex as Lex
import ply.yacc as yacc
lexer = Lex.lex()
parser = yacc.yacc()

def parse(input) :
    return parser.parse(input)

    

