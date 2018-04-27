'''
Created on 27 Apr 2018

@author: Bryan
'''
from .datacase import Datacase
from ...model import SingularContinuousVariable, JointContinuousVariable
from ...reasoner.evidence import Evidence

class ContinuousDatacase(Datacase):
    '''
    classdocs
    '''
    def __init__(self, variables):
        '''
        Param: list of Variable
        '''
        self._variables = variables
        self._map = dict()
        for i in range(len(self._variables)):
            var = self._variables[i]
            self._map[var] = i
        self._data = None # should be a list or 1d array
        
    @staticmethod
    def create(varNames):
        '''
        Param: list of string of variable name
        '''
        variables = []
        for name in varNames:
            variables.append(SingularContinuousVariable(name))
        return ContinuousDatacase(variables)
        
    def getEvidence(self):
        '''return Evidence'''
        evidence = Evidence()
        evidence.add(self._variables, self._data)
        return evidence
    
    def putValues(self, values):
        self._data = values
        
    @property
    def variables(self):
        return self._variables
    
    def getValue(self, var):
        return self._data[self._map[var]]

    def synchronize(self, model):
        # create a dictionary mapping variable name to Variable
        varmap = dict()
        for var in list(model._variables.keys()):
            if isinstance(var, JointContinuousVariable):
                for v in var.variables:
                    varmap[v.name] = v
            else:
                varmap[var.name] = var
        for i in range(len(self._variables)):
            oldvariable = self._variables[i]
            variable = varmap[oldvariable.name]
            if variable is None:
                continue
            self._variables[i] = variable
            self._map.pop(oldvariable)
            self._map[variable] = i
        