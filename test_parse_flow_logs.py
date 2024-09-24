import unittest

from unittest.mock import patch, mock_open, Mock
from io import StringIO

from parse_flow_logs import (
    load_protocols, create_lookup_table, parse_flow_logs, write_output,
    PROTOCOLS, LOOKUP
)


class TestFlowLogParser(unittest.TestCase):

    def setUp(self):
        # Reset global dictionaries before each test
        PROTOCOLS.clear()
        LOOKUP.clear()

    @patch('builtins.open', new_callable=mock_open, read_data="number,name\n1,ICMP\n6,TCP\n17,UDP")
    def test_load_protocols(self, mock_file):
        load_protocols('dummy_protocols.csv')
        self.assertEqual(PROTOCOLS, {1: 'icmp', 6: 'tcp', 17: 'udp'})

    @patch('builtins.open', new_callable=mock_open, read_data="dstport,protocol,tag\n80,TCP,HTTP\n443,TCP,HTTPS\n53,UDP,DNS")
    def test_create_lookup_table(self, mock_file):
        create_lookup_table('dummy_lookup.csv')
        self.assertEqual(LOOKUP, {(80, 'tcp'): 'HTTP',
                         (443, 'tcp'): 'HTTPS', (53, 'udp'): 'DNS'})

    @patch('builtins.open')
    def test_parse_flow_logs(self, mock_open):
        # Populate PROTOCOLS and LOOKUP dictionaries in the parse_flow_logs module
        PROTOCOLS.update({6: 'tcp', 17: 'udp'})
        LOOKUP.update({(80, 'tcp'): 'tag_1', (443, 'tcp')
                      : 'tag_1', (53, 'udp'): 'tag_2'})

        mock_file_content = StringIO(
            "2 1234 eni-0ab 192.168.1.1 10.0.0.1 12345 80 6 1000 2000 1620140761 1620140821 ACCEPT OK\n"
            "2 1234 eni-0ab 192.168.1.2 10.0.0.2 54321 443 6 1500 3000 1620140761 1620140821 ACCEPT OK\n"
            "2 1234 eni-0ab 192.168.1.3 10.0.0.3 56789 53 17 500 1000 1620140761 1620140821 ACCEPT OK\n"
            "2 1234 eni-0ab 192.168.1.4 10.0.0.4 65432 8080 6 2000 4000 1620140761 1620140821 ACCEPT OK\n"
        )
        mock_open.return_value = mock_file_content

        tag_counts, port_protocol_counts = parse_flow_logs(
            'dummy_flow_logs.txt')

        self.assertEqual(len(tag_counts), 3)
        self.assertEqual(tag_counts['tag_1'], 2)
        self.assertEqual(tag_counts['tag_2'], 1)
        self.assertEqual(tag_counts['untagged'], 1)

        self.assertEqual(len(port_protocol_counts), 4)
        self.assertEqual(port_protocol_counts[(80, 'tcp')], 1)
        self.assertEqual(port_protocol_counts[(443, 'tcp')], 1)
        self.assertEqual(port_protocol_counts[(53, 'udp')], 1)
        self.assertEqual(port_protocol_counts[(8080, 'tcp')], 1)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_output(self, mock_file):
        tag_counts = {'tag_1': 2, 'tag_2': 1, 'untagged': 1}
        port_protocol_counts = {
            (80, 'tcp'): 1, (443, 'tcp'): 1, (53, 'udp'): 1, (8080, 'tcp'): 1}

        write_output(tag_counts, port_protocol_counts)

        # Check if the files were opened for writing
        mock_file.assert_any_call('tc_output.txt', 'w')
        mock_file.assert_any_call('ppc_output.txt', 'w')

        # Check if the files were written correctly
        mock_file().write.assert_any_call("Tag,Count\n")
        mock_file().write.assert_any_call("tag_1,2\n")
        mock_file().write.assert_any_call("tag_2,1\n")
        mock_file().write.assert_any_call("untagged,1\n")

        mock_file().write.assert_any_call("Port,Protocol,Count\n")
        mock_file().write.assert_any_call("80,tcp,1\n")
        mock_file().write.assert_any_call("443,tcp,1\n")
        mock_file().write.assert_any_call("53,udp,1\n")
        mock_file().write.assert_any_call("8080,tcp,1\n")


if __name__ == '__main__':
    unittest.main()
