#!/usr/bin/python

import commands
from argparse import ArgumentParser
from time import time
import platform


VERSION = "0.1"
hostname = str(platform.node())


def collect_arguments():
    parser = ArgumentParser()
    parser.prog = "collector"
    parser.description = 'collector: collects and sends stats to collectd'
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-v', '--version', action='version', version=VERSION, help='display version information')
    parser.add_argument('-o', '--oid', help='OID where to store data')
    parser.add_argument('-c', '--command', required=True, help='command to execute', metavar='')
    parser.add_argument('-V', '--verbose', help='print data to stdout before sending to server')
    group.add_argument('-t', '--time', action='store_true', help='send command time execution as metric to collectd')
    group.add_argument('-d', '--data', action='store_true', help='send command data to collectd, must be integer or '
                       'float')
    parser.epilog = 'default OID will be formed hostname.stats.command.[time|data], where hostname is taken from system\
                    hostname stats is static string, command is the command name passed with -c flag and time or data \
                    depending on the execution mode -t or -d'
    args = parser.parse_args()
    return args


def create_oid(hostname, command, mode):
    oid_separator = '.'
    oid = oid_separator.join((hostname, "stats", command, mode))
    return oid


def measure_command_time(command):
    start = time()
    commands.getoutput(command)
    end = time()
    return end-start


def main():
    args = collect_arguments()
    command = args.command
    if args.time is True:
        mode = 'time'
    elif args.data is True:
        mode = 'data'
    else:
        raise 'Something really bad happend'
    oid = create_oid(hostname, command, mode)
    print oid
#    print oid
#    execution_time = measure_command_time(command)


if __name__ == "__main__": main()  # noqa allow 2 satements on the same line
