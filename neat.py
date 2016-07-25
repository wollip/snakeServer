import random
import numpy as np
import math
import operator

# location of different normalizing operations
def noChange(n):
    return n

def sigmoid( x):
    return 1/(1+np.exp(-x))

def abstanh(x):
    return math.fabs(math.tanh(x))

def absolute(x):
    return math.fabs(x)

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
                nodeVals[instruction[0]] = sigmoid(nodeVals[instruction[0]])
                
            nodeVals[instruction[1]] += nodeVals[instruction[0]] * instruction[2]
        
        outputs = []
        for node in outputNode:
        	outputs.append(sigmoid(nodeVals[node]))

        index, value = max(enumerate(outputs), key=operator.itemgetter(1))
	
        return index
    
class Tester(object):
	def __init__(self, soc, individual):
		self.soc = soc
		self.individual = individual
		if self.soc.recv(1024)[2:] == "Do you want to start a game?":
			self.soc.send("yes")
		else:
			print("there is an error in Tester. we failed to intialize the game")

	def generateMap(self):
		self.currentMap = [0]*961
		for index in self.currentMap:
			index = soc.recv(8)
		print(self.currentMap)

	def askIndividual(self):
		index = self.individual.predict(self.currentMap)
		return index

	def run(self):
		self.generateMap()
		index = self.askIndividual()
		self.soc.send(str(index))

	def test(self):
		if self.soc.recv(1024)[2:] == "what is your next move?":
			self.run()
		else:
			
			message = self.soc.recv(1024)[2:]
			self.individual.fitness = int(message)


class Breed(object):

	def startEvolution():
		for i in range(100):
			self.evalPopulation()
			self.weedPopulation()
			if i%5 == 0:
				text = open("c:\\Users\\Owner\\Desktop\\python\\snake\\instructions{}.txt".format(i/20), 'w')
				for instruction in breed.oldGeneration[0].instructions:
					text.write('{}, {}, {}\n'.format(instruction[0], instruction[1], instruction[2]))
			self.breed()
    
	def __init__(self, populationSize, mutationLevel, evolvulationLevel, retainPercentage, soc):
		self.populationSize = populationSize
    	self.retainSize = int(populationSize*retainPercentage)
        
        self.mutationLevel = mutationLevel
        self.evolvulationLevel = evolvulationLevel
        
        self.species = []
        self.generationNumber = 0
    
    	self.soc = soc

        self.individuals = []
        #this the conenctions can change
        
	def initializePopulation(self):
		name = list(range(962))
        for i in range(self.populationSize):
            #this has to  match the length of connectionsNames
            weights = [random.uniform(-1,1) for i in range(961)]
            instructions = [[index, 961] + [weights[index]] for index in range(961)]
            self.individuals.append(Individual(instructions, name))
    
	def evalPopulation(self):
		totalFitness = 0
		for individual in self.individuals:
			testing = Tester(self.soc, individual)
        	testing.test()
        	totalFitness += individual.fitness
        self.GenerationFitness = totalFitness / self.populationSize
		
    
	def weedPopulation(self):
		self.oldGeneration = []
        for individual in self.individuals:
            if individual.fitness < self.GenerationFitness:
                self.oldGeneration.append(individual)
        
        self.oldGeneration = sorted(self.oldGeneration, key = lambda cell: cell.fitVal)
        
        while len(self.oldGeneration) < self.retainSize:
            self.oldGeneration.append(self.individuals[random.randint(0,len(self.individuals)-1)])
        
        while len(self.oldGeneration)> self.retainSize:
            del self.oldGeneration[-1]
            del self.oldGeneration[random.randint(0,len(self.oldGeneration)-1)]
        
        sumed = 0
        for individual in self.oldGeneration:
            sumed += individual.fitness
        self.oldAVG = sumed / len(self.oldGeneration)
    
	def breed(self):
		if random.random() <  self.evolvulationLevel:
			print('***************we are evolving******************')
			self.evolve()
        self.newGeneration = self.oldGeneration[:]
        self.addMutants()
        self.mate()
        self.individuals = self.newGeneration
    
	def addMutants(self):
		for individual in self.oldGeneration:
			if random.random() < self.mutationLevel:
				newInstructions = [x[:] for x in individual.instructions]
                newInstructions[random.randint(0,len(newInstructions)-1)][2] = random.uniform(-1,1)
                
                self.newGeneration.append(Individual(newInstructions, individual.name))
    #### mate needs to make sure the instructions match up
	def mate(self):
		while len(self.newGeneration) < self.populationSize:
			father = self.oldGeneration[random.randint(0, len(self.oldGeneration)-1)]
			mother = self.newGeneration[random.randint(0, len(self.newGeneration)-1)]
			if father is not mother:
				if father.name == mother.name:
					newInstructions = [ x[:] for x in father.instructions]
					for index in range(len(newInstructions)):
						newInstructions[index][2] = 0
                        if random.random()>0.5:
                            
                            for instruction in father.instructions:
                                if instruction[:2] == newInstructions[index][:2]:
                                    newInstructions[index][2] = instruction[2]
                                    break
                            
                        else:
                            for instruction in mother.instructions:
                                if instruction[:2] == newInstructions[index][:2]:
                                    newInstructions[index][2] = instruction[2]
                                    break
                        self.newGeneration.append(Individual(newInstructions, father.name))
 
 	def checkPath(self, valid, exploringNode, path, newConnections, checkedConnections, depth, instructions, depthToInstruction):
 		if depth >= maxDepth:
 			print("max depth has been reached")
 			return False
        
        #depth +=1
        
        if not valid:
        	print("somehow passed a not valid function")
        	return False
                   
        for index in range(len(newConnections)):
            
            if newConnections[index][1] == exploringNode:
                #print()
                #print('current depth', depth)
                #print(exploringNode, "connects to:", newConnections[index][0])
                
                newpath = path[:] + [newConnections[index][0]]
                #print("current path:", newpath)
                
                if len(np.unique(newpath)) != len(newpath):
                    #print('individual is no longer valid')
                    valid = False
                    return False
                
                if not checkedConnections[index]:
                    instructions.insert(depthToInstruction[depth], newConnections[index])
                    #print("inserting instruction at location",depthToInstruction[depth])
                    for index1 in range(depth, maxDepth):
                        depthToInstruction[index1] += 1
                    #print(depthToInstruction)
                    #print(instructions)
                    checkedConnections[index] = True
                
                
             
            
                
                if nodes[newConnections[index][0]] != 'input':
                    #print("recursively calling on check Path for node", newConnections[index][0])
                    newDepth = depth + 1
                    boolean = self.checkPath(valid, newConnections[index][0], newpath, newConnections, checkedConnections, newDepth, instructions, depthToInstruction)
                    #if not boolean:
                    #    return False
        return True
    
	def evolve(self):
		startNode = None
        endNode = None
        addNode = False
        name = self.oldGeneration[0].name[:]
        oldInstructions = self.oldGeneration[0].instructions[:]
        newConnections = []
        mutantConnections = []
        mutationLocation = []
        newSpecie = []
        
        print(' starting evolution')
        
        #finding the start and end Node
        while True:
            startNode = random.choice(name)
            if nodes[startNode] == 'output':
                continue
            
            endNode = random.choice(name)
            if nodes[endNode] != 'input' and endNode != startNode:
                break
            
        print(startNode, endNode)
        
        #checking if we need to add a new node
        for connection in oldInstructions:
            if [startNode, endNode] == connection[:2]:
                addNode = True
                break
        print(addNode)
        
        #creating list of conncetions
        for instruction in oldInstructions:
            newConnections.append(instruction[:2])
            
        if addNode:
            newNode = len(nodes)
            nodes.append('hidden')
            newConnections.append([startNode, newNode])
            mutantConnections.append([startNode, newNode])
            newConnections.append([newNode, endNode])
            mutantConnections.append([newNode, endNode])
            name.append(newNode)
        else:
            newConnections.append([startNode, endNode])
            mutantConnections.append([startNode, endNode])
        
        print(newConnections)
        
        #creating new instructions
        checkedConnections = [False]*len(newConnections)
        valid = True
        exploringNode = outputNode
        path = []
        depth = 0
        newInstructions = []
        depthToInstruction = [0]*maxDepth
        
        self.checkPath(valid, exploringNode, path, newConnections, checkedConnections, depth, newInstructions, depthToInstruction)
        if valid:
            newInstructions.reverse()
        else:
            self.evolve()
            return
         
        print(newInstructions)
        
        #finding mutationLocation
        for connection in mutantConnections:
            mutationLocation.append(newInstructions.index(connection))
            oldInstructions.insert( mutationLocation[-1], connection + [0]) 
        
        newInstructions = oldInstructions
        print(newInstructions)
        
        #modifying oldGeneration Instruction to new instructions
        
        #creating new Specie
        for i in range(int(populationSize * retainPercentage)):
            for index in mutationLocation:
                newInstructions[index][2] = random.uniform(-1,1)
            newSpecie.append( Individual(newInstructions, name))
        print( 'finished generating new specie' )
        
        #training new species
        mutantEvolution = Breed(len(newSpecie), mutationLevel, 0, retainPercentage*2, self.soc)
        mutantEvolution.individuals = newSpecie
        for i in range(7):
            mutantEvolution.evalPopulation()
            mutantEvolution.weedPopulation()
            mutantEvolution.breed()
        self.oldGeneration.extend(mutantEvolution.individuals)
 
#global variables
outputNode = [931,932,933]
maxDepth = 10
#nodes
nodes = []
for i in range(961):
	nodes.append('input')
for i in range(3):
	nodes,append('output')

#connections
connections = []
for i in range(961):
	for node in outputNode:
		connections.append([i,node])

import socket
soc = socket.socket()

Breed(100, 0.2, 0.2, 0.2, soc).startEvolution