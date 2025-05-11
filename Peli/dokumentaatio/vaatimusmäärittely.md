# Requirements Specification

## Purpose of the Application
The application is an Asteroids-style space survival game where the player controls a spaceship and tries to survive as long as possible by destroying asteroids. The player earns points for destroyed asteroids and aims to achieve the highest possible score.

## Users
The game has one user role: the player.

## Technical Requirements
The game is made in Python
The game uses Pygame

## Functionalities
Player can control the spaceship with arrow keys (acceleration, turning)
Player can shoot with a weapon
Various sized asteroids move around the play area and can be destroyed when hit
The Player's ship loses health if it collides with an asteroid
The game ends when the players health runs out
Player earns points for destroyed asteroids
The final score is displayed at the end of the game
The game saves the highest score (high score) in a database

## User Interface
The game's user interface consists of the following views:

### Start Screen
    - Game title
    - Button to start the game
    - Button to view high scores
    - Button to exit the game

### Game View
    - Player's spaceship
    - Score displayed at the top
    - Remaining life visible

### End Game Screen
    - Player's score
    - Best score (high score)
    - Button to start a new game
    - Button to return to the start screen
