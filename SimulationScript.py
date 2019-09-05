import sys
import subprocess

procs = []
for i in range(4):
    proc = subprocess.Popen([sys.executable, './Config'+str(i)+'.py'], close_fds=True)
    procs.append(proc)

for proc in procs:
    proc.wait()