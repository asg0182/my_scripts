import requests
import argparse
import json
import csv


def create_parser():
    parser = argparse.ArgumentParser(description='Unused docker image')
    parser.add_argument('--base-url', type=str, nargs='?', default='http://mvn/artifactory/', required=False)
    parser.add_argument('--repo-key', type=str, required=True)
    parser.add_argument('--user', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--out', type=str, nargs='?', default='console', required=False)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    # base_url = 'http://mvn/artifactory/' # docker_releases_local2
    base_url = args.base_url
    repo_key = args.repo_key
    headers = {
        'content-type': 'text/plain',
    }
    user = args.user
    passw = args.password
    out = args.out

    data = 'items.find({"name":{"$eq":"manifest.json"}, "repo":{"$eq":"%s"}}).include("stat")' % repo_key
    myResp = requests.post(base_url + 'api/search/aql',
                           auth=(user, passw), headers=headers, data=data)
    resp_data = myResp.json().get('results')

    if resp_data:
        filtered_data = [
            item for item in resp_data if item['stats'][0]['downloads'] == 0
        ]
        if out == 'console':
            for item in filtered_data:
                print(item)
        elif out == 'json':
            with open('out.json', 'w', encoding='utf-8') as f:
                json.dump(filtered_data, f)
        elif out == 'csv':
            with open('out.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=filtered_data[0].keys(), delimiter=',')
                writer.writeheader()
                for row in filtered_data:
                    writer.writerow(row)

if __name__ == '__main__':
    main()
