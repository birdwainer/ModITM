# ModITM

```sh
iptables -A PREROUTING -i eth0 -p tcp --dport 80 --source 192.168.1.221 --destination 192.168.1.222  -j DNAT --to-destination 192.168.1.64
```