from __future__ import annotations

from pathlib import Path


CANDIDATE_ENCODINGS = [
    'utf-8-sig',
    'utf-16',
    'cp949',
    'euc-kr',
    'latin1',
]


def read_delphi_text(path: str | Path) -> tuple[str, str]:
    data = Path(path).read_bytes()
    for enc in CANDIDATE_ENCODINGS:
        try:
            text = data.decode(enc)
            if 'object ' in text or 'unit ' in text or 'procedure ' in text:
                return text, enc
        except UnicodeDecodeError:
            continue
    return data.decode('latin1', errors='replace'), 'latin1'
