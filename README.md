# parse-flow-logs

Illumio Technical Assessment 2024

## Problem

Write a program that can parse a file containing [flow log data](./flowlogs.txt)
and maps each row to a tag based on a lookup table. The [lookup
table](./lookup.csv) has 3 columns, `dstport`, `protocol`, `tag`. The `dstport`
and `protocol` combination decide what `tag` can be applied.

## Assumptions

1. The flow log file will have at least 14 fields in each line. If a line has
   less than 14 fields, it will be skipped.
2. The protocols are populated from the [protocols file](/protocols.csv). It has
   the popular protocols listed in the format of `protocol number,protocol
   name`. If a protocol is not found in this CSV file, it will be counted as
   `unknown`.

## Usage

```bash
python3 parse_flow_logs.py
```

The program will read the flow logs from `flowlogs.txt` and the lookup table
from `lookup.csv`. It will write the output to `tc_output.txt` and
`ppc_output.txt`.

## Requirements

The program should generate an output file containing the following:

1. Tag Counts: Count of matches for each tag

   ```
   Tag,Count
   sv_P2,1
   sv_P1,2
   sv_P4,1
   email,3
   Untagged,9
   ```

2. Port/Protocol Combination Counts: Count of matches for each port/protocol
   combination

   ```
   Port,Protocol,Count
   22,tcp,1
   23,tcp,1
   25,tcp,1
   110,tcp,1
   143,tcp,1
   443,tcp,1
   993,tcp,1
   1024,tcp,1
   49158,tcp,1
   80,tcp,1
   ```

## Specifications

- Input file as well as the file containing tag mappings are plain text (ascii)
  files.
- The flow log file size can be up to 10 MB.
- The lookup file can have up to 10000 mappings.
- The tags can map to more than one port, protocol combinations. For e.g. sv_P1
  and sv_P2 in the sample above.
- The matches should be case insensitive.

For anything else that is not clear, please make reasonable assumptions and
document those in the Readme to be sent with your submission.

## Notes

### `flowlogs.txt`

Each line in the log entry follows the format of an AWS VPC Flow Log which
records network traffic information for the VPC in AWS. The fields in the log
entry are separated by spaces.

```log
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
```

The fields in the log entry are as follows:

```log
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
```

The required fields are :

7. Destination Port (`dstport`) [integer]
8. Protocol (`protocol`) [tcp/udp/icmp]

Reference:
https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields

### `lookup.csv`

The lookup table is used to map the destination port and protocol to a tag.

```csv
dstport,protocol,tag
25,tcp,sv_P1
```

The fields in the lookup table are as follows:

1. Destination Port (`dstport`) [integer]
2. Protocol (`protocol`) [tcp/udp/icmp]
3. Tag (`tag`) [string]
