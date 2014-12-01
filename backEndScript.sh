#!/bin/bash 
for i in backTestCases/masterAccounts/*.txt
do
	#move the valid accounts file for the required test case to the in directory
	cp $i in/masterAccounts.txt

	cp backTestCases/transactionSum/transactionSummary_$(basename $i .txt).txt out/transactionSummary/transactionSummary.txt
	
	for j in $i
	do
		echo $j
		echo $i
	done | python ../backEnd.py <$i \ >out/logBackEnd/$(basename $i .txt).txt.log

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
