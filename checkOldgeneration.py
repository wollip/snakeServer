import csv
import numpy as np

import random

import math
import operator

with open("C:\\Users\\Owner\\Desktop\\python\\snake\\Generation0.txt", 'r') as csvfile:
	reader = csv.reader(csvfile)
	totalList = list(reader)

#from pythonServer import Tester, Individual

def sigmoid( x):
    return 1/(1+np.exp(-x))
def noChange(x):
	return x
class Individual(object):
    def __init__(self, instructions, name):

        self.instructions = instructions
        self.name = name
        self.fitness = float('inf')

    def predict(self, oneInputSet):
        nodeVals = oneInputSet[:] + [0]*(len(nodes)-len(oneInputSet))
        changedNodes = [False]*len(nodes)

        for instruction in self.instructions:

            if not changedNodes[instruction[0]]:
                changedNodes[instruction[0]] = True

                #change this for different type of functions
                nodeVals[instruction[0]] = noChange(nodeVals[instruction[0]])

            nodeVals[instruction[1]] += nodeVals[instruction[0]] * instruction[2]

        outputs = []
        for node in outputNode:
            outputs.append(sigmoid(nodeVals[node]))
        #print(outputs)
        index = outputs.index(max(outputs))
        return index

class Tester(object):
    def __init__(self, soc, individual):
        print("Tester is launched")
        self.soc = soc
        self.individual = individual
        print(self.soc.recv(1024)[2:])
        self.soc.send("yes\n")
        #else:
        #    print("there is an error in Tester. we failed to intialize the game")

    def generateMap(self):
        #print("begin to generateMap")
        self.currentMap = []
        i = 0
        for index in range(961):
        	message = soc.recv(4)
        	self.currentMap.append(int(message[2:]))
        #print(self.currentMap)

    def askIndividual(self):
        index = self.individual.predict(self.currentMap)
        #print("direction:", index)
        return index

    def run(self):
        #print("run")
        self.generateMap()
        index = self.askIndividual()
        self.soc.send(str(index) + "\n")

    def test(self):
        print("begin testing")
        while True:
            #print("waiting for message")
            message = self.soc.recv(25)

            #print(message)
            if  message[2:] == "what is your next move?":
                self.run()
            else:
                self.individual.fitness = int(message[2:])
                print("individual fitness: ", self.individual.fitness)
                break


instructionSet = []
i = -1
for line in totalList:
	if line[0][0] == 'i':
		instructionSet.append([])
		i+=1
		print('creating a new individual')
	else:
		instructionSet[i].append([int(line[0]), int(line[1]), float(line[2])])


#print(instructionSet[0])

#global variables
outputNode = [961,962,963]
maxDepth = 10
#nodes
nodes = []
for i in range(961):
    nodes.append('input')
for i in range(3):
    nodes.append('output')

#connections
connections = []
for i in range(961):
    for node in outputNode:
        connections.append([i,node])

name = list(range(964))
individuals = []
for instructions in instructionSet:
	individuals.append(Individual(instructions, name))



import socket
soc = socket.socket()
serverName = 'localhost'
port = 6066

soc.connect((serverName, port))

for individual in individuals:
	testing = Tester(soc, individual)
	testing.test()

