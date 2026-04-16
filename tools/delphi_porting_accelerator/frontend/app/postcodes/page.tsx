'use client';

import { useEffect, useState } from 'react';

import { Nav } from '@/components/Nav';
import { api, type PostcodeRow } from '@/lib/api';

export default function PostcodesPage() {
  const [keyword, setKeyword] = useState('');
  const [rows, setRows] = useState<PostcodeRow[]>([]);
  const [selected, setSelected] = useState<PostcodeRow | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function search(nextKeyword = keyword) {
    setLoading(true);
    setError('');
    try {
      const response = await api.searchPostcodes(nextKeyword);
      setRows(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : '검색 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void search('');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className="page-shell">
      <Nav />
      <section className="card">
        <h1 className="section-title">우편번호검색현황</h1>
        <p className="small-muted">Seak04 폼을 웹 화면으로 재구성한 버전</p>
        <div className="filter-grid">
          <div className="field" style={{ gridColumn: 'span 3' }}>
            <label htmlFor="keyword">우편번호 / 주소</label>
            <input
              id="keyword"
              value={keyword}
              onChange={(event) => setKeyword(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') void search();
              }}
              placeholder="우편번호 또는 주소를 입력하세요"
            />
          </div>
          <div className="field" style={{ justifyContent: 'flex-end' }}>
            <label>&nbsp;</label>
            <button className="btn primary" onClick={() => void search()}>
              검색
            </button>
          </div>
        </div>
        {error ? <p style={{ color: '#b91c1c' }}>{error}</p> : null}
      </section>

      <section className="card">
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>우편번호</th>
                <th>주소</th>
                <th>^</th>
                <th>지역</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr
                  key={`${row.post}-${row.addr}`}
                  className={selected?.post === row.post && selected?.addr === row.addr ? 'selected' : ''}
                  onClick={() => setSelected(row)}
                  onDoubleClick={() => setSelected(row)}
                >
                  <td>{row.post}</td>
                  <td>{row.addr}</td>
                  <td>{row.dddd || '-'}</td>
                  <td>{row.dong || row.city || '-'}</td>
                </tr>
              ))}
              {!loading && rows.length === 0 ? (
                <tr>
                  <td colSpan={4}>검색 결과가 없습니다.</td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
        <div className="action-row">
          <button className="btn primary" disabled={!selected}>선택</button>
          <button className="btn">취소</button>
          <div className="small-muted" style={{ marginLeft: 'auto' }}>
            {loading ? '검색 중...' : `총 ${rows.length}건`}
          </div>
        </div>
      </section>
    </main>
  );
}
