import classes as cl
cl.load()
ID = raw_input('ID: ')
description = raw_input('description: ')
loc = cl.location()
loc.ID = ID
loc.description = description
cl.inv.listAllLocations.append(loc)
cl.save()
print('Location added!')
