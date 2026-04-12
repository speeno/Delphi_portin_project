"""
최종 완료 보고서 생성기

프로젝트 전체 결과를 하네스 증거 기반으로 종합한다.

사용법:
  python final_report.py --project-root <path> --output <report_path>
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


def load_json_safe(path: str):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def generate_report(project_root: str) -> dict:
    """프로젝트 전체 결과 보고서를 생성한다."""

    project_data = load_json_safe(os.path.join(project_root, "dashboard", "data", "project.json")) or {}
    sprints_data = load_json_safe(os.path.join(project_root, "dashboard", "data", "sprints.json")) or []
    harness_data = load_json_safe(os.path.join(project_root, "dashboard", "data", "harness.json")) or {}
    deliverables_data = load_json_safe(os.path.join(project_root, "dashboard", "data", "deliverables.json")) or []
    approvals_data = load_json_safe(os.path.join(project_root, "dashboard", "data", "approvals.json")) or []
    risks_data = load_json_safe(os.path.join(project_root, "dashboard", "data", "risks.json")) or []
    ops_status = load_json_safe(os.path.join(project_root, "ops", "harness_ops_status.json")) or {}

    completed_deliverables = sum(1 for d in deliverables_data if d.get("status") == "완료")
    passed_gates = sum(1 for a in approvals_data if a.get("status") == "통과")
    resolved_risks = sum(1 for r in risks_data if r.get("status") == "해소됨")

    harness_layers = harness_data.get("layers", [])
    harness_maturity = {l["id"]: l.get("maturity", "unknown") for l in harness_layers}

    all_ops_converted = all(v.get("status") == "converted" for v in ops_status.values()) if ops_status else False

    report = {
        "report_title": "델파이 도서 물류 시스템 무중단 웹 포팅 - 최종 완료 보고서",
        "generated_at": datetime.now().isoformat(),
        "project_summary": {
            "name": project_data.get("name", ""),
            "start_date": project_data.get("startDate", ""),
            "team_size": sum(t.get("count", 0) for t in project_data.get("team", [])),
            "total_sprints": len(sprints_data),
        },
        "deliverables": {
            "total": len(deliverables_data),
            "completed": completed_deliverables,
            "completion_rate": f"{(completed_deliverables / max(len(deliverables_data), 1)) * 100:.0f}%",
        },
        "approval_gates": {
            "total": len(approvals_data),
            "passed": passed_gates,
            "details": [{"name": a["name"], "status": a["status"]} for a in approvals_data],
        },
        "harness_engineering": {
            "framework": "8계층 하네스 엔지니어링",
            "layers_maturity": harness_maturity,
            "operationalized": all_ops_converted,
            "conversions": {
                "Capture → Audit Log": ops_status.get("capture_to_audit", {}).get("status", "pending"),
                "Comparison → CI 회귀 테스트": ops_status.get("comparison_to_ci", {}).get("status", "pending"),
                "Test → CI/CD 자동 테스트": ops_status.get("test_to_cicd", {}).get("status", "pending"),
                "Routing → Canary 배포": ops_status.get("routing_to_canary", {}).get("status", "pending"),
            },
        },
        "risk_management": {
            "total_risks": len(risks_data),
            "resolved": resolved_risks,
            "remaining": len(risks_data) - resolved_risks,
        },
        "key_achievements": [
            "8계층 하네스 엔지니어링 프레임워크 구축",
            "10대 표준 산출물 생성 파이프라인 자동화",
            "Capture → Test → Compare → Route 통합 파이프라인",
            "5축 평가(Outcome/Process/UI/Efficiency/Variant) 체계 구현",
            "점진적 전환 관리 (0% → 100%) + 즉시 롤백 메커니즘",
            "Go/No-Go 자동 판단 시스템",
            "하네스 → 운영 인프라 전환 (Audit Log/CI/Canary)",
        ],
        "recommendations": [
            "정기적인 회귀 테스트 실행 (CI/CD 파이프라인)",
            "Canary 배포를 통한 안전한 신규 기능 릴리즈",
            "Audit Log 기반 운영 모니터링 강화",
            "Known Unknowns 목록의 지속적 해소",
            "고객사 커스터마이징 설정 기반 전환 완료",
        ],
    }

    return report


def main():
    parser = argparse.ArgumentParser(description="최종 완료 보고서 생성기")
    parser.add_argument("--project-root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    parser.add_argument("--output", default="final_report.json")
    args = parser.parse_args()

    report = generate_report(args.project_root)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"  최종 완료 보고서")
    print(f"{'='*60}")
    print(f"  프로젝트: {report['project_summary']['name']}")
    print(f"  산출물: {report['deliverables']['completed']}/{report['deliverables']['total']} 완료")
    print(f"  승인 게이트: {report['approval_gates']['passed']}/{report['approval_gates']['total']} 통과")
    print(f"  하네스 운영화: {'완료' if report['harness_engineering']['operationalized'] else '진행중'}")
    print(f"  위험: {report['risk_management']['resolved']}/{report['risk_management']['total_risks']} 해소")
    print(f"\n  Report: {args.output}")


if __name__ == "__main__":
    main()
