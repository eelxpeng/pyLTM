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
    NAME_PREFIX = "BayesNet"
    
    def __init__(self, name=None):
        '''
        Constructor
        '''
        super().__init__()
        if name is None:
            name = BayesNet.createDefaultName()
        self._name = name
        self._variables = dict()    # dict variable : beliefNode
        self._loglikelihood = dict()
        BayesNet._count += 1
        
    @staticmethod
    def createDefaultName():
        return BayesNet.NAME_PREFIX + str(BayesNet._count)
    
    @classmethod
    def createFromOther(cls, other):
        net = cls()
        # copy nodes
        for node in other.nodes:
            net.addNode(node.variable)
        # copy edges
        for edge in other.edges:
            net.addEdge(net.getNode(edge.head.name), net.getNode(edge.tail.name))
        # copy CPT
        for node in net.nodes:
            othernode = other.getNode(node.variable)
            node.setPotential(othernode.potential.clone())
        net._loglikelihood = dict(other._loglikelihood)
        return net
        
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
            raise ValueError("BayesNet addNode: only variable/node is allowed")
        return node
    
    def getNode(self, variable):
        return self._variables[variable]
    
    def __str__(self):
        toStr = "BayesNet " + self._name + " {\n"
        toStr += "number of nodes: " + str(self.getNumberOfNodes()) +"\n"
        toStr += "nodes = {\n"
        for node in self.nodes:
            toStr += str(node) + " "
        toStr += "}\n"
        toStr += "number of edges: " + str(self.getNumberOfEdges()) + "\n"
        toStr += "edges = {\n"
        for edge in self.edges:
            toStr += str(edge) + " "
        toStr += "\n}\n"
        toStr += "}\n"
        return toStr
        
        
        