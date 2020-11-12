import yaml


def prod_db():
    with open("docker-compose.yml", 'r') as yml_file:
        docker_config = yaml.load(yml_file)

    mysql_container = docker_config['services']['mysql']['container_name']
    base_pass = docker_config['services']['mysql']['environment']['MYSQL_ROOT_PASSWORD']
    base = docker_config['services']['mysql']['environment']['MYSQL_DATABASE']

    return 'root:{}@{}/{}'.format(base_pass,mysql_container, base)


def dev_db():
    return 'root:12345@127.0.0.1/sherlock'
