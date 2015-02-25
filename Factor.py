'''
This is a class that implements a factor in a Bayesian network. 

The potential field is a conditional probability distribution among the nodes passed to the constructor. The first node is the query variable
in the if the factor is a CPD. The other variables are the parents. If the factor is JPD or other type of factor, this is not the case

This is my implementation for a factor. Feel free to alter it based on your own design for what a node should look like.
If you change the node constructor parameters, however, remember to change the BIF parse script so that the number of variables
received by the constructor is the same as the number of variables given to the constructor. 

'''

import copy
import numpy as np

__author__ = "Antoine Bosselut"
__version__ = "1.0.3"
__maintainer__ = "Antoine Bosselut"
__email__ = "antoine.bosselut@uw.edu"
__status__ = "Prototype"

class Factor:
	def __init__(self, table, nodes):
		self.fields = nodes
		self.states = table.keys()[0][0]
		self.potential = {}
		self.information = {}
		for key, value in table.iteritems():
			i=0
			while i<len(value):
				newKey = [key[0][i]]
				newKey.extend(list(key[1]))
				newKey = tuple(newKey)
				self.potential[newKey] = value[i]
				i+=1

	def receiveBelief(self, message, node):
		#Set Information for the node received using its message
		self.information[node.getName()] = message

	def getIndex(self, nodeName):
		i = 0
		while i < len(self.getFields()):
			if self.fields[i].getName() == nodeName:
				return i
			i+=1

	def getFields(self):
		return self.fields;

	def getPotential(self):
		return self.potential;

	def sendBelief(self, node):
		i=self.getIndex(node.getName())
		j=len(self.fields)-1 #0
		sumOver = copy.deepcopy(self.potential)
		while j >= 0: #len(self.fields):
			#print ("i: %s" %i)
			#print ("numFields: %s" %len(self.fields))
			if i != j:
				tempNode = self.getFields()[j]
				key = tempNode.getName()
				#self.printFactor()
				info = copy.deepcopy(self.information[key])
				tupleKeys = sumOver.keys()
				tempDict = {}
				for tups in tupleKeys:
					tempDict[tups[:j] + tups[j+1:]] = 0
				for tups in tupleKeys:
					#print("Length Tups: %s" %len(tups))
					#print("j: %s" %j)
					#if j != len(tups):
					#print tups
					tempDict[tups[:j] + tups[(j+1):]] = tempDict[tups[:j] + tups[(j+1):]] + sumOver[tups]*info[tups[j]]
					#else:
					#	tempDict[tups[:j]] = tempDict[tups[:j]] + sumOver[tups]*info[tups[j]]
				sumOver = copy.deepcopy(tempDict)
			j-=1 #+=1
		return sumOver

	def printFactor(self):
		print("Fields: ")
		for a in self.fields:
			print a.getName()
						
		#TODO get product of information and multiply by potential. Then sum over nodes that don't matter and send