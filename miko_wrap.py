import getpass
import paramiko

class Miko_Wrapper(object):
	def __init__(self, username, password, host, auto_add_keys=True):
		self.username = username
		self.password = password
		self.host = host
		self.auto_add_keys = auto_add_keys

	def open(self):
		self.client = paramiko.SSHClient()
		self.client.load_system_host_keys()
		
		if self.auto_add_keys == True:
			key_policy = paramiko.AutoAddPolicy
		else:
			key_policy = paramiko.WarningPolicy

		self.client.connect(
				self.host, 
				port     = 22, 
				username = self.username, 
				password = self.password
		)

	def run(self, command):
		stdin, stdout, stderr = self.client.exec_command(command)
		return stdout.read()

	def close(self):
		self.client.close()

	def __repr__(self):
		return "USERNAME={}\nPASSWORD={}\nHOSTNAME={}\nAUTO_ADD_KEYS={}".format(
			self.username, "REDACTED", self.host, self.auto_add_keys)


def single_shot(*commands, **creds):
	if 'username' not in creds.keys():
		creds['username'] = getpass.getuser()
	if 'password' not in creds.keys():
		creds['password'] = getpass.getpass()
	if 'auto_add_keys' not in creds.keys():
		creds['auto_add_keys'] = True
	if 'hostname' not in creds.keys():
		raise "Need a hostname"

	device = Miko_Wrapper(creds['username'], creds['password'], creds['hostname'])
	device.open()

	all_out = {}

	for command in commands:
		all_out[command] = device.run(command)

	device.close()
	return all_out
