"""
레거시 델파이 소스 텍스트 인코딩.

한국 Windows 기본 ANSI(CP949)로 저장된 .pas/.dfm/.dpr 과 UTF-8(델파이 2009+ 등)이 혼재할 수 있어,
UTF-8(BOM 포함) 우선 후 CP949 등으로 폴백한다.
"""

from pathlib import Path


def read_delphi_source(filepath: str) -> str:
    """소스 파일을 텍스트로 읽는다. UTF-8 → CP949 → EUC-KR → UTF-8 replace."""
    raw = Path(filepath).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8-sig")
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")
