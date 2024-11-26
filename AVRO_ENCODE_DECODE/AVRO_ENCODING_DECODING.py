import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import json, os
from datetime import datetime

ORIGINAL_FILEs_DIR = 'D://Data_Serialization//CDRs_Generator//original_cdrs'
AVRO_ENCODED_FILEs = 'D:\Data_Serialization\AVRO_ENCODE_DECODE\AVRO_ENCODED_FILEs'
AVRO_DECODED_FILEs = 'D:\Data_Serialization\AVRO_ENCODE_DECODE\AVRO_DECODED_FILEs'


############ Encoding
start_encoding_time = datetime.now()
print('Start Encoding',start_encoding_time)

all_files = os.listdir(ORIGINAL_FILEs_DIR)
schema = avro.schema.parse(open("CALL_CDRs_SCHEMA.avsc", "rb").read())
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

    writer = DataFileWriter(open(os.path.join(AVRO_ENCODED_FILEs,each_file.replace('json','avro')), "wb"), DatumWriter(), schema)
    writer.append(avro_obj)
    writer.close()

############ Decoding
start_decoding_time = datetime.now()
print('Start Decoding',start_decoding_time)

all_files = os.listdir(AVRO_ENCODED_FILEs)
for each_file in all_files:
    print(each_file)
    reader = DataFileReader(open(os.path.join(AVRO_ENCODED_FILEs,each_file), "rb"), DatumReader())
    with open(os.path.join(AVRO_DECODED_FILEs,each_file.replace('avro','json')),'w') as output:
        for elem in reader:
            json.dump(elem,output, indent = 4)
    reader.close()

end_time = datetime.now()
print('encoding_time', start_decoding_time-start_encoding_time)
print('decoding_time', end_time - start_decoding_time)