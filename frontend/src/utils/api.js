/**
 * API 클라이언트
 *
 * Routing Harness 연동을 위해 모든 요청에
 * X-Request-Id, X-User-Id 헤더를 자동 추가한다.
 */

const API_BASE = window.__API_BASE__ || '/api';

let authToken = '';
let userId = '';

export function setAuth(token, user) {
  authToken = token;
  userId = user;
}

export async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const headers = {
    'Content-Type': 'application/json',
    'X-Request-Id': `fe-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    ...options.headers,
  };

  if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
  if (userId) headers['X-User-Id'] = userId;

  const start = performance.now();

  const response = await fetch(url, { ...options, headers });
  const elapsed = performance.now() - start;

  const data = await response.json();

  if (window.__HARNESS_DEBUG__) {
    console.log(`[API] ${options.method || 'GET'} ${path} -> ${response.status} (${elapsed.toFixed(0)}ms)`);
  }

  return { status: response.status, data, elapsed };
}

export const api = {
  get: (path, params) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return request(path + qs);
  },
  post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) }),
  put: (path, body) => request(path, { method: 'PUT', body: JSON.stringify(body) }),
  delete: (path) => request(path, { method: 'DELETE' }),
};
