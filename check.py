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
    parser.description = 'collector: collects and sends stats to carbon'

    parser.add_argument('-m', '--metric', required=True, help='OID where to store data')
    parser.add_argument('-c', '--command', required=True, help='command to execute')
    parser.add_argument('-V', '--verbose', action='store_true', help='print data to stdout before sending to server')
    parser.add_argument('-s', '--server', required=True, help='carbon server address')
    parser.add_argument('-p', '--port', default=2003, help='carbon server port, default 2003')
    parser.add_argument('-D', '--daemon', default=5, type=int, nargs='?', help='run as daemon with default interval of '
                        '5 seconds, specifing a value will make the dameon run with specified interval')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--time', action='store_true', help='send command time execution as metric to carbon')
    group.add_argument('-d', '--data', action='store_true', help='send command data to carbon, must be integer, float')
    parser.epilog = 'default OID will be formed hostname.stats.command.[time|data], where hostname is taken from system\
                    hostname stats is static string, command is the command name passed with -c flag and time or data \
                    depending on the execution mode -t or -d'
    args = parser.parse_args()
    return args


def measure_command_time(command):
    start = time()
    commands.getstatus(command)
    end = time()
    return end-start


def get_command_output(command):
    data = commands.getoutput(command)
    return data


def send_data(metric, data, server, port, verbose):
    if verbose:
        print "{0} {1} {2}".format(metric, data)
    else:
        print "sending {0} {1} {2}".format(metric, data)


def get_data(args):
    if args.time is True:
        data = str(measure_command_time(args.command))
    elif args.data is True:
        data = str(get_command_output(args.command))
    else:
        raise 'Something really bad happend, could not get command data'
    return data


def get_mode(args):
    if args.time is True:
        mode = 'time'
    elif args.data is True:
        mode = 'data'
    else:
        raise 'Something really bad happend, could not get command mode'
    return mode


def main():
    args = collect_arguments()
    data = get_data(args)
    send_data(args.metric, data, args.server, args.port, args.verbose)



if __name__ == "__main__": main()  # noqa allow 2 satements on the same line
