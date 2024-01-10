import math
import random

class Erreur():
    def __init__(self, message) :
        print("Erreur log : " + message)
        self.message = message
    
    def __str__(self) -> str:
        return "ERR: " + self.message


class Intervalle_net_continu():
    def __init__(self, a1, a2):
        self.a1 = a1
        self.a2 = a2

    def __str__(self):
        return "[" + str(self.a1) + ", " + str(self.a2) + "]"

    def __add__(self, other):
        return Intervalle_net(self.a1 + other.a1, self.a2 + other.a2)

    def __neg__(self):
        return Intervalle_net(-self.a2, -self.a1)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return Intervalle_net(max([self.a1 * other.b1, self.a1 * other.b2, self.a2 * other.b1, self.a2 * other.b2]),
                              max([self.b1 * other.a1, self.b1 * other.a2, self.b2 * other.a1, self.b2 * other.a2]))

    def __pow__(self, value):
        if value != -1:
            return Erreur("Only -1 is supported")
        if self.a1 == 0 or self.a2 == 0:
            return Erreur("Only non-zero intervals are supported")
        if self.a1 <= 0 <= self.a2:
            return Erreur("Only  strictly positive or strictly négative intervals are supported by this operation.")
        return Intervalle_net(1 / self.a2, 1 / self.a1)

    def __div__(self, other):
        return self * (other ** -1)

    def union(self, other):
        if self.a2 < other.a1 or other.a2 < self.a1:
            return Erreur("The intervals must be joined")

        return Intervalle_net(min(self.a1, other.a1), max(self.a2, other.a2))

    def __str__(self) -> str:
        return "[" + str(self.a1) + ";" + str(self.a2) + "]"

class Intervalle_net():
    def __init__(self, *args): # Attention pas sur que ca marche le *args
        if len(args) % 2 != 0:
            #preturn Erreur("The number of arguments must be even")
            pass
        self.intervalles_continus = []
        for i in range(0, len(args), 2):
            if args[i] >= args[i + 1]:
                return Erreur("The arguments must be ordered")
            self.intervalles_continus.append(Intervalle_net_continu(args[i], args[i + 1]))

    def simplifier(self):
        """
        Untested, coded by codeium AI
        """
        for i in range(len(self.intervalles_continus)):
            for j in range(i + 1, len(self.intervalles_continus)):
                if self.intervalles_continus[i].a2 >= self.intervalles_continus[j].a1:
                    self.intervalles_continus[i] = self.intervalles_continus[i] + self.intervalles_continus[j]
                    del self.intervalles_continus[j]
                    break
    
    def __str__(self) -> str:
        return str(self.intervalles_continus)


class UnionIFT():
    def __init__(self, IFTS, Tco=max):
        self.IFTS = IFTS
        self.Tco = Tco
    def possibilite(self,other):
        if isinstance(other, UnionIFT):
            pos = 0
            for IFT1 in self.IFTS:
                pos = max(pos, IFT1.possibilite(other))
            return pos
        pos = 0
        for IFT in self.IFTS:
            pos = max(pos,IFT.possibilite(other))
        return pos

    def valeur(self, x):
        val = 0
        for ift in self.IFTS:
            val = self.Tco(ift.valeur(x), val)
        return val
class InterIFT():
    def __init__(self, IFTS, Tno=min):
        self.IFTS = IFTS
        self.Tno = Tno
    def valeur(self, x):
        val = 1
        for ift in self.IFTS:
            val = self.Tno(ift.valeur(x), val)
        return val

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    x1,y1 = p1
    x2, y2 = p2
    return A, B, -C, x1,y1,x2,y2



def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    x1, y1, x2, y2 = L1[3:]
    x3, y3, x4, y4 = L2[3:]
    xmin = max(min(x1,x2),min(x3,x4))
    xmax = min(max(x1,x2),max(x3,x4))
    if D != 0:
        x = Dx / D
        y = Dy / D
        if x < xmin or x > xmax:
            return None
        return x,y
    else:
        return None
class Trapeseflou():
    def __init__(self, a1, a2, a3, a4, h=1):
        if not (a1 <= a2 <= a3 <= a4):
            pass
            #return Erreur("mauvais ordre des args")
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.h = h
        self.lines = [line((self.a1,0), (self.a2, self.h)), line((self.a2, self.h), (self.a3, self.h)), line((self.a3, self.h),(self.a4, 0))]

    def possibilite(self, other):
        if isinstance(other, UnionIFT):
            return other.possibilite(self)
        intersections = []
        for l1 in self.lines:
            for l2 in other.lines:
                pt = intersection(l1, l2)
                if pt != None:
                    intersections.append(pt)
        if len(intersections) == 0:
            if (self.a1 >= other.a1 and self.a4 <= other.a4) or (other.a1 >= self.a1 and other.a4 <= self.a4):
                return min(self.h, other.h)
            return 0
        return max([pts[1] for pts in intersections])

    def __add__(self, other):
        if self.h > other.h:
            ift = self.troncature(other.h)
        else:
            ift = self
            other = other.troncature(self.h)
        return Trapeseflou(ift.a1 + other.a1, ift.a2 + other.a2, ift.a3 + other.a3, ift.a4 + other.a4, ift.h)

    def __mul__(self, other):
        if isinstance(other, Trapeseflou):  # si l'autre élément est lui même un IFT
            ift = other
            if self.h > ift.h:
                ift1 = self.troncature(ift.h)
            else:
                ift1 = self
                ift = ift.troncature(self.h)
            return Trapeseflou(ift1.a1 * ift.a1, ift1.a2 * ift.a2, ift1.a3 * ift.a3, ift1.a4 * ift.a4, ift1.h)
        else:  # si l'autre élément est un scalaire
            alpha = other
            if alpha > 0:
                a1 = alpha * self.a1
                a2 = alpha * self.a2
                a3 = alpha * self.a3
                a4 = alpha * self.a4
            else:
                a1 = alpha * self.a4
                a2 = alpha * self.a3
                a3 = alpha * self.a2
                a4 = alpha * self.a1
            return Trapeseflou(a1, a2, a3, a4, self.h)

    def __pow__(self, value):
        if value == -1:
            return Trapeseflou(1 / self.a4, 1 / self.a3, 1 / self.a2, 1 / self.a1, self.h)
        elif value == 1:
            return self
        else:
            return self * self ** (value - 1)


    def __truediv__(self, other):
        return self * (other ** -1)

    def __neg__(self):
        return Trapeseflou(-self.a4, -self.a3, -self.a2, -self.a1, self.h)

    def __sub__(self, other):
        return self + (-other)

    def troncature(self, h):
        """Fait une troncature de l'ITF en h"""
        if type(h) != float and type(h) != int:
            return Erreur(str(h) + " not int or float")
        if h > self.h:
            return Erreur(str(h) + "> h de l'intervalle")
        elif h == self.h:
            return self
        else:
            a2 = h * (self.a2 - self.a1) / self.h + self.a1
            a3 = - h * (self.a4 - self.a3) / self.h + self.a4
            return Trapeseflou(self.a1, a2, a3, self.a4, h)

    

    def valeur(self, x):
        if x == self.a2:  # x dans noyau
            return self.h
        if x <= self.a1:  # x pas dans le support
            return 0
        if x > self.a1 and x <= self.a2:
            return self.h * ((x - self.a1) / (self.a2 - self.a1))
        if x > self.a2 and x <= self.a3:  # x dans le noyau
            return self.h

        if x > self.a3 and x <= self.a4:
            return self.h * ((self.a4 - x) / (self.a4 - self.a3))
        if x > self.a4:  # x pas dans support
            return 0

    def alpha_coupe(self, alpha):
        # renvoie l'alpha coupe
        if alpha > 0 and alpha <= self.h:  # l'alpha coupe n'est pas l'intervalle vide
            A1 = ((self.a2 - self.a1) * (alpha / self.h) + self.a1)
            A2 = (-(self.a4 - self.a3) * (alpha / self.h) + self.a4)
            return Intervalle_net_continu(A1, A2)
        else:
            return None  # rien dans l'alpha coupe

    def __str__(self) -> str:
        
        if self.a2 == self.a3:
            return "NFT[" + str(self.a1) + " " + str(self.a2) + " " + str(self.a3) +" " + "h=" + str(self.h) + "]"  
        

        return  "IFT[" + str(self.a1) + " " + str(self.a2) + " " + str(self.a3) + " " + str(self.a4)+ " h="+ str(self.h)+"]"




    


def convert_to_float(nombre):
    """
    conertit un nb en float, sans erreurs
    """
    print(nombre)
    if "," in nombre or "." in nombre:
        chaine = nombre.replace(",", ".")
        try :  
            result = float(chaine) 
        except : 
            return Erreur(str(nombre) + " not float")
        return float(chaine)
    try : 
        result = int(nombre)
    except :
        return Erreur(str(nombre) + " not float")

    return result

def parseIFT(chaine):
    """
    crée un IFT à partir d'une chaine str
    """
    arg = [convert_to_float(i) for i in chaine.split(" ") if len(i) > 0 ]
    if any(type(i) == Erreur for i in arg):
        return arg.index(key=lambda x: type(x) == Erreur)
    

    if len(arg) == 2:
        if arg[1] <= arg[0] : 
            return Erreur("Bornes mal ordonnées")
        return Intervalle_net_continu(arg[0], arg[1])
    if len(arg) == 3:
        if not (arg[0] <= arg[1] <= arg[2]):
            return Erreur("Bornes mal ordonnées")
        return Trapeseflou(arg[0], arg[1], arg[1], arg[2])
    if len(arg) == 4: # IFT ou NFT ? 
        if 0 < arg[3] < 1:
            if not (arg[0] <= arg[1] <= arg[2]):
                return Erreur("Bornes mal ordonnées")
            return Trapeseflou(arg[0], arg[1], arg[1], arg[2], h=arg[3])
        else:
            if not (arg[0] <= arg[1] <= arg[2] <= arg[3]):
                return Erreur("Bornes mal ordonnées")
            return Trapeseflou(arg[0], arg[1], arg[2], arg[3])
    if len(arg) == 5:
        if not (arg[0] < arg[1] < arg[2] < arg[3]):
            return Erreur("Bornes mal ordonnées")
        return Trapeseflou(arg[0], arg[1], arg[2], arg[3],h = arg[4])
    return Erreur("Pas le bon nombre de paramètres")









## FONCTIONS OPERATIONS DE BASE ##
## PERMETTENT DE CATCH LES ERREURS ##
## ET DE LES RENVOYER A TRAVERS LE CALCUL ##
def mul(a,b) : 
    if type(a) == Erreur :
        return a
    elif type(b) == Erreur :
        return b
    return a.__mul__(b)

def add(a,b) : 
    if type(a) == Erreur :
        return a
    elif type(b) == Erreur :
        return b
    return a+b

def sub(a,b) : 
    if type(a) == Erreur :
        return a
    elif type(b) == Erreur :
        return b
    return a.__sub__(b)

def div(a,b) :
    if type(a) == Erreur :
        return a
    elif type(b) == Erreur :
        return b
    return a.__truediv__(b)

def tronc(a,b) :
    if type(a) == Erreur :
        return a
    elif type(b) == Erreur :
        return b
    return a.troncature(b)


def isnumeric(chaine):
    try : 
        float(chaine)
        return True
    except : 
        return False

