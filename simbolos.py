

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

    def __init__(self, simbolos = {}, salida='',ambito='global'):
        self.simbolos = simbolos
        self.salida = salida
        self.listaErrores =[]
        self.ambito= ambito

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

        

    def limpiar(self):
        #self.salida=""
        self.listaErrores.clear()
        self.simbolos.clear()
        self.ambito='global'
