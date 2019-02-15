from unittest import TestCase
from unittest.mock import patch
from process import main
import argparse

from processor import WaypointListProcessor, WaypointStreamProcessor


class TestProcessMain(TestCase):

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(list=True, source="whatever"))
    def test_process_with_invalid_source(self, mock_args):
        with self.assertRaises(SystemExit) as sys_ex:
            main()
        self.assertEqual(sys_ex.exception.code, 0)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(list=False, stream=True,
                                           source="data/waypoints.json"))
    def test_stream_processer(self, mock_args):
        with patch.object(WaypointStreamProcessor, 'process_waypoint',
                          return_value=[]) as mock_method:
            main()
        self.assertEqual(mock_method.called, True)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(list=True, stream=False,
                                           source="data/waypoints.json"))
    def test_list_processer(self, mock_args):
        with patch.object(WaypointListProcessor, 'get_trips',
                          return_value=[]) as mock_method:
            main()
        self.assertEqual(mock_method.called, True)
