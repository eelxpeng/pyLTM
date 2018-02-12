'''
Created on 11 Feb 2018

@author: Bryan
'''
from abc import ABCMeta
from ...util import Counter
class Variable(metaclass=ABCMeta):
    '''
    classdocs
    '''
    _counter = Counter("variable")

    def __init__(self, name=None):
        '''
        Constructor
        '''
        if name is None:
            name, index = Variable._counter.next()
        else:
            name = name.strip()
            index = Variable._counter.nextIndex()
            Variable._counter.encounterName(name)
        self._name = name
        self._index = index
    
    def _compare(self, o):
        """
        depends on _index, indicating this object created earlier or later than o
        """
        return self._index - o._index

    def __lt__(self, other):
        return self._compare(other)<0

    def __le__(self, other):
        return self._compare(other)<=0

    def __eq__(self, other):
        return self._compare(other)==0

    def __ge__(self, other):
        return self._compare(other)>=0

    def __gt__(self, other):
        return self._compare(other)>0

    def __ne__(self, other):
        return self._compare(other)!=0
    
    def __hash__(self):
        return hash(self._index)
    
    @property
    def name(self):
        return self._name
    
    def setName(self, name):
        self._name = name.strip()
    
    def __str__(self):
        return self.name
        