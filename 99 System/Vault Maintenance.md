---
title: "Vault Maintenance"
type: standard
status: active
updated: 2026-10-20
tags: ["vault"]
verification: not-applicable
---

# Vault Maintenance

Use this workflow to keep the collection consistent. [[Note Standards]] defines the format and [[Sources of Truth]] defines evidence rules.

## Capture and organize

1. Copy a template into `00 Inbox` and give it a descriptive name.
2. Set the title, type, status, updated date, and tags.
3. Add the source and distinguish copied claims from your own notes.
4. Move it into the subject folder defined in [[Vault Structure]].
5. Link it from the topic index and add related notes when useful.

## Review a note

1. Read the canonical source for each consequential claim.
2. Record the source date or version and what was checked.
3. Keep unresolved claims marked unverified or split them into a draft.
4. Set `verification: reviewed` and `checked` only when the stated review is complete.
5. Keep dated research snapshots intact. Add a dated follow-up if new evidence changes the conclusion.

## Validate local structure

Run from the Discoverable repository root.

```bash
python3 scripts/check_vault.py
```

The checker validates metadata, headings, trailing whitespace, the final newline, fenced code, internal targets, and reachability from [[Discoverable Home]]. It does not fetch external URLs, check facts, execute saved commands, or inspect the parent My Notes vault.

For the initial organization pass, compare the preserved material with the original Git revision.

```bash
python3 scripts/check_migration.py
```

This migration check maps original notes through `origin`, compares source URLs and code blocks, and checks retained equity and contract research. It is tied to the original revision and is not a rule that future research must never change.

The frontmatter parser supports the subset in [[Note Standards]]. Use inline JSON arrays for tags and aliases. Avoid multiline YAML values and nested objects.

## Review Git scope

```bash
git status --short
git diff --stat
git diff --check
git diff --cached --name-status
```

Stage only named paths for the requested task. Review the staged diff before any requested commit. Do not use `git add .` or `git add -A` in this vault. Do not commit or push merely because a maintenance check passed.

`.gitignore` excludes new OS metadata, trash, local audit output, workspace state, plugin bundles, and environment files. Some of these files were already tracked before this work. Ignore rules do not remove tracked files from the index. Keep existing unrelated tracked files untouched unless a separate cleanup is requested.

The standalone vault's Git plugin configuration now has automatic commit, push, and pull intervals disabled and automatic commits limited to staged files. Manual Git actions remain available. The parent My Notes vault has its own independent configuration.

## Obsidian setup

When Discoverable is opened as its own vault, its local settings route new notes to `00 Inbox`, attachments to `99 System/Attachments`, and built-in templates to `99 System/Templates`.

When using Discoverable inside My Notes, select the corresponding parent-relative folders in that vault if desired. Do not copy settings blindly across the two vaults. Check that a note created from a template has the new title in its properties and H1.

## Archive

Move inactive material to `90 Archive`, set `status: archived`, and update its links. Keep substantive content and provenance. Delete a note only when its content is duplicated elsewhere or deletion was explicitly requested.

## Related

- [[Discoverable Home]]
- [[Note Standards]]
- [[Sources of Truth]]
