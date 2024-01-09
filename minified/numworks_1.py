_D='lettres'
_C=True
_B=False
_A=None
from ion import*
from kandinsky import*
import time
from fuzzy_logic import*
width_constant=320
height_constant=240
black=0,0,0
white=255,255,255
red=255,0,0
blue=0,0,255
yellow=255,255,0
green=0,255,0
g=green
KEY_TO_CHAR={KEY_ONE:'1',KEY_TWO:'2',KEY_THREE:'3',KEY_FOUR:'4',KEY_FIVE:'5',KEY_SIX:'6',KEY_SEVEN:'7',KEY_EIGHT:'8',KEY_NINE:'9',KEY_ZERO:'0',KEY_ANS:' ',KEY_DOT:'.',KEY_SHIFT:' ',KEY_PLUS:'+',KEY_MINUS:'-',KEY_MULTIPLICATION:'*',KEY_DIVISION:'/'}
class class_bouton:
	'\n   \n    '
	def __init__(self,text,color,x,y,focused=_B,action=_A):
		"\n        les x sont les colonnes ou le bouton s'étend dans la grid\n        les y sont les lignes ou le bouton s'étend dans la grid\n        x et y doivent etre des listes\n\n        ";self.text=text;self.color=color;self.focused_color=color[0]+40,color[1]+40,color[2]+40;self.focused=focused
		if action is not _A:self.action=action
		self.x=x;self.y=y;self.height=_A;self.width=_A;self.coordinates=_A;self.grid_coordinates=[self.x[0],self.y[0]];self.grid=_A
	def draw(self,color=_A):
		self.updater_coordonnees()
		if color is not _A:color_used=color
		elif self.focused:color_used=self.focused_color
		else:color_used=self.color
		print('COLOR USED',color_used);left_top=self.coordinates[0],self.coordinates[1];fill_rect(left_top[0],left_top[1],self.width,self.height,color_used);draw_string(self.text,left_top[0],left_top[1],(0,0,0))
	def updater_coordonnees(self):
		if self.grid is _A:print('ERREUR',self.text,"n'est pas encore ajouté à une grille !")
		self.grid.updater_coordonees(self)
	def focus(self):print(self.text,'at',self.grid_coordinates,'is focused');self.focused=_C;self.draw()
	def unfocus(self):self.focused=_B;self.draw()
	def __str__(self):return self.text+' '+str(self.grid_coordinates)
	def changer_coordonnees(self,x=0,y=0):self.grid_coordinates[0]+=x;self.grid_coordinates[1]+=y;self.x=list(map(lambda x_orginal:x_orginal+x,self.x));self.y=list(map(lambda y_orginal:y_orginal+y,self.y));self.coordinates=_A
class classtextinput(class_bouton):
	' \n    Une extention de la classe bouton. Elle a quelques particularitée en plus. \n    - Sa touche "action" permet de faire entrer l\'interface en mode texte et donc de changer le texte\n    - En mode texte, l\'interface utilise ces fonctions : \n        - del_char permet de supprimer le dernier caractère \n        - add_char permet d\'ajouter un caractère\n        - enter_text_mode est appellé quand l\'interface entre en text-mode, et permet d\'effacer le texte par défaut\n        - exit text_mode est appellé quand l\'interface quitte le mode texte et permet de remettre le texte par défaut si on a rien écrit\n    '
	def __init__(self,text,color,x,y,focused=_B,action=_A):action=self.toggle_text_mode;super().__init__(text,color,x,y,focused,action);self.text_mode=_B;self.text_mode_color=230,230,230
	def draw(self):
		if self.text_mode:super().draw(self.text_mode_color)
		else:super().draw()
	def add_char(self,char):self.text+=char;draw_string(self.text,self.coordinates[0],self.coordinates[1],(0,0,0))
	def add_char_with_action(self,key_number):self.add_char(KEY_TO_CHAR[key_number])
	def del_char(self):
		if len(self.text)==0:return
		self.text=self.text[:-1];self.draw()
	def enter_text_mode(self):
		self.text_mode=_C
		if self.text==_A:self.text=''
		self.draw()
	def exit_text_mode(self):
		self.text_mode=_B
		if self.text=='':self.text=_A
		self.draw()
	def toggle_text_mode(self):
		"\n        Ce fonctionnement est basé sur l'idée que c'est bien ce bouton qui est le text_focused_button quand toggle_text_mode est appelé\n        Et donc que c'est bien ce bouton qui va entrer ou sortir du mode texte, sinon on pourrais avoir plusieurs boutons en mode texte.\n        "
		if self.text_mode:deactivate_text_mode()
		else:activate_text_mode()
class boutonvaleur(class_bouton):
	def __init__(self,text,color,x,y,focused=_B,action=_A):self.char=text[0];super().__init__(text,color,x,y,focused,action)
	def action(self):ajouter_lettre(self.char)
class result_type_selector(class_bouton):
	def __init__(self,text,color,x,y,focused=_B,action=_A,type_resultat='%'):super().__init__(text,color,x,y,focused,action);self.type=type_resultat
	def action(self):ajouter_type_resultat(self.type);change_grid(main_list)
class class_bouton_calcul(classtextinput):
	def __init__(self,text,color,x,y,focused=_B,action=_A):super().__init__(text,color,x,y,focused,action);self.resultat=_A;self.type_resultat='%'
	def draw(self):
		A='CALC';print('Draw result with type',self.type_resultat);text=self.text
		if text is _A:text=A
		self.text=text;super().draw();result_affiche=str(self.resultat)if self.resultat!=_A else''
		if text==A:self.text=_A
		draw_string(result_affiche,self.coordinates[0],self.coordinates[1]+int(self.height/2),(0,0,0))
	def exit_text_mode(self):self.resultat=self.evaluate(self.text);super().exit_text_mode();self.draw()
	def del_char(self):
		if len(self.text)==0 and self.type_resultat!='%':self.type_resultat='%';self.draw()
		return super().del_char()
	def add_char(self,char):self.text+=char;self.draw()
	def ajouter_resultat(self,type_resultat):self.type_resultat=type_resultat;self.draw()
	def get_value(self,chaine):
		"\n        si la chaine est un nb, on le converti en trapèse flou mais net ducoup. \n        Sinon aller chercher avec l'id\n        Ca ca va dans l'interface de la calculatrice\n        ";check_num=chaine.replace(',','').replace('.','')
		if isnumeric(check_num):
			nb=convert_to_float(chaine)
			if type(nb)==Erreur:return nb
			return Trapeseflou(nb,nb,nb,nb,1)
		else:return self.grid.get_result_by_id(chaine)
	def calcul(self,chaine):
		A='#'
		if'+'in chaine:a,b=self.split_chaine(chaine,'+');return add(a,b)
		if'-'in chaine:a,b=self.split_chaine(chaine,'-');return sub(a,b)
		if'*'in chaine:a,b=self.split_chaine(chaine,'*');return mul(a,b)
		if'/'in chaine:a,b=self.split_chaine(chaine,'/');return div(a,b)
		if A in chaine:return tronc(self.calcul(chaine.split(A)[0]),convert_to_float(chaine.split(A)[1]))
		return self.get_value(chaine)
	def split_chaine(self,chaine,symbole):" \n        cette focntion fait partie de la recurtion de calcul. \n        elle permet de diviser une chaine en deux parties\n        et de lancer le calcul sur chacune d'elles\n        ";splited=chaine.split(symbole);return self.calcul(splited[0]),self.calcul(''.join(splited[1:]))
	def evaluate(self,chaine):
		'\n        Le parseur\n        '
		if chaine=='':return
		chaine_check=chaine.replace(' ','').replace(',','').replace('.','')
		if isnumeric(chaine_check):return parseIFT(chaine)
		else:
			try:return self.calcul(chaine.replace(' ',''))
			except Exception as e:raise e;return Erreur('Le calcul a échoué')
class class_grid:
	'\n    La grille contient l\'ensemble des boutons. Ici, chaque élément est appellé une "cell".\n    On accède au contenu de la grille avec la methode get_cell(x, y)\n    ATTENTION : pour accéder au contenu des cell avec la propriété __grid, il faudra utiliser :  self.__grid[y][x]\n    Les méthode suivantes sont aussi disponibles : \n    - get_focused_cell() : renvoie le contenu de la cellule en cours de selection\n    - focus_cell(button : Bouton) : déselectionne la cellule en cours de selection, puis selectionne le bouton qu\'on vien de lui passer.\n    - __getitem__ permet de récupérer les contenus des cellules avec grid[y][x] ou grid est l\'objet grid et non la propriété __grid. Cela permet une interface plus simple\n    - __setitem__ permet de modifier les contenus des cellules avec grid[y][x] \n    - travel_x() permet de focus la cellule directement a droite ou a gauche de la cellule en cours de selection\n    - travel_y() permet de focus la cellule directement en haut ou en bas de la cellule en cours de selection\n\n    Les paramètre suivants sont disponibles lors de la création de la grille \n    - offset_x : position de la grille sur l\'axe x (coin supérieur gauche)\n    - offset_y : position de la grille sur l\'axe y (coin supérieur gauche)\n    - width : largeur de la grille\n    - height : hauteur de la grille\n    - x_div : nb de divisions sur l\'axe x\n    - y_div : nb de divisions sur l\'axe y\n\n    Les valeurs par défaut sont celles de la grille principale\n\n    '
	def __init__(self,offset_x=0,offset_y=0,width=width_constant,height=height_constant,x_div=4,y_div=5):'\n        On initialise la grille avec sa hauteur et sa largeur\n        ';self.offset_x=offset_x;self.offset_y=offset_y;self.x_div=x_div;self.y_div=y_div;self.width=self.x_div;self.height=self.y_div;self.cell_w=width//self.x_div;self.cell_h=height//self.y_div;self.focused=[0,0];self.__grid=[[_A for j in range(self.width)]for i in range(self.height)]
	def get_cell(self,x,y):
		'\n        retourne la cellule\n        '
		if x<0 or x>self.width-1:0
		if y<0 or y>self.height-1:0
		return self.__grid[y][x]
	def updater_coordonees(self,cell):"\n        donne au bouton ces veritables coordonées pour qu'il puisse se dessiner au bon endroit sur l'écran\n        ";cell.coordinates=cell.x[0]*self.cell_w+self.offset_x,cell.y[0]*self.cell_h+self.offset_y;cell.height=self.cell_h*len(cell.y);cell.width=self.cell_w*len(cell.x)
	def get_focused_cell(self):
		'\n        retourne la cellule focused. Celle ci ne devrait pas etre nulle. \n        ';cell_content=self.__grid[self.focused[1]][self.focused[0]]
		if cell_content is _A:print('Cell',{self.focused},'is empty');print(self.__grid);return
		return cell_content
	def focus_cell(self,cell):
		if cell is _A:0
		button_to_unfocus=self.get_cell(self.focused[0],self.focused[1])
		if button_to_unfocus is _A:print('UNFOCUSING EMPTY CELL')
		button_to_unfocus.unfocus();cell.focus();self.focused=[cell.grid_coordinates[0],cell.grid_coordinates[1]]
	def __getitem__(self,index):return self.__grid[index]
	def __setitem__(self,index,value):self.__grid[index]=value
	def travel_x(self,i):
		"\n        n'admet que 1 et -1\n        ";x,y=self.focused
		if i==1:
			for cell in self.__grid[y][x+1:]:
				if cell is not _A:self.focus_cell(cell);return
		elif i==-1:
			for cell in self.__grid[y][:x][::-1]:
				if cell is not _A:self.focus_cell(cell);return
			return
	def travel_y(self,i):
		"\n        On parcour les lignes pour trouver la ligne au dessus ou au dessou qui renvoie\n        n'admet que 1 et -1 \n        ";x,y=self.focused
		if i==1:
			for list in self.__grid[y+1:]:
				if list[x]is not _A:self.focus_cell(list[x]);return
			print(self.__grid);return
		if i==-1:
			for list in self.__grid[:y][::-1]:
				if list[x]is not _A:self.focus_cell(list[x]);return
			print('EDGE');return
	def add_button(self,button):
		print('ADD TO GRID',button.text);x,y=button.grid_coordinates
		if self.affichable(button):
			self.__grid[button.grid_coordinates[1]][button.grid_coordinates[0]]=button
			for i in button.x:
				for j in button.y:
					if i==button.grid_coordinates[0]and j==button.grid_coordinates[1]:continue
					self.__grid[j][i]=_A
		button.grid=self
	def draw(self):
		for row in self.__grid:
			for cell in row:
				if cell is not _A and self.affichable(cell):cell.draw()
	def __str__(self):
		st=''
		for y in range(self.y_div):
			for x in range(self.x_div):st+=str(type(self.get_cell(x,y)));st+=' '
			st+='\n'
		return st
	def affichable(self,cell):
		if cell.grid_coordinates[0]<0 or cell.grid_coordinates[0]>self.x_div-1:return _B
		if cell.grid_coordinates[1]<0 or cell.grid_coordinates[1]>self.y_div-1:return _B
		return _C
class class_liste_principale(class_grid):
	def __init__(self):
		self.rows=[];ids=[]
		for j in range(10):ids+=[i+str(j)if j!=0 else i for i in'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
		self.ids=ids;self.remaining_ids=ids.copy();super().__init__(x_div=4,y_div=5)
		for i in range(self.y_div):self.append_list()
		self.rows[3][1].resultat='Heelo world'
	def move_up(self,cell):
		'\n        bouge un bouton de 1 vers le haut\n        ATTENTION : elle écrase la cellule vers laquelle le bouton est déplacé\n        ';x,y=cell.grid_coordinates
		if self.affichable(cell):self[y][x]=_A
		cell.changer_coordonnees(y=-1)
		if self.affichable(cell):self[y-1][x]=cell;cell.draw()
	def move_down(self,cell):
		'\n        bouge un bouton de 1 vers le bas. \n        ATTENTION : elle écrase la cellule vers la quelle le bouton est déplacé\n        ';x,y=cell.grid_coordinates
		if self.affichable(cell):self[y][x]=_A
		cell.changer_coordonnees(y=1)
		if self.affichable(cell):self[y+1][x]=cell;cell.draw()
	def go_down(self):
		'\n        fait descendre tout les boutons\n        ';self.get_focused_cell().unfocus()
		for i in self.rows[::-1]:self.move_down(i[0]);self.move_down(i[1])
		x,y=self.focused;print(x,y);self.focus_cell(self[y][x])
	def go_up(self):
		'\n        fait monter tout les boutons\n        ';self.get_focused_cell().unfocus()
		for i in self.rows:self.move_up(i[0]);self.move_up(i[1])
		x,y=self.focused;print(x,y);self.focus_cell(self[y][x])
	def append_list(self):
		print('APPEND LIST')
		if len(self.rows)==0:y_pos=0
		else:y_pos=self.rows[-1][0].grid_coordinates[1]+1
		if len(self.ids)==0:print('Plus de lettres');return
		bouton_calcul=class_bouton_calcul(_A,black,[1,2,3],[y_pos]);bouton_valeur=boutonvaleur(self.remaining_ids.pop(0)+' = ',white,[0],[y_pos]);self.add_button(bouton_calcul);self.add_button(bouton_valeur);self.rows.append((bouton_valeur,bouton_calcul))
	def travel_y(self,i):
		y=self.focused[1]
		if y==0 and i==-1 and self.rows[0][0].grid_coordinates[1]!=0:print('GO DOWN');self.go_down()
		elif y==self.y_div-1 and i==1:
			if self.rows[-1][0].grid_coordinates[1]==self.y_div-1:self.append_list()
			print('GO UP');self.go_up()
		else:super().travel_y(i)
	def get_result_by_id(self,id):
		'\n        Cette fonction fait la supposition que la liste est composée des id suivantes : \n        A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z\n        A1, A2, A3, A4 , etc...\n        '
		if type(id)!=str or len(id)==0 or len(id)>2:return Erreur(str(id)+' invalide id')
		print(self.ids);index=self.ids.index(id[0])
		if len(id)>1:
			try:index+=26*int(id[1])-1
			except:return Erreur('id invalide')
			index+=26*int(id[1])
		bouton=self.rows[index][1]
		if type(bouton.resultat)==Erreur:return Erreur('id'+' à renvoyé ERR')
		elif bouton.resultat is _A:return Erreur('bouton vide')
		return bouton.resultat
types=['INT','IFT','NFT']
class menu_secondaire(class_grid):
	def __init__(self):
		super().__init__(x_div=4,y_div=5)
		for i in range(len(types)):self.add_button(result_type_selector(types[i],black,[0,1,2,3],[i],type_resultat=types[i]+'[%]'))
	def travel_x(self,i):
		if i==-1:change_grid(main_list)
		return super().travel_x(i)
class class_interface:
	def __init__(self,grid,menu):self.main_grid=grid;self.menu=menu;self.text_mode=_B;self.text_focused_button=_A;self.grid_focused=self.main_grid;self.focused_button=self.grid_focused.get_focused_cell();self.actions={KEY_UP:lambda:self.grid_focused.travel_y(-1),KEY_DOWN:lambda:self.grid_focused.travel_y(1),KEY_LEFT:lambda:self.grid_focused.travel_x(-1),KEY_RIGHT:lambda:self.grid_focused.travel_x(1),KEY_EXE:lambda:self.grid_focused.get_focused_cell().action()};self.text_mode_actions={KEY_BACKSPACE:lambda:self.text_focused_button.del_char(),_D:[KEY_ONE,KEY_TWO,KEY_THREE,KEY_FOUR,KEY_FIVE,KEY_SIX,KEY_SEVEN,KEY_EIGHT,KEY_NINE,KEY_ZERO,KEY_ANS,KEY_DOT,KEY_SHIFT,KEY_PLUS,KEY_DIVISION,KEY_MINUS,KEY_MULTIPLICATION]};self.action_rate_constant=.15
	def main_loop(self):
		self.grid_focused.draw()
		while _C:
			if keydown(KEY_PI):change_grid(self.menu);time.sleep(self.action_rate_constant)
			self.scan_actions()
			if self.text_mode:self.scan_text_mode_actions()
			time.sleep(.01)
	def scan_actions(self):
		for i in self.actions.keys():
			if keydown(i):self.actions[i]();self.focused_button=self.grid_focused.get_focused_cell();time.sleep(self.action_rate_constant);continue
	def scan_text_mode_actions(self):
		if keydown(KEY_BACKSPACE):self.text_mode_actions[KEY_BACKSPACE]();time.sleep(self.action_rate_constant)
		else:
			for j in self.text_mode_actions[_D]:
				if keydown(j):self.text_focused_button.add_char_with_action(j);time.sleep(self.action_rate_constant);break
	def enter_text_mode(self):
		self.text_mode=_C
		if self.text_focused_button!=_A:self.text_focused_button.exit_text_mode()
		self.text_focused_button=self.focused_button;self.focused_button.enter_text_mode()
	def exit_text_mode(self):
		self.text_mode=_B
		if self.text_focused_button!=_A:self.text_focused_button.exit_text_mode();self.text_focused_button=_A
	def switch_grid(self,grid):self.grid_focused=grid;self.grid_focused.draw();self.focused_button=self.grid_focused.get_focused_cell()
def ajouter_type_resultat(type_resultat):
	if interface.text_focused_button==_A:return
	interface.text_focused_button.ajouter_resultat(type_resultat)
def ajouter_lettre(char):
	if interface.text_focused_button==_A:return
	interface.text_focused_button.add_char(char)
def activate_text_mode():print('Text mode activated');interface.enter_text_mode()
def deactivate_text_mode():print('Text mode deactivated');interface.exit_text_mode()
def change_grid(grid):interface.switch_grid(grid)
main_list=class_liste_principale()
menu=menu_secondaire()
interface=class_interface(main_list,menu)
interface.main_loop()