#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import classes as cl
import datetime
import qdarkstyle
import re
import csv
import sys
import subprocess
from PyQt4 import QtGui, QtCore, uic

Crude = []
Distillate = []

class DistillateWindow(QtGui.QMainWindow):
    def __init__(self):
        super(DistillateWindow, self).__init__()
        uic.loadUi(cl.UIstem+'distillate.ui', self)
        
        self.actionNew.triggered.connect(self.new)
        self.actionExit.triggered.connect(self.endProgram)
        self.actionStart_Run.triggered.connect(self.startRun)
        self.actionSave_2.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.openF)
        
        self.runSource = ''
        
        self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py'))
        self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        self.actionProduct_Management.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        self.actionPackaging.triggered.connect(lambda: self.pageOpen('packaging.py'))
        #self.actionDistillate.triggered.connect(lambda: self.pageOpen('distillate.py'))
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
        subprocess.call('python '+page, shell=True)
        
    def save(self):
        self.runSource.intendedFinish = '(C)Distillate'
        
        
        path = QtGui.QFileDialog.getSaveFileName(self,'Save File','','CSV(*.csv)')
        if not path.isEmpty():
            with open(unicode(path),'wb') as stream:
                writer = csv.writer(stream)
                for row in range(self.tableWidget.rowCount()):
                    rowdata = []
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row,column)
                        if item is not None:
                            rowdata.append(unicode(item.text()).encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
                writer.writerow([self.runSource,'','','','','','','','',''])
        cl.save()
        
    def openF(self):
        path = QtGui.QFileDialog.getOpenFileName(self,'Open File','','CSV(*.csv)')
        if not path.isEmpty():
            with open(unicode(path),'rb') as stream:
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(0)
                for rowdata in csv.reader(stream):
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    self.tableWidget.setColumnCount(len(rowdata))
                    for column, data in enumerate(rowdata):
                        item = QtGui.QTableWidgetItem(data.decode('utf8'))
                        self.tableWidget.setItem(row,column,item)
        
        
    def startRun(self):
        cl.load()
        target_list = cl.inv.listAllUnfinishedProduct
        options = []
        optionsID = []
        for item in target_list:
            if item.intendedFinish == 'Distillate':
                options.append(item)
                optionsID.append(item.ID)
                
        inn, ok = QtGui.QInputDialog.getItem(self,'Choose','Choose source:',optionsID)
        if ok:
            target = options[optionsID.index(inn)]
            self.listWidget.clear()
            self.listWidget.addItem('Date/Time: '+str(datetime.datetime.now()))
            self.listWidget.addItem('Run ID: '+str(target.ID))
            self.runSource = target
            self.listWidget.addItem('Start Weight: '+str(target.weight))
                
        
    def endProgram(self):
        app.quit()
        self.hide()
        
    def new(self):
        options = ['Crude','Distillate']
        inn, ok = QtGui.QInputDialog.getItem(self,'Choose','Choose source type:',options)
        if ok:
            newW.setType(str(inn))
            newW.show()
            
        
        newW.show()
        
        
        
class NewWindow(QtGui.QDialog):
    def __init__(self):
        super(NewWindow, self).__init__()
        uic.loadUi(cl.UIstem+'distillateNew.ui', self)

        self.sourceType = 'Crude'
        self.sourceList = []
        self.crudeList = []
        self.distillateList = []
        
        self.lineCurrentWeight.textChanged.connect(self.calculateUsed)
        self.productBox.currentIndexChanged.connect(self.setWeight)
        
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        
        self.loadOptions()
        
    def setWeight(self):
        if self.sourceType == 'Crude': tlist = self.crudeList
        else: tlist = self.distillateList
        
        for item in tlist:
            if item.ID == str(self.productBox.currentText()):
                self.lineStartWeight.setText(str(item.weight))
        
    def calculateUsed(self):
        x = float(self.lineCurrentWeight.text())
        y = float(self.lineStartWeight.text())
        z = y-x
        self.lineWeightUsed.setText(str(z))
        
    def cancelPressed(self):
        self.hide()
        self.lineStartWeight.clear()
        self.lineID.clear()
        self.lineWeightUsed.clear()
        self.lineCurrentWeight.clear()
        
    def okPressed(self):
        target_container = ''
        if self.sourceType == 'Crude':
            target_container = self.crudeList[self.productBox.currentIndex()]
        elif self.sourceType == 'Distillate':
            target_container = self.distillateList[self.productBox.currentIndex()]
        weight = float(self.lineWeightUsed.text())
        
        newProduct = cl.unfinishedProduct()
        newProduct.intendedFinish = 'Distillate'
        newProduct.owner = target_container.productIncluded[0].unfinishedProductIncluded[0].owner
        runs = []
        for product in target_container.productIncluded:
            for unfinishedProduct in product.unfinishedProductIncluded:
                for run in unfinishedProduct.runsIncluded:
                    runs.append(run)
        for run in runs:
            newProduct.runsIncluded.append(run)
        newProduct.ID = str(self.lineID.text())
        newProduct.weight = weight
        
        cl.inv.listAllUnfinishedProduct.append(newProduct)
        
        target_container.weight -= weight
        if target_container.weight <= 0:
            tlist = cl.inv.listAllContainers
            tlist.pop(tlist.index(target_container))
            if self.sourceType == 'Crude':
                self.crudeList.pop(self.crudeList.index(target_container))
            elif self.sourceType == 'Distillate':
                self.distillateList.pop(self.distillateList.index(target_container))
        
        cl.save()
        self.hide()
        
    def setType(self, inn):
        self.sourceType = inn
        self.productBox.clear()
        if self.sourceType == 'Crude':
            self.sourceList = self.crudeList[:]
        elif self.sourceType == 'Distillate':
            self.sourceList = self.distillateList[:]
            
        self.productBox.clear()
        for item in self.sourceList:
            self.productBox.addItem(item.ID)
        self.setWeight()
        
    def loadOptions(self):
        cl.load()
        preSourceList = cl.inv.listAllContainers[:]
        for item in preSourceList:
            if '(D)' in item.kind:
                self.crudeList.append(item)
            if 'Distillate' in item.kind:
                self.distillateList.append(item)
                

def logClose():
    app.quit()
    #lg.write('Terminating Session...')
    #lg.close()
    
import atexit
atexit.register(logClose)


if __name__ == '__main__':
#def begin():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())

    #Create Base Windows
    distillateW = DistillateWindow()
    newW = NewWindow()
    

    #Display Start
    distillateW.show()

    sys.exit(app.exec_())
