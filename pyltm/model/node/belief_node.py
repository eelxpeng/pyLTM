'''
Created on 11 Feb 2018

@author: Bryan
'''
from abc import ABCMeta, abstractmethod, abstractproperty
from ...graph import DirectedNode
from ..variable import DiscreteVariable

class BeliefNode(DirectedNode):
    '''
    classdocs
    '''

    def __init__(self, graph, variable):
        '''
        Constructor
        '''
        super().__init__(graph, variable.name)
        self._potential = None
        self._variable = variable
        
    @property
    def potential(self):
        return self._potential
    
    @property
    def variable(self):
        return self._variable
    
    def setPotential(self, potential):
        self._potential = potential
        self._graph.expireLoglikelihoods()
    
    def attachInEdge(self, edge):
        super().attachInEdge(edge)
        # create new CPT to include the parent variable
        parent = edge.tail.variable
        self.setPotential(self._potential.addParentVariable(parent))
        
    def detachInEdge(self, edge):
        super().detachInEdge(edge)
        # create new CPT to exclude the parent variable
        oldparent = edge.tail.variable
        self.setPotential(self.potential.removeParentVariable(oldparent))
        
    @abstractmethod
    def computeDimension(self):
        pass
    
    def setName(self, name):
        super().setName(name)
        self.variable.setName(name)
    
    def expireNetworkLogLikelihoods(self):
        self._graph.expireLoglikelihoods()
        
    def getDiscreteParentVariables(self):
        parents = []
        for v in self._parents:
            if isinstance(v.variable, DiscreteVariable):
                parents.append(v)
        return parents
        
    def __str__(self):
        toStr = ""
        parents = self.getDiscreteParentVariables()
        if len(parents)==0:
            toStr += ("P(%s) {\n" % (self.variable.name))
        else:
            toStr += ("P(%s| %s) {\n" % (self.variable.name, ",".join([v.name for v in parents])))
        if self.potential is not None:
            toStr += str(self.potential)
            toStr += "\n"
        else:
            toStr += "potential: None\n"
        toStr += "}\n"
            
        return toStr
        