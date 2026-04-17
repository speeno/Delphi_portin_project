# Seak80 �� ���� (���ǻ�˻���Ȳ + DB ����)

`docs/phase1-structure/wireframes/Seak80.svg` ���̾������ӿ� ���� ���� ����Ʈ��, **���� MySQL**�� �ٴ� �鿣�� API�Դϴ�. ������ [Seak08.pas](../../Seak08.pas)�� `FilterTing`�� ������ `G7_Ggeo`�� **�κ� LIKE**�� ��ȸ�մϴ� (`D_Select` / `Lower` �ɼ�).

�߰� ȭ��: **Seek20** (`frontend/seek20.html`) ? �԰�ó `G2_Ggwo` ([Seek02.pas](../../��������/�ѱ���������/����/MySQL/��������/chul_09(������)/Seek02.pas)), **Seek30** (`frontend/seek30.html`) ? ���� `G3_Gjeo` ([Seek03.pas](../../Seek03.pas)). ���� �鿣�忡�� `/api/seek20/search`, `/api/seek30/search`�� �����մϴ�.

## ���� ����

- `backend/` ? FastAPI + PyMySQL, `servers.yaml`(���, ����), `seek_sql.py`
- `frontend/` ? `index.html`, `seek20.html`, `seek30.html`, `styles.css`, `app.js`, `seek20.js`, `seek30.js`

## �غ�

1. MySQL�� ���ǻ� �����Ͱ� �ִ� `G7_Ggeo` ���̺��� �ִ� DB(��: `chul_09_db`). Seek20/30�� �߰��� `G2_Ggwo`, `G3_Gjeo`�� �ʿ��մϴ�.
2. Python 3.10+

```bash
cd web/seak80-sample/backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp servers.example.yaml servers.yaml
# servers.yaml ����: host, user, password, database
```

## ���� (����: �� ��Ʈ����)

�鿣�尡 `frontend/`�� �������� �����ϹǷ� **�� ��Ʈ**�� UI + API�� ���� ��ϴ�.

```bash
cd web/seak80-sample/backend
source .venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000
```

������:

- Seak80: `http://127.0.0.1:8000/`
- Seek20: `http://127.0.0.1:8000/seek20.html`
- Seek30: `http://127.0.0.1:8000/seek30.html`

`uvicorn` ��Ʈ�� �ٲ㵵(��: `--port 9000`), **���� ȣ��Ʈ���� ������ ����** ���� ������ ��ũ��Ʈ�� ���� ��ó�� `/api/...`�� ȣ���մϴ�.

## ���� (����Ʈ�� ���� ����)

```bash
# �͹̳� 1
cd web/seak80-sample/backend && source .venv/bin/activate && uvicorn main:app --host 127.0.0.1 --port 8000

# �͹̳� 2
cd web/seak80-sample/frontend && python3 -m http.server 5500
```

�̶��� `index.html` **��**�� �Ʒ��� �־� API �ּҸ� �����ϼ���(�ڵ� ���� ��ũ��Ʈ���� **����** �ε�).

```html
<script>window.SEAK80_API_BASE = "http://127.0.0.1:8000";</script>
```


**masters-hub / masters-read (5500 + 8000):** With `python3 -m http.server 5500`, same-origin `fetch` hits `/api/...` on port 5500 and returns 404 unless the API base is set. Prefer `http://127.0.0.1:8000/masters-hub.html` via uvicorn, or open `masters-read.html` on 5500: its inline bootstrap sets `SEAK80_API_BASE` to `http://<hostname>:8000` when the page port is 5500.

**Why 5500 appears in docs:** Port 5500 is only for the optional `python3 -m http.server` workflow (README “실행” second terminal). `uvicorn` on 8000 does not use 5500.

**HTTP 404 on `/api/phase2/...` or other `/api/...`:** If the path matches OpenAPI (`/docs`) but the browser shows “not found”, check the JSON body: `detail.stage` may be `config` when `serverId` is not listed in `servers.yaml` (e.g. `remote_153` must be added there); that is not a missing API route.

�鿣�� CORS �⺻���� `*`�Դϴ�.

## ȯ�� ����

| ���� | ���� |
|------|------|
| `SEAK80_SERVERS_CONFIG` | `servers.yaml` ���/�̸� �������̵� (�⺻: `backend/servers.yaml`) |
| `SEAK80_CORS_ORIGINS` | ��� ��ó ���, �Ǵ� `*` (�⺻ `*`, credentials ��Ȱ��) |

## API

- `GET /api/health`
- `GET /api/servers` ? `{ id, label }[]`
- `GET /api/publishers?serverId=&q=&limit=` ? `G7_Ggeo` �� JSON (`q`�� ��� �� �迭��`gcode` ��)
- `GET /api/seek20/search?serverId=&q=&hcode=&limit200=&lower=&excludeGrat9=&limit=` ? **�԰�ó** `G2_Ggwo`. `q`�� ��� �� �迭(Seek02 `FilterTing` Exit). `hcode`�� ������ `Hnnnn`. `limit200=true`�̸� `LIMIT 0,200` (`limit`�� �Բ��� `min(200,limit)`). `lower=true`�̸� `LOWER(col) LIKE LOWER('%q%')`. `excludeGrat9=true`�̸� `(Grat9<>1 OR Grat9 IS NULL)` AND �˻�����. ���信 `sname`(������� ���̻�) ����.
- `GET /api/seek30/search?serverId=&q=&hcode=&limit200=&lower=&limit=` ? **����** `G3_Gjeo`. �Ķ���ʹ� Seek20�� ����(Grat9 �ɼ� ����).

**`servers.yaml` ���� �ʵ� `d_select_sql`**: Seek20/30 SQL���� `WHERE` �ٷ� �ڿ� �̾� �ٴ� ���ڿ�(���Ž� `D_Select`). ��: `` `Check`=0 and ``

OpenAPI: `http://127.0.0.1:8000/docs`

## DB ���� ���С��� ��� ��

- `backend/servers.yaml`�� ������ API�� �� �迭�� ���� �ְ� �ֿܼ� `(servers.yaml ����)`�� ����ϴ�. `servers.example.yaml`�� ������ ä�켼��.
- �鿣�尡 ���� �ְų� �ּҰ� Ʋ���� `(���� ����)` �ɼǰ� ���� �޽����� ǥ�õ˴ϴ�.

## �ѱ� ����

- `frontend/*.html|css|js`�� **UTF-8(�� BOM)** ���� �����ϼ���.
- �����Ͱ� CP949�� ���� �ѱ� DB�� ���� �� �ֽ��ϴ�. �ʿ� �� ����� ��Ʈ�� `python3 debug/write_seak80_frontend_utf8.py`�� `index.html`��`app.js`�� �ٽ� UTF-8�� �� �� �ֽ��ϴ�.
- �鿣�� ���� ����� `Content-Type: ��; charset=utf-8`�� �ٽ��ϴ� (`EnsureUtf8CharsetMiddleware`).
- DB ���ڼ��� MySQL ���� ���ڼ�(`utf8mb4`)��collation�� Ȯ���ϼ���.
