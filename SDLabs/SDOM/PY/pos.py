import os
import classes as cl
import logger
import qdarkstyle
import datetime
import copy
import time
import re
import sys
import subprocess
from PyQt4 import QtGui, QtCore, uic

products = {}
windows = []

class POSMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(POSMainWindow, self).__init__()
        uic.loadUi(cl.UIstem+'posMain.ui', self)
        
        self.kinds ={'Crumble':self.listCrum,
                     'Crystals':self.listCry,
                     'Distillate':self.listDisto,
                     'Resin':self.listLive,
                     'RSO':self.listRsopt}
                     
        self.actionSell_Selected.triggered.connect(self.sellSelected)
        self.actionPending_Payments.triggered.connect(self.acceptPay)
        self.actionPayments_Recieved.triggered.connect(self.reviewPay)
        self.actionProduct_Management.triggered.connect(self.sendProduct)
        self.actionExit.triggered.connect(self.exitApp)
        
        self.listCrum.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listCry.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listDisto.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listLive.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listRsopt.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        self.listCrum.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCrum))
        self.listCry.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listCry))
        self.listDisto.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listDisto))
        self.listLive.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listLive))
        self.listRsopt.itemSelectionChanged.connect(lambda: self.uncheckLists(self.listRsopt))
                     
        self.updateLists()
        
        self.actionCustomer_Relations.triggered.connect(lambda: self.pageOpen('customerRelations.py'))
        self.actionIntake.triggered.connect(lambda: self.pageOpen('intake.py'))
        self.actionLab.triggered.connect(lambda: self.pageOpen('lab.py'))
        self.actionFinishing.triggered.connect(lambda: self.pageOpen('finishing.py'))
        self.actionYield.triggered.connect(lambda: self.pageOpen('yieldW.py'))
        self.actionProduct_Management_2.triggered.connect(lambda: self.pageOpen('productManagement.py'))
        self.actionPackaging.triggered.connect(lambda: self.pageOpen('packaging.py'))
        self.actionDistillate.triggered.connect(lambda: self.pageOpen('distillate.py'))
        #self.actionPOS.triggered.connect(lambda: self.pageOpen('pos.py'))
        
        self.center()
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def exitApp(self):
        QtCore.QCoreApplication.instance().quit()
        self.hide()
        
    def pageOpen(self,page):
        if self.actionPage_Switch_On_Off.isChecked(): QtCore.QCoreApplication.instance().quit(); self.hide()
        #lg.close()
        subprocess.call('python '+page, shell=True)
        
    def sendProduct(self):
        global products
        for kind in self.kinds.values():
            current = kind.currentItem()
            print kind.currentItem()
            if current != None:
                for container in products.values():
                    if container.isPackaged: ins = '(P)'
                    elif container.isPackaged == False: ins = '(B)'
                    else: ins = ''
                    conName = container.ID +ins+' : ' + str(container.numberOfUnits)
                    if str(conName) == str(current.text()):
                        container.kind = container.kind[3:]
        cl.save()
        self.updateLists()
        
    def acceptPay(self):
        payWindow = POSPaymentWindow()
        
    def reviewPay(self):
        reviewPayWindow = POSPaymentReviewWindow()
        
    def uncheckLists(self,avoidList):
        
        for kind in self.kinds.values():
            item = kind
            current = item.currentItem()
            if current != None and item is not avoidList and self.pushMultiple.isChecked() == False:
                current.setSelected(False)
                kind.setCurrentItem(None)
        
    def sellSelected(self,item):
        global products, windows
        
        productsToSell = list()
        for kind in self.kinds.values():
            current = kind.currentItem()
            print kind.currentItem()
            if current != None:
                product = products[str(current.text())]
                productsToSell.append(product)
        print product.ID
        soldWindow = POSSoldToWindow()
        windows.append(soldWindow)
        priceWindows = list()
        for item in productsToSell:
            priceWindow = POSPricingWindow()
            priceWindows.append(priceWindow)
            windows.append(priceWindow)
        soldWindow.setProduct(productsToSell,priceWindows)
        soldWindow.show()
        
    def updateLists(self):
        global products
        cl.load()
        products = {}
        source = cl.inv.listAllContainers

        for kindList in self.kinds.values():
            kindList.clear()
                
        for container in source:
            if '(S)' in str(container.kind):
                target = container.kind[3:]
                if target in self.kinds.keys():
                    if container.isPackaged: ins = '(P)'
                    elif container.isPackaged == False: ins = '(B)' ; container.numberOfUnits = int(container.weight) ; container.unitSize = 1.00
                    else: ins = ''
                    conName = container.ID +ins+' : ' + str(container.numberOfUnits)
                    self.kinds[target].addItem(conName)
                    products.update({str(conName):container})

class POSPaymentWindow(QtGui.QDialog):
    def __init__(self):
        global windows
        super(POSPaymentWindow, self).__init__()
        uic.loadUi(cl.UIstem+'posPayment.ui', self)
        
        self.payments = list()
        
        self.listPayments.itemDoubleClicked.connect(self.pay)
        
        cl.load()
        for payment in cl.inv.listAllReciepts:
            if payment.paymentRecieved == False:
                self.payments.append(payment)
                self.listPayments.addItem(str(payment.transaction.sendingEntity.name)+' : $'+str(payment.transaction.amountToBePayed)+' -- '+payment.dateSold)
        windows.append(self)
        self.show()
        
    def pay(self):
        payment = self.payments[self.listPayments.currentRow()]
        inn, ok = QtGui.QInputDialog.getText(self,'Enter','Amount:')
        if ok:
            payment.transaction.amountToBePayed -= float(inn)
            payment.transaction.amountPayed += float(inn)
            if payment.transaction.amountToBePayed <= 0:
                payment.paymentRecieved = True
        cl.save()
        self.hide()
        posMain.updateLists()
        
class POSPaymentReviewWindow(QtGui.QDialog):
    def __init__(self):
        global windows
        super(POSPaymentReviewWindow, self).__init__()
        uic.loadUi(cl.UIstem+'posPayment.ui',self)
        
        self.payments = list()
        
        cl.load()
        for payment in cl.inv.listAllReciepts:
            self.listPayments.addItem(str(payment.transaction.sendingEntity.name)+' : $'+str(payment.transaction.amountPayed)+'/'+str(payment.transaction.amountPayed+payment.transaction.amountToBePayed))
            
        windows.append(self)
        self.show()

class POSPricingWindow(QtGui.QDialog):
    def __init__(self):
        super(POSPricingWindow, self).__init__()
        uic.loadUi(cl.UIstem+'posPricing.ui', self)
        
        self.currentCompany = None
        self.currentProduct = cl.container()
        self.priceWindows = list()
        self.productsToSell = list()
        
        self.unitButtons = [self.pushAllUnit, self.pushPartialUnit]
        
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        self.pushAllUnit.clicked.connect(lambda: self.unitClicked(self.pushAllUnit))
        self.pushPartialUnit.clicked.connect(lambda: self.unitClicked(self.pushPartialUnit))
        
    def ok(self):
        global windows
        if self.pushAllUnit.isChecked():
            unitsSold = float(self.currentProduct.numberOfUnits)
        elif self.pushPartialUnit.isChecked():
            unitsSold = float(self.linePartialUnit.text())
        pricePerUnit = float(self.lineUnitPrice.text())
        totalPrice = pricePerUnit * unitsSold
        
        trans = cl.transaction()
        trans.recievingEntity = 'Super Dope'
        trans.sendingEntity = self.currentCompany
        trans.valuedEntity = self.currentProduct
        trans.amountToBePaid = totalPrice
        
        sold = cl.soldProduct()
        sold.ID = self.currentProduct.ID
        sold.kind = self.currentProduct.kind
        sold.container = self.currentProduct
        sold.weight = self.currentProduct.weight
        sold.totalPrice = totalPrice
        sold.unitPrice = pricePerUnit
        sold.unitsSold = float(unitsSold)
        sold.paymentStatus = trans
        
        cl.inv.listAllSoldProduct.append(sold)
        cl.inv.listAllTransactions.append(trans)
        cl.inv.listAllSoldProductArchive.append(sold)
        cl.inv.listAllTransactionsArchive.append(trans)
        
        posReview.soldProducts.append(sold)
        posReview.transactions.append(trans)
        
        print self.priceWindows
        print self.productsToSell
        
        if self.productsToSell == []:
            posReview.review()
            self.hide()
        else:
            self.hide()
            window1 = self.priceWindows[0]
            window1.setCompany(self.currentCompany,self.productsToSell[0])
            self.priceWindows.pop(0)
            self.productsToSell.pop(0)
            window1.passLists(self.priceWindows,self.productsToSell)
        
    def cancel(self):
        self.lineUnitPrice.clear()
        self.linePartialUnit.clear()
        for button in self.unitButtons:
            if button.isChecked(): button.toggle()
        self.hide()
        
    def unitClicked(self,button):
        for choice in self.unitButtons:
            if choice != button and choice.isChecked(): choice.toggle()
        
    def setCompany(self,company,product):
        self.currentCompany = company
        self.currentProduct = product
        self.labelProduct.setText(str(product.ID) + ' being sold to ' + str(company.name))
        self.show()
        
    def passLists(self,listPages,listProducts):
        self.priceWindows = listPages
        self.productsToSell = listProducts

class POSReviewWindow(QtGui.QDialog):
    def __init__(self):
        super(POSReviewWindow, self).__init__()
        uic.loadUi(cl.UIstem+'posReview.ui', self)
        
        self.soldProducts = list()
        self.transactions = list()
        
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        
    def ok(self):
        paid = bool()
        total = float(self.lineSaleTotal.text())
        transaction = copy.deepcopy(self.transactions[0])
        transaction.amountToBePayed = total
        
        if self.pushPaidFull.isChecked(): transaction.amountPayed = transaction.amountToBePayed ; transaction.amountToBePayed = 0.00
        else: transaction.amountPayed = float(self.linePaidPartial.text()) ; transaction.amountToBePayed -= float(self.linePaidPartial.text())
        
        if transaction.amountToBePayed == 0.00: recieved = True
        else: recieved = False
        
        for item in self.soldProducts:
            container = item.container
            container.numberOfUnits -= item.unitsSold
            container.weight -= container.unitSize*item.unitsSold
            if container.numberOfUnits <= 0:
                cl.inv.listAllContainers.pop(cl.inv.listAllContainers.index(container))
        
        final = cl.finalizedSale(self.soldProducts[:],transaction,str(datetime.datetime.now()),recieved,total)
        cl.inv.listAllReciepts.append(final)
        cl.inv.listAllRecieptsArchive.append(final)
        self.hide()
        cl.save()
        posMain.updateLists()
        
    def cancel(self):
        pass
        
    def review(self):
        totalTotal = 0.00
        for item in self.soldProducts:
            soldString = str(item.ID)+' @ $'+str(item.unitPrice)+'*'+str(item.unitsSold)+' units -- $'+str(item.totalPrice)
            self.listProductSoldReview.addItem(soldString)
            totalTotal += item.totalPrice
        self.lineSaleTotal.setText(str(totalTotal))
        self.labelCompany.setText(str(self.soldProducts[0].paymentStatus.sendingEntity.name))
        self.labelDate.setText(str(datetime.datetime.now()))
        self.show()
        
class POSSoldToWindow(QtGui.QDialog):
    def __init__(self):
        super(POSSoldToWindow, self).__init__()
        uic.loadUi(cl.UIstem+'posSoldTo.ui', self)
        
        self.priceWindows = None
        self.lineOther.hide()
        self.currentChoice = 0
        self.currentProducts = list()
        self.companyList = list()
        self.comboCompany.currentIndexChanged.connect(self.setOther)
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        
        self.setOptions()
        
    def ok(self):
        if str(self.comboCompany.itemText(self.currentChoice)) == 'Other':
            tempCompany = cl.company()
            tempCompany.name = str(self.lineOther.text())
            tempCompany.isBuyer = True
            company = tempCompany
        else:
            company = self.companyList[self.currentChoice]
        
        window1 = self.priceWindows[0]
        window1.setCompany(company,self.currentProducts[0])
        self.priceWindows.pop(0)
        self.currentProducts.pop(0)
        window1.passLists(self.priceWindows,self.currentProducts)
        self.hide()
        
        
    def cancel(self):
        self.comboCompany.setCurrentIndex(0)
        self.hide()
        
    def setOptions(self):
        for company in cl.inv.listAllCompanies:
            if company.isBuyer:
                self.comboCompany.addItem(company.name)
                self.companyList.append(company)
        self.comboCompany.addItem('Other')
        
    def setOther(self,index):
        self.currentChoice = index
        if str(self.comboCompany.itemText(index)) == 'Other':
            self.lineOther.show()
        else:
            self.lineOther.hide()
            
    def setProduct(self,products,priceWindows):
        self.priceWindows = priceWindows
        self.currentProducts = products

def logClose():
    app.quit()
    #lg.write('Terminating Session...')
    #lg.close()
    subprocess.call('python SDOM.pyw', shell=True)
    
import atexit
atexit.register(logClose)

if __name__ == '__main__':
#def begin():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())

    #Create Base Windows
    posMain = POSMainWindow()
    #posPricing = POSPricingWindow()
    posReview = POSReviewWindow()
    #posSoldTo = POSSoldToWindow()


    #Display Start
    posMain.show()

    sys.exit(app.exec_())
