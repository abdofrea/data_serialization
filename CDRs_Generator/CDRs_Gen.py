import os.path
from datetime import datetime, timedelta
import json, pprint
import random
import time


PREFIX = '21899'
RECORD_TYPE = ['voice', 'sms'] # Voice, SMS
MSCIDs = ['218999999001','218999999002','218999999003','218999999004','218999999005']

def make_record_id(integer): ### Some function that combin the timestamp with file counter id
    init = str(str(int(time.time()))+f"{integer*random.randrange(2,5):04}")[::-1]
    swapped = [init[13-j]+init[j] for j in range(0,len(init))]
    swapped.reverse()
    swapped = ''.join(swapped)[:14]
    return(hex(int(swapped)))

def make_LocationInfo():
    return {
        'cellID': random.choice([x for x in range(1000)]),
        'locationAreaCode': random.choice([x for x in range(100)]),
        'mcc': 606,
        'mnc': 99,
    }

log_file = open('CDRs_Gen_LOGs.csv','w')

z = 0
while z <= 150:
    z+=1
    print(z)
    CDRs = []
    for i in range(0,random.randrange(4000,4500)):
        recordType = random.choice(RECORD_TYPE)
        callStartTime = datetime.now() - timedelta(seconds=random.randrange(0, 240))
        CallDetailRecord = {
            'CallDetailRecord':{
                'recordType':recordType,
                'recordID':make_record_id(i),
                'callingPartyNumber':PREFIX+f"{random.randrange(0,9999999):07}",
                'calledPartyNumber': PREFIX + f"{random.randrange(0, 9999999):07}",
                'callStartTime':str(callStartTime.strftime("%Y-%m-%d %H:%M:%S")),
                'callType':random.choice(['incoming','outgoing']), # Outgoing, Incoming
                'isRoaming' : bool(random.random() < 0.08), # assuming only 8% of the calls are for roaming,
                'mscID': random.choice(MSCIDs),
                'locationInformation': make_LocationInfo()}
        }
        if recordType == 'voice':
            callDuration = random.randrange(0,1800)
            callEndTime = callStartTime + timedelta(seconds=callDuration)
            CallDetailRecord['CallDetailRecord'].setdefault('callDuration',callDuration)
            CallDetailRecord['CallDetailRecord'].setdefault('callEndTime', str(callEndTime.strftime("%Y-%m-%d %H:%M:%S")))
        CDRs.append(CallDetailRecord)
        counter = i
    file_timestamp =  str(datetime.now().strftime("%Y%m%d%H%M%S"))
    file_name = f"CALLCDRS-{file_timestamp}-{z:04}.json"
    log_file.write(str(file_name)+','+str(counter)+'\n')
    with open(os.path.join('original_cdrs',file_name),'w') as output:
        json.dump(CDRs, output, indent = 4)

