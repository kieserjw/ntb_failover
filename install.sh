cd /root/jkieser

rpm -Uvh bison-2.7-4.el7.x86_64.rpm
rpm -Uvh byacc-1.9.20130304-3.el7.x86_64.rpm
rpm -Uvh m4-1.4.16-10.el7.x86_64.rpm
rpm -Uvh flex-2.5.37-3.el7.x86_64.rpm

tar -xf netperf-2.7.0.tar.gz
tar -xf libpcap-1.7.4.tar.gz
tar -xf ucarp-1.5.1.tar.bz2

cd /root/jkieser/netperf-2.7.0
./configure
make install

cd /root/jkieser/libpcap-1.7.4
./configure 
make install

cd /root/jkieser/ucarp-1.5.1
./configure
make install

cp /usr/local/lib/libpcap.so.1 /usr/lib
ldconfig

exit 0

service corosync stop

#ph1-c500
ip addr del 192.168.1.2 dev eth1
ip addr add 192.168.1.2 dev eth1

/usr/local/sbin/ucarp -v 42 -p cris -a 192.168.1.5 -s 192.168.1.1 &
/usr/local/sbin/ucarp -v 42 -p cris -a 192.168.1.5 -s 192.168.1.2 &

#ph1-c501
ip addr del 192.168.2.1 dev eth0
ip addr del 192.168.2.2 dev eth1

ip addr add 192.168.1.3 dev eth0
ip addr add 192.168.1.4 dev eth1

