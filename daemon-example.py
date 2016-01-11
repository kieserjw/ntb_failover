#!/usr/bin/env python

import sys, time
from daemon import Daemon
import logging
import logging.handlers
from datetime import datetime
import subprocess

def delete_address(interface, address):
	address = address + '/24'
	if address in subprocess.Popen(["ip", "addr", "show", "dev", interface], stdout=subprocess.PIPE).communicate()[0]:
		subprocess.Popen(["ip", "addr", "del", address, "dev", interface])


def add_address(interface, address):
	address = address + '/24'
	if address not in subprocess.Popen(["ip", "addr", "show", "dev", interface], stdout=subprocess.PIPE).communicate()[0]:
		subprocess.Popen(["ip", "addr", "add", address, "dev", interface])


def network_state(interface):
        return 'state UP' in subprocess.Popen(["ip", "link", "show", interface], stdout=subprocess.PIPE).communicate()[0]

class MyDaemon(Daemon):
        def run(self):
                logging.basicConfig(filename='/root/jkieser/daemon.log', level=logging.DEBUG)
                interface = 'eth0'
		address = '192.168.1.1'
                is_up = network_state(interface)
                logging.info("{} -- {} is {}".format(datetime.now(), interface, ('down', 'up')[is_up]))
                while True:
                        while is_up:
                                is_up = network_state(interface)
                                time.sleep(1)
                        logging.info("{} -- {} is down".format(datetime.now(), interface))
			delete_address(interface, address)
			add_address('eth1', address)
                        while not is_up:
                                is_up = network_state(interface)
                                time.sleep(1)
                        logging.info("{} -- {} is up".format(datetime.now(), interface))
			delete_address('eth1', address)
			add_address(interface, address)


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


