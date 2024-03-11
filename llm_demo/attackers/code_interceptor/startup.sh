#! /bin/bash

sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 11434 --source 192.168.2.24 --destination 192.168.2.221  -j DNAT --to-destination 192.168.2.32

poetry run python3 code_interceptor.py