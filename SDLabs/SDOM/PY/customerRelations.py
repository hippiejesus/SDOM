#!/usr/bin/env python
# -*- coding: utf-8 -*-

import classes as cl
import logger
import qdarkstyle
import os
import sys
import subprocess
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import QRect, QPropertyAnimation
from PyQt4.QtGui import QPainter

class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        uic.loadUi(cl.UIstem+'CustomerRelations.ui', self)
        
        self.actionNew.triggered.connect(self.newCustomer)
        self.actionView_Selected.triggered.connect(self.viewSelected)
        self.actionEdit_Selected.triggered.connect(self.editSelected)
        self.actionDelete_Selected.triggered.connect(self.deleteSelected)
        self.actionQuit.triggered.connect(self.quitProgram)
        
        #self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py')
        self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        self.actionProduct_Management.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        self.actionPackaging.triggered.connect(lambda: self.pageOpen('packaging.py'))
        self.actionDistillate.triggered.connect(lambda: self.pageOpen('distillate.py'))
        self.actionPOS.triggered.connect(lambda: self.pageOpen('pos.py'))
        
        self.listWidget.itemDoubleClicked.connect(self.viewSelected)
        
        companyList = cl.inv.listAllCompanies[:] 
        for item in companyList: #for companies in inventory, add names
            self.listWidget.addItem(item.name)
          
            
        self.center()
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
            
    def pageOpen(self,page):
        self.hide()
        app.quit()
        subprocess.call('python '+page, shell=True)
            
    def quitProgram(self):
        app.quit()
        self.hide()
        
            
    def newCustomer(self):
        try:
            cNew.show()
            cLog.write('mainWindow - cNew show...')
        except:
            cLog.write('mainWindow - ERROR: newCustomer(self)',deepData=str(sys.exc_info()))

    def viewSelected(self):
        try:
            cView.view(str(self.listWidget.currentItem().text()))
            cView.show()
            cLog.write('mainWindow - cView show...')
        except:
            cLog.write('mainWindow - ERROR: viewSelected(self)',deepData=str(sys.exc_info()))
        
    def editSelected(self):
        try:
            cEdit.edit(str(self.listWidget.currentItem().text()))
            cEdit.show()
            cLog.write('mainWindow - cEdit show...')
        except:
            cLog.write('mainWindow - ERROR: editSelected(self)',deepData=str(sys.exc_info()))
        
    def deleteSelected(self):
        toDelete = str(self.listWidget.currentItem().text())
        cLog.write('mainWindow - attempting account deletion...')
        try:
            for c in cl.inv.listAllCompanies:
                if c.name == toDelete:
                    inn = QtGui.QMessageBox.question(self,'Really?','Delete '+toDelete+'?',
                                                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if inn == QtGui.QMessageBox.Yes:
                        cl.inv.listAllCompanies.pop(cl.inv.listAllCompanies.index(c))
                        self.listWidget.takeItem(self.listWidget.currentRow())
                    
                        cl.save()
                        cLog.write('mainWindow - account deleted...',deepData=toDelete)
        except:
            cLog.write('mainWindow - ERROR: deleteSelected(self)',deepData=str(sys.exc_info()))

class customerNewWindow(QtGui.QDialog):
    def __init__(self):
        super(customerNewWindow, self).__init__()
        uic.loadUi(cl.UIstem+'customerNew.ui', self)
        
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
        
    def cancelClick(self):
        try:
            self.hide()
            self.lineCompany.clear()
            self.lineContactName.clear()
            self.lineContactNum.clear()
            self.lineEmail.clear()
            self.lineLicenseNum.clear()
            self.textNoteBox.clear()
            if self.pushBuyer.isChecked(): self.pushBuyer.toggle()
            if self.pushSupplier.isChecked(): self.pushSupplier.toggle()
            cLog.write('customerNewWindow - cancelled...')
        except:
            cLog.write('customerNewWindow - ERROR: cancelClick(self)',deepData=str(sys.exc_info()))
        
    def okClick(self):
        try:
            company = cl.company()
            contact = cl.contact()
        
            company.name = str(self.lineCompany.displayText())
            contact.name = str(self.lineContactName.displayText())
            contact.phone = str(self.lineContactNum.displayText())
            contact.email = str(self.lineEmail.displayText())
            company.licenseNumber = str(self.lineLicenseNum.displayText())
            company.notes = str(self.textNoteBox.toPlainText())
            
            if self.pushBuyer.isChecked(): company.isBuyer = True
            if self.pushSupplier.isChecked(): company.isSupplier = True

            company.contacts.append(contact)
            contact.companies.append(company)
        
            cl.inv.listAllCompanies.append(company)
            cl.inv.listAllCompaniesArchive.append(company)
            cl.inv.listAllContacts.append(contact)
            cl.inv.listAllContactsArchive.append(contact)
            cl.save()
        
            self.hide()
            self.lineCompany.clear()
            self.lineContactName.clear()
            self.lineContactNum.clear()
            self.lineEmail.clear()
            self.lineLicenseNum.clear()
            self.textNoteBox.clear()
        
            cMain.listWidget.addItem(company.name)
            cLog.write('customerNewWindow - account added...',deepData=company.name)
        except:
            cLog.write('customerNewWindow - ERROR: okClick(self)',deepData=str(sys.exc_info()))

class customerEditWindow(QtGui.QDialog):
    def __init__(self):
        super(customerEditWindow, self).__init__()
        uic.loadUi(cl.UIstem+'CustomerEdit.ui', self)
        self.currentCompany = cl.company()
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
     
    def okClick(self):
        try:
            c = self.currentCompany
            contact = c.contacts[0]
            c.name = str(self.lineCompany.displayText())
            contact.name = str(self.lineContactName.displayText())
            contact.phone = str(self.lineContactNum.displayText())
            contact.email = str(self.lineEmail.displayText())
            c.licenseNumber = str(self.lineLicenseNum.displayText())
            c.notes = str(self.textNoteBox.toPlainText())
            if self.pushBuyer.isChecked(): 
                c.isBuyer = True
            else: c.isBuyer = False
            if self.pushSupplier.isChecked(): 
                c.isSupplier = True
            else: c.isSupplier = False
        
            cl.save()
        
            self.lineCompany.clear()
            self.lineContactName.clear()
            self.lineContactNum.clear()
            self.lineEmail.clear()
            self.lineLicenseNum.clear()
            self.textNoteBox.clear()
            if self.pushBuyer.isChecked(): self.pushBuyer.toggle()
            if self.pushSupplier.isChecked(): self.pushSupplier.toggle()
        
            self.hide()
            cLog.write('customerEditWindow - account edited...',deepData=c.name)
        except:
            cLog.write('customerEditWindow - ERROR: okClick(self)',deepData=str(sys.exc_info()))
        
    def cancelClick(self):
        self.hide()
        cLog.write('customerEditWindow - cancelled...')
        self.lineCompany.clear()
        self.lineContactName.clear()
        self.lineContactNum.clear()
        self.lineEmail.clear()
        self.lineLicenseNum.clear()
        self.textNoteBox.clear()
        if self.pushBuyer.isChecked(): self.pushBuyer.toggle()
        if self.pushSupplier.isChecked(): self.pushSupplier.toggle()
        
    def edit(self,name):
        for c in cl.inv.listAllCompanies:
            if c.name == name:
                self.currentCompany = c
                contact = c.contacts[0]
                self.lineCompany.setText(c.name)
                self.lineContactName.setText(contact.name)
                self.lineContactNum.setText(contact.phone)
                self.lineEmail.setText(contact.email)
                self.lineLicenseNum.setText(c.licenseNumber)
                self.textNoteBox.setText(c.notes)
                if c.isBuyer == True: self.pushBuyer.toggle()
                if c.isSupplier == True: self.pushSupplier.toggle()
        
class customerViewWindow(QtGui.QDialog):
    def __init__(self):
        super(customerViewWindow, self).__init__()
        uic.loadUi(cl.UIstem+'CustomerView.ui', self)
        
        self.pushOk.pressed.connect(self.hideSelf)
        
    def hideSelf(self):
        try:
            self.hide()
            cLog.write('customerViewWindow - closed...')
        except:
            cLog.write('customerViewWindow - ERROR: hideSelf(self)',deepData=str(sys.exc_info()))
        
    def view(self,name):
        try:
            for c in cl.inv.listAllCompanies:
                if c.name == name:
                    contact = c.contacts[0]
                    self.labelCompany.setText(c.name)
                    self.labelContactName.setText(contact.name)
                    self.labelContactNum.setText(contact.phone)
                    self.labelEmail.setText(contact.email)
                    self.labelLicenseNum.setText(c.licenseNumber)
                    self.labelNotes.setText(c.notes)
                    cLog.write('customerViewWindow - fields set...',deepData=c.name)
        except:
            cLog.write('customerViewWindow - ERROR: view(self,name)',deepData=str(sys.exc_info()))
   
def logClose():
    app.quit()
    cLog.write('Terminating Session...')
    cLog.close()
    subprocess.call('python SDOM.pyw', shell=True)
    
import atexit
atexit.register(logClose)
        
if __name__ == '__main__':
#def begin():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())

    #Create Base Windows
    try:
        cLog = logger.log('customerRelations')
        cLog.write('Logging session begin...',deepData='begin_')
    except:
        print('Logger failure...\n'+str(sys.exc_info()))
        sys.exit()
    try:
        cMain = mainWindow()
        cLog.write('mainWindow initialized...')
    except:
        cLog.write('mainWindow error...\n'+str(sys.exc_info()))
    try:
        cNew = customerNewWindow()
        cLog.write('customerNewWindow initialized...')
    except:
        cLog.write('customerNewWindow error...\n'+str(sys.exc_info()))
    try:
        cEdit = customerEditWindow()
        cLog.write('customerEditWindow initialized...')
    except:
        cLog.write('customerEditWindow error...\n'+str(sys.exc_info()))
    try:
        cView = customerViewWindow()
        cLog.write('customerViewWindow initialized...')
    except:
        cLog.write('customerViewWindow error...\n'+str(sys.exc_info()))
    

    #Display Intake
    cMain.show()

    sys.exit(app.exec_())
