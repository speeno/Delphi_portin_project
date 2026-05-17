export function LandingVividAlerts() {
  return (
    <section
      id="notice"
      className="scroll-mt-24 border-t border-border bg-background py-16 sm:py-20"
    >
      <div className="mx-auto max-w-6xl space-y-8 px-4 sm:px-6">
        <header className="max-w-2xl space-y-3">
          <h2 className="text-2xl font-bold tracking-tight">
            공지·경고 표현 (Vivid Section)
          </h2>
          <p className="text-base font-medium text-muted-foreground">
            운영자에게 즉시 주목이 필요할 때만 라임·스카이 배경을 사용합니다.
            일반 본문 배너는 상단 Light Section 규칙을 우선합니다.
          </p>
        </header>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl bg-[var(--vivid-lime)] px-6 py-8 text-center shadow-sm">
            <p className="text-xs font-black uppercase tracking-[0.35em] text-foreground">
              Notice
            </p>
            <p className="mt-4 text-lg font-bold text-foreground">
              새 야간 배치 작업이 등록되었습니다.
            </p>
          </div>
          <div className="rounded-2xl bg-[var(--vivid-sky)] px-6 py-8 text-center shadow-sm">
            <p className="text-xs font-black uppercase tracking-[0.35em] text-foreground">
              Important
            </p>
            <p className="mt-4 text-lg font-bold text-foreground">
              외부 API 점검으로 02:00~03:00 동기화가 지연될 수 있습니다.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
