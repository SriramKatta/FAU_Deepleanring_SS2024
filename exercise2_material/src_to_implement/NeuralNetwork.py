from Layers import *
from Optimization import *
import copy

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

  def forward(self):
    input_tensor, self.label_tensor = self.data_layer.next()
    for layer in self.layers:
      input_tensor = layer.forward(input_tensor)
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
