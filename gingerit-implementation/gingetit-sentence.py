from gingerit.gingerit import GingerIt

ip = str(input("Input: \n"))

print()

dividedInput = ip.split(".")

unifiedOutput = ''

for i in range(len(dividedInput)):
    parser = GingerIt()
    #print("Corrected Output:")
    unifiedOutput += parser.parse(dividedInput[i])['result']

print("Corrected Output:")
print(unifiedOutput)