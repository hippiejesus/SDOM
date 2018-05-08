import os
import sys
import customerRelations
import lab
import intake
import finishing
import yieldW
import productManagement
import distillate
import multiprocessing as mp
from PyQt4 import QtGui, QtCore, uic

class ChoiceWindow(QtGui.QInputDialog):
    def __init__(self):
        super(ChoiceWindow, self).__init__()
        
    def choose(self):
        options = ['customerRelations','intake','lab','finishing','yield','productManagement','distillate']
        inn, ok = QtGui.QInputDialog.getItem(self,'Choose','Window:',options)
        if ok:
        #inn = raw_input("start: ")
            inn = str(inn)
            if inn == 'customerRelations':
                customerRelations.begin()
            if inn == 'intake':
                intake.begin()
            if inn == 'lab':
                lab.begin()
            if inn == 'finishing':
                finishing.begin()
            if inn == 'yield':
                yieldW.begin()
            if inn == 'productManagement':
                productManagement.begin()
            if inn == 'distillate':
                distillate.begin()
        


if __name__ == '__main__':
    print('Begin.')
    app = QtGui.QApplication(sys.argv)
    c = ChoiceWindow()
    while True:
        c.choose()
    sys.exit(app.exec_())
    
    
