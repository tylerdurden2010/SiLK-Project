import sys
import silk
import json
import pymongo

class jsonFormat():
    def __init__(self):
        self.MongoDB = pymongo.MongoClient("mongodb://Username:Password@IP:Port/DBName?authMechanism=SCRAM-SHA-1").DBName

    def send(self,rec):
	    a = dict()
        #I mean to switch the dip and sip
	    #because I rw file what I generated is switchd format
	    #be care of theses
        a['sip'] = str(rec.dip)
        a['dip'] = str(rec.sip)
        a['sport'] = rec.dport
        a['dport'] = rec.sport
        a['startTime'] = rec.stime_epoch_secs
        a['endTime'] = rec.etime_epoch_secs
        a['durationTime'] = rec.duration.secs
        self.MongoDB.OutConnection.insert(a)

j = jsonFormat()

register_filter(j.send)