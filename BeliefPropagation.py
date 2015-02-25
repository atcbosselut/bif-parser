#!/usr/bin/env python

'''
BeliefPropagation.py

'''

import Node
import Factor
import BIFParser
import sys
import numpy as np

__author__ = "Antoine Bosselut"
__version__ = "1.0.2"
__maintainer__ = "Antoine Bosselut"
__email__ = "antoine.bosselut@uw.edu"
__status__ = "Prototype"

def main():
	f = open("hw3-dist/%s" %sys.argv[1],"r")
	BIF = f.readlines()

	BIF = BIFParser.fixWhiteSpace(BIF)
	BN = BIFParser.parseBIF(BIF)
	factors = []
	for nodes in BN:
		if not nodes.isRoot():
			tempArray = [nodes]
			tempArray.extend(nodes.getParents())
			factors.append(Factor.Factor(nodes.getDist(), tempArray))
	#print len(factors)
	#for f in factors:
		#print f.getPotential()

	i=0
	while i<1:
		for a in BN:
			for f in factors:
				if partOf(a,f):
					message = a.sendMarginal(f)
					f.receiveBelief(message, a)
		#for f in factor:
		#	f.updateBelief()
		for f in factors:
			for a in BN:
				if partOf(a,f):
					message = f.sendBelief(a)
					a.receiveMarginal(message, f)
		for a in BN:
			a.updateMarginal()
		i+=1

	for a in BN:
		print a.getMarginal()

def partOf(node,factor):
	for b in factor.getFields():
		if node.getName() == b.getName():
			return True
	return False

main()