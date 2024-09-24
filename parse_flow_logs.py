import csv
from collections import defaultdict

import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


LOOKUP = {}
PROTOCOLS = {}


def load_protocols(protocols_file):
    """
    Read protocols file and populate the dictionary.

    PROTOCOLS = {
        protocol_number: protocol_name
    }
    """
    logging.info(f"Loading protocols from {protocols_file}")
    with open(protocols_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            PROTOCOLS[int(row['number'])] = row['name']


def create_lookup_table(lookup_file):
    """
    Read lookup table and populate the lookup dictionary. The key is a tuple of
    (dstport, protocol), and the value is the tag.

    LOOKUP = {
        (dstport, protocol): tag
    }
    """
    logging.info(f"Creating lookup table from {lookup_file}")
    with open(lookup_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (int(row['dstport']), row['protocol'].lower())
            LOOKUP[key] = row['tag']


def parse_flow_logs(flow_log_file):
    """
    Parse flow logs and update the tag_counts and port_protocol_counts
    dictionaries.
    """
    logging.info(f"Parsing flow logs from {flow_log_file}")
    with open(flow_log_file, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            fields = line.strip().split()
            if len(fields) < 14:
                logging.warning(
                    f"\nInvalid line: less than 14 fields at line {line_number}, skipping it \n{line}")
                continue

            dstport = int(fields[6])
            protocol = PROTOCOLS.get(int(fields[7]), 'unknown')

            key = (dstport, protocol)
            tag = LOOKUP.get(key, 'untagged')

            tag_counts[tag] += 1
            port_protocol_counts[key] += 1


# Setup
flow_log_file = 'flowlogs.txt'
lookup_file = 'lookup.csv'

protocols_file = 'protocols.csv'

create_lookup_table(lookup_file)
load_protocols(protocols_file)

tag_counts_output_file = 'tc_output.txt'
port_protocol_counts_output_file = 'ppc_output.txt'

# Initialize counters
tag_counts = defaultdict(int)
port_protocol_counts = defaultdict(int)

# Parse flow logs
parse_flow_logs(flow_log_file)

# Write output
logging.info(
    f"Writing output to the files, {tag_counts_output_file} and {port_protocol_counts_output_file}")
with open(tag_counts_output_file, 'w') as f:
    f.write("Tag,Count\n")
    for tag, count in tag_counts.items():
        f.write(f"{tag},{count}\n")

with open(port_protocol_counts_output_file, 'w') as f:
    f.write("Port,Protocol,Count\n")
    for (port, protocol), count in port_protocol_counts.items():
        f.write(f"{port},{protocol},{count}\n")
