from tipos import TIPOS_P


class display(): #VALOR - NODO
    
    def __init__(self, Lsalida="",Lcontinue="",RA=0,func="",tipo=TIPOS_P.VOID):
        self.Lsalida = Lsalida
        self.Lcontinue = Lcontinue
        self.RA = RA
        self.func= func
        self.tipo=tipo