# Interview

## Problem 1

Extend this program to print the count of 5 tuples in the log. A 5 tuple is
represented by the combination of source ip, destination ip, source port,
destination port and protocol.

Sample log:

```log
2 123456789010 eni-1235b8ca123456789 172.31.16.139 172.31.16.21 143 143 6 20 4249 1418530010 1418530070 ACCEPT OK
2 123456789010 eni-1235b8ca123456789 172.31.16.139 172.31.16.21 143 143 6 20 4249 1418530010 1418530070 ACCEPT OK
2 123456789010 eni-1235b8ca123456789 172.31.16.139 172.31.16.21 143 143 6 20 4249 1418530010 1418530070 ACCEPT OK
2 123456789010 eni-1235b8ca123456789 172.31.16.139 172.31.16.21 144 144 6 20 4249 1418530010 1418530070 ACCEPT OK
```

Sample output:

```
172.31.16.139 172.31.16.21 143 143 6 -> 3
172.31.16.139 172.31.16.21 144 144 6 -> 1
```

## Problem 2

We can have up to a Billion records. Each log line would max 256 bytes.

We will develop this on AWS. Lets assume we will be using typical EC2 instances
in AWS, each instance has 64 GB RAM 32 core CPU. You may use more instances if
needed.

Process these records <= 5 secs
