import SDPickler as sdp
import datetime
import os
import zlib

class log:
    def __init__(self,logType):
        self.logType = logType
        self.timeStamp = datetime.datetime.now()
        self.directory = '../.Logs/'+str(logType)+'/'
        if os.path.isdir(self.directory):
            pass
        else:
            os.makedirs(self.directory)
        ofile = open(self.directory+str(self.timeStamp)+'.log','w')
        self.ofile = ofile
    def close(self):
        self.ofile.close()
        
    def write(self,data,noTime = False):
        if noTime == False:
            self.ofile.write(str(datetime.datetime.now())+' -> '+str(data))
        else:
            message = ' --------> '+str(data)
            self.ofile.write(str(message)+'\n')
            
