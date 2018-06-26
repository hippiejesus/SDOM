#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os.path
import qdarkstyle
import classes as cl
import logger
import time
import sys
import subprocess
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import QRect, QPropertyAnimation

OpenTotes = []
OpenRuns = []
CurrentNum = {}
currentDate = ''
viewWindows = []
weightLoss = {}

class StartWindow(QtGui.QDialog):
    def __init__(self):
        super(StartWindow, self).__init__()
        uic.loadUi(cl.UIstem+'Start.ui', self)

        #Selection Options
        self.run.clicked.connect(self.runMan)
        self.review.clicked.connect(self.reviewMan)

    #Display Run Manager/Hide Start
    def runMan(self):
        try:
            self.hide()
            manager.show()
            lg.write('StartWindow - manager show...')
        except:
            lg.write('StartWindow - ERROR: runMan(self)',deepData=str(sys.exc_info()))

    #Display Review Logs/Hide Start
    def reviewMan(self):
        try:
            self.hide()
            review.show()
            lg.write('StartWindow - review show...')
        except:
            lg.write('StartWindow - ERROR: reviewMan(self)',deepData=str(sys.exc_info()))


class ManagerWindow(QtGui.QMainWindow):
    def __init__(self):
        global OpenTotes
        super(ManagerWindow, self).__init__()
        uic.loadUi(cl.UIstem+'runMain.ui', self)

        #Selection Options
        self.newBag.triggered.connect(self.bagStart)
        self.startRun.triggered.connect(self.runStart)
        self.actionSave.triggered.connect(self.saveDay)
        #self.actionClose.triggered.connect(self.closeBag)
        self.actionRemove_Selected.triggered.connect(self.removeRun)
        self.actionExit.triggered.connect(self.exitManager)
        
        self.listOpenTotes.itemDoubleClicked.connect(self.runStart)
        self.listDailyRuns.itemDoubleClicked.connect(self.viewSelected)

        #Return Options
        self.reviewLogs.triggered.connect(self.logLink)
        self.mainMenu.triggered.connect(self.mainLink)
        
        self.updateBags()
        
        self.currentRunTote = None
        
        for tote in cl.inv.listAllTotes:
            OpenTotes.append(tote)
            CurrentNum.update({tote:int(tote.lastRun)})
            
        self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py'))
        self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        #self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        self.actionProduct_Management.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        self.actionPackaging.triggered.connect(lambda: self.pageOpen('packaging.py'))
        self.actionDistillate.triggered.connect(lambda: self.pageOpen('distillate.py'))
        self.actionPOS.triggered.connect(lambda: self.pageOpen('pos.py'))
        
        self.center()
        
    def pageOpen(self,page):
        self.hide()
        app.quit()
        subprocess.call('python '+self.page, shell=True)
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def updateBags(self):
        global OpenTotes
        try:
            self.listOpenTotes.clear()
            for tote in cl.inv.listAllTotes:
                try:
                    self.listOpenTotes.addItem(str(tote.ID)+ ' | '+str(tote.flavor)+' | '+str(tote.trimWeight-weightLoss[tote]))
                except:
                    self.listOpenTotes.addItem(str(tote.ID)+ ' | '+str(tote.flavor)+' | '+str(tote.trimWeight))
            lg.write('ManagerWindow - listOpenTotes populated...',deepData=self.listOpenTotes)
        except:
            lg.write('ManagerWindow - ERROR: updateBags(self)',deepData=str(sys.exc_info()))

    def exitManager(self):
        app.quit()
        self.hide()

    def removeRun(self):
        try:
            self.listDailyRuns.takeItem(self.listDailyRuns.currentRow())
            self.currentRunTote.lastRun -= 1
            CurrentNum[self.currentRunTote] -= 1
            lg.write('ManagerWindow - run removed from listDailyRuns...')
        except:
            lg.write('ManagerWindow - ERROR: removeRun(self)',deepData=str(sys.exc_info()))

    #Save Daily Runs into inProcess.zzz
    def saveDay(self):
        global currentDate, OpenTotes, OpenRuns, weightLoss
        weightLoss = {}
        saveList = []
        date = (str(currentDate.month)+'-'+str(currentDate.day)+'-'+str(currentDate.year))
        print(str(date))
        lg.write('ManagerWindow - beginning save...',deepData=date)
        i = 0
        try:
            while i < self.listDailyRuns.count():
                saveString = str(self.listDailyRuns.item(i).text())
                saveList.append(OpenRuns[i])
                isplit = saveString.split()
                unfinished = cl.unfinishedProduct()
                unfinished.ID = isplit[0]
                for run in OpenRuns:
                    if str(run.ID) == unfinished.ID:
                        unfinished.runsIncluded.append(run)
                        unfinished.location = run.location
                        run.location.items.append(unfinished)
                for tote in OpenTotes:
                    if str(tote.ID) in isplit[0]:
                        unfinished.owner = tote.owner
                        tote.trimWeight -= float(isplit[4])
                        print('trim subtracted')
                        if tote.trimWeight <= 0.0:
                            cl.inv.listAllTotes.pop(cl.inv.listAllTotes.index(tote))
                            cl.inv.listFinishedTotes.append(tote)
                            cl.inv.listFinishedTotesArchive.append(tote)
                            tote.location.items.pop(tote.location.items.index(tote))
                            tote.location = 'Retired'
                            print('bag retired')
                cl.inv.listAllUnfinishedProduct.append(unfinished)
                cl.inv.listAllUnfinishedProductArchive.append(unfinished)
                print(isplit[0])
                i += 1
            self.listDailyRuns.clear()
            OpenRuns = []
            cl.inv.listAllRuns.append([date,saveList])
            cl.inv.listAllRunsArchive.append([date,saveList])
            cl.save()
            self.updateBags()
            lg.write('ManagerWindow - save successful...')
        except:
            lg.write('ManagerWindow - ERROR: saveDay(self)',deepData=str(sys.exc_info()))
        
    #Display Bag Prompt
    def bagStart(self):
        try:
            bagPrompt.show()
            lg.write('ManagerWindow - bagPrompt show...')
        except:
            lg.write('ManagerWindow - ERROR: bagStart(self)',deepData=str(sys.exc_info()))

    def viewSelected(self):
        global viewWindows
        try:
            rview = RunView(OpenRuns[self.listDailyRuns.currentRow()])
            viewWindows.append(rview)
        except:
            lg.write('ManagerWindow - ERROR: viewSelected(self)',deepData=str(sys.exc_info()))

    #Display Run Prompt
    def runStart(self):
        try:
            runPrompt.bagNumBox.setCurrentIndex(self.listOpenTotes.currentRow())
            runPrompt.setT()
            runPrompt.show()
            lg.write('ManagerWindow - runPrompt show...')
        except:
            lg.write('ManagerWindow - ERROR: runStart(self)',deepData=str(sys.exc_info()))

    #Display Review Logs/Hide Run Manager
    def logLink(self):
        try:
            self.hide()
            review.show()
            lg.write('ManagerWindow - review show...')
        except:
            lg.write('ManagerWindow - ERROR: logLink(self)',deepData=str(sys.exc_info()))

    #Display Start/Hide Run Manager
    def mainLink(self):
        try:
            self.hide()
            start.show()
            lg.write('ManagerWindow - start show...')
        except:
            lg.write('ManagerWindow - ERROR: mainLink(self)',deepData=str(sys.exc_info()))


class RunPrompt(QtGui.QDialog):
    def __init__(self):
        global OpenTotes,CurrentNum
        super(RunPrompt, self).__init__()
        uic.loadUi(cl.UIstem+'runPrompt.ui', self)
        
        self.runWeight.setText('1200')
        for item in OpenTotes:
            self.bagNumBox.addItem(item.ID)
        self.bagNumBox.currentIndexChanged.connect(self.setT)
        self.pushOther.clicked.connect(self.otherB)
        self.evButt.clicked.connect(self.evB)
        self.patButt.clicked.connect(self.patB)
        
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
        
        self.lineOther.hide()
        
    def okClick(self):
        global OpenTotes, OpenRuns, CurrentNum, weightLoss
        try:
            name = str(self.runNumText.text())
                        
            if self.evButt.isChecked(): blaster = 'Evan'
            elif self.pushOther.isChecked(): blaster = str(self.lineOther.text())
            elif self.patButt.isChecked(): blaster = 'Patrick'
            else: blaster = ''
            run = cl.run()
            run.ID = name
            run.blaster = blaster
            run.timeStart = datetime.datetime.now()
            try:
                tbag = ''
                for bag in OpenTotes:
                    if str(self.bagNumBox.currentText()) == str(bag.ID):
                        try:
                            if bag.trimWeight - weightLoss[bag] - float(self.runWeight.displayText()) < 0: self.hide() ; return
                        except:
                            if bag.trimWeight - float(self.runWeight.displayText()) < 0: self.hide() ; return
                        print('found')
                        CurrentNum[bag] += 1
                        run.trimIncluded.append(bag)
                        run.owner = bag.shipment.source
                        location = None
                        for i in cl.inv.listAllLocations:
                            if str(i.ID) == 'Lab': location = i
                        run.location = location
                        run.trimAmounts.append(float(self.runWeight.displayText()))
                        bag.lastRun += 1
                        manager.currentRunTote = bag
                        if bag in weightLoss.keys():
                            weightLoss[bag] += float(sum(run.trimAmounts))
                        else:
                            weightLoss.update({bag:float(sum(run.trimAmounts))})
                    else:
                        print('not found')
            except: print(str(sys.exc_info()))
            manager.listDailyRuns.addItem(name+' | '+
                                          str(blaster)+' | '+str(self.runWeight.displayText()))
            OpenRuns.append(run)
            self.setT()
            manager.updateBags()
            self.hide()
            lg.write('RunPrompt - run added...',deepData=run)
        except:
            lg.write('RunPrompt - ERROR: okClick(self)',deepData=str(sys.exc_info()))
        
    def cancelClick(self):
        try:
            self.hide()
            lg.write('RunPrompt - cancelled...')
        except:
            lg.write('RunPrompt - ERROR: cancelClick(self)',deepData=str(sys.exc_info()))
        
    def otherB(self):
        try:
            if self.evButt.isChecked(): self.evButt.toggle()
            if self.patButt.isChecked(): self.patButt.toggle()
            self.lineOther.show()
        except:
            lg.write('RunPrompt - ERROR: otherB(self)',deepData=str(sys.exc_info()))
        
    def patB(self):
        try:
            if self.evButt.isChecked(): self.evButt.toggle()
            if self.pushOther.isChecked(): self.branButt.toggle()
            self.lineOther.hide()
        except:
            lg.write('RunPrompt - ERROR: patB(self)',deepData=str(sys.exc_info()))
        
    def evB(self):
        try:
            if self.pushOther.isChecked(): self.branButt.toggle()
            if self.patButt.isChecked(): self.patButt.toggle()
            self.lineOther.hide()
        except:
            lg.write('RunPrompt - ERROR: evB(self)',deepData=str(sys.exc_info()))
            
    def setT(self):
        global OpenTotes,CurrentNum
        try:    
            print CurrentNum
            tbag = ''
            for bag in OpenTotes:
                if str(self.bagNumBox.currentText()) == str(bag.ID):
                    tbag = bag
            self.runNumText.setText(str(self.bagNumBox.currentText())+
                                    '-'+str(CurrentNum[tbag]))
        except:
            print('key error')
            lg.write('RunPrompt - ERROR: setT(self)',deepData=str(sys.exc_info()))
            self.runNumText.setText('')

class RunView(QtGui.QDialog):
    def __init__(self,run):
        global OpenTotes,CurrentNum
        super(RunView, self).__init__()
        uic.loadUi(cl.UIstem+'runView.ui', self)
        
        totalWeight = 0
        for i in run.trimAmounts:
            totalWeight += int(i)
        
        self.labelSerial.setText('Serial: '+str(run.trimIncluded[0].ID))
        self.labelRun.setText('Run: '+str(run.ID))
        self.labelWeight.setText('Weight: '+str(totalWeight))
        self.labelBlaster.setText('Blaster: '+str(run.blaster))
        self.labelTime.setText('Time: '+str(run.timeStart))
        self.labelOwner.setText('Owner: '+str(run.owner))
        
        self.show()

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
        lg = logger.log('lab')
        lg.write('Logging session begin...',deepData='begin_')
    except:
        print('Logger failure...\n'+str(sys.exc_info()))
        sys.exit()

    #Create Base Windows
    try:
        start = StartWindow()
        lg.write('StartWindow initialized...')
    except:
        lg.write('StartWindow error...\n'+str(sys.exc_info()))
    try:
        manager = ManagerWindow()
        lg.write('ManagerWindow initialized...')
    except:
        lg.write('ManagerWindow error...\n'+str(sys.exc_info()))
    try:
        runPrompt = RunPrompt()
        lg.write('RunPrompt initialized...')
    except:
        lg.write('RunPrompt error...\n'+str(sys.exc_info()))
        
    try:
        currentDate = datetime.datetime.now()
        lg.write('currentDate set...')
    except:
        lg.write('currentDate - error setting date...\n'+str(sys.exc_info()))
        
    
    #Display Start
    manager.show()

    sys.exit(app.exec_())
