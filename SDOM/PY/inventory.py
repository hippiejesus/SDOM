import classes as cl
import os
import logger

os.system('clear')

targetList = []
searchList = []
commands = {'container':['List containers',
                        {'product [index]':['list product at given index',
                                           {'unfinished [index]':'same as above'}]}],
            'finished product':['List finished product',
                               {'unfinished [index]':'same as above'}],
            'unfinished product':'List unfinished product',
            'runs':'List runs',
            'shipment':'List shipments',
            '&&CET+':'Set screen clear to TRUE',
            '&&CET-':'Set screen clear to FALSE',
            '~ [inn]':'add [inn] on to last querry',
            '< [inn]':'replace last number with [inn]',
            '<<< [inn]':'remove [inn] number of items from the last querry'}

def load():
    cl.load()
    
def save():
    cl.save()
    
def clearTargetList():
    global targetList
    targetList = []
    
def clearSearchList():
    global searchList
    searchList = []

def access(target):
    global targetList
    if 'container' in target:
        if 'product' in target:
            tsplit = target.split()
            searchContainer(int(tsplit[2]))
            try:
                if tsplit[3] == 'unfinished':
                    searchFinishedUnfinished(int(tsplit[4]))
            except:
                pass
        else:
            for item in cl.inv.listAllContainers:
                targetList.append(item)
                result = (str(item.ID) + ' : ' + str(item.kind) + ' -> ' + 
                    str(item.weight) + ' at index ' + str(targetList.index(item)))
                print(result)
                lg.write(result,noTime=True)
    if 'finished product' in target and 'unfinished product' not in target:
        if 'unfinished' in target:
            tsplit = target.split()
            searchFinishedUnfinished(int(tsplit[3]))
        else:
            for item in cl.inv.listAllFinishedProduct:
                targetList.append(item)
                result = (str(item.ID) + ' : ' + str(item.kind) + ' -> ' +
                      str(item.weight) + ' in ' + str(item.container.ID) +
                      ' at index ' + str(targetList.index(item)))
                print(result)
                lg.write(result,noTime=True)
    if 'unfinished product' in target:
        if 'runs' in target:#MUST FINISH
            tsplit = target.split()
            pass
        else:
            for item in cl.inv.listAllUnfinishedProduct:
                targetList.append(item)
                result = (str(item.ID) + ' : ' + str(item.owner) + 
                      ' -> ' + str(item.weight) +
                      ' at index ' + str(targetList.index(item)))
                print(result)
                lg.write(result,noTime=True)
    if 'runs' in target:
        if 'trim' in target:#MUST FINISH
            tsplit = target.split()
            pass
        else:
            for item in cl.inv.listAllRuns:
                for i in item[1]:
                    targetList.append(i)
                    trimList = []
                    for trim in i.trimIncluded:
                        trimList.append(str(trim.ID)+ ' : ' + str(i.trimAmounts) + ' <= ' + str(trim.trimWeight)+'/'+str(trim.ogTrimWeight))
                    result = (str(i.timeStart)+' >> '+str(i.ID) + ' <- ' + str(trimList)+str(targetList.index(i)))
                    print(result)
                    lg.write(result,noTime=True)
    if 'shipment' in target:
        if 'bags' in target:#MUST FINISH
            tsplit = target.split()
            pass
        else:
            for item in cl.inv.listAllShipments:
                targetList.append(item)
                weight = 0.00
                ogweight = 0.00
                for bag in item.bags:
                    weight += bag.trimWeight
                    ogweight += bag.ogTrimWeight
                result = (str(item.ID)+' <- '+str(item.source)+' : '+str(item.flavor)+' -- ' +str(item.dateIn) + ' == ' + str(weight)+'/'+str(ogweight))
                print(result)
                lg.write(result,noTime=True)
    elif 'CLR' in target:
        clearTargetList()
        clearSearchList()
        last = ''
        
        
def searchFinishedUnfinished(targetIndex):
    global targetList
    item = targetList[targetIndex]
    for i in item.unfinishedProductIncluded:
        targetList.append(i)
        runList = []
        for run in i.runsIncluded:
            runList.append(run.ID)
        if runList == []: runList.append(i.run)
        result = (str(i.ID) + ' : ' + str(i.intendedFinish) + ' <- ' + str(runList) + ' at index ' + str(targetList.index(i)))
        print(result)
        lg.write(result,noTime=True)

def searchContainer(targetIndex):
    global targetList
    item = targetList[targetIndex]
    for i in item.productIncluded:
        targetList.append(i)
        result = (str(i.ID) + ' : ' + str(i.kind) + ' -> ' + str(i.weight) + ' at index ' + str(targetList.index(i)))
        print(result)
        lg.write(result,noTime=True)
    
    
    
target = ''
inn = ''
clear_each_time = True
if __name__ == '__main__':
    lg = logger.log('inventory')
    
    while True:
        #try:
            last = target
            inn = raw_input('search --> ')
            
            if clear_each_time == True:
                os.system('clear')
            
            if inn == 'quit':
                lg.close()
                break
            elif '~' in inn:
                target = last+inn[1:]
            elif '<' in inn and '<<<' not in inn:
                targetSplit = target.split()
                targetSplit[-1] = inn[2:]
                target = ''
                for item in targetSplit:
                    target += item + ' '
            elif '<<<' in inn:
                targetSplit = target.split()
                innSplit = inn.split()
                for num in range(int(innSplit[1])):
                    targetSplit.pop(-1)
                target = ''
                for item in targetSplit:
                    target += item + ' '
            elif '&&HELP' in inn:
                print(str(commands))
            elif '&&CET+' in inn:
                clear_each_time = True
                target = ''
            elif '&&CET-' in inn:
                clear_each_time = False
                target = ''
            else:
                target = inn
            print('attempting: '+target)
            lg.write('attempting: '+target+'\n')
            access(target)
        #except:
            #print('error')
    
