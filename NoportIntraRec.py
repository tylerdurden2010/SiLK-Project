import sys
import pymongo

class jsonFormat():
    def __init__(self):
        self.MongoDB = pymongo.MongoClient("mongodb://Data:Password@IP:Port/DbName?authMechanism=SCRAM-SHA-1").Dbname

    def send(self,rec):
        self.MongoDB.IntraNoPortConnection.insert(rec)

j = jsonFormat()


filename = sys.argv[1]
if filename:
    filehandle = open(filename)
    line = filehandle.readline().strip()
    while(line):
        rec = dict()
        tempList = line.split('|')
        rec['sip'] = tempList[0]
        rec['dip'] = tempList[1]
        rec['startTime'] = int(tempList[2])
        rec['durationTime'] = int(tempList[3])
        j.send(rec)
        line = filehandle.readline().strip()
else:
    exit(0)
