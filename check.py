#!/usr/bin/python

import commands
from argparse import ArgumentParser
from time import time,sleep
import platform
import socket


VERSION = "0.1"
hostname = str(platform.node())


def int_or_float(value):
    """ returns value if value is int or float , TBI """
    return value


def collect_arguments():
    parser = ArgumentParser()
    parser.prog = "collector"
    parser.description = 'collector: collects and sends stats to carbon'

    parser.add_argument('-m', '--metric', required=True, help='OID where to store data')
    parser.add_argument('-V', '--verbose', action='store_true', help='print data to stdout before sending to server')
    parser.add_argument('-s', '--server', required=True, help='carbon server address')
    parser.add_argument('-p', '--port', default=2003, help='carbon server port, default 2003')
    parser.add_argument('-D', '--daemon', action='store_true', help='run as daemon, sends data at regular intervals')
    parser.add_argument('-i', '--interval', type=float, default=5.0, help='interval to send data in daemon mode, defaults 5s')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--value', type=int_or_float,  help='metric value to send, must be int or float ')
    group.add_argument('-P', '--plugin', default=False,  help='call plugin to collect metric data')
    parser.epilog = 'metric must be in standard collectd format e.g.  hostname.stats.command.[time|data]'
    args = parser.parse_args()
    return args


def get_command_output(command):
    data = commands.getoutput(command)
    return data


def send_data(metric, data, server, port, retry_interval=5, verbose=False):
    send_data = create_carbon_data(metric, data)
    sock = socket.socket()
    print "creating socket"
    while True:
        try:
            sock.connect((server, port))
            sock.sendall(send_data+'\n') # note we need to append end of line at the end off the message
            if verbose:
                print "sent data: {0} to {1} {2}".format(send_data, server, port)
            break
        except socket.error:
            print "Could not connect to {0}:{1}, retrying".format(server, port)
            sleep(float(retry_interval))
    print "closing socket"
    sock.close()
    

def include_plugin():
    pass


def create_carbon_data(metric, data):

    def _validate_metric(metric):
        """ validates metric format 
            not yet implemented

        Args:
            metric (str): carbon metric path http://graphite.readthedocs.io/en/latest/feeding-carbon.html
        Returns:
            metric (str): carbon metric path http://graphite.readthedocs.io/en/latest/feeding-carbon.html
        Raises:
            ValueError
        """
        return metric 

    """ creates data to be sent to carbon server 

    Args: 
        metric (str): carbon metric path http://graphite.readthedocs.io/en/latest/feeding-carbon.html
        data (int|float): data for the metric 

    Returns:
        metric (str): returns <metric path> <metric value> <metric timestamp> 
    """
    return "{0} {1} {2}".format(_validate_metric(metric), data,  int(time()))



def create_data(args):
    if args.plugin is True:
        include_plugin()
    else:
        data = args.value
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
    if args.daemon:
        while True:
            data = create_data(args)
            send_data(args.metric, data, args.server, args.port, args.interval, args.verbose)
            sleep(args.interval)
    else:
        data = create_data(args)
        send_data(args.metric, data, args.server, args.port, args.interval, rgs.verbose)


if __name__ == "__main__": main()  # noqa allow 2 satements on the same line
