'''
Created on 11 Feb 2018

@author: Bryan
'''
from pyltm.model import BayesNet
from pyltm.model import DiscreteVariable, SingularContinuousVariable
from pyltm.model import CPTPotential
import numpy as np

# test discrete BayesNet
# net = BayesNet("toy")
# y = DiscreteVariable("y", 2)
# z = DiscreteVariable("z", 2)
# x = DiscreteVariable("x", 2)
# node_y = net.addNode(y)
# node_z = net.addNode(z)
# node_x = net.addNode(x)
# net.addEdge(node_z, node_y)
# net.addEdge(node_x, node_z)
# 
# print(str(net))
# 
# node_y.potential.setCells([y], np.array([0.5, 0.5]))
# node_z.potential.setCells([y, z], np.array([[0.2, 0.4], [0.1, 0.3]]))
# node_x.potential.setCells([z, x], np.array([[0.2, 0.3], [0.2, 0.3]]))
# 
# print(str(net))

# test continuous BayesNet
net = BayesNet("continuousToy")
y = DiscreteVariable("y", 2)
z = DiscreteVariable("z", 2)
x = SingularContinuousVariable("x")
node_y = net.addNode(y)
node_z = net.addNode(z)
node_x = net.addNode(x)
net.addEdge(node_z, node_y)
net.addEdge(node_x, node_z)

mus = np.array([[0.], [4.]])
covars = np.array([[[1.]], [[4.]]])
node_x.potential.setEntries(mus, covars)
print(str(net))