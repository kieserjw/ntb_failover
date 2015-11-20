import netifaces
import sys

def main():
    interface = 'eth0'
    if len(sys.argv) == 2:
        interface = sys.argv[1]
    if interface in netifaces.interfaces():        
        addr = netifaces.ifaddresses(interface)   
        print netifaces.AF_INET in addr
    else:
        print False
    return
         
if __name__ == '__main__':
    main()

