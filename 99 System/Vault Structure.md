---
title: "Vault Structure"
type: standard
status: active
updated: 2026-10-20
tags: ["vault"]
verification: not-applicable
---

# Vault Structure

This document owns folder placement. [[Note Standards]] owns note formatting. [[Sources of Truth]] owns evidence rules.

## Folder map

| Folder | Purpose | Entry point |
| --- | --- | --- |
| `00 Inbox` | Unsorted captures | [[Inbox]] |
| `10 Knowledge/AI` | AI concepts, learning, and specialist resources | [[AI Index]] |
| `10 Knowledge/Engineering` | Software and infrastructure knowledge | [[Engineering Index]] |
| `20 Resources` | General tool and resource collections | [[Resources Index]] |
| `30 Business` | Business operations, client work practices, and opportunities | [[Business Index]] |
| `40 Investing` | Dated financial research and research prompts | [[Investing Index]] |
| `90 Archive` | Inactive notes and empty placeholders | [[Archive Index]] |
| `99 System` | Vault rules, templates, and migration records | [[Discoverable Home]] |
| `scripts` | Read-only maintenance checks | [[Vault Maintenance]] |

## Placement rules

- Choose the subject first. Use `type` to distinguish research, resources, prompts, and other notes within that subject.
- Give each topic one canonical note. Link to it from other topics rather than copying its content.
- Add a subfolder only when it groups several related notes or separates a useful workflow, such as research prompts.
- Keep standalone notes out of the repository root. The root contains [[Discoverable Home]] and `AGENTS.md`.
- Use `90 Archive/Unstarted` for placeholders that contain no knowledge yet.
- Store future attachments in `99 System/Attachments`. Keep credentials and private client records outside this discovery repository.
- Never treat `.trash` as the archive. It is Obsidian's recovery area and is outside active-note maintenance.

## Naming and links

Use descriptive Title Case file names and globally unique note names within this repository. Preserve established product capitalization such as JavaScript, TypeScript, GitHub, and n8n.

Use `[[Note Title]]` for internal navigation. Add an alias when a rename would remove a useful former title. Do not rely on aliases to repair a broken link. Update links to the canonical title.

Number folders only to control the top-level browsing order. Number individual notes only when sequence matters, as with the investing prompts.

## Vault boundary

This repository is `Discoverable`. Obsidian was observed with the parent `My Notes` vault open. The parent vault's settings and other folders are outside this task's scope.

The relative paths in this document start at the repository root. The local `.obsidian` settings apply when `Discoverable` is opened as a standalone vault. If it remains inside `My Notes`, its parent settings control new-note and template behavior. Unique note titles keep navigation usable in either arrangement, subject to name collisions elsewhere in the parent vault.

## Related

- [[Discoverable Home]]
- [[Note Standards]]
