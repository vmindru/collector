#!/usr/bin/python

import commands
from time import time
from sys import argv



def measure_command_time(command):
    start = time()
    commands.getoutput(command)
    end = time()
    return round(end-start, 4)


def main():
    com = 'df -h' 
    if len(argv) == 2:
        path = argv[1]
        com = com+path
        print measure_command_time(com)

if __name__ == "__main__": main()  # noqa allow 2 satements on the same line
