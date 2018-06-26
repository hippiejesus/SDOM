import os
import classes as cl
import logger
import qdarkstyle
import datetime
import time
import re
import sys
import subprocess
from PyQt4 import QtGui, QtCore, uic

products = []
    

class packagingMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(packagingMainWindow, self).__init__()
        uic.loadUi(cl.UIstem+'packagingMain.ui', self)
        
        self.kinds ={'Crumble':self.listCrum,
                     'Crystals':self.listCry,
                     'Distillate':self.listDisto,
                     'Resin':self.listLive,
                     'RSO':self.listRsopt,
                     'Crude':self.listCrude}
        
        self.actionQuit.triggered.connect(self.quitApp)
        self.actionSave.triggered.connect(self.save)
        self.actionPackage_Selected.triggered.connect(self.package)
        self.actionSend_to_Bulk.triggered.connect(self.sendBulk)
        self.actionMake_RSO_PT.triggered.connect(self.makeRsopt)
        
        self.listCrum.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCrum))
        self.listCry.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCry))
        self.listDisto.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listDisto))
        self.listLive.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listLive))
        self.listRsopt.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listRsopt))
        self.listCrude.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCrude))
        
        self.updateLists()
        
        self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py'))
        self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        self.actionProduct_Management.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        #self.actionPackaging.triggered.connect(lambda: self.pageOpen('packaging.py'))
        self.actionDistillate.triggered.connect(lambda: self.pageOpen('distillate.py'))
        self.actionPOS.triggered.connect(lambda: self.pageOpen('pos.py'))
        
        self.center()
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def pageOpen(self,page):
        if self.actionPage_Switch_On_Off.isChecked(): QtCore.QCoreApplication.instance().quit(); self.hide()
        lg.close()
        subprocess.call('python '+page, shell=True)
   
    def quitApp(self):
        QtCore.QCoreApplication.instance().quit()
        self.hide()
        
    def uncheckLists(self,avoidList):
        
        for kind in self.kinds.values():
            item = kind
            current = item.currentItem()
            if current != None and item is not avoidList:
                current.setSelected(False)
                kind.setCurrentItem(None)
            
    def makeRsopt(self):
        for kind in self.kinds.values():
            current = kind.currentItem()
            print kind.currentItem()
            if current != None:
                for product in products:
                    if str(product.ID) == str(current.text()):
                        make.setContainer(product)
        make.show()
                        
        
    def package(self):
        for kind in self.kinds.values():
            current = kind.currentItem()
            print kind.currentItem()
            if current != None:
                for product in products:
                    if str(product.ID) == str(current.text()):
                        select.setContainer(product)
        select.show()
        
    def sendBulk(self):
        for kind in self.kinds.values():
            current = kind.currentItem()
            print kind.currentItem()
            if current != None:
                for product in products:
                    if str(product.ID) == str(current.text()):
                        product.kind = product.kind[3:]
        
    def save(self):
        #try:
        lg.write('packagingMainWindow - saving...')
        cl.save()
        self.updateLists()
        lg.write('packagingMainWindow - save complete...')
        #except:
            #lg.write('packagingMainWindow - ERROR: save(self)')
        
    def updateLists(self):
        global products
        try:
            cl.load()
            products = []
            source = cl.inv.listAllContainers
                   
            for kindList in self.kinds.values():
                kindList.clear()
                
            for container in source:
                if '(P)' in str(container.kind):
                    target = container.kind[3:]
                    if target in self.kinds.keys():
                        self.kinds[target].addItem(container.ID)
                        products.append(container)
                        
            lg.write('packagingMainWindow - lists populated...')
        except:
            lg.write('packagingMainWindow - ERROR: updateLists(self)')
                
        
class packagingMakeWindow(QtGui.QDialog):
    def __init__(self):
        super(packagingMakeWindow, self).__init__()
        uic.loadUi(cl.UIstem+'packagingMake.ui',self)
        
        self.currentContainer = None
        
        self.lineFlavorName.hide()
        
        self.typeButtons = [self.pushRsopt,self.pushDistillate]
        self.lineCurrentWeight.textChanged.connect(self.calculateUsed)
        
        self.buttonBox.rejected.connect(self.cancel)
        self.buttonBox.accepted.connect(self.confirm)
        
        self.pushRsopt.clicked.connect(lambda: self.productTypeClicked(self.pushRsopt))
        self.pushDistillate.clicked.connect(lambda: self.productTypeClicked(self.pushDistillate))
        
    def confirm(self):
        try:
            typeChoice = None
            if self.pushRsopt.isChecked(): typeChoice = 'RSO'
            elif self.pushDistillate.isChecked(): typeChoice = 'Distillate'
        
            cont = self.currentContainer
            newCont = cl.container()
            cont.kind = str(cont.kind)[3:]
            cont.weight = float(self.lineCurrentWeight.text())
            newCont.ID = cont.ID
            if typeChoice == 'RSO': newCont.kind = '(P)RSO'
            elif typeChoice == 'Distillate': 
                newCont.kind = '(P)Distillate'
                newCont.ID = str(self.lineFlavorName.text())
        
            newCont.weight = float(self.lineWeightUsed.text())
            cont.history.append([str(datetime.datetime.now()),'-',newCont.weight,'made into '+str(newCont.ID)+' : '+newCont.kind])
            newCont.history.append([str(datetime.datetime.now()),'+',newCont.weight,'made from '+str(cont.ID)])
            newCont.productIncluded = cont.productIncluded[:]
            cl.inv.listAllContainers.append(newCont)
            cl.inv.listAllContainersArchive.append(newCont)
            newCont.location = cont.location
            newCont.location.items.append(newCont)
        
            self.cancel()
            lg.write('packagingMakeWindow - '+str(typeChoice)+' made...')
        except:
            lg.write('packagingMakeWindow - ERROR: confirm(self)',deepData=str(sys.exc_info()))
        
        
    def productTypeClicked(self, button):
        try:
            for item in self.typeButtons:
                if item != button:
                    if item.isChecked():
                        item.toggle()
                if self.pushDistillate.isChecked():
                    self.lineFlavorName.show()
                else:
                    self.lineFlavorName.hide()
        except:
            lg.write('packagingMakeWindow - ERROR: productTypeClicked(self)',deepData=str(sys.exc_info()))
        
    def update(self):
        try:
            self.lineContainerName.setText(self.currentContainer.ID)
            self.lineStartWeight.setText(str(self.currentContainer.weight))
            lg.write('packagingMakeWindow - update successful...')
        except:
            lg.write('packagingMakeWindow - ERROR: update(self)',deepData=str(sys.exc_info()))
        
    def setContainer(self,container):
        try:
            self.currentContainer = container
            self.update()
            lg.write('packagingMakeWindow - setContainer successful...')
        except:
            lg.write('packagingMakeWindow - ERROR: setContainer(self,container)',deepData=str(sys.exc_info()))
        
    def calculateUsed(self):
        try:
            x = float(self.lineCurrentWeight.text())
            y = float(self.lineStartWeight.text())
            z = y-x
            self.lineWeightUsed.setText(str(z))
        except:
            lg.write('packagingMakeWindow - ERROR: calculateUsed(self)',deepData=str(sys.exc_info()))
        
    def cancel(self):
        try:
            self.lineContainerName.clear()
            self.lineStartWeight.setText('0.00')
            self.lineWeightUsed.setText('0.00')
            self.lineCurrentWeight.setText('0.00')
            self.lineFlavorName.clear()
            self.hide()
            lg.write('packagingMakeWindow - cancelled...')
        except:
            lg.write('packagingMakeWindow - ERROR: cancel(self)',deepData=str(sys.exc_info()))
        
    
        
class packagingSelectWindow(QtGui.QDialog):
    def __init__(self):
        super(packagingSelectWindow, self).__init__()
        uic.loadUi(cl.UIstem+'packagingSelect.ui',self)
        
        self.lineOtherPurp.hide()
        self.lineOtherType.hide()
        
        
        self.lineEdits = [self.lineContainerName,self.lineStartWeight,self.lineUnitPacked,self.lineCurrentWeight,self.lineWeightUsed,self.lineOtherPurp,self.lineOtherType]
        
        self.unitButtons = [self.pushOneGram, self.pushHalfGram, self.pushOtherType]
        
        self.purposeButtons = [self.pushPackaging, self.pushSample, self.pushTesting_2, self.pushOtherPurp]
        
        self.buttonBox.accepted.connect(self.confirm)
        self.buttonBox.rejected.connect(self.cancel)
        
        self.pushOneGram.clicked.connect(lambda: self.unitTypeClicked(self.pushOneGram))
        self.pushHalfGram.clicked.connect(lambda: self.unitTypeClicked(self.pushHalfGram))
        self.pushOtherType.clicked.connect(lambda: self.unitTypeClicked(self.pushOtherType))
        
        self.pushPackaging.clicked.connect(lambda: self.purposeClicked(self.pushPackaging))
        self.pushSample.clicked.connect(lambda: self.purposeClicked(self.pushSample))
        self.pushTesting_2.clicked.connect(lambda: self.purposeClicked(self.pushTesting_2))
        self.pushOtherPurp.clicked.connect(lambda: self.purposeClicked(self.pushOtherPurp))
        
        self.lineCurrentWeight.textChanged.connect(self.calculateUsed)
        
        pass
       
    def confirm(self):
        try:
            global products

            unitChoice = None
            purposeChoice = None 
           
            if self.pushOneGram.isChecked(): unitChoice = 1.00
            elif self.pushHalfGram.isChecked(): unitChoice = 0.50
            elif self.pushOtherType.isChecked(): unitChoice = float(self.lineOtherType.text())
        
            if self.pushPackaging.isChecked(): purposeChoice = 'packaging'
            elif self.pushSample.isChecked(): purposeChoice = 'sample'
            elif self.pushTesting_2.isChecked(): purposeChoice = 'testing'
            elif self.pushOtherPurp.isChecked(): purposeChoise = str(self.lineOtherPurpose.text())
                
                    
        
            cont = self.currentContainer
            newCont = cl.container()
            cont.kind = str(cont.kind)[3:]
        
            cont.weight = float(self.lineCurrentWeight.text())
        
            if purposeChoice == 'packaging': newCont.isPackaged = True
            newCont.purpose = purposeChoice
            newCont.weight = float(self.lineWeightUsed.text())
            newCont.unitSize = unitChoice
            newCont.numberOfUnits = int(self.lineUnitPacked.text())
            newCont.ID = self.lineContainerName.text()
            newCont.kind = cont.kind
            newCont.productIncluded = cont.productIncluded[:]
            newCont.location = cont.location
            newCont.location.items.append(newCont)
            cl.inv.listAllContainers.append(newCont)
            cl.inv.listAllContainersArchive.append(newCont)
            cont.history.append([str(datetime.datetime.now()),'-',newCont.weight,'packaged into '+str(newCont.numberOfUnits)+' units'])
            newCont.history.append([str(datetime.datetime.now()),'+',newCont.weight,'made from '+str(cont.ID)+' : '+cont.kind])
        
            products.append(newCont)
            self.cancel()
            print('Packing Complete')
            lg.write('packagingSelectWindow - packaging successful...')
        except:
            lg.write('packagingSelectWindow - ERROR: confirm(self)',deepData=str(sys.exc_info()))
       
    def calculateUsed(self):
        try:
            x = float(self.lineCurrentWeight.text())
            y = float(self.lineStartWeight.text())
            z = y-x
            self.lineWeightUsed.setText(str(z))
        except:
            lg.write('packagingSelectWindow - ERROR: calculateUsed(self)',deepData=str(sys.exc_info()))
       
    def unitTypeClicked(self, button):
        try:
            for item in self.unitButtons:
                if item != button:
                    if item.isChecked():
                        item.toggle()
                if self.pushOtherType.isChecked():
                    self.lineOtherType.show()
                else:
                    self.lineOtherType.hide()
        except:
            lg.write('packagingSelectWindow - ERROR: unitTypeClicked(self,button)',deepData=str(sys.exc_info()))
    
    def purposeClicked(self, button):
        try:
            for item in self.purposeButtons:
                if item != button:
                    if item.isChecked():
                        item.toggle()
                if self.pushOtherPurp.isChecked():
                    self.lineOtherPurp.show()
                else:
                    self.lineOtherPurp.hide()
        except:
            lg.write('packagingSelectWindow - ERROR: purposeClicked(self,button)',deepData=str(sys.exc_info()))
        
    def cancel(self):
        try:
            self.lineContainerName.clear()
            self.lineStartWeight.setText('0.00')
            self.lineUnitPacked.setText('0')
            self.lineWeightUsed.setText('0.00')
            self.lineCurrentWeight.setText('0.00')
            self.hide()
            lg.write('packagingSelectWindow - cancelled...')
        except:
            lg.write('packagingSelectWindow - ERROR: cancel(self)',deepData=str(sys.exc_info()))
        
    def setContainer(self,container):
        try:
            self.currentContainer = container
            self.update()
            lg.write('packagingSelectWindow - setContainer successful...')
        except:
            lg.write('packagingSelectWindow - ERROR: setContainer(self,container)',deepData=str(sys.exc_info()))
    
    def update(self):
        try:
            self.lineContainerName.setText(self.currentContainer.ID)
            self.lineStartWeight.setText(str(self.currentContainer.weight))
            lg.write('packagingSelectWindow - update successful...')
        except:
            lg.write('packagingSelectWindow - ERROR: update(self)',deepData=str(sys.exc_info()))

def logClose():
    app.quit()
    lg.write('Terminating Session...')
    lg.close()
    subprocess.call('python SDOM.pyw', shell=True)
    
import atexit
atexit.register(logClose)

if __name__ == '__main__':
#def begin():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())
    
    try:
        lg = logger.log('packaging')
        lg.write('Logging session begin...',deepData='begin_')
    except:
        print('Logger failure...')
        sys.exit()

    #Create Base Windows
    try:
        main = packagingMainWindow()
        lg.write('packagingMainWindow initialized...')
    except:
        lg.write('packagingMainWindow error...')
    try:
        make = packagingMakeWindow()
        lg.write('packagingMakeWindow initialized...')
    except:
        lg.write('packagingMakeWindow error...')
        
    try:
        select = packagingSelectWindow()
        lg.write('packagingSelectWindow initialized...')
    except:
        lg.write('packagingSelectWindow error...')

    #Display Start
    main.show()

    sys.exit(app.exec_())
