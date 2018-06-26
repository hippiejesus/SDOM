import classes as cl

cl.load()

cl.inv.listAllCompaniesArchive = []
cl.inv.listAllEmployeesArchive = []
cl.inv.listAllRunsArchive = []
cl.inv.listAllBagsArchive = []
cl.inv.listAllTotesArchive = []
cl.inv.listFinishedBagsArchive = []
cl.inv.listFinishedTotesArchive = []
cl.inv.listAllUnfinishedProductArchive = []
cl.inv.listAllFinishedProductArchive = []
#cl.inv.listAllSourcesArchive = []
cl.inv.listAllContactsArchive = []
cl.inv.listAllDestinationsArchive = []
cl.inv.listAllLocationsArchive = []
cl.inv.listAllShipmentsArchive = []
cl.inv.listAllContainersArchive = []
cl.inv.listAllSoldProductArchive = []
cl.inv.listAllTransactionsArchive = [] #All pending transactions
cl.inv.listAllRecieptsArchive = [] #All closed transactions

cl.save()
print('save success')
