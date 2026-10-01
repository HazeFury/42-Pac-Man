# Devlog

## Explanation of what we built day after day on this project.

### Day 1

- Discovery and analysis of the subject as a team (**both**)
- Setup of the Trello board and discussion about project organization (**both**)
- Repository creation and establishment of collaborative workflow processes (**both**)
- Discovery of Pygame using simple examples (**marberge**)

### Day 2

- Parsing the configuration file (**gchmilew**)
- Creation of a simple menu using Pygame (**marberge**)
- Creation of reusable UI components and views to streamline development (**marberge**)
- Discovery and familiarization with MazeGenerator (**gchmilew**)

### Day 3

- Creation of the Cell class representing each maze cell (**gchmilew**)
- Creation of the Maze class to generate a matrix of Cells forming the maze (**gchmilew**)
- Algorithm for adding pac-gums to the grid (**gchmilew**)
- Visual rendering of the maze, pac-gums, and super pac-gums (**marberge**)

### Day 4

- Alignment of Pac-Man on the grid and movement strictly within cells rather than free movement (**gchmilew**)
- Addition of wall collisions (**gchmilew**)
- Addition of score tracking when Pac-Man eats pac-gums (with pac-gums disappearing from the screen) (**gchmilew**)
- Code refactoring to put the GameEngine at the core of the logic (**marberge**)
- Ghost rendering (no movement yet) (**gchmilew**)

### Day 5

- Collision detection between Pac-Man and ghosts (print only for now) (**gchmilew**)
- Ghost AI => BFS algorithm for each ghost (**gchmilew**)
- Replacement of hardcoded values with those from the config file (**gchmilew**)
- Addition of the EndGameView for the end of the game (**marberge**)
- Addition of the HighScoreView to display the top 10 scores (**marberge**)

### Day 6

- GameEngine refactoring (reassignment of code logic to the appropriate classes: Ghost, Player, HighScore) (**gchmilew**)
- Merging GameOverView and WinView into a single file: EndGameView (**marberge**)
- Addition of the player's score to the highscore file (**marberge**)

### Day 7

- Displaying the score at the end of the game (**marberge**)
- Displaying the top 10 scores by reading the "highscore.json" file (**marberge**)
- Updating the config file to include levels (**marberge**, **gchmilew**)
- Updating the parser to match the new config (**gchmilew**)
- Ghosts become edible when eating a super pac-gum / ghosts respawn after the cooldown (**gchmilew**)
- Resetting positions of all movable entities when a life is lost (**gchmilew**)
- Ghost flee algorithm (**gchmilew**)

### Day 8

- Updating Pac-Man sprites according to his actual direction (**marberge**)
- End-of-level system (victory and defeat) (**marberge**)
- Addition of the pause option during a game (**marberge**)
- Complete cheat system implementation (**marberge**)
- Smoother movement animation for entities (**gchmilew**)
- Various adjustments: 
	- Super pac-gums reset on level change (**gchmilew**)
	- Revision of the entity spawn system (next level or new game) (**gchmilew**)

### Day 9-10-11

- Improvement of various timers and game pause logic (**gchmilew**)
- Fixing ghost rendering upon player defeat and respawn (**gchmilew**)
- Improved visual collisions (**gchmilew**)
- Addition of a game instructions window (**marberge**)
- Modification of the pause menu (**gchmilew**)
- Setup of the final package creation (**marberge**)
- Refactoring of multiple classes (game_engine, ghost, player) (**gchmilew**)
- Various minor improvements (**gchmilew**, **marberge**)

### Day 12

- Writing the README (**marberge**)
- Levels 2 to 10 are now truly random (seed-based) (**marberge**)
- Visual fix for desynchronized Pac-Man death animations (**gchmilew**) 
- Debugging Pac-Man's impact against walls (**gchmilew**)
- MyPy corrections and addition of missing docstrings (**gchmilew**)
- Various minor improvements (**gchmilew**, **marberge**)


### DAY 13

- Fixing various minor issues (**gchmilew**)
- Update project management files (**marberge**)
- Deployed to itch.io (**marberge**)