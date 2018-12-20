from kafka import KafkaConsumer
import elasticsearch5
import json
from datetime import datetime
import logging
logging.basicConfig(filename='/data/silk/log/consumer.log', filemode='w+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
es = elasticsearch5.Elasticsearch(["", ""], http_auth=('username', 'password'))
consumer = KafkaConsumer("sec-log-S0",
                         bootstrap_servers=['', '', ''],
                         group_id="group1",
                         sasl_plain_username='',
                         sasl_plain_password='',
                         security_protocol="SASL_PLAINTEXT",
                         sasl_mechanism='PLAIN')
for msg in consumer:
    es_value = dict()
    es_value = json.loads(msg.value)
    # transfer the time format to adapt the ES
    # unify the utc time for the right time line
    # the kibana will +8 automatically
    es_value['start_time'] = datetime.utcfromtimestamp(es_value['start_time'])
    es_value['end_time'] = datetime.utcfromtimestamp(es_value['end_time'])
    try:
        es.index(index='sec-log-silk-'+datetime.now().strftime("%Y-%m-%d"), doc_type='record', body=es_value, id=None)
    except Exception as e:
        logging.warning(e)
