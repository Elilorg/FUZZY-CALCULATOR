# Installation

## Pour coder et tester sur ordi

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

Pour actualiser le code installé par les utilisateur, il faut run ```minify.sh``` qui minifie les fichier, de manière à ce qu'ils soient utilisables par l'utilisateur, puis les commit. 

**ATTENTION** ne pas commit dans minified sans avoir testé AUSSI sur la calculatrice. 


## Pour tester sur la numworks

### Installation
Nous n'avons pas encore tester cette dernière vertion de notre programme sur la numworks. 
Pour l'installer, vous devez mettre les 2 fichiers python du dossier ```minified``` sur vortre calculatrice : 
```fuzzy_logic.py``` et ```numworks_1.py```. La vertion que vous devez installer se trouve dans le dossier apellé ```minified```. C'est bien les fichiers de ce dossier que vous devez installer, sans quoi le script ne marchera pas car il prend trop de place sur la calculatrice. 

Pour les installer, il faut aller sur son compte, puis dans "mes scripts". 
Cliquer sur "Ajouter un script", et faire de meme pour l'autre fichier python. Attention a bien les ajouter en concervant leur nom exact !
Maintenant qe vos scripts sont sur le site, vous pouvez cliquer sur "Envoyer sur ma calculatrice". 

Ceci fait, dans la liste des scripts c'est numworks_1.py qu'il faut séléctionner.

### Commandes de la calculatrice : 
- nombres -> les nombres 
- espace -> ```Ans```
- +, *, -, / -> meme touches
- Entrer dans le mode texte -> ````EXE````
- En mode, texte, ajouter un nom de variable -> aller sur le bouton (ex : ```A=```) et ```EXE```.
- troncature : touche racine carrée (écrit le symbole #)
- possibilité : touche cos (écrit le symbole ```^_v```) 

Pas encore ajouté : 
t-troncature, alpha coupe. Déjà dans le fichier math mais pas l'interface

### Comment l'utiliser 

L'interface se présente sous la forme d'une grille, avec à gauche les boutons dit "valeurs" et à droite, les grand boutons dit "calculs". (appelés CALC par défaut). 
1. Le mode texte : 
    - On l'active en appuyant sur la touche ```EXE``` en étant sur un bouton calcul
    - On peut ensuite se déplacer du mode texte et on restera en mode texte sur la meme case 
    - On peut alors entrer des nombres. En utilisant les boutons de la colonne de gauche, on peut réutiliser des résultats précédents. 
    - pour terminer le calcul, il faut sortir du mode texte, en réappuyant sur le bouton calcul en question avec ```EXE```, ou entrer en mode texte sur un autre bouton de calcul, de la meme manière. 
2. Ajouter des intervalles flous
    - Pour ajouter un intervalle net : inscrire les deux nombre séparés par un espace (touche ```ANS```) (Ex : ```13 20.5```)
    - pour ajouter un NFT, entrer trois valeurs séparées par des espaces (Ex : ```1 2 3```) 
        - si vous voulez entrer un NFT avec une hauteur != de 1, bous pouvez ajouter un nombre, inférieure à 0 à la fin, toujour séparées par un espace  (EX : ```1 2 3 0.6```)
    - pour ajouter un IFT, entrer 4 valeurs séparées par des espaces (Ex : ```1 2.5 3.5 4```)
        - pour un IFT de hauteur != 1, ajouter une valeur < à 1, séparée par un espace (Ex : ```1 2.5 3.5 4 0.2```)
    - **Attention !** Les nombre à virgule s'écrivent avec le ```.``` 

3. Faire des calculs
    - vous pouvez utiliser les opérateurs ```+```, ```-```, ```*```, ```/```
    - Et ce entre les intervalles flous et aussi entre un espace flou et un scalaire. 

# A faire 

- AJOUTER UN MENU : **FAIT** 

- FAIRE ROULER LA LISTE DE CALCULS  : **FAIT**
    - la liste s'étend automatiquement : **fait**
    - plus que 26 variables serait bien. **fait**
    - petit bug : la couleur reste en focus quand on fait monter la liste : **fix**
- CREER UN MODE TEXTE AVEC UN ECHAP ( LES ARROW KEYS verticales ) 
    - créer text mode basique : **fait**
    - disocié le bouton texte focused du bouton focused : **fait**
    - créer un curseur pour la navigation

- CREER LA CALCULATRICE
    - Creer les objets flous (IFT, NTF, Intervalles, etc..0) done !  : **fait**
    - intégrer les calculs avec l'interface : **fait**
- TERMINER : 
    - ajouter le calcul de possibilité
    - améliorer l'interface     
    - Arrondir les valeurs au millième

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


# Les choses à ne pas faire sur python numworks

- Ne pas utiliser les décorateurs comme ```@property```
- Ne pas utiliser d'autres packages que maths, time et ceux dans le requirement.txt
- Les noms de variables doivent être en minuscule et sans accent
- Les f string ne sont pas supportées
- On ne peut pas utiliser *variable_liste pour passer les éléments d'une liste d'un coup
- Les ```raise error``` ne fonctionnent pas
- On ne peut pas importer de fonction spécifique. C'est pourquoi on est forcé d'écrire : ```from package import *```
- utiliser les méthodes ```str.isnumeric()``` ou ```str.isdigit()```


Tout cela n'est pas permis par la numworks qui ne supporte pas ces feature de python. 