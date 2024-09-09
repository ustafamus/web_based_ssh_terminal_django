from channels.generic.websocket import WebsocketConsumer
import paramiko
import threading

class SSHConsumer(WebsocketConsumer):
  def connect(self):
      self.accept()
      self.ssh_client = paramiko.SSHClient()
      self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  def disconnect(self, close_code):
      if hasattr(self, 'ssh_client'):
          self.ssh_client.close()

  def receive(self, text_data):
      # Example: text_data could be a JSON string with connection details
      # Parse the text_data to get hostname, username, password, etc.
      # For simplicity, let's assume text_data is a command to execute
      try:
          stdin, stdout, stderr = self.ssh_client.exec_command(text_data)
          output = stdout.read().decode('utf-8')
          self.send(text_data=output)
      except Exception as e:
          self.send(text_data=str(e))

  def ssh_connect(self, hostname, username, password):
      try:
          self.ssh_client.connect(hostname, username=username, password=password)
          self.send(text_data="Connection successful")
      except Exception as e:
          self.send(text_data=f"Connection failed: {str(e)}")