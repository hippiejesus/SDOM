#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import classes as cl
import time
import re
import sys
from PyQt4 import QtGui, QtCore, uic

class FinishWindow(QtGui.QMainWindow):
    def __init__(self):
        super(FinishWindow, self).__init__()
        uic.loadUi(cl.UIstem+'finishingMain.ui', self)
        self.listToBe.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.changeDat = {}
        self.finishingList = []
        
        self.update()
                    
        print(self.changeDat)
        
        self.actionGroup_Selected.triggered.connect(self.group)
        self.actionCrumble_Goo.triggered.connect(self.crumGoo)
        self.actionLive_Resin.triggered.connect(self.liveRes)
        self.actionCrystals.triggered.connect(self.crystal)
        self.actionCrystals_2.triggered.connect(self.closeCrystal)
        self.actionLive_Resin_2.triggered.connect(self.closeLiveResin)
        self.actionCrum_Goo.triggered.connect(self.closeCrumGoo)
        self.actionQuit.triggered.connect(self.quitnow)
        
    def quitnow(self):
        sys.exit()
        
    def update(self):
        cl.load()
        
        self.listToBe.clear() ; self.listCrumFin.clear()
        self.listCry.clear() ; self.listLRFin.clear()
        print(cl.inv.listAllUnfinishedProduct)
        for item in cl.inv.listAllUnfinishedProduct:
            if item.intendedFinish == '':
                self.listToBe.addItem(item.ID)
            elif item.intendedFinish == 'Crumble':
                self.listCrumFin.addItem(item.ID)
            elif item.intendedFinish == 'Crystal':
                self.listCry.addItem(item.ID)
            elif item.intendedFinish == 'Resin':
                self.listLRFin.addItem(item.ID)
            self.finishingList.append(item)
        
    def crumGoo(self):
        self.sendTo('Crumble',self.listToBe) 
                
    def liveRes(self):
        self.sendTo('Resin',self.listToBe)
        
    def crystal(self):
        self.sendTo('Crystal',self.listToBe)
        
    def closeCrystal(self):
        self.sendTo('(C)Crystal',self.listCry)
        
    def closeCrumGoo(self):
        self.sendTo('(C)Crumble',self.listCrumFin)
        
    def closeLiveResin(self):
        self.sendTo('(C)Resin',self.listLRFin)
                
    def sendTo(self,target,fromT):
        ilist = fromT.selectedItems()
        items = []
        for item in ilist:
            for i in self.finishingList:
                if str(i.ID) == str(item.text()):
                    i.intendedFinish = target
        cl.save()
        self.update()
            
        
    def group(self):
        ilist = self.listToBe.selectedItems()
        tlist = []
        flist = []
        nums = []
        changeList = self.changeDat.copy() 
        combo = cl.unfinishedProduct()
        for item in ilist:
            print(str(item.text()))
            for i in self.finishingList:
                if str(i.ID) == str(item.text()):
                    cl.inv.listAllUnfinishedProduct.pop(cl.inv.listAllUnfinishedProduct.index(i))
                    tlist.append(i.ID)
                    combo.runsIncluded.append(i)
                else: flist.append(i)
        combo.ID = tlist[0]
        tlist.pop(0)
        for item in tlist:
            combo.ID += "/"+item[-1]
        cl.inv.listAllUnfinishedProduct.append(combo)
        self.finishingList = flist[:]
        cl.save()
        self.update()
            
        
if __name__ == '__main__':
#def begin():
    app = QtGui.QApplication(sys.argv)

    #Create Base Windows
    finish = FinishWindow()

    #Display Start
    finish.show()

    sys.exit(app.exec_())
