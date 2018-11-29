'''
Created on 12 Feb 2018

@author: Bryan
'''
from .parameter import Parameter
import numpy as np
import scipy.stats as stats

class CGParameter(Parameter):
    '''
    classdocs
    '''
    def __init__(self, p, num_dim, mu=None, covar=None):
        '''
        Constructor
        '''
        self.p = p
        if mu is None and covar is None:
            self.mu = np.zeros(num_dim)
            self.covar = np.diag(np.ones(num_dim))
        else:
            self.mu = np.copy(mu)
            self.covar = np.copy(covar)
        
    def clone(self):
        newparameter = CGParameter(self.p, len(self.mu), self.mu, self.covar)
        return newparameter
    
    def getEntries(self):
        return self.mu, self.covar
    
    def setEntries(self, mu, covar):
        assert mu.shape==self.mu.shape and covar.shape == self.covar.shape
        self.mu[:] = mu
        self.covar[:] = covar
        
    def setDiagonalTo(self, value):
        np.fill_diagonal(self.covar, value)
        
    def pdf(self, value):
        '''
        value: numpy array, same dimension as mu
        return p*Normal(value | mu, covar)
        '''
        return self.p * stats.multivariate_normal.pdf(value, mean=self.mu, cov=self.covar)

    def logpdf(self, value):
        '''
        value: numpy array, same dimension as mu
        return p*Normal(value | mu, covar)
        '''
        return self.p * stats.multivariate_normal.pdf(value, mean=self.mu, cov=self.covar)
        
    def __str__(self):
        toStr = self.__class__.__name__ + "\n"
        toStr += str(self.p) + "\n"
        toStr += str(self.mu) + "\n"
        toStr += str(self.covar) + "\n"
        return toStr