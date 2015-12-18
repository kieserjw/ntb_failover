cd /root/jkieser

rpm -Uvh bison-2.7-4.el7.x86_64.rpm
rpm -Uvh byacc-1.9.20130304-3.el7.x86_64.rpm
rpm -Uvh m4-1.4.16-10.el7.x86_64.rpm
rpm -Uvh flex-2.5.37-3.el7.x86_64.rpm

tar -xvf netperf-2.7.0.tar.gz
tar -xvf libpcap-1.7.4.tar.gz
tar -zxvf ucarp-1.5.1.tar.bz2

cd /root/jkieser/netperf-2.7.0
./configure
make install

cd /root/jkieser/libpcap-1.7.4
./configure 
make install

cd /root/jkieser/ucarp-1.5.1
./configure
make install


