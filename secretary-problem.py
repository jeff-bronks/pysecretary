# Monte Carlo simulation of the secretary problem.

# Goal is to obtain an estimate of e. The optimal stopping rule should have a factor of 1/e.
# Secondary goal is to confirm the probability (37%) of finding the best candidate.

# Using what Wikipedia says is the best algorithm, viz:
# - Given a list of n candidates, ranked, in random order...
# - Reject the first n * a candidates
# - Record the best score so far (eBest)
# - Continue scoring until one beats eBest (choose this candidate) or no more candidates (choose the last one). 
# - Determine whether the chosen candidate was the best (success) or not (failure).
# - Repeat for random values of a.
# - Build up a histogram of success probability versus a.
# - Find the optimal value of a, which should be approximately 1/e.

# 29.04.23 Started writing.
# 30.04.23 First returned the right answer.

# Python learnings:
# range
# input()
# random.shuffle()
# matplotlib


import numpy as np # for random numbers
import matplotlib.pyplot as plt # for graph plotting
import random
import time

aMin = 0.0
aMax = 1.0
roundSize = 1000 # number of candidates
histSize = 999 # number of bins (needs to be fewer than roundSize to avoid empty bins)
replotSeconds = 1.0 # seconds between plots

def chooseByAlgo(scores,rejectNumber,bestReject):
    i = rejectNumber # first non-rejected candidate; where to start search
    l = len(scores)
    indexBest = 0
    valueBest = 0
    foundItYet = False

    # Search list for first score that beats the reject pile, then stop.
    
    while ((i < l) and not foundItYet):
        if (scores[i] > bestReject):
            valueBest = scores[i]
            indexBest = i
            foundItYet = True
        i += 1

    if (not foundItYet): # failed, so last candidate wins
        valueBest = scores[l-1]
        indexBest = l-1
        
    result={'index': indexBest, 'value': valueBest}
    return result
        
def doRound(roundSize, rejectNumber):
    scores = list(range(roundSize)) # ordered sequence
    random.shuffle(scores) # unorder it
    bestOfAll = np.max(scores)
    #print("Round")
    #print("scores=",scores)
    #print("bestOfAll=",bestOfAll)
    #input("Press Enter")

    # Get best score out of the reject pile.
    if (rejectNumber == 0): # don't reject any
        bestReject = 0
    else:
        if (rejectNumber == 1):
            bestReject = scores[0]
        else:
            bestReject = np.max(scores[0:rejectNumber-1]) 

    # Find first score higher than bestReject, if any, from remaining candidates.
    algoResult = chooseByAlgo(scores,rejectNumber,bestReject)
    value = algoResult['value']
    index = algoResult['index']

    if (value >= bestOfAll): # algorithm succeeded
        return True
    else:
        return False

def dumpHist(histSize,histCount,histSuccess,histMin,histMax):
    print("--- start of histogram ---")
    print("i, amin, amax, count, success, prob")
    binWidth = (histMax - histMin)/histSize
    for i in range(histSize):
        binMin = histMin + binWidth * i
        binMax = histMin + binWidth * (i + 1)
        
        if (histCount[i] == 0):
            prob = "?"
        else:
            prob = format(histSuccess[i]/histCount[i],'.2f')
            
        print(i,format(binMin,'.2f'),format(binMax,'.2f'),histCount[i],histSuccess[i],prob)
    print("--- end of histogram ---")

# Main.

roundCounter = 0

# Intialise the histogram:

histX = np.arange(aMin,aMax,(aMax-aMin)/histSize) # properly scaled x values
histCount = [0] * histSize; # number of rounds done on this bin value
histSuccess = [0] * histSize; # number of successful rounds
histProb = [0] * histSize; # success probabilities

# print("Initial histogram:")
# dumpHist(histSize,histCount,histSuccess,aMin,aMax)
print('Simulation of the secretary problem')
print('Number of bins: ', histSize)

plt.ion() # interactive mode, so we can update the graph
figure, ax = plt.subplots()
line1, = ax.plot(histX,histProb)
ax.set(ylim=[0,0.5])
plt.title('Secretary problem: P vs 1/a ('+str(roundCounter)+' rounds)')
plt.ylabel('P')
plt.xlabel('a')

nextPlotTime = time.time()+replotSeconds

while (True):
    # Pick a random number of candidates to reject.
    rejectNumber = np.random.randint(roundSize) # range 0 to roundSize-1
    a = rejectNumber/roundSize
    binNum = int((a - aMin) * histSize)

    # Do a round of interviews and see if it returns the best candidate or not.
    success = doRound(roundSize, rejectNumber)
    roundCounter += 1

    # Update the histogram.
    histCount[binNum] += 1

    if success:
        histSuccess[binNum] += 1

    if (histCount[binNum] != 0): # avoid dividing by zero
        histProb[binNum] = histSuccess[binNum]/histCount[binNum]
    
    # Replot the graph after a specified time interval:
    if time.time() >= nextPlotTime:
        # print("Round ", roundCounter, ", RejN", rejectNumber, "Result", result)    
        # dumpHist(histSize,histCount,histSuccess,aMin,aMax)
        line1.set_ydata(histProb)
        plt.title('Secretary problem: P vs 1/a ('+str(roundCounter)+' rounds)')
        figure.canvas.draw()
        figure.canvas.flush_events()
        nextPlotTime = time.time()+replotSeconds
