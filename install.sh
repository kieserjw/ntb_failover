c /root/jkieser

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

/sbin/ip addr add 192.168.1.5/24 dev eth0
/sbin/ip addr add 192.168.1.5/24 dev eth1

tc qdisc add dev eth0 root handle 1: cbq avpkt 1000 bandwidth 2mbit;tc class add dev eth0 parent 1: classid 1:1 cbq rate 8bit allot 1500 prio 5 bounded isolated;tc filter add dev eth0 parent 1: protocol ip prio 16 u32 match ip dst 192.168.1.1 flowid 1:1;tc filter add dev eth0 parent 1: protocol ip prio 16 u32 match ip src 192.168.1.1 flowid 1:1

tc qdisc add dev eth0 root handle 1: cbq avpkt 1000 bandwidth 2mbit;tc class add dev eth0 parent 1: classid 1:1 cbq rate 8bit allot 1500 prio 5 bounded isolated;tc filter add dev eth0 parent 1: protocol ip prio 16 u32 match ip dst 192.168.1.5 flowid 1:1;tc filter add dev eth0 parent 1: protocol ip prio 16 u32 match ip src 192.168.1.5 flowid 1:1

tc qdisc del dev eth0 root

#ph1-c501
ip addr del 192.168.2.1 dev eth0
ip addr del 192.168.2.2 dev eth1

ip addr add 192.168.1.3 dev eth0
ip addr add 192.168.1.4 dev eth1



