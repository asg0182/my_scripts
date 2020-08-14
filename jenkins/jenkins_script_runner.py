import os
import json
import datetime
import time
import jenkins
from jenkins import (
    TimeoutException, EmptyResponseException, BadHTTPException, JenkinsException, NotFoundException
)
import requests
import argparse
from requests import auth


def create_parser():
    parser = argparse.ArgumentParser(description='Jenkins groovy script runner')
    parser.add_argument('--jenkins-work-delay', type=int, nargs='?', default=5, required=False)
    parser.add_argument('--jenkins-urls', type=list, nargs='+', required=True)
    parser.add_argument('--groovy-script', type=str, required=True)
    parser.add_argument('--login', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    return parser


def run_grrovy_script(jenkins_url, login, password, groovy_script):
    jenkins_server = jenkins.Jenkins(
        url=jenkins_url, username=login, password=password
    )
    jenkins_server._session.verify = False
    return js.run_script(script=groovy_script)


def main():
    parser = create_parser()
    args = parser.parse_args()

    jenkins_work_delay = args.jenkins_work_delay
    groovy_script = args.groovy_script
    service_login = args.login
    service_passw = args.password
    jenkins_urls = args.jenkins_urls

    groovy_script_path = os.path.join(os.path.abspath('.'), 'groovy', groovy_script)

    with open(groovy_script_path, 'r', encoding='utf-8') as f:
        groovy_script_data = f.read()
        print('===>> RECEIVE {} JENKINS INSTANCES FOR WORK'.format(len(jenkins_urls)))
        for jenkins_url in jenkins_urls:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ' ', jenkins_url, ' in work')
            try:
                script_result = run_grrovy_script(
                    jenkins_url=jenkins_url, login=service_login, password=service_passw,
                    groovy_script=groovy_script_data
                )
                print(script_result)
            except (
                    TimeoutException, EmptyResponseException, BadHTTPException, JenkinsException, NotFoundException
            ) as e:
                print(str(e))
                continue
            time.sleep(jenkins_work_delay)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ' WORK IS FINISH')


if __name__ == '__main__':
    main()
