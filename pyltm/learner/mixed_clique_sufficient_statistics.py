'''
Created on 12 Sep 2018

@author: Bryan
'''
from .sufficient_statistics import SufficientStatistics
from pyltm.model.potential.cgpotential import CGPotential
from pyltm.model import JointContinuousVariable, CGParameter
import collections
import numpy as np
from pyltm.model.parameter import cgparameter
from pyltm.model.variable.discrete_variable import DiscreteVariable
from pyltm.model.parameter.cptparameter import CPTParameter

class MixedCliqueSufficientStatistics(SufficientStatistics):
    '''
    classdocs
    '''


    def __init__(self, node, batch_size):
        '''
        Constructor
        '''
        jointVariables = node.jointVariable
        discreteVariable = node.discreteVariable
        if isinstance(jointVariables, JointContinuousVariable):
            jointVariables = list(jointVariables.variables)
        elif isinstance(jointVariables, collections.Iterable):
            jointVariables = list(jointVariables)
        assert isinstance(jointVariables, list)
        self._continuousVariables = jointVariables
        self._discreteVariable = discreteVariable
        
        self.resetParameters(node.potential, batch_size)
        
    def resetParameters(self, cgpotential, batch_size):
        cardinality = 1 if self._discreteVariable is None else self._discreteVariable.getCardinality()
        self.statistics = [None]*cardinality
        for i in range(cardinality):
            self.statistics[i] = cgpotential.get(i).clone()
        self.normalize()
        for i in range(cardinality):
            # sufficient counts
            self.statistics[i].p = self.statistics[i].p * batch_size
            # sufficient sum_square
            self.statistics[i].covar[:] = (self.statistics[i].covar + np.outer(self.statistics[i].mu, self.statistics[i].mu)
                                           ) * self.statistics[i].p
            # sufficient sum 
            self.statistics[i].mu[:] = self.statistics[i].mu * self.statistics[i].p
            
        
    def normalize(self, constant=None):
        if constant is None:
            constant = np.sum([x.p for x in self.statistics])
        for i in range(len(self.statistics)):
            self.statistics[i].p /= constant
        return constant
    
    def reset(self):
        for stat in self.statistics:
            stat.p = 0
            stat.mu[:] = 0
            stat.covar[:] = 0
        
    def add(self, potential):
        for i in range(potential.size):
            weight = potential.get(i).p
            self.statistics[i].p += weight
            self.statistics[i].mu[:] += potential.get(i).mu * weight
            self.statistics[i].covar[:] += np.outer(potential.get(i).mu, potential.get(i).mu) * weight 
            
    def update(self, batchStatistics, learning_rate):
        assert(len(self.statistics)==len(batchStatistics.statistics))
        for i in range(len(self.statistics)):
            self.statistics[i].p = self.statistics[i].p + learning_rate * (batchStatistics.statistics[i].p - self.statistics[i].p)
            self.statistics[i].mu = self.statistics[i].mu + learning_rate * (batchStatistics.statistics[i].mu - self.statistics[i].mu)
            self.statistics[i].covar = self.statistics[i].covar + learning_rate * (batchStatistics.statistics[i].covar - self.statistics[i].covar)
        
    def computePotential(self, variable):
        if isinstance(variable, JointContinuousVariable):
            parameters = [None]*len(self.statistics)
            for i in range(len(self.statistics)):
                parameters[i] = CGParameter(1, len(self.statistics[i].mu), self.computeMean(self.statistics[i]), self.computeCovariance(self.statistics[i]))
            return parameters
        elif isinstance(variable, DiscreteVariable):
            # only possibility is that variable is root
            parameter = CPTParameter(len(self.statistics))
            for i in range(len(self.statistics)):
                parameter.prob[i] = self.statistics[i].p
            parameter.normalize()
            return parameter
                
    def computeMean(self, cgparameter):
        if cgparameter.p == 0:
            return np.zeros_like(cgparameter.mu)
        return cgparameter.mu / cgparameter.p
                
    def computeCovariance(self, cgparameter):
        if cgparameter.p==0:
            return np.ones_like(cgparameter.covar)
        mu = self.computeMean(cgparameter)
        return cgparameter.covar / cgparameter.p - np.outer(mu, mu)