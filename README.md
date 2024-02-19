# python-AMI-crawler
This repository is the implementation of the required python module as described in the assessment pdf.


## Repository Overview
<details>
<summary>Repository Structure</summary>

```text
.
├── README.md
├── Infrastructure Engineering - Coding Proficiency Assessment.pdf #requirements 
├── executor-sample-output.py
└── executor.py

```
</details>

## Implementation
[executor.py](https://github.com/tudoricc/python-AMI-crawler/blob/main/executor.py) - uses boto3 to query an aws account and to retrieve information about the instances and about each ami retrieved while describing the instances.

[executor-sample-output.py](https://github.com/tudoricc/python-AMI-crawler/blob/main/executor-sample-output.py) - doesn't use boto3 to query aws but instead creates mock data(the same data format that would be returned by running executor.py but with random instance-ids and amiIDs)

Both python modules  leverage the threadpool executor from Python to paralellize the AMI mapping(in accordance to the required output format)

## How to run
If you want to run it straight into a aws account you need to run the executor.py module but you need to modify some values in it: the AWS_PROFILE ([line 7](https://github.com/tudoricc/python-AMI-crawler/blob/main/executor.py#L7)) and regionToBeQueried([line 118](https://github.com/tudoricc/python-AMI-crawler/blob/main/executor.py#L118))
```bash
python3 executor.py
```

If you don't want to run it against an AWS account you can use  executor-sample-output.py that will create mock data for you(a lot of random information for ami and instances).
```bash
python3 executor-sample-output.py
```
