# MonkeyJump
`pygame` based game inspired by the  Dinosaur Game built into the Google Chrome web browser.

 - `main.py`: Main script. The fame loop is defined here. 
 - `obstacle.py`:  Defines the classes Obstacle and ObstaclePool. The latter is used for optimising performance by reusing obstacle objects.
 - `monkey.py`: Instructions for the main character.
 - `peanut.py`: Another obstacle.

Usage: 
> python main.py

## Reinforced learning
The game can be used for reinforcement learning by creating a custom Gym environment compatible with Stable-Baselines3. See repository [Learn_MonkeyJump](https://github.com/MartinezAgullo/Learn_MonkeyJump) for this the RL integration.
