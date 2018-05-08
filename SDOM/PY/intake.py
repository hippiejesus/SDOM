#!/usr/bin/env python
# -*- coding: utf-8 -*-

import classes as cl
import time
import datetime
import os
import sys
from PyQt4 import QtGui, QtCore, uic

class IntakeWindow(QtGui.QMainWindow):
    def __init__(self):
        super(IntakeWindow, self).__init__()
        uic.loadUi(cl.UIstem+'Intake.ui', self)

        self.newBag.triggered.connect(self.intakeBag)
        self.quit.triggered.connect(self.exit)

    def exit(self):
        QtCore.QCoreApplication.instance().quit()

    def intakeBag(self):
        intakeMain.show()

class IntakeMainWindow(QtGui.QDialog):
    def __init__(self):
        super(IntakeMainWindow, self).__init__()
        uic.loadUi(cl.UIstem+'intakeMain.ui',self)
        
        for company in cl.inv.listAllCompanies:
            self.dropOwner.addItem(company.name)
            
        for location in cl.inv.listAllLocations:
            self.dropLocation.addItem(location.ID)
        
        #Handle Ok and Cancel buttons
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
        
    def okClick(self):
        owner = self.dropOwner.currentText()
        flavor = self.editFlavor.displayText()
        numBags = self.editNumBag.displayText()
        storeLoc = self.dropLocation.currentText()
        
        intakeContainer.setLoad(owner,flavor,numBags,storeLoc)
        intakeContainer.show()
        self.hide()
        intakeContainer.cycle()
        
    def cancelClick(self):
        print('Test Cancel IntakeMain')
        self.hide()
        

class IntakeContainerWindow(QtGui.QDialog):
    def __init__(self):
        super(IntakeContainerWindow, self).__init__()
        uic.loadUi(cl.UIstem+'intakeContainerInput.ui',self)
        
        self.owner = '' ; self.flavor = '' ; self.numBags = '' ; self.storeLoc = ''
        self.shipment = cl.shipment()
        
        #Handle Ok and Cancel buttons
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
        
    def cycle(self):
        currentBags = 0
        self.bagsSoFar = []
        
        while self.buttonBox.accepted != True and int(self.numBags) > currentBags:
            if currentBags >= int(self.numBags): break
            weight, ok= QtGui.QInputDialog.getText(self,self.flavor,'Weight(g): ')
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
                                           ' | '+str(bag.trimWeight)+' g')
                cl.inv.listAllBags.append(bag)
                self.shipment.bags.append(bag)
            else: break;
        
        
    def okClick(self):
        cl.save()
        self.listContainer.clear()
        self.shipment = cl.shipment()
        self.hide()
        
    def cancelClick(self):
        cl.load()       
        self.hide()
        self.listContainer.clear()
        intakeMain.show()
    
    def setLoad(self,owner,flavor,numBags,storeLoc):
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

if __name__ == '__main__':
#def begin():
    app = QtGui.QApplication(sys.argv)

    #Create Base Windows
    intake = IntakeWindow()
    intakeMain = IntakeMainWindow()
    intakeContainer = IntakeContainerWindow()
    

    #Display Intake
    intake.show()

    sys.exit(app.exec_())
