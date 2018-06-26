#!/usr/bin/env python
# -*- coding: utf-8 -*-

#self.listProduct
#self.label

import os.path
import classes as cl
import datetime
import qdarkstyle
import re
import csv
import sys
import subprocess
from PyQt4 import QtGui, QtCore, uic

cl.load()
options = {'Containers':cl.inv.listAllContainers,
           'Product':cl.inv.listAllFinishedProduct,
           'Unfinished Product':cl.inv.listAllUnfinishedProduct,
           'Trim':cl.inv.listAllTotes,
           'Runs':cl.inv.listAllRuns,
           'Shipments':cl.inv.listAllShipments,
           'Locations':cl.inv.listAllLocations}

class SearchWindow(QtGui.QDialog):
    def __init__(self):
        super(SearchWindow, self).__init__()
        uic.loadUi(cl.UIstem+'inventoryView.ui', self)
        
        self.currentItem = None
        self.currentCategory = None
        
        self.edit = dict()
        
        self.currentLabel = None
        
        self.listProduct.itemDoubleClicked.connect(self.doubleEvent)
        self.pushBack.clicked.connect(self.back)
        self.save.clicked.connect(self.saveData)
        
        self.setContents()
        
        self.center()
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def saveData(self):
        cl.save()
    
    def back(self):
        if self.currentItem != None: self.currentItem = None
        elif self.currentCategory != None: self.currentCategory = None
        
        self.setContents()
    
    def doubleEvent(self):
        if self.currentCategory != None:
            if self.currentItem != None:
                current = self.listProduct.currentItem()
                text = str(current.text())
                split = text.split(' : ')
                current = self.currentItem
                if split[0] == 'runs included':
                            optionList = []
                            for i in self.currentItem.runsIncluded:
                                optionList.append(i.ID)
                            inn, ok = QtGui.QInputDialog.getItem(self,'Choose','Choose run to view:',optionList)
                            if ok:
                                for i in self.currentItem.runsIncluded:
                                    if i.ID == inn:
                                        self.currentItem = i
                                        self.setContents()
                                        return
                if split[0] == 'trim included':
                            optionList = []
                            for i in self.currentItem.trimIncluded:
                                optionList.append(i.ID)
                            inn, ok = QtGui.QInputDialog.getItem(self,'Choose','Choose trim to view:',optionList)
                            if ok:
                                for i in self.currentItem.trimIncluded:
                                    if i.ID == inn:
                                        self.currentItem = i
                                        self.setContents()
                                        return
                elif split[0] == 'bags recieved':
                            optionList = []
                            for i in self.currentItem.bags:
                                optionList.append(str(i.ID))
                            inn, ok = QtGui.QInputDialog.getItem(self,'Choose','Choose bag to view:',optionList)
                            if ok:
                                for i in cl.inv.listAllBags:
                                    if i.ID == inn:
                                        self.currentItem = i
                                        self.setContents()
                                        return
                elif split[0] == 'location':
                            optionList = []
                            for i in cl.inv.listAllLocations:
                                optionList.append(i.ID)
                            inn, ok = QtGui.QInputDialog.getItem(self,'Choose','Choose location to move to:',optionList)
                            if ok:
                                for i in cl.inv.listAllLocations:
                                    if i.ID == inn:
                                        try:
                                            self.currentItem.location.items.pop(self.currentItem.location.items.index(self.currentItem))
                                        except: pass
                                        self.currentItem.location = i
                                        i.items.append(self.currentItem)
                                        self.setContents()
                                        return
                elif split[0] == 'shipment':
                            for i in cl.inv.listAllShipments:
                                if i.ID == split[1]:
                                    self.currentItem = i
                                    self.setContents()
                                    return
                elif split[0] == 'container':
                            for i in cl.inv.listAllContainers:
                                if i.ID == split[1]:
                                    self.currentItem = i
                                    self.setContents()
                                    return
                elif split[0] == 'unfinished product included':
                            optionList = []
                            for i in self.currentItem.unfinishedProductIncluded:
                                optionList.append(str(i.ID))
                            inn, ok = QtGui.QInputDialog.getItem(self,'Choose','Choose unfinished product to view:',optionList)
                            if ok:
                                for i in self.currentItem.unfinishedProductIncluded:
                                    if str(i.ID) == inn:
                                        self.currentItem = i
                                        self.setContents()
                                        return
                elif split[0] == 'product included':
                            optionList = []
                            for i in self.currentItem.productIncluded:
                                optionList.append(str(i.ID))
                            inn, ok = QtGui.QInputDialog.getItem(self,'Choose','Choose finished product to view:',optionList)
                            if ok:
                                for i in self.currentItem.productIncluded:
                                    if str(i.ID) == inn:
                                        self.currentItem = i
                                        self.setContents()
                                        return
                                
                
                inn, ok = QtGui.QInputDialog.getText(self,'Choose','Choose a new value for this variable:')
                if ok:
                    print(split[0])
                    try:
                        if split[0] == 'ID':
                            current.ID = str(inn)
                        elif split[0] == 'owner':
                            current.owner = str(inn)
                        elif split[0] == 'trim weight':
                            current.trimWeight = float(inn)
                        elif split[0] == 'weight':
                            current.weight = float(inn)
                        elif split[0] == 'original trim weight':
                            current.ogTrimWeight = float(inn)
                        elif split[0] == 'flavor':
                            current.flavor = str(inn)
                        elif split[0] == 'test results':
                            pass
                    except:
                        print('double click error')
                    self.setContents()
                
            else:
                current = self.listProduct.currentItem()
                text = str(current.text())
                split = text.split(' : ')
                for item in options[self.currentCategory]:
                    try:
                        if item.ID == split[0]:
                            self.currentItem = item
                    except:
                        runs = []
                        for i in cl.inv.listAllRuns:
                            for run in i[1]:
                                runs.append(run)
                        for run in runs:
                            if run.ID == split[0]:
                                self.currentItem = run
        else: 
            current = self.listProduct.currentItem()
            self.currentCategory = str(current.text())
        
        self.setContents()
        
    def setContents(self):
        self.listProduct.clear()
        if self.currentItem == None and self.currentCategory == None:
            self.label.hide()
            for item in options.keys():
                self.listProduct.addItem(str(item))
        elif self.currentItem != None:
            self.label.show()
            self.label.setText(str(self.currentItem.ID)+': '+str(self.currentItem.kind))
            item = self.currentItem
            if isinstance(item,cl.trimTote):
                self.listProduct.addItem('ID : '+str(item.ID))
                self.listProduct.addItem('shipment : '+str(item.shipment.ID))
                self.listProduct.addItem('owner : '+str(item.owner))
                self.listProduct.addItem('trim weight : '+str(item.trimWeight))
                self.listProduct.addItem('original trim weight : '+str(item.ogTrimWeight))
                self.listProduct.addItem('flavor : '+str(item.flavor))
                try:
                    self.listProduct.addItem('location : '+str(item.location.ID))
                except:
                    self.listProduct.addItem('location : '+str(item.location))
                self.listProduct.addItem('test results : '+str(item.testResults))
            elif isinstance(item,cl.trimBag):
                self.listProduct.addItem('ID : '+str(item.ID))
                self.listProduct.addItem('shipment : '+str(item.shipment.ID))
                self.listProduct.addItem('owner : '+str(item.owner))
                self.listProduct.addItem('trim weight : '+str(item.trimWeight))
                self.listProduct.addItem('original trim weight : '+str(item.ogTrimWeight))
                self.listProduct.addItem('flavor : '+str(item.flavor))
            elif isinstance(item,cl.unfinishedProduct):
                self.listProduct.addItem('ID : '+str(item.ID))
                runsIn = []
                for i in item.runsIncluded:
                    runsIn.append(str(i.ID))
                self.listProduct.addItem('runs included : '+str(runsIn))
                self.listProduct.addItem('owner : '+str(item.owner))
                self.listProduct.addItem('intended finish : '+str(item.intendedFinish))
                self.listProduct.addItem('test results : '+str(item.testResults))
                try:
                    self.listProduct.addItem('location : '+str(item.location.ID))
                except:
                    self.listProduct.addItem('location : '+str(item.location))
            elif isinstance(item,cl.finishedProduct):
                self.listProduct.addItem('ID : '+str(item.ID))
                uPIn = []
                for i in item.unfinishedProductIncluded:
                    uPIn.append(str(i.ID))
                self.listProduct.addItem('unfinished product included : '+str(uPIn))
                self.listProduct.addItem('owner : '+str(item.owner))
                self.listProduct.addItem('kind : '+str(item.kind))
                self.listProduct.addItem('weight : '+str(item.weight))
                self.listProduct.addItem('container : '+str(item.container.ID))
                self.listProduct.addItem('test results : '+str(item.testResults))
            elif isinstance(item,cl.run):
                self.listProduct.addItem('ID : '+str(item.ID))
                trimIn = []
                for i in item.trimIncluded:
                    trimIn.append(str(i.ID))
                trimAm = []
                for i in item.trimAmounts:
                    trimAm.append(i)
                self.listProduct.addItem('trim included : '+str(trimIn))
                self.listProduct.addItem('trim amounts : '+str(trimAm))
                self.listProduct.addItem('start time : '+str(item.timeStart))
                self.listProduct.addItem('owner : '+str(item.owner))
                self.listProduct.addItem('blaster : '+str(item.blaster))
                try:
                    self.listProduct.addItem('location : '+str(item.location.ID))
                except:
                    self.listProduct.addItem('location : '+str(item.location))
            elif isinstance(item,cl.shipment):
                self.listProduct.addItem('ID : '+str(item.ID))
                self.listProduct.addItem('source : '+str(item.source))
                self.listProduct.addItem('flavor : '+str(item.flavor))
                self.listProduct.addItem('date in : '+str(item.dateIn))
                self.listProduct.addItem('test results : '+str(item.testResults))
                bags = []
                for i in item.bags:
                    bags.append(str(i.ID))
                self.listProduct.addItem('bags recieved : '+str(bags))
                self.listProduct.addItem('total weight : '+str(item.totalWeight))
                self.listProduct.addItem('total price : '+str(item.totalPrice))
            elif isinstance(item,cl.container):
                self.listProduct.addItem('ID : '+str(item.ID))
                self.listProduct.addItem('kind : '+str(item.kind))
                self.listProduct.addItem('weight : '+str(item.weight))
                self.listProduct.addItem('# of units : '+str(item.numberOfUnits))
                self.listProduct.addItem('unit size : '+str(item.unitSize))
                self.listProduct.addItem('history : '+str(item.history))
                try:
                    self.listProduct.addItem('location : '+str(item.location.ID))
                except:
                    self.listProduct.addItem('location : '+str(item.location))
                prod = []
                for i in item.productIncluded:
                    prod.append(str(i.ID))
                self.listProduct.addItem('product included : '+str(prod))
            elif isinstance(item,cl.location):
                self.listProduct.addItem('ITEMS IN '+str(item.ID))
                for i in item.items:
                    self.listProduct.addItem(str(i.kind)+' : '+str(i.ID))
        elif self.currentCategory != None:
            self.label.show()
            self.label.setText(self.currentCategory)
            for item in options[self.currentCategory]:
                if self.currentCategory == 'Runs':
                    runs = []
                    for i in cl.inv.listAllRuns:
                        for run in i[1]:
                            runs.append(run)
                    for i in runs:
                        self.listProduct.addItem(str(i.ID)+' : '+str(i.owner))
                if isinstance(item,cl.container):
                    self.listProduct.addItem(str(item.ID)+' : '+str(item.kind)+' : '+str(item.weight))
                elif isinstance(item,cl.finishedProduct):
                    self.listProduct.addItem(str(item.ID)+' : '+str(item.kind)+' : '+str(item.weight))
                elif isinstance(item,cl.trimTote):
                    self.listProduct.addItem(str(item.ID)+' : '+str(item.trimWeight)+' : '+str(item.owner))
                elif isinstance(item,cl.unfinishedProduct):
                    self.listProduct.addItem(str(item.ID)+' : '+str(item.intendedFinish))
                #elif isinstance(item,cl.run):
                #    self.listProduct.addItem(str(item.ID)+' : '+str(item.owner))
                elif isinstance(item,cl.shipment):
                    self.listProduct.addItem(str(item.ID)+' : '+str(item.source)+' : '+str(item.dateIn))
                elif isinstance(item,cl.location):
                    self.listProduct.addItem(str(item.ID)+' : '+str(item.description))

def logClose():
    app.quit()
    #lg.write('Terminating Session...')
    #lg.close()
    subprocess.call('python SDOM.pyw', shell=True)
    
import atexit
atexit.register(logClose)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())

    #Create Base Windows
    sw = SearchWindow()
    

    #Display Start
    sw.show()

    sys.exit(app.exec_())
