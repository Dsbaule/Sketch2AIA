import os

classes = '10'
train = 'train.txt'
valid = 'val.txt'
names = 'obj.names'
backup = 'backup'

curFolder = os.path.dirname(os.path.abspath(__file__))

fileString = 'classes=' + classes + '\n'
fileString += 'train=' + os.path.join(curFolder, train) + '\n'
fileString += 'valid=' + os.path.join(curFolder, valid) + '\n'
fileString += 'names=' + os.path.join(curFolder, names) + '\n'
fileString += 'backup=' + os.path.join(curFolder, backup) + '\n'

with open("./obj.data", "w") as metaFile:
    metaFile.write(fileString)