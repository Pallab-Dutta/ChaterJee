#from subprocess import PIPE, Popen
from asyncio.subprocess import PIPE, STDOUT
import subprocess
import sys
import threading, queue
import time
import select
import asyncio

#cmds = ['sshpass','-p','tcbg@123','ssh','tcbg@10.20.74.156']

f2=open('stdout.txt','w')
f3=open('stderr.txt','w')

cmds = ['python', '-i']
#proc = subprocess.run(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,universal_newlines=True,bufsize=1)
proc = subprocess.Popen(cmds, stdout=f2, stderr=f3, stdin=subprocess.PIPE ,universal_newlines=True,bufsize=1)

def getout():
    time.sleep(5)
    fout=open('stdout.txt','r')
    ferr=open('stderr.txt','r')
    line = fout.readlines()
    print(' '.join(line))
    fout.close()
    ferr.close()
    fouts=open('stdout.txt','w')
    fouts.close()

getout()
proc.stdin.write('for i in range(5):print(i)\n')
getout()
