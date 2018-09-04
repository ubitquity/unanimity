import json

import paramiko
from django.conf import settings
from paramiko.client import SSHClient as ParamikoSSHClient


class SSHClient(object):

    def __init__(self):
        self.client = ParamikoSSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.credentials = {}

    def connect(self):
        self.get_credentials()
        self.client.connect(
            hostname=settings.UBITQUITY_HOST,
            username=self.credentials.get('username'),
            password=self.credentials.get('password'),
        )

    def close(self):
        self.client.close()

    def get_credentials(self):
        if self.credentials:
            return self.credentials
        with open('ssh-credentials', 'rb') as f:
            self.credentials = json.loads(f.read())
        return self.credentials

    def put_data(self, data):
        self.connect()
        json_data = json.dumps(data)
        self.client.exec_command("echo '{}' > /var/www/html/aicdocs/{}".format(
            json_data,
            "{}.json".format(data['file_hash'])
        ))
        self.close()
