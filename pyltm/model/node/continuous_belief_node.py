'''
Created on 11 Feb 2018

@author: Bryan
'''
from .belief_node import BeliefNode
from ..variable import DiscreteVariable
from ..variable import JointContinuousVariable
from ..potential import CGPotential

class ContinuousBeliefNode(BeliefNode):
    '''
    classdocs
    '''

    def __init__(self, graph, variable):
        '''
        Constructor
        '''
        if isinstance(variable, list):
            variable = JointContinuousVariable(variable)
        if not isinstance(variable, JointContinuousVariable):
            raise ValueError("ContinuousBeliefNode should take JointContinuousVariable")
        super().__init__(graph, variable)
        self._variable = variable
        self._potential = CGPotential(variable, None)
        
    def computeDimension(self):
        numberOfVariable = len(self._variable.variables())
        dimensionPerConfig = numberOfVariable * (numberOfVariable + 3) / 2
        return dimensionPerConfig * self.getCardinalities(self.getDiscreteParentVariables())
    
    
        