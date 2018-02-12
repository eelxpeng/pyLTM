'''
Conditional Probability Table Potential for discrete belief node
Created on 11 Feb 2018

@author: Bryan
'''
from .potential import Potential
from ..parameter import CPTParameter

class CPTPotential(Potential):
    '''
    classdocs
    '''
    def __init__(self, variable, parameter=None):
        '''
        Constructor
        '''
        super().__init__()
        self._variables = list()    # save the variables involved
        self._variables.append(variable)
        if parameter is None:
            # initialize the table to uniform
            self._parameter = CPTParameter(variable.getCardinality())
        else:
            self._parameter = parameter
        
    def addParentVariable(self, variable):
        return self.addVariable(variable)
        
    def addVariable(self, variable):
        """
        Not normalizing.
        Let f and g be this function and the new function to be created, 
        respectively. Also, let X and Y be the variables involved in f and the
        new variable to be involved in g, respectively. We will set the cells of
        g such that g(X, y) = f(X)
        """
        assert not self.contains(variable.name)
        cardinality = variable.getCardinality()
        self._variables.append(variable)
        self._parameter.expand_dim(-1, cardinality)
        return self
    
    def removeParentVariable(self, variable):
        return self.project(variable, 0)
        
    def project(self, variable, state):
        """
        Inplace project variable to a state
        """
        if isinstance(variable, list) and isinstance(state, list):
            assert len(variable)==len(state)
            for i in range(len(variable)):
                self.project(variable[i], state[i])
        else:
            variableIndex = self._variables.index(variable)
            self._variables.pop(variableIndex)
            assert variableIndex>=0
            self._parameter.reduce_dim(variableIndex, state)
        return self
        
    def contains(self, name):
        return name in [v.name for v in self._variables]
    
    def setCell(self, variables, states, cell):
        """
        variables no need to be in order
        """
        indexes = [variables.index(v) for v in self._variables]
        states = states[indexes]
        self._parameter.set_value(states, cell)
        
    def setCells(self, variables, cells):
        """
        variables: list of variable
        cells: numpy array
        """
        indexes = [variables.index(v) for v in self._variables]
        self._parameter.set(cells, axes=indexes)

    def clone(self):
        pass
    
    def function(self):
        pass
    
    def marginalize(self, variable):
        pass
    
    def normalize(self, constant=None):
        return self._parameter.normalize(constant)
            
    
    def __str__(self):
        toStr = "CPTPotential {\n"
        toStr += "\tdimension = " + str(len(self._variables)) + ";\n"
        toStr += "\tvariables = { " + " ".join([v.name for v in self._variables]) + "};\n"
        toStr += "\tcells = [\n" + str(self._parameter) + "\t];\n"
        toStr += "}"
        return toStr
        