#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import classes as cl
import logger
import qdarkstyle
import time
import re
import sys
import datetime
import subprocess
from PyQt4 import QtGui, QtCore, uic

Crumble = []
Crystal = []
Resin = []
Distillate = []
Crude = []

class YieldWindow(QtGui.QMainWindow):
    def __init__(self):
        super(YieldWindow, self).__init__()
        uic.loadUi(cl.UIstem+'yieldMain.ui', self)
        
        self.actionCrumble_Goo.triggered.connect(self.crumGoo)
        self.actionCrystals.triggered.connect(self.crystals)
        self.actionLive_Resin.triggered.connect(self.resin)
        self.actionDistillate.triggered.connect(self.distillate)
        
        self.actionQuit.triggered.connect(self.exitProgram)
        
        self.listCrude.itemDoubleClicked.connect(self.crude)
        self.listCrum.itemDoubleClicked.connect(self.crumGoo)
        self.listCry.itemDoubleClicked.connect(self.crystals)
        self.listLive.itemDoubleClicked.connect(self.resin)
        self.listDisto.itemDoubleClicked.connect(self.distillate)
        
        self.update()
        
        self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py'))
        self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        #self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        self.actionProduct_Management.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        self.actionPackaging.triggered.connect(lambda: self.pageOpen('packaging.py'))
        self.actionDistillate_2.triggered.connect(lambda: self.pageOpen('distillate.py'))
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
        
    def exitProgram(self):
        app.quit()
        self.hide()
        
    def crude(self):
        try:
            yieldP.update('Crude')
            yieldP.show()
            lg.write('YieldWindow - crude --> update recieved...')
        except:
            lg.write('YieldWindow - ERROR: crude(self)',deepData=str(sys.exc_info()))
        
    def crumGoo(self):
        try:
            yieldP.update('Crumble')
            yieldP.show()
            lg.write('YieldWindow - crumble --> update recieved...')
        except:
            lg.write('YieldWindow - ERROR: crumGoo(self)',deepData=str(sys.exc_info()))
    def crystals(self):
        try:
            yieldP.update('Crystal')
            yieldP.show()
            lg.write('YieldWindow - crystal --> update recieved...')
        except:
            lg.write('YieldWindow - ERROR: crystals(self)',deepData=str(sys.exc_info()))
    def resin(self):
        try:
            yieldP.update('Resin')
            yieldP.show()
            lg.write('YieldWindow - resin --> update recieved...')
        except:
            lg.write('YieldWindow - ERROR:resin(self)',deepData=str(sys.exc_info()))
    def distillate(self):
        try:
            yieldP.update('Distillate')
            yieldP.show()
            lg.write('YieldWindow - distillate --> update recieved...')
        except:
            lg.write('YieldWindow - ERROR: distillate(self)',deepData=str(sys.exc_info()))
        
    def update(self):
        global Crumble,Crystal,Resin,Distillate,Crude
        Crumble = []
        Crystal = []
        Resin = []
        Distillate = []
        Crude = []
        cl.load()
        
        self.listDisto.clear() ; self.listCrum.clear()
        self.listCry.clear() ; self.listLive.clear()
        self.listCrude.clear()
        
        print(cl.inv.listAllUnfinishedProduct)
        try:
            for item in cl.inv.listAllUnfinishedProduct:
                if item.intendedFinish == '(C)Crumble':
                    self.listCrum.addItem(item.ID)
                    Crumble.append(item)
                elif item.intendedFinish == '(C)Crystal':
                    self.listCry.addItem(item.ID)
                    Crystal.append(item)
                elif item.intendedFinish == '(C)Resin':
                    self.listLive.addItem(item.ID)
                    Resin.append(item)
                elif item.intendedFinish == '(C)Distillate':
                    self.listDisto.addItem(item.ID)
                    Distillate.append(item)
                elif item.intendedFinish == '(C)Crude':
                    self.listCrude.addItem(item.ID)
                    Crude.append(item)
            lg.write('YieldWindow - update complete...')
        except:
            lg.write('YieldWindow - ERROR: update(self)',deepData=str(sys.exc_info()))

class YieldPOP(QtGui.QDialog):
    def __init__(self):
        super(YieldPOP, self).__init__()
        uic.loadUi(cl.UIstem+'yieldPOP.ui', self)
        
        self.ok.clicked.connect(self.okPress)
        
    def okPress(self):
        try:
            finished = cl.finishedProduct()
            finished.ID = self.target_product.ID
            finished.weight = float(self.totalYield.text())
            finished.kind = self.kind
            finished.location = self.target_product.location
            self.target_product.location.items.pop(self.target_product.location.items.index(self.target_product))
            finished.owner = self.target_product.owner###
            finished.unfinishedProductIncluded.append(self.target_product)
            cl.inv.listAllUnfinishedProduct.pop(cl.inv.listAllUnfinishedProduct.index(self.target_product))
            cl.inv.listAllFinishedProduct.append(finished)
            cl.inv.listAllFinishedProductArchive.append(finished)
        
            target_container = str(self.container.text())
            found = False
            for item in cl.inv.listAllContainers:
                if str(item.ID) == target_container:
                    target_container = item
                    found = True
            if found == False: 
                newContainer = cl.container()
                newContainer.ID = target_container
                newContainer.kind = finished.kind
                cl.inv.listAllContainers.append(newContainer)
                cl.inv.listAllContainersArchive.append(newContainer)
                target_container = newContainer
            target_container.history.append([str(datetime.datetime.now()),'+',finished.weight,'yielded from '+str(finished.ID)])
            target_container.productIncluded.append(finished)
            finished.container = target_container
            target_container.weight += finished.weight
            
            optionList = []
            for i in cl.inv.listAllLocations:
                optionList.append(str(i.ID))
            inn2, ok = QtGui.QInputDialog.getItem(self,'Choose','Choose location to store:',optionList)
            if ok:
                for i in cl.inv.listAllLocations:
                    if str(i.ID) == inn2:
                        target_container.location = i
                        i.items.append(target_container)
            else: return
            
            try:
                cl.inv.ALLCONTAINERS.append(target_container)
            except:
                cl.inv.ALLCONTAINERS = [target_container]
        
        
            cl.save()
            yieldW.update()
            self.hide()
            lg.write('YieldPOP - product yielded...',deepData=finished)
        except:
            lg.write('YieldPOP - ERROR: okPress(self)',deepData=str(sys.exc_info()))
        
        
        
    def update(self,kind):
        global Crumble,Crystal,Resin,Distillate
        try:
            if kind == 'Crumble':
                self.target_product = Crumble[yieldW.listCrum.currentRow()]
            elif kind == 'Crystal':
                self.target_product = Crystal[yieldW.listCry.currentRow()]
            elif kind == 'Resin':
                self.target_product = Resin[yieldW.listLive.currentRow()]
            elif kind == 'Distillate':
                self.target_product = Distillate[yieldW.listDisto.currentRow()]
            elif kind == 'Crude':
                self.target_product = Crude[yieldW.listCrude.currentRow()]
            else: print('Damn')
            self.kind = kind
            self.label.setText(str(self.target_product.ID))
            self.totalYield.clear()
            self.container.clear()
            lg.write('YieldPOP - '+kind+' --> updating...')
        except:
            lg.write('YieldPOP - ERROR: update(self,kind)',deepData=str(sys.exc_info()))

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
        lg = logger.log('yield')
        lg.write('Logging session begin...',deepData='begin_')
    except:
        print('Logger failure...')
        sys.exit()

    #Create Base Windows
    try:
        yieldW = YieldWindow()
        lg.write('YieldWindow initialized...')
    except:
        lg.write('YieldWindow error...')
    try:
        yieldP = YieldPOP()
        lg.write('YieldPOP initialized...')
    except:
        lg.write('YieldPOP error...')

    #Display Start
    yieldW.show()

    sys.exit(app.exec_())
