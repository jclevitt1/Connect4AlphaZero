Alpha Zero Solver for Connect Four

This is a project for the development of my own knowledge of Deep Reinforcement Learning. The goal is to create a solver for Connect Four using the Deep Reinforcement Learning Algorithm used in Google's Alpha Zero published in 2016 (could have been 2015). This is my first project using this algorithm, and first project working with Convolutional Neural Networks; thus I felt a simple game such as Connect Four was a great starting point- as it has already been solved and thus the functionality of my algorithm is easily testable.

I abstracted most of the files that determine the algorithm itself, and therefore this algorithm could be applied to any "game," under certain constraints of the definition of "game." With a few parameter tweaks and a new game file that satisfies the requirements of the abstracted definition of the word "game," this same algorithm can be applied to any other game.

The definition of what a suitable "game" would be consists of mainly three parts:
1. There exists a game state, that describes all information available to either player at any given point in time.
2. The game is a symmetric-information game (i.e. NOT poker, the information in game state is available to both players at any given point in time).
3. There is a win condition in which terminates the game.

Mostly, this project is for me to further understand this algorithm so it can be applied to more concrete areas. The only bridge needed is to define these concrete areas in such a way where they are a "game."

The model.py function was largely inspired by a similar project made by Applied Data Science Partners, as this was my first time dealing with Convolutional Neural Networks. I attempted to "make the code my own," but much of the construction of this file is the same. No copy pasting was done, each line was written individually and understood to an extent before moving on to the next line of code. Credit for most of this file definitely goes to David Foster at Applied Data Science Partners.

The loss function used in this project is a "two part" loss function, one of which is mostly self constructed. The first part of the loss function is a basic MSE of the game state evaluated by the neural network and the outcome of the game itself. This MSE is added to the second part of the loss function, which is a "cross entropy with logits," or in math terms:

-pi \cdot log(p(s_t)), where:
Pi is the policy head/probability vector of the MCTS.
P(s_t) is the policy head/probability vector of the neural net.

Other files were inspired by this algorithm's setup, but mostly written on my own. Other sources for this project include:

https://web.stanford.edu/~surag/posts/alphazero.html
https://ai-boson.github.io/mcts/
https://medium.com/applied-data-science/how-to-build-your-own-alphazero-ai-using-python-and-keras-7f664945c188

Of course, credit for Alpha Zero itself stems from Google's project which is described in the PDF below (also used as a resource):

https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ

Some research went into this project, and a few of the files (listed below) were taken from a Github Repo:

https://github.com/AppliedDataSciencePartners/DeepReinforcementLearning

The files taken were:
log.py, logsetup.py, (some of) model.py

