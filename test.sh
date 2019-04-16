#!/bin/bash

#Create a new Certificate Authority(CA) to generate SSL/TSL certificates
openssl req -new -newkey rsa:4096 -days 365 -x509 -subj "/CN=Kafka-Security-CA" -keyout ca-key -out ca-cert -nodes

#Create a keystore for Kafka broker
keytool -genkey -keystore kafka.server.keystore.jks -validity 365 -storepass password -keypass password -dname "CN=*.hashedin.com" -storetype pkcs12

#Obtain a signing request
keytool -keystore kafka.server.keystore.jks -certreq -file cert-file -storepass password -keypass password

#Sign the certificate
openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days 365 -CAcreateserial -passin pass:password

#Create a truststore
keytool -keystore kafka.server.truststore.jks -alias CARoot -import -file ca-cert -storepass password -keypass password -noprompt

#Add the signing request to the keystore
keytool -keystore kafka.server.keystore.jks -alias CARoot -import -file ca-cert -storepass password -keypass password -noprompt

#Add the signed certificate to the keystore
keytool -keystore kafka.server.keystore.jks -import -file cert-signed -storepass password -keypass password -noprompt

#Add the Certificate request to the the client truststore
keytool -keystore kafka.client.truststore.jks -alias CARoot -import -file ca-cert -storepass password -keypass password -noprompt

#Create a file called client.properties
touch client.properties

#Add the following lines to the client.properties file
echo "security.protocol=SSL" >> client.properties
echo "ssl.truststore.location=/home/kafka/ssl/kafka.client.truststore.jks
" >> client.properties
echo "ssl.truststore.password=password" >> client.properties

