#!/bin/bash
# Put this test script at .git/hooks/pre-commit and make it +x mode
# Prevent a commit if the program won't run

# Test normal files (not server, not tester)
for file in `ls *.py`
do
	if [[ "$file" != "server.py" && "$file" != "tester.py" ]]; then
		python $file
		if [ $? -ne 0 ]; then
			echo "Unit tests failed in file" "$file"
			echo "Aborting tests"
			exit 1
		fi
	fi
done


python server.py --unit-tests
if [ $? -ne 0 ]; then
	echo "Error: Server doesn't run or tests failed"
	echo "Go fix it before you commit"
	exit 1
fi
