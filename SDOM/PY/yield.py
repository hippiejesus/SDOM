#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import classes as cl
import time
import re
import sys
from PyQt4 import QtGui, QtCore, uic

Crumble = []
Crystal = []
Resin = []
Distillate = []

class YieldWindow(QtGui.QMainWindow):
    def __init__(self):
        super(YieldWindow, self).__init__()
        uic.loadUi(cl.UIstem+'yieldMain.ui', self)
        
        self.actionCrumble_Goo.triggered.connect(self.crumGoo)
        self.actionCrystals.triggered.connect(self.crystals)
        self.actionLive_Resin.triggered.connect(self.resin)
        self.actionDistillate.triggered.connect(self.distillate)
        self.actionQuit.triggered.connect(self.exitProgram)
        
        self.update()
        
    def exitProgram(self):
        sys.exit()
        
    def crumGoo(self):
        yieldP.update('Crumble')
        yieldP.show()
    def crystals(self):
        yieldP.update('Crystal')
        yieldP.show()
    def resin(self):
        yieldP.update('Resin')
        yieldP.show()
    def distillate(self):
        yieldP.update('Distillate')
        yieldP.show()
        
    def update(self):
        global Crumble,Crystal,Resin,Distillate
        Crumble = []
        Crystal = []
        Resin = []
        Distillate = []
        cl.load()
        
        self.listDisto.clear() ; self.listCrum.clear()
        self.listCry.clear() ; self.listLive.clear()
        
        print(cl.inv.listAllUnfinishedProduct)
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

class YieldPOP(QtGui.QDialog):
    def __init__(self):
        super(YieldPOP, self).__init__()
        uic.loadUi(cl.UIstem+'yieldPOP.ui', self)
        
        self.ok.clicked.connect(self.okPress)
        
    def okPress(self):
        finished = cl.finishedProduct()
        finished.ID = self.target_product.ID
        finished.weight = float(self.totalYield.text())
        finished.kind = self.kind
        finished.unfinishedProductIncluded.append(self.target_product)
        cl.inv.listAllUnfinishedProduct.pop(cl.inv.listAllUnfinishedProduct.index(self.target_product))
        cl.inv.listAllFinishedProduct.append(finished)
        
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
            target_container = newContainer
        target_container.productIncluded.append(finished)
        finished.container = target_container
        target_container.weight += finished.weight
        
        
        cl.save()
        yieldW.update()
        self.hide()
        
        
        
    def update(self,kind):
        global Crumble,Crystal,Resin,Distillate
        if kind == 'Crumble':
            self.target_product = Crumble[yieldW.listCrum.currentRow()]
        elif kind == 'Crystal':
            self.target_product = Crystal[yieldW.listCry.currentRow()]
        elif kind == 'Resin':
            self.target_product = Resin[yieldW.listLive.currentRow()]
        elif kind == 'Distillate':
            self.target_product = Distillate[yieldW.listDisto.currentRow()]
        else: print('Damn')
        self.kind = kind
        self.label.setText(str(self.target_product.ID))
        self.totalYield.clear()
        self.container.clear()
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    #Create Base Windows
    yieldW = YieldWindow()
    yieldP = YieldPOP()

    #Display Start
    yieldW.show()

    sys.exit(app.exec_())
