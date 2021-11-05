from gingerit.gingerit import GingerIt

ip = str(input("Input: \n"))
constraint = 300
print()

dividedInput = ip.split(".")

unifiedOutput = ''

for i in range(len(dividedInput)):
    if(len(dividedInput[i] >= 300)):
        smallerInput = [(ip[i : i + constraint]) for i in range(0, len(dividedInput[i]), constraint)]
        for j in range(len(smallerInput)):
            parser = GingerIt()
            unifiedOutput += parser.parse(smallerInput[i])['result']
    else:
        parser = GingerIt()
        #print("Corrected Output:")
        unifiedOutput += parser.parse(dividedInput[i])['result']

print("Corrected Output:")
print(unifiedOutput)