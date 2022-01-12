import log as lg
import numpy as np
import config

from keras.models import load_model, Model, Sequential
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add

#may need to change the below
from loss import softmax_cross_entropy_with_logits

#note this model seems to rely on softmax cross entropy loss function. After minimial
#research on this loss function, I am not sure if this is the loss function that is described in
#https://web.stanford.edu/~surag/posts/alphazero.html
#as this loss function has a difference between a current game state and the otucome of the game added to what I believe to be is a cross entropy loss function (the second term is softmax cross entropy but not the first? Check back up on this.

#using the softmax cross entropy function is originally done because of the repo 
#https://github.com/AppliedDataSciencePartners/DeepReinforcementLearning,
#in which in his model construction he uses softmax cross entropy

class GeneralModel():
    def __init__(self, regConstant, stepSize, inDim, outDim):
        self.regConstant = regConstant
        self.stepSize = stepSize
        self.inDim = inDim
        self.outDim = outDim
        
    #must be called once self.model is instantitated
    def predict(self, modelIn):
        return self.model.predict(modelIn)
    
    def fit(self, stateList, targets, epochs, verbose, validationSplit, batchSize):
        return self.model.fit(stateList, targets, epochs = epochs, verbose=verbose, validation_split = validationSplit, batch_size = batchSize)
    
    #saves the current model in a file
    def write(self, game, version):
        self.model.save(config.run_folder + '/models/version' + '{0}'.format(version) + '.h5'
        return
       
    #DIRECTLY FROM LOSS FILE. MAY NEED TO REWRITE IN THE FUTURE.
    def read(self, game, version):
        return load_model(config.run_folder + '/models/version' + '{0}'.format(version) + '.h5', custom_objects = {'softmax_cross_entropy_with_logits':softmax_cross_entropy_with_logits})
                          
                        
    #he uses some logging functions which i will not write myself until I understand them (and will make them useful for me in particular.
                        
                        
class ResidualCnn(GeneralModel):
    def __init__(self, regConstant, stepSize, inDim, outDim, hiddenLayers):
        GeneralModel.__init__(self, regConstant, stepSize, inDim, outDim)
        self.hiddenLayers = hiddenLayers
        self.numHiddenLayers = len(hiddenLayers)
        self.model = self.buildModel()
    
    def buildModel(self):
        modelInput = Input(shape = self.inDim, name = 'modelInput')
        
        x = self.convLayer(modelInput, self.hiddenLayers[0]['filters'], self.hiddenLayers[0]['kernelSize']
                           
        if len(self.hiddenLayers > 1):
            for l in self.hiddenLayers[1:]:
                x = self.hiddenLayer(x, h['filters'], h['kernelSize'])
                     
        valueHead = self.valueHead(x)
                           
        policyHead = self.policyHead(x)
        
        model = Model(inputs=[modelInput], outputs = [valueHead, policyHead])
                   
        #ALSO COMPLETELY FROM THE LOSS FILE.
        model.compile(loss = {'valueHead': 'mean_squared_error', 'policyHead': softmax_cross_entropy_with_logits},
                     optimizer = SGD(lr = self.stepSize, momentum = config.MOMENTUM),
                      loss_weights = {'valueHead': 0.5, 'policyHead': 0.5})
        
        return model
                           
    def convLayer(self, x, filters, kernelSize):
        x = Conv2D(
            filters = filters
            , kernel_size = kernelSize
            , data_format = 'channels_first'
            , padding = 'same'
            , use_bias = False,
            , activation = 'linear'
            , kernel_regularizer = regularizers.12(self.regConstant)
        ) (x)
        
        #unsure what these are for. seems to function to make the gradient smaller to increase efficiency in SGD? But at this point the loss function hasn't even been specified, so not certain. Could be setting the NN up specifically for this loss function?
        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)
                          
        return (x)
              
    #the only difference here is adding the input block and x to the layer. Not sure why this is needed as a different function from the outer convolutional layers, but will attempt to understand.
    #my intuition: this add function is there in order to KEEP TRACK of the development of the neural network itself, as given some LAST block, record the new one in order to debug later to see the relationship. Not sure if this actually serves any real functionality to the project itself though (other than debugging)
    def hiddenLayer(self, modelInput, filters, kernelSize):
        x = self.convLayer(modelInput, filters, kernelSize)
        
        x = Conv2D(
            filters = filters
            , kernel_size = kernelSize
            , data_format = 'channels_first'
            , padding = 'same'
            , use_bias = False
            , activation = 'linear'
            , kernel_regularizer = regularizers.12(self.regConstant)
        )(x)
                           
        x = BatchNormalization(axis = 1)(x)
                           
        x = add([modelInput, x])
                           
        x = LeakyReLU()(x)
                           
        return (x)
                           
                           
    def valueHead(self, x):
        return 0
                           
    def policyHead(self, x):
        return 0
                          
                           