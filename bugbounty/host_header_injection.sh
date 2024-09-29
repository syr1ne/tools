#!/bin/bash

httpx_file=$1

if ! [[ -n $1 ]]
then
  echo "provide httpx file with status codes"
  exit
fi

echo "creating files based on status codes"
cat $1 | grep "503" | cut -d " " -f1 | anew "503.txt" > /dev/null
echo ""

# getting all the subject alternative names (SANs) on TLS Certificate
echo "getting all unaccessable SANs domains"
echo ""
for url503 in $(cat "503.txt" | cut -d "/" -f3)
do
  openssl s_client -connect $url503:443 2>&1 < /dev/null | openssl x509 -noout -text | grep "DNS:" | tr ',' '\n' | cut -d ":" -f2 | grep -v "*" | httpx -fc 200,301,302 -silent | anew sans-hosts.txt
done
echo ""
echo "SANs domains fetched"
echo ""

# using sans domain for testing host header
echo "looking for host header injection"
echo ""
for url503 in $(cat "503.txt" | cut -d "/" -f3)
do
  for host in $(cat sans-hosts.txt | cut -d "/" -f3)
  do
    result=$(httpx -u "$url503" -H "Host: $host" -mc 200 --silent)
    
    if [[ -z $result ]]
    then
      continue
    fi

    if ! [[ $result == $url503 ]]
    then
      echo "url: "$url503" host: $host"
    fi
    result=""
  done
done
echo ""
echo "scan completed"
echo ""
