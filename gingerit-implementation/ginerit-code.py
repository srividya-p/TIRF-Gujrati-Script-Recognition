from gingerit.gingerit import GingerIt

# text = 'The project  aims at developing affine Handwritten Gujarati ScriptRecognitionsysem which can be effectively used for recognizing handwritten Gujarat in scripts'

# Air pollution is one of the most serious problemsin the world. It refers to the contamination of the atmoshere b harmful chemicals orbioloicalmaterials Accordin to the WorldsWorst Poluted Pacesp by Blaycksmith lnstitute in 2O0d,twog of  the worst .pollution pgroblems in the world are uban air quality and ndoor air pollution. To solve the problem of air pollution, its necessary to  understand the issues and look for was to counter itSothe aim of ourroject is to collect air  poluton statistics and analyze it to check it the level .of d,iferent pollutan tsp in air is controlled or check for pattems in the riselfall in the level of different pollutants and extract more of such meaningful information.

ip = str(input("Input: \n"))
constraint = 300

print()

dividedInput = [(ip[i:i+constraint]) for i in range(0, len(ip), constraint)]
#print("Divided input:", dividedInput)

unifiedOutput = ''

for i in range(len(dividedInput)):
    parser = GingerIt()
    #print("Corrected Output:")
    unifiedOutput += parser.parse(dividedInput[i])['result']

print("Corrected Output:")
print(unifiedOutput)