# dehasher

QOL script for querying the DeHashed API.

_Note: For performing API queries both a DeHashed account with an active subscription and API credits are required._ 


### Usage

```
usage: dehasher.py [-h] [-q QUERY] -o OUTPUT_FILE [-i INPUT_FILE]

Query DeHashed API and dump data to disk

optional arguments:
  -h, --help      show this help message and exit
  -q QUERY        API query to execute, e.g. "-q google.co.uk"
  -o OUTPUT_FILE  Name to use for output files, e.g. "-o dump" will output dump.json & dump.csv
  -i INPUT_FILE   Input JSON file for if not wanting to perform an API query (used for testing purposes to avoid spending API credits)
```

### References
- [https://www.dehashed.com/docs](https://www.dehashed.com/docs)