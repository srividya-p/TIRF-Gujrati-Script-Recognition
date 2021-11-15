import time
from gingerit.gingerit import GingerIt

#ip = str(input("Input: \n"))

ip = '''The project  aims at developing affine Handwritten Gujarati Script
Recognition sysem which can be effectively used for recognizing handwritten 
Gujarat in scripts.The system wlltake an image  input which can be of anystandard format such as pg.nzetc, which will de then be pre-processed,then passed to the recognized which will extractthe text  nd 
output through our app. The system wil table to recognize gujarat of different hand writings and wil save overall ime of physical to digital conversion'''

constraint = 300

ip = ip.replace("\n", " ")
dividedInput = ip.split(".")

unifiedOutput = ''

begin = time.time()

for i in range(len(dividedInput)):
    if(len(dividedInput[i]) >= 300):
        smallerInput = [(ip[i : i + constraint]) for i in range(0, len(dividedInput[i]), constraint)]
        for j in range(len(smallerInput)):
            parser = GingerIt()
            unifiedOutput += parser.parse(smallerInput[j])['result']
    else:
        parser = GingerIt()
        #print("Corrected Output:")
        unifiedOutput += parser.parse(dividedInput[i])['result']

end = time.time()

print("Corrected Output:")
print(unifiedOutput)

print("\n\n Time taken = ",str(end-begin), "s")