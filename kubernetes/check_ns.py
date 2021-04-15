import os
from kubernetes import client, config


base_path = os.path.abspath('.')
config.load_kube_config(os.path.join(base_path, '.kube', 'config'), context='k8s-dev')


def get_empty_namespaces(v1):
    namespaces = v1.list_namespace()

    for n in namespaces.items:
        if is_namespace_empty(v1, n.metadata.name) \
                and not n.metadata.name == 'default' \
                and not n.metadata.name.startswith('kube'):
            print(n.metadata.name, " Is EMPTY!!!!")


def is_namespace_empty(v1, namespace):
    pods = v1.list_namespaced_pod(namespace=namespace)
    return len(pods.items) == 0


def main():
    v1 = client.CoreV1Api()
    get_empty_namespaces(v1)


if __name__=='__main__':
    main()
