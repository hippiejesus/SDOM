#!/usr/bin/env python
# -*- coding: utf-8 -*-

import classes as cl
import os
import sys
from PyQt4 import QtGui, QtCore, uic

class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        uic.loadUi(cl.UIstem+'CustomerRelations.ui', self)
        
        self.actionNew.triggered.connect(self.newCustomer)
        self.actionView_Selected.triggered.connect(self.viewSelected)
        self.actionEdit_Selected.triggered.connect(self.editSelected)
        self.actionDelete_Selected.triggered.connect(self.deleteSelected)
        self.actionQuit.triggered.connect(self.quitProgram)
        
        companyList = cl.inv.listAllCompanies[:] 
        for item in companyList: #for companies in inventory, add names
            self.listWidget.addItem(item.name)
            
    def quitProgram(self):
        sys.exit()
            
    def newCustomer(self):
        cNew.show()

    def viewSelected(self):
        cView.view(str(self.listWidget.currentItem().text()))
        cView.show()
        
    def editSelected(self):
        cEdit.edit(str(self.listWidget.currentItem().text()))
        cEdit.show()
        
    def deleteSelected(self):
        toDelete = str(self.listWidget.currentItem().text())
        for c in cl.inv.listAllCompanies:
            if c.name == toDelete:
                inn = QtGui.QMessageBox.question(self,'Really?','Delete '+toDelete+'?',
                                                 QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if inn == QtGui.QMessageBox.Yes:
                    cl.inv.listAllCompanies.pop(cl.inv.listAllCompanies.index(c))
                    self.listWidget.takeItem(self.listWidget.currentRow())
                    
                    cl.save()

class customerNewWindow(QtGui.QDialog):
    def __init__(self):
        super(customerNewWindow, self).__init__()
        uic.loadUi(cl.UIstem+'customerNew.ui', self)
        
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
        
    def cancelClick(self):
        self.hide()
        self.lineCompany.clear()
        self.lineContactName.clear()
        self.lineContactNum.clear()
        self.lineEmail.clear()
        self.lineLicenseNum.clear()
        self.textNoteBox.clear()
        
    def okClick(self):
        company = cl.company()
        contact = cl.contact()
        
        company.name = str(self.lineCompany.displayText())
        contact.name = str(self.lineContactName.displayText())
        contact.phone = str(self.lineContactNum.displayText())
        contact.email = str(self.lineEmail.displayText())
        company.licenseNumber = str(self.lineLicenseNum.displayText())
        company.notes = str(self.textNoteBox.toPlainText())

        company.contacts.append(contact)
        contact.companies.append(company)
        
        cl.inv.listAllCompanies.append(company)
        cl.inv.listAllContacts.append(contact)
        cl.save()
        
        self.hide()
        self.lineCompany.clear()
        self.lineContactName.clear()
        self.lineContactNum.clear()
        self.lineEmail.clear()
        self.lineLicenseNum.clear()
        self.textNoteBox.clear()
        
        cMain.listWidget.addItem(company.name)

class customerEditWindow(QtGui.QDialog):
    def __init__(self):
        super(customerEditWindow, self).__init__()
        uic.loadUi(cl.UIstem+'CustomerEdit.ui', self)
        self.currentCompany = cl.company()
        self.buttonBox.accepted.connect(self.okClick)
        self.buttonBox.rejected.connect(self.cancelClick)
     
    def okClick(self):
        c = self.currentCompany
        contact = c.contacts[0]
        c.name = str(self.lineCompany.displayText())
        contact.name = str(self.lineContactName.displayText())
        contact.phone = str(self.lineContactNum.displayText())
        contact.email = str(self.lineEmail.displayText())
        c.licenseNumber = str(self.lineLicenseNum.displayText())
        c.notes = str(self.textNoteBox.toPlainText())
        
        cl.save()
        
        self.lineCompany.clear()
        self.lineContactName.clear()
        self.lineContactNum.clear()
        self.lineEmail.clear()
        self.lineLicenseNum.clear()
        self.textNoteBox.clear()
        
        self.hide()
        
    def cancelClick(self):
        self.hide()
        
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
        
class customerViewWindow(QtGui.QDialog):
    def __init__(self):
        super(customerViewWindow, self).__init__()
        uic.loadUi(cl.UIstem+'CustomerView.ui', self)
        
        self.pushOk.pressed.connect(self.hideSelf)
        
    def hideSelf(self):
        self.hide()
        
    def view(self,name):
        for c in cl.inv.listAllCompanies:
            if c.name == name:
                contact = c.contacts[0]
                self.labelCompany.setText(c.name)
                self.labelContactName.setText(contact.name)
                self.labelContactNum.setText(contact.phone)
                self.labelEmail.setText(contact.email)
                self.labelLicenseNum.setText(c.licenseNumber)
                self.labelNotes.setText(c.notes)
        
if __name__ == '__main__':
#def begin():
    app = QtGui.QApplication(sys.argv)

    #Create Base Windows
    cMain = mainWindow()
    cNew = customerNewWindow()
    cEdit = customerEditWindow()
    cView = customerViewWindow()
    

    #Display Intake
    cMain.show()

    sys.exit(app.exec_())
