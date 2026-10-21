"""Mutate real rendered pages to prove the publication checks detect damage."""
import shutil
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import check_site


class GeneratedSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='math-site-check-')
        self.original = check_site.DOCS
        self.docs = Path(self.temp.name)/'docs'
        shutil.copytree(self.original,self.docs)
        check_site.DOCS = self.docs

    def tearDown(self):
        check_site.DOCS = self.original
        self.temp.cleanup()

    def change_home(self, old, new):
        p = self.docs/'index.html'; text = p.read_text()
        assert old in text
        p.write_text(text.replace(old,new,1))

    def test_reject_rendered_number_tampering(self):
        self.change_home('577 new terms','578 new terms')
        with self.assertRaises(AssertionError): check_site.check_pages()

    def test_reject_broken_internal_link(self):
        self.change_home('href="oeis/index.html"','href="oeis/missing.html"')
        with self.assertRaises(AssertionError): check_site.check_pages()

    def test_reject_duplicate_page_title(self):
        self.change_home('<title>Computer-Verified Mathematics</title>',
                         '<title>BB(6) local lemmas and unresolved proof gap</title>')
        with self.assertRaises(AssertionError): check_site.check_pages()

    def test_reject_invalid_json_ld(self):
        self.change_home('"@type": "WebSite"','"@type": BROKEN')
        with self.assertRaises(ValueError): check_site.check_pages()

    def test_reject_sitemap_omission(self):
        p = self.docs/'sitemap.xml'
        tree = ET.parse(p)
        namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        target = next(node for node in tree.getroot()
                      if node.find('s:loc', namespace).text == check_site.BASE+'bb6.html')
        tree.getroot().remove(target)
        tree.write(p, encoding='utf-8', xml_declaration=True)
        with self.assertRaises(AssertionError): check_site.check_pages()


if __name__ == '__main__':
    unittest.main()
