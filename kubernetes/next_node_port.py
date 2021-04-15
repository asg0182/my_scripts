import os
from kubernetes import client, config

base_path = os.path.abspath('.')
config_path = os.path.join(base_path, '.kube', 'config')
config.load_kube_config(config_path, context='k8s-dev')
apik8s = client.CoreV1Api()


def main():
    services = apik8s.list_service_for_all_namespaces()
    node_ports = []
    for service in services.items:
        port = service.spec.ports[0].node_port
        if port:
            node_ports.append(port)

    sorted_node_ports = sorted(node_ports)
    print('Listen node ports: {}'.format(sorted_node_ports))
    print('Next free nodePort = ', sorted_node_ports[-1]+1)


if __name__=='__main__':
    main()
