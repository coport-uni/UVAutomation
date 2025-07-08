import paramiko
from scp import SCPClient, SCPException

class SSHManager:
    def __init__(self):
        '''
        This function clears each ssh sessions 

        Input : None
        Output : None
        '''
        self.ssh_client = None

    def create_ssh_client(self, hostname : str , port: str, username : str, password : str):
        '''
        This function create a new ssh session. 

        Input : str, str ,str, str
        Output : None
        '''
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname = hostname, port = port, username = username, password = password)

        else:
            print("SSH client session exist.")

    def close_ssh_client(self):
        '''
        This function closes ssh session. 

        Input : None
        Output : None
        '''
        self.ssh_client.close()

    def send_file_to(self, local_path : str , remote_path : str):
        '''
        This function send a file to opened session with designated path. 

        Input : str, str
        Output : None
        '''
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_path, remote_path, preserve_times=True)
                print("Transfer complete")

        except SCPException:
            raise SCPException.message

    def get_file_from(self, remote_path, local_path):
        '''
        This function receive a file from opened session with designated path. 

        Input : str, str
        Output : None
        '''
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.get(remote_path, local_path)

        except SCPException:
            raise SCPException.message

    def send_command_to(self, command):
        '''
        This function send a command to opened session. 

        Input : str
        Output : None
        '''
        stdin, stdout, stderr = self.ssh_client.exec_command(command)

        return stdout.readlines()