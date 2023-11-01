#! /bin/bash

sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 --source 192.168.1.221 --destination 192.168.1.222  -j DNAT --to-destination 192.168.1.64
nginx -c /etc/nginx/nginx.conf &

tail -f /dev/null