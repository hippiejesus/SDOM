#Super Dope pickler. [Fully Functional]
#---use: import pickler
#------- save = pickler.pickleSession(saveName,data)
#------- load = pickler.snackTime(saveName)
#------- data = load.data()

import pickle 
import zlib
import os

MODE = 'verbose'

SDPstem = '../.zzz/'
class pickleSession:
    def __init__(self,name,material):
        self.name = name
        if MODE == 'verbose': print("Growing Pickle...")
        pickle_out = open(SDPstem+self.name+".pickle","wb")
        #print("Pickling: " + str(material))
        pickle.dump(material,pickle_out)
        if MODE == 'verbose': print("Putting Pickle in Jar...")
        pickle_out.close()
        if MODE == 'verbose': print("Congrats, its out of your hands now!")
        
        to_compress = open(SDPstem+self.name+".pickle","rb")
        string = to_compress.read()
        compstring = zlib.compress(string)
        to_compress.close()
        
        to_save = open(SDPstem+self.name+".zzz","wb")
        to_save.write(compstring)
        to_save.close()
        
        os.remove(SDPstem+self.name+".pickle")
        
class snackTime:
    def __init__(self,name):
        self.name = name
        to_decompress = open(SDPstem+self.name+".zzz","rb")
        string = to_decompress.read()
        decompstring = zlib.decompress(string)
        to_decompress.close()
        
        to_save = open(SDPstem+self.name+".pickle","wb")
        to_save.write(decompstring)
        to_save.close()
        
        if MODE == 'verbose': print("Juicing Pickle...")
        pickle_in = open(SDPstem+self.name+".pickle","rb")
        self.material = pickle.load(pickle_in)
        #print("Unpickling: "+str(self.material))
        if MODE == 'verbose': print("Closing lid...")
        pickle_in.close()
        os.remove(SDPstem+self.name+".pickle")
        if MODE == 'verbose': print("Enjoy the snack!")

    def data(self):
        return self.material
