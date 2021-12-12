from gingerit.gingerit import GingerIt

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