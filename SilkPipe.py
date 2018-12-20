import silk
import json
from kafka import KafkaProducer
import logging

logging.basicConfig(filename='/data/silk/log/producer.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# Notice:
# before you produce data into kafka
# you should create a topic at web-ui at first.
producer = KafkaProducer(bootstrap_servers=['','',''],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                         sasl_plain_username = '',
                         sasl_plain_password = '',
                         security_protocol = "SASL_PLAINTEXT",
                         sasl_mechanism='PLAIN')


def json_format(rec):
    global rec_to_json
    rec_to_json = dict()
    rec_to_json['sip'] = str(rec.sip)
    rec_to_json['sport'] = rec.sport
    rec_to_json['dip'] = str(rec.dip)
    rec_to_json['dport'] = rec.dport
    rec_to_json['proto'] = rec.protocol
    rec_to_json['start_time'] = rec.stime_epoch_secs
    if rec.tcpflags:
        rec_to_json['flags'] = str(rec.tcpflags)
    else:
        rec_to_json['flags'] = ""
    rec_to_json['end_time'] = rec.etime_epoch_secs
    rec_to_json['duration'] = rec.duration_secs
    # force convert is avoiding for json format error
    rec_to_json['bytes'] = float(rec.bytes)
    rec_to_json['packets'] = float(rec.packets)
    rec_to_json['sensor'] = str(rec.sensor)
    line = str(rec_to_json).replace("'", '"')
    silk_json_data = json.loads(line)
    # todo Trying to use https://msgpack.org/ instead of json format
    # Improving the efficiency
    try:
        future = producer.send('sec-log-' + rec_to_json['sensor'], silk_json_data)
    except Exception as e:
        logging.warning(e)

register_filter(json_format)
