'use client';

import { useEffect, useMemo, useState } from 'react';

import { Nav } from '@/components/Nav';
import { api, type PickupPayload, type PickupRecord } from '@/lib/api';

const EMPTY_FORM: PickupPayload = {
  gdate: '2026.04.16',
  hcode: '',
  hname: '',
  gnumb: '',
  name1: '',
  gname: '',
  name2: '',
  gbigo: '',
  gqut1: 0,
  gqut2: 0,
};

export default function PickupsPage() {
  const [filters, setFilters] = useState({ gdate: '2026.04.16', publisher: '', customer: '' });
  const [rows, setRows] = useState<PickupRecord[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [form, setForm] = useState<PickupPayload>(EMPTY_FORM);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const selected = useMemo(() => rows.find((row) => row.id === selectedId) || null, [rows, selectedId]);

  async function load() {
    setLoading(true);
    setMessage('');
    try {
      const response = await api.listPickups(filters);
      setRows(response.items);
      if (selectedId) {
        const keep = response.items.find((item) => item.id === selectedId);
        if (!keep) setSelectedId(null);
      }
    } catch (err) {
      setMessage(err instanceof Error ? err.message : '조회 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (selected) {
      const { id: _id, ...rest } = selected;
      setForm(rest);
    }
  }, [selected]);

  function updateField<K extends keyof PickupPayload>(key: K, value: PickupPayload[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function createRecord() {
    const created = await api.createPickup(form);
    setMessage(`추가 완료: ${created.id}`);
    setSelectedId(created.id);
    await load();
  }

  async function updateRecord() {
    if (!selectedId) return;
    const updated = await api.updatePickup(selectedId, form);
    setMessage(`수정 완료: ${updated.id}`);
    await load();
  }

  async function deleteRecord() {
    if (!selectedId) return;
    await api.deletePickup(selectedId);
    setSelectedId(null);
    setForm({ ...EMPTY_FORM, gdate: filters.gdate || EMPTY_FORM.gdate });
    setMessage('삭제 완료');
    await load();
  }

  return (
    <main className="page-shell">
      <Nav />
      <section className="card">
        <h1 className="section-title">반품수거내역</h1>
        <p className="small-muted">Subu36 폼을 웹 CRUD 화면으로 재구성한 버전</p>
        <div className="filter-grid">
          <div className="field">
            <label>거래일자</label>
            <input value={filters.gdate} onChange={(e) => setFilters((p) => ({ ...p, gdate: e.target.value }))} />
          </div>
          <div className="field">
            <label>출판사명</label>
            <input value={filters.publisher} onChange={(e) => setFilters((p) => ({ ...p, publisher: e.target.value }))} />
          </div>
          <div className="field">
            <label>거래처명</label>
            <input value={filters.customer} onChange={(e) => setFilters((p) => ({ ...p, customer: e.target.value }))} />
          </div>
          <div className="field" style={{ justifyContent: 'flex-end' }}>
            <label>&nbsp;</label>
            <button className="btn primary" onClick={() => void load()}>검색</button>
          </div>
        </div>
      </section>

      <section className="card">
        <div className="filter-grid">
          <div className="field"><label>출판사코드</label><input value={form.hcode} onChange={(e) => updateField('hcode', e.target.value)} /></div>
          <div className="field"><label>출판사명</label><input value={form.hname} onChange={(e) => updateField('hname', e.target.value)} /></div>
          <div className="field"><label>운송장번호</label><input value={form.gnumb} onChange={(e) => updateField('gnumb', e.target.value)} /></div>
          <div className="field"><label>지역</label><input value={form.name1} onChange={(e) => updateField('name1', e.target.value)} /></div>
          <div className="field"><label>서점명</label><input value={form.gname} onChange={(e) => updateField('gname', e.target.value)} /></div>
          <div className="field"><label>화물명</label><input value={form.name2} onChange={(e) => updateField('name2', e.target.value)} /></div>
          <div className="field"><label>시내</label><input type="number" value={form.gqut1} onChange={(e) => updateField('gqut1', Number(e.target.value))} /></div>
          <div className="field"><label>지방</label><input type="number" value={form.gqut2} onChange={(e) => updateField('gqut2', Number(e.target.value))} /></div>
          <div className="field" style={{ gridColumn: '1 / -1' }}><label>메모</label><textarea rows={3} value={form.gbigo} onChange={(e) => updateField('gbigo', e.target.value)} /></div>
        </div>
        <div className="action-row">
          <button className="btn" onClick={() => { setSelectedId(null); setForm({ ...EMPTY_FORM, gdate: filters.gdate || EMPTY_FORM.gdate }); }}>추가</button>
          <button className="btn" disabled={!selectedId} onClick={() => void updateRecord()}>수정</button>
          <button className="btn" disabled={!selectedId} onClick={() => void deleteRecord()}>삭제</button>
          <button className="btn primary" onClick={() => void createRecord()}>저장</button>
          <button className="btn" onClick={() => { if (selected) { const { id: _id, ...rest } = selected; setForm(rest); } else { setForm(EMPTY_FORM); } }}>취소</button>
          <div className="small-muted" style={{ marginLeft: 'auto' }}>{message}</div>
        </div>
      </section>

      <section className="card">
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>출판사코드</th>
                <th>출판사명</th>
                <th>지역명</th>
                <th>거래처명</th>
                <th>화물명</th>
                <th>시내</th>
                <th>지방</th>
                <th>메모</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id} className={row.id === selectedId ? 'selected' : ''} onClick={() => setSelectedId(row.id)}>
                  <td>{row.hcode}</td>
                  <td>{row.hname}</td>
                  <td>{row.name1}</td>
                  <td>{row.gname}</td>
                  <td>{row.name2}</td>
                  <td>{row.gqut1}</td>
                  <td>{row.gqut2}</td>
                  <td>{row.gbigo}</td>
                </tr>
              ))}
              {!loading && rows.length === 0 ? <tr><td colSpan={8}>데이터가 없습니다.</td></tr> : null}
            </tbody>
          </table>
        </div>
        <div className="summary-bar">
          <span>레코드: {rows.length}</span>
          <span>시내 합계: {rows.reduce((sum, row) => sum + row.gqut1, 0)}</span>
          <span>지방 합계: {rows.reduce((sum, row) => sum + row.gqut2, 0)}</span>
        </div>
      </section>
    </main>
  );
}
