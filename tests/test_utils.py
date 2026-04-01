import datetime
import unittest
from pathlib import Path

from xmltv import xmltv, utils

test_data = Path(__file__).parent.joinpath('test_data')


class TestUtils(unittest.TestCase):
    def test_merge(self):
        file1 = test_data.joinpath('disneychannel.no', 'xmltv-go', 'disneychannel.no_2026-03-31.xml')
        file2 = test_data.joinpath('disneychannel.no', 'xmltv-go', 'disneychannel.no_2026-04-01.xml')
        tz = datetime.timezone(datetime.timedelta(hours=2))
        date = datetime.datetime(2026, 4, 1, tzinfo=tz)
        merged = utils.merge_days(date, xmltv.parse_file(file1), xmltv.parse_file(file2))
        self.assertEqual('Phineas og Ferb', str(merged[0].title))
        self.assertEqual('Kiff', str(merged[- 1].title))
