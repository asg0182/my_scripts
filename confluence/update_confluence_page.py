import csv
import os
import pprint
from bs4 import BeautifulSoup
from atlassian import Confluence
import argparse


STATUSES = {
    'active': 'Greenactive',
    'inactive': 'greyINACTIVE',
    'deleted': 'RedDELETED',
    'readytodelete': 'orangeREADYTODELETE'
}


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--login', type=str, required=True, help='Your AD login')
    parser.add_argument('--password', type=str, required=True, help='Your AD password')
    parser.add_argument('--confluence-url', type=str, required=True, help='Confluence Server')
    parser.add_argument('--jenkins-page-id', type=str, required=True, help='Confluence page')

    parser.add_argument('--empty-fields', type=int, nargs='+', required=False, help='Indexes of empty fields')
    parser.add_argument('--status', type=str, required=False,
                        help='Status Jenkins in table: active, deleted, inactiove or readytodelete')
    parser.add_argument('--all-fields', type=bool, default=True, required=False,
                        help='All fields table or jenkins link only')
    parser.add_argument('--csv', type=bool, required=False, help='may be csv')

    parser.add_argument('--add-jenkins-project-name', type=str, required=False, help='Project name')
    parser.add_argument('--add-jenkins-description', type=str, required=False, help='Description for jenkins')
    parser.add_argument('--add-jenkins-url', type=str, required=False, help='Jenkins url')
    parser.add_argument('--add-jenkins-ci', type=str, required=False, help='Project CI')
    parser.add_argument('--add-jenkins-resp', type=str, required=False, help='Project responsible')

    return parser


def get_html_content(login, passw):
    c = Confluence(BASE_URL, login, passw)
    page = c.get_page_by_id(page_id=JENKINS_PAGE_ID, expand='body.storage')
    return page['body']['storage']['value']


def update_html_content(login, passw, html):
    c = Confluence(BASE_URL, login, passw)
    page = c.get_page_by_id(page_id=JENKINS_PAGE_ID, expand='body.storage')
    resp = c.update_existing_page(page_id=JENKINS_PAGE_ID, body=html, title=page['title'])
    return resp.ok


def get_jenkins_table(login, passw):
    html = get_html_content(login, passw)
    soup = BeautifulSoup(html, 'html.parser')
    tabls = soup.find_all('table')
    return tabls[1]


def get_data_from_jenkins_table(login, passw):
    jenkins_table = get_jenkins_table(login, passw)
    data = []
    for row in jenkins_table.find_all('tr')[1:]:
        data.append([cell.get_text(strip=True).replace('\n', ' ') for cell in row.find_all('td')])
    return data


def add_new_jenkins(login, passw, project_name, description, jenkins_url, ci, otv):
    html = get_html_content(login, passw)
    soup = BeautifulSoup(html, 'html.parser')
    tabls = soup.find_all('table')
    jenkins_table = tabls[1]
    rows = jenkins_table.find_all('tr')
    last_row = rows[-1]
    last_num = len(rows)
    new_row = BeautifulSoup(
            """
            <tr>
            <td class="numberingColumn tf-colspan-1" colspan="1">{new_num}</td>
            <td class="tf-colspan-1" colspan="1"><ac:link><ri:page ri:content-title="{project_name}" ri:space-key="LOANMGR"></ri:page></ac:link></td>
            <td class="tf-colspan-1" colspan="1"><div class="content-wrapper"><p class="auto-cursor-target"><br/></p>{description}<p class="auto-cursor-target"><br/></p></div></td>
            <td class="tf-colspan-1" colspan="1"><a href="{jenkins_url}">{jenkins_url}</a></td>
            <td class="tf-colspan-1" colspan="1">{project_ci}</td>
            <td class="tf-colspan-1" colspan="1">{otv}</td>
            <td class="tf-colspan-1" colspan="1"><div class="content-wrapper"><p><ac:structured-macro ac:macro-id="a8b6f80f-3caf-4b3d-be18-d1bcfac1107f" ac:name="status" ac:schema-version="1"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">active</ac:parameter></ac:structured-macro></p></div></td>
            </tr>
            """.format(
                new_num=last_num, project_name=project_name, description=description,
                jenkins_url=jenkins_url, project_ci=ci, otv=otv
            ), 'html.parser'
        )
    last_row.insert_after(new_row)
    return soup


def get_jenkins_by_status(data, status, all_fields=True):
    s = STATUSES[status].lower()
    return my_filter(data, 6, s, all_fields)


def my_filter(data, field_num, field_val, all_fields=True):
    if all_fields:
        return [item for item in data if item[field_num].lower() == field_val]
    return [item[3] for item in data if item[field_num].lower() == field_val]


def get_info(login, passw, status=None, csvfile=None, all_fields=None, empty_fields=None):
    base_path = os.path.abspath('.')
    data = get_data_from_jenkins_table(login, passw)
    if empty_fields:
        for field in empty_fields:
            data = my_filter(data, field, '')

    if status:
        data = get_jenkins_by_status(data, status, all_fields)

    if csvfile:
        file = os.path.join(base_path, 'report.csv')
        with open(file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(data)
    else:
        pp = pprint.PrettyPrinter(width=41, compact=True)
        pp.pprint(data)


def update_inf0(
        login, passw, add_jenkins_project_name, add_jenkins_description,
        add_jenkins_url, add_jenkins_ci, add_jenkins_resp):
    soup = add_new_jenkins(
        login=login, passw=passw, project_name=add_jenkins_project_name,
        description=add_jenkins_description, jenkins_url=add_jenkins_url,
        ci=add_jenkins_ci, otv=add_jenkins_resp
    )
    new_html = str(soup)
    update_html_content(login, passw, new_html)


def main():
    parser = create_parser()
    args = parser.parse_args()

    login = args.login
    passw = args.password

    status = args.status
    csvfile = args.csv
    all_fields = args.all_fields
    empty_fields = args.empty_fields
    JENKINS_PAGE_ID = args.jenkins_page_id
    global JENKINS_PAGE_ID
    BASE_URL = args.confluence_url
    global BASE_URL

    if status or csvfile or empty_fields:
        get_info(login, passw, status, csvfile, all_fields, empty_fields)

    add_jenkins_project_name = args.add_jenkins_project_name
    add_jenkins_description = args.add_jenkins_description
    add_jenkins_url = args.add_jenkins_url
    add_jenkins_ci = args.add_jenkins_ci
    add_jenkins_resp = args.add_jenkins_resp

    if add_jenkins_project_name and \
            add_jenkins_description and \
            add_jenkins_url and \
            add_jenkins_ci and add_jenkins_resp:
        update_inf0(
            login, passw, add_jenkins_project_name, add_jenkins_description,
            add_jenkins_url, add_jenkins_ci, add_jenkins_resp
        )


if __name__=='__main__':
    main()
