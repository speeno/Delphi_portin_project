/**
 * 데이터 테이블 공통 컴포넌트
 *
 * 기존 델파이 TDBGrid의 동작을 웹으로 재현한다.
 * - 컬럼 정렬
 * - 페이지네이션
 * - 행 선택
 * - 검색 필터
 */

export function renderDataTable({ columns, data, page, pageSize, total, onPageChange, onRowClick }) {
  const totalPages = Math.ceil(total / pageSize);

  const headerCells = columns.map(col =>
    `<th style="width:${col.width || 'auto'}">${col.label}</th>`
  ).join('');

  const rows = data.length > 0
    ? data.map((row, idx) => {
        const cells = columns.map(col => `<td>${row[col.key] ?? ''}</td>`).join('');
        return `<tr data-idx="${idx}" class="clickable">${cells}</tr>`;
      }).join('')
    : `<tr><td colspan="${columns.length}" class="empty-row">데이터가 없습니다.</td></tr>`;

  const pagination = totalPages > 1 ? `
    <div class="pagination">
      <button class="page-btn" data-page="${page - 1}" ${page <= 1 ? 'disabled' : ''}>이전</button>
      <span class="page-info">${page} / ${totalPages} (총 ${total}건)</span>
      <button class="page-btn" data-page="${page + 1}" ${page >= totalPages ? 'disabled' : ''}>다음</button>
    </div>` : '';

  return `
    <div class="data-table-wrapper">
      <table class="data-table">
        <thead><tr>${headerCells}</tr></thead>
        <tbody>${rows}</tbody>
      </table>
      ${pagination}
    </div>`;
}

export function renderSearchForm({ fields, onSearch }) {
  const fieldHTML = fields.map(f => `
    <div class="search-field">
      <label>${f.label}</label>
      ${f.type === 'select'
        ? `<select name="${f.name}">${f.options.map(o => `<option value="${o.value}">${o.label}</option>`).join('')}</select>`
        : `<input type="${f.type || 'text'}" name="${f.name}" placeholder="${f.placeholder || ''}" />`
      }
    </div>`
  ).join('');

  return `
    <div class="search-form">
      ${fieldHTML}
      <button class="btn btn-primary search-btn">조회</button>
    </div>`;
}
