'''
This is a class that implements a factor in a Bayesian network. 

The potential field is a conditional probability distribution among the nodes passed to the constructor. The first node is the query variable
in the if the factor is a CPD. The other variables are the parents. If the factor is JPD or other type of factor, this is not the case

This is my implementation for a factor. Feel free to alter it based on your own design for what a node should look like.
If you change the node constructor parameters, however, remember to change the BIF parse script so that the number of variables
received by the constructor is the same as the number of variables given to the constructor. 

'''

import numpy as np

__author__ = "Antoine Bosselut"
__version__ = "1.0.2"
__maintainer__ = "Antoine Bosselut"
__email__ = "antoine.bosselut@uw.edu"
__status__ = "Prototype"

class Factor:
	def __init__(self, table, nodes):
		self.fields = nodes
		self.potential = table
		self.belief = {}

	def updateBelief(self, table):
		self.belief = table;

	def getFields(self):
		return self.nodes;

	def getPotential(self):
		return self.potential;

	def sendBelief(self, information, index):
		i=0
		while (i<len(information))

