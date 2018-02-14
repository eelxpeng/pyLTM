'''
Created on 14 Feb 2018

@author: Bryan
'''
import math
import collections

class Evidence(object):
    '''
    classdocs
    '''


    def __init__(self, other=None):
        '''
        Constructor
        '''
        if other is None:
            self._entries = dict()
        else:
            self._entries = other.entries.copy()
            
    def project(self, variables):
        '''list/set of Variable'''
        projected = Evidence()
        for var in self._entries:
            if var in variables:
                projected.add(var, self._entries[var])
        
        return projected
    
    def add(self, variable, value):
        if isinstance(variable, collections.Iterable):
            for i in range(len(variable)):
                self.add(variable[i], value[i])
        else:
            if math.isnan(value):
                self._entries.pop(variable)
            else:
                self._entries[variable] = value
                
    def clear(self):
        self._entries.clear()
        
    def clone(self):
        return Evidence(self)
    
    def __str__(self):
        return str(self._entries)
            
    