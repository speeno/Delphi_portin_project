export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export interface PostcodeRow {
  post: string;
  addr: string;
  dddd?: string | null;
  dong?: string | null;
  city?: string | null;
}

export interface PostcodeResponse {
  items: PostcodeRow[];
  count: number;
}

export interface PickupRecord {
  id: number;
  gdate: string;
  hcode: string;
  hname: string;
  gnumb: string;
  name1: string;
  gname: string;
  name2: string;
  gbigo: string;
  gqut1: number;
  gqut2: number;
}

export interface PickupListResponse {
  items: PickupRecord[];
  count: number;
  sum_gqut1: number;
  sum_gqut2: number;
}

export interface PickupPayload {
  gdate: string;
  hcode: string;
  hname: string;
  gnumb: string;
  name1: string;
  gname: string;
  name2: string;
  gbigo: string;
  gqut1: number;
  gqut2: number;
}

export const api = {
  searchPostcodes(keyword: string) {
    const params = new URLSearchParams({ keyword });
    return request<PostcodeResponse>(`/api/postcodes/search?${params.toString()}`);
  },
  listPickups(filters: { gdate?: string; publisher?: string; customer?: string }) {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.set(key, value);
    });
    return request<PickupListResponse>(`/api/pickups?${params.toString()}`);
  },
  createPickup(payload: PickupPayload) {
    return request<PickupRecord>('/api/pickups', { method: 'POST', body: JSON.stringify(payload) });
  },
  updatePickup(id: number, payload: Partial<PickupPayload>) {
    return request<PickupRecord>(`/api/pickups/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
  },
  deletePickup(id: number) {
    return request<void>(`/api/pickups/${id}`, { method: 'DELETE' });
  },
};
