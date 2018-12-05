#!/bin/bash

# Remove a bunch of extraneous output
cat ./results/utilization.txt |
	grep -v $USER |
	grep -v KiB |
	grep -v PID |
	grep -v Tasks |
	grep -v -e '^$' |
	grep -v JOB |
	grep -v Entire |
	sed 'N;s/\n/ /' > ./results/utilization_parsed.txt

# Manually check when jobs were completed
# and put that information back into script
cat ./results/utilization.txt | grep -E 'JOB|Entire'