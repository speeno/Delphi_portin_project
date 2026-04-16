from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .encodings import read_delphi_text


EVENT_PROC_RE = re.compile(r'procedure\s+(?:T\w+)\.(\w+)\s*\((.*?)\)\s*;', re.IGNORECASE | re.DOTALL)
ASSIGNMENT_RE = re.compile(r'(\w+)\.(Caption|Visible|Enabled|Text|Hint|Value)\s*:=\s*(.+?);', re.IGNORECASE)
RESOURCESTR_RE = re.compile(r'resourcestring\s+(.*?)(?=\n\s*(?:const|type|var|procedure|function|implementation|begin)\b)', re.IGNORECASE | re.DOTALL)
RESOURCE_ITEM_RE = re.compile(r'(\w+)\s*=\s*(.+?);')
RUNSQL_RE = re.compile(r'RunSQL\((.+?)\);', re.IGNORECASE | re.DOTALL)
SHOWMSG_RE = re.compile(r'ShowMessage\((.+?)\);', re.IGNORECASE | re.DOTALL)


def analyze_pas(path: str | Path) -> dict[str, Any]:
    text, encoding = read_delphi_text(path)
    handlers = [{'name': name, 'signature': sig.strip()} for name, sig in EVENT_PROC_RE.findall(text)]
    assignments = [
        {'component': comp, 'property': prop, 'expression': expr.strip()}
        for comp, prop, expr in ASSIGNMENT_RE.findall(text)
    ]
    resourcestrings: dict[str, str] = {}
    match = RESOURCESTR_RE.search(text)
    if match:
        block = match.group(1)
        for name, raw in RESOURCE_ITEM_RE.findall(block):
            resourcestrings[name] = raw.strip().strip("'")
    sql_calls = [sql.strip() for sql in RUNSQL_RE.findall(text)]
    messages = [msg.strip() for msg in SHOWMSG_RE.findall(text)]
    return {
        'encoding': encoding,
        'event_handlers': handlers,
        'runtime_assignments': assignments,
        'resourcestrings': resourcestrings,
        'sql_calls': sql_calls,
        'messages': messages,
    }


def dump_pas_analysis(data: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
