import pyzabbix
import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Get hosts and groups from Zabbix')
    parser.add_argument('--zabbix-login', type=str, required=True)
    parser.add_argument('--zabbix-password', type=str, required=True)
    parser.add_argument('--zabbix-url', type=str, required=True)
    return parser


def get_hosts_by_group(z, group):
    return z.host.get(groupids=group['groupid'], output='extend')


def get_zabbix_host_data(login, password, zabbix_url):
    z = pyzabbix.ZabbixAPI(
        url=zabbix_url,
        user=login,
        password=password
    )
    res = {}
    groups = z.hostgroup.get()
    my_groups = [g for g in groups if g['name'].startswith('@')]
    for group in my_groups:
        g_hosts = get_hosts_by_group(z, group)
        group_name = group['name']
        res[group_name] = [host['name'] for host in g_hosts]
    return res


def main():
    args = create_parser().parse_args()
    login = args.login
    password = args.password
    zabbix_url = args.zabbix_url

    info = get_zabbix_host_data(
        login=login, password=password, zabbix_url=zabbix_url
    )
    print(info)
