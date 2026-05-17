import { Plus, TrendingUp } from "lucide-react";

import { CmsShell } from "@/components/app-shell/cms-shell";
import { Button } from "@/components/ui/button";
import { ColorNotice } from "@/components/ui/color-notice";

export default function DashboardPage() {
  return (
    <CmsShell title="대시보드">
      <div className="mx-auto flex max-w-6xl flex-col gap-8">
        <ColorNotice title="오늘의 운영 포인트" tone="info">
          신규 입고 요청 3건이 확인되었습니다. 목록 화면에서 필터로 상태를
          좁혀 보세요.
        </ColorNotice>

        <section className="grid gap-4 md:grid-cols-3">
          {[
            { label: "처리 대기", value: "12건", hint: "전일 대비 +2" },
            { label: "출고 완료", value: "48건", hint: "목표 대비 96%" },
            { label: "반품 접수", value: "5건", hint: "주의 필요 1건" },
          ].map((card) => (
            <article
              key={card.label}
              className="rounded-2xl border border-border bg-card p-5 shadow-sm"
            >
              <p className="text-sm font-medium text-muted-foreground">
                {card.label}
              </p>
              <p className="mt-2 text-3xl font-bold tracking-tight">
                {card.value}
              </p>
              <p className="mt-2 flex items-center gap-1.5 text-xs text-muted-foreground">
                <TrendingUp className="size-3.5 text-status-ok" aria-hidden />
                {card.hint}
              </p>
            </article>
          ))}
        </section>

        <section className="rounded-2xl border border-dashed border-border bg-muted/40 p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-lg font-bold">빠른 작업</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                가이드에 따라 한 화면에는 라임 Primary Filled 버튼을 하나만 둡니다.
              </p>
            </div>
            <Button variant="brand-primary" size="brand" type="button">
              <Plus className="size-5" aria-hidden />
              새 작업 등록
            </Button>
          </div>
        </section>

        <ColorNotice title="재고 경고" tone="warn">
          특정 로케이션에서 안전재고 미달 SKU 가 감지되었습니다. 목록 화면에서
          열 필터를 사용해 확인할 수 있습니다.
        </ColorNotice>
      </div>
    </CmsShell>
  );
}
