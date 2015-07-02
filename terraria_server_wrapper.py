import subprocess
import shlex
import threading
import sys
import time

server = "\"C:\\Program Files (x86)\\Steam\\steamapps\\common\\terraria\\TerrariaServer.exe\""
config_flag = "-config"
config = sys.argv[1]

args = server + " " + config_flag + " " + config

args = shlex.split(args)
print(args)
server_process = subprocess.Popen(args,bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def output_loop(process):
    running = True
    while running:
        stdout = process.stdout.readline()
        if len(stdout) > 0:
            print(stdout[:-2].decode("ascii"))

def input_loop(process):
    running = True
    while running:
        command = input() + "\r\n"
        process.stdin.write(command.encode("ascii"))
        process.stdin.flush()
        print(process.poll())

def input_test(process):
    command = "say test" + "\r\n"
    process.stdin.write(command.encode("ascii"))
    process.stdin.flush()
    
        
o = threading.Thread(target=output_loop, args=(server_process,))
i = threading.Thread(target=input_loop, args=(server_process,))
o.start()
time.sleep(15)
print("done sleeping")
i.start()

#server_process.kill()

