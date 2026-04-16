"""
레거시 델파이 소스 텍스트 인코딩.

한국 Windows 기본 ANSI(CP949)로 저장된 .pas/.dfm/.dpr 과 UTF-8(델파이 2009+ 등)이 혼재할 수 있어,
UTF-8(BOM 포함) 우선 후 CP949 등으로 폴백한다.
"""

from pathlib import Path


def decode_delphi_raw_bytes(raw: bytes) -> tuple[str, str]:
    """
    바이트를 텍스트로 디코드한다(read_delphi_source 와 동일 순서).
    반환: (텍스트, 추정 인코딩 라벨).
    """
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8-sig"), "utf-8-bom"
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8-replace"


def utf8_body_bytes(raw: bytes) -> bytes:
    """UTF-8 본문 비교용(BOM 제거)."""
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:]
    return raw


def classify_delphi_source_bytes(raw: bytes) -> dict:
    """
    UTF-8 재저장 필요 여부(read_delphi_source 디코드 후 UTF-8 바이트와 본문 비교).

    - action: skip | convert
    - inferred_encoding: decode_delphi_raw_bytes 의 라벨
    - has_bom: 원본이 UTF-8 BOM 으로 시작하는지
    """
    text, inferred = decode_delphi_raw_bytes(raw)
    body = utf8_body_bytes(raw)
    out_utf8 = text.encode("utf-8")
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    if out_utf8 == body:
        return {"action": "skip", "inferred_encoding": inferred, "has_bom": has_bom}
    return {"action": "convert", "inferred_encoding": inferred, "has_bom": has_bom}


def read_delphi_source(filepath: str) -> str:
    """소스 파일을 텍스트로 읽는다. UTF-8 → CP949 → EUC-KR → UTF-8 replace."""
    raw = Path(filepath).read_bytes()
    return decode_delphi_raw_bytes(raw)[0]
