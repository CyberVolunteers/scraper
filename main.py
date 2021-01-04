#!/usr/bin/env python
import subprocess

from sys import argv

from getpass import getpass

import psutil as psutil

import os


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


def start():
    lastPid = getStoredPid()
    for process in psutil.process_iter():
        if process.pid == lastPid:
            raise Exception("Last instance is still running")

    # log in
    cookie = getpass(prompt="cookie >")

    print("cookie: ", "'" + cookie + "'")

    path = input("path >")

    if cookie == "":
        cookie = "not_specified"
        path = "not_specified"

    print("Creating a subprocess:")
    if os.name == "nt":  # win
        scrapingProcess = subprocess.Popen("python ./scraper.py {} {} {} {}".format(cookie, path, timePeriod, doPrint),
                                           creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:  # linux
        scrapingProcess = subprocess.Popen("python3 ./scraper.py {} {} {} {}".format(cookie, path, timePeriod, doPrint),
                                           shell=True)
    print("Process pid:", scrapingProcess.pid)

    # record the process
    with open("./scraper.pid", "w") as f:
        f.seek(0)
        f.write(str(scrapingProcess.pid))
        f.close()


def restart():
    stop()
    start()


if __name__ == '__main__':

    if len(argv) < 2:
        raise Exception("Expected at least 2 arguments, got %i" % len(argv), argv)

    command = argv[1]

    print(argv)

    if len(argv) >= 3:
        doPrint = argv[2][0].lower() != "f"
    else:
        doPrint = True

    if len(argv) >= 4:
        timePeriod = argv[3]
    else:
        timePeriod = 7 * 24 * 60 * 60

    if command == "stop":
        stop()
    elif command == "start":
        start()
    elif command == "restart":
        restart()
    else:
        raise Exception("Command not found")
