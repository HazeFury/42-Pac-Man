# Devlog

## Explaination of what we build day after day on this project.


### Day 1

- Découverte et analyse du sujet en équipe (tous les deux)
- Mise en place du Trello et discussion autour de l'organisation du projet (tous les deux)
- Création du repo et mise au point des processus de travail collaboratif (tous les deux)
- Découverte de Pygame avec des exemples simples (marberge)

### Day 2

- Parsing du fichier de configuration (gchmilew)
- Création d'un menu simple avec pygame (marberge)
- Création de composant ui réutilisable et de vues pour simplifier le developpement (marberge)
- Découverte et prise en main du MazeGenerator (gchmilew)

### Day 3

- Création de la classe Cell symbolisant chaque cellule du labyrinthe (gchmilew)
- Création de la classe Maze pour générer une matrice de Cell formant le labyrinthe (gchmilew)
- Algorithme d'ajout des pac-gums sur la grille (gchmilew)
- affichage visuel du labyrinthe, des pac-gums et super pac-gums (marberge)

### Day 4

- Alignement du pacman sur la grille et déplacement dans les cellules plutôt que déplacement libre (gchmilew)
- rajout des collisions dans les murs (gchmilew)
- rajout du score lorsque pacman mange des pacgums (et les pacgums disparaissent de l'écran) (gchmilew)
- refacto du code pour le GameEngine soit au coeur de la logique (marberge)
- affichage des ghosts (pas encore de déplacement) (gchmilew)


### Day 5

- Détection de collision entre pacman et ghost (print uniquement pour l'instant) (gchmilew)
- IA des ghost => algorithme BFS pour chaque ghost (gchmilew)
- remplacement des valeurs en dure par celles du fichier de config (gchmilew)
- ajout du EndGameView pour la fin de la partie (marberge)
- ajout du HighScoreView pour afficher le top 10 des scores (marberge)


### Day 6

- refacto du GameEngine (réattribution d'une partie du code dans les classes concernés (Ghost, Player, HighScore)) (gchmilew)
- merge du la GameOverView et la WinView en un seul fichier : EndGameView (marberge)
- ajout du score du joueur au fichier des scores. (marberge)


### DAY 7

- affichage du score en fin de partie (marberge)
- affichage du top 10 score en lisant le fichier " highscore.json" (marberge)
- mise à jour du fichier de config pour avoir des niveaux (marberge, gchmilew)
- mise à jour du parser pour s'adapter à la config (gchmilew)
- ghost mangable lorsqu'on mange un super pacgum / réapparition des ghosts après le cooldown (gchmilew)
- reset des positions de tout les movable lorsqu'on perd une vie (gchmilew)
- algo des fuite des ghosts (gchmilew)


### DAY 8

- Mise à jour des sprites du pacman suivant sa direction réelle (marberge)
- Système de fin de niveau (victoire et défaite) (marberge)
- Ajout de l'option pause pendant une partie (marberge)
- Système de cheat complet (marberge)
- Animation plus smooth de déplacement pour les entités (gchmilew)
- Ajustement divers : 
	- super pacgums reset au changement de niveau (gchmilew)
	- Révision du système de spawn des entités (level suivant ou new game) (gchmilew)
