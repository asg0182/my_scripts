import re
import argparse
from webdav3.client import Client
from tabulate import tabulate


def create_parser():
    parser = argparse.ArgumentParser(description='Add dashboards to Grafana')
    parser.add_argument('--login', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--webdav-url', type=str, required=True)
    parser.add_argument('--webdav-path', type=str, required=True)
    parser.add_argument('--pattern', type=str, required=True)
    return parser


def main():
    args = create_parser().parse_args()
    webdav_url = args.webdav_url
    webdav_path = args.webdav_path
    pattern = args.pattern
    login = args.login
    password = args.password

    options = {
        'webdav_hostname': webdav_url,
        'webdav_login': login,
        'webdav_password': password
    }

    client = Client(options)
    client.verify = False

    not_matched_files = {}

    for dir in client.list(webdav_path):
        new_path = '/'.join([webdav_path, dir])
        files = client.list(new_path)
        for file in files:
            if not re.match(pattern, file):
                not_matched_files[''.join([new_path, file])] = 'NOT MATCHED'

    print('Running on the options {}'.format({
        'webdav_url': webdav_url, 'webdav_path': webdav_path, 'pattern': pattern
    }))
    print(tabulate(not_matched_files.items(), headers=['FILENAME', 'WARNING'], tablefmt="grid"))


if __name__=='__main__':
    main()
