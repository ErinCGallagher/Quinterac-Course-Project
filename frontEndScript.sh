#!/bin/bash 
for i in testCases/*.txt
do
	#move the valid accounts file for the required test case to the in directory
	cp testAccount/$(basename $i .txt)_validAccounts.txt in/validAccounts.txt
	
	for j in $i
	do
		echo $j
	done | python ../frontEnd.py <$i \ >out/log/$(basename $i .txt).txt.log
 
	#moves the transaction summary file to the logSum folder for storing
	cp out/transactionSummary.txt out/logSum/$(basename $i .txt)_transactionSummary.txt

	#compare the terminal output file to the expectedOutput file 
	diff -c -b -B out/log/$(basename $i .txt).txt.log expOut/testCases/$(basename $i .txt).txt.log >> out/failLog.txt
	
	#compares the transaction summary file outputed to the expect transaction summary file
	diff -c -b -B out/logSum/$(basename $i .txt)_transactionSummary.txt expOut/transactionSummary/$(basename $i .txt)_transactionSummary.txt >> out/failLog.txt

done

# we had 5 directories 
#expOut contain 2 directories : 
	#testCases --> stored the expected terminal output
	#transactionSummary --> stored the expected transaction summary file
#testAccount --> stored the required input test Account files
#testCases --> store the required terminal input for each test cases as txt files
#in --> the script movedthe reuqired validAccounts file in here and renamed it so the program could access it as input
#out contained 2 directories:
	#log --> stored the outputted terminal logs from the program
	#logSum --> stored the outputted transactionSummary files from the program
	# the failLog was stored in the out directory
