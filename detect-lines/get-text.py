import pandas as pd

infFile = open('0.txt', 'r')
annotations = []
for line in infFile:
    annList = line.strip().split(' ')
    for i in range(1, len(annList)): annList[i] = float(annList[i])
    annList.remove(annList[1])
    annotations.append(annList)

df = pd.DataFrame.from_records(annotations)
df.to_csv('coords.csv')