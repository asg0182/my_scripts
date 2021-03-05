import os
import argparse
import requests
import json
from requests import auth


def create_parser():
    parser = argparse.ArgumentParser(description='save dashboards from Grafana')
    parser.add_argument('--login', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--grafana-url', type=str, default='https://grafanahost/grafana/api/', required=False)
    parser.add_argument('--folder-id', type=int, default=0, required=False)
    parser.add_argument('--save-path', type=str, default='/opt/grafana/dashboards/', required=False)
    return parser


def main():
    args = create_parser().parse_args()

    grafana_url = args.grafana_url
    login = args.login
    password = args.password
    folder_id = args.folder_id
    save_path = args.save_path

    search_url = grafana_url + "search?folderIds={}".format(folder_id)

    r = requests.get(
        url=search_url, auth=auth.HTTPBasicAuth(login, password)
    )

    if r.ok:
        dashboards_data = r.json()
        for dashboard in dashboards_data:
            title = dashboard.get('title')
            uid = dashboard.get('uid')
            dashboard_uid_url = grafana_url + 'dashboards/uid/{}'.format(uid)
            request_dashboard = requests.get(
                url= dashboard_uid_url, auth=auth.HTTPBasicAuth(login, password)
            )
            if request_dashboard.ok:
                dashboard_data = request_dashboard.json()
                print( title, ' save')
                with open(os.path.join(save_path, title + '.json'), 'w', encoding='utf-8') as f:
                    json.dump(dashboard_data.get('dashboard'), f)


if __name__ == '__main__':
    main()
