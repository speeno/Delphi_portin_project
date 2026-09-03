#!/usr/bin/env python3
"""계정 메일 템플릿(ACM-DEC-09) 전 변형 미리보기 HTML 생성 → Chrome 헤드리스로 PDF 변환.

    python3 tools/render_account_email_preview.py /tmp/preview.html
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \\
      --no-pdf-header-footer --print-to-pdf=out.pdf file:///tmp/preview.html

(로컬 macOS 는 WeasyPrint 시스템 라이브러리(libgobject)가 없어 Chrome 경로를 쓴다.)


- 원본: app/services/email_templates/account_code.py::render_code_email
- 변형: switch(신규 전환) / link(기존 계정 연결) / relink(재연결) / reset(비밀번호 재설정)
- 인증코드는 예시값(실제 발송 코드 아님). 비밀·자격증명 0건.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
BACKEND = Path("/Users/speeno/Delphi_porting/도서물류관리프로그램/backend")
sys.path.insert(0, str(BACKEND))

from app.services.email_templates import account_code as tpl  # noqa: E402

BASE = "https://books-logistics-web.vercel.app"
VARIANTS = [
    ("switch", "계정 전환 — 신규 이메일 계정", "교문사", "123456"),
    ("link", "기존 북이오웍스 계정에 회사 추가 연결", "위러브1", "204815"),
    ("relink", "레거시 아이디 변경 후 재연결", "한국도서유통", "770132"),
    ("reset", "비밀번호 재설정", "", "648290"),
]

sections = []
for purpose, caption, company, code in VARIANTS:
    path = "/account/switch" if purpose != "reset" else "/account/reset"
    link = tpl.deep_link(BASE, path=path, ticket="<ticket>", email="name@company.com", code=code)
    subject, html, text = tpl.render_code_email(
        code=code, purpose=purpose, minutes=10, link_url=link, company_label=company
    )
    body = html.split("<body", 1)[1].split(">", 1)[1].rsplit("</body>", 1)[0]
    sections.append(
        f"""
<section class="variant">
  <header class="meta">
    <p class="tag">{purpose}</p>
    <h2>{caption}</h2>
    <dl>
      <div><dt>제목</dt><dd>{subject}</dd></div>
      <div><dt>발신</dt><dd>북이오웍스 &lt;admin@bukio.works&gt; · Brevo SMTP</dd></div>
      <div><dt>수신 예시</dt><dd>name@company.com</dd></div>
    </dl>
  </header>
  <div class="render">{body}</div>
  <details class="plain" open><summary>평문(HTML 미지원 메일 클라이언트)</summary><pre>{text}</pre></details>
</section>
"""
    )

page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>북이오웍스 계정 메일 템플릿 미리보기</title>
<style>
  @page {{ size: A4; margin: 14mm 12mm; }}
  body {{ font-family: 'Pretendard Variable', Pretendard, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif;
         color: #282828; font-size: 11px; line-height: 1.6; }}
  h1 {{ font-size: 20px; margin: 0 0 4px; }}
  .lede {{ color: #555; margin: 0 0 4px; }}
  .src {{ color: #777; font-size: 10px; margin: 0 0 16px; font-family: Menlo, monospace; }}
  .variant {{ break-inside: avoid; page-break-inside: avoid; margin-bottom: 18px;
              border: 1px solid #E6E6E6; border-radius: 8px; overflow: hidden; }}
  .meta {{ background: #FCFFE9; padding: 10px 14px; border-bottom: 1px solid #E6E6E6; }}
  .tag {{ font-family: Menlo, monospace; font-size: 10px; color: #555; margin: 0 0 2px;
          text-transform: uppercase; letter-spacing: .08em; }}
  .meta h2 {{ font-size: 14px; margin: 0 0 6px; }}
  .meta dl {{ margin: 0; display: grid; gap: 2px; }}
  .meta dl div {{ display: flex; gap: 8px; }}
  .meta dt {{ color: #777; min-width: 52px; font-size: 10px; }}
  .meta dd {{ margin: 0; font-size: 10px; }}
  .render {{ padding: 0; background: #F5F5F7; }}
  .render > div {{ max-width: none !important; padding: 14px 10px !important; }}
  .plain {{ padding: 8px 14px 12px; border-top: 1px solid #E6E6E6; }}
  .plain summary {{ font-size: 10px; color: #555; cursor: default; }}
  .plain pre {{ white-space: pre-wrap; font-family: Menlo, monospace; font-size: 9.5px;
                background: #F5F5F5; padding: 8px; border-radius: 4px; margin: 6px 0 0; }}
  footer {{ margin-top: 10px; color: #777; font-size: 9.5px; border-top: 1px solid #E6E6E6; padding-top: 6px; }}
</style></head><body>
<h1>북이오웍스 계정 메일 템플릿 미리보기</h1>
<p class="lede">계정 전환·비밀번호 재설정 인증코드 메일 4개 변형 (2026-09-03 기준 구현본)</p>
<p class="src">app/services/email_templates/account_code.py::render_code_email · 발신 admin@bukio.works · Brevo SMTP(smtp-relay.brevo.com:587)</p>
{''.join(sections)}
<footer>인증코드는 예시값입니다(실제 발송 코드 아님). 문서에 자격증명·SMTP 키 0건 — secrets-policy G3.
메일 클라이언트는 JavaScript 를 실행하지 않으므로 '복사 버튼' 대신 코드 단독 블록(더블클릭 선택)과 「인증 계속하기」 딥링크를 제공합니다.</footer>
</body></html>"""

out = Path(sys.argv[1] if len(sys.argv) > 1 else "email-templates-preview.html")
out.write_text(page, encoding="utf-8")
print(f"saved {out} ({out.stat().st_size:,} bytes)")
