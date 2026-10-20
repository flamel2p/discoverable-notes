#!/usr/bin/env python3
"""Check the vault's documented Markdown subset without changing any files.

Frontmatter accepts one key per line, JSON-quoted or bare scalar values, and
inline JSON string lists. Markdown checks cover ATX headings, fenced code,
wikilinks, inline links/images, and explicit reference links. HTML, setext
headings, indented code, and shortcut reference links are outside this subset.
External URLs and the factual accuracy of source material are not validated.
"""

import argparse
import datetime
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set
from urllib.parse import unquote, urlsplit


FOLDERS = {
    "00 Inbox", "10 Knowledge", "20 Resources", "30 Business",
    "40 Investing", "90 Archive", "99 System",
}
TYPES = {"note", "resource", "research", "prompt", "index", "standard", "template"}
STATUSES = {"draft", "active", "archived"}
VERIFICATIONS = {"unverified", "reviewed", "not-applicable"}
REQUIRED = {"title", "type", "status", "updated", "tags", "verification"}


def normalized(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def heading_text(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    return re.sub(r"[*_`~]", "", value).strip()


def slug(value: str) -> str:
    value = normalized(heading_text(value))
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", value))


@dataclass
class Link:
    target: str
    line: int
    wiki: bool = False


@dataclass
class Note:
    path: Path
    relative: str
    metadata: Dict[str, object] = field(default_factory=dict)
    headings: Set[str] = field(default_factory=set)
    blocks: Set[str] = field(default_factory=set)
    links: List[Link] = field(default_factory=list)
    edges: Set[Path] = field(default_factory=set)


class Checker:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.notes: Dict[Path, Note] = {}
        self.stems: Dict[str, List[Note]] = {}
        self.errors: List[str] = []
        self.link_count = 0

    def error(self, note: Note, line: int, message: str) -> None:
        self.errors.append("{}:{}: {}".format(note.relative, line, message))

    def discover(self) -> None:
        for path in sorted(self.root.rglob("*.md")):
            parts = path.relative_to(self.root).parts
            if any(part.startswith(".") for part in parts):
                continue
            if path.name.casefold() in {"agents.md", "readme.md"}:
                continue
            if "scripts" in parts[:-1]:
                continue
            note = Note(path.resolve(), path.relative_to(self.root).as_posix())
            if len(parts) > 1 and parts[0] not in FOLDERS:
                self.error(note, 1, "note is outside the folders defined in Vault Structure")
            if len(parts) == 1 and path.stem != "Discoverable Home":
                self.error(note, 1, "move this root note into its subject folder")
            self.notes[note.path] = note
            self.stems.setdefault(normalized(path.stem), []).append(note)
        for notes in self.stems.values():
            if len(notes) > 1:
                for note in notes:
                    self.error(note, 1, "duplicate note stem: {}".format(
                        ", ".join(other.relative for other in notes if other is not note)))

    def frontmatter(self, note: Note, lines: List[str]) -> int:
        if not lines or lines[0] != "---":
            self.error(note, 1, "missing opening frontmatter delimiter ---")
            return 0
        try:
            end = lines.index("---", 1)
        except ValueError:
            self.error(note, 1, "missing closing frontmatter delimiter ---")
            return 1
        locations = {}
        for number in range(1, end):
            line = lines[number]
            if not line:
                continue
            match = re.fullmatch(r"([a-z][a-z0-9_]*): (.+)", line)
            if not match:
                self.error(note, number + 1, "use one frontmatter key: value per line")
                continue
            key, raw = match.groups()
            if key in locations:
                self.error(note, number + 1, "duplicate frontmatter key {}".format(key))
                continue
            locations[key] = number + 1
            if raw.startswith(('"', '[')):
                try:
                    value = json.loads(raw)
                except json.JSONDecodeError:
                    self.error(note, number + 1, "invalid JSON value for {}".format(key))
                    continue
                if not isinstance(value, (str, list)) or (
                    isinstance(value, list) and any(not isinstance(item, str) for item in value)
                ):
                    self.error(note, number + 1, "{} must be a scalar or JSON string list".format(key))
                    continue
            elif raw[0] in "'{}>|&*!#%@`" or ": " in raw or " #" in raw:
                self.error(note, number + 1, "quote {} as JSON to avoid unsupported YAML syntax".format(key))
                continue
            else:
                value = raw
            note.metadata[key] = value
        for key in sorted(REQUIRED - note.metadata.keys()):
            self.error(note, 1, "missing required frontmatter key {}".format(key))
        title = note.metadata.get("title")
        if title is not None and (
            not isinstance(title, str) or unicodedata.normalize("NFC", title) !=
            unicodedata.normalize("NFC", note.path.stem)
        ):
            self.error(note, locations.get("title", 1), "title must match the filename stem")
        for key, choices in (("type", TYPES), ("status", STATUSES), ("verification", VERIFICATIONS)):
            if key in note.metadata and (
                not isinstance(note.metadata[key], str) or note.metadata[key] not in choices
            ):
                self.error(note, locations[key], "{} must be one of {}".format(key, ", ".join(sorted(choices))))
        for key in ("tags", "aliases"):
            if key in note.metadata:
                value = note.metadata[key]
                if not isinstance(value, list) or (key == "tags" and not value) or any(
                    not isinstance(item, str) or not item.strip() for item in value
                ):
                    self.error(note, locations[key], "{} must be an inline JSON list of nonempty strings".format(key))
        for key in ("updated", "as_of", "checked"):
            if key not in note.metadata:
                continue
            value = note.metadata[key]
            try:
                if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError()
                datetime.date.fromisoformat(value)
            except ValueError:
                self.error(note, locations[key], "{} must be a valid YYYY-MM-DD date".format(key))
        if note.metadata.get("verification") == "reviewed" and "checked" not in note.metadata:
            self.error(note, 1, "reviewed notes require a checked YYYY-MM-DD date")
        return end + 1

    def read(self, note: Note) -> None:
        data = note.path.read_bytes()
        text = data.decode("utf-8")
        if b"\r" in data:
            self.error(note, 1, "use LF line endings")
        if not data.endswith(b"\n"):
            self.error(note, max(1, len(text.splitlines())), "missing final newline")
        lines = text.splitlines()
        for number, line in enumerate(lines, 1):
            if line.rstrip(" \t") != line:
                self.error(note, number, "trailing whitespace")
        start = self.frontmatter(note, lines)
        fence = None
        fence_line = 0
        previous_level = 0
        h1s = []
        body = []
        slug_counts: Dict[str, int] = {}
        for number in range(start, len(lines)):
            line = lines[number]
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if fence:
                if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                    fence = None
                body.append("")
                continue
            if marker:
                fence, fence_line = marker[1], number + 1
                if not marker[2].strip():
                    self.error(note, number + 1, "opening code fence requires a language marker")
                body.append("")
                continue
            heading = re.match(r"^ {0,3}(#{1,6})\s+(.+?)\s*$", line)
            if heading:
                level = len(heading[1])
                title = re.sub(r"\s+#+\s*$", "", heading[2])
                if level > previous_level + 1:
                    self.error(note, number + 1, "heading skips a level")
                previous_level = level
                if level == 1:
                    h1s.append((number + 1, title))
                note.headings.add(normalized(heading_text(title)))
                heading_slug = slug(title)
                count = slug_counts.get(heading_slug, 0)
                note.headings.add(heading_slug if not count else "{}-{}".format(heading_slug, count))
                slug_counts[heading_slug] = count + 1
            if re.fullmatch(r"\s*(?:[-+*]|\d+[.)])(?:\s+\[[ xX]\])?\s*", line):
                self.error(note, number + 1, "empty list item")
            note.blocks.update(re.findall(r"(?:^|\s)\^([A-Za-z0-9-]+)\s*$", line))
            body.append(line)
        if fence:
            self.error(note, fence_line, "unmatched code fence")
        if len(h1s) != 1:
            self.error(note, start + 1, "expected exactly one H1; found {}".format(len(h1s)))
        elif unicodedata.normalize("NFC", h1s[0][1]) != unicodedata.normalize("NFC", str(note.metadata.get("title", ""))):
            self.error(note, h1s[0][0], "H1 must match title")
        visible = "\n".join(body)
        visible = re.sub(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)", lambda match: re.sub(r"[^\n]", " ", match[0]), visible, flags=re.S)
        self.extract_links(note, visible, start + 1)

    def extract_links(self, note: Note, text: str, first_line: int) -> None:
        references = {}
        for match in re.finditer(r"(?m)^ {0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)(?:\s+.*)?$", text):
            references[normalized(match[1])] = match[2].strip("<>")
        patterns = (
            (r"!?\[\[([^\]\n]+)\]\]", "wiki"),
            (r"!?\[([^\]\n]*)\]\((<[^>\n]+>|(?:[^()\n]|\([^()\n]*\))*)\)", "inline"),
            (r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]", "reference"),
        )
        for pattern, kind in patterns:
            for match in re.finditer(pattern, text):
                if match.start() and text[match.start() - 1] == "\\":
                    continue
                number = first_line + text.count("\n", 0, match.start())
                if kind == "wiki":
                    target = match[1].split("|", 1)[0].strip()
                elif kind == "reference":
                    label = normalized(match[2] or match[1])
                    if label not in references:
                        self.error(note, number, "missing Markdown reference definition [{}]".format(label))
                        continue
                    target = references[label]
                else:
                    target = match[2].strip()
                    target = re.sub(r'''\s+["'].*["']$''', "", target)
                    if target.startswith("<") and target.endswith(">"):
                        target = target[1:-1]
                note.links.append(Link(target, number, kind == "wiki"))

    def resolve(self, note: Note, link: Link) -> None:
        if not link.wiki:
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", link.target) or link.target.startswith("//"):
                return
            parsed = urlsplit(link.target)
            if parsed.scheme or parsed.netloc:
                return
            target, fragment = unquote(parsed.path), unquote(parsed.fragment)
        else:
            target, _, fragment = unquote(link.target).partition("#")
        self.link_count += 1
        destination = None
        if not target:
            destination = note.path
        elif link.wiki:
            target = target.removesuffix(".md").replace("\\", "/")
            target_key = normalized(target)
            if "/" not in target:
                candidates = self.stems.get(target_key, [])
            else:
                candidates = [other for other in self.notes.values() if
                              normalized(other.relative.removesuffix(".md")) == target_key or
                              normalized(other.relative.removesuffix(".md")).endswith("/" + target_key)]
            if len(candidates) == 1:
                destination = candidates[0].path
            elif len(candidates) > 1:
                self.error(note, link.line, "ambiguous internal target [[{}]]".format(target))
                return
            else:
                attachment = (self.root / target).resolve()
                if attachment.is_file() and attachment not in self.notes:
                    destination = attachment
        else:
            destination = (note.path.parent / target).resolve()
            if not destination.is_file() and not destination.suffix:
                destination = destination.with_suffix(".md")
        if destination is None or not destination.is_file():
            self.error(note, link.line, "missing internal target {}".format(link.target))
            return
        try:
            destination.relative_to(self.root)
        except ValueError:
            self.error(note, link.line, "internal target leaves the vault: {}".format(link.target))
            return
        if destination in self.notes:
            note.edges.add(destination)
            other = self.notes[destination]
            if fragment.startswith("^"):
                exists = fragment[1:] in other.blocks
            else:
                exists = not fragment or normalized(fragment) in other.headings or slug(fragment) in other.headings
            if not exists:
                self.error(note, link.line, "missing fragment #{} in {}".format(fragment, other.relative))

    def run(self) -> int:
        if not self.root.is_dir():
            raise ValueError("vault root is not a directory: {}".format(self.root))
        self.discover()
        for note in self.notes.values():
            try:
                self.read(note)
            except (OSError, UnicodeError) as error:
                self.error(note, 1, "cannot read UTF-8 Markdown: {}".format(error))
        for note in self.notes.values():
            for link in note.links:
                self.resolve(note, link)
        homes = self.stems.get(normalized("Discoverable Home"), [])
        reachable: Set[Path] = set()
        if len(homes) != 1:
            self.errors.append("Discoverable Home.md:1: expected one Discoverable Home entry note")
        else:
            pending = [homes[0].path]
            while pending:
                path = pending.pop()
                if path in reachable:
                    continue
                reachable.add(path)
                pending.extend(self.notes[path].edges - reachable)
            for note in self.notes.values():
                if note.path not in reachable and note.metadata.get("type") != "template":
                    self.error(note, 1, "unreachable from Discoverable Home")
        for error in self.errors:
            print(error)
        print("{}: {} notes, {} internal links, {} reachable notes, {} issues".format(
            "ISSUES" if self.errors else "PASS", len(self.notes), self.link_count,
            len(reachable), len(self.errors)))
        print("Scope: local formatting, metadata, links and navigation; no web or factual validation.")
        return 1 if self.errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("vault_root", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    try:
        return Checker(args.vault_root).run()
    except (OSError, UnicodeError, ValueError) as error:
        print("ISSUES: {}".format(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
