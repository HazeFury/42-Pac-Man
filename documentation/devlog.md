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