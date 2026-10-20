#!/usr/bin/env python3

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).with_name('check_vault.py')


def document(title, body, kind='note'):
    return '''---
title: "{}"
type: {}
status: draft
updated: 2026-10-20
tags: ["test"]
verification: unverified
---

# {}

{}
'''.format(title, kind, title, body)


class VaultChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='discoverable-check-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '10 Knowledge').mkdir()
        self.home = self.root / 'Discoverable Home.md'
        self.note = self.root / '10 Knowledge/Example.md'
        self.home.write_text(document('Discoverable Home', '[[Example#Evidence]]'))
        self.note.write_text(document('Example', '## Evidence\n\nSaved evidence. ^record'))

    def check(self, expected_error=None):
        result = subprocess.run([sys.executable, str(CHECKER), str(self.root)], text=True, capture_output=True)
        output = result.stdout + result.stderr
        if expected_error is None:
            self.assertEqual(result.returncode, 0, output)
            self.assertIn('PASS:', output)
        else:
            self.assertNotEqual(result.returncode, 0, output)
            self.assertIn(expected_error, output)

    def test_valid_local_navigation(self):
        self.check()

    def test_broken_content_is_rejected(self):
        before = self.note.read_text()
        cases = {
            'frontmatter': (before.split('---', 2)[2].lstrip(), 'missing opening frontmatter'),
            'date': (before.replace('2026-10-20', '2026-02-30'), 'valid YYYY-MM-DD date'),
            'title': (before.replace('title: "Example"', 'title: "Different"'), 'title must match'),
            'target': (before + '\n[[Missing]]\n', 'missing internal target'),
            'fragment': (before + '\n[[Example#Absent]]\n', 'missing fragment'),
            'tags': (before.replace('["test"]', '[test]'), 'invalid JSON value'),
            'heading': (before.replace('## Evidence', '#### Evidence'), 'heading skips'),
            'list': (before + '\n- \n', 'empty list item'),
            'fence': (before + '\n```text\nunclosed\n', 'unmatched code fence'),
            'fence language': (before + '\n```\ntext\n```\n', 'requires a language marker'),
            'verification': (before.replace('verification: unverified\n', ''), 'missing required frontmatter key verification'),
            'review date': (before.replace('unverified', 'reviewed'), 'require a checked'),
        }
        for name, (content, message) in cases.items():
            with self.subTest(name=name):
                self.note.write_text(content)
                self.check(message)
        self.note.write_text(before)
        self.check()

    def test_orphan_and_unknown_folder(self):
        path = self.root / '10 Knowledge/Orphan.md'
        path.write_text(document('Orphan', 'Unlinked content.'))
        self.check('unreachable from Discoverable Home')
        path.unlink()
        (self.root / 'Unsorted').mkdir()
        (self.root / 'Unsorted/Stray.md').write_text(document('Stray', 'Content.'))
        self.home.write_text(self.home.read_text() + '\n[[Stray]]\n')
        self.check('outside the folders defined in Vault Structure')

    def test_code_is_not_interpreted_as_links(self):
        self.note.write_text(self.note.read_text() + '\n```text\n[[Missing]]\n```\n\n`[[Also Missing]]`\n')
        self.check()

    def test_unicode_and_block_fragments(self):
        self.note.write_text(self.note.read_text() + '\n## 中文标题\n\nDetails.\n')
        self.home.write_text(self.home.read_text() + '\n[[Example#中文标题]]\n\n[[Example#^record]]\n')
        self.check()


if __name__ == '__main__':
    unittest.main()
