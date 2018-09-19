import json

import paramiko
from django.conf import settings
from paramiko.client import SSHClient as ParamikoSSHClient


class SSHClient(object):

    def __init__(self):
        self.client = ParamikoSSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.client.connect(
            hostname=settings.UBITQUITY_HOST,
            username=settings.SSH_USERNAME,
            password=settings.SSH_PASSWORD,
        )

    def close(self):
        self.client.close()

    def put_data(self, data):
        self.connect()
        json_data = json.dumps(data)
        self.client.exec_command("echo '{}' > {}/{}".format(
            json_data,
            settings.UBITQUITY_FILE_PATH,
            "uuid_{}.json".format(data['uuid_name'].split('.')[0])
        ))
        self.close()
