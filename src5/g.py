from os import listdir
from os.path import isfile, join

mypath = "C:/Users/parveshgoyal/OneDrive - Nagarro/bned/d-zone/production support/PROD-2072/production/download"
mypath1 = "C:/Users/parveshgoyal/OneDrive - Nagarro/bned/d-zone/production support/PROD-2072/production"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

with open(mypath1 + "/order-sales-029-20201217151000", "w", encoding="utf-8", newline='\n') as f0:
    for f in listdir(mypath):
        if isfile(join(mypath, f)):
            print("writing " + join(mypath, f))
            with open(join(mypath, f), "r", encoding="utf-8") as f:
                while True:
                    c = f.readline()
                    if not c:
                        break
                    f0.write(c)

