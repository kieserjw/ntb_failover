#!/usr/bin/env python

import sys, time
from daemon import Daemon
import logging
import logging.handlers
from datetime import datetime
import fcntl, struct
from socket import *

def network_state(interface):
        # set some contants
        SIOCGIFFLAGS = 0x8913
        null256 = '\0'*256

        # Create a socket so we have a handle to query
        s = socket(AF_INET, SOCK_DGRAM)

        # Call ioctl(  ) to get the flags for the given interface
        result = fcntl.ioctl(s.fileno(  ), SIOCGIFFLAGS, interface + null256)

        # Extract the interface's flags from the return value
        flags, = struct.unpack('H', result[16:18])

        # Check "UP" bit and print a message
        return flags & 1

class MyDaemon(Daemon):
        def run(self):
                logging.basicConfig(filename='daemon.log', level=logging.DEBUG)
                interface = 'eth0'
                is_up = network_state(interface)
                logging.info("{} -- {} is {}".format(datetime.now(), interface, ('down', 'up')[is_up]))
                while True:
                        while is_up:
                                is_up = network_state(interface)
                                time.sleep(1)
                        logging.info("{} -- {} is down".format(datetime.now(), interface))
                        while not is_up:
                                is_up = network_state(interface)
                                time.sleep(1)
                        logging.info("{} -- {} is up".format(datetime.now(), interface))


if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)


