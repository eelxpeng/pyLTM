'''
Created on 12 Sep 2018

@author: Bryan
'''
import numpy as np
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
        self._variables = node.potential._variables
        self.prob = node.potential.prob.copy() * batch_size
        
    def reset(self):
        self.prob[:] = 0
        
    def add(self, potential):
        self.prob[:] += np.sum(potential.prob, axis=0)
        
    def update(self, statistics, learning_rate):
        self.prob[:] = self.prob + learning_rate * (statistics.prob - self.prob)
        
    def computePotential(self, variable):
        cptpotential = CPTPotential(self._variables)
        cptpotential.parameter.prob[:] = self.prob
        cptpotential.normalizeOver(variable)
        return cptpotential.parameter