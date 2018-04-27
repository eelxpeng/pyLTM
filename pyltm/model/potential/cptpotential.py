'''
Conditional Probability Table Potential for discrete belief node
Created on 11 Feb 2018

@author: Bryan
'''
from .potential import Potential
from ..parameter import CPTParameter
from ..variable import Variable
from sortedcontainers import SortedSet
import numpy as np

class CPTPotential(Potential):
    '''
    classdocs
    '''
    def __init__(self, variables, parameter=None):
        '''
        variables: a single Variable, or a list of Variable
        parameter: CPTParameter or None
        '''
        super().__init__()
        if isinstance(variables, Variable):
            variables = [variables]
        self._variables = list(variables)    # save the variables involved
        if parameter is None:
            # initialize the table to uniform
            self._parameter = CPTParameter([v.getCardinality() for v in variables])
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
        """
        copy _variables and _parameter
        But does not copy the variable in the _variables. Keep the same reference
        """
        variables = list(self._variables)
        parameters = self._parameter.clone()
        return CPTPotential(variables, parameters)
    
    def function(self):
        return self
    
    def marginalize(self, variable):
        raise Exception("method not implemented.")
    
    def normalize(self, constant=None):
        return self._parameter.normalize(constant)
    
    def getDimension(self):
        return len(self._variables)
        
    def times(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.parameter.times(other)
        
        other = other.function()
        fDim = self.getDimension()
        gDim = other.getDimension()
        if fDim==0:
            result = other.clone()
            result.times(self.parameter.prob[0])
            return result
        elif gDim == 0:
            result = self.clone()
            result.times(other.parameter.prob[0])
            return result
        
        # union of variables in this and other
        var_prod = list(SortedSet(self.variables).union(other.variables))
        
        def getPermAxes(variables, subVars):
            index = list(range(len(variables)))
            transformAxes = []
            reverseAxes = [0]*len(variables)
            for i in range(len(subVars)):
                j = variables.index(subVars[i])
                transformAxes.append(j)
                index.remove(j)
                reverseAxes[j] = i
            for i in index:
                transformAxes.append(i)
                reverseAxes[i] = len(transformAxes)-1
            return transformAxes, reverseAxes
        
        ftransformAxes, freverseAxes = getPermAxes(var_prod, self.variables)
        gtransformAxes, greverseAxes = getPermAxes(var_prod, other.variables)
        newcpt = CPTPotential(var_prod)
        # utilize the broadcast of numpy array
        diff_axes = len(var_prod) - len(self.variables)
        arr = self.parameter.prob
        for i in range(diff_axes):
            arr = np.expand_dims(arr, axis=-1)
        fcpt = np.transpose(newcpt.parameter.prob.copy(), ftransformAxes)
        fcpt[:] = arr
        fcpt = np.transpose(fcpt, freverseAxes)
        
        diff_axes = len(var_prod) - len(other.variables)
        arr = other.parameter.prob
        for i in range(diff_axes):
            arr = np.expand_dims(arr, axis=-1)
        gcpt = np.transpose(newcpt.parameter.prob.copy(), gtransformAxes)
        gcpt[:] = arr
        gcpt = np.transpose(gcpt, greverseAxes)
        
        prod = fcpt*gcpt
        newcpt.parameter.prob[:] = prod
        
        return newcpt
    
    def sumOut(self, variable):
        '''
        return CPTPotential with the specified variable summed out
        '''
        variableIndex = self._variables.index(variable)
        summedArray = np.sum(self._parameter.prob, axis=variableIndex)
        resultVariables = list(self._variables).pop(variableIndex)
        cpt = CPTPotential(resultVariables)
        cpt._parameter.prob = summedArray
        return cpt
    
    def divide(self, other):
        '''in place divide'''
        if isinstance(other, float) or isinstance(other, int):
            self._parameter.prob[:] = self._parameter.prob / other
        else:
            self._parameter.prob[:] = self._parameter.prob / other._parameter.prob
    
    @property
    def parameter(self):
        return self._parameter
        
    @property
    def variables(self):
        return self._variables
            
    
    def __str__(self):
        toStr = "CPTPotential {\n"
        toStr += "\tdimension = " + str(len(self._variables)) + ";\n"
        toStr += "\tvariables = { " + " ".join([v.name for v in self._variables]) + "};\n"
        toStr += "\tcells = [\n" + str(self._parameter) + "\t];\n"
        toStr += "}"
        return toStr
        