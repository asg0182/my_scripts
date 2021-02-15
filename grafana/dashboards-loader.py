import os, glob
import argparse
import json
import requests
from requests import auth


def create_parser():
    parser = argparse.ArgumentParser(description='Add dashboards to Grafana')
    parser.add_argument('--login', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--grafana-url', type=str,  required=True)
    return parser


def main():
    args = create_parser().parse_args()
    grafana_url = args.grafana_url
    login = args.login
    password = args.password

    dashboards_path = os.path.join(os.path.abspath('../../kubernetes'), '../dashboards')
    os.chdir(dashboards_path)
    for dashboard_file in glob.glob('*.json'):
        with open(os.path.join(dashboards_path, dashboard_file), 'r', encoding='utf-8') as f:
            dashboard = json.load(f)
            resp = requests.post(
                url=grafana_url + 'db', auth=auth.HTTPBasicAuth(login, password),
                json={'dashboard':dashboard, 'folderId': 0, 'overwrite': True}, verify=False
            )
            print(resp, ' ', resp.content)


if __name__ == '__main__':
    main()
