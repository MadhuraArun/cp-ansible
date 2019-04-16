#This is a python script used to create an Ansible Inventory hosts.yml file for Confluent Platform
#This script obtains the public and private IPs of the EC2 instances belonging to the ConfluentDemo group
#The public IPs are updated in the hosts.yml file accordingly


#!/bin/python
import os

#Get public IP addresses of group ConfluentDemo, sort and input it to pubIP.txt
os.system("aws ec2 describe-instances --filters  'Name=tag:Name,Values=PreDemo-Confluent' | grep PublicIpAddress | grep -o -P '\d+\.\d+\.\d+\.\d+' | grep -v '^10\.' | sort -u > pubIP.txt")

#Get private IP addresses of group ConfluentDemo, sort and input it to priIP.txt
os.system("aws ec2 describe-instances --filters  'Name=tag:Name,Values=PreDemo-Confluent' | grep PrivateIpAddress | grep -o -P '\d+\.\d+\.\d+\.\d+' | grep -v '^10\.' | sort -u > priIP.txt")

#Open pubIP.txt in read mode
f1=open("priIP.txt","r")

#Create an array of all the IP addresses
rd=f1.read().splitlines()

#Write in the Ansible Inventory hosts.yml
os.system("echo all: >> hosts.yml")
os.system("echo '  vars:' >> hosts.yml")
os.system("echo '    ansible_connection: ssh' >> hosts.yml")
os.system("echo '    ansible_ssh_user: ec2-user' >> hosts.yml")
os.system("echo '    ansible_become: true' >> hosts.yml")
os.system("echo '    ansible_ssh_private_key_file: /home/ec2-user/Confluent.pem' >> hosts.yml")
os.system("echo '    security_mode: plaintext' >> hosts.yml")

#Get preflight host IPs
os.system("echo preflight: >> hosts.yml")
os.system("echo '  hosts:' >> hosts.yml")
x1=len(rd)
for i in range(0,x1):
    final=rd[i]
    #Write the preflight host IPs into hosts.yml
    os.system("echo '    {}:' >> hosts.yml".format(final))

#Get ssl_CA hosts
#os.system("echo ssl_CA: >> hosts.yml")
#os.system("echo '\thosts:' >> hosts.yml")
#for i in range(0,4):
#    final=rd[i]
#    #Write the preflight hosts into hosts.yml
#    os.system("echo '\t\t{}:' >> hosts.yml".format(final))

#Get zookeeper hosts
os.system("echo zookeeper: >> hosts.yml")
os.system("echo '  hosts:' >> hosts.yml")
for i in range(0,3):
    final=rd[i]
    #Write the zookeeper hosts into hosts.yml
    os.system("echo '    {}:' >> hosts.yml".format(final))

#Get broker hosts
os.system("echo broker: >> hosts.yml")
os.system("echo '  hosts:' >> hosts.yml")
for i in range(0,3):
    final=rd[i]
    #Write the broker hosts into host.yml
    os.system("echo '    {}:' >> hosts.yml".format(final))
    os.system("echo '      kafka:' >> hosts.yml")
    os.system("echo '        broker:' >> hosts.yml")
    os.system("echo '          id: {}' >> hosts.yml".format(i+1))

#Get schema-registry hosts
os.system("echo schema-registry: >> hosts.yml")
os.system("echo '  hosts:' >> hosts.yml")
final=rd[3]
#Write the schema-registry hosts into host.yml
os.system("echo '    {}:' >> hosts.yml".format(final))

#Get control-center hosts
os.system("echo control-center: >> hosts.yml")
os.system("echo '  hosts:' >> hosts.yml")
final=rd[3]
os.system("echo '    {}:' >> hosts.yml".format(final))
os.system("echo '      confluent:' >> hosts.yml")
os.system("echo '        control:' >> hosts.yml")
os.system("echo '          center:' >> hosts.yml")
os.system("echo '            config:' >> hosts.yml")
final=rd[3]
os.system("echo '              confluent.controlcenter.connect.cluster: {}:8083' >> hosts.yml".format(final))

#Get connect-distributed hosts
os.system("echo connect-distributed: >> hosts.yml")
os.system("echo '  hosts:' >> hosts.yml")
final=rd[3]
#Write the connect-distributed hosts into host.yml
os.system("echo '    {}:' >> hosts.yml".format(final))

#Get kafka-rest hosts
os.system("echo kafka-rest: >> hosts.yml")
os.system("echo '  hosts:' >> hosts.yml")
final=rd[3]
#Write the kafka-rest hosts into host.yml
os.system("echo '    {}:' >> hosts.yml".format(final))

#Get ksql hosts
os.system("echo ksql: >> hosts.yml")
os.system("echo '  hosts:' >> hosts.yml")
final=rd[3]
#Write the ksql hosts into host.yml
os.system("echo '    {}:' >> hosts.yml".format(final))

#Get tools hosts
os.system("echo tools: >> hosts.yml")
os.system("echo '  hosts:' >> hosts.yml")
final=rd[0]
#Write the tools hosts into host.yml
os.system("echo '    {}:' >> hosts.yml".format(final))

