#!/usr/bin/env python

import sys, time
from daemon import Daemon
import logging
import logging.handlers
from datetime import datetime
import subprocess

#checks interface for address before deleting
def delete_address(interface, address):
	address = address + '/24'
	if address in subprocess.Popen(["ip", "addr", "show", "dev", interface], stdout=subprocess.PIPE).communicate()[0]:
		subprocess.Popen(["ip", "addr", "del", address, "dev", interface])

# Will not add the address if it is already present on the specified interface
def add_address(interface, address):
	address = address + '/24'
	if address not in subprocess.Popen(["ip", "addr", "show", "dev", interface], stdout=subprocess.PIPE).communicate()[0]:
		subprocess.Popen(["ip", "addr", "add", address, "dev", interface])

#checks whether interface is up or down
def network_state(interface):
        return 'state UP' in subprocess.Popen(["ip", "link", "show", interface], stdout=subprocess.PIPE).communicate()[0]

class MyDaemon(Daemon):
        def run(self, address='192.168.1.1', primary='eth0', secondary='eth1'):
                logging.basicConfig(filename='/root/jkieser/daemon.log', level=logging.DEBUG)
                is_up = network_state(primary)
                logging.info("{} -- {} is {}".format(datetime.now(), primary, ('down', 'up')[is_up]))
                while True:
			#first half of loop checks interface state every second and then 
			#cycles to other half if the state has changed
                        while is_up:
                                is_up = network_state(primary)
                                time.sleep(1)
                        logging.info("{} -- {} is down".format(datetime.now(), primary))	
			#migrates address to secondary interface
			delete_address(primary, address)
			add_address(secondary, address)

                        while not is_up:
                                is_up = network_state(primary)
                                time.sleep(1)
                        logging.info("{} -- {} is up".format(datetime.now(), primary))
			#migrates address back to primary
			delete_address(secondary, address)
			add_address(primary, address)


if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid')
        if len(sys.argv) == 2 or len(sys.argv) == 5:
                if 'start' == sys.argv[1] and len(sys.argv) > 2:
			#condition allows cmd line to set address and primary and secondary interface
                        daemon.start(sys.argv[2], sys.argv[3], sys.argv[4])
		elif 'start' == sys.argv[1]:
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
                print "usage: %s start|stop|restart [address primary secondary]" % sys.argv[0]
                sys.exit(2)


