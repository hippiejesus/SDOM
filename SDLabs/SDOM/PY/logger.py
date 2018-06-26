import SDPickler as sdp
import datetime
import os
import zlib

deep = []

class log:
    def __init__(self,logType):
        self.anonymousResult = True
        self.logType = logType
        self.timeStamp = datetime.datetime.now()
        self.directory = '../.Logs/'+str(logType)+'/'
        self.deepDirectory = '../.zzz/.Deep_Log/'+self.logType
        if os.path.isdir(self.directory):
            pass
        else:
            os.makedirs(self.directory)
        if os.path.isdir(self.deepDirectory):
            pass
        else:
            os.makedirs(self.deepDirectory)
        self.title = str(self.timeStamp)
        ofile = open(str(self.directory)+str(self.timeStamp)+'.log','w')
        self.ofile = ofile
    def toggleResult(self):
        if self.anonymousResult:
            self.anonymousResult = False
        else:
            self.anonymousResult = True
    def close(self):
        global deep
        self.ofile.close()
        if deep != []:
            deepFile = sdp.pickleSession('.Deep_Log/'+self.logType+'/'+self.title,deep)
        
    def write(self,data,deepData=[],noTime = False):
        global deep
        deep.append(str(deepData))
        message = ' --------> '+str(data)
        if self.anonymousResult == True:
            message = ' --------> '+'Result Found...'
        if noTime == False:
            self.ofile.write(str(datetime.datetime.now())+' -> '+str(data)+'\n')
        else:
            self.ofile.write(str(message)+'\n')
            
