'''
Created on 12 Sep 2018

@author: Bryan
'''
from .sufficient_statistics import SufficientStatistics
from pyltm.model import CPTPotential

class DiscreteCliqueSufficientStatistics(SufficientStatistics):
    '''
    classdocs
    '''


    def __init__(self, node, batch_size):
        '''
        Constructor
        '''
        self.statistics = node.potential.clone()
        self.statistics.parameter.prob[:] = self.statistics.parameter.prob * batch_size 
        
    def reset(self):
        self.statistics.parameter.prob[:] = 0
        
    def add(self, potential, weight):
        self.statistics.parameter.prob[:] += potential.parameter.prob * weight
        
    def update(self, cptpotential, learning_rate):
        self.statistics.parameter.prob[:] = self.statistics.parameter.prob + learning_rate * (
            cptpotential.parameter.prob - self.statistics.parameter.prob)
        
    def computePotential(self, variable):
        self.statistics.normalizeOver(variable)
        return self.statistics.parameter