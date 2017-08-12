#!/usr/bin/python

import commands
from argparse import ArgumentParser
from time import time
from sys import exit
import platform


VERSION = "0.1"
hostname = str(platform.node())
application = "df.latency"
node = 'mountname'
command = 'df -h'


def collect_arguments():
    parser = ArgumentParser()
    parser.prog = "collector"
    parser.description = 'collector: collects and sends stats to collectd'
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-v', '--version', action='version', version=VERSION, help='display version information')
    parser.add_argument('-O', '--oid', required=True, help='OID where to store data')
    parser.add_argument('-a', '--command', required=True, help='command to execute')
    parser.add_argument('-V', '--verbose', help='print data to stdout before sending to server')
    group.add_argument('-t', '--time', action='store_true', help='send command time execution as metric to collectd')
    group.add_argument('-d', '--data', action='store_true', help='send command data to collectd, must be integer or '
                       'float')

    args = parser.parse_args()
    return args


def create_oid(hostname, application, node):
    oid = hostname+"."+application+"."+node
    return oid


def measure_command_time(command):
    start = time()
    commands.getoutput(command)
    end = time()
    return end-start


def main():
    collect_arguments()
    oid = create_oid(hostname, application, node)
    execution_time = measure_command_time(command)
    if execution_time > 0.5:
        print "duration {0}".format(str(execution_time))
        exit(1)
    else:
        print "{0} {1} {2}".format(oid, execution_time, int(time()))


if __name__ == "__main__": main()  # noqa allow 2 satements on the same line
