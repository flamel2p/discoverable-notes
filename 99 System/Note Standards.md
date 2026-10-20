---
title: "Note Standards"
type: standard
status: active
updated: 2026-10-20
tags: ["vault"]
verification: not-applicable
---

# Note Standards

This document owns the note format. Apply it to every active Markdown note, including indexes, system documents, templates, and archived notes. `AGENTS.md` is an agent instruction file and does not need note metadata. Hidden folders and `scripts` are outside the note schema.

## Required properties

Place YAML properties at the start of the file. Use one property per line. The checker supports plain or JSON-quoted scalars and inline JSON arrays. Use this subset so checks need no extra packages.

```yaml
title: "Example Note"
type: note
status: draft
updated: 2026-10-20
tags: ["engineering"]
verification: unverified
```

| Property | Rule |
| --- | --- |
| `title` | Exactly the filename without `.md`. Quote it with JSON-compatible double quotes. |
| `type` | `note`, `resource`, `research`, `prompt`, `index`, `standard`, or `template`. |
| `status` | `draft`, `active`, or `archived`. Active means maintained, not fact-checked. |
| `updated` | Date of the last meaningful edit in `YYYY-MM-DD`. A formatting migration counts as an edit. |
| `tags` | Nonempty inline JSON array of short topic strings. Avoid copying the whole folder path into tags. |
| `verification` | `unverified`, `reviewed`, or `not-applicable`. Use unverified for imported claims. |
| `checked` | Required only when verification is reviewed. Record the actual review date. |
| `as_of` | Optional date for time-sensitive source material, separate from updated. |
| `origin` | Optional original path or provenance label, quoted as a string. |
| `aliases` | Optional inline JSON array of former names. |

Do not invent creation dates. Do not mark a note reviewed because it was formatted, moved, or generated. A source review must state its scope and unresolved gaps in the body. Use not-applicable only when there are no factual claims to verify, such as an index or a prompt template.

## Body structure

Start the body with one H1 that exactly matches `title`. Follow it with one short paragraph that states the note's purpose. Use sentence case for H2 and H3 headings, preserving proper names. Do not skip heading levels.

Use sections that serve the content. A resource list can consist of Resources and Related. A research note usually needs findings, assumptions, source references, and unresolved questions. Do not fill empty sections with invented information.

Keep exactly one blank line between blocks. End the file with a newline. Remove trailing spaces and empty list items. Use `-` for unordered lists and numbers for ordered steps. Keep nested list indentation consistent within the note.

## Links and sources

- Use descriptive Markdown links for external URLs.
- Keep citations beside the claim they support. Resource entries are themselves source links and do not need a second duplicate Sources section.
- Preserve URL query parameters unless you have confirmed they are only tracking parameters.
- Use Obsidian wikilinks for related notes. Link every note from its topic index or another reachable note.
- Keep source titles, quoted text, code, and original research intact during formatting. Existing quotations and saved prompt blocks are exempt from prose style changes.
- Keep exact code indentation. Add a language to each fenced code block, using `text` for prompts or plain text.
- Keep a single canonical resource entry per URL within a note when duplicates add no meaning. Preserve descriptions, category context, and favorite markers as text.

## Evidence labels

Use the following labels when the distinction affects a decision.

- Fact. Cite the supporting record and state the date or version when relevant.
- Inference. State the source facts and the reasoning.
- Recommendation. State the suggested action and tradeoff.
- Proposal. State who still needs to approve it.
- Unverified. State what has not been checked or which source is missing.

A note-level warning is enough for imported research whose individual claims have not been rechecked. Do not relabel all imported statements as verified facts.

## Templates and checks

Copy [[Note Template]], [[Resource Template]], or [[Research Template]]. Rename the file and update both its title property and H1. Set the appropriate type, status, date, and verification state before adding content.

Run the read-only checker described in [[Vault Maintenance]]. Passing it confirms structural rules and link resolution. It does not establish factual accuracy or external URL availability.

## Related

- [[Sources of Truth]]
- [[Vault Maintenance]]
- [[Discoverable Home]]
