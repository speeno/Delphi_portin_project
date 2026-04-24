/**
 * 공통 레이아웃 컴포넌트
 *
 * 메뉴/헤더/사이드바 구조를 정의한다.
 * 기존 델파이 메뉴 구조를 웹으로 재현한다.
 */

// DEC-RBAC-02 — 라벨은 docs/onboarding-rbac-menu-matrix.md (정본 매트릭스) 의
// NAV 캡션 표기에 맞춘다. 본 prototype 은 사이드바 게이트가 없으므로 라벨만 동기.
export const menuItems = [
  {
    id: 'inbound',
    label: '입고관리',
    icon: '📥',
    children: [
      { id: 'inbound-list', label: '입고 조회', path: '/inbound' },
      { id: 'inbound-create', label: '입고 등록', path: '/inbound/create' },
    ],
  },
  {
    id: 'outbound',
    label: '출고관리',
    icon: '📤',
    children: [
      { id: 'outbound-list', label: '출고 조회', path: '/outbound' },
      { id: 'outbound-create', label: '출고 등록', path: '/outbound/create' },
    ],
  },
  {
    id: 'inventory',
    label: '재고관리',
    icon: '📦',
    children: [
      { id: 'inventory-list', label: '재고 조회', path: '/inventory' },
      { id: 'inventory-adjust', label: '재고 조정', path: '/inventory/adjust' },
    ],
  },
  {
    id: 'admin',
    label: '웹관리',
    icon: '⚙️',
    children: [
      { id: 'admin-users', label: '사용자 관리', path: '/admin/users' },
      { id: 'admin-harness', label: '하네스 상태', path: '/admin/harness' },
    ],
  },
];

export function renderLayout(content, activeMenuId = '') {
  const sidebar = menuItems.map(group => {
    const children = group.children.map(item => {
      const active = item.id === activeMenuId ? 'active' : '';
      return `<a href="${item.path}" class="menu-item ${active}" data-id="${item.id}">${item.label}</a>`;
    }).join('');

    return `
      <div class="menu-group">
        <div class="menu-group-title">${group.icon} ${group.label}</div>
        ${children}
      </div>`;
  }).join('');

  return `
    <div class="layout">
      <header class="top-header">
        <div class="header-title">도서 물류 시스템</div>
        <div class="header-info">
          <span id="current-warehouse"></span>
          <span id="current-user"></span>
        </div>
      </header>
      <div class="layout-body">
        <nav class="sidebar">${sidebar}</nav>
        <main class="content">${content}</main>
      </div>
    </div>`;
}
