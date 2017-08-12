#!/usr/bin/python

import commands
from time import time
from sys import exit
import platform

hostname = str(platform.node())
application = "df.latency"
node = 'mountname'
command = 'df -h'


def create_oid(hostname, application, node):
    oid = hostname+"."+application+"."+node
    return oid


def measure_command_time(command):
    start = time()
    commands.getoutput(command)
    end = time()
    return end-start


def main():
    oid = create_oid(hostname, application, node)
    execution_time = measure_command_time(command)
    if execution_time > 0.5:
        print "duration {0}".format(str(execution_time))
        exit(1)
    else:
        print "{0} {1} {2}".format(oid, execution_time, int(time()))


if __name__ == "__main__": main()  # noqa allow 2 satements on the same line
