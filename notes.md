# Summary of results, started on 2018/12/04

## Procedure:

Command: `./runner.sh`

1. Using a `screen` session for this entire procedure, start recording server-wide capacity metrics using `top` on <SERVER_NAME>
2. Sleep for 4 hours, capturing a snapshot of four hours' worth of utilization on that server
	- **Observations**:
		- CPU load usually stays between 3.5-4.5%
		- One very large spike over a two-minute interval from 17:17 to 17:19
		- Slight uptick in utilization post-business hours (from ~3.5% average to ~4.5%)
3. Begin jobs
	- Notes:
		- Eight (8) parallel processes specified for all
		- Number of samples: 1,000,000
		- Number of features: 75
	- Job 1:
		- Run process with default `nice`ness of 0 (same `nice`ness as `python3 -c 'import os;print(os.nice(0))` would show)
		- **Observations**:
			- This job looks to be the cause of CPU spiking to ~10-12% on average over the 1.5-hour duration
			- Major spike (likely from other processes kicking off) from 19:40-19:46
				- Max CPU of 77%
			- Cross-validation workflow brings CPU to around 25%
				- Lasts around 15 minutes
	- Job 2:
		- `nice`ness of 15, meaning a lower priority versus default
		- **Observations**:
			- This job looks to be the cause of CPU spiking to ~9-10% on average over the 1.5-hour duration
			- No other major spikes (likely due to no other jobs being scheduled in relatively short window)
			- Cross-validation workflow brings CPU to around 25%
				- Lasts around 15 minutes
	- Job 3:
		- `nice`ness of 5, meaning a lower priority versus default, but higher than job 2
		- **Observations**:
			- This job looks to be the cause of CPU spiking to ~9-10% on average over the 1.5-hour duration
			- No other major spikes (likely due to no other jobs being scheduled in relatively short window)
			- Cross-validation workflow brings CPU to around 25%
				- Lasts around 15 minutes
4. Sleep, again...
	- CPU utilization returns to around 3.5-4.5%

## Additional notes:

More science *could be* required, but from these results, it looks like the `nice`ness of a CPU-intensive process like this *may* have a significant effect on server utilization, **but the actual size of that effect is small (maybe 1%, eyeballing things)**.

Irrespective of `nice`ness, this workflow roughly triples server-wide CPU utilization over its ~2-hour duration, taking usage from around 4% to between 9-12%. Over the course of this sequence of 3 CPU-intensive processes, we saw a few instances of other jobs running simultaneously that brought CPU upwards of 50% for relatively short periods of time (5-10 minutes).

Effect of increasing `n_samples` or `n_features`: computation time increases, but CPU utilization stays (relatively) constant. Instead of processing `n` samples or `k` features, instead you're processing `n + m` samples or `k + j` features **at *p*% CPU utilization**, the latter case for likely a longer time (because of more data to process). More data, but the same utilization, just for a longer time.

## Conclusion:

Since retraining workflows such as these occur relatively infrequently - anywhere from biweekly to monthly - this CPU-intensive workload should not present any issues when running on any of the relevant dedicated servers. Measures can be taken (e.g. scheduling the retraining in off-hours) to minimize risk of impacting the core integrity of the dedicated servers, but there seems to be little risk in the first place.

Scoring/prediction workflows are not as CPU-intensive as those of retraining, so they also should not present any issues.