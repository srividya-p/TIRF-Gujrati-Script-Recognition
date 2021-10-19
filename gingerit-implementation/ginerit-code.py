from gingerit.gingerit import GingerIt

# text = 'The project  aims at developing affine Handwritten Gujarati ScriptRecognitionsysem which can be effectively used for recognizing handwritten Gujarat in scripts'

ip = str(input("Input: \n"))
constraint = 300

dividedInput = [(ip[i:i+constraint]) for i in range(0, len(ip), constraint)]
print("Divided input:", dividedInput)

for i in range(len(dividedInput)):
    parser = GingerIt()
    print("Corrected Output:")
    print(parser.parse(ip)['result'])