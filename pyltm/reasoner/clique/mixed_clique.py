'''
Created on 12 Feb 2018

@author: Bryan
'''
from .clique import Clique
from ..clique_potential import CliquePotential
from ..message import Message
from pyltm.model.potential.cgpotential import CGPotential

class MixedClique(Clique):
    '''
    classdocs
    '''


    def __init__(self, tree, name, jointVar, discreteVar):
        '''
        Constructor
        '''
        super().__init__(tree, name)
        self._jointVariable = jointVar
        self._discreteVariable = discreteVar
        
    @property
    def discreteVariable(self):
        return self._discreteVariable
    @property
    def jointVariable(self):
        return self._jointVariable
    
    def potential(self):
        return self._potential.content if self._potential is not None else None
    
    def logNormalization(self):
        return self._potential.logNormalization
    
    def addLogNormalization(self, logNormalization):
        self._potential.logNormalization += logNormalization
        return self._potential.logNormalization
    
    def contains(self, variable):
        return self._discreteVariable is variable or self._jointVariable is variable or \
            variable in self._jointVariable.variables
            
    def assign(self, potential):
        """
        potential: CGPotential
        """
        self._potential = CliquePotential(potential)
        
    def absorbEvidence(self, variable, value):
        self._potential.logNormalization += self._potential.content.absorbEvidence(variable, value)
        
    def computeMessage(self, separator, multiplier=None, retainingVariables=None):
        """
        Should only contain discrete variable of the separator
        Always retain the discrete variable and marginalize out continuous
        """
        cptpotential = self._potential.content.marginalize(separator.variable)
        message = Message(cptpotential, self._potential.logNormalization)
        return message.times(multiplier) if multiplier is not None else message
    
    def reset(self):
        self._potential = None
        
    def combine(self, other, logNormalization):
        """
        other: Potential
        """
        if isinstance(other, CGPotential):
            if self._potential is None:
                self._potential = CliquePotential(other.clone(), logNormalization())
            else:
                self._potential.content.combine(other)
                self._potential.logNormalization += logNormalization
        else:
            # other is CPTPotential
            if self._potential is None:
                cgpotential = CGPotential(self._jointVariable, self._discreteVariable)
                self._potential = CliquePotential(cgpotential, logNormalization)
                
            self._potential.content.multiply(other)
            self._potential.logNormalization += logNormalization
                
        if self.pivot:
            self.normalize()
        
    def variables(self):
        variables = self._jointVariable.variables() + [self._discreteVariable]
        return variables
        
    def __str__(self):
        toStr = "" + self.__class__.__name__() + ": " 
        toStr += " ".join([v.name for v in self._jointVariables])
        toStr += " ".join([v.name for v in self._discreteVariable])
        toStr += "neighbors={ " + " ".join([n.name for n in self.getNeighbors()]) + " }\n"
        
        if self.potential is not None:
            toStr += str(self.potential)
            toStr += "\n"
        else:
            toStr += "potential: None\n"
        toStr += "}\n"
            
        return toStr