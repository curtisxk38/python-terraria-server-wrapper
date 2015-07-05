import subprocess
import shlex
import threading
import sys
import time

class Server():
	def __init__(self, server, config):
		self.args = shlex.split(server + " -config " + config)
		self.running = True
		
		
	def output(self, process):
		stdout = process.stdout.readline()
		if len(stdout) > 0:
			print(stdout[:-2].decode("ascii"))
	
	def input(self, process):
		command = input()
		if command == "exit" or command == "exit-nosave":
			self.running = False
			print("exiting")
		command += "\r\n"
		process.stdin.write(command.encode("ascii"))
		process.stdin.flush()
	
	def main(self):
		server_process = subprocess.Popen(self.args, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		input_thread = threading.Thread(target=self.input, args=(server_process,))
		input_thread.daemon = True
		input_thread.start()
		
		while self.running:
			self.output(server_process)
			#self.input_thread.daemon = True
			if not input_thread.isAlive():
				input_thread = threading.Thread(target=self.input, args=(server_process,))
				input_thread.daemon = True
				input_thread.start()
		
		

server = "\"C:\\Program Files (x86)\\Steam\\steamapps\\common\\terraria\\TerrariaServer.exe\""
config = sys.argv[1]

server_obj = Server(server, config)
server_obj.main()


