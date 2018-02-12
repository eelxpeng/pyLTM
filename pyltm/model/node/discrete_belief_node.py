'''
Created on 11 Feb 2018

@author: Bryan
'''
from .belief_node import BeliefNode
from ..potential import CPTPotential
from ..variable import DiscreteVariable

class DiscreteBeliefNode(BeliefNode):
    '''
    classdocs
    '''
    def __init__(self, graph, variable):
        '''
        Constructor
        '''
        super().__init__(graph, variable)
        self._potential = CPTPotential(variable)
        
    def computeDimension(self):
        dimension = self._variable.getCardinality()-1
        dimension *= self.getCardinalities(self.getDiscreteParentVariables())
        return dimension
    
    def getDiscreteParentVariables(self):
        parentList = list()
        for parent in self._parents:
            if isinstance(parent, DiscreteBeliefNode):
                parentList.append(parent.variable)
        return parentList
    
    
    
    