from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .encodings import read_delphi_text
from .models import DfmNode
from .values import parse_scalar


OBJECT_RE = re.compile(r'^(object|inherited|inline)\s+(\w+)\s*:\s*([\w\.]+)')
PROP_RE = re.compile(r'^([\w\.]+)\s*=\s*(.*)$')


class DfmParser:
    def parse_file(self, path: str | Path) -> DfmNode:
        text, _ = read_delphi_text(path)
        return self.parse(text)

    def parse(self, text: str) -> DfmNode:
        lines = text.splitlines()
        stack: list[DfmNode] = []
        root: DfmNode | None = None
        i = 0

        while i < len(lines):
            stripped = lines[i].strip()
            i += 1

            if not stripped:
                continue

            match = OBJECT_RE.match(stripped)
            if match:
                kind, name, class_name = match.groups()
                node = DfmNode(kind=kind, name=name, class_name=class_name)
                if stack:
                    stack[-1].add_child(node)
                else:
                    root = node
                stack.append(node)
                continue

            if stripped == 'end':
                if stack:
                    stack.pop()
                continue

            if not stack:
                continue

            prop_match = PROP_RE.match(stripped)
            if not prop_match:
                continue

            key, raw = prop_match.groups()
            raw = raw.strip()

            if raw == '<':
                value, i = self._parse_angle_block(lines, i)
            elif raw == '(':
                value, i = self._parse_paren_block(lines, i)
            elif raw == '{':
                value, i = self._parse_brace_block(lines, i)
            elif raw.startswith('<') and not raw.endswith('>'):
                value, i = self._parse_inline_angle_block(raw, lines, i)
            elif raw.startswith('(') and not raw.endswith(')'):
                value, i = self._parse_inline_paren_block(raw, lines, i)
            elif raw.startswith('{') and not raw.endswith('}'):
                value, i = self._parse_inline_brace_block(raw, lines, i)
            else:
                value = parse_scalar(raw)

            stack[-1].props[key] = value

        if root is None:
            raise ValueError('No DFM root object found')
        return root

    def _parse_paren_block(self, lines: list[str], i: int) -> tuple[list[Any], int]:
        values: list[Any] = []
        while i < len(lines):
            stripped = lines[i].strip()
            i += 1
            if stripped == ')':
                break
            if stripped:
                values.append(parse_scalar(stripped))
        return values, i

    def _parse_angle_block(self, lines: list[str], i: int) -> tuple[list[Any], int]:
        items: list[Any] = []
        current: dict[str, Any] | None = None
        while i < len(lines):
            stripped = lines[i].strip()
            i += 1
            if stripped in {'>', 'end>', 'end >'}:
                if stripped.startswith('end') and current is not None:
                    items.append(current)
                    current = None
                if current is not None:
                    items.append(current)
                break
            if stripped == 'item':
                if current is not None:
                    items.append(current)
                current = {}
                continue
            if stripped == 'end':
                if current is not None:
                    items.append(current)
                    current = None
                continue
            prop_match = PROP_RE.match(stripped)
            if prop_match and current is not None:
                key, raw = prop_match.groups()
                current[key] = parse_scalar(raw.strip())
        return items, i

    def _parse_brace_block(self, lines: list[str], i: int) -> tuple[str, int]:
        parts: list[str] = []
        while i < len(lines):
            stripped = lines[i].strip()
            i += 1
            if stripped.endswith('}'):
                parts.append(stripped[:-1])
                break
            parts.append(stripped)
        return ''.join(parts), i

    def _parse_inline_angle_block(self, raw: str, lines: list[str], i: int) -> tuple[list[Any], int]:
        merged = [raw]
        while i < len(lines):
            merged.append(lines[i].strip())
            if lines[i].strip().endswith('>'):
                i += 1
                break
            i += 1
        temp = merged[:]
        temp[0] = '<'
        return self._parse_angle_block(temp, 1)

    def _parse_inline_paren_block(self, raw: str, lines: list[str], i: int) -> tuple[list[Any], int]:
        merged = [raw]
        while i < len(lines):
            merged.append(lines[i].strip())
            if lines[i].strip().endswith(')'):
                i += 1
                break
            i += 1
        values: list[Any] = []
        for line in merged:
            clean = line.strip().strip('()')
            if clean:
                values.append(parse_scalar(clean))
        return values, i

    def _parse_inline_brace_block(self, raw: str, lines: list[str], i: int) -> tuple[str, int]:
        merged = [raw]
        while i < len(lines):
            merged.append(lines[i].strip())
            if lines[i].strip().endswith('}'):
                i += 1
                break
            i += 1
        return ''.join(x.strip('{}') for x in merged), i


def dump_tree_json(node: DfmNode, path: str | Path) -> None:
    Path(path).write_text(json.dumps(node.to_dict(), ensure_ascii=False, indent=2), encoding='utf-8')
