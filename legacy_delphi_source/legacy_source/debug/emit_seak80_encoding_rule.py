"""Rewrite .cursor/rules/seak80-frontend-encoding.mdc as UTF-8 (ASCII-only source)."""
from __future__ import annotations

import ast
from pathlib import Path

RULE = Path(__file__).resolve().parents[1] / ".cursor" / "rules" / "seak80-frontend-encoding.mdc"


def J(s: str) -> str:
    return ast.literal_eval('"' + s + '"')


def main() -> None:
    body = f"""---
description: {J(r'Seak80 sample \ud504\ub860\ud2b8\uc5d4\ub4dc \ud55c\uae00\u00b7\uc778\ucf54\ub529 \uaddc\uce59 (UTF-8 \uc800\uc7a5, JS \uc774\uc2a4\ucf00\uc774\ud504)')}
globs: web/seak80-sample/frontend/**/*
alwaysApply: false
---

# {J(r'Seak80 sample \ud504\ub860\ud2b8\uc5d4\ub4dc \uc778\ucf54\ub529 \uaddc\uce59')}

## {J(r'\ud575\uc2ec \uc6d0\uce59 (\uc544\ub798 \ud56d\ubaa9\uc740 \ubc18\ubcf5 \uac80\ud1a0)')}

1. **{J(r'\ub514\uc2a4\ud06c \uc800\uc7a5\uc740 UTF-8')}**  
   `<meta charset="UTF-8">`{J(r'\uc778\ub370 \ud30c\uc77c\uc774')} **EUC-KR(CP949)** {J(r'\ub85c \uc800\uc7a5\ub418\uba74 \ube0c\ub77c\uc6b0\uc800\ub294 UTF-8\ub85c \uc77d\uc5b4')} **{J(r'\uae68\uc9c4 \uae00\uc790')}**{J(r'\uac00 \ub41c\ub2e4.')} (`xxd`{J(r'\ub85c \ud55c\uae00 \ubc14\uc774\ud2b8\uac00')} `ea b8` {J(r'\uacc4\uc5f4\uc774 \uc544\ub2c8\ub77c')} `b0 ed` {J(r'\uc2dd\uc774\uba74 \uc758\uc2ec')})
2. **{J(r'UTF-8\ub85c \uc798\ubabb \uc7ac\uc778\ucf54\ub529\ub41c \ubcf8\ubb38')}**  
   {J(r'\ud55c\uae00\uc774')} **`?`(0x3f){J(r'\ub85c\ub9cc \ubcf4\uc774\ub294 \uacbd\uc6b0')}**{J(r'\ub294 \uc774\ubbf8')} **{J(r'\uc815\ubcf4 \uc190\uc2e4')}**{J(r'\uc774\ub77c \ucf54\ub4dc\ub85c \ubcf5\uad6c \ubd88\uac00.')} Git/{J(r'\uc5d0\ub514\ud130 \uc124\uc815\uc744 \ub9de\ucd94\uac70\ub098 UTF-8\ub85c')} **{J(r'\uc6d0\ubb38\uc744 \ub2e4\uc2dc \uc785\ub825')}**{J(r'\ud574\uc57c \ud55c\ub2e4.')}
3. **{J(r'\uc5d0\uc774\uc804\ud2b8 Write/apply_patch')}**  
   {J(r'\uc77c\ubd80 \ud658\uacbd\uc5d0\uc11c UTF-8 \ud55c\uae00 \ub9ac\ud130\ub7f4\uc774')} **{J(r'\ub2e4\ub978 \uc778\ucf54\ub529\uc73c\ub85c \uae68\uc838 \uc800\uc7a5')}**{J(r'\ub420 \uc218 \uc788\ub2e4.')} {J(r'\uc800\uc7a5 \ud6c4')} **`file -I` / UTF-8 decode**{J(r'\ub97c \ud544\uc218\ub85c \ud55c\ub2e4.')}
3b. **{J(r'\ud55c\uae00 HTML\uc774 \ub514\uc2a4\ud06c\uc5d0\uc11c CP949\ub85c\ub9cc \ub0a8\ub294 \uacbd\uc6b0')}**  
   {J(r'\uc18c\uc2a4\uc5d0 \ud55c\uae00 \ub9ac\ud130\ub7f4 \uc5c6\uc774 \uc720\uc9c0\ud558\uba70 UTF-8\ub85c \ub2e4\uc2dc \uc4f0\ub824\uba74')} `python3 debug/emit_frontend_html_utf8.py` {J(r'\ub97c \uc0ac\uc6a9 (\uae30\ucd08\uad00\ub9ac\u00b7\u0031\ub2e8\uacc4 POC \uad00\ub828 HTML).')}

## {J(r'\uc2e4\ubb34 (\uc800\uc7a5\u00b7\uac80\uc99d \uc2dc \ud544\uc218)')}

1. **`web/seak80-sample/frontend`{J(r'\uc758')} `*.html`, `*.js`, `*.css`**{J(r'\ub294')} **UTF-8({J(r'\ubb34 BOM \uad8c\uc7a5')})**{J(r'\ub85c\ub9cc \uc800\uc7a5\ud55c\ub2e4.')}  
   - {J(r'\ub8e8\ud2b8')} `.editorconfig`{J(r'\uc5d0')} `charset = utf-8`, `eol = lf`{J(r'\uac00 \uc788\ub2e4.')}
2. **{J(r'\uc800\uc7a5 \uac80\uc99d')}** ({J(r'\uc790\ub3d9\ud654 \ub610\ub294 \uc218\ub3d9')}):  
   - `python3 -c "p=open('...','rb').read(); ..."` {J(r'\ub4f1\uc73c\ub85c UTF-8 \ud55c\uae00 \uc2dc\uadf8\ub2c8\ucc98 \ud655\uc778, \ub610\ub294')}  
   - {J(r'\uc5d0\ub514\ud130\uac00 UTF-8\uc774\uba74')} `python3`{J(r'\uc758')} `write_text(..., encoding='utf-8', newline='\\n')`{J(r'\ub85c')} **{J(r'\uc0c8 \ud30c\uc77c \uc0dd\uc131')}**{J(r'\uc744 \uc120\ud638\ud55c\ub2e4.')}
3. **{J(r'UI \ubb38\uc790\uc5f4\uc774 \uc788\ub294')} `*.js` ({J(r'\uba54\uc2dc\uc9c0\u00b7\ub77c\ubca8')})**  
   {J(r'\ud55c\uae00\uc740')} **ASCII{J(r'\ub9cc \uc4f0\uace0')} `\\\\uXXXX` {J(r'\uc774\uc2a4\ucf00\uc774\ud504')}**{J(r'\ub85c \ub454\ub2e4.')} (`seek20.js` {J(r'\ud328\ud134')}, `sobo12.js`/`sobo13.js` {J(r'\uc0c1\ud0dc \uba54\uc2dc\uc9c0')})  
   - {J(r'\ub7f0\ud0c0\uc784\uc5d0\ub294 \ube0c\ub77c\uc6b0\uc800\uac00 \uc815\uc0c1 \ub514\ucf54\ub529\ub418\uc5b4 \ud55c\uae00\ub85c \ud45c\uc2dc\ub41c\ub2e4.')}
4. **`*.html`{J(r'\uc5d0 \uc9c1\uc811 \uc4f4 \ud55c\uae00')}**  
   - UTF-8{J(r'\ub85c \uc800\uc7a5\ud558\uace0, \ucee4\ubc0b \uc804')} **`file -I` / `xxd`{J(r'\ub85c UTF-8\uc784\uc744 \ud655\uc778')}**{J(r'\ud55c\ub2e4.')}  
   - {J(r'\uae68\uc9c4 \ud30c\uc77c\uc744 \ubc1c\uacac\ud558\uba74 \uc5d0\ub514\ud130\ub97c UTF-8\ub85c \ub9de\ucd98 \ud6c4')} `python3` {J(r'\uc2a4\ud06c\ub9bd\ud2b8\ub85c HTML\uc744 \uc7ac\uc0dd\uc131\ud55c\ub2e4.')}

## {J(r'\ud53c\ud560 \uac83')}

- CP949/EUC-KR{J(r'\ub85c \uc800\uc7a5\ud55c \ucc44')} `charset="UTF-8"`{J(r'\ub9cc \ubd99\uc774\uae30.')}
- {J(r'\uae68\uc9c4 \ubb38\uc790\uc5f4\uc744 \uadf8\ub300\ub85c \ub450\uace0 \ub2e4\ub978 \ud654\uba74\ub9cc \uc218\uc815\ud558\uae30 (\ub3d9\uc77c \uc6d0\uc778 \uc7ac\ubc1c).')}
"""
    RULE.parent.mkdir(parents=True, exist_ok=True)
    RULE.write_text(body, encoding="utf-8", newline="\n")
    RULE.read_bytes().decode("utf-8")
    print("wrote", RULE)


if __name__ == "__main__":
    main()
