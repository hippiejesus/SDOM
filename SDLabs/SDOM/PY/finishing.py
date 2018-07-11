#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import classes as cl
import logger
import qdarkstyle
import time
import re
import sys
import copy
import subprocess
from PyQt4 import QtGui, QtCore, uic

class FinishWindow(QtGui.QMainWindow):
    def __init__(self):
        super(FinishWindow, self).__init__()
        uic.loadUi(cl.UIstem+'finishingMain.ui', self)
        self.listToBe.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.changeDat = {}
        self.finishingList = []
        
        self.kinds = {'Crumble':self.listCrumFin,'Crystal':self.listCry,'Resin':self.listLRFin,'':self.listToBe,'Crude':self.listCrudeFin}
        
        self.update()
                    
        print(self.changeDat)
        
        self.actionGroup_Selected.triggered.connect(self.group)
        self.actionCrumble_Goo.triggered.connect(self.crumGoo)
        self.actionCrude.triggered.connect(self.crude)
        self.actionLive_Resin.triggered.connect(self.liveRes)
        self.actionCrystals.triggered.connect(self.crystal)
        
        """self.actionCrystals_2.triggered.connect(self.closeCrystal)
        self.actionLive_Resin_2.triggered.connect(self.closeLiveResin)
        self.actionCrum_Goo.triggered.connect(self.closeCrumGoo)"""
        
        
        self.actionQuit.triggered.connect(self.quitnow)
        self.actionHarvest_2.triggered.connect(self.harvestCrystals)
        
        '''self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py'))
        self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        #self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        self.actionProduct_Management.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        self.actionPackaging.triggered.connect(lambda: self.pageOpen('packaging.py'))
        self.actionDistillate.triggered.connect(lambda: self.pageOpen('distillate.py'))
        self.actionPOS.triggered.connect(lambda: self.pageOpen('pos.py'))'''
        
        self.listCrudeFin.itemDoubleClicked.connect(self.closeCrude)
        self.listCrumFin.itemDoubleClicked.connect(self.closeCrumGoo)
        self.listCry.itemDoubleClicked.connect(self.closeCrystal)
        self.listLRFin.itemDoubleClicked.connect(self.closeLiveResin)
        
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
        
    def quitnow(self):
        app.quit()
        self.hide()
        
    def update(self):
        try:
            cl.load()
            self.finishingList = []
        
            self.listToBe.clear() ; self.listCrumFin.clear()
            self.listCry.clear() ; self.listLRFin.clear()
            self.listCrudeFin.clear()
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
                elif item.intendedFinish == 'Crude':
                    self.listCrudeFin.addItem(item.ID)
                self.finishingList.append(item)
            lg.write('FinishWindow - finishingList populated...',deepData=self.finishingList)
        except:
            lg.write('FinishWindow - ERROR: update(self)',deepData=str(sys.exc_info()))
        
    def crude(self):
        try:
            self.sendTo('Crude',self.listToBe)
        except:
            lg.write('FinishWindow - ERROR: crude(self)',deepData=str(sys.exc_info()))
        
    def crumGoo(self):
        try:
            self.sendTo('Crumble',self.listToBe)
        except:
            lg.write('FinishWindow - ERROR: crumGoo(self)',deepData=str(sys.exc_info()))
                
    def liveRes(self):
        try:
            self.sendTo('Resin',self.listToBe)
        except:
            lg.write('FinishWindow - ERROR: liveRes(self)',deepData=str(sys.exc_info()))
        
    def crystal(self):
        try:
            self.sendTo('Crystal',self.listToBe)
        except:
            lg.write('FinishWindow - ERROR: crystal(self)',deepData=str(sys.exc_info()))
        
    def closeCrystal(self):
        try:
            self.sendTo('(C)Crystal',self.listCry)
        except:
            lg.write('FinishWindow - ERROR: closeCrystal(self)',deepData=str(sys.exc_info()))
        
    def closeCrumGoo(self):
        try:
            self.sendTo('(C)Crumble',self.listCrumFin)
        except:
            lg.write('FinishWindow - ERROR: closeCrumGoo(self)',deepData=str(sys.exc_info()))
        
    def closeLiveResin(self):
        try:
            self.sendTo('(C)Resin',self.listLRFin)
        except:
            lg.write('FinishWindow - ERROR: closeLiveResin(self)',deepData=str(sys.exc_info()))
            
    def closeCrude(self):
        try:
            self.sendTo('(C)Crude',self.listCrudeFin)
        except:
            lg.write('FinishWindow - ERROR: closeCrude(self)',deepData=str(sys.exc_info()))
                
    def sendTo(self,target,fromT):
        try:
            if '(C)' in target:
                message = 'Close '
            else: message = 'Finish '
            inn = QtGui.QMessageBox.question(self,'Really?',message+str(target)+'?',
                                                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if inn == QtGui.QMessageBox.Yes:
                ilist = fromT.selectedItems()
                items = []
                for item in ilist:
                    for i in self.finishingList:
                        if str(i.ID) == str(item.text()):
                            i.intendedFinish = target
                cl.save()
                self.update()
                lg.write('FinishWindow - '+target+' --> product transfered...',deepData=ilist)
        except:
            lg.write('FinishWindow - ERROR: sendTo(self,target,fromT)',deepData=str(sys.exc_info()))
            
    
    def harvestCrystals(self):
        try:
            lg.write('FinishWindow - harvesting crystals...')
            listItem = self.listCry.selectedItems()
            targetSource = ''
            for item in listItem:
                for i in self.finishingList:
                    if str(i.ID) == str(item.text()):
                        targetSource = i
            targetSource.intendedFinish = ''
            resinToBe = copy.deepcopy(targetSource)
            resinToBe.ID +='R'
            targetSource.ID += 'C'
            cl.inv.listAllUnfinishedProduct.append(resinToBe)
            cl.inv.listAllUnfinishedProductArchive.append(resinToBe)
            cl.save()
            self.update()
            lg.write('FinishWindow - crystals harvested...',deepData=targetSource.ID)
        except:
            lg.write('FinishWindow - ERROR: harvestCrystals(self)',deepData=str(sys.exc_info()))
            
        
    def group(self):
        try:
            lg.write('FinishWindow - attempting group...')
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
                        combo.owner = i.owner
                        combo.location = i.location
                        i.location.items.pop(i.location.items.index(i))
                    else: flist.append(i)
            combo.ID = str(tlist[0])
            combo.location.items.append(combo)
            tlist.pop(0)
            for item in tlist:
                splitCombo = combo.ID.split('-')
                splitItem = item.split('-')
                targetCombo = splitCombo[0]+'-'+splitCombo[1]
                targetItem = splitItem[0]+'-'+splitItem[1]
                print targetCombo
                print targetItem
                if targetCombo == targetItem:
                    combo.ID += "/"+item[-1]
                else:
                    combo.ID += "/"+item
            cl.inv.listAllUnfinishedProduct.append(combo)
            cl.inv.listAllUnfinishedProductArchive.append(combo)
            self.finishingList = flist[:]
            cl.save()
            self.update()
            lg.write('FinishWindow - group successful...',deepData=combo)
        except:
            lg.write('FinishWindow - ERROR: group(self)',deepData=str(sys.exc_info()))
            
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
        lg = logger.log('finishing')
        lg.write('Logging session begin...',deepData='begin_')
    except:
        print('Logger failure...')
        sys.exit()

    #Create Base Windows
    try:
        finish = FinishWindow()
        lg.write('FinishWindow initialized...')
    except:
        lg.write('FinishWindow error...')

    #Display Start
    finish.show()

    sys.exit(app.exec_())
