import SDPickler as sdp
import uuid
import datetime
import os

UIstem = '../UI/'

class employee:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.name = ''
        self.kind = 'employee'
        self.company = ''
        self.phone = ''
        self.email = ''
        self.position = ''
        self.permissions = []

class company:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.ID = ''
        self.name = ''
        self.kind = 'company'
        #self.sources = []
        
        self.amountOwed = 0.00 #How much is currently owed to this company
        
        self.contacts = []
        self.licenseNumber = ''
        #self.destinations = []
        self.notes = []
        self.listAllEntities = [] #unfinished product, product, trimbags, etc...everything from that company.
        self.isBuyer = False #Denotes if the company purchases products from Super Dope
        self.isSupplier = False #Denotes if the company sells products to Super Dope

class contact:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.name = ''
        self.phone = ''
        self.notes = []
        self.email = ''
        self.companies = []
        self.isPrimary = False
        
"""class source:
    def __init__(self):
        self.name = ''
        self.contacts = [] #list of contact objects
        self.licenseNumber = ''
        self.notes = []"""
        
class trimBag:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.ID = ''
        self.kind = 'bag'
        self.shipment = ''
        self.owner = ''
        self.trimWeight = 0.00
        self.ogTrimWeight = 0.00
        self.flavor = ''
        self.location = '' #location object
        #self.testResults = []
        self.lastRun = 1
        inProcess = False
        
        
class trimTote:
    def __init__(self,trimbag):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.ID = trimbag.ID
        self.kind = 'tote'
        self.shipment = trimbag.shipment
        self.owner = trimbag.owner
        self.trimWeight = 0.00
        self.ogTrimWeight = 0.00
        
        self.flavor = trimbag.flavor
        self.location = '' #location object
        self.testResults = []
        self.lastRun = 1
        inProcess = False
  
class shipment:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.source = '' #company object
        self.kind = 'shipment'
        self.ID = ''
        self.bags = []
        self.flavor = ''
        
        self.paymentPlan = None #Can be 'pound' or 'percent'
        
        self.dateIn = ''
        self.testResults = []
        self.locations = [] #list of location objects
        self.totalWeight = 0.00
        self.totalPrice = 0.00
        
        
class run:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.ID = ''
        self.kind = 'blasted run'
        self.trimIncluded = []
        self.trimAmounts = []
        #self.machine = ''
        self.weightYield = 0.0
        self.timeStart = ''
        self.owner = ''
        self.blaster = ''
        self.location = '' #location object
        
class unfinishedProduct:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.ID = ''
        self.kind = 'unfinished product'
        self.runsIncluded = []
        self.run = ''
        self.owner = ''
        self.intendedFinish = ''
        #self.machine = ''
        self.testResults = []
        self.weight = 0.00
        self.location = '' #location object
  
class container:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.ID = ''
        self.productIncluded = []
        self.kind = ''
        self.numberOfUnits = 0 #in bulk, #=number of grams, in packaged goods #=number of units packaged
        self.weight = 0.00
        self.testResults = []
        self.isPackaged = False
        self.unitSize = 0.00 #float - grams per unit
        self.purpose = None #destination
        self.history = [] #list of lists, each containing (date),(add/subtract),(amount),(reason)
        self.location = '' #location object
        
class finishedProduct:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.ID = ''
        self.unfinishedProductIncluded = []
        self.finishedProductIncluded = []
        self.kind = ''
        self.weight = 0.00
        self.grade = ''
        self.container = ''
        self.testResults = []
        self.location = '' #location object
        
        self.isPaidFor = False #Set to true upon creation if shipment was by pound.
        
class soldProduct:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.ID = ''
        self.kind = ''
        self.container = ''
        self.weight = 0.00
        self.totalPrice = 0.00
        self.unitPrice = 0.00
        self.unitsSold = 0
        self.paymentStatus = '' #pending, recieved, etc. 
        self.location = '' #location object
    
class finalizedSale:
    def __init__(self,products,transaction,date,recieved,value):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.soldProductIncluded = products
        self.kind = 'finalized sale'
        self.transaction = transaction
        self.dateSold = date
        self.paymentRecieved = recieved
        self.totalValue = value #The amount the total order sold for

class transaction:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.recievingEntity = '' #who is being payed. let this be the object reference of that entity.
        self.sendingEntity = '' #who is paying.
        self.amountToBePayed = 0.00
        self.amountPayed = 0.00
        self.valuedEntity = [] #what is being transacted.
        self.kind = 'transaction'
        self.status = ''
        
class location:
    def __init__(self):
        unique = False
        while unique == False:
            self.uid = uuid.uuid4()
            if self.uid not in inv.listAllByUID.keys():
                inv.listAllByUID.update({self.uid:self})
                unique = True
        self.time_stamp = datetime.datetime.now()
        self.ID = ''
        self.kind = 'location'
        self.description = ''
        self.items = []
        
class inventory:
    def __init__(self):
        self.listAllCompanies = []
        self.listAllEmployees = []
        self.listAllRuns = []
        self.listAllBags = []
        self.listAllTotes = []
        self.listFinishedBags = []
        self.listFinishedTotes = []
        self.listAllUnfinishedProduct = []
        self.listAllFinishedProduct = []
        #self.listAllSources = []
        self.listAllContacts = []
        self.listAllDestinations = []
        self.listAllLocations = []
        self.listAllShipments = []
        self.listAllContainers = []
        self.listAllSoldProduct = []
        self.listAllTransactions = [] #All pending transactions
        self.listAllReciepts = [] #All closed transactions
        self.shipmentNumber = 0
        
        self.listAllCompaniesArchive = []
        self.listAllEmployeesArchive = []
        self.listAllRunsArchive = []
        self.listAllBagsArchive = []
        self.listAllTotesArchive = []
        self.listFinishedBagsArchive = []
        self.listFinishedTotesArchive = []
        self.listAllUnfinishedProductArchive = []
        self.listAllFinishedProductArchive = []
        #self.listAllSourcesArchive = []
        self.listAllContactsArchive = []
        self.listAllDestinationsArchive = []
        self.listAllLocationsArchive = []
        self.listAllShipmentsArchive = []
        self.listAllContainersArchive = []
        self.listAllSoldProductArchive = []
        self.listAllTransactionsArchive = [] #All pending transactions
        self.listAllRecieptsArchive = [] #All closed transactions
        
        self.listAllByUID = {}
  
inv = inventory() #define global inv

def load():
    global inv
    load = sdp.snackTime('data')
    inv = load.data() #load the inventory

def save():
    global inv
    save = sdp.pickleSession('data',inv)

if __name__!='__main__':
    if os.path.exists('../.zzz/data.zzz'):
        load()
    else:
        save()
        
