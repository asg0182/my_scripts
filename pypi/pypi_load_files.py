import argparse
from pypi_simple import PyPISimple
import requests
import os


def create_parser():
    parser = argparse.ArgumentParser(description='Get all files from local simple pypi for migrate to Nexus')
    parser.add_argument('--login', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--pypi-endpoint', type=str, required=False)
    return parser


def main():
    args = create_parser().parse_args()
    login = args.login
    password = args.password
    pypi_endpoint = args.pypi_endpoint # http://localpypiserver:8080/simple

    base_path = os.path.abspath('.')

    with PyPISimple(
        endpoint=pypi_endpoint,
        auth=(login, password)
    ) as client:
        index_page = client.get_index_page()
        projects = index_page.projects

        for project in projects:
            try:
                url = client.get_project_url(project)
                packages = client.get_project_page(project).packages
                print(project, ' ', url)
                for package in packages:
                    r = requests.get(package.url, allow_redirects=True)
                    path_to_file = os.path.join(base_path, 'downloaded_files', package.filename)
                    open(path_to_file, 'wb').write(r.content)
                    print(package.filename, ' downloaded')
            except requests.exceptions.HTTPError as exc:
                print(exc, ' ', 'Project {} is a proxy url on oriiginal pypi'.format(project))


if __name__=='__main__':
    main()
