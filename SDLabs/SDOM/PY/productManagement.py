#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import classes as cl
import time
import re
import logger
import qdarkstyle
import sys
import subprocess
from PyQt4 import QtGui, QtCore, uic

CrumbleB = []
CrystalB = []
ResinB = []
DistillateB = []
RSOB = []
CrudeB = []

CrumbleP = []
CrystalP = []
ResinP = []
DistillateP = []
RSOP = []
CrudeP = []

class ProductWindow(QtGui.QMainWindow):
    def __init__(self):
        super(ProductWindow, self).__init__()
        uic.loadUi(cl.UIstem+'productManagement.ui', self)
        
        self.kinds ={'Crumble':self.listCrumBulk,
                     'Crystals':self.listCryBulk,
                     'Distillate':self.listDistoBulk,
                     'Resin':self.listLiveBulk,
                     'RSO':self.listRsoptBulk,
                     'Crude':self.listCrudeBulk}
                     
        self.kinds2 ={'Crumble':self.listCrumUnit,
                      'Crystals':self.listCryUnit,
                      'Distillate':self.listDistoUnit,
                      'Resin':self.listLiveUnit,
                      'RSO':self.listRsoptUnit,
                      'Crude':self.listCrudeUnit}
                      
        self.comboList = []
        
        self.actionDistolate.triggered.connect(lambda: self.send('(D)')) #DISTILLATE
        self.actionPackaging.triggered.connect(lambda: self.send('(P)')) #PACKAGING
        self.actionPOS.triggered.connect(lambda: self.send('(S)')) #SALES

        self.listDistoBulk.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listDistoBulk))
        self.listCrumBulk.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCrumBulk))
        self.listLiveBulk.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listLiveBulk))
        self.listCryBulk.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCryBulk))
        self.listRsoptBulk.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listRsoptBulk))
        self.listCrudeBulk.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCrudeBulk))
        
        self.listDistoUnit.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listDistoUnit))
        self.listCrumUnit.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCrumUnit))
        self.listLiveUnit.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listLiveUnit))
        self.listCryUnit.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCryUnit))
        self.listRsoptUnit.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listRsoptUnit))
        self.listCrudeUnit.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCrudeUnit))
        
        self.listDistoBulk.itemDoubleClicked.connect(self.itemView)
        self.listCrumBulk.itemDoubleClicked.connect(self.itemView)
        self.listLiveBulk.itemDoubleClicked.connect(self.itemView)
        self.listCryBulk.itemDoubleClicked.connect(self.itemView)
        self.listRsoptBulk.itemDoubleClicked.connect(self.itemView)
        self.listCrudeBulk.itemDoubleClicked.connect(self.itemView)
        
        self.listDistoUnit.itemDoubleClicked.connect(self.itemView)
        self.listCrumUnit.itemDoubleClicked.connect(self.itemView)
        self.listLiveUnit.itemDoubleClicked.connect(self.itemView)
        self.listCryUnit.itemDoubleClicked.connect(self.itemView)
        self.listRsoptUnit.itemDoubleClicked.connect(self.itemView)
        self.listCrudeUnit.itemDoubleClicked.connect(self.itemView)
        
        self.actionQuit.triggered.connect(self.quitApp)
        self.actionSave.triggered.connect(self.save)
        
        
        self.update()
        
        '''self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py'))
        self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        #self.actionProduct_Management.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        self.actionPackaging_2.triggered.connect(lambda: self.pageOpen('packaging.py'))
        self.actionDistillate.triggered.connect(lambda: self.pageOpen('distillate.py'))
        self.actionPOS_2.triggered.connect(lambda: self.pageOpen('pos.py'))'''
        
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
        
    def itemView(self,item):
        for kind in self.kinds.values() + self.kinds2.values():
            current = kind.currentItem()
            print kind.currentItem()
            if current != None:
                for product in self.comboList:
                    if str(product.ID) + ' : ' + str(product.weight) == str(item.text()) or str(product.ID) + ' : ' + str(product.numberOfUnits) == str(item.text()):
                        if kind == self.listDistoBulk: target = DistillateB[self.listDistoBulk.currentRow()]
                        elif kind == self.listCrumBulk: target = CrumbleB[self.listCrumBulk.currentRow()]
                        elif kind == self.listLiveBulk: target = ResinB[self.listLiveBulk.currentRow()]
                        elif kind == self.listCryBulk: target = CrystalB[self.listCryBulk.currentRow()]
                        elif kind == self.listRsoptBulk: target = RSOB[self.listRsoptBulk.currentRow()]
                        elif kind == self.listCrudeBulk: target = CrudeB[self.listCrudeBulk.currentRow()]
                        elif kind == self.listDistoUnit: target = DistillateP[self.listDistoUnit.currentRow()]
                        elif kind == self.listCrumUnit: target = CrumbleP[self.listCrumUnit.currentRow()]
                        elif kind == self.listLiveUnit: target = ResinP[self.listLiveUnit.currentRow()]
                        elif kind == self.listCryUnit: target = CrystalP[self.listCryUnit.currentRow()]
                        elif kind == self.listRsoptUnit: target = RSOP[self.listRsoptUnit.currentRow()]
                        elif kind == self.listCrudeUnit: target = CrudeP[self.listCrudeUnit.currentRow()]
                
        view.setContainer(target)
        view.show()
        
        
    def save(self):
        cl.save()
        self.update()
        
    def quitApp(self):
        app.quit()
        self.hide()
        
    def uncheckLists(self,avoidList):
        
        #if avoidList in self.kinds.values(): target = self.kinds.values()
        #elif avoidList in self.kinds2.values(): target = self.kinds2.values()
        target = self.kinds.values() + self.kinds2.values()
        for kind in target:
            item = kind
            current = item.currentItem()
            if current != None and item is not avoidList:
                current.setSelected(False)
                kind.setCurrentItem(None)

    def send(self,whereTo):
        target = None    
        for kind in self.kinds.values() + self.kinds2.values():
            current = kind.currentItem()
            print kind.currentItem()
            if current != None:
                for product in self.comboList:
                    if str(product.ID) + ' : ' + str(product.weight) == str(current.text()) or str(product.ID) + ' : ' + str(product.numberOfUnits) == str(current.text()):
                        if kind == self.listDistoBulk: target = DistillateB[self.listDistoBulk.currentRow()]
                        elif kind == self.listCrumBulk: target = CrumbleB[self.listCrumBulk.currentRow()]
                        elif kind == self.listLiveBulk: target = ResinB[self.listLiveBulk.currentRow()]
                        elif kind == self.listCryBulk: target = CrystalB[self.listCryBulk.currentRow()]
                        elif kind == self.listRsoptBulk: target = RSOB[self.listRsoptBulk.currentRow()]
                        elif kind == self.listCrudeBulk: target = CrudeB[self.listCrudeBulk.currentRow()]
                        elif kind == self.listDistoUnit: target = DistillateP[self.listDistoUnit.currentRow()]
                        elif kind == self.listCrumUnit: target = CrumbleP[self.listCrumUnit.currentRow()]
                        elif kind == self.listLiveUnit: target = ResinP[self.listLiveUnit.currentRow()]
                        elif kind == self.listCryUnit: target = CrystalP[self.listCryUnit.currentRow()]
                        elif kind == self.listRsoptUnit: target = RSOP[self.listRsoptUnit.currentRow()]
                        elif kind == self.listCrudeUnit: target = CrudeP[self.listCrudeUnit.currentRow()]
             
            
        if target != None: target.kind = whereTo+target.kind

    def update(self):
        global CrumbleB,CrystalB,ResinB,DistillateB,RSOB,CrudeB, CrumbleP,CrystalP,ResinP,DistillateP,RSOP,CrudeP
        CrumbleB = []
        CrystalB = []
        ResinB = []
        DistillateB = []
        RSOB = []
        CrudeB = []
        
        CrumbleP = []
        CrystalP = []
        ResinP = []
        DistillateP = []
        RSOP = []
        CrudeP = []
        cl.load()
        
        for i in self.kinds.values() + self.kinds2.values():
            i.clear()
        
        print(cl.inv.listAllContainers)
        for item in cl.inv.listAllContainers:
            print(item.ID+' : '+item.kind)
        for item in cl.inv.listAllContainers:
            if item.weight <= 0.00: item.kind = 'finished'
            if item.kind == 'Crumble':
                if item.isPackaged:
                    self.listCrumUnit.addItem(item.ID+' : '+str(item.numberOfUnits))
                    CrumbleP.append(item)
                else:
                    self.listCrumBulk.addItem(item.ID+' : '+str(item.weight))
                    CrumbleB.append(item)
            elif item.kind == 'Crystal':
                if item.isPackaged:
                    self.listCryUnit.addItem(item.ID+' : '+str(item.numberOfUnits))
                    CrystalP.append(item)
                else:
                    self.listCryBulk.addItem(item.ID+' : '+str(item.weight))
                    CrystalB.append(item)
            elif item.kind == 'Resin':
                if item.isPackaged:
                    self.listLiveUnit.addItem(item.ID+' : '+str(item.numberOfUnits))
                    ResinP.append(item)
                else:
                    self.listLiveBulk.addItem(item.ID+' : '+str(item.weight))
                    ResinB.append(item)
            elif item.kind == 'Distillate':
                if item.isPackaged:
                    self.listDistoUnit.addItem(item.ID+' : '+str(item.numberOfUnits))
                    DistillateP.append(item)
                else:
                    self.listDistoBulk.addItem(item.ID+' : '+str(item.weight))
                    DistillateB.append(item)
            elif item.kind == 'RSO':
                if item.isPackaged:
                    self.listRsoptUnit.addItem(item.ID+' : '+str(item.numberOfUnits))
                    RSOP.append(item)
                else:
                    self.listRsoptBulk.addItem(item.ID+' : '+str(item.weight))
                    RSOB.append(item)
            elif item.kind == 'Crude':
                if item.isPackaged:
                    self.listCrudeUnit.addItem(item.ID+' : '+str(item.numberOfUnits))
                    CrudeP.append(item)
                else:
                    self.listCrudeBulk.addItem(item.ID+' : '+str(item.weight))
                    CrudeB.append(item)
            self.comboList.append(item)

class ViewWindow(QtGui.QDialog):
    def __init__(self):
        super(ViewWindow, self).__init__()
        uic.loadUi(cl.UIstem+'productManagementView.ui', self)
        
    def setContainer(self,product):
        self.listHistory.clear()
        self.labelContainerName.setText(str(product.ID))
        startWeight = 0.00
        for i in product.productIncluded:
            startWeight += i.weight
            
        self.labelStartWeight.setText(str(startWeight))
        for i in product.history:
            self.listHistory.addItem(str(i))
        self.lineCurrentWeight.setText(str(product.weight))
        companyName = str(product.productIncluded[0].unfinishedProductIncluded[0].runsIncluded[0].owner)
        print companyName
        self.labelCompanyName.setText(companyName)
        
def logClose():
    app.quit()
    lg.write('Terminating Session...')
    lg.close()
    
import atexit
atexit.register(logClose)

if __name__ == '__main__':
    #def begin():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())
    
    try:
        lg = logger.log('productManagement')
        lg.write('Logging session begin...',deepData='begin_')
    except:
        print('Logger failure...\n'+str(sys.exc_info()))
        sys.exit()

    #Create Base Windows
    try:
        pm = ProductWindow()
        lg.write('ProductWindow initialized...')
    except:
        lg.write('ProductWindow - initialization error...\n'+str(sys.exc_info()))
        
    try:
        view = ViewWindow()
        lg.write('ViewWindow initialized...')
    except:
        lg.write('ProductWindow - initialization error...\n'+str(sys.exc_info()))

    #Display Start
    pm.show()

    sys.exit(app.exec_())
