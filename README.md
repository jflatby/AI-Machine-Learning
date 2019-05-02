# AI-Machine-Learning
Using a neural network to have an AI teach itself to play a simple 
game using unsupervised reinforcement learning in python3.
<div class="dritt">
<img src="https://media.giphy.com/media/1zlDb7dbcpFV6ZZhyv/giphy.gif" alt="drawing" width="400"/> <img src="https://media.giphy.com/media/1dGZVe0j11AfHvEnsI/giphy.gif" alt="drawing" width="400"/> 
<p align="center">Untrained vs. trained AI</p>
</div>

The game is made using pygame, and the neural network is set up using 
keras which uses a tensorflow backend, all of which need to be installed 
for this program to work.


The neural network consists of a single input node in the input layer, 
one hidden layer with 120 neurons, and an output layer with two nodes.
The input is solely defined by one boolean which is True/False depending 
on whether the position of the food is to the right or left of the current 
direction vector. In other words whether the angle between those two vectors 
is larger or smaller than 180 degrees.

Positive reward is given when food is collected, negative reward is given on death 
and otherwise no reward is given. In the first 30 games, a decreasing amount of 
randomness is applied to the decision-making process for the AI, to make sure
it keeps trying new things in the beginning.

Given this "simple" setup of one input and two output nodes, the AI learns the right 
way to play the game pretty quickly, depending on how long it takes to randomly get 
the first couple points. The negative reward on death makes it so that it usually 
figures out in the first 2-4 games that turning a lot lets it survive longer. 
After 10-20 games it usually gets the idea, and starts consistently turning towards the food.
At game 30 and onwards the randomness is taken out of the process and it acts solely on its own
prediction. 

However the game is intentionally designed so that the player will always die even if the AI 
constantly turns the correct way. The turning speed is set pretty low compared to the movement speed, 
which makes it so that the turning radius is pretty big. So when the food spawns close to the wall
the player is likely to die after collecting it. If the turning speed is set really high the AI would
probably be able to play the game forever.

An idea moving forward is to add collision detection to the front-right and front-left of the player, 
giving the neural network two more booleans as input. Hopefully the AI would be able to learn to use those
booleans to avoid the wall, and maybe in the end learn to pick up food that is close to the wall without dying.
