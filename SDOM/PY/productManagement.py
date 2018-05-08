#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import classes as cl
import time
import re
import sys
from PyQt4 import QtGui, QtCore, uic

CrumbleB = []
CrystalB = []
ResinB = []
DistillateB = []

class ProductWindow(QtGui.QMainWindow):
    def __init__(self):
        super(ProductWindow, self).__init__()
        uic.loadUi(cl.UIstem+'productManagement.ui', self)
        
        self.actionDistolate.triggered.connect(self.sd) #DISTILLATE
        self.actionPackaging.triggered.connect(self.sp) #PACKAGING
        self.actionPOS.triggered.connect(self.ss) #SALES

        self.update()

    def sd(self):
        self.send('(D)')
        
    def sp(self):
        self.send('(P)')
        
    def ss(self):
        self.send('(S)')

    def send(self,whereTo):
        target = ''
        options = ['Distillate','Crumble/Goo','Live Resin', 'Crystals']
        inn, ok = QtGui.QInputDialog.getItem(self,'From where?','From Which Type?:',options)
        if ok:
            if str(inn) == 'Distillate':
                target = DistillateB[self.listDistoBulk.currentRow()]
            elif str(inn) == 'Crumble/Goo':
                target = CrumbleB[self.listCrumBulk.currentRow()]
            elif str(inn) == 'Live Resin':
                target = ResinB[self.listLiveBulk.currentRow()]
            elif str(inn) == 'Crystals':
                target = CrystalB[self.listCryBulk.currentRow()]
                
            target.kind = whereTo+target.kind
            
            cl.save()
            
            self.update()

    def update(self):
        global CrumbleB,CrystalB,ResinB,DistillateB
        CrumbleB = []
        CrystalB = []
        ResinB = []
        DistillateB = []
        cl.load()
        
        self.listDistoBulk.clear() ; self.listCrumBulk.clear()
        self.listCryBulk.clear() ; self.listLiveBulk.clear()
        
        print(cl.inv.listAllContainers)
        for item in cl.inv.listAllContainers:
            print(item.ID+' : '+item.kind)
        for item in cl.inv.listAllContainers:
            if item.kind == 'Crumble':
                self.listCrumBulk.addItem(item.ID)
                CrumbleB.append(item)
            elif item.kind == 'Crystal':
                self.listCryBulk.addItem(item.ID)
                CrystalB.append(item)
            elif item.kind == 'Resin':
                self.listLiveBulk.addItem(item.ID)
                ResinB.append(item)
            elif item.kind == 'Distillate':
                self.listDistoBulk.addItem(item.ID)
                DistillateB.append(item)

if __name__ == '__main__':
#def begin():
    app = QtGui.QApplication(sys.argv)

    #Create Base Windows
    pm = ProductWindow()

    #Display Start
    pm.show()

    sys.exit(app.exec_())
