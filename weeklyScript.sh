#!/bin/bash 
echo "hello"
for i in testCases/*.txt
do
	echo $i
	sh dailyScript.sh $(basename $i .txt).txt
done
