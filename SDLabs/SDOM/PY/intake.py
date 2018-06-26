#!/usr/bin/env python
# -*- coding: utf-8 -*-

import classes as cl
import logger
import qdarkstyle
import time
import datetime
import os
import sys
import subprocess
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import QRect, QPropertyAnimation

class IntakeWindow(QtGui.QMainWindow):
    def __init__(self):
        super(IntakeWindow, self).__init__()
        uic.loadUi(cl.UIstem+'intakeMain.ui', self)

        #self.label.setPixmap(QtGui.QPixmap("/home/pi/python/SDLabs/SDLOGO.jpg"))
        #self.label.setScaledContents(True)

        self.newBag.triggered.connect(self.intakeBag)
        self.quit.triggered.connect(self.exit)
        
        self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py'))
        #self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        self.actionProduct_Management.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        self.actionPackaging.triggered.connect(lambda: self.pageOpen('packaging.py'))
        self.actionDistillate.triggered.connect(lambda: self.pageOpen('distillate.py'))
        self.actionPOS.triggered.connect(lambda: self.pageOpen('pos.py'))
        
        self.listShipments.itemDoubleClicked.connect(self.intakePost)
        
        self.actionPost_Test.triggered.connect(self.intakePost)
        
        self.currentShipments = list()
        self.update()
        
        self.center()
        
    def pageOpen(self,page):
        self.hide()
        app.quit()
        subprocess.call('python '+page, shell=True)
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
       
    def intakePost(self):
        intakePost.setShipment(self.currentShipments[self.listShipments.currentRow()])
        intakePost.show()
        
    def update(self):
        cl.load()
        
        shipments = cl.inv.listAllShipments
        
        self.listShipments.clear()
        self.currentShipments = []
        
        for shipment in shipments:
            if shipment.testResults == []:
                self.listShipments.addItem(str(shipment.ID)+' : '+str(shipment.source)+' -- '+str(shipment.dateIn))
                self.currentShipments.append(shipment)

    def exit(self):
        app.quit()
        self.hide()
        

    def intakeBag(self):
        try:
            intakeMain.show()
            lg.write('IntakeWindow - intakeMain show...')
        except:
            lg.write('IntakeWindow - ERROR: intakeBag(self)',deepData=str(sys.exc_info()))

class IntakeMainWindow(QtGui.QDialog):
    def __init__(self):
        super(IntakeMainWindow, self).__init__()
        uic.loadUi(cl.UIstem+'intakeInitial.ui',self)
        
        for company in cl.inv.listAllCompanies:
            if company.isSupplier: self.dropOwner.addItem(company.name)
            
        for location in cl.inv.listAllLocations:
            self.dropLocation.addItem(location.ID)
        
        #Handle Ok and Cancel buttons
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
        
    def okClick(self):
        try:
            owner = self.dropOwner.currentText()
            flavor = self.editFlavor.displayText()
            numBags = self.editNumBag.displayText()
            storeLoc = self.dropLocation.currentText()
        
            intakeContainer.setLoad(owner,flavor,numBags,storeLoc)
            intakeContainer.show()
            self.hide()
            intakeContainer.cycle()
            lg.write('IntakeContainerWindow - cycling...',deepData=(str(owner)+':'+str(flavor)))
        except:
            lg.write('IntakeMainWindow - ERROR: okClick(self)',deepData=str(sys.exc_info()))
        
    def cancelClick(self):
        try:
            self.hide()
            lg.write('IntakeMainWindow - cancel...')
        except:
            lg.write('IntakeMainWindow - ERROR: cancelClick(self)',deepData=str(sys.exc_info()))
        

class IntakeContainerWindow(QtGui.QDialog):
    def __init__(self):
        super(IntakeContainerWindow, self).__init__()
        uic.loadUi(cl.UIstem+'intakeInitialWeight.ui',self)
        
        self.owner = '' ; self.flavor = '' ; self.numBags = '' ; self.storeLoc = ''
        self.totalWeight = 0.00
        self.shipment = cl.shipment()
        
        #Handle Ok and Cancel buttons
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
        
        self.linePoundPrice.textChanged.connect(self.calculateTotalPrice)
        
    def calculateTotalPrice(self):
        pricePerPound = float(self.linePoundPrice.text())
        totalPrice = float(self.totalWeight)*pricePerPound
        self.labelTotalPrice.setText(str(totalPrice))
        
    def cycle(self):
        currentBags = 0
        self.bagsSoFar = []
        self.totalWeight = 0.00
        self.listContainer.clear()
        try:
            while self.buttonBox.accepted != True and int(self.numBags) > currentBags:
                if currentBags >= int(self.numBags): break
                weight, ok= QtGui.QInputDialog.getText(self,self.flavor,'Weight(lb): ')
                if ok:
                    currentBags += 1
                    bag = cl.trimBag()
                    bag.ID = self.shipment.ID+'-'+str(currentBags)
                    bag.shipment = self.shipment
                    bag.owner = self.owner
                    bag.trimWeight = float(weight)
                    bag.ogTrimWeight = bag.trimWeight
                    bag.flavor = self.flavor
                    self.bagsSoFar.append(bag)
                    self.listContainer.addItem(bag.ID+' | '+self.owner+' | '+
                                                self.flavor+' | '+self.storeLoc+
                                                ' | '+str(bag.trimWeight)+' lb')
                    cl.inv.listAllBags.append(bag)
                    self.shipment.bags.append(bag)
                    self.totalWeight += bag.trimWeight
                    self.labelTotalWeight.setText(str(self.totalWeight))
                    lg.write('IntakeContainerWindow/cycle - bag added...',deepData=bag.ID)
                else: break;
                
        except:
            lg.write('IntakeContainerWindow - ERROR: cycle(self)',deepData=str(sys.exc_info()))
        
        
    def okClick(self):
        try:
            self.shipment.totalPrice = float(self.labelTotalPrice.text())
            self.shipment.totalWeight = float(self.labelTotalWeight.text())
            cl.save()
            self.listContainer.clear()
            self.shipment = cl.shipment()
            self.hide()
            intake.update()
            lg.write('IntakeContainerWindow - shipment saved...')
        except:
            lg.write('IntakeContainerWindow - ERROR: okClick(self)',deepData=str(sys.exc_info()))
        
    def cancelClick(self):
        try:
            cl.load()       
            self.hide()
            self.listContainer.clear()
            intakeMain.show()
            lg.write('IntakeContainerWindow - shipment cancelled...')
        except:
            lg.write('IntakeContainerWindow - ERROR: cancelClick(self)',deepData=str(sys.exc_info()))
    
    def setLoad(self,owner,flavor,numBags,storeLoc):
        try:
            self.shipment = cl.shipment()
            self.shipment.dateIn = time.ctime()
            self.shipment.ID = owner[0]+str(cl.inv.shipmentNumber)+flavor[0]
            cl.inv.shipmentNumber += 1
            cl.inv.listAllShipments.append(self.shipment)
            #cl.save()
        
            self.owner = owner
            self.shipment.source = owner
            self.flavor = flavor
            self.shipment.flavor = flavor
            self.numBags = numBags
            self.storeLoc = storeLoc
            self.shipment.locations.append(storeLoc) 
            self.labelOwnerFlavor.setText('Owner:'+self.owner+'\nFlavor: '+self.flavor)
            self.labelSerial.setText('Serial: '+self.shipment.ID)
            lg.write('IntakeContainerWindow - shipment opened...',deepData=str(owner)+':'+str(flavor)+':'+str(storeLoc))
        except:
            lg.write('IntakeContainerWindow - ERROR: setLoad(self,owner,flavor,numBags,storeLoc)',deepData=str(sys.exc_info()))

###ERROR: items being created before ok is clicked. Cancel does nothing to reverse this. FIX
class IntakePostWindow (QtGui.QDialog):
    def __init__(self):
        super(IntakePostWindow, self).__init__()
        uic.loadUi(cl.UIstem+'intakePost.ui',self)
        
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
        self.totesToSave = list()
        
        self.currentShipment = None
        
    def setShipment(self,shipment):
        try:
            self.currentShipment = shipment
            self.labelOwnerFlavor.setText(str(shipment.source)+'/'+str(shipment.flavor))
            self.labelSerial.setText('Serial: '+str(shipment.ID))
        
            self.fillTotes()
            lg.write('IntakePostWindow - shipment set...')
        except:
            lg.write('IntakePostWindow - ERROR: setShipment(self,shipment)',deepData=str(sys.exc_info()))
      
    def cancelClick(self):
        try:
            self.listContainer.clear()
            if self.pushPass.isChecked(): self.pushPass.toggle()
            if self.pushFail.isChecked(): self.pushFail.toggle()
            self.hide()
            lg.write('IntakePostWindow - post intake cancelled...')
        except:
            lg.write('IntakePostWindow - ERROR: cancelClick(self)',deepData=str(sys.exc_info()))
      
    def okClick(self):
        try:
            locations = cl.inv.listAllLocations
            locationDict = dict()
            for location in locations:
                locationDict.update({str(location.ID):location})
            for tote in self.totesToSave:
                inn, ok = QtGui.QInputDialog.getItem(self,str(tote.ID),'Choose Location:',locationDict.keys())
                if ok:
                    tote.location = locationDict[str(inn)]
                    tote.location.items.append(tote)
                    cl.inv.listAllTotes.append(tote)
                    cl.inv.listAllTotesArchive.append(tote)
                
            self.currentShipment.totes = self.totesToSave
            if self.pushPass.isChecked(): self.currentShipment.testResults.append('Pass')
            elif self.pushFail.isChecked(): self.currentShipment.testResults.append('Fail')
            cl.save()
            self.listContainer.clear()
            self.hide()
            intake.update()
            lg.write('IntakePostWindow - post results saved...',deepData=str(self.totesToSave))
        except:
            lg.write('IntakePostWindow - ERROR: okClick(self)',deepData=str(sys.exc_info()))
        
    def fillTotes(self):
        try:
            weightLbs = self.currentShipment.totalWeight
            weightGs = weightLbs * 450.0
            self.totesToSave = []
            toteNumber = 1
            while weightGs >= 6000:
                tote = cl.trimTote(self.currentShipment.bags[0])
                tote.ID = tote.ID[:-1] + str(toteNumber)
                toteNumber += 1
                tote.ogTrimWeight = 6000
                tote.trimWeight = 6000
                #cl.inv.listAllTotes.append(tote)
                #cl.inv.listAllTotesArchive.append(tote)
                self.totesToSave.append(tote)
                self.listContainer.addItem(str(tote.ID)+' : '+str(tote.trimWeight)+' g -- '+'Flavor: '+tote.flavor+' ___ from '+str(tote.owner))
                weightGs -= 6000
            tote = cl.trimTote(self.currentShipment.bags[0])
            tote.ID = tote.ID[:-1] + str(toteNumber)
            tote.ogTrimWeight = weightGs
            tote.trimWeight = weightGs
            #cl.inv.listAllTotes.append(tote)
            self.totesToSave.append(tote)
            self.listContainer.addItem(str(tote.ID)+' : '+str(tote.trimWeight)+' g -- '+str(tote.owner))
            lg.write('IntakePostWindow - totes filled...')
        except:
            lg.write('IntakePostWindow - ERROR: fillTotes(self)',deepData=str(sys.exc_info()))
        
        
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
        lg = logger.log('intake')
        lg.write('Logging session begin...',deepData='begin_')
    except:
        print('Logger failure...\n'+str(sys.exc_info()))
        sys.exit()

    #Create Base Windows
    try:
        intake = IntakeWindow()
        lg.write('IntakeWindow initialized...')
    except:
        lg.write('IntakeWindow error...\n'+str(sys.exc_info()))
    try:
        intakeMain = IntakeMainWindow()
        lg.write('IntakeMainWindow initialized...')
    except:
        lg.write('IntakeMainWindow error...\n'+str(sys.exc_info()))
    try:
        intakeContainer = IntakeContainerWindow()
        lg.write('IntakeContainerWindow initialized...')
    except:
        lg.write('IntakeContainerWindow error...\n'+str(sys.exc_info()))
        
    intakePost = IntakePostWindow()
    

    #Display Intake
    intake.show()

    sys.exit(app.exec_())
