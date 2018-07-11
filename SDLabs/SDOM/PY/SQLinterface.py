import os
import sys
import csv
import SDPickler as sdp
import emailMe
import backup
import sqlite3
import classes as cl
#Set pickler not to give messages
sdp.MODE = 'silent'

#Store the last query made
lastQuery = None

#Create dictionary for aliases
aliases = dict()

#Establish connection with the SDOM database
connection = sqlite3.connect('SDOM.db')
print('Connected to SDOM.db')

#Define the cursor object for this connection
cursor = connection.cursor()

#Load the local picklebase
cl.load()

#Uploads the current listAllCompanies to SDOM.db
def uploadListAllCompanies(archive = False):
    #define target list as cl.listAllCompanies
    if archive == False: 
        name = 'companies'
        tlist = cl.inv.listAllCompanies
    else:
        name = 'archive_companies'
        tlist = cl.inv.listAllCompaniesArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()
    
    for company in tlist:
        #Check to see if the companies table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,name,contacts,licenseNumber,notes,isBuyer,isSupplier)''')
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        c = company
        
        #Info to be uploaded for each object
        t.append(str(c.uid))
        t.append(str(c.time_stamp))
        t.append(c.name)
        con = list()
        for contact in c.contacts:
            con.append(contact.name)
        con = ','.join(con)
        t.append(con)
        t.append(c.licenseNumber)
        t.append(c.notes)
        t.append(c.isBuyer)
        t.append(c.isSupplier)
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE name=? AND licenseNumber=?',[c.name,c.licenseNumber])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))
     
#Uploads the current listAllEmployees to SDOM.db
def uploadListAllEmployees(archive = False):
    #define target list as cl.listAllEmployees
    if archive == False:
        name = 'employees'
        tlist = cl.inv.listAllEmployees
    else:
        name = 'archive_employees'
        tlist = cl.inv.listAllEmployeesArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()
    
    for employee in tlist:
        #Check to see if the employees table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,name,company,phone,email,position)''')
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        e = employee
        
        #Info to be uploaded for each object
        t.append(str(e.uid))
        t.append(str(e.time_stamp))
        t.append(e.name)
        t.append(e.company)
        t.append(e.phone)
        t.append(e.email)
        t.append(e.position)
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE name=? AND company=?',[e.name,e.company])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllRuns to SDOM.db
def uploadListAllRuns(archive = False):
    #define target list as cl.listAllRuns
    if archive == False:
        name = 'runs'
        tlist = cl.inv.listAllRuns
    else:
        name = 'archive_runs'
        tlist = cl.inv.listAllRunsArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()
    
    runList = list()
    for lis in tlist:
        for item in lis[1]:
            runList.append(item)
    for run in runList:
        #Check to see if the runs table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,ID,trimIncluded,trimAmounts,timeStart,owner,blaster)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        r = run
        
        #Info to be uploaded for each object
        t.append(str(r.uid))
        t.append(str(r.time_stamp))
        t.append(r.ID)
        trimIn = list()
        for tote in r.trimIncluded:
            trimIn.append(str(tote.ID))
        trimIn = ','.join(trimIn)
        t.append(trimIn)
        trimAm = list()
        for weight in r.trimAmounts:
            trimAm.append(str(weight))
        trimAm = ','.join(trimAm)
        t.append(trimAm)
        t.append(r.timeStart)
        t.append(str(r.owner))
        t.append(r.blaster)
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE ID=? AND owner=?',[r.ID,str(r.owner)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))
        

#Uploads the current listAllBags to SDOM.db
def uploadListAllBags(archive = False):
    #define target list as cl.listAllBags
    if archive == False:
        name = 'bags'
        tlist = cl.inv.listAllBags
    else:
        name = 'archive_bags'
        tlist = cl.inv.listAllBagsArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for bag in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,ID,shipment,owner,originalWeight,flavor)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        b = bag
        
        #Info to be uploaded for each object
        t.append(str(b.uid))
        t.append(str(b.time_stamp))
        t.append(str(b.ID))
        t.append(str(b.shipment.ID))
        t.append(str(b.owner))
        t.append(str(b.ogTrimWeight))
        t.append(str(b.flavor))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE ID=? AND owner=?',[str(b.ID),str(b.owner)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllTotes to SDOM.db
def uploadListAllTotes(archive = False):
    #define target list as cl.listAllTotes
    if archive == False:
        name = 'totes'
        tlist = cl.inv.listAllTotes
    else:
        name = 'archive_totes'
        tlist = cl.inv.listAllTotesArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for tote in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,ID,shipment,owner,currentWeight,originalWeight,flavor)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        b = tote
        
        #Info to be uploaded for each object
        t.append(str(b.uid))
        t.append(str(b.time_stamp))
        t.append(str(b.ID))
        t.append(str(b.shipment.ID))
        t.append(str(b.owner))
        t.append(str(b.trimWeight))
        t.append(str(b.ogTrimWeight))
        t.append(str(b.flavor))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE ID=? AND owner=?',[str(b.ID),str(b.owner)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllUnfinishedProduct to SDOM.db
def uploadListAllUnfinishedProduct(archive = False):
    #define target list as cl.listAllUnfinishedProduct
    if archive == False:
        name = 'unfinished'
        tlist = cl.inv.listAllUnfinishedProduct
    else:
        name = 'archive_unfinished'
        tlist = cl.inv.listAllUnfinishedProductArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for product in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,ID,intendedFinish,runsIncluded,owner)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        p = product
        
        #Info to be uploaded for each object
        t.append(str(p.uid))
        t.append(str(p.time_stamp))
        t.append(str(p.ID))
        t.append(str(p.intendedFinish))
        runs = list()
        for run in p.runsIncluded:
            runs.append(str(run.ID))
        t.append(','.join(runs))
        t.append(str(p.owner))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE ID=? AND owner=?',[str(p.ID),str(p.owner)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllFinishedProduct to SDOM.db
def uploadListAllFinishedProduct(archive = False):
    #define target list as cl.listAllFinishedProduct
    if archive == False:
        name = 'finished'
        tlist = cl.inv.listAllFinishedProduct
    else:
        name = 'archive_finished'
        tlist = cl.inv.listAllFinishedProductArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for product in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,ID,kind,runsIncluded,owner,container)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        p = product
        
        #Info to be uploaded for each object
        t.append(str(p.uid))
        t.append(str(p.time_stamp))
        t.append(str(p.ID))
        t.append(str(p.kind))
        up = list()
        for pro in p.unfinishedProductIncluded:
            for i in pro.runsIncluded:
                up.append(str(i.ID))
        t.append(','.join(up))
        t.append(str(p.owner))
        t.append(str(p.container.ID))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE ID=? AND owner=?',[str(p.ID),str(p.owner)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllContacts to SDOM.db
def uploadListAllContacts(archive = False):
    #define target list as cl.listAllContacts
    if archive == False:
        name = 'contacts'
        tlist = cl.inv.listAllContacts
    else:
        name = 'archive_contacts'
        tlist = cl.inv.listAllContactsArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for contact in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,name,phone,email,notes,companies,isPrimary)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        c = contact
        
        #Info to be uploaded for each object
        t.append(str(c.uid))
        t.append(str(c.time_stamp))
        t.append(str(c.name))
        t.append(str(c.phone))
        t.append(str(c.email))
        notes = list()
        for item in c.notes:
            notes.append(str(item))
        t.append(','.join(notes))
        companies = list()
        for company in c.companies:
            companies.append(str(company.name))
        t.append(','.join(companies))
        t.append(str(c.isPrimary))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE name=? AND phone=?',[str(c.name),str(c.phone)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllLocations to SDOM.db
def uploadListAllLocations(archive = False):
    #define target list as cl.listAllContacts
    if archive == False:
        name = 'locations'
        tlist = cl.inv.listAllLocations
    else:
        name = 'archive_locations'
        tlist = cl.inv.listAllLocationsArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for location in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,ID,description,items)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        l = location
        
        #Info to be uploaded for each object
        t.append(str(l.uid))
        t.append(str(l.time_stamp))
        t.append(str(l.ID))
        t.append(str(l.description))
        items = list()
        for item in l.items:
            items.append(str(item.ID))
        t.append(','.join(items))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE ID=?',[str(l.ID)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllShipments to SDOM.db
def uploadListAllShipments(archive = False):
    #define target list as cl.listAllShipments
    if archive == False:
        name = 'shipments'
        tlist = cl.inv.listAllShipments
    else:
        name = 'archive_shipments'
        tlist = cl.inv.listAllShipmentsArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for shipment in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,ID,source,bags,flavor,dateIn,totalWeight,totalPrice,testResults)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        s = shipment
        
        #Info to be uploaded for each object
        t.append(str(s.uid))
        t.append(str(s.time_stamp))
        t.append(str(s.ID))
        t.append(str(s.source))
        bags = list()
        for bag in s.bags:
            bags.append(str(bag.ID))
        t.append(','.join(bags))
        t.append(str(s.flavor))
        t.append(str(s.dateIn))
        t.append(str(s.totalWeight))
        t.append(str(s.totalPrice))
        t.append(str(s.testResults))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE ID=?',[str(s.ID)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllContainers to SDOM.db
def uploadListAllContainers(archive = False):
    #define target list as cl.listAllContainers
    if archive == False:
        name = 'containers'
        tlist = cl.inv.listAllContainers
    else:
        name = 'archive_containers'
        tlist = cl.inv.listAllContainersArchive
        
    if tlist == []:
        print('list empty')
        return
        
    
    uploadList = list()
    ommitList = list()

    for container in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,ID,kind,productIncluded,weight,isPackaged,unitSize,unitNumber,purpose,history)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        c = container
        
        #Info to be uploaded for each object
        t.append(str(c.uid))
        t.append(str(c.time_stamp))
        t.append(str(c.ID))
        t.append(str(c.kind))
        products = list()
        for product in c.productIncluded:
            products.append(str(product.ID))
        t.append(','.join(products))
        t.append(str(c.weight))
        t.append(str(c.isPackaged))
        t.append(str(c.unitSize))
        t.append(str(c.numberOfUnits))
        t.append(str(c.purpose))
        history = list()
        for item in c.history:
            history.append(str(item))
        t.append(','.join(history))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE ID=?',[str(c.ID)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllSoldProduct to SDOM.db
def uploadListAllSoldProduct(archive = False):
    #define target list as cl.listAllSoldProduct
    if archive == False:
        name = 'sold'
        tlist = cl.inv.listAllSoldProduct
    else:
        name = 'archive_sold'
        tlist = cl.inv.listAllSoldProductArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for product in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,ID,kind,container,totalPrice,unitPrice,unitsSold,paymentStatus)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        p = product
        
        #Info to be uploaded for each object
        t.append(str(p.uid))
        t.append(str(p.time_stamp))
        t.append(str(p.ID))
        t.append(str(p.kind))
        t.append(str(p.container.ID))
        t.append(str(p.totalPrice))
        t.append(str(p.unitPrice))
        t.append(str(p.unitsSold))
        if p.paymentStatus.amountToBePayed == 0.00:
            t.append('Paid')
        else:
            t.append('Pending: '+str(p.paymentStatus.amountToBePayed))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE ID=? AND container=?',[str(p.ID),str(p.container.ID)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllTransactions to SDOM.db
def uploadListAllTransactions(archive = False):
    #define target list as cl.listAllTransactions
    if archive == False:
        name = 'transactions'
        tlist = cl.inv.listAllTransactions
    else:
        name = 'archive_transactions'
        tlist = cl.inv.listAllTransactionsArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for transaction in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,recievingEntity,sendingEntity,paid,toBePaid,product)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        tr = transaction
        
        #Info to be uploaded for each object
        t.append(str(tr.uid))
        t.append(str(tr.time_stamp))
        t.append(str(tr.recievingEntity))
        t.append(str(tr.sendingEntity.name))
        t.append(str(tr.amountPayed))
        t.append(str(tr.amountToBePayed))
        t.append(str(tr.valuedEntity.ID))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE sendingEntity=? AND product=?',[str(tr.sendingEntity),str(tr.valuedEntity.ID)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#Uploads the current listAllReciepts to SDOM.db
def uploadListAllReciepts(archive = False):
    #define target list as cl.listAllReciepts
    if archive == False:
        name = 'reciepts'
        tlist = cl.inv.listAllReciepts
    else:
        name = 'archive_reciepts'
        tlist = cl.inv.listAllRecieptsArchive
        
    if tlist == []:
        print('list empty')
        return
    
    uploadList = list()
    ommitList = list()

    for reciept in tlist:
        #Check to see if the bags table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",[name])
        fetchall = cursor.fetchall()
        length = len(fetchall)
        if length == 0:
            print('creating table...')
            #Create the table if it does not exist
            cursor.execute('''CREATE TABLE '''+name+'''
                          (uid,time_stamp,sold,dateSold,buyer,seller,paymentRecieved,totalValue)''')
        
        #Define list in which all company info will be assembled.
        toSave = list()
        t = toSave
        r = reciept
        
        #Info to be uploaded for each object
        t.append(str(r.uid))
        t.append(str(r.time_stamp))
        products = list()
        for product in r.soldProductIncluded:
            products.append(str(product.ID))
        t.append(','.join(products))
        t.append(str(r.dateSold))
        t.append(str(r.transaction.sendingEntity))
        t.append(str(r.transaction.recievingEntity))
        t.append(str(r.paymentRecieved))
        t.append(str(r.totalValue))
        
        toSaveTuple = tuple(toSave)
        
        #Only insert item if the name and licensenumbers are new
        cursor.execute('SELECT * FROM '+name+' WHERE sold=? AND buyer=?',[','.join(products),str(r.transaction.sendingEntity)])
        fetchall = cursor.fetchall()
        if len(fetchall) == 0:
            uploadList.append(toSaveTuple)
        else:
            ommitList.append(toSaveTuple)
            #print(str(c.name)+' already in table!')
        
    #Insert list of tuples into SDOM.db
    try:
        cursor.executemany('INSERT INTO '+name+' VALUES (?,?,?,?,?,?,?,?)',uploadList)
        print('insertion successful...')
        
        #Commit changes
        connection.commit()
        print('the following entries were ommited...')
        for item in ommitList:
            print item
    except:
        print('Error: '+str(sys.exc_info()))

#execute from another program
def execute(query,inAlias = False):
    if inAlias != False:
        loadAliases(str(inAlias))
    cursor.execute(str(query))
    return cursor.fetchall()
    
def csvMe(command):
    query = None
    csplit = command.split()
    print('recieved csv request...')
    if csplit[0] == 'import':
        inAlias = csplit[1]
        csplit.pop(0)
        csplit.pop(0)
        fileName = csplit[0]
        csplit.pop(0)
        try:
            query = aliases[csplit[0]]
        except:
            print(str(sys.exc_info()))
    else: 
        inAlias = False
        fileName = csplit[0]
        csplit.pop(0)
        query = ' '.join(csplit)
    try:
        print('Creating file')
        with open('../CSV/'+str(fileName),'wb') as csvfile:
            print('writing...')
            writer = csv.writer(csvfile,delimiter=',')
            print('executing query')
            print(query)
            rowdata = execute(query,inAlias)
            names = list(map(lambda x: x[0], cursor.description))
            writer.writerow(names)
            for row in rowdata:
                writer.writerow(row)
    except:
        print(str(sys.exc_info()))
    
    
    print('task complete')
    if os.path.exists('../CSV/'+fileName):
        return fileName
    else:
        return False
        
    #resultList = execute(query,inAlias)
    
    

#Backs up the local drive and stores the path in the SQL database
def backupNow():
    #Check to see if the bags table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='backupPaths'")
    fetchall = cursor.fetchall()
    length = len(fetchall)
    if length == 0:
        print('creating table...')
        #Create the table if it does not exist
        cursor.execute('''CREATE TABLE backupPaths (path)''')
    backup.writeLog()
    path = backup.backup()
    cursor.execute("INSERT INTO backupPaths VALUES (?)",[str(path)])
    connection.commit()
    
#Restores current local database from the backup last uploaded to the backupPaths table
def restoreNow():
    pass

#Saves aliases for later use
def saveAliases(name):
    save = sdp.pickleSession(name,aliases)
    print('Aliases saved!')
    
def loadAliases(name):
    global aliases
    load = sdp.snackTime(name)
    aliases = load.data()
    print('Aliases loaded!')

#The Main Loop, allowing for command interpretation   
if __name__=='__main__':
    global lastQuery
    os.system('clear') 
    print(u'Howdy! Type \u001b[32m\u001b[1m"help()"\u001b[0m if you are confused!')
    while True:
        inn = raw_input(u'\u001b[33mSQLinterface>\u001b[0m ')
        innS = inn.split()
        if innS == []: innS = ['pass','pass']
        if innS[0] == 'upload':
            mod = False
            if 'archive' in inn:
                mod = True
            if innS[1] == 'companies':
                uploadListAllCompanies(mod)
            elif innS[1] == 'employees':
                uploadListAllEmployees(mod)
            elif innS[1] == 'runs':
                uploadListAllRuns(mod)
            elif innS[1] == 'bags':
                uploadListAllBags(mod)
            elif innS[1] == 'totes':
                uploadListAllTotes(mod)
            elif innS[1] == 'unfinishedProduct':
                uploadListAllUnfinishedProduct(mod)
            elif innS[1] == 'finishedProduct':
                uploadListAllFinishedProduct(mod)
            elif innS[1] == 'contacts':
                uploadListAllContacts(mod)
            elif innS[1] == 'locations':
                uploadListAllLocations(mod)
            elif innS[1] == 'shipments':
                uploadListAllShipments(mod)
            elif innS[1] == 'containers':
                uploadListAllContainers(mod)
            elif innS[1] == 'sold':
                uploadListAllSoldProduct(mod)
            elif innS[1] == 'transactions':
                uploadListAllTransactions(mod)
            elif innS[1] == 'reciepts':
                uploadListAllReciepts(mod)
            elif innS[1] == 'all':
                uploadListAllCompanies(mod)
                uploadListAllEmployees(mod)
                uploadListAllRuns(mod)
                uploadListAllBags(mod)
                uploadListAllTotes(mod)
                uploadListAllUnfinishedProduct(mod)
                uploadListAllFinishedProduct(mod)
                uploadListAllContacts(mod)
                uploadListAllLocations(mod)
                uploadListAllShipments(mod)
                uploadListAllContainers(mod)
                uploadListAllSoldProduct(mod)
                uploadListAllTransactions(mod)
                uploadListAllReciepts(mod)
        elif innS[0] == 'alias':
            try:
                innS.pop(0)
                key = innS[0]
                innS.pop(0)
            except:
                for item in aliases.keys():
                    print(item+' -> '+aliases[item])
                continue
            command = ' '.join(innS)
            if key in aliases.keys():
                print('Alias already occupied')
            else: 
                aliases.update({key:command})
                print('Alias added!')
        elif innS[0] == 'call':
            alias = innS[1]
            try:
                command = aliases[alias]
                lastQuery = command
            except:
                print('invalid alias.')
                continue
            try:
                cursor.execute(command)
            except: 
                print('invalid command.')
                continue
            print(u'\u001b[43mexecuting:\u001b[0m\u001b[37m "'+command+u'"\u001b[0m')
            names = list(map(lambda x: x[0], cursor.description))
            print (u'\u001b[1m'+str(names)+u'\u001b[0m')
            for item in cursor.fetchall():
                print(item)
        elif innS[0] == 'exit()':
            break
        elif innS[0] == 'clear()':
            os.system('clear')
        elif innS[0] == 'tables()':
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            for item in cursor.fetchall():
                print(item)
        elif innS[0] == 'help()':
            os.system('clear')
            print(u'\u001b[46mWelcome to the SDOM SQLinterface!\u001b[0m')
            print(u'\nType \u001b[32m\u001b[1m"upload"\u001b[0m followed by a category to update the database from the local drive.')
            print(u'Type \u001b[32m\u001b[1m"upload all"\u001b[0m to update the database with every list from the local inventory.')
            print(u'\nTo see a list of table names, type \u001b[32m\u001b[1m"tables()"\u001b[0m')
            print(u'To display contents from the tables, queries can be made with the \u001b[32m\u001b[1mexec\u001b[0m command.')
            print(u'Enter \u001b[32m\u001b[1m"exec"\u001b[0m followed by the SQL query of your choosing.')
            print(u'Par example: \u001b[1m"exec SELECT * FROM companies;"\u001b[0m')
            print(u'\nCommands may be saved as shorter aliases and called back later.')
            print(u'Par example: \u001b[1m"alias sc SELECT * FROM companies;"\u001b[0m')
            print(u'^^^This saves the command \u001b[1m"SELECT * FROM companies;"\u001b[0m under the alias \u001b[1msc\u001b[0m')
            print(u'To invoke this alias, enter \u001b[32m\u001b[1m"call\u001b[0m\u001b[1m sc\u001b[32m"\u001b[0m. Time saved!')
            print(u'Type \u001b[32m\u001b[1m"export"\u001b[0m followed by an identifier to save your current aliases.')
            print(u'Type \u001b[32m\u001b[1m"import"\u001b[0m followed by the identifier to load the aliases for further use.')
            print(u'Type \u001b[32m\u001b[1m"alias"\u001b[0m followed by nothing to see a list of current aliases.')
            print(u'\nType \u001b[32m\u001b[1m"csv"\u001b[0m followed by a filename ending in .csv followed by a query.')
            print(u'This will save the specified query as a tabulated csv file with the name specified.')
            print(u'Par example: \u001b[1m"csv tables.csv SELECT * FROM sqlite_master WHERE type="table"\u001b[0m')
            print(u'You may also enter  \u001b[32m\u001b[1m"csv"\u001b[0m followed by just a filename.')
            print(u'This will write the last query that was made with \u001b[32m\u001b[1m"exec"\u001b[0m or \u001b[32m\u001b[1m"call"\u001b[0m to csv.')
            print(u'\nType \u001b[32m\u001b[1m"mail"\u001b[0m followed by relevant information in the following order:')
            print(u'\u001b[1maddress | filename | subject')
            print(u'\u001b[0mPar example:\u001b[1m "mail test@test.com test.csv testing!"\u001b[0m') 
            print(u'\nType  \u001b[32m\u001b[1m"backup()"\u001b[0m to backup the local drive.')
            print(u'\nType  \u001b[32m\u001b[1m"restore()"\u001b[0m to restore the local drive from the last backup.')
            print(u'Type  \u001b[32m\u001b[1m"restore"\u001b[0m followed by the specified path to restore from a specific backup.')
            print(u'\nType \u001b[32m\u001b[1m"clear()"\u001b[0m to clear the screen to a blank prompt.')
            print(u'Type \u001b[32m\u001b[1m"exit()"\u001b[0m to quit this application.')
            print(u'\u001b[46m\nEnjoy searching!!!\u001b[0m')
        elif innS[0] == 'csv':
            innS.pop(0)
            if len(innS)==1:
                fileName = csvMe(innS[0]+' '+lastQuery)
            else:
                command = ' '.join(innS)
                fileName = csvMe(command)
            print('Resulting File: '+str(fileName))
        elif innS[0] == 'mail':
            #emailMe.py | address | subject | filename | password
            #emailMe.py | address | filename| subject  | password
            args = list()
            args.append('emailMe.py')
            args.append(str(innS[1]))
            args.append(str(innS[3]))
            args.append(str(innS[2]))
            args.append('sdope101')
            emailMe.main(args)
        elif innS[0] == 'backup()':
            backupNow()
        elif innS[0] == 'restore()':
            restoreNow()
        elif innS[0] == 'export':
            saveAliases(innS[1])
        elif innS[0] == 'import':
            loadAliases(innS[1])
        elif innS[0] == 'exec':
            innS.pop(0)
            command = ' '.join(innS)
            lastQuery = command
            try:
                cursor.execute(command)
            except: 
                print('invalid command.')
                continue
            print(u'\u001b[43mexecuting:\u001b[0m\u001b[37m "'+command+u'"\u001b[0m')
            names = list(map(lambda x: x[0], cursor.description))
            print (u'\u001b[1m'+str(names)+u'\u001b[0m')
            for item in cursor.fetchall():
                print(item)
        
    #Close the database connection after all procedures have been run.
    connection.close()
    

        
