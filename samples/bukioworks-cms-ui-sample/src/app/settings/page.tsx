import { CmsShell } from "@/components/app-shell/cms-shell";
import { Button } from "@/components/ui/button";

export default function SettingsPage() {
  return (
    <CmsShell title="설정 (예시)">
      <div className="mx-auto flex max-w-3xl flex-col gap-6">
        <p className="text-sm text-muted-foreground">
          실제 설정 항목 대신 폼 간격·레이블 정렬만 보여 주는 스켈레톤입니다.
        </p>
        <div className="space-y-5 rounded-2xl border border-border bg-card p-6 shadow-sm">
          <label className="flex flex-col gap-2 text-sm font-medium">
            회사 표시 이름
            <input
              type="text"
              defaultValue="북이오웍스 데모창고"
              className="h-11 rounded-[var(--radius-md)] border border-input bg-background px-3 text-sm outline-none ring-ring/50 focus-visible:ring-3"
            />
          </label>
          <label className="flex flex-col gap-2 text-sm font-medium">
            알림 수신 이메일
            <input
              type="email"
              placeholder="ops@example.com"
              className="h-11 rounded-[var(--radius-md)] border border-input bg-background px-3 text-sm outline-none ring-ring/50 focus-visible:ring-3"
            />
          </label>
          <div className="flex flex-wrap gap-3 pt-2">
            <Button variant="outline" type="button">
              취소
            </Button>
            <Button variant="default" type="button">
              저장
            </Button>
          </div>
        </div>
      </div>
    </CmsShell>
  );
}
