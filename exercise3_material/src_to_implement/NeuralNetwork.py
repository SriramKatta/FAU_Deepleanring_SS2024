from Layers import *
from Optimization import *
import copy
import pickle

class NeuralNetwork:
  def __init__(self,optimizer,weights_initializer, bias_initializer):
    self.optimizer = optimizer
    self.loss = []
    self.layers = []
    self.loss_layer = []
    self.weights_initializer = weights_initializer
    self.bias_initializer = bias_initializer
    self.data_layer = None
    self.label_tensor = None

  def __getstate__(self):
    state = self.__dict__.copy()
    del state['data_layer']
    return state
  
  def __setstate__(self,state):
    self.__dict__ = state

  def forward(self):
    input_tensor, self.label_tensor = self.data_layer.next()
    regloss = 0
    for layer in self.layers:
      input_tensor = layer.forward(input_tensor)
      if layer.trainable and layer.optimizer :
        if layer.optimizer.regularizer :
          regloss += layer.optimizer.regularizer.norm(layer.weights)
          
    return self.loss_layer.forward(input_tensor, self.label_tensor)

  def backward(self):
    error_tensor = self.loss_layer.backward(self.label_tensor)
    for layer in reversed(self.layers):
      error_tensor = layer.backward(error_tensor)

  
  def append_layer(self, layer):
    if(layer.trainable):
      layer.optimizer = copy.deepcopy(self.optimizer)
      layer.initialize(self.weights_initializer, self.bias_initializer)
    self.layers.append(layer)

  def train(self, iter):
    for _ in range(iter):
      self.loss.append(self.forward())
      self.backward()
    
  def test(self, input_tensor):
    for layer in self.layers:
      input_tensor = layer.forward(input_tensor)
    return input_tensor
  
  @property
  def phase(self):
    return self.layers[0].testing_phase
  
  @phase.setter
  def phase(self, newval):
    for layer in self.layers:
      layer.testing_phase = newval

def save(filename, net):
  pickle.dump(net, open(filename, 'wb'))

def load(filename, data_layer):
  net = pickle.load(open(filename))
  net.data_layer = data_layer
  return net
