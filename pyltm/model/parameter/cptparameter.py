'''
Conditional probability table (Array)
Implemented using numpy
May be extended to Tensor computation on GPU.

Created on 12 Feb 2018

@author: Bryan
'''
from .parameter import Parameter
import numpy as np

class CPTParameter(Parameter):
    '''
    classdocs
    '''

    def __init__(self, dims):
        '''
        Constructor
        '''
        self.prob = np.ones(dims) * 1. / np.sum(dims)
        
    def expand_dim(self, axis, cardinality):
        """
        expand current array by adding axis with cardinality specified
        common usage: expand_dim(-1, 2)
        """
        self.prob = np.expand_dims(self.prob, axis=axis)
        self.prob = np.repeat(self.prob, cardinality, axis=axis)
        
    def reduce_dim(self, axis, index):
        """
        reduce current array by slicing the index at specified axis
        example usage: reduce_dim(1, 0)
        """
        swapped_array = np.swapaxes(self._parameter, 0, axis)
        swapped_array = swapped_array[[index], ...]
        back = np.swapaxes(swapped_array, 0, axis)
        self._parameter = np.squeeze(back, axis=axis)
        
    def set_value(self, indexes, value):
        ref = self.prob
        for index in indexes[:-1]:
            ref = ref[index]
        ref[indexes[-1]] = value
        
    def set(self, values, axes=None):
        """
        set values according to axes order
        """
        if axes is None:
            self.prob[:] = values
        else:
            self.prob[:] = np.transpose(values, axes=axes)
            
    def normalize(self, constant=None):
        if constant is None:
            constant = np.sum(self.prob)
            self.prob[:] = self.prob / constant
        else:
            self.prob[:] = self.prob / constant
        return constant 
    
    def copy(self):
        newparameter = CPTParameter(self.prob.shape)
        newparameter.prob[:] = self.prob
        return newparameter
    
    def __str__(self):
        return str(self.prob)
        
        