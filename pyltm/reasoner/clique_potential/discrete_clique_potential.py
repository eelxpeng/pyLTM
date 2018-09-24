'''
Created on 18 Sep 2018

@author: Bryan
'''
import numpy as np
from sortedcontainers import SortedSet
from .clique_potential import CliquePotential
from pyltm.model import CPTPotential

class DiscreteCliquePotential(CliquePotential):
    '''
    classdocs
    '''


    def __init__(self, potential, constant=0):
        '''
        potential: cptpotential
        '''
        self._variables = potential._variables
        self.prob = potential.parameter.prob.copy()
        self.logNormalization = constant
        
    def isBatch(self):
        return len(self.prob.shape) == (len(self._variables)+1)
    
    def times(self, other):
        '''other: DiscreteCliquePotential
        return new DiscreteCliquePotential
        TODO: convert to batch operation'''
        if isinstance(other, float) or isinstance(other, int):
            result = self.clone()
            result.prob *= other
            return
        
        other = other.function()
        fDim = self.getDimension()
        gDim = other.getDimension()
        if fDim==0:
            result = other.clone()
            return result
        elif gDim == 0:
            result = self.clone()
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
        isbatch = self.isBatch() or other.isBatch()
        diff_axes = len(var_prod) - len(self.variables)
        arr = self.prob
        for i in range(diff_axes):
            arr = np.expand_dims(arr, axis=-1)
        fcpt = np.transpose(newcpt.parameter.prob.copy(), ftransformAxes)
        if isbatch and self.isBatch():
            batch_size = self.prob.shape[0]
            fcpt = np.repeat(np.expand_dims(fcpt, axis=0), batch_size, axis=0)
            freverseAxes = [0] + [x+1 for x in freverseAxes]
        fcpt[:] = arr
        fcpt = np.transpose(fcpt, freverseAxes)
        
        diff_axes = len(var_prod) - len(other.variables)
        arr = other.prob
        for i in range(diff_axes):
            arr = np.expand_dims(arr, axis=-1)
        gcpt = np.transpose(newcpt.parameter.prob.copy(), gtransformAxes)
        if isbatch and other.isBatch():
            batch_size = other.prob.shape[0]
            gcpt = np.repeat(np.expand_dims(gcpt, axis=0), batch_size, axis=0)
            greverseAxes = [0] + [x+1 for x in greverseAxes]
        gcpt[:] = arr
        gcpt = np.transpose(gcpt, greverseAxes)
        
        if isbatch:
            if not self.isBatch():
                fcpt = np.expand_dims(fcpt, axis=0)
            if not other.isBatch():
                gcpt = np.expand_dims(gcpt, axis=0)
        prod = fcpt*gcpt
        result = DiscreteCliquePotential(newcpt) 
        result.prob = prod
        result.logNormalization = self.logNormalization + other.logNormalization
        return result
        
    def divide(self, other):
        '''in place divide'''
        if isinstance(other, float) or isinstance(other, int):
            self.prob[:] = self.prob / other
        else:
            self.prob[:] = self.prob / np.maximum(other.prob, 1e-10)
            self.logNormalization -= other.logNormalization
            
    def function(self):
        return self
    
    def marginalize(self, variable):
        assert(variable in self._variables)
        cpt = self
        for var in self._variables:
            if var != variable:
                cpt = cpt.sumOut(var)
        return cpt
    
    def normalize(self, constant=None):
        if constant is None:
            if self.isBatch():
                batch_size = self.prob.shape[0]
                axis = tuple(list(range(1, len(self.prob.shape))))
                constant = np.sum(self.prob, axis=axis, keepdims=True)
                normalizeConstant = np.reshape(constant, (batch_size, ))
            else:
                constant = np.sum(self.prob)
                normalizeConstant = constant
            self.prob[:] = self.prob / constant
        else:
            self.prob[:] = self.prob / constant
        self.logNormalization = np.log(normalizeConstant) + self.logNormalization
    
    def normalizeOver(self, variable):
        # 0th dimension is batch_size
        index = self._variables.index(variable)+1
        constant = np.sum(self.prob, axis=index, keepdims=True)
        self.prob[:] = self.prob / constant
        
    def getDimension(self):
        return len(self._variables)
    
    @property
    def variables(self):
        return self._variables
    
    def sumOut(self, variable):
        '''
        return DiscreteCliquePotential with the specified variable summed out
        '''
        variableIndex = self._variables.index(variable)
        summedArray = np.sum(self.prob, axis=variableIndex+1)
        newvars = list(self._variables)
        newvars.pop(variableIndex)
        cpt = CPTPotential(newvars)
        cliquepotential = DiscreteCliquePotential(cpt)
        cliquepotential.prob = summedArray
        cliquepotential.logNormalization = self.logNormalization.copy()
        return cliquepotential
    
    def clone(self):
        """
        copy _variables and _parameter
        But does not copy the variable in the _variables. Keep the same reference
        """
        variables = list(self._variables)
        result = DiscreteCliquePotential(CPTPotential(variables))
        result.prob = self.prob.copy()
        result.logNormalization = self.logNormalization
        return result
        