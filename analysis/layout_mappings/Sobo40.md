# 레이아웃 매핑: Sobo40 (패스워드 다이얼로그) → 모던 `<AuditPasswordModal>`

DEC-028 의무. C4 Phase 1 신규 매핑 — **재고 변경 작업의 권한 인증 게이트** (Sobo24/25/51 의 처리 트랜잭션 직전 호출).

## 0. 입력 산출물

- 본 폼: [`tools/.../Subu40/Sobo40.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu40/Sobo40.html) + `Sobo40.form.json` + `Sobo40.tree.json` + `Sobo40.pas_analysis.json`
- 변형 부재 — `Subu40` 단일
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu40.dfm`](../../legacy_delphi_source/legacy_source/Subu40.dfm)
- pas: [`legacy_delphi_source/legacy_source/Subu40.pas`](../../legacy_delphi_source/legacy_source/Subu40.pas)
- 모던 컴포넌트(예정 — T6): `frontend/src/components/audit/audit-password-modal.tsx`
- 백엔드 엔드포인트(예정 — T5): `POST /api/v1/audit/password-verify`
- 계약: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) `endpoints[/audit/password-verify]` (T3)

## 1. 의미 분기 — 단순 패스워드 다이얼로그

레거시 `Sobo40` 은 **단순 모달 다이얼로그**:
- 라벨 1개 ("패스워드:")
- 입력 1개 (Edit101 — 패스워드 마스킹)
- 버튼 2개 (확인/취소)

호출 패턴: Sobo24/25/51 등 재고 변경 화면에서 처리 직전 `Sobo40.ShowModal` 호출 → 사용자 입력 → 백엔드 검증 → 통과 시 트랜잭션 실행.

모던 Phase 1: 공통 컴포넌트 `<AuditPasswordModal>` — 호출자에게 onSuccess/onCancel 콜백 노출, 백엔드 검증 후 token 반환 → 트랜잭션 헤더에 첨부.

## 2. dfm 영역 인벤토리 (tree.json)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 다이얼로그 본체 | `Sobo40` (TForm, BorderStyle=bsDialog) | n/a | myLabel3d2, Edit101, Button101, Button102 | `<Dialog>` (shadcn/ui) |

> dfm 의 BorderStyle=bsDialog → 모던에서는 `<DialogContent>` 로 흡수 (오버레이 + 중앙 정렬).

## 3. 위젯 매핑 (전체)

| dfm TO | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| n/a | `myLabel3d2` | TmyLabel3d ('패스워드:') | 입력 라벨 | `<Label htmlFor="audit_password">패스워드</Label>` | `Sobo40.myLabel3d2` |
| 0 | `Edit101` | TFlatEdit (PasswordChar='*') | 패스워드 입력 | `<Input id="audit_password" type="password" autoFocus>` | `Sobo40.Edit101` |
| 1 | `Button101` | TFlatButton ('확인') | 검증 실행 | `<Button onClick=onConfirm>확인</Button>` (PRIMARY) | `Sobo40.Button101` |
| 2 | `Button102` | TFlatButton ('취소') | 취소 (다이얼로그 닫기) | `<Button variant=ghost onClick=onCancel>취소</Button>` | `Sobo40.Button102` |

## 4. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `FormShow` | `useEffect` mount → `Edit101` autoFocus |
| `Edit101.OnKeyPress` (Enter) | `onConfirm` 트리거 (단축키) |
| `Button101Click` ('확인') | `onConfirm` → `auditApi.verifyPassword({password})` → 통과 시 `props.onSuccess(token)`, 실패 시 `setError("패스워드가 올바르지 않습니다")` |
| `Button102Click` ('취소') | `props.onCancel()` → 다이얼로그 닫기 |
| `FormClose` (Esc) | `onCancel` 트리거 |

## 5. out-of-scope

해당 없음 — 위젯 트리가 4개로 단순.

## 6. Deltas — 모던 신설

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | 에러 메시지 영역 | Edit101 아래 빨강 텍스트 | dfm 은 ShowMessage 별도 호출 → 모던은 inline 표시 |
| 모던 신규 | 토큰 기반 검증 결과 | onSuccess(token) 콜백 | dfm 은 boolean 반환 → 모던은 짧은 수명 토큰 (5분) 반환, 트랜잭션 헤더 첨부 |
| 모던 신규 | autoFocus + Enter 단축키 | Edit101 | UX 개선 |
| 모던 신규 | 검증 실패 횟수 제한 | (3회 실패 시 모달 닫기 + 페이지 reload) | 무차별 대입 방지 |
| 모던 신규 | 마스킹 + 보이기 토글 | `<Button>` (눈 아이콘) | 접근성 개선 |

## 7. 호출자 매핑 (어떤 폼에서 Sobo40 을 호출하는가)

| 호출자 | 호출 시점 | 모던 호출 위치 |
| --- | --- | --- |
| Sobo24 (재생) | `Button700Click` 직전 | `/returns/dispose/regen/page.tsx` 의 onRegenerate 핸들러 |
| Sobo25 (해체) | `Button700Click` 직전 | `/returns/dispose/disassemble/page.tsx` 의 onDisassemble 핸들러 |
| Sobo51 (변경) | `Button801/802Click` 직전 | `/returns/change/page.tsx` 의 onMoveToBipum 핸들러 |
| (후속) Sobo34_4 (폐기 원장 - "본사출고->변경" 토글) | CheckBox2 활성화 시 | Phase 2 |
| (후속) Sobo23 의 일괄 취소 | (조사 필요) | Phase 2 |

> 모던 사용 패턴 (코드 스니펫):
> ```tsx
> const [showPwd, setShowPwd] = useState(false);
> const onRegenerate = () => setShowPwd(true);
> // ...
> <AuditPasswordModal
>   open={showPwd}
>   onCancel={() => setShowPwd(false)}
>   onSuccess={(token) => { setShowPwd(false); doRegenerate(token); }}
>   data-legacy-id="Sobo40"
> />
> ```

## 8. 변형 차이

`legacy_source_root/Subu40` 단일 — variant 0건. contract `customer_variants.Sobo40` 에 "variant 0건" 단언 (T3).

## 9. 회귀 가드 체크리스트

- [ ] 본 노트의 부착 대상 `data-legacy-id` (~5개) 가 `<AuditPasswordModal>` DOM 에 존재:
  - `Sobo40` (다이얼로그 컨테이너)
  - `Sobo40.myLabel3d2`, `Sobo40.Edit101`, `Sobo40.Button101`, `Sobo40.Button102`
- [ ] **Sobo24/25/51 의 트랜잭션 호출은 반드시 토큰을 헤더에 첨부** (백엔드 검증 — 토큰 없이 트랜잭션 호출 시 401)
- [ ] Edit101 의 type=password (마스킹 보존)
- [ ] Enter 키 → onConfirm 동작
- [ ] Esc 키 → onCancel 동작
- [ ] 패스워드 검증 실패 메시지 inline 표시 (별도 alert 호출 금지)
- [ ] 토큰 수명 = 5분 (백엔드 강제), 만료 시 모달 재표시
- [ ] DEC-028 §3 "버리는 정보" 가 코드에 없음

## 10. 보안 결정 사항 (DEC-029 신설 예정 — T8)

- **백엔드 검증 알고리즘**: bcrypt(cost=12) 비교 — 평문 비교 금지
- **토큰 수명**: 5분 (HMAC-SHA256, 키는 환경변수 `AUDIT_TOKEN_SECRET`)
- **토큰 페이로드**: `{user_id, expires_at, scope: 'inventory_change'}`
- **검증 실패 횟수**: 3회 → 모달 닫기 + 30초 잠금
- **감사 로그**: 검증 시도 (성공/실패) 모두 `audit_log` 테이블 INSERT
- **현재 임시 구현 (Phase 1)**: 환경변수 `AUDIT_PASSWORD` 와 평문 비교 → DEC-029 에 정식 정책 + Phase 2 마이그레이션 일정 명시

## 11. 참조

- DEC-028: dfm→html 산출물 영구 입력 동결
- DEC-029 (T8 신설): 재고 변경 작업의 패스워드 게이트 정책 (본 노트 §10)
- 호출자: [`Sobo24.md`](Sobo24.md), [`Sobo25.md`](Sobo25.md), [`Sobo51.md`](Sobo51.md)
- contract: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) (T3 — `endpoints[/audit/password-verify]`)
- 회귀 테스트: [`test/test_c4_returns_phase1.py`](../../test/test_c4_returns_phase1.py) (T4 — `TestAuditPasswordGate`)
- OQ-RT-2 (T8 신설): "Phase 2 패스워드 검증 백엔드 강화" — bcrypt + audit_log 마이그레이션
