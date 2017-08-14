# simple wrapper for sending data to collectd 

        usage: pycollect [-h] -m METRIC [-V] -s SERVER [-p PORT] [-D] [-i INTERVAL]
                         [--version] (-c VALUE | -P PLUGIN | -S SCRIPT)
        
        collector: collects and sends stats to carbon
        
        optional arguments:
          -h, --help            show this help message and exit
          -m METRIC, --metric METRIC
                                metric path where to store data
          -V, --verbose         print data to stdout before sending to server
          -s SERVER, --server SERVER
                                carbon server address
          -p PORT, --port PORT  carbon server port, default 2003
          -D, --daemon          run as daemon, sends data at regular intervals
          -i INTERVAL, --interval INTERVAL
                                interval to send data in daemon mode, defaults 5s
          --version             show program's version number and exit
          -c VALUE, --value VALUE
                                metric value to send, must be int or float
          -P PLUGIN, --plugin PLUGIN
                                call plugin to collect metric data
          -S SCRIPT, --script SCRIPT
                                get value from script outpout
        
        metric must be in standard collectd format e.g.
        hostname.stats.command.[time|data]
