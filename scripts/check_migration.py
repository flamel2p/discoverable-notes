#!/usr/bin/env python3

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = '2bfd460bcad286f915bf360af80e7339a79c8078'
originals = subprocess.check_output(
    ['git', 'ls-tree', '-r', '--name-only', '-z', BASE], cwd=ROOT
).decode().split('\0')
originals = [name for name in originals if name.endswith('.md') and not name.startswith('.')]
assert len(originals) == 38, 'The migration baseline must contain exactly 38 notes.'
current = {}
for path in ROOT.rglob('*.md'):
    if any(part.startswith('.') for part in path.relative_to(ROOT).parts):
        continue
    text = path.read_text()
    match = re.search(r'^origin: (".*")$', text, re.M)
    if match:
        current.setdefault(json.loads(match[1]), []).append((path, text))

errors = []
urls = set()
blocks = 0
for old in originals:
    before = subprocess.check_output(['git', 'show', BASE + ':' + old], cwd=ROOT).decode()
    destinations = current.get(old, [])
    if not destinations:
        errors.append('No destination for ' + old)
        continue
    after = '\n'.join(text for _, text in destinations)
    if (ROOT / old).exists():
        errors.append('Original path still exists: ' + old)
    for match in re.finditer(r'https?://[^\s<>|]+', before):
        url = match.group()
        if before[max(0, match.start() - 2):match.start()] == '](' and url.endswith(')'):
            url = url[:-1]
        urls.add(url)
        if url not in after:
            errors.append('Missing original URL in ' + old + ': ' + url)
    for block in re.findall(r'```[^\n]*\n(.*?)```', before, re.S):
        blocks += 1
        original_lines = [line.rstrip() for line in block.strip().splitlines() if line.strip()]
        candidates = re.findall(r'```[^\n]*\n(.*?)```', after, re.S)
        if not any(original_lines == [line.rstrip() for line in candidate.strip().splitlines() if line.strip()] for candidate in candidates):
            errors.append('Changed or missing code/prompt block in ' + old)
    if old.startswith('Stock Analysis/') and '/Prompts/' not in old:
        for line in before.splitlines():
            if not line.strip() or line.startswith(('#', 'Data as of')) or re.fullmatch(r'[-| :]+', line):
                continue
            normalized = re.sub(r'\s+', '', line)
            if normalized not in re.sub(r'\s+', '', after):
                errors.append('Changed research statement in ' + old + ': ' + line[:100])
    if old == 'Untitled.md':
        research = before.split('References:', 1)[1]
        for line in research.splitlines():
            if not line.strip() or line.startswith(('**1.', '**2.', '**3.', '**4.', '💡')) or re.fullmatch(r'[-| :]+', line):
                continue
            if re.sub(r'\s+', '', line) not in re.sub(r'\s+', '', after):
                errors.append('Changed contract research statement: ' + line[:100])
        for phrase in ('20%', 'full refund', '14 days', '3–6 months', 'non-refundable'):
            if phrase not in after:
                errors.append('Missing proposed commercial term: ' + phrase)

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('PASS: {} original notes mapped; {} distinct source URL strings and {} code/prompt blocks preserved.'.format(len(originals), len(urls), blocks))
print('Original equity and contract research statements are retained. Commercial-term checks are partial; editorial meaning also needs review.')
