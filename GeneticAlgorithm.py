from random import random, randint, choice
import math

#### Genetic Algorithm ####

### Helper funcitons ###
## Tournament selection. ##
def tournament(population, tournamentMembers, fitnessFunction, inverse=False):
    tournament = [] # Create list of random indexes.
    # Add random index to tournament list if index not already in the list.
    while(len(tournament) < tournamentMembers):
        randomIndex = randint(0, len(population) - 1)
        if(randomIndex not in tournament):
            tournament.append(randomIndex)

    if(inverse == False):
        winnerIndex = max(tournament, key = lambda member: fitnessFunction(population[member])) # Get the member with the highest fitness.
    else:
        winnerIndex = min(tournament, key = lambda member: fitnessFunction(population[member])) # Get the member with the lowest fitness.
    #print(winnerIndex, tournament)
    return winnerIndex
## ##
### ###

### Genetic Algorithm ####
def geneticAlg(chromosomeSize, popSize, endValue, fitnessFunction, crossoverChance = 0.7, mutationChance = 0.01, tournamentMembers = 2, generations = 1000):
    # End program when fitnessFunction value >= endValue.
    population = []
    
    ## Create random starting population. ##
    for n in range(popSize):
        # Crate a random binary chromosome.
        newChromosome = "".join(choice('01') for i in range(chromosomeSize))
        population.append(newChromosome)
    ## ##
    #print(population) 


    # Loop while fitness < end value or current generation < generations.
    generation = 1
    while(generation < generations and max(fitnessFunction(chromosome) for chromosome in population) < endValue):
        print("Average:", sum(fitnessFunction(chromosome) for chromosome in population) // len(population))
        print("Best:", max(fitnessFunction(chromosome) for chromosome in population))
        print("Generation:", generation)
        
        # Go through each individual.
        for individual in population:
            newChromosome = ""
            if random() > crossoverChance:
                # Clone.
                # Tournament select.
                indIndex = tournament(population, tournamentMembers, fitnessFunction)
                #print("winnerIndex : ", winnerIndex)
                newChromosome =  population[indIndex]               
            else:
                ## 1-point crossover. ##
                # Pick two individuals.
                indIndex1 = tournament(population, tournamentMembers, fitnessFunction)
                indIndex2 = tournament(population, tournamentMembers, fitnessFunction)

                # Pick random point (not start or end) to cut.
                cutIndex = randint(1, chromosomeSize-2)
                newChromosome = population[indIndex1][0:cutIndex] + population[indIndex2][cutIndex:]
                ## ##
                
                #print(population[indIndex1], population[indIndex2], cutIndex, newChromosome)

            ## Random Mutation ##
            mutation = ""
            # Go through each bit in the new chromosome.
            for i in range(len(newChromosome)):
                if(random() < mutationChance):
                    mutation += str(1 - int(newChromosome[i]))
                    #print("Mutate", newChromosome[i], "to", str(1 - int(newChromosome[i])))
                else:
                    mutation += newChromosome[i]
            newChromosome = mutation
            ## ##

            ## Steady State GA: Put individual back into the current population. ##
            # Get the worst individual.
            indIndex = tournament(population, tournamentMembers, fitnessFunction, inverse=True)
            population[indIndex] = newChromosome
            ## ##
        
        generation = generation + 1
    print("\nBest chromosome:", max(population, key=fitnessFunction) + ",", "Value:", fitnessFunction(max(population, key=fitnessFunction)))
### ###
    
#### ####


### 1. Maximise the ones. ###
# Fitness function counts the number of 1's in the given binary string.
def binaryCount(binaryString):
    t = 0
    return t + sum((int(bit) for bit in binaryString))

# Run the genetic algorithm.
geneticAlg(chromosomeSize = 100, popSize = 500, endValue = 100, fitnessFunction = binaryCount
, crossoverChance = 0.8, mutationChance = 0.05, tournamentMembers = 5, generations = 100)

### ###


### 2. Knapsack Problem. ###
# Boxes and the max weight the container can hold.
boxes = [
    {"weight": 30, "value": 15},
    {"weight": 60, "value": 40},
    {"weight": 10, "value": 20},
    {"weight": 25, "value": 20},
    {"weight": 40, "value": 30},
]
wTotal = 100

# Loop through all the bits, and if bit is 1, first add the weight and then add the value of the box if the weight remains below wTotal.
def knapsackProblem(binaryString):
    totalValue = 0
    totalWeight = 0
    for index in range(len(binaryString)):
        if(int(binaryString[index]) == 1):
            totalWeight += boxes[index]["weight"]
            totalValue += boxes[index]["value"]

    if(totalWeight <= wTotal):
        return totalValue
    else:
        return 0

# Run the genetic algorithm.
geneticAlg(chromosomeSize = len(boxes), popSize = 5, endValue = 80, fitnessFunction = knapsackProblem
, crossoverChance = 0.75, mutationChance = 0.15, tournamentMembers = 2, generations = 100)

### ###


### 3. Function Optimisation. ###

## Single-objective Optimization: Schaffer function N.2 ##
# Finding the minimum, which is at x = 0, y = 0.

# First 7 digits in binary string turns into decimal which represents x, and last 7 digits in binary string turns into decimal which represents y.
# 7 digit long binary because it is the minimum number to achieve 100 decimal number.
def schafferFunctionN2(binaryString):
    # Max value of x and y is 100 according to the function.
    x = int(binaryString[0:len(binaryString)//2], 2) if int(binaryString[0:len(binaryString)//2], 2) <= 100 else 100
    y = int(binaryString[len(binaryString)//2:len(binaryString)], 2) if int(binaryString[len(binaryString)//2:len(binaryString)], 2) <= 100 else 100

    formulaAnswer = 0.5+(((math.sin(x**2 - y**2))**2 - 0.5) / ((1 + 0.01*(x**2 + y**2))**2))
    return formulaAnswer

# Run the genetic algorithm. -Fitness funciton turns the maximisation GE into a minimisation GE.
geneticAlg(chromosomeSize = 14, popSize = 10, endValue = 0, fitnessFunction = lambda x: -schafferFunctionN2(x)
, crossoverChance = 0.7, mutationChance = 0.03, tournamentMembers = 2, generations = 500)
## ##


## Constrained Optimisation : Rosenbrock function constrained to a disk ##
# Finding the minimum, which is at x = 1, y = 1.

# First digit designate sign (+ or -) and the second the bit before the fractional binary.
# First half is for the x value, second half is for the y.
# Fractional numbers x and y are from 1.5 to -1.5.
# Need at least 2 binary digits to represent 1 and 1.5. The larger the number of fractional digits, the smaller the number increments.
def rosenbrockFConstrainedToDisk(binaryString):
    b_x = binaryString[1:2]+'.'+binaryString[2:len(binaryString)//2] # Put decimal point after 2nd digit. x Value.
    s_x, f_x = b_x.find('.')+1, int(b_x.replace('.',''), 2) # Get binary before decimal, and after decimal.
    b_y = binaryString[(len(binaryString)//2)+1:(len(binaryString)//2)+2]+'.'+binaryString[(len(binaryString)//2)+2:len(binaryString)] # Put decimal point after 2nd digit. y Value.
    s_y, f_y = b_y.find('.')+1, int(b_y.replace('.',''), 2) # Get binary before decimal, and after decimal.
    #print(b_x, b_y, s_x, f_x, s_y, f_y)
    # Formula for converting fractional binary to decimal.
    x = f_x/2.**(len(b_x)-s_x) if s_x else f_x
    y = f_y/2.**(len(b_y)-s_y) if s_y else f_y
    # Check if positive or nagative (0 bit means negative 1 means positive)
    x = x if binaryString[0:1] == '1' else -x
    y = y if binaryString[len(binaryString)//2:(len(binaryString)//2)+1] == '1' else -y

    # Constraint.
    if(x**2 + y**2 <= 2):
        return (1-x)**2+100*((y-x**2)**2) # Formula
    else:
        return 525

# Best fitness is 11001100 => x = 1 and y=1 => 0.
    
# Run the genetic algorithm. -Fitness funciton turns the maximisation GE into a minimisation GE.
geneticAlg(chromosomeSize = 10, popSize = 50, endValue = 0, fitnessFunction = lambda x: -rosenbrockFConstrainedToDisk(x)
, crossoverChance = 0.75, mutationChance = 0.2, tournamentMembers = 2, generations = 1000)

### ###


### 4. Own problem. ###
# Modified Assignment Problem: Maximise the values given that one row can have one column as its assignment.
# i.e., Any agent (row) can be assigned to perform any task (column), with the [row, column] being the cost associated with that task.
# An agent can only have one task. Find an assignment of agent/tasks in such a way that the total cost of the assignment is maximised.
costMatrix = [[3,0,3,4],
              [5,5,0,8],
              [9,0,13,5],
              [2,14,1,25]]

## Fitness Function ##
# Every two bits is treated like a binary and gets converted into a decimal number.
# This decimal number denotes which column to assign for row 0 to n every two bits.
def modifiedAssignmentProblem(binary):
    total = 0
    i = 0
    costMatrixI = 0
    occupiedIndexes = []
    # Loop every two bits
    for bit in binary:
        if(i % 2 == 0):
            bitString = ""
            bitString = bitString + str(binary[i]) + str(binary[i + 1])
            binaryValue = int(bitString, 2)
            # Check if index denoted by the binary to decimal number is available.
            if(binaryValue not in occupiedIndexes):
                total = total + costMatrix[costMatrixI][binaryValue]
                occupiedIndexes.append(binaryValue)
                costMatrixI = costMatrixI + 1
            else:
                return 0
        i = i + 1

    #print("binary: ", binary)
    #print("occupiedIndexes: ", occupiedIndexes)
    return total

# Run the genetic algorithm.
geneticAlg(chromosomeSize = len(costMatrix)*2, popSize = 5, endValue = 46, fitnessFunction = modifiedAssignmentProblem
, crossoverChance = 0.75, mutationChance = 0.05, tournamentMembers = 2, generations = 500)

### ###










    
