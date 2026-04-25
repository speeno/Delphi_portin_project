-- ============================================================================
-- DSN-DEC-10 — Welove 테넌트 신규 DB 부트스트랩 정본 스키마 (스켈레톤 시드)
-- ----------------------------------------------------------------------------
-- 본 파일은 ``tenant_db_provisioner`` 가 신규 테넌트 DB 생성 직후 import 하는
-- 정본 스키마 SQL 입니다.
--
-- ⚠️ 본 파일은 **운영 표준 DB 에서 추출한 정본 스키마로 1회 교체** 되어야 합니다.
--
-- 1) 운영자 PC 에서 표준 DB(권장: ``chul_05_db``) 의 스키마만 추출:
--      mysqldump -h <서버4 host> -u root -p \
--        --no-data --skip-comments --skip-add-drop-table \
--        --default-character-set=euckr \
--        chul_05_db > docs/schema/welove_tenant_template.sql
--
-- 2) 본 파일 상단에 다음 헤더 주석을 추가 (운영자 책임):
--      -- DSN-DEC-10 정본 — 추출일 YYYY-MM-DD, 추출원: <server>/<db>, 행 데이터 0건
--
-- 3) 추출 결과에 ``INSERT INTO`` 문 / 자격증명이 포함되지 않았는지 검증:
--      ! grep -i "INSERT INTO\|GRANT\|IDENTIFIED BY" docs/schema/welove_tenant_template.sql
--
-- 4) git commit (행 데이터 0건이므로 G3 비밀 정책 위반 없음).
-- ----------------------------------------------------------------------------
-- 현재 스켈레톤 (정본 교체 전 임시) — ``Id_Logn`` 1 테이블만 정의하여 부트스트랩
-- 단계가 동작하도록 한다. 정본 교체 후에는 본 스켈레톤이 운영 전체 테이블 셋으로
-- 대체된다 (``tenant_db_provisioner`` 의 시드 INSERT 는 본 테이블만 의존).
-- ============================================================================

CREATE TABLE IF NOT EXISTS `Id_Logn` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `hcode` VARCHAR(5) DEFAULT NULL COMMENT '출판사코드 (RBAC 분기 키)',
  `hname` VARCHAR(50) DEFAULT NULL COMMENT '출판사명',
  `gcode` VARCHAR(50) DEFAULT NULL COMMENT '로그인 ID (DEC-RBAC-01)',
  `gname` VARCHAR(50) DEFAULT NULL COMMENT '표시명',
  `f11` VARCHAR(2) DEFAULT NULL,
  `f12` VARCHAR(2) DEFAULT NULL,
  `f13` VARCHAR(2) DEFAULT NULL,
  `f14` VARCHAR(2) DEFAULT NULL,
  `f15` VARCHAR(2) DEFAULT NULL,
  `f16` VARCHAR(2) DEFAULT NULL,
  `f17` VARCHAR(2) DEFAULT NULL,
  `f18` VARCHAR(2) DEFAULT NULL,
  `f19` VARCHAR(2) DEFAULT NULL,
  `f21` VARCHAR(2) DEFAULT NULL,
  `f22` VARCHAR(2) DEFAULT NULL,
  `f23` VARCHAR(2) DEFAULT NULL,
  `f24` VARCHAR(2) DEFAULT NULL,
  `f25` VARCHAR(2) DEFAULT NULL,
  `f26` VARCHAR(2) DEFAULT NULL,
  `f27` VARCHAR(2) DEFAULT NULL,
  `f28` VARCHAR(2) DEFAULT NULL,
  `f29` VARCHAR(2) DEFAULT NULL,
  `f31` VARCHAR(2) DEFAULT NULL,
  `f32` VARCHAR(2) DEFAULT NULL,
  `f33` VARCHAR(2) DEFAULT NULL,
  `f34` VARCHAR(2) DEFAULT NULL,
  `f35` VARCHAR(2) DEFAULT NULL,
  `f36` VARCHAR(2) DEFAULT NULL,
  `f37` VARCHAR(2) DEFAULT NULL,
  `f38` VARCHAR(2) DEFAULT NULL,
  `f39` VARCHAR(2) DEFAULT NULL,
  `f41` VARCHAR(2) DEFAULT NULL,
  `f42` VARCHAR(2) DEFAULT NULL,
  `f43` VARCHAR(2) DEFAULT NULL,
  `f44` VARCHAR(2) DEFAULT NULL,
  `f45` VARCHAR(2) DEFAULT NULL,
  `f46` VARCHAR(2) DEFAULT NULL,
  `f47` VARCHAR(2) DEFAULT NULL,
  `f48` VARCHAR(2) DEFAULT NULL,
  `f49` VARCHAR(2) DEFAULT NULL,
  `f51` VARCHAR(2) DEFAULT NULL,
  `f52` VARCHAR(2) DEFAULT NULL,
  `f53` VARCHAR(2) DEFAULT NULL,
  `f54` VARCHAR(2) DEFAULT NULL,
  `f55` VARCHAR(2) DEFAULT NULL,
  `f56` VARCHAR(2) DEFAULT NULL,
  `f57` VARCHAR(2) DEFAULT NULL,
  `f58` VARCHAR(2) DEFAULT NULL,
  `f59` VARCHAR(2) DEFAULT NULL,
  `f61` VARCHAR(2) DEFAULT NULL,
  `f62` VARCHAR(2) DEFAULT NULL,
  `f63` VARCHAR(2) DEFAULT NULL,
  `f64` VARCHAR(2) DEFAULT NULL,
  `f65` VARCHAR(2) DEFAULT NULL,
  `f66` VARCHAR(2) DEFAULT NULL,
  `f67` VARCHAR(2) DEFAULT NULL,
  `f68` VARCHAR(2) DEFAULT NULL,
  `f69` VARCHAR(2) DEFAULT NULL,
  `f71` VARCHAR(2) DEFAULT NULL,
  `f72` VARCHAR(2) DEFAULT NULL,
  `f73` VARCHAR(2) DEFAULT NULL,
  `f74` VARCHAR(2) DEFAULT NULL,
  `f75` VARCHAR(2) DEFAULT NULL,
  `f76` VARCHAR(2) DEFAULT NULL,
  `f77` VARCHAR(2) DEFAULT NULL,
  `f78` VARCHAR(2) DEFAULT NULL,
  `f79` VARCHAR(2) DEFAULT NULL,
  `f81` VARCHAR(2) DEFAULT NULL,
  `f82` VARCHAR(2) DEFAULT NULL,
  `f83` VARCHAR(2) DEFAULT NULL,
  `f84` VARCHAR(2) DEFAULT NULL,
  `f85` VARCHAR(2) DEFAULT NULL,
  `f86` VARCHAR(2) DEFAULT NULL,
  `f87` VARCHAR(2) DEFAULT NULL,
  `f88` VARCHAR(2) DEFAULT NULL,
  `f89` VARCHAR(2) DEFAULT NULL,
  `gpass` VARCHAR(20) DEFAULT NULL COMMENT '비밀번호 (평문 — 레거시 호환)',
  `gmemo` VARCHAR(14) DEFAULT NULL COMMENT 'timestamp YYYYMMDDHHMMSS',
  PRIMARY KEY (`id`),
  KEY `idx_gcode` (`gcode`),
  KEY `idx_hcode_gcode` (`hcode`, `gcode`)
) ENGINE=InnoDB DEFAULT CHARSET=euckr;

-- (정본 스키마 교체 시 위러브 운영 테이블 80+ 개가 모두 추가됩니다.
--  본 스켈레톤은 인증/RBAC 기본 동작만 보장하기 위한 임시 시드입니다.)
