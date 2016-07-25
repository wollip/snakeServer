import socket
import random
import numpy as np
import math
import operator


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


def sigmoid( x):
	return 1/(1+np.exp(-x))
def noChange(x):
	return x

class Individual(object):
	def __init__(self, instructions, name, individualName):

		self.instructions = instructions
		self.name = name
		self.individualName = individualName
		self.fitness = 0
		self.testTime = 0

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
	def __init__(self, soc, individual, generationFitness):
		print("Tester is launched")
		self.soc = soc
		self.individual = individual
		self.generationFitness = generationFitness

	def generateMap(self):
		print("begin to generateMap")
		self.currentMap = []
		i = 0
		for index in range(961):
			message = soc.recv(4)
			#print(message)
			self.currentMap.append(int(message[2:]))
		#print(self.currentMap)

	def askIndividual(self):
		index = self.individual.predict(self.currentMap)
		print("direction:", index)
		return index

	def run(self):
		print("run")
		self.generateMap()
		index = self.askIndividual()
		self.soc.send((str(index) + "\n").encode())

	def test(self):
		print("begin testing")
		if self.individual.testTime ==0 :
			for i in range(3):
				message = self.soc.recv(1024)[2:]
				message = str(message)
				if message.find("Do you want to start a game?") != -1:
					self.soc.send("yes\n".encode())
					
				else:
					print(message)
					print("there is an error in Tester. we failed to intialize the game")

				while True:
					print("waiting for message")
					message = str(self.soc.recv(25)[2:])

					print(message)
					if  message.find("what is your next move?") != -1:
						self.run()
					else:
						self.individual.fitness = (self.individual.testTime*self.individual.fitness + int(message[2:-1]) / (self.individual.testTime+1))
						self.individual.testTime +=1
						print(self.individual.testTime)
						#if self.individual.fitness > 350:
						#	self.individual.fitness += int(message[2:])
						#	self.individual.fitness /= 2
						#else:
						#	self.individual.fitness = int(message[2:])
						break

				if self.individual.fitness < self.generationFitness:
					break
		else:
			message = self.soc.recv(1024)[2:]
			message = str(message)
			if message.find("Do you want to start a game?") != -1:
				self.soc.send("yes\n".encode())
			else:
				print(message)		
				print("there is an error in Tester. we failed to intialize the game")

			while True:
				print("waiting for message")
				message = str(self.soc.recv(25)[2:])

				print(message)
				if  message.find( "what is your next move?") != -1:
					self.run()
				else:
					self.individual.fitness = (self.individual.testTime*self.individual.fitness + int(message[2:])) / (self.individual.testTime+1)
					self.individual.testTime +=1
					#print("what the heck are you doing here?")
					break
		print("individual fitness: ", self.individual.fitness, ", testTime: ", self.individual.testTime)

class Breed(object):

	def startEvolution(self):
		for i in range(100):
			print("Generation: ", self.generationNumber, self.GenerationFitness)

			self.evalPopulation()
			self.weedPopulation()

			if self.generationNumber%10 == 0:
				print("********************* begin cleaning generation ************************")
				self.cleanGeneration()

			
			print("********************* begin saving generation data**********************")
			text = open("c:\\Users\\Owner\\Desktop\\python\\snake\\Generation{}.txt".format(self.generationNumber), 'w')
			i2 = 0
			for individual in self.oldGeneration:
				text.write("individual: " + str(i2) + "," + str(individual.fitness) +  "," + str(individual.testTime) + "\n")
				i2+=1
				for instruction in individual.instructions:
					text.write('{}, {}, {}\n'.format(str(instruction[0]), str(instruction[1]), str(instruction[2])))
			text.close()
			
			self.breed()




			self.generationNumber += 1

				

	def cleanGeneration(self):
		print("begin cleaning genes")
		for index, father in enumerate(individuals):
			print(index, father.individualName)
			for mother in individuals[index+1:]:
				#print("testing to see if they are the same", len(father.instructions), len(mother.instructions))
				if len(father.instructions) == len(mother.instructions):
					same = True
					for instructionIndex in range(len(father.instructions)):
						#print(father.instructions[instructionIndex] , mother.instructions[instructionIndex])
						if mother.instructions[instructionIndex] != father.instructions[instructionIndex]:
							same = False

							break
						if same:
							#print("we found something", father.individualName, mother.individualName)
							mother.fitness = (father.fitness*father.testTime + mother.fitness*mother.testTime)/(father.testTime + mother.testTime)
							mother.testTime = father.testTime + mother.testTime
							#print(individuals[index].individualName)
							del individuals[index]
							#print("we are going break")
							break 



	def __init__(self, populationSize, mutationLevel, evolvulationLevel, retainPercentage, soc):

		self.populationSize = populationSize
		self.retainPercentage = retainPercentage
		self.retainSize = int(populationSize*retainPercentage)

		self.mutationLevel = mutationLevel
		self.evolvulationLevel = evolvulationLevel

		self.species = []
		self.generationNumber = 0
		self.GenerationFitness  = 0

		self.restPeriod = 0

		self.soc = soc

		self.individuals = []
		self.oldGeneration = []
		#this the conenctions can change

	def initializePopulation(self):
		print("initializePopulation")
		inputs = []
		for i in range(353,507,31):
			for i2 in range(7):
				inputs.append(i + i2)
		name = inputs + [961, 962, 963]
		for i in range(self.populationSize):
			#this has to  match the length of connectionsNames
			instructions = []
			for oneInput in inputs:
				for outputs in range(961,964):
					weights = random.uniform(0,1)
					instructions.append([oneInput, outputs, weights])
			#print(instructions)
			self.individuals.append(Individual(instructions, name, [i]))

	def evalPopulation(self):
		print("evalPopulation")
		totalFitness = 0
		i = 0
		for individual in self.individuals:
			print()
			print("Testing individual: ", i, ",", individual.individualName)
			i+=1
			testing = Tester(self.soc, individual, self.GenerationFitness)
			testing.test()
			totalFitness += individual.fitness
		self.GenerationFitness = totalFitness / self.populationSize


	def weedPopulation(self):
		print("weedPopulation")
		self.oldGeneration = []
		#for individual in self.individuals:
		#	if individual.fitness > self.GenerationFitness:
		#		self.oldGeneration.append(individual)

		self.individuals = sorted(self.individuals, key = lambda cell: cell.fitness, reverse = True)
		self.oldGeneration = self.individuals[:self.retainSize]

		while len(self.oldGeneration) < self.retainSize:
			self.oldGeneration.append(self.individuals[random.randint(0,len(self.individuals)-1)])

		while len(self.oldGeneration)> self.retainSize:
			del self.oldGeneration[-1]
			#del self.oldGeneration[random.randint(0,len(self.oldGeneration)-1)]

		for individual in self.oldGeneration:
			print(individual.fitness, individual.testTime)
		#sumed = 0
		#for individual in self.oldGeneration:
		#	sumed += individual.fitness
		#self.oldAVG = sumed / len(self.oldGeneration)

	def breed(self):
		print("breed")
		if random.random() <  self.evolvulationLevel and self.restPeriod > 5:
			print('***************we are evolving******************')
			self.evolve()
			self.restPeriod = 0
			self.newGeneration = self.oldGeneration[:]
			self.mate()
		else: 
			self.newGeneration = self.oldGeneration[:]
			self.absoluteMutant()
			self.addMutants()
			self.mate()
			self.restPeriod += 1
		self.individuals = self.newGeneration

	def absoluteMutant(self):
		newInstruction = []
		for instruction in self.oldGeneration[0].instructions:
			newInstruction.append([instruction[0], instruction[1], random.uniform(0,1)])
		self.newGeneration.append(Individual(newInstruction, self.oldGeneration[0].name, [random.choice(range(10000))] ))

	def addMutants(self):
		for individual in self.oldGeneration:
			if random.random() < self.mutationLevel:
				newInstructions = [x[:] for x in individual.instructions]
				if random.random() > 0.5:
					
					newInstructions[random.randint(0,len(newInstructions)-1)][2] = random.uniform(0,1)
				else:
					newInstructions[random.randint(0,len(newInstructions)-1)][2] += random.uniform(-0.1,0.1)*newInstructions[random.randint(0,len(newInstructions)-1)][2] 

				self.newGeneration.append(Individual(newInstructions, individual.name, individual.individualName + [random.choice(range(10000,20000))]))

	def mate(self):
		while len(self.newGeneration) < self.populationSize:
			#print(len(self.newGeneration))
			father = self.oldGeneration[random.randint(0, len(self.oldGeneration)-1)]
			mother = self.newGeneration[random.randint(0, len(self.newGeneration)-1)]
			#print(father.individualName, mother.individualName)

			boolean = set(father.individualName).isdisjoint(mother.individualName)
			if (father is not mother) and (father.name == mother.name) and boolean:
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
				if len(father.individualName) + len(mother.individualName) > 8:
					self.newGeneration.append(Individual(newInstructions, father.name, [random.choice(range(20000,30000))] ))
				else:
					self.newGeneration.append(Individual(newInstructions, father.name, father.individualName + mother.individualName))

				#self.newGeneration.append(Individual(newInstructions, father.name))

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

		print("********************* begin saving generation data**********************")
		text = open("c:\\Users\\Owner\\Desktop\\python\\snake\preEvolution{}.txt".format(self.generationNumber), 'w')
		i2 = 0
		for individual in self.oldGeneration:
			text.write("individual: " + str(i2) + "," + str(individual.fitness) +  "," + str(individual.testTime) + "\n")
			i2+=1
			for instruction in individual.instructions:
				text.write('{}, {}, {}\n'.format(str(instruction[0]), str(instruction[1]), str(instruction[2])))
		text.close()


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
			startNode = random.choice(name*30 + list(range(961)))
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
		print("addingNode is: ", str(addNode))

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

		#print(newConnections)

		#creating new instructions
		checkedConnections = [False]*len(newConnections)
		valid = True

		path = []
		depth = 0
		oneSetOfInstructions = []
		depthToInstruction = [0]*maxDepth
		newInstructions = []
		for exploringNode in outputNode:
			self.checkPath(valid, exploringNode, path, newConnections, checkedConnections, depth, oneSetOfInstructions, depthToInstruction)
			newInstructions.extend(oneSetOfInstructions)

		if valid:
			print("it is valid")
			newInstructions.reverse()
		else:
			self.evolve()
			return

		#print(newInstructions)

		#finding mutationLocation
		for connection in mutantConnections:
			mutationLocation.append(newInstructions.index(connection))
			oldInstructions.insert( mutationLocation[-1], connection + [0])

		newInstructions = oldInstructions
		#print(newInstructions)

		#modifying oldGeneration Instruction to new instructions

		#creating new Specie
		for i in range(int(self.populationSize/2)):
			for index in mutationLocation:
				newInstructions[index][2] = random.uniform(0,1)
				newSpecie.append( Individual(newInstructions, name, [random.choice(range(30000,40000))] ))
		print( 'finished generating new specie' )

		#training new species
		mutantEvolution = Breed(len(newSpecie), self.mutationLevel, 0, self.retainPercentage, self.soc)
		mutantEvolution.individuals = newSpecie
		mutantEvolution.evalPopulation()
		mutantEvolution.weedPopulation()

		originalEvolution = Breed(self.populationSize, self.mutationLevel , 0, self.retainPercentage, self.soc)
		originalEvolution.oldGeneration = self.oldGeneration

		for i in range(3):

			print("training in evolve", i)
			mutantEvolution.breed()
			mutantEvolution.evalPopulation()
			mutantEvolution.weedPopulation()
			
			print("training originalEvolution")
			originalEvolution.breed()
			originalEvolution.evalPopulation()
			originalEvolution.weedPopulation()
			self.generationNumber += 1


		self.oldGeneration = originalEvolution.oldGeneration
		self.oldGeneration.extend(mutantEvolution.oldGeneration)

		print("********************* begin saving generation data**********************")
		text = open("c:\\Users\\Owner\\Desktop\\python\\snake\\endEvolution{}.txt".format(self.generationNumber), 'w')
		i2 = 0
		for individual in self.oldGeneration:
			text.write("individual: " + str(i2) + "," + str(individual.fitness) +  "," + str(individual.testTime) + "\n")
			i2+=1
			for instruction in individual.instructions:
				text.write('{}, {}, {}\n'.format(str(instruction[0]), str(instruction[1]), str(instruction[2])))
		text.close()
		


#def send(message):
#	soc.send(message)

#def receive():
#	return soc.recv(1024)

soc = socket.socket()

serverName = 'localhost'
port = 6066

soc.connect((serverName,port))
print('connected')

print("starting newest version")

populationSize = 200
mutationRate = 0.9
evolutionRate = 0.2
retainPercentage = 0.3
evolution = Breed(populationSize, mutationRate, evolutionRate, retainPercentage, soc)

evolution.initializePopulation()
'''
import csv

with open("c:\\users\owner\\desktop\\python\\snake\\Generation114.txt", 'r') as csvfile:
	reader = csv.reader(csvfile)
	totalList = list(reader)

instructionSet = []
nameSet = []
fitnessSet = []
testTimeSet = []
for line in totalList:
	#print(line)
	if line[0][0] == 'i':

		instructionSet.append([])
		nameSet.append([])
		fitnessSet.append(int(line[1]))
		testTimeSet.append(int(line[2]))
	else:
		if not np.equal(float(line[2]), 0):
			instructionSet[-1].append([int(line[0]), int(line[1]), float(line[2])])
			nameSet[-1].append(int(line[0]))
			nameSet[-1].append(int(line[1]))
names = []
for name in nameSet:
	names.append(list(np.unique(name)))
inputs = []
for i in range(384,509,31):
	for i2 in range(7):
		inputs.append(i + i2)
name = inputs + [961, 962, 963]

name = list(range(964))
individuals = []
for index in range(len(instructionSet)):
	individuals.append(Individual(instructionSet[index], names[index], [index]))
	individuals[-1].fitness = fitnessSet[index]
	individuals[-1].testTime = testTimeSet[index]
	print(individuals[-1].individualName)

evolution.oldGeneration = individuals
print("finished adding previous data")

evolution.evolutionLevel = 0
evolution.breed()
evolution.evolutionLevel = evolutionRate
evolution.generationNumber = 114
evolution.GenerationFitness = 30000
print("finished breeding")
'''






#soc.send('yes')
evolution.startEvolution()

print(soc.recv(1024))

soc.close
print('web socket closed')