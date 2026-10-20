---
title: "Sources of Truth"
type: standard
status: active
updated: 2026-10-20
tags: ["vault"]
verification: not-applicable
---

# Sources of Truth

This document owns evidence and authority rules. It does not certify the imported notes.

## Vault authorities

| Concern | Canonical source |
| --- | --- |
| Agent workflow, permissions, and Git boundaries | [AGENTS.md](../AGENTS.md) |
| Folder placement and note ownership | [[Vault Structure]] |
| Formatting and metadata | [[Note Standards]] |
| Evidence labels and source precedence | This document |
| How to capture, review, and validate | [[Vault Maintenance]] |
| Navigation | [[Discoverable Home]] and topic indexes |
| Outstanding evidence gaps | [[Source Review Queue]] |
| Original-to-new locations | [[Migration Map]] |

Keep each rule in its owning document. Other documents link to it. If rules conflict, resolve the conflict explicitly instead of copying another version.

## Subject evidence

| Subject | Preferred evidence | Limits |
| --- | --- | --- |
| Rarticle client commitments | The signed agreement, accepted statement of work, and approved changes for that client | Generic workflow drafts cannot override an agreement. No signed agreement was supplied here. |
| Company policy | A dated decision approved by ZP | A generated suggestion or draft is not policy. |
| Software configuration | Installed version, vendor documentation for that version, and recorded test output | A saved command or green formatting check does not prove runtime behavior. |
| Financial research | Dated issuer filings, investor relations releases, and attributable market data | Opinions, forecasts, and social sentiment remain distinct from reported figures. |
| Malaysian legal or regulatory claims | Identified official legislation, regulator guidance, or qualified advice relevant to the question | Unresolved citation numbers are not evidence. |
| Tools and vendors | The linked official product documentation or repository | A bookmark records discovery, not suitability or endorsement. |
| Learning and methodology | The original paper, author, documentation, or source material | A summary must preserve uncertainty and avoid expanding the source's claim. |

## Recording a source

Record the title or organization, exact URL or internal record, the claim it supports, and any relevant publication date, version, or data date. Add an access date only when you actually open and inspect the source.

Keep citations near claims. When the source is unavailable or unknown, write that explicitly. Do not invent a source URL, research date, author, or quote.

## Resolving disagreement

Preserve both claims with their sources and dates. Check whether they describe the same period, definition, or version. Record the resolution or keep the issue in [[Source Review Queue]]. Do not average conflicting values or silently choose a convenient one.

## Existing imported material

The October 2026 organization pass checked files, formatting, and local links. It did not recheck product availability, stock data, legal claims, or the Coolify configuration against external sources.

Original source links and research dates remain with each note. The original client draft was split into [[Client Engagement Workflow]] and [[Contract Research]]. Their status remains draft.

## Related

- [[Note Standards]]
- [[Source Review Queue]]
- [[Discoverable Home]]
