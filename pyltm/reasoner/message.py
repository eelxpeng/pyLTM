'''
Created on 13 Feb 2018

@author: Bryan
'''
from ..model import CPTPotential
class Message(object):
    '''
    classdocs
    '''


    def __init__(self, cptpotential, logNormalization):
        '''
        Constructor
        '''
        self.cptpotential = cptpotential
        self.logNormalization = logNormalization
        
    def clone(self):
        return Message(self.cptpotential.clone(), self.logNormalization)
    
    def times(self, message):
        return Message(self.cptpotential.times(message.cptpotential), self.logNormalization+message.logNormalization)
    
    @staticmethod
    def computeProduct(messages):
        """
        messages: list of Message
        """
        raise Exception("computeProduct not implemented!")
#         cpt_list = [m.cptpotential for m in messages]
#         logProduct = sum([m.logNormalization for m in messages])
#         return Message(CPTPotential.computeProduct(cpt_list), logProduct)
    
    def divide(self, divider):
        '''divider: Message'''
        if isinstance(divider, CPTPotential):
            self.cptpotential.divide(divider)
        elif isinstance(divider, Message):
            self.cptpotential.divide(divider.cptpotential)
            self.logNormalization -= divider.logNormalization
        
    def function(self):
        return self.cptpotential
        