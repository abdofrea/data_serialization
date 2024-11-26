import CALL_DETAILS_SCHEMA_pb2 as cdrs_pb2
import os, json
from google.protobuf.json_format import MessageToDict
from datetime import datetime

ORIGINAL_FILEs_DIR = '/media/sf_D_DRIVE/Data_Serialization/CDRs_Generator/original_cdrs'
PROTOBUF_ENCODED_FILEs = '/media/sf_D_DRIVE/Data_Serialization/PROTOBUF_ENCODER_DECODER/PROTOBUF_ENCODED'
PROTOBUF_DECODED_FILEs = '/media/sf_D_DRIVE/Data_Serialization/PROTOBUF_ENCODER_DECODER/PROTOBUF_DECODED'

################## Encoded
start_encoding_time = datetime.now()
print('Start Encoding',start_encoding_time)

all_files = os.listdir(ORIGINAL_FILEs_DIR)
for each_file in all_files:
    # print(each_file)
    json_objs = json.load(open(os.path.join(ORIGINAL_FILEs_DIR,each_file)))
    cdrs_list = cdrs_pb2.CDRsList()
    for elem in json_objs:
        call_detail_record = cdrs_pb2.CallDetailRecord()
        call_detail_record.recordID = int(elem['CallDetailRecord']['recordID'],16)
        call_detail_record.callStartTime = elem['CallDetailRecord']['callStartTime']
        if elem['CallDetailRecord']['recordType'] == 'voice':
            call_detail_record.callDuration = elem['CallDetailRecord']['callDuration']
            call_detail_record.callEndTime = elem['CallDetailRecord']['callEndTime']
        call_detail_record.calledPartyNumber = elem['CallDetailRecord']['calledPartyNumber']
        call_detail_record.callingPartyNumber = elem['CallDetailRecord']['callingPartyNumber']
        call_detail_record.isRoaming = elem['CallDetailRecord']['isRoaming']
        call_detail_record.mscID = elem['CallDetailRecord']['mscID']
        call_detail_record.recordType = cdrs_pb2.CallDetailRecord.VOICE if elem['CallDetailRecord']['recordType'] == 'voice' else cdrs_pb2.CallDetailRecord.SMS
        call_detail_record.callType = cdrs_pb2.CallDetailRecord.INCOMING if elem['CallDetailRecord']['callType'] == 'incoming' else cdrs_pb2.CallDetailRecord.OUTGOING
        # callType = 'INCOMING' if elem['CallDetailRecord']['callType'] == 'incoming' else 'OUTGOING'

        location_info = cdrs_pb2.LocationInfo()
        location_info.cellID = elem['CallDetailRecord']['locationInformation']['cellID']
        location_info.locationAreaCode = elem['CallDetailRecord']['locationInformation']['locationAreaCode']
        location_info.mcc = elem['CallDetailRecord']['locationInformation']['mcc']
        location_info.mnc = elem['CallDetailRecord']['locationInformation']['mnc']
        call_detail_record.locationInformation.CopyFrom(location_info)

        event_record = cdrs_pb2.EventRecord()
        event_record.callDetailRecord.CopyFrom(call_detail_record)
        cdrs_list.eventRecords.append(event_record)
    with open(os.path.join(PROTOBUF_ENCODED_FILEs,each_file.replace('json','ber')), "wb") as file:
        serialized_data = cdrs_list.SerializeToString()
        file.write(serialized_data)


############ Decoding
start_decoding_time = datetime.now()
print('Start Decoding',start_decoding_time)


all_files = os.listdir(PROTOBUF_ENCODED_FILEs)

for each_file in all_files:
    # print(each_file)
    with open(os.path.join(PROTOBUF_ENCODED_FILEs,each_file), 'rb') as reader_binary:
        decoded_cdrs = cdrs_pb2.CDRsList()
        decoded_cdrs.ParseFromString(reader_binary.read())
    with open(os.path.join(PROTOBUF_DECODED_FILEs,each_file.replace('ber','json')), 'w') as output:
        for record in decoded_cdrs.eventRecords:
            output_dict = MessageToDict(record)
            output_dict['callDetailRecord'].setdefault('recordType', 'VOICE')
            output_dict['callDetailRecord'].setdefault('callType', 'INCOMING')
            json.dump(output_dict, output, indent=4)

end_time = datetime.now()
print('Protobuf encoding_time', start_decoding_time-start_encoding_time)
print('Protobuf decoding_time', end_time - start_decoding_time)