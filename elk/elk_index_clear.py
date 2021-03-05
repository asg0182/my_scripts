import argparse
import datetime
from elasticsearch import Elasticsearch


def create_parser():
    parser = argparse.ArgumentParser(description='CLear Elk index')
    parser.add_argument('--login', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--indices', action="extend", nargs="+", type=str, required=True)
    parser.add_argument('--dry', type=bool, default=False, required=False)
    parser.add_argument('--query-operator', default='lte', type=str, required=False)
    parser.add_argument('--query-datetime', type=str, required=False)
    return parser


def delete_by_query(es, index, query, dry):
    if dry:
        res = es.search(
            index=index,
            body=query
        )
    else:
        res = es.delete_by_query(
            index=index,
            body=query
        )

    print(res)


def main():
    args = create_parser().parse_args()
    login = args.login
    password = args.password
    index_list = args.indices
    dry = args.dry
    query_operator = args.query_operator
    query_datetime = args.query_datetime

    if not query_datetime:
        query_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(query_datetime)

    es = Elasticsearch(
        hosts=['m1k8sdlel01.lsp.team'],
        scheme='https',
        port=9200,
        use_ssl=True,
        verify_certs=False,
        http_auth=(login, password)
    )

    _query = '{"query":{"bool":{"filter":{"range": {"@timestamp": {"' + query_operator + \
             '": "' + query_datetime + '","format": "yyyy-MM-dd HH:mm:ss"}}}}}}'

    for index_name in index_list:
        delete_by_query(es, index_name, _query, dry)


if __name__=='__main__':
    main()
