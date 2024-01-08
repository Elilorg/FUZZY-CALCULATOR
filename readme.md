# Installation

- Installer python3.11
- installer les packages python avec la commande suivante : 

```
pip install -r requirements.txt
```
*sur certaines machines, vous devrez peut etre lancer le programme en mode administrateur.*

Les controles : 
Voici les nouveaux controles : 

- les fleches pour bouger 
- entrée pour rentrer en mode texte
- maj pour faire un espace 
- point pour faire un point
- les touches des numéros pour faire des numéros

# A faire 

- AJOUTER UN MENU : **FAIT** 

- FAIRE ROULER LA LISTE DE CALCULS  : **FAIT**
    - la liste s'étend automatiquement : fait
    - plus que 26 variables serait bien. 
    - petit bug : la couleur reste en focus quand on fait monter la liste : **fix**
- CREER UN MODE TEXTE AVEC UN ECHAP ( LES ARROW KEYS verticales ) 
    - créer text mode basique : **fait**
    - disocié le bouton texte focused du bouton focused : **fait**
    - créer un curseur pour la navigation

- CREER LA CALCULATRICE
    - Creer les objets flous (IFT, NTF, Intervalles, etc..0) done !  : **fait**
    - intégrer les calculs avec l'interface : *en cour*
    

# Attention

- Ne pas utiliser les décorateurs comme ```@property```
- Ne pas utiliser d'autres packages que maths, time et ceux dans le requirement.txt
- Les noms de variables doivent être en minuscule et sans accent
- Les f string ne sont pas supportées
- On ne peut pas utiliser *variable_liste pour passer les éléments d'une liste d'un coup
- Les ```raise error``` ne fonctionnent pas
- On ne peut pas importer de fonction spécifique. C'est pourquoi on est forcé d'écrire : ```from package import *```


Tout cela n'est pas permis par la numworks qui ne supporte pas ces feature de python. 

# Structure de l'interface 
**la class bouton** : il fit dans la grid, il contient des infos sur ou il est dans la grid. De la, c'est la grid qui lui donne sa position sur l'écran, et sa taille pour qu'il puisse etre déssiné


**la class textinput** : c'est un dérivé de la classe bouton mais en plus de  ca, son action quand activé est de lancer le text mode, il a aussi ka fonction add char et del char qui permettent d'ajouter et retirer les caractère. Il a également deux méthode : enter_text_mode et exit_text_mode. Son action est toujours : toggle text mode : si il est en text mode il en sors, et si il est en dehors du text mode il y entre. 

**la class bouron_calcul** C'est elle qui gère de stocker et interpréter le calcul etstocker et afficher le résultat. Le résultat est un objet flou ou une erreur. (on pourrais peut etre implémenter un objet Erreur qui contient l'erreur) qui est un texte qui commence par ERREUR. Quand on fait un calcul il y a 2 possibilité. 
1. On crée une variable a partir de nombre, de zéro
    - On récupère le type d'objet qu'on veut a partir du menu
    - On parse les nombres (séparés par des espaces)
    - On crée l'objet 
    - on le renvoie dans self.resultat
2. On fait un calcul entre 2 objets flous. 
    - Ici, il faut récupérer les résultats des autres boutons calcul, (c la liste qui le fait?)  *ici, a l'aide de self.grid, on fait self.grid.calculs[id] et on retrouve nos petits comme ca car les boutons ont acces a leur grid. C'est la liste globale qui gère la grid*
    - interpréter le calcul
    - renvoyer le résultat dans self.résultat 
3. Un calcul entre 1 objet flou et un scalaire. *la question est quelle touche et symbole pour ce genre d'opérations ?*
    - On récupère les résultats
    - On interprète le calcul
    - on renvoie. 
Donc : comment on récupère les anciens résultats. 

**la class bouton valeur** Cette classe représente les boutons qui sont a gauche des calcul. Elle permettent d'ajouter leur id au calcul en cour simplement en se déplaceemnt et en appuyant sur entrée. Elle définis simplement l'action d'ajouter son id a l'input qui est focused.

**la class grid** : Elle a une hauteur et une largeur. Elle divise l'écran et contient les boutons. Elle contient également l'information de la cellule sur la quelle on est focus. C'est aussi elle qui gère le fait de focuser une de ses cell, et de déplacer le focus vers le haut ou le bas. on y ajoute des boutons via add bouton. 

**la class liste_principale** : elle est une grid spéciale : elle contient des éléments bien définis, en colonne. elle se charge de déplacer les éléments qu'elle contient vers le haut, ou vers le bas quand on arrive en haut ou en bas de la liste. son self.rows contient tout les boutons, meme ceux en dehors de l'écran


**la classe Interface**
C'est elle qui récolte les inputs. Elle controle les deux grid (bientot deux) qui composent l'interface. C'est aussi elle qui gère le text mode et donc l'envoi du caractère au text input


*problème à résoudre : les boutons text input ont pour action de activer text mode dans l'interface, donc donner un ordre a un objet au quel ils n'ont pas accès mais en vrai pk pas? Juste daire une fontion externe au code qui s'appelle activate text mode. C juste que les txt inuput sont initialisés dans la liste principale et ca ca va pas. Il faudrait définir l'interface d'abord, puis la fonction d'activation du mode texte, puis les boutons et la liste principale*

compliqué.