#!/usr/bin/env python
import subprocess

from sys import argv

from getpass import getpass

import psutil as psutil

def getStoredPid():
    with open("./scraper.pid", "r") as f:
        pid = int(f.read())
        f.close()
        return pid

def stop():
    pid = getStoredPid()
    print("Retrieved pid:", pid)

    for process in psutil.process_iter():
        if process.pid == pid:
            process.terminate()
            print("Terminated")
            return
    print("Could not find the process to terminate")


def start(timePeriod):

    lastPid = getStoredPid()
    for process in psutil.process_iter():
        if process.pid == lastPid:
            raise Exception("Last instance is still running")

    # log in
    cookie = getpass(prompt="cookie >")
    path = input("path >")

    if cookie == "":
        cookie = "not_specified"
        path = "not_specified"

    print("Creating a subprocess:")
    scrapingProcess = subprocess.Popen("python ./scraper.py {} {} {}".format(cookie, path, timePeriod),
                                       creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    print("Process pid:", scrapingProcess.pid)

    # record the process
    with open("./scraper.pid", "w") as f:
        f.seek(0)
        f.write(str(scrapingProcess.pid))
        f.close()


def restart(timePeriod):
    stop()
    start(timePeriod)


if __name__ == '__main__':

    if len(argv) < 2:
        raise Exception("Expected at least 2 arguments, got %i" % len(argv), argv)

    command = argv[1]

    if len(argv) == 2:
        timePeriod = 7 * 24
    else:
        timePeriod = argv[2]


    if command == "stop":
        stop()
    elif command == "start":
        start(timePeriod)
    elif command == "restart":
        restart(timePeriod)
    else:
        raise Exception("Command not found")
