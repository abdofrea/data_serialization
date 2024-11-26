from fastavro import writer, reader, parse_schema
import json, os
from datetime import datetime

ORIGINAL_FILEs_DIR = '/media/sf_D_DRIVE/Data_Serialization/CDRs_Generator/original_cdrs'
AVRO_ENCODED_FILEs = '/media/sf_D_DRIVE/Data_Serialization/AVRO_ENCODE_DECODE/AVRO_ENCODED_FILEs'
AVRO_DECODED_FILEs = '/media/sf_D_DRIVE/Data_Serialization/AVRO_ENCODE_DECODE/AVRO_DECODED_FILEs'

########### Encoding
start_encoding_time = datetime.now()
print('Start Encoding',start_encoding_time)

all_files = os.listdir(ORIGINAL_FILEs_DIR)
schema = json.load(open('CALL_CDRs_SCHEMA.avsc'))
parsed_schema = parse_schema(schema)
for each_file in all_files:
    print(each_file)
    t1 = datetime.now()
    json_reader = json.load(open(os.path.join(ORIGINAL_FILEs_DIR,each_file)))
    avro_obj = {"CDRsList":[]}
    for elem in json_reader:
        CallDetailRecord = {"callDetailRecord": {
            "recordType": elem['CallDetailRecord']['recordType'],
            "recordID": int(elem['CallDetailRecord']['recordID'],16),
            "callingPartyNumber": elem['CallDetailRecord']['callingPartyNumber'],
            "calledPartyNumber": elem['CallDetailRecord']['calledPartyNumber'],
            "callStartTime": elem['CallDetailRecord']['callStartTime'],
            "callType": elem['CallDetailRecord']['callType'],  # Outgoing, Incoming
            "isRoaming": bool(elem['CallDetailRecord']['isRoaming']),
            "mscID": elem['CallDetailRecord']['mscID'],
            "locationInformation": elem['CallDetailRecord']['locationInformation'] }}
        if elem['CallDetailRecord']['recordType'] == 'voice':
            CallDetailRecord['callDetailRecord'].setdefault('callDuration', elem['CallDetailRecord']['callDuration'])
            CallDetailRecord['callDetailRecord'].setdefault('callEndTime', elem['CallDetailRecord']['callEndTime'])
        avro_obj['CDRsList'].append(CallDetailRecord)

    with open(os.path.join(AVRO_ENCODED_FILEs,each_file.replace('json','avro')), 'wb') as out:
        records = [avro_obj]
        writer(out, parsed_schema, records)



######### Decode
start_decoding_time = datetime.now()
print('Start Decode',start_decoding_time)

all_files = os.listdir(AVRO_ENCODED_FILEs)
for each_file in all_files:
    print(each_file)
    with open(os.path.join(AVRO_ENCODED_FILEs,each_file),'rb') as avro_file:
        with open(os.path.join(AVRO_DECODED_FILEs, each_file.replace('avro', 'json')), 'w') as output:
            for elem in reader(avro_file):
                json.dump(elem, output, indent=4)


end_time = datetime.now()
print('Avro encoding_time', start_decoding_time-start_encoding_time)
print('Avro decoding_time', end_time - start_decoding_time)