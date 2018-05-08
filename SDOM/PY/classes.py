import SDPickler as sdp
import os

UIstem = '../UI/'

class company:
    def __init__(self):
        self.name = ''
        self.sources = []
        self.contacts = []
        self.licenseNumber = ''
        self.destinations = []
        self.notes = []

class contact:
    def __init__(self):
        self.name = ''
        self.phone = ''
        self.notes = []
        self.email = ''
        self.companies = []
        
class source:
    def __init__(self):
        self.name = ''
        self.contacts = [] #list of contact objects
        self.licenseNumber = ''
        self.notes = []
        
class trimBag:
    def __init__(self):
        self.ID = ''
        self.shipment = ''
        self.owner = ''
        self.trimWeight = 0.00
        self.ogTrimWeight = 0.00
        self.flavor = ''
        self.location = '' #location object
        self.testResults = []
        inProcess = False
  
class shipment:
    def __init__(self):
        self.source = '' #company object
        self.ID = ''
        self.bags = []
        self.flavor = ''
        self.dateIn = ''
        self.locations = [] #list of location objects
        
        
class run:
    def __init__(self):
        self.ID = ''
        self.trimIncluded = []
        self.trimAmounts = []
        self.machine = ''
        self.weightYield = 0.0
        self.timeStart = ''
        self.owner = ''
        
class unfinishedProduct:
    def __init__(self):
        self.ID = ''
        self.runsIncluded = []
        self.run = ''
        self.owner = ''
        self.intendedFinish = ''
        self.machine = ''
        self.testResults = []
        self.weight = 0.00
  
class container:
    def __init__(self):
        self.ID = ''
        self.productIncluded = []
        self.kind = ''
        self.weight = 0.00
        
class finishedProduct:
    def __init__(self):
        self.ID = ''
        self.unfinishedProductIncluded = []
        self.finishedProductIncluded = []
        self.kind = ''
        self.weight = 0.00
        self.grade = ''
        self.container = ''
        self.testResults = []
        

        
class location:
    def __init__(self):
        self.ID = ''
        self.description = ''
        self.items = []
        
class inventory:
    def __init__(self):
        self.listAllRuns = []
        self.listAllBags = []
        self.listAllUnfinishedProduct = []
        self.listAllFinishedProduct = []
        self.listAllSources = []
        self.listAllContacts = []
        self.listAllDestinations = []
        self.listAllLocations = []
        self.listAllCompanies = []
        self.listAllShipments = []
        self.listFinishedBags = []
        self.listAllContainers = []
        self.shipmentNumber = 0
  
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
        
