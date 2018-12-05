# nice-ml
PoC using the `nice` command in Linux

## Getting started

First, use `virtualenv` to build the Python virtual environment containing a few necessary third-party packages:

```{shell}
$ ./create_virtual_environment.sh
```

If the environment isn't automatically accessed, run `source venv/bin/activate`. `(venv)` should appear at the left of your console.

Next, open a `screen` session and run `./runner.sh`. You'll be emailed (at least, *I'll* be emailed, unless you change the email in `runner.sh`) once the job completes.

**Note**: although machine learning training workflows are very resource-intensive, the frequency with which these jobs run is completely dependent on your use case. Typical retraining schedules are weekly or monhtly, so whatever level of resource utilization accompanies your job, know that job won't be running all day, every day.
