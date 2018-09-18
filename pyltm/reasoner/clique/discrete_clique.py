'''
Created on 12 Feb 2018

@author: Bryan
'''
from .clique import Clique
from ..message import Message
from pyltm.reasoner.clique_potential.clique_potential import CliquePotential

class DiscreteClique(Clique):
    '''
    classdocs
    '''


    def __init__(self, tree, name, variables):
        '''
        variables: list of Variable
        '''
        super().__init__(tree, name)
        self._variables = list(variables)
        
    @property
    def variables(self):
        return self._variables
    @property
    def discreteVariables(self):
        return self._variables
    @property
    def potential(self):
        return self._potential.content if self._potential is not None else None
    
    def logNormalization(self):
        return self._potential.logNormalization
    
    def addLogNormalization(self, logNormalization):
        self._potential.logNormalization += logNormalization
        
    def contains(self, variable):
        return variable in self._variables
    
    def computeMessage(self, separator, multiplier=None, retainingVariables=None):
        """
        multiplier: Message from upstream
        """
        cptpotential = self._potential.content if multiplier is None else self._potential.content.times(multiplier.cptpotential)
        for variable in self._potential.content.variables:
            if variable is separator.variable:
                continue
            if retainingVariables is not None and variable in retainingVariables:
                continue
            cptpotential = cptpotential.sumOut(variable)
        constant = self.logNormalization() if multiplier is None else self.logNormalization()+multiplier.logNormalization()
        return Message(cptpotential, constant)
        
    def reset(self):
        self._potential = None
    
    def combine(self, other, logNormalization=0):
        """
        other: Potential
        """
        if isinstance(other, Message):
            self.combine(other.function(), other.logNormalization)
            return
        if self._potential is None:
            cptpotential = other.clone()
            self._potential = CliquePotential(cptpotential, logNormalization)
        else:
            other = other.function()
            newcpt = self._potential.content.times(other)
            self._potential = CliquePotential(newcpt, self.logNormalization()+logNormalization)
            
        if self.pivot:
            self.normalize()
             
            