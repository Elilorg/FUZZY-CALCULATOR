from  ion import *
from kandinsky import *
import time
from fuzzy_logic import *
# Set the screen size
width_constant = 320
height_constant = 240
            
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
g = green


KEY_TO_CHAR = {
            KEY_ONE : "1",
            KEY_TWO : "2",
            KEY_THREE : "3",
            KEY_FOUR : "4",
            KEY_FIVE : "5",
            KEY_SIX : "6",
            KEY_SEVEN : "7",
            KEY_EIGHT : "8",
            KEY_NINE : "9",
            KEY_ZERO : "0",
            KEY_ANS : " ",
            KEY_DOT : ".",
            KEY_SHIFT : " ",
            KEY_PLUS : "+",
            KEY_MINUS : "-",
            KEY_MULTIPLICATION : "*",
            KEY_DIVISION : "/",
            KEY_SQRT : "#",
            KEY_COSINE : "^_v"
        }
### BOUTONS

class class_bouton : 
    """
   
    """
    def __init__(self, text, color, x:list[int], y : list[int], focused = False, action = None) :
        """
        les x sont les colonnes ou le bouton s'étend dans la grid
        les y sont les lignes ou le bouton s'étend dans la grid
        x et y doivent etre des listes

        """
        self.text = text

        self.color = color
        self.focused_color = (color[0]+40, color[1]+40, color[2]+40)

        self.focused = focused
        if action is not None : 
            self.action = action


        self.x = x
        self.y = y
        
        # SONT SET PAR LA GRID QUAND ILS Y SONT AJOUTES
        self.height = None
        self.width = None
        self.coordinates = None  #   (self.x[0] * grid.cell_w, self.y[0] * grid.cell_h)


        self.grid_coordinates = [self.x[0], self.y[0]]
        self.grid = None
    

    def draw(self, color = None) :

        self.updater_coordonnees()
            #raise ValueError(f"height, width, cordinates not set, button {self.text} at {self.grid_coordinates} must not be in grid yet")
        if color is not  None :
            color_used = color
        elif self.focused  :
            color_used = self.focused_color
        else :
            color_used = self.color
        left_top = (self.coordinates[0], self.coordinates[1]) 
        fill_rect(left_top[0], left_top[1], self.width, self.height, color_used)
        draw_string(self.text, left_top[0], left_top[1], (0, 0, 0))
    
    def updater_coordonnees(self) :
        self.grid.updater_coordonees(self)
    
    def focus(self) :
        self.focused = True
        self.draw()
    
    def unfocus(self) : 
        self.focused = False
        self.draw()
    
    def __str__(self) -> str:
        return self.text + " " + str(self.grid_coordinates)

    def changer_coordonnees(self, x = 0, y = 0) :
        self.grid_coordinates[0] += x
        self.grid_coordinates[1] += y
        
        self.x = list(map(lambda x_orginal : x_orginal + x, self.x))
        self.y = list(map(lambda y_orginal : y_orginal + y, self.y))

        self.coordinates = None # Cela permettra de lancer une erreur si les coordinates ne sont pas réevaluées par la grille après un déplacement. 


class classtextinput(class_bouton) :
    """ 
    Une extention de la classe bouton. Elle a quelques particularitée en plus. 
    - Sa touche "action" permet de faire entrer l'interface en mode texte et donc de changer le texte
    - En mode texte, l'interface utilise ces fonctions : 
        - del_char permet de supprimer le dernier caractère 
        - add_char permet d'ajouter un caractère
        - enter_text_mode est appellé quand l'interface entre en text-mode, et permet d'effacer le texte par défaut
        - exit text_mode est appellé quand l'interface quitte le mode texte et permet de remettre le texte par défaut si on a rien écrit
    """
    def __init__(self, text, color, x:list[int], y : list[int], focused = False, action =  None) :
        action =self.toggle_text_mode
        super().__init__(text, color, x, y, focused, action)
        
        self.text_mode = False
        self.text_mode_color = (230, 230, 230) 
    
    def draw(self):
        if self.text_mode : 
            super().draw(self.text_mode_color)
        else : 
            super().draw()
        
    def add_char(self, char) :
        self.text += char
        draw_string(self.text, self.coordinates[0], self.coordinates[1], (0, 0, 0))

    def add_char_with_action(self, key_number) :
        self.add_char(KEY_TO_CHAR[key_number])
    
    def del_char(self) :
        if len(self.text) == 0 : 
            return 
        self.text = self.text[:-1]
        self.draw()
    
    def enter_text_mode(self) : 
        self.text_mode = True
        if self.text == None : 
            self.text = ""
            
        self.draw()
    
    def exit_text_mode(self) :
        self.text_mode = False
        if self.text == "" : 
            self.text = None
        self.draw()
    
    def toggle_text_mode(self) :  
        """
        Ce fonctionnement est basé sur l'idée que c'est bien ce bouton qui est le text_focused_button quand toggle_text_mode est appelé
        Et donc que c'est bien ce bouton qui va entrer ou sortir du mode texte, sinon on pourrais avoir plusieurs boutons en mode texte.
        """
        if self.text_mode : 
            deactivate_text_mode()
        else : 
            activate_text_mode()
          ## AJOUTER UN COURSEUR ET DES M2THODE POUR TRAVAILLER AVEC DU TEXTE


class boutonvaleur(class_bouton) :
    def __init__(self, text, color, x:list[int], y : list[int], focused = False, action = None) :
        self.char = text[0]
        
        super().__init__(text, color, x, y, focused, action)

    def action(self) :
        ajouter_lettre(self.char)
    


class class_bouton_calcul(classtextinput) :
    def __init__(self, text, color, x:list[int], y : list[int], focused = False, action = None) :
        super().__init__(text, color, x, y, focused, action)
        self.resultat = None
        self.type_resultat = "%"  # Ca pourrait etre : "IFT[%]" ou "NFT[%]"
        
    def draw(self) :
        text = self.text
        if text is None : text = "CALC"
        self.text = text
        super().draw()
        result_affiche = str(self.resultat) if self.resultat != None else ""
        if text == "CALC" : self.text = None
        draw_string(result_affiche, self.coordinates[0], self.coordinates[1] + int(self.height/2), (0, 0, 0))
    
    def exit_text_mode(self):
        self.resultat = self.evaluate(self.text)
        super().exit_text_mode()
        self.draw()  # Oui, risque de redraw alors qu'on a déja draw parce que texte vide. A voir comment ca se fix

    def del_char(self):
        if len(self.text) == 0 and self.type_resultat != "%" : 
            self.type_resultat = "%" # Quand on supprime alors que le texte est vide ca supprime le type de résultat qu'on cherche
            self.draw()
        return super().del_char()
    
    def add_char(self, char):
        self.text += char
        self.draw()

    def ajouter_resultat(self, type_resultat) :
        self.type_resultat = type_resultat
        self.draw()

    def get_value(self, chaine):
        """
        si la chaine est un nb, on le converti en trapèse flou mais net ducoup. 
        Sinon aller chercher avec l'id
        Ca ca va dans l'interface de la calculatrice
        """
        check_num = chaine.replace(",", "").replace(".", "")
        if isnumeric(check_num):
            nb = convert_to_float(chaine)
            if type(nb) == Erreur : 
                return nb
            
            return Scalaire(nb,1)

        else :
            return self.grid.get_result_by_id(chaine)
        #return Erreur(chaine + " n'est pas un nb valide")

    def valeur(self, ifts, alpha):
        dico = {}
        alpha = convert_to_float(alpha)
        for ift in [ift for ift in ifts.split(" ") if ift != None]:
            dico[ift] = self.grid.get_result_by_id(ift).valeur(alpha)
        return dico
    def Tnorme(self, a,b, tno):
        if isinstance(a, Erreur):
            return a
        if isinstance(b, Erreur):
            return b
        if isinstance(a, Scalaire) and isinstance(b, Scalaire):
            return Tnormes[tno](a.a1,b.a1)
        return InterIFT([a,b], Tnormes[tno])


    def Tconorme(self, a,b, tco):
        if isinstance(a, Erreur):
            return a
        if isinstance(b, Erreur):
            return b
        if isinstance(a, Scalaire) and isinstance(b, Scalaire):
            return Tconormes[tco](a.a1,b.a1)
        return UnionIFT([a,b], Tconormes[tco])

    def calcul(self, chaine): # Donc ca aussi ca va dans l'interface 
        if "+" in chaine:
            a, b = self.split_chaine(chaine, "+")
            return add(a,b)
        if "-" in chaine:
            a, b = self.split_chaine(chaine, "-")
            return sub(a,b)
        if "*" in chaine:
            a, b = self.split_chaine(chaine, "*")
            return mul(a,b)
        if "/" in chaine:
            a, b = self.split_chaine(chaine, "/")
            return div(a,b)
        if "#" in chaine:
            a, b = self.split_chaine(chaine, "#")
            return tronc(self.calcul(chaine.split("#")[0]), convert_to_float(chaine.split("#")[1]))
        if "^_v" in chaine:
            return pos(self.calcul(chaine.split("^_v")[0]), self.calcul(chaine.split("^_v")[1]))
        if "=" in chaine:
            return self.valeur(chaine.split("=")[0], convert_to_float(chaine.split("=")[1]))
        for tno in Tnormes.keys():
            if tno in chaine:
                a, b = self.split_chaine(chaine, tno)
                return self.Tnorme(a,b, tno)
        for tco in Tconormes.keys():
            if tco in chaine:
                a, b = self.split_chaine(chaine, tco)
                return self.Tnorme(a, b, tco)


        return self.get_value(chaine)


    def split_chaine(self, chaine, symbole):
        """ 
        cette focntion fait partie de la recurtion de calcul. 
        elle permet de diviser une chaine en deux parties
        et de lancer le calcul sur chacune d'elles
        """
        splited = chaine.split(symbole)
        return self.calcul(splited[0]), self.calcul(symbole.join(splited[1:]))

    def evaluate(self, chaine):
        """
        Le parseur
        """
        if chaine == "" :
            return None
        chaine_check = chaine.replace(" ", "").replace(",", "").replace("." , "")
        if isnumeric(chaine_check): # Que des nombres
            return parseIFT(chaine)
        else:
            try : 
                return self.calcul(chaine.replace(" ", "")) # Pas d'espace (utile) dans les calculs
            except Exception as e:
                raise e
                return Erreur("Le calcul a échoué")

### INTERFACES ###
class class_grid:
    """
    La grille contient l'ensemble des boutons. Ici, chaque élément est appellé une "cell".
    On accède au contenu de la grille avec la methode get_cell(x, y)
    ATTENTION : pour accéder au contenu des cell avec la propriété __grid, il faudra utiliser :  self.__grid[y][x]
    Les méthode suivantes sont aussi disponibles : 
    - get_focused_cell() : renvoie le contenu de la cellule en cours de selection
    - focus_cell(button : Bouton) : déselectionne la cellule en cours de selection, puis selectionne le bouton qu'on vien de lui passer.
    - __getitem__ permet de récupérer les contenus des cellules avec grid[y][x] ou grid est l'objet grid et non la propriété __grid. Cela permet une interface plus simple
    - __setitem__ permet de modifier les contenus des cellules avec grid[y][x] 
    - travel_x() permet de focus la cellule directement a droite ou a gauche de la cellule en cours de selection
    - travel_y() permet de focus la cellule directement en haut ou en bas de la cellule en cours de selection

    Les paramètre suivants sont disponibles lors de la création de la grille 
    - offset_x : position de la grille sur l'axe x (coin supérieur gauche)
    - offset_y : position de la grille sur l'axe y (coin supérieur gauche)
    - width : largeur de la grille
    - height : hauteur de la grille
    - x_div : nb de divisions sur l'axe x
    - y_div : nb de divisions sur l'axe y

    Les valeurs par défaut sont celles de la grille principale

    """
    def __init__(self, offset_x = 0, offset_y = 0, width = width_constant, height = height_constant, x_div = 4, y_div = 5) :   
        """
        On initialise la grille avec sa hauteur et sa largeur
        """
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.x_div = x_div # division on x
        self.y_div = y_div # division on y

        self.width = self.x_div
        self.height = self.y_div

        self.cell_w = width//self.x_div
        self.cell_h = height//self.y_div
        self.focused = [0, 0]

        # Contient tout les boutons.
        self.__grid = [[None for j in range(self.width)] for i in range(self.height)]
    
    def get_cell(self, x, y) : 
        """
        retourne la cellule
        """
        if x < 0 or x > self.width - 1 :
            pass 
            #raise ValueError("x not inside Grid")
        if y < 0 or y > self.height -1 :
            pass 
            #raise ValueError("y not inside Grid")
        return self.__grid[y][x]

    def updater_coordonees(self, cell : class_bouton) :
        """
        donne au bouton ces veritables coordonées pour qu'il puisse se dessiner au bon endroit sur l'écran
        """
        #x, y = cell.grid_coordinates
        cell.coordinates = (cell.x[0] * self.cell_w + self.offset_x, cell.y[0] * self.cell_h + self.offset_y)
        cell.height = self.cell_h * len(cell.y)
        cell.width = self.cell_w * len(cell.x)


    def get_focused_cell(self) :
        """
        retourne la cellule focused. Celle ci ne devrait pas etre nulle. 
        """
        cell_content = self.__grid[self.focused[1]][self.focused[0]]
        if cell_content is None : 
            return None
        return cell_content
    
    def focus_cell(self, cell : class_bouton) :
        if cell is None :
            pass 
            #raise Exception(f"Can't focus an empty cell at {cell}")
        
        button_to_unfocus = self.get_cell(self.focused[0],self.focused[1])
        
        button_to_unfocus.unfocus()
        cell.focus()
        self.focused = [cell.grid_coordinates[0], cell.grid_coordinates[1]]
    
    def __getitem__(self, index) : 
            return self.__grid[index]
        
        
    def __setitem__(self,  index, value) :
        self.__grid[index] = value
    
    def travel_x(self, i) :
        """
        n'admet que 1 et -1
        """
        x, y = self.focused
    
        if i == 1  :  # GO RIGHT
            for cell in self.__grid[y][x+1:] : 
                if cell is not None :
                    self.focus_cell(cell)
                    return
        elif i == -1 : # Go LEFT
            for cell in self.__grid[y][:x][::-1]: # On part notre cell et on va vers la gauche et focus le premier bouton. 
                if cell is not None : 
                    self.focus_cell(cell)
                    return
            return

    def travel_y(self, i) : 
        """
        On parcour les lignes pour trouver la ligne au dessus ou au dessou qui renvoie
        n'admet que 1 et -1 
        """
        x, y = self.focused
        if i == 1  :  # GO DOWN
            for list in self.__grid[y+1:] : 
                if list[x] is not None :
                    self.focus_cell(list[x])
                    return
            return
        if i == -1 : # Go UP
            for list in self.__grid[:y][::-1] : # On part notre cell et on va vers le haut et focus le premier bouton. 
                if list[x] is not None : 
                    self.focus_cell(list[x])
                    return
            return
        
    def add_button(self, button : class_bouton) :
        x, y = button.grid_coordinates
    
        if self.affichable(button) :
            self.__grid[button.grid_coordinates[1]][button.grid_coordinates[0]] = button
            # Efface tout ce qu'il y avais a l'endroit ou est le nouveau bouton
            for i in button.x :
                for j in button.y :
                    if i == button.grid_coordinates[0] and j == button.grid_coordinates[1] :
                        continue
                    self.__grid[j][i] = None 

        button.grid = self
        
    def draw(self) : 
        for row in self.__grid : 
            for cell in row : 
                if cell is not None and self.affichable(cell) : 
                    cell.draw()

    def __str__(self) : 
        st = ""
        for y in range(self.y_div) : 
            for x in range(self.x_div) : 
                
                st += str(type(self.get_cell(x, y)))
                st += " "
            st += "\n"
        return st

    def affichable(self, cell) :
        if cell.grid_coordinates[0] < 0 or cell.grid_coordinates[0] > self.x_div - 1 : 
            return False
        if cell.grid_coordinates[1] < 0 or cell.grid_coordinates[1] > self.y_div - 1 : 
            return False
        return True


class class_liste_principale(class_grid) :

    def __init__(self) : 
        self.rows : list[tuple(class_bouton, class_bouton_calcul)]= []
        ids : list[str] = []
        for j in range(10):
            ids += [i + str(j) if j != 0 else i for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        self.ids = ids
        self.remaining_ids = ids.copy()        

        super().__init__(x_div=6, y_div=5)
        for i in range(self.y_div) :
            self.append_list()
        # Ajouter les rows

    def move_up(self, cell : class_bouton) : 
        """
        bouge un bouton de 1 vers le haut
        ATTENTION : elle écrase la cellule vers laquelle le bouton est déplacé
        """
        x, y = cell.grid_coordinates
        if self.affichable(cell) :
            self[y][x] = None
        cell.changer_coordonnees(y=-1)
        if self.affichable(cell) :
            self[y-1][x] = cell
            cell.draw()
    
    def move_down(self, cell : class_bouton) :
        """
        bouge un bouton de 1 vers le bas. 
        ATTENTION : elle écrase la cellule vers la quelle le bouton est déplacé
        """
        x, y = cell.grid_coordinates
        if self.affichable(cell) :
            self[y][x] = None
        cell.changer_coordonnees(y=1)
        if self.affichable(cell) :
            self[y+1][x] = cell 
            cell.draw()
        
    def go_down(self) : 
        """
        fait descendre tout les boutons
        """
        self.get_focused_cell().unfocus()
        for i in self.rows[::-1] : # du BAS VERS LE HAUT pour qu'aucun bouton ne soit écrasé
            self.move_down(i[0])
            self.move_down(i[1])
        x, y = self.focused
        self.focus_cell(self[y][x])

    def go_up(self) : 
        """
        fait monter tout les boutons
        """
        self.get_focused_cell().unfocus()
        for i in self.rows : 
            self.move_up(i[0])
            self.move_up(i[1])
        x, y = self.focused
        self.focus_cell(self[y][x])
        
        
    def append_list(self) : 
        if len(self.rows) == 0 :
            y_pos = 0
        else : 
            y_pos = self.rows[-1][0].grid_coordinates[1] + 1 # A la hauteur 1 en dessous du dernier bouton
        if len(self.ids) == 0 :
            return
        bouton_calcul = class_bouton_calcul(None, black, [1, 2, 3, 4, 5], [y_pos])
        bouton_valeur = boutonvaleur(self.remaining_ids.pop(0) + " = ", white,[0], [y_pos])
        self.add_button(bouton_calcul)
        self.add_button(bouton_valeur)
        self.rows.append((bouton_valeur, bouton_calcul))

    def travel_y(self, i): # OVERWRITE LA FONCTION ORIGINALE
        y = self.focused[1]
        if y == 0 and i == -1 and self.rows[0][0].grid_coordinates[1] != 0:  # On est en haut et on veut monter et il y a des boutons au dessus
            self.go_down()
        elif y == self.y_div -1  and i == 1 : # On est en bas et on veut aller vers le bas :
            if self.rows[-1][0].grid_coordinates[1] == self.y_div - 1: # On a plus de rows apres ca 
                self.append_list()
            self.go_up()
        else : 
            super().travel_y(i)


    def get_result_by_id(self, id) :
        """
        Cette fonction fait la supposition que la liste est composée des id suivantes : 
        A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
        A1, A2, A3, A4 , etc...
        """
        if type(id) != str or len(id) == 0 or len(id) > 2:
            return Erreur(str(id) + " invalide id")

        index = self.ids.index(id[0]) 
        if len(id) > 1 :
            try : 
                index += 26 * int(id[1]) - 1
            except :
                return Erreur("id invalide") 
            index += 26 * int(id[1])
        bouton = self.rows[index][1]

        if type(bouton.resultat) == Erreur  : 
            return Erreur("id" + " à renvoyé ERR")
        elif bouton.resultat is None : 
            return Erreur("bouton vide")
        return bouton.resultat
    




class class_interface() : 
    def __init__(self, grid : class_liste_principale) : 
        self.main_grid = grid
        self.text_mode = False
        self.text_focused_button = None
        self.grid_focused = self.main_grid
        self.focused_button : classtextinput = self.grid_focused.get_focused_cell()

        self.actions = {   # Actions de navigation
            KEY_UP : lambda :  self.grid_focused.travel_y(-1), # touche echap
            KEY_DOWN : lambda : self.grid_focused.travel_y(1), # touche 1
            KEY_LEFT : lambda : self.grid_focused.travel_x(-1),
            KEY_RIGHT :lambda : self.grid_focused.travel_x(1), # touche 2
            KEY_EXE : lambda : self.grid_focused.get_focused_cell().action() # touche . sur le clavier
            # On remplacera ans par exe et ans servira a mettre le dernier  résutat dans le calcul
        }

        self.text_mode_actions = {
            KEY_BACKSPACE : lambda : self.text_focused_button.del_char() ,
            "lettres" : [KEY_ONE,KEY_TWO,KEY_THREE,KEY_FOUR,KEY_FIVE,KEY_SIX,KEY_SEVEN,KEY_EIGHT,KEY_NINE, KEY_ZERO, KEY_ANS, KEY_DOT, KEY_SHIFT, KEY_PLUS, KEY_DIVISION, KEY_MINUS, KEY_MULTIPLICATION,KEY_SQRT, KEY_COSINE]
        }

        self.action_rate_constant = 0.15
    
    def main_loop(self) :       
        self.grid_focused.draw()
        while True :
        ### LE DEBUG FAIT TOUT BEUGUER C NORMAL ###
            
                
            self.scan_actions()                
            if self.text_mode : 
                self.scan_text_mode_actions()
            time.sleep(0.01)    
    
    def scan_actions(self) : 
        for i in self.actions.keys() : 
                if keydown(i) : 
                    
                    self.actions[i]()
                    self.focused_button = self.grid_focused.get_focused_cell()
                    time.sleep(self.action_rate_constant)
                    continue
    
    def scan_text_mode_actions(self) : 
        if keydown(KEY_BACKSPACE) : # Touche H sur le clavier
            self.text_mode_actions[KEY_BACKSPACE]()
            time.sleep(self.action_rate_constant)
        else : 

            for j in self.text_mode_actions["lettres"] : 
                if keydown(j) : 
                    self.text_focused_button.add_char_with_action(j)
                    time.sleep(self.action_rate_constant)
                    break
    
    def enter_text_mode(self) : 
        self.text_mode = True
        if self.text_focused_button != None :
            self.text_focused_button.exit_text_mode()
        self.text_focused_button = self.focused_button
        self.focused_button.enter_text_mode()

    def exit_text_mode(self) : 
        self.text_mode = False
        if self.text_focused_button != None :
            self.text_focused_button.exit_text_mode()
            self.text_focused_button = None
    
    
    def switch_grid(self, grid) : 
        self.grid_focused = grid
        self.grid_focused.draw()
        self.focused_button = self.grid_focused.get_focused_cell()
        

## COMMANDES
def ajouter_lettre(char) :
    if interface.text_focused_button == None : 
        return
    interface.text_focused_button.add_char(char)

def activate_text_mode() : 
    interface.enter_text_mode()

def deactivate_text_mode() : 
    interface.exit_text_mode()



main_list = class_liste_principale()
main_list.focus_cell(main_list.get_cell(0,0))

interface = class_interface(main_list)
interface.main_loop()
