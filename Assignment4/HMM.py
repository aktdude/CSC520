import sys
import pandas as pd
import numpy as np
import copy
import random

# List of hidden variables
global hiddenVars
# List of observable variables
global observedVars
# Dictionary of start probabilities
global startDict
# List of hidden to hidden probabilities
global transProbs
# List of hidden to observable probabilities
global observedProbs
# Dictionary of H1 Probabilities
global h1Probs

def variableNames(lines):
    global hiddenVars
    global observedVars   
   
    for line in lines:
        if line.startswith('HIDDEN'):
            hiddenVars = commaSeparate(line)
            hiddenVars.pop(0)
        elif line.startswith('OBSERVED'):
            observedVars = commaSeparate(line)
            observedVars.pop(0)
    # print("Variables:")
    # print(hiddenVars)
    # print(observedVars)
    # printLineBreak()
    return
def transitionStartVariables(lines):
    global hiddenVars
    global startDict
    
    print("\nSTART PROBABILITIES")
    for line in lines:
        start = commaSeparate(line)
        start.pop(0)
        start.pop(0)
        if(start[0] in hiddenVars):
            startDict[start[0]]=start[1]
            print("p(H0 = " + start[0] + ") = " + start[1])
    printLineBreak()
    return
def transitionVariables(lines):
    global transProbs
    print("TRANSITION PROBABILITIES")
    for line in lines:
        transition = commaSeparate(line)
        transition.pop(0)
        transProbs.append(transition)
        print("p(H(i) = " + transition[0]+ " | H(i-1) = "+ transition[1] +") = " + transition[2])
    transProbs = np.array(transProbs)
    printLineBreak()
    return
def observationVariables(lines):
    global observedProbs
    print("OBSERVATION PROBABILITIES")
    for line in lines:
        observation = commaSeparate(line)
        observation.pop(0)
        observedProbs.append(observation)
        print("p(O(i) = " + observation[0]+ " | H(i) = "+ observation[1] +") = " + observation[2])
    printLineBreak()
    return
def firstTransitionNoEvidence():
    global hiddenVars
    global h1Probs
    global transProbs
    firstCol =  transProbs[:,0]
    for i in range(len(hiddenVars)):
        sum = 0
        currentLetter = hiddenVars[i]
        for j in range(len(firstCol)):
            if firstCol[j] == currentLetter:
                sum += float(startDict[transProbs[j][1]]) * float(transProbs[j][2])
        h1Probs[hiddenVars[i]] = round(sum,5)
        #h1Probs[hiddenVars[i]] = round(sum,2)
    print("\np(H1): "+ str(h1Probs) + "\n")
    return

def filterNext(iteration, currentInput, previousDict):
    global h1Probs
    currentDict = {}
    alpha = 0
    # For first case, since we've already found p(H1)
    if(iteration == 0):        
        givenObservedProbs = {}
        # Get the probabilities of the current input given the different states
        for i in range(len(observedProbs)):
            if(observedProbs[i][0] == currentInput):
                givenObservedProbs[observedProbs[i][1]] = float(observedProbs[i][2])
        flippedAlpha = 0
        # Multiply with our already calculated p(H1)
        for i in range(len(hiddenVars)):
            givenObservedProbs[hiddenVars[i]] = float(givenObservedProbs[hiddenVars[i]] * h1Probs[hiddenVars[i]])
            flippedAlpha = flippedAlpha + givenObservedProbs[hiddenVars[i]]
        
        #Flip alpha
        alpha = 1/ flippedAlpha
        for i in range(len(hiddenVars)):
            currentDict[hiddenVars[i]] = round(float(givenObservedProbs[hiddenVars[i]] * alpha),5)
        alpha = round(alpha,5)
    #For recursive case
    else:
        global transProbs
        hNextProbs = {}
        firstCol =  transProbs[:,0]
        givenObservedProbs = {}
        # Get the probabilities of the current input given the different states
        for i in range(len(observedProbs)):
            if(observedProbs[i][0] == currentInput):
                givenObservedProbs[observedProbs[i][1]] = float(observedProbs[i][2])
        flippedAlpha = 0
        for i in range(len(hiddenVars)):
            sum = 0
            currentLetter = hiddenVars[i]
            for j in range(len(firstCol)):
                if firstCol[j] == currentLetter:
                    sum += float(previousDict[transProbs[j][1]]) * float(transProbs[j][2])
            hNextProbs[hiddenVars[i]] = round(sum,5)
        for i in range(len(hiddenVars)):
            givenObservedProbs[hiddenVars[i]] = float(givenObservedProbs[hiddenVars[i]] * hNextProbs[hiddenVars[i]])
            flippedAlpha = flippedAlpha + givenObservedProbs[hiddenVars[i]]
        #Flip alpha
        alpha = 1/ flippedAlpha
        for i in range(len(hiddenVars)):
            currentDict[hiddenVars[i]] = round(float(givenObservedProbs[hiddenVars[i]] * alpha),5)
        alpha = round(alpha,5)


    return currentDict, alpha

def updatedDistribution(inputs):
    global startDict
    given = ""

    # Initial No Evidence Probabilities
    print("RESULTS")
    print("\nBefore evidence observed:")
    print("p(H0): "+ str(startDict))
    firstTransitionNoEvidence()
    currentDict = {}
    # Iterate through evidence
    for i in range(len(inputs)):
        
        alpha = 0
        # String formatting
        if(given == ""):
            given = given + inputs[i]
        else:
            given = given + "," + inputs[i]

        currentDict, alpha = filterNext(i, inputs[i], currentDict)
        # Print new distribution
        print("State " + inputs[i] + " observed")
        print("\tUpdated distribution ( p(H" + str(i+1) + " | " + given + ") ) = " + str(currentDict) + " (alpha=" + str(alpha) + ")\n")
    return

def printLineBreak():
    print("--------------------------------")
def commaSeparate(line):
    line = line.replace("\n", "")
    return line.split(",")

def filterFromFile(filename, inputs):
    #Initialize global variables
    global observedVars
    global hiddenVars
    global startDict
    global transProbs
    global observedProbs
    global h1Probs
    observedVars = []
    hiddenVars= []
    startDict = {}
    transProbs = []
    observedProbs= []
    h1Probs = {}

    # open the file
    with open(filename, 'r') as f:
        # break the file into 4 groups
        group1 = []
        group2 = []
        group3 = []
        group4 = []
        
        # read the file line by line and split into sections
        for line in f:
            # determine which group the line belongs to based on its prefix
            if line.startswith('HIDDEN'):
                group1.append(line)
            elif line.startswith('OBSERVED'):
                group1.append(line)
            elif line.startswith('TRANSITION-PROBABILITY,START'):
                group4.append(line)
            elif line.startswith('TRANSITION'):
                group2.append(line)
            elif line.startswith('OBSERVATION'):
                group3.append(line)

    # Input From File
    variableNames(group1)
    
    transitionStartVariables(group4)

    transitionVariables(group2)

    observationVariables(group3)

    # Calculations
    updatedDistribution(inputs)


def main():
    fileName = sys.argv[1]
    inputs = sys.argv[2]
    filterFromFile(fileName, inputs)   

if __name__ == "__main__":
    main()