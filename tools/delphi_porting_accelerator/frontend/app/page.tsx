import { Nav } from '@/components/Nav';

export default function HomePage() {
  return (
    <main className="page-shell">
      <Nav />
      <section className="card">
        <h1 className="section-title">Delphi → Next.js/FastAPI 포팅 스타터</h1>
        <p>
          이 프로젝트는 DFM/PAS를 기반으로 한 레거시 화면을 웹 화면과 API 구조로 재구성하는 예시입니다.
          기능 화면과 원본 폼 미리보기를 나눠서 확인할 수 있습니다.
        </p>
        <ul>
          <li>Seak04: 우편번호 검색 팝업 → 검색형 화면</li>
          <li>Subu36: 반품수거내역 → CRUD 중심 업무 화면</li>
          <li>dfm2web: DFM/PAS → HTML/JSON 변환기</li>
        </ul>
      </section>
    </main>
  );
}
