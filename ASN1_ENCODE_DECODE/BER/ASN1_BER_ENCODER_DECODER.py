import asn1tools
import json, os, pprint
from datetime import datetime

ORIGINAL_FILEs_DIR = 'D:\Data_Serialization\CDRs_Generator\original_cdrs'
BER_ENCODED_DIR = 'D:\Data_Serialization\ASN1_ENCODE_DECODE\BER\ASN1_BER_ENCODED'
BER_DECODED_DIR = 'D:\Data_Serialization\ASN1_ENCODE_DECODE\BER\ASN1_BER_DECODED'

# ORIGINAL_FILEs_DIR = '/media/sf_D_DRIVE/Data_Serialization/CDRs_Generator/original_cdrs'
# BER_ENCODED_DIR = '/media/sf_D_DRIVE/Data_Serialization/ASN1_ENCODE_DECODE/BER/ASN1_BER_ENCODED'
# BER_DECODED_DIR = '/media/sf_D_DRIVE/Data_Serialization/ASN1_ENCODE_DECODE/BER/ASN1_BER_DECODED'

################# Encoding
start_encoding_time = datetime.now()
print('Start Encoding',start_encoding_time)

ENCODING_TYPE = 'ber'
codex = asn1tools.compile_files('CALL_CDR_SCHEMA.asn', ENCODING_TYPE)
all_original_files = list(os.listdir(ORIGINAL_FILEs_DIR))
for each_file in all_original_files:
    print(each_file)
    json_objs = json.load(open(os.path.join(ORIGINAL_FILEs_DIR,each_file)))
    output_file = open(os.path.join(BER_ENCODED_DIR,each_file.replace('json','ber')),'wb')
    CDRsList = []
    for elem in json_objs:
        CallDetailRecord = {
            'recordType': elem['CallDetailRecord']['recordType'],
            'recordID': int(elem['CallDetailRecord']['recordID'],16),
            'callingPartyNumber': elem['CallDetailRecord']['callingPartyNumber'],
            'calledPartyNumber': elem['CallDetailRecord']['calledPartyNumber'],
            'callStartTime': datetime.strptime(elem['CallDetailRecord']['callStartTime'],"%Y-%m-%d %H:%M:%S"),
            'callType': elem['CallDetailRecord']['callType'],  # Outgoing, Incoming
            'isRoaming': bool(elem['CallDetailRecord']['isRoaming']),  # assuming only 8% of the calls are for roaming,
            'mscID': elem['CallDetailRecord']['mscID'],
            'locationInformation': elem['CallDetailRecord']['locationInformation']
            }
        if elem['CallDetailRecord']['recordType'] == 'voice':
            CallDetailRecord.setdefault('callDuration', elem['CallDetailRecord']['callDuration'])
            CallDetailRecord.setdefault('callEndTime', datetime.strptime(elem['CallDetailRecord']['callEndTime'],("%Y-%m-%d %H:%M:%S")))
        CDRsList.append(tuple(['callDetailRecord',CallDetailRecord]))

    encoded = codex.encode('CDRsList',CDRsList)
    output_file.write(encoded)
    output_file.close()


#################### Decoding
start_decoding_time = datetime.now()
print('Start Decoding')
all_binary_files = os.listdir(BER_ENCODED_DIR)
codex = asn1tools.compile_files('CALL_CDR_SCHEMA.asn', 'ber') ## BER or PER

for each_file in all_binary_files:
    print(each_file)
    binary_file = open(os.path.join(BER_ENCODED_DIR,each_file),'rb').read()
    decoded_obj = codex.decode('CDRsList',binary_file)
    with open(os.path.join(BER_DECODED_DIR,each_file.replace('per','json')),'w') as output:
        pprint.pprint(decoded_obj, stream=output)

end_time = datetime.now()
print('encoding_time', start_decoding_time-start_encoding_time)
print('decoding_time', end_time - start_decoding_time)