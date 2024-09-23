# parse-flow-logs

Illumio Technical Assessment 2024

## Problem

Write a program that can parse a file containing [flow log data](./flowlogs.txt)
and maps each row to a tag based on a lookup table. The [lookup
table](./lookup.csv) has 3 columns, `dstport`, `protocol`, `tag`. The `dstport`
and `protocol` combination decide what `tag` can be applied.

## Requirements

The program should generate an output file containing the following:

1. Tag Counts: Count of matches for each tag, sample o/p shown below

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
