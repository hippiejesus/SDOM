#!/usr/bin/env python
# -*- coding: utf-8 -*-
import classes as cl
import os
import sys
import time
import qdarkstyle
import subprocess
import fader
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import QRect, QPropertyAnimation

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(cl.UIstem+'SDOM.ui', self)
        
        self.label.hide()
        self.toSwitch = None
        
        self.setWindowTitle('Super Dope Operations Management')
        self.showFullScreen()

        self.label.setPixmap(QtGui.QPixmap("/home/pi/python/SDLabs/SDLOGO.jpg"))
        self.label.setScaledContents(True)
        
        
        self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py'))
        self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        self.actionProduct_Management.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        self.actionPackaging.triggered.connect(lambda: self.pageOpen('packaging.py'))
        self.actionDistillate.triggered.connect(lambda: self.pageOpen('distillate.py'))
        self.actionPOS.triggered.connect(lambda: self.pageOpen('pos.py'))
        self.actionIClick.triggered.connect(lambda: self.pageOpen('iclick.py'))
        self.actionLog_Access.triggered.connect(lambda: self.pageOpen('../../.logAccess/logAccess.py'))
        self.actionExit.triggered.connect(logClose)
        
        self.center()
        
    def fadeOutPix(self):
        self.effect = QtGui.QGraphicsOpacityEffect()
        self.label.setGraphicsEffect(self.effect)
        self.anim = QPropertyAnimation(self.effect,"opacity")
        self.fadeOut()
        self.anim.finished.connect(self.switch)
        
    def fadeInPix(self):
        self.effect = QtGui.QGraphicsOpacityEffect()
        self.label.setGraphicsEffect(self.effect)
        self.anim = QPropertyAnimation(self.effect,"opacity")
        self.fadeIn()
        self.anim.finished.connect(self.switch)
        
    def fadeIn(self):
        self.anim.setDuration(1200)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.anim.start()
        
    def fadeOut(self):
        self.anim.setDuration(1000)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.anim.start()
        
    def pageOpen(self,page):
        self.toSwitch = page
        self.fadeOut()
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        self.label.move(frameGm.topLeft())
        
    def switch(self):
        if self.toSwitch == None: return
        elif self.toSwitch == 'quit': exit()
        elif self.toSwitch == 'start':
            self.toSwitch = None
            self.label.show()
            self.fadeInPix()
            return
        self.label.hide()
        app.quit()
        subprocess.call('python '+self.toSwitch, shell=True)
    
def logClose():
    main.toSwitch = 'quit'
    main.fadeOutPix()
    
import atexit
atexit.register(logClose)
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())
    
    main = MainWindow()
    
    main.show()
    main.label.show()
    main.fadeInPix()
    #main.doAnim()
    
    sys.exit(app.exec_())
