'''
Created on 21 Jan 2018

@author: Bryan
'''
from ..graph import DirectedAcyclicGraph
from .variable import Variable, DiscreteVariable, JointContinuousVariable, SingularContinuousVariable
from .node import BeliefNode, DiscreteBeliefNode, ContinuousBeliefNode

class BayesNet(DirectedAcyclicGraph):
    '''
    classdocs
    '''
    _count = 0  # static variable: the number of BNs created
    
    def __init__(self, name):
        '''
        Constructor
        '''
        super().__init__()
        self._name = name
        self._variables = dict()    # dict variable : beliefNode
        self._loglikelihood = dict()
        BayesNet._count += 1
        
    def addEdge(self, head, tail):
        """
        Override addEdge to expire all loglikelihood
        """
        edge = super().addEdge(head, tail)
        self.expireLoglikelihoods()
        return edge
    
    def expireLoglikelihoods(self):
        if len(self._loglikelihood)!=0:
            self._loglikelihood.clear()
            
    def addNode(self, node):
        """
        Override addNode to only allow addNode through variable/node
        """
        if isinstance(node, Variable):
            variable = node
            if isinstance(variable, DiscreteVariable):
                node = DiscreteBeliefNode(self, variable)
            elif isinstance(variable, SingularContinuousVariable) or isinstance(variable, JointContinuousVariable):
                node = ContinuousBeliefNode(self, variable)
            else:
                raise ValueError("variable type error")
            self.addNode(node)
                
        elif isinstance(node, BeliefNode):
            assert not self.containsNode(node.name)
            self._nodes.append(node)
            self._names[node.name] = node
            self._variables[node.variable] = node
            self.expireLoglikelihoods()
        else:
            raise ValueError("BayesNet addNode: only variable is allowed")
        
        
        