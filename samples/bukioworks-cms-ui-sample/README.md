# 북이오웍스 CMS UI 샘플

도서물류관리 프로그램 본체와 분리된 **디자인 가이드 데모**입니다. 레이아웃·타이포·토큰은 저장소 루트 [`docs/Design.md`](../../docs/Design.md) 및 운영 프론트의 `globals.css` 계열과 맞춰 두었습니다.

## 실행

```bash
cd samples/bukioworks-cms-ui-sample
npm install
npm run dev
```

개발 서버 기본 포트: **3010** (`http://localhost:3010`).

## 포함 화면

| 경로 | 내용 |
|------|------|
| `/` | **북이오웍스 소개 랜딩** ([buk.io](https://buk.io/) 스타일 헤더·풋터, 일러스트·가이드 산출물, Light/Vivid 섹션) |
| `/dashboard` | 사이드바+헤더 셸, 카드·안내 블록, 화면당 1개 라임 CTA |
| `/list` | 검색 패널·테이블 헤더 음영·합계 행 Pale Lime |
| `/settings` | 폼 간격 스켈레톤 |
| `/login` | 분할 레이아웃 로그인 데모 (API 없음) |

정적 이미지는 `public/marketing/` 에 두었습니다 (워드마크·일러스트·가이드 캡처 등).

백엔드/API 연동은 없습니다.
