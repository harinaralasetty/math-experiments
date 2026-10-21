"""Mutation tests for the static-site validation boundary."""
import unittest
from check_site import validate_html

GOOD = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Example</title></head><body><main><h1>Example</h1><p>Text <a href="index.html">Home</a></p></main></body></html>'


class ValidatorTests(unittest.TestCase):
    def test_accept_valid_document(self):
        validate_html(GOOD)

    def test_reject_misnested_elements(self):
        with self.assertRaises(AssertionError):
            validate_html(GOOD.replace('</a></p>', '</p></a>'))

    def test_reject_missing_alt(self):
        with self.assertRaises(AssertionError):
            validate_html(GOOD.replace('</p>', '<img src="x.png"></p>'))

    def test_reject_block_in_paragraph(self):
        with self.assertRaises(AssertionError):
            validate_html(GOOD.replace('Text ', '<div>Text</div>'))

    def test_reject_duplicate_attribute(self):
        with self.assertRaises(AssertionError):
            validate_html(GOOD.replace('lang="en"', 'lang="en" lang="fr"'))

    def test_reject_unknown_element(self):
        with self.assertRaises(AssertionError):
            validate_html(GOOD.replace('Text ', '<madeup>Text</madeup>'))


if __name__ == '__main__':
    unittest.main()
