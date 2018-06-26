import os
from shutil import copyfile
import SDPickler as sdp

sdp.SDPstem = '../SDOM/.zzz/'
pathHead = '/home/pi/python/SDLabs/SDOM/'
myPathMaster = pathHead
myPathMasterBranches = []
myPathRequest = pathHead
myPathRequestBranches = []
currentFile = ''



def listFiles(target):
    return [f for f in os.listdir(target) if os.path.isfile(target+f)]
    
def sub(root,folder,returnFolder=False):
    if folder == 'logs' : target = '.Logs/'
    elif folder == 'backups' : target = '.BackUps/'
    elif folder == 'data' : target = '.zzz/'
    elif folder == 'deep' : target = '.Deep_Log/'
    elif folder == 'customerRelations' or folder == 'cr' : target = 'customerRelations/'
    elif folder == 'intake' or folder == 'in' : target = 'intake/'
    elif folder == 'finishing' or folder == 'fi' : target = 'finishing/'
    elif folder == 'yield' or folder == 'yi' : target = 'yield/'
    elif folder == 'distillate' or folder == 'di' : target = 'distillate/'
    elif folder == 'packaging' or folder == 'pa' : target = 'packaging/'
    elif folder == 'productManagement' or folder == 'pm' : target = 'productManagement/'
    elif folder == 'lab' : target = 'lab/'
    else: target = folder
    if returnFolder == False: return listFiles(root + target)
    else: return root + target
    
def listList(source):
    
    i = 0
    for item in source:
        print(str(i)+' == '+item)
        i += 1
        
def chooseFromList(source):
    listList(source)
    targetIndex = raw_input('enter index___')
    return source[int(targetIndex)]
    
def getDeep(source,sourcePath,target):
    global deepLogs
    sp = sourcePath.split('/')
    st = str(sp[-2])
    return deep(st+'/'+target)
    
def deep(source):
    global deepPath
    return deepPath + source[:-3] + 'zzz'
    
def unPickle(deepFilePath):
    global dataPath
    #fileName = deepFilePath.split('/')[-1]
    copyfile(deepFilePath,dataPath+'temp.zzz')
    load = sdp.snackTime('temp')
    return load.data()
    
def openFile(sourceFilePath):
    global currentFile
    currentFile = open(sourceFilePath,'r')
    
def closeFile():
    global currentFile
    currentFile.close()
    
def listFile():
    global currentFile
    result = []
    for line in currentFile:
        result.append(line)
    return result
    
def files(source):
    return sub(source,'')
    
def compare(filePath,target):
    openFile(filePath+'/'+target)
    fileData = listFile()
    deepData = unPickle(getDeep(files(filePath),filePath,target))
    for i in fileData:
        print(str(i)+' -d- '+str(deepData[fileData.index(i)]))
    closeFile()
        
def invokeCompare(path):
    sourcePath = path
    target = chooseFromList(files(sourcePath))
    openFile(sourcePath+'/'+target)
    compare(sourcePath,target)
    
    
logPath = sub(myPathMaster,'logs',True)

crPath = sub(logPath,'cr',True)

inPath = sub(logPath,'in',True)

labPath = sub(logPath,'lab',True)

yiPath = sub(logPath,'yi',True)

fiPath = sub(logPath,'fi',True)

diPath = sub(logPath,'di',True)

paPath = sub(logPath,'pa',True)

pmPath = sub(logPath,'pm',True)

dataPath = sub(myPathMaster,'data',True)

deepPath = sub(dataPath,'deep',True)

if __name__ == '__main__':
    
    while True:

        paths = {'Customer Relations':crPath,'Intake':inPath,'Lab':labPath,
                 'Yield':yiPath,'Finishing':fiPath,'Distillate':diPath,'Packaging':paPath,
                 'Product Management':pmPath}
 
        pathList = ['Customer Relations','Intake','Lab','Yield','Finishing','Distillate','Packaging','Product Management']
        try:
            invokeCompare(paths[chooseFromList(pathList)])
        except:
            print('Path Empty...')



