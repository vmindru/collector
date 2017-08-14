# simple wrapper for sending data to collectd 
        usage: collector [-h] -m METRIC [-V] -s SERVER [-p PORT] [-D] [-i INTERVAL]
                         (-c VALUE | -P PLUGIN)
        
        collector: collects and sends stats to carbon
        
        optional arguments:
          -h, --help            show this help message and exit
          -m METRIC, --metric METRIC
                                OID where to store data
          -V, --verbose         print data to stdout before sending to server
          -s SERVER, --server SERVER
                                carbon server address
          -p PORT, --port PORT  carbon server port, default 2003
          -D, --daemon          run as daemon, sends data at regular intervals
          -i INTERVAL, --interval INTERVAL
                                interval to send data in daemon mode, defaults 5s
          -c VALUE, --value VALUE
                                metric value to send, must be int or float
          -P PLUGIN, --plugin PLUGIN
                                call plugin to collect metric data
        
        default OID will be formed hostname.stats.command.[time|data], where hostname
        is taken from system hostname stats is static string, command is the command
        name passed with -c flag and time or data depending on the execution mode -t
        or -d
