import csv
import fileops

stashdict = {}
stashdict['yarn'] = {}

with open ('stash.csv',encoding = 'utf-8-sig') as file:
    reader = csv.reader(file, delimiter=',')
    #next(reader,None)
    for row in reader:
        name = row[0]
        thickness = row[1]
        weight = float(row[3])
        length = float(row[4])
        stashdict['yarn'][name] = {}

for yarn in stashdict['yarn']:
    stashdict['yarn'][yarn]['weight'] = weight
    stashdict['yarn'][yarn]['fibertype'] = None
    stashdict['yarn'][yarn]['length'] = length
    stashdict['yarn'][yarn]['twist'] = None
    stashdict['yarn'][yarn]['thickness'] = thickness
    stashdict['yarn'][yarn]['source'] = None

print(stashdict['yarn']["'﻿Debbie BlissCashmerino ChunkyBlue'"]['weight'])
#
# s = fileops.FileOps()
# s.save_data(stashdict,'Stash')
