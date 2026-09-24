Voici un résumé détaillé des changements apportés pour passer d’un mouvement saccadé à un mouvement fluide à 60 FPS.

---

### 1. Le problème initial (Avant)

#### Comment cela fonctionnait :
- **Logique par case brute** : Pac-Man et les fantômes avaient des coordonnées entières sur la grille (`x` et `y` entiers, ex: `5, 10`).
- **Déplacement discontinu** : Dès que le timer interne atteignait le seuil de déplacement (`move_delay`), la coordonnée sautait brutalement d'une case entière d'un coup (`x += 1`).
- **Affichage direct** : La vue graphique calculait la position en pixels directement depuis ces coordonnées entières :
  ```python
  px = self.pacman.x * 32 + x_offset + 9
  py = self.pacman.y * 32 + y_offset + 8
  ```
- **Résultat visuel** : L'entité restait immobile pendant 100 ms (ou 500 ms pour un fantôme), puis sautait instantanément de 32 pixels. À l'écran, cela donnait une impression de téléportation et de saccade constante.

---

### 2. Le principe de la solution : L'Interpolation Linéaire (*Lerp*)

Pour avoir un rendu fluide sans casser la logique de grille (murs, BFS, pac-gums) :
1. **La logique du jeu reste sur la grille** : les entités continuent d'avoir des coordonnées entières (`x, y`) pour les collisions et l'IA.
2. **On retient la case de départ** : `(prev_x, prev_y)`.
3. **On calcule la progression du trajet** : un float de `0.0` (case de départ) à `1.0` (case d'arrivée) grâce au timer :
   $$\text{progress} = \frac{\text{timer}}{\text{move\_delay}}$$
4. **La position graphique est interpolée à chaque frame (60 FPS)** :
   $$\text{vis\_x} = \text{prev\_x} + (\text{x} - \text{prev\_x}) \times \text{progress}$$
   $$\text{vis\_y} = \text{prev\_y} + (\text{y} - \text{prev\_y}) \times \text{progress}$$

---

### 3. Détail des modifications fichier par fichier (Après)

#### A. [`player.py`](file:///home/gchmilew/42Cursus/Python/pac-man/src/core/player.py)
* **Avant** :
  - Seules `self.x` et `self.y` existaient.
  - Dans `next_move()`, on modifiait directement `x` ou `y`.
* **Après** :
  - Ajout des attributs `self.prev_x` et `self.prev_y`.
  - Dans `next_move()`, on sauvegarde la case actuelle avant de changer :
    ```python
    self.prev_x = self.x
    self.prev_y = self.y
    ```
  - Ajout de la méthode `get_visual_pos()` :
    - Si Pac-Man est à l'arrêt (`self.current_dir == "NONE"`), on renvoie directement `(self.x, self.y)` (évite les oscillations contre un mur).
    - Sinon, on calcule la position intermédiaire flottante grâce au ratio `self.timer / self.move_delay`.
  - Synchronisation de `prev_x` et `prev_y` dans `spawn()`.

---

#### B. [`ghost.py`](file:///home/gchmilew/42Cursus/Python/pac-man/src/core/ghost.py)
* **Avant** :
  - Les fantômes mettaient à jour `self.x` et `self.y` directement dans l'algorithme de fuite ou de BFS.
* **Après** :
  - Ajout de `self.prev_x` et `self.prev_y`.
  - Dans `ghost_ai()`, juste avant d'assigner les nouvelles coordonnées calculées par le BFS ou le déplacement aléatoire en mode effrayé :
    ```python
    self.prev_x, self.prev_y = self.x, self.y
    self.x, self.y = destination
    ```
  - Ajout de `get_visual_pos()` avec gestion de l'état `DEAD` (si le fantôme est mort, position fixe sans interpolation).
  - Réinitialisation propre de `prev_x, prev_y` et remise à zéro de `timer` dans `spawn()` et `reset_position()`.

---

#### C. [`game_engine.py`](file:///home/gchmilew/42Cursus/Python/pac-man/src/core/game_engine.py)
* **Avant** :
  - Quand Pac-Man rencontrait un mur, `current_dir` passait à `"NONE"` sans toucher au timer.
  - Dans `reset_position()`, seules les coordonnées cibles `x, y` étaient réinitialisées.
* **Après** :
  - Lors d'une collision contre un mur dans `_resolve_player_movement()` :
    ```python
    self.player.current_dir = "NONE"
    self.player.prev_x = self.player.x
    self.player.prev_y = self.player.y
    ```
    *Effet* : Empêche Pac-Man de rebondir/boucler visuellement sur place contre le mur.
  - Dans `reset_position()` : réalignement de `prev_x = x`, `prev_y = y` et réinitialisation de `timer = 0.0`.

---

#### D. [`game_view.py`](file:///home/gchmilew/42Cursus/Python/pac-man/src/views/game_view.py)
* **Avant** :
  - Les sprites étaient positionnés en multipliant les entiers discrets :
    ```python
    px = self.pacman.x * 32 + x_offset + 9
    py = self.pacman.y * 32 + y_offset + 8
    ```
* **Après** :
  - Utilisation de la position interpolée pour Pac-Man :
    ```python
    vis_x, vis_y = self.pacman.get_visual_pos()
    px = int(vis_x * 32) + x_offset + 9
    py = int(vis_y * 32) + y_offset + 8
    active_pacman_sprite.update_position(px, py)
    ```
  - Idem pour chaque fantôme :
    ```python
    for ghost, normal_sprite, frightened_sprite in self.ghost_sprite:
        g_vis_x, g_vis_y = ghost.get_visual_pos()
        pos_x = int(g_vis_x * 32) + x_offset + 9
        pos_y = int(g_vis_y * 32) + y_offset + 8
        normal_sprite.update_position(pos_x, pos_y)
        frightened_sprite.update_position(pos_x, pos_y)
    ```

---

### Résumé des bénéfices
| Critère | Avant | Après |
|---|---|---|
| **Animation visuelle** | Téléportation de 32 px toutes les 100~500 ms | Défilement continu pixel par pixel à 60 FPS |
| **Logique de grille (murs, BFS, points)** | Basée sur des entiers `(x, y)` | Reste intacte, 100 % basée sur des entiers `(x, y)` |
| **Gestion des arrêts / murs** | N/A | Arrêt net et propre sans tremblement |