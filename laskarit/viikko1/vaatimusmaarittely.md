# Requirements Specification (Alustava)

## Purpose of the Application

The application is an Asteroids-style space adventure where the player controls a spaceship and tries to survive as long as possible by destroying asteroids. The player earns points for destroyed asteroids and aims to achieve the highest possible score.

## Users

The game has one user role: the player.

## Technical Requirements

* The game will be implemented using Python
* The Pygame library will be used for game development
* SQLite database will be used to store leaderboard data

## Planned Functionalities

### Basic Version Features

* Player can control the spaceship with arrow keys (acceleration, turning)
* Player can shoot with a weapon (spacebar)
* Various sized asteroids move around the play area and can be destroyed when hit
   * Larger asteroids break into smaller asteroids when hit
   * The smallest asteroids disappear completely when hit
* The player's ship is destroyed if it collides with an asteroid
* The game ends when the player loses all lives
* Player earns points for destroyed asteroids
   * Different sized asteroids give different point values
* The final score is displayed at the end of the game
* The game saves the highest score (high score) in a database

### Further Development Ideas

* Additional enemy types (e.g., hostile spaceships)
* Power-ups, such as:
   * Shield
   * Enhanced weapons
   * Extra lives
* Different difficulty levels (easy, medium, hard)
* Sound effects and background music
* Graphical user interface for starting the game and changing settings
* Level/stage system with increasing difficulty
* Player profile creation and score statistics storage in the database
* Ability to pause the game and continue later
* Different game modes (time trial, survival mode)

## User Interface Draft

The game's user interface consists of the following views:

1. **Start Screen**
   * Game title
   * Button to start the game
   * Button to view high scores
   * Button to read instructions

2. **Game View**
   * Starry background
   * Player's spaceship in the center
   * Score displayed at the top
   * Remaining lives visible

3. **End Game Screen**
   * Player's score
   * Best score (high score)
   * Button to start a new game
   * Button to return to the start screen

---
*Note: AI was used in the editing of this document*