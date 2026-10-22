"""Stage 4 publication coverage, including sequences whose offset is one."""
import json
import unittest
from pathlib import Path
from lxml import html
from site_data import ROOT, load_verification


class Stage4Tests(unittest.TestCase):
    def test_stage4_ranges_and_downloads_reach_published_pages(self):
        sequences = {row['id']: row for row in load_verification()['sequences']}
        for a in ['A304382', 'A320052', 'A325549', 'A336131', 'A353426']:
            with self.subTest(sequence=a):
                self.assertIn(a, set(sequences))
                seq = sequences[a]
                meta = json.loads((ROOT/'oeis/data'/f'{a}.json').read_text())
                first = int(meta['offset'].split(',')[0])
                rows = (ROOT/'docs/data'/f'{a}.txt').read_text().splitlines()
                self.assertEqual([int(row.split()[0]) for row in rows],
                                 list(range(first, seq['last']+1)))
                doc = html.parse(str(ROOT/'docs/oeis'/f'{a}.html'))
                self.assertIn(f'{first} through {seq["listed_last"]}',
                              doc.xpath(f'string(//section[@id="{a}-range"])'))
                self.assertEqual(doc.xpath('//pre[@class="terms"]/text()')[0].splitlines(), rows[:20])


if __name__ == '__main__':
    unittest.main()
