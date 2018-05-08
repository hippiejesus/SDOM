#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os.path
import classes as cl
import time
import sys
from PyQt4 import QtGui, QtCore, uic

OpenBags = []
OpenRuns = []
CurrentNum = {}
currentDate = ''

class StartWindow(QtGui.QDialog):
    def __init__(self):
        super(StartWindow, self).__init__()
        uic.loadUi(cl.UIstem+'Start.ui', self)

        #Selection Options
        self.run.clicked.connect(self.runMan)
        self.review.clicked.connect(self.reviewMan)

    #Display Run Manager/Hide Start
    def runMan(self):
        self.hide()
        manager.show()

    #Display Review Logs/Hide Start
    def reviewMan(self):
        self.hide()
        review.show()


class ManagerWindow(QtGui.QMainWindow):
    def __init__(self):
        super(ManagerWindow, self).__init__()
        uic.loadUi(cl.UIstem+'Manager.ui', self)

        #Selection Options
        self.newBag.triggered.connect(self.bagStart)
        self.startRun.triggered.connect(self.runStart)
        self.actionSave.triggered.connect(self.saveDay)
        #self.actionClose.triggered.connect(self.closeBag)
        self.actionRemove_Selected.triggered.connect(self.removeRun)
        self.actionExit.triggered.connect(self.exitManager)

        #Return Options
        self.reviewLogs.triggered.connect(self.logLink)
        self.mainMenu.triggered.connect(self.mainLink)
        
        self.updateBags()
        
        for bag in cl.inv.listAllBags:
            OpenBags.append(bag)
            CurrentNum.update({bag:1})
        
    def updateBags(self):
        global OpenBags
        self.listOpenBags.clear()
        for bag in cl.inv.listAllBags:
            self.listOpenBags.addItem(str(bag.ID)+ ' | '+str(bag.flavor)+' | '+str(bag.trimWeight))

    def exitManager(self):
        sys.exit()

    def removeRun(self):
        self.listDailyRuns.takeItem(self.listDailyRuns.currentRow())

    #Save Daily Runs into inProcess.zzz
    def saveDay(self):
        global currentDate, OpenBags, OpenRuns
        saveList = []
        date = (str(currentDate.month)+'-'+str(currentDate.day)+'-'+str(currentDate.year))
        print(str(date))
        i = 0
        while i < self.listDailyRuns.count():
            saveString = str(self.listDailyRuns.item(i).text())
            saveList.append(OpenRuns[i])
            isplit = saveString.split()
            unfinished = cl.unfinishedProduct()
            unfinished.ID = isplit[0]
            for run in OpenRuns:
                if str(run.ID) == unfinished.ID:
                    unfinished.runsIncluded.append(run)
            for bag in OpenBags:
                if str(bag.ID) in isplit[0]:
                    unfinished.owner = bag.owner
                    bag.trimWeight -= float(isplit[4])
                    print('trim subtracted')
                    if bag.trimWeight <= 0.0:
                        cl.inv.listAllBags.pop(cl.inv.listAllBags.index(bag))
                        cl.inv.listFinishedBags.append(bag)
                        print('bag retired')
            cl.inv.listAllUnfinishedProduct.append(unfinished)
            print(isplit[0])
            i += 1
            
        cl.inv.listAllRuns.append([date,saveList])
        cl.save()
        self.updateBags()
        
    #Display Bag Prompt
    def bagStart(self):
        bagPrompt.show()

    #Display Run Prompt
    def runStart(self):
        runPrompt.bagNumBox.setCurrentIndex(self.listOpenBags.currentRow())
        runPrompt.setT()
        runPrompt.show()

    #Display Review Logs/Hide Run Manager
    def logLink(self):
        self.hide()
        review.show()

    #Display Start/Hide Run Manager
    def mainLink(self):
        self.hide()
        start.show()


class RunPrompt(QtGui.QDialog):
    def __init__(self):
        global OpenBags,CurrentNum
        super(RunPrompt, self).__init__()
        uic.loadUi(cl.UIstem+'RunPrompt.ui', self)
        
        self.runWeight.setText('1200')
        for item in OpenBags:
            self.bagNumBox.addItem(item.ID)
        self.bagNumBox.currentIndexChanged.connect(self.setT)
        self.branButt.clicked.connect(self.branB)
        self.evButt.clicked.connect(self.evB)
        self.patButt.clicked.connect(self.patB)
        
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
        
    def okClick(self):
        global OpenBags, OpenRuns, CurrentNum
        print('Test RunPrompt OK Click')
        name = str(self.runNumText.text())
                        
        if self.evButt.isChecked(): blaster = 'Evan'
        elif self.branButt.isChecked(): blaster = 'Brandon'
        elif self.patButt.isChecked(): blaster = 'Patrick'
        else: blaster = ''
        manager.listDailyRuns.addItem(name+' | '+
                                      str(blaster)+' | '+str(self.runWeight.displayText()))
        run = cl.run()
        run.ID = name
        run.timeStart = datetime.datetime.now()
        try:
            tbag = ''
            for bag in OpenBags:
                if str(self.bagNumBox.currentText()) == str(bag.ID):
                    print('found')
                    CurrentNum[bag] += 1
                    run.trimIncluded.append(bag)
                    run.owner = bag.shipment.name
                    run.trimAmounts.append(float(self.runWeight.displayText()))
                else:
                    print('not found')
        except: print('CurrentNum empty')
        OpenRuns.append(run)
        self.setT()
        manager.updateBags()
        self.hide()
        
    def cancelClick(self):
        self.hide()
        
    def branB(self):
        if self.evButt.isChecked(): self.evButt.toggle()
        if self.patButt.isChecked(): self.patButt.toggle()
        
    def patB(self):
        if self.evButt.isChecked(): self.evButt.toggle()
        if self.branButt.isChecked(): self.branButt.toggle()
        
    def evB(self):
        if self.branButt.isChecked(): self.branButt.toggle()
        if self.patButt.isChecked(): self.patButt.toggle()
    def setT(self):
        global OpenBags,CurrentNum
        try:    
            print CurrentNum
            tbag = ''
            for bag in OpenBags:
                if str(self.bagNumBox.currentText()) == str(bag.ID):
                    tbag = bag
            self.runNumText.setText(str(self.bagNumBox.currentText())+
                                    '-'+str(CurrentNum[tbag]))
        except:
            print('key error')
            self.runNumText.setText('')

if __name__ == '__main__':
#def begin():
    app = QtGui.QApplication(sys.argv)

    #Create Base Windows
    start = StartWindow()
    manager = ManagerWindow()
    runPrompt = RunPrompt()

    currentDate = datetime.datetime.now()
    
    #Display Start
    manager.show()

    sys.exit(app.exec_())
