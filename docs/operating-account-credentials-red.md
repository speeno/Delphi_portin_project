# 운영 계정 자격증명 RED 산출물 처리 메모

## 현재 상태

- `WeLove_FTP/_oneoff_distributor_credentials_DELETE_AFTER_USE.xlsx` 는 RED 등급 파일이며 `WeLove_FTP/` 가 `.gitignore` 대상이라 git 추적 대상이 아니다.
- 운영 이관(vault/1Password) 완료 여부는 사용자 확인이 필요하다. 확인 전에는 임의 삭제하지 않는다.
- 재생성 도구는 `tools/export_id_logn_credentials_red.py` 로 명시화했다. 도구 자체에는 비밀번호가 포함되지 않지만, 실행 결과 xlsx 에는 평문 `Gpass` 가 포함된다.

## 운영 절차

1. `python3 tools/export_id_logn_credentials_red.py --dry-run` 으로 서버별 행 수만 확인한다.
2. 필요한 경우 `--server remote_153` 처럼 범위를 줄여 xlsx 를 재생성한다.
3. xlsx 를 vault/1Password 또는 사내 secret store 로 이관한다.
4. 이관 완료 후 xlsx 는 `rm -P` 또는 동등한 zeroize 방식으로 삭제한다.

## 금지 사항

- `Gpass`/토큰/DB 비밀번호를 문서, PR, 이슈, 메신저 본문에 붙여 넣지 않는다.
- xlsx 를 `WeLove_FTP/` 밖, 동기화 클라우드, git 추적 경로에 저장하지 않는다.
