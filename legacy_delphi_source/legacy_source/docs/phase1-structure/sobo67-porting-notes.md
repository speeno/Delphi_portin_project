# Sobo67 (�������⸻����) web porting notes

Source: [Subu67.pas](../../Subu67.pas), [Subu67.dfm](../../Subu67.dfm), wireframe [Sobo67.svg](wireframes/Sobo67.svg).

## DBGrid columns (Subu67.dfm)

### DBGrid101 (DataSource1 �� Base10.T6_Sub71), caption ���⵵�� on GDATE

| FieldName | Title.Caption |
|-----------|----------------|
| GDATE | �⵵ |
| GNAME | �� �� �� |
| GIQUT | �԰����� |
| GOQUT | ������� |
| GJQUT | �������� |
| GBQUT | ��ǰ���� |
| GPQUT | ������ |
| GOSUM | ����ݾ� |
| GBSUM | ��ǰ�ݾ� |

### DBGrid201 (DataSource2 �� Base10.T6_Sub72)

Same fields except first column title is **���** (still `GDATE`).

Footer row uses EhGrid sum on quantity/amount columns (Delphi).

## Button101 / Button201 SQL fragments (Subu67.pas)

Both run a first aggregate on **S1_Ssub**:

```text
Select Bcode,Gdate,Scode,Gubun,Pubun,
  Sum(Gsqut) as Gsqut, Sum(Gssum) as Gssum
From S1_Ssub Where {D_Select}{St1}
Group By Bcode,Gdate,Scode,Gubun,Pubun
```

`St1` includes (typical):

- `Gdate >= 'yyyy.mm.00' and Gdate <= 'yyyy.mm.99'`
- `Hcode = '��'` when Edit107 set
- `Ocode Like '%B%'` or `'%A%'` from Panel102 (������/â������ �� B, ���絵�� �� A)
- Optional `Bcode` / `Gcode` ranges from Edit103?105
- Optional `S_Where1`
- If CheckBox2: `((Scode='X' and Gcode<>'00001') or (Scode='Y') or (Scode='Z'))`

Delphi then **iterates the result grid** and maps rows into client `nSqry` / `mSqry` with rules (�԰�/��ǰ/���/����/���). The web sample reproduces this classification in `sobo67_aggregate.py` (see Web sample section below).

Second aggregate for **Gpsum** uses **Sg_Csum**:

```text
Select Gcode,Gdate,Sum(Gbsum) as Gbsum
From Sg_Csum Where {D_Select}{St1}
Group By Gcode,Gdate
```

(Button101 uses `Gcode` range variant of `St1` in a second pass; see pas around lines 394?410.)

## Web sample (Subu67-aligned `/api/sobo67/search`)

- SQL: [web/seak80-sample/backend/sobo67_sql.py](../../web/seak80-sample/backend/sobo67_sql.py) — `S1_Ssub s` detail `GROUP BY` + optional `G4_Book` join; `Sg_Csum` uses `Scode LIKE` for the second pass.
- Aggregate: [web/seak80-sample/backend/sobo67_aggregate.py](../../web/seak80-sample/backend/sobo67_aggregate.py) — Delphi `While` classification + `gpsum` merge.
- API: [web/seak80-sample/backend/main.py](../../web/seak80-sample/backend/main.py) — `footerTotals`, params `bcodeFrom`/`bcodeTo`/`parentGcode`/`t00`; `GET /api/sobo67/hcode-check` (sample row in `G4_Book`).
- UI: [web/seak80-sample/frontend/sobo67.html](../../web/seak80-sample/frontend/sobo67.html) — year-row click loads month grid; Seek20 `?postMessage=1`; print CSS `.no-print`.
- Regression: compare CSV vs Delphi for same Hcode/range; if `d_select_sql` is set, validate column qualification vs alias `s`.
- Ops: env `SEAK80_SOBO67_DETAIL_LIMIT` (default 25000) caps grouped detail rows per request.

## References in repo

- Menu: [11-screen-business-flows.md](11-screen-business-flows.md) (Menu607Click �� TSobo67).
- Tong02 `Srart_67_01` / `Srart_67_02`: status-bar totals (commented in chul_09 branch).
