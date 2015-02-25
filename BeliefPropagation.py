#!/usr/bin/env python

'''
BeliefPropagation.py

'''
from __future__ import division
import Node
import Factor
import BIFParser
import sys
import copy
import numpy as np

__author__ = "Antoine Bosselut"
__version__ = "1.0.4"
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

	converged=False
	converNum=0
	while not converged:
		prevConverNum = copy.deepcopy(converNum)
		converNum=0
		for a in BN:
			for f in factors:
				if partOf(a,f):
					message = a.sendMarginal(f)
					f.receiveBelief(message, a)
		for f in factors:
			for a in BN:
				if partOf(a,f):
					message = f.sendBelief(a)
					a.receiveMarginal(message, f)
		for a in BN:
			a.updateMarginal()
			converNum += a.getMarginal()[a.getMarginal().keys()[0]]
		if (np.abs(converNum-prevConverNum) < .00001):
			converged=True		
	g=open("results.txt","w")

	for a in BN:
		g.write(a.getName() + " ")
		print a.getMarginal()
		i=len(a.getMarginal().keys())-1
		while(i >= 0):
			g.write(str(a.getMarginal()[a.getMarginal().keys()[i]]) + " ")
			i-=1
		g.write("\n")

	g.close()


def partOf(node,factor):
	for b in factor.getFields():
		if node.getName() == b.getName():
			return True
	return False

main()