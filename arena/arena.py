#!/usr/bin/env python

import os, random, string, sys
import subprocess, time

init_dir = "/home/enx-mmteam00/mm/"
os.chdir(init_dir)

#accounts = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20"]
accounts = ["test1","test2","test3","test4"]

def r():
    return"".join(random.choice(string.letters + string.digits) for i in xrange(10))

def doThis(commands):
    print "[arena] Performing maintenance..."
    for i in accounts:
        os.chdir(i)
        for c in commands:
            subprocess.call(c, shell=True)
        os.chdir(init_dir)
    print "[arena] Maintenance complete."

#doThis(["echo `sed ","git add README", "git commit -m 'Updated readmes.'", "git push"])
#doThis(["echo \"mmteam`pwd | sed 's/.*\///'`\" > name","git add name","git commit -m \"Setup name file\"","git push"])

def updateRepos():
    print "[arena] Pulling repositories..."
    p = []
    for i in accounts:
        os.chdir(i)
        p.append(subprocess.Popen(["git", "pull"]))
        os.chdir(init_dir)
    for i in p:
        i.wait()
    print "[arena] Pull complete."

def runClients(n):
    print "[arena] RUNNING ALL THE CLIENTS"
    server = subprocess.Popen(["/usr/bin/python", "/home/enx-mmteam00/mm17/server.py", "-n", str(n)],stdin=subprocess.PIPE)
    viz = r()
    print "Visualizer authcode is",viz
    server.stdin.write(viz + "\n")
    p = []
    for i in random.sample(accounts,n):
        os.chdir(i)
        f = open("name")
        p.append( (f.read().strip(), subprocess.Popen(["./run"],stdin=subprocess.PIPE), r() ) )
        os.chdir(init_dir)
    for i,v,k in p:
        server.stdin.write(k + "\n")
    time.sleep(0.2)
    for i,v,k in p:
        try:
            v.stdin.write(k +"\n")
            time.sleep(0.1)
        except:
            print "Failed to add player",i,"with authcode",k
    server.wait()
    print "Server returned",server.returncode
    for i,v,k in p:
        v.wait()
        print i,"-",v.returncode,"~",k
    print "[arena] Run complete."

updateRepos()
runClients(4)
