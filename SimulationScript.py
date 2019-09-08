import sys
import subprocess

procs = []
configs = [2,3,5,6,8,9]
for i in configs:
    proc = subprocess.Popen([sys.executable, './Config'+str(i)+'.py'], close_fds=True)
    procs.append(proc)

for proc in procs:
    proc.wait()