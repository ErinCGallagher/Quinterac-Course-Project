#!/bin/bash 

#validAccounts.txt inside in dir
echo $1
rm out/transactionSummary/*
python ../frontEnd.py <testCases/$1 \ >out/log/"frontEnd"+$(date +"%Y-%m-%d-%S").txt.log

#moves the transaction summary file to the logSum folder for storing
#cp out/transactionSummary/* out/logSum/transactionSummary.txt.log

python ../backEnd.py <in/masterAccounts.txt \ >out/logBackEnd/"backEnd"+$(date +"%Y-%m-%d-%S").txt.log
cp in/masterAccounts.txt out/logBackEnd/masterAccounts+$1
