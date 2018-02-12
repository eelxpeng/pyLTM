'''
Conditional Probability Table Potential for discrete belief node
Implemented using numpy
May be extended to Tensor computation on GPU.
Created on 11 Feb 2018

@author: Bryan
'''
from .potential import Potential
import numpy as np

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
            self._parameter = np.ones(variable.getCardinality())*1./variable.getCardinality()
        else:
            self._parameter = parameter
        
    def addParentVariable(self, variable):
        return self.addVariable(variable)
        
    def addVariable(self, variable):
        assert not self.contains(variable.name)
        cardinality = variable.getCardinality()
        self._variables.append(variable)
        self._parameter = self._parameter[..., np.newaxis]
        self._parameter = np.repeat(self._parameter, cardinality, axis=-1)
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
            swapped_array = np.swapaxes(self._parameter, 0, variableIndex)
            swapped_array = swapped_array[[state], ...]
            back = np.swapaxes(swapped_array, 0, variableIndex)
            self._parameter = np.squeeze(back, axis=variableIndex)
        return self
        
    def contains(self, name):
        return name in [v.name for v in self._variables]
    
    def setCell(self, variables, states, cell):
        """
        variables no need to be in order
        """
        indexes = [variables.index(v) for v in self._variables]
        states = states[indexes]
        ref = self._variables
        for state in states[:-1]:
            ref = ref[state]
        ref[states[-1]] = cell
        
    def setCells(self, variables, cells):
        """
        variables: list of variable
        cells: numpy array
        """
        indexes = [variables.index(v) for v in self._variables]
        cells = np.transpose(cells, axes=indexes)
        self._parameter[:] = cells

    def clone(self):
        pass
    
    def function(self):
        pass
    
    def marginalize(self, variable):
        pass
    
    def normalize(self, constant):
        pass
    
    def __str__(self):
        toStr = "CPTPotential {\n"
        toStr += "\tdimension = " + str(len(self._variables)) + ";\n"
        toStr += "\tvariables = { " + " ".join([v.name for v in self._variables]) + "};\n"
        toStr += "\tcells = [\n" + str(self._parameter) + "\t];\n"
        toStr += "}"
        return toStr
        