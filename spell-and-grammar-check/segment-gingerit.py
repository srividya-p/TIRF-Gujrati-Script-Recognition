import time
from gingerit.gingerit import GingerIt
from wordsegment import load, segment
load() #loading word segment

#ip = str(input("Input: \n"))

ip = '''Air pollution is one of the most serious problemsin the world. It refers to the contamination of the atmoshere b harmful chemicals orbioloicalmaterials Accordin to the WorldsWorst Poluted Pacesp by Blaycksmith lnstitute in 2O0d,twog of  the worst .pollution pgroblems in the world are uban air quality and ndoor air pollution. To solve the problem of air pollution, its necessary to  understand the issues and look for was to counter itSothe aim of ourroject is to collect air  poluton statistics and analyze it to check it the level .of d,iferent pollutan tsp in air is controlled or check for pattems in the riselfall in the level of different pollutants and extract more of such meaningful information.'''

constraintG = 300
constraintW = 200
begin = time.time()

ip = ip.replace("\n", " ")
dividedInput = ip.split(".")

unifiedOutput = ''
segmentOutput = ''

#gingerit
for i in range(len(dividedInput)):
    if(len(dividedInput[i]) >= 300):
        smallerInput = [(ip[i : i + constraintG]) for i in range(0, len(dividedInput[i]), constraintG)]
        for j in range(len(smallerInput)):
            parser = GingerIt()
            unifiedOutput += parser.parse(smallerInput[j])['result']
    else:
        parser = GingerIt()
        #print("Corrected Output:")
        unifiedOutput += parser.parse(dividedInput[i])['result']

#word segment

wordList = unifiedOutput.split()

for i in range(len(wordList)):
    if(len(wordList[i]) >= 200):
        smallerInput = [(ip[i : i + constraintW]) for i in range(0, len(wordList[i]), constraintW)]
        for j in range(len(smallerInput)):
            segmentOutput += str(segment(smallerInput[j]))
    else:
        segmentOutput += str(segment(wordList[i]))


print(type(segmentOutput))
print()
print(segmentOutput)

finalOutput = ''
# spelling and grammar check
for i in range(len(segmentOutput)):
    if(len(segmentOutput[i]) >= 300):
        smallerInput = [(segmentOutput[i : i + constraintG]) for i in range(0, len(segmentOutput[i]), constraintG)]
        for j in range(len(smallerInput)):
            parser = GingerIt()
            finalOutput += parser.parse(smallerInput[j])['result']
    else:
        parser = GingerIt()
        #print("Corrected Output:")
        finalOutput += parser.parse(segmentOutput[i])['result']
 
# for i in range(len(unifiedOutput)):
#     finalOutput += str(segment(unifiedOutput[i]))

# segmentInput = [(ip[i:i+constraint]) for i in range(0, len(unifiedOutput), constraint)]

# for i in range(len(segmentInput)):
#     finalOutput += segment(segmentInput[i])

end = time.time()

print("Corrected Output:")
print(finalOutput)
print("\n Time taken = ",str(end-begin), "s")