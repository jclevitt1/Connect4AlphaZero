#this file was taken from the github repository:
#https://github.com/AppliedDataSciencePartners/DeepReinforcementLearning

#### SELF PLAY

EPISODES = 30
MCTS_SIMS = 20
MEMORY_SIZE = 30000
TURNS_TILL_DETERM = 10 # turn on which it starts playing deterministically
CPUCT = 1
#epsilon alpha.... not sure what these parameters are for?
EPSILON = 0.2
ALPHA = 0.8


#### RETRAINING
BATCH_SIZE = 256
EPOCHS = 1
REG_CONST = 0.0001
LEARNING_RATE = 0.1
MOMENTUM = 0.9
TRAINING_LOOPS = 10

HIDDEN_CNN_LAYERS = [
    {'filters':75, 'kernelSize': (4,4)}
     , {'filters':75, 'kernelSize': (4,4)}
     , {'filters':75, 'kernelSize': (4,4)}
     , {'filters':75, 'kernelSize': (4,4)}
     , {'filters':75, 'kernelSize': (4,4)}
     , {'filters':75, 'kernelSize': (4,4)}
    ]

#### EVALUATION
EVAL_EPISODES = 20
SCORING_THRESHOLD = 1.3


run_folder = './run/'
run_archive_folder = './run_archive/'