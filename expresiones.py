from enum import Enum
from tipos import TIPOS_P

class OPERACION_ARITMETICA(Enum):
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDIDO = 4
    MODULO = 5

class OPERACION_REL(Enum):
    MAYOR_QUE = 1
    MENOR_QUE = 2
    IGUAL = 3
    NO_IGUAL = 4
    MAYORIGUAL =5
    MENORIGUAL=6

class OPERACION_LOGICA(Enum):
    AND=1
    OR=2
    




class ExpresionAritmetica:
    '''Clase Abstracta'''

class ExpresionBinaria(ExpresionAritmetica):
    def __init__(self,exp1,exp2,operador,tipo=TIPOS_P.ENTERO):
        self.exp1= exp1
        self.exp2 = exp2
        self.operador = operador
        self.tipo = tipo



class ExpresionNegativa(ExpresionAritmetica):
    def __init__(self,exp1,tipo=TIPOS_P.ENTERO):
        self.exp1= exp1
        self.tipo = tipo
        
class ExpresionEntero(ExpresionAritmetica):
    def __init__(self,exp1):
        self.exp1= exp1
        self.tipo = TIPOS_P.ENTERO
    
class ExpresionDecimal(ExpresionAritmetica):
    def __init__(self,exp1):
        self.exp1= exp1
        self.tipo = TIPOS_P.FLOAT

class ExpresionID():
    def __init__(self,id):
        self.id= id

class ExpresionNull():
    def __init__(self):
        self.tipo= None


class ExpresionRelacional():
    def __init__(self,exp1,exp2,operador):
        self.exp1= exp1
        self.exp2 = exp2
        self.operador = operador
        self.tipo = TIPOS_P.BOOLEAN

class ExpresionBoleana:
    '''Clase Abstracta'''



class ExpresionLogica(ExpresionBoleana):
    def __init__(self,exp1,exp2,operador):
        self.exp1= exp1
        self.exp2 = exp2
        self.operador = operador
        self.tipo = TIPOS_P.BOOLEAN  

class ExpresionNot(ExpresionBoleana):
    def __init__(self,exp1):
        self.exp1= exp1
        self.tipo = TIPOS_P.BOOLEAN

class Expresion_True_False(ExpresionBoleana):
    def __init__(self,exp1):
        self.exp1= exp1
        self.tipo = TIPOS_P.BOOLEAN
    
class ExpresionCadena:
    '''Clase Abstracta'''

class ExpresionDobleComilla(ExpresionCadena):
    def __init__(self, cad) :
        self.cad = cad
        self.tipo = TIPOS_P.CADENA

class ExpresionComillaSimple(ExpresionCadena):
    def __init__(self, cad) :
        self.cad =cad
        self.tipo = TIPOS_P.CHAR

class ExpresionTernaria():
    def __init__(self,exp1,exp2,exp3):
        self.exp1=exp1
        self.exp2=exp2
        self.exp3=exp3
        
class ExpresionArray():
    def __init__(self,valores):
        self.valores=valores

class Expresion_AccesoArray():
    def __init__(self,id,indice):
        self.id = id
        self.indice = indice

class Expresion_AccesoMatriz():
    def __init__(self,id,listaIndices):
        self.id = id
        self.listaIndices = listaIndices

        
        
    

