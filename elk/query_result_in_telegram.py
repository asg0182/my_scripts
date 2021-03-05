import os
import requests
import datetime, time
from elasticsearch import Elasticsearch


ES_HOST = os.getenv('ES_HOST')
ES_USER = os.getenv('ES_USER')
ES_PASSW = os.getenv('ES_PASSW')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_alert(msg):
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + msg
    response = requests.get(send_text)
    return response.json()


def main():

    now = datetime.datetime.now()
    now_int = int(time.mktime(now.timetuple()) * 1000)
    now_m2 = now - datetime.timedelta(minutes=1)
    now_m2_int = int(time.mktime(now_m2.timetuple()) * 1000)
    index = 'filebeat-*'
    login = ES_USER
    password = ES_PASSW
    query = {"query":
                 {"bool":
                      {"filter":
                          [
                              {"range":
                                   {"@timestamp":
                                        {"gte":now_m2_int,"lte":now_int,"format":"epoch_millis"}
                                    }
                               },
                              {"query_string":
                                   {"analyze_wildcard":True,"query":"OpenContract"}
                               }
                          ]
                      }
                 }
            }

    es = Elasticsearch(
        hosts=[ES_HOST],
        scheme='https',
        port=9200,
        use_ssl=True,
        verify_certs=False,
        http_auth=(login, password)
    )

    res = es.search(
        index=index,
        body=query
    )

    contract_count = res['hits']['total']['value']

    if contract_count < 5:
        send_alert("""
        Value is less then 5
        """)


if __name__=='__main__':
    main()
