from datetime import datetime
import hashlib, sys, json, boto3, logging

LOGGER = logging.getLogger(__name__)

def main(event, environment):

    LOGGER.info(event)

    data_stream = environment['DATA_STREAM']
    try:
        output = []
        for record in event['Records']:
            if record['eventName'] in ['INSERT', 'MODIFY']:
                converted_record = unmarshal_dynamodb_json(record['dynamodb']['NewImage'])
                converted_record['streaming_timestamp'] = datetime.utcnow()
            elif record['eventName'] == 'REMOVE':
                pass

        if len(output) > 0:
            partition_key = hashlib.md5(json.dumps(output).encode()).hexdigest()
            LOGGER.info(f"this is output: {output}")
            put_batch_data_stream(output, partition_key, data_stream)


    except Exception as e:
        LOGGER.error(str(e), exc_info=True)
        sys.exit(1)

def unmarshal_dynamodb_json(node):
    data = dict({})
    data['M'] = node
    return unmarshal_value(data)

def unmarshal_value(node):
    if type(node) is not dict:
        return node

    for key, value in node.items():
        # S – String - return string
        # N – Number - return int or float (if includes '.')
        # B – Binary - not handled
        # BOOL – Boolean - return Bool
        # NULL – Null - return None
        # M – Map - return a dict
        # L – List - return a list
        # SS – String Set - not handled
        # NN – Number Set - not handled
        # BB – Binary Set - not handled
        key = key.lower()
        if key == 'bool':
            return value
        if key == 'null':
            return None
        if key == 's':
            return value
        if key == 'n':
            if '.' in str(value):
                return float(value)
            return int(value)
        if key in ['m', 'l']:
            if key == 'm':
                data = {}
                for key1, value1 in value.items():
                    if key1.lower() == 'l':
                        data = [unmarshal_value(n) for n in value1]
                    else:
                        if type(value1) is not dict:
                            return unmarshal_value(value)
                        data[key1] = unmarshal_value(value1)
                return data
            data = []
            for item in value:
                data.append(unmarshal_value(item))
            return data
        
def put_batch_data_stream(output, partition_key, data_stream_name):

    client = boto3.client('kinesis')
    records = []
    count = 1
    for observation in output:
        if count % 20 == 0:
            client.put_records(
                StreamName=data_stream_name,
                Records= records
            )
            records.clear()
        record = {
            "Data": json.dumps(observation) + '\n',
             'PartitionKey': partition_key
        }
        records.append(record)
        count = count + 1

    if len(records) > 0:
        client.put_records(
                StreamName=data_stream_name,
                Records= records
            )