#!/bin/bash

rm results/*

printf "Entire workflow started $(date +'%A, %d %B %Y %H:%M:%S')\n" >> results/utilization.txt

# Start recording system metrics
if [ "$HOSTNAME" == "<YOUR LOCAL $HOSTNAME HERE>" ]; then
	echo "Running locally"
	
	n_samples=1000;
	sleep_seconds=5;
	top_delay=5;

	top -U $USER -s $top_delay >> results/utilization.txt &
else
	echo "Running remotely"

	n_samples=1000000;
	sleep_seconds=$((60 * 60 * 4));
	top_delay=15;

	top -U $USER -b -d $top_delay >> results/utilization.txt &
fi

n_jobs=8;
cross_validate=False;

# Parse command-line input, too,
# overwriting n_samples if passed
POSITIONAL=()
while [[ $# -gt 0 ]]
	do
	key="$1"

	case $key in
		--n_samples)
		n_samples="$2"
		shift # past argument
		shift # past value
		;;
	esac
	case $key in
		--sleep_seconds)
		sleep_seconds="$2"
		shift
		shift
		;;
	esac
	case $key in
		--n_jobs)
		n_jobs="$2"
		shift
		shift
		;;
	esac
	case $key in
		--cross_validate)
		cross_validate="$2"
		shift # past argument
		shift # past value
		;;
	esac
done
set -- "${POSITIONAL[@]}"

printf "n_jobs: $n_jobs, n_samples: $n_samples, sleep_seconds: $sleep_seconds, cross_validate: $cross_validate\n"

# Sleep for a given time in order to record
# and understand system utilization before below processing
sleep $sleep_seconds

printf "\nJOBS_STARTING $(date +'%A, %d %B %Y %H:%M:%S')\n" >> results/utilization.txt

# Sample dataset, eight processors
python3 app.py \
	--n_samples $n_samples \
	--n_jobs $n_jobs \
	--cross_validate $cross_validate \
	--filename ./results/1.csv

printf "\nJOB_1_COMPLETE - $(date +'%A, %d %B %Y %H:%M:%S')\n" >> results/utilization.txt

# Nice things up, lower priority (higher `nice` value means lower priority versus default of 10)
nice -15 python3 app.py \
	--n_samples $n_samples \
	--n_jobs $n_jobs \
	--cross_validate $cross_validate \
	--filename ./results/2.csv

printf "\nJOB_2_COMPLETE - $(date +'%A, %d %B %Y %H:%M:%S')\n" >> results/utilization.txt

# Nice things up, higher priority (lower `nice` value means higher priority versus default of 10)
nice -5 python3 app.py \
	--n_samples $n_samples \
	--n_jobs $n_jobs \
	--cross_validate $cross_validate \
	--filename ./results/3.csv

printf "\nJOB_3_COMPLETE - $(date +'%A, %d %B %Y %H:%M:%S')\n" >> results/utilization.txt

mail -s 'nice-ml: retraining sections completed. Still sleeping for a bit' <YOUR EMAIL HERE> < /dev/null

sleep $sleep_seconds

kill %1