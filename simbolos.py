

class Simbolos(): #VALOR - NODO
    
    def __init__(self, id, tipo_simbolo,tipo, valor,ambito, instrucciones = [], parametros = [], props = {},linea=0,columna=0):
        self.id = id
        self.tipo = tipo
        self.tipo_simbolo =tipo_simbolo
        self.valor = valor
        self.ambito = ambito
       
        self.instrucciones = instrucciones
        self.parametros = parametros
        self.props = props
        self.linea = linea
        self.columna = columna


class TablaSimbolos():

    def __init__(self, simbolos = {},ambito='global'):
        self.simbolos = simbolos
        
        self.listaErrores =[]
        self.ambito= ambito
        self.temp=-1
        self.label=-1
        self.msg=-1
        self.inst=""
        self.Datos ="msgSalto: .byte 10 \n"

    def agregar(self, simbolo):
        self.simbolos[simbolo.id] = simbolo

    def obtener(self, id):
        if not id in self.simbolos:
            return None
        else:
            return self.simbolos[id]
    
    def actualizar(self, id, valor):
        if not id in self.simbolos:
            return None
        else:
            self.simbolos[id].valor = valor

    def getNextMsg(self):
        self.msg+=1
        return self.msg
    
    def getLastMsg(self):
        return self.msg
    
    def getNextLabel(self):
        self.label+=1
        return self.label

    def getLastLabel(self):
        return self.label
    
    def getNextTemp(self,offset):
        self.temp+=1
        self.temp-=offset
        if self.temp==17:
            self.temp=0

        if self.temp>6:
            return f's{self.temp-6}'
        else:
            return f't{self.temp}'
    
    
    
    def getLastTemp(self):
        return self.temp
    
    def restoreTemp(self,num):
        self.temp -=num


        

    def limpiar(self):
        #self.salida=""
        self.listaErrores.clear()
        self.simbolos.clear()
        self.ambito='global'
        self.inst=""
        self.Datos="msgSalto: .byte 10 \n"

    def getSalida(self):
        return f'''
    .data
          
    {self.Datos}

    .text
    .globl main
    main:

    {self.inst}

    li a7, 10    
    ecall

    '''
