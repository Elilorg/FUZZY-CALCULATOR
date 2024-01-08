import math
import random

class Erreur():
    def __init__(self, message) :
        print("Erreur log : " + message)
        self.message = message
    
    def __str__(self) -> str:
        return "ERREUR : " + self.message


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
    def __init__(self, *args):
        if len(args % 2 != 0):
            return Erreur("The number of arguments must be even")

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
    

class Trapèseflou():
    def __init__(self, a1, a2, a3, a4, h=1):
        if not (a1 <= a2 <= a3 <= a4):
            return Erreur("mauvais ordre des args")
        if h <= 0:
            return Erreur("Hauteur négative")
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.h = h

    def __add__(self, other):
        if self.h > other.h:
            ift = self.troncature(other.h)
        else:
            ift = self
            other = other.troncature(self.h)
        return Trapèseflou(ift.a1 + other.a1, ift.a2 + other.a2, ift.a3 + other.a3, ift.a4 + other.a4, ift.h)

    def __mul__(self, other):
        if isinstance(other, Trapèseflou):  # si l'autre élément est lui même un IFT
            ift = other
            if self.h > ift.h:
                ift1 = self.troncature(ift.h)
            else:
                ift1 = self
                ift = ift.troncature(self.h)
            return Trapèseflou(ift1.a1 * ift.a1, ift1.a2 * ift.a2, ift1.a3 * ift.a3, ift1.a4 * ift.a4, ift1.h)
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
            return Trapèseflou(a1, a2, a3, a4, self.h)

    def __pow__(self, value):
        if value == -1:
            return Trapèseflou(1 / self.a4, 1 / self.a3, 1 / self.a2, 1 / self.a1, self.h)
        elif value == 1:
            return self
        else:
            return self * self ** (value - 1)


    def __truediv__(self, other):
        return self * (other ** -1)

    def __neg__(self):
        return Trapèseflou(-self.a4, -self.a3, -self.a2, -self.a1, self.h)

    def __sub__(self, other):
        return self + (-other)

    def troncature(self, h):
        """Fait une troncature de l'ITF en h"""
        if type(h) != float and type(h) != int:
            return Erreur(str(h) + " not int or float")
        if h > self.h:
            return Erreur("H est au dessus de la hauteur de l'intervalle")
        elif h == self.h:
            return self
        else:
            a2 = h * (self.a2 - self.a1) / self.h + self.a1
            a3 = - h * (self.a4 - self.a3) / self.h + self.a4
            return Trapèseflou(self.a1, a2, a3, self.a4, h)

    def __str__(self) -> str:
        return f"({self.a1}, {self.a2}, {self.a3}, {self.a4}, {self.h})"

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
        return "IFT[" + str(self.a1) + " " + str(self.a2) + " " + str(self.a3) + " " + str(self.a4)+ " "+ str(self.h)+"]"



class NFT(Trapèseflou) : 
    def __init__(self, a1, a2, a3, h=1):
        super().__init__(a1, a2, a2, a3, h)
    
    def __str__(self) : 
        return "NFT[" + str(self.a1) + " "+ str(self.a2) + " " + "str(self.a4)"+ "]"
    


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
        return Intervalle_net_continu(arg[0], arg[1])
    if len(arg) == 3:
        return Trapèseflou(arg[0], arg[1], arg[1], arg[2])
    if len(arg) == 4: # IFT ou NFT ? 
        if 0<arg[3] and arg[3]<1:
            return Trapèseflou(arg[0], arg[1], arg[1], arg[2], h=arg[3])
        else:
            return Trapèseflou(arg[0], arg[1], arg[2], arg[3])
    if len(arg) == 5:
        return Trapèseflou(arg[0], arg[1], arg[2], arg[3],h = arg[4])
    return Erreur("Pas le bon nombre de paramètres")

def get_value(chaine):
    """
    si la chaine est un nb, on le converti en trapèse flou mais net ducoup. 
    Sinon aller chercher avec l'id
    Ca ca va dans l'interface de la calculatrice
    """
    check_num = chaine.replace(",", "").replace(".", "")
    if check_num.isnumeric():
        nb = convert_to_float(chaine)
        if type(nb) == Erreur : return nb
        return Trapèseflou(nb,nb,nb,nb,1)

    """
    Remplacer par la value dans le grid
    """
    dico = {"a1" : result_chaine("1 7 8 11 0,2"), "a2": result_chaine("2 4 8 10 0,3")}
    result = dico.get(chaine)
    if result is None:
        return Erreur(chaine + " ID invalide")
    return result
    #return Erreur(chaine + " n'est pas un nb valide")


def calcul(chaine): # Donc ca aussi ca va dans l'interface 
    if "+" in chaine:
        a, b = split_chaine(chaine, "+")
        return add(a,b)
    if "-" in chaine:
        a, b = split_chaine(chaine, "-")
        return sub(a,b)
    if "*" in chaine:
        a, b = split_chaine(chaine, "*")
        return mul(a,b)
    if "/" in chaine:
        a, b = split_chaine(chaine, "/")
        return div(a,b)
    if "#" in chaine:
        return tronc(calcul(chaine.split("#")[0]), convert_to_float(chaine.split("#")[1]))
    return get_value(chaine)

def split_chaine(chaine, symbole):
    """ 
    cette focntion fait partie de la recurtion de calcul. 
    elle permet de diviser une chaine en deux parties
    et de lancer le calcul sur chacune d'elles
    """
    splited = chaine.split(symbole)
    return calcul(splited[0]), calcul("".join(splited[1:]))

def result_chaine(chaine):
    """
    Le parseur
    """
    chaine_check = chaine.replace(" ", "").replace(",", "").replace("." , "")
    if chaine_check.isnumeric(): # Que des nombres
        return parseIFT(chaine)
    else:
        try : 
            return calcul(chaine.replace(" ", "")) # Pas d'espace (utile) dans les calculs
        except Exception as e:
            raise e
            return Erreur("Le calcul a échoué")



## FONCTIONS OPERATIONS DE BASE ##
## PERMETTENT DE CATCH LES ERREURS ##
## ET DE LES RENVOYER A TRAVERS LE CALCUL ##
def mul(a,b) : 
    if type(a) == Erreur :
        return a
    elif type(b) == Erreur :
        return b
    return a*b

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
    return a-b

def div(a,b) :
    if type(a) == Erreur :
        return a
    elif type(b) == Erreur :
        return b
    return a/b

def tronc(a,b) :
    if type(a) == Erreur :
        return a
    elif type(b) == Erreur :
        return b
    return a.troncature(b)

if __name__ == "__main__":
    print(result_chaine("a1"))
    print(result_chaine("a1-a2+3"))




