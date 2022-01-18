import log as lg
import numpy as np
import config
from keras import regularizers

from keras.models import load_model, Model, Sequential
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add
from tensorflow.keras.optimizers import SGD
import tensorflow as tf

#may need to change the below
from loss import softmax_cross_entropy_with_logits

#note this model seems to rely on softmax cross entropy loss function. After minimial
#research on this loss function, I am not sure if this is the loss function that is described in
#https://web.stanford.edu/~surag/posts/alphazero.html
#as this loss function has a difference between a current game state and the otucome of the game added to what I believe to be is a cross entropy loss function (the second term is softmax cross entropy but not the first? Check back up on this.

#using the softmax cross entropy function is originally done because of the repo 
#https://github.com/AppliedDataSciencePartners/DeepReinforcementLearning,
#in which in his model construction he uses softmax cross entropy

#add some logging functions to this model.
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
        self.model.save(config.run_folder + '/models/version' + '{0}'.format(version) + '.h5')
       
    #DIRECTLY FROM LOSS FILE. MAY NEED TO REWRITE IN THE FUTURE.
    def read(self, game, version):
        return load_model(config.run_folder + '/models/version' + '{0}'.format(version) + '.h5', custom_objects = {'softmax_cross_entropy_with_logits':softmax_cross_entropy_with_logits})
                          
                        
    #he uses some logging functions which i will not write myself until I understand them (and will make them useful for me in particular.
                        
                        
class ResidualCNN(GeneralModel):
    def __init__(self, regConstant, stepSize, inDim, outDim, hiddenLayers):
        GeneralModel.__init__(self, regConstant, stepSize, inDim, outDim)
        self.hiddenLayers = hiddenLayers
        self.numHiddenLayers = len(hiddenLayers)
        self.model = self.buildModel()
    
    def buildModel(self):
        modelInput = Input(shape = self.inDim, name = 'modelInput')
        
        x = self.convLayer(modelInput, self.hiddenLayers[0]['filters'], self.hiddenLayers[0]['kernelSize'])
                           
        if (self.numHiddenLayers > 1):
            for l in self.hiddenLayers[1:]:
                x = self.hiddenLayer(x, l['filters'], l['kernelSize'])
                     
        valueHead = self.valueHead(x)
                           
        policyHead = self.policyHead(x)
        
        model = Model(inputs=[modelInput], outputs = [valueHead, policyHead])
                   
        #ALSO COMPLETELY FROM THE LOSS FILE.
        model.compile(loss = {'valueHead': 'mean_squared_error', 'policyHead': softmax_cross_entropy_with_logits},
                     optimizer = SGD(lr = self.stepSize, momentum = config.MOMENTUM),
                      loss_weights = {'valueHead': 0.5, 'policyHead': 0.5})
        
        return model
                           
    def convLayer(self, x, filters, kernelSize):
        data_format = ''
        if tf.test.is_built_with_cuda():
            data_format = 'channels_first'
        else:
            data_format = 'channels_last'
        x = Conv2D(
            filters = filters
            , kernel_size = kernelSize
            , data_format = data_format
            , padding = 'same'
            , use_bias = False
            , activation='linear'
            , kernel_regularizer = regularizers.l2(self.regConstant)
        ) (x)
        
        #unsure what these are for. seems to function to make the gradient smaller to increase efficiency in SGD? But at this point the loss function hasn't even been specified, so not certain. Could be setting the NN up specifically for this loss function?
        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)
                          
        return (x)
              
    #the only difference here is adding the input block and x to the layer. Not sure why this is needed as a different function from the outer convolutional layers, but will attempt to understand.
    #my intuition: this add function is there in order to KEEP TRACK of the development of the neural network itself, as given some LAST block, record the new one in order to debug later to see the relationship. Not sure if this actually serves any real functionality to the project itself though (other than debugging)
    def hiddenLayer(self, modelInput, filters, kernelSize):
        x = self.convLayer(modelInput, filters, kernelSize)
        data_format = ''
        if tf.test.is_built_with_cuda():
            data_format = 'channels_first'
        else:
            data_format = 'channels_last'
        x = Conv2D(
            filters = filters
            , kernel_size = kernelSize
            , data_format = data_format
            , padding = 'same'
            , use_bias = False
            , activation = 'linear'
            , kernel_regularizer = regularizers.l2(self.regConstant)
        )(x)
                           
        x = BatchNormalization(axis = 1)(x)
                           
        x = add([modelInput, x])
                           
        x = LeakyReLU()(x)
                           
        return (x)
                           
         #only difference between this first convolutional layer and the one constructed
    #in the conv_layer function is the KERNEL SIZE. This must have to do with the size
    #of the output. Note that the expected value of a move is simply a single value, thus it makes sense for the kernrel to be a 1 by 1 matrix. 
                           
    #this method is taken straight from Applied Data Science Partners.
    def valueHead(self, x):
        data_format = ''
        if tf.test.is_built_with_cuda():
            data_format = 'channels_first'
        else:
            data_format = 'channels_last'
        x = Conv2D(
            filters = 1
            , kernel_size = (1, 1)
            , data_format = data_format
            , padding = 'same'
            , use_bias = False
            , activation = 'linear'
            , kernel_regularizer = regularizers.l2(self.regConstant)
        )(x)
                           
        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)
                           
        x = Flatten()(x)
                           
        x = Dense(
            20
            , use_bias=False
            , activation='linear'
            , kernel_regularizer=regularizers.l2(self.regConstant)
            )(x)

        x = LeakyReLU()(x)

        x = Dense(
            1
            , use_bias=False
            , activation='tanh'
            , kernel_regularizer=regularizers.l2(self.regConstant)
            , name = 'value_head'
            )(x)
                           
        return (x)
       
    #this method is taken straight from Applied Data Science Partners.
    def policyHead(self, x):
        data_format = ''
        if tf.test.is_built_with_cuda():
            data_format = 'channels_first'
        else:
            data_format = 'channels_last'
        x = Conv2D(
        filters = 2
        , kernel_size = (1,1)
        , data_format=data_format
        , padding = 'same'
        , use_bias=False
        , activation='linear'
        , kernel_regularizer = regularizers.l2(self.regConstant)
        )(x)

        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)

        x = Flatten()(x)

        x = Dense(
            self.outDim
            , use_bias=False
            , activation='linear'
            , kernel_regularizer=regularizers.l2(self.regConstant)
            , name = 'policy_head'
            )(x)

        return (x)
                           
                           
    def makeValidModelInput(self, state):
        modelInput = state.binary
        modelInput = np.reshape(modelInput, self.inDim)
        return (modelInput)
                          
                           