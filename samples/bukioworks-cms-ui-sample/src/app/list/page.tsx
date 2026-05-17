import { Filter, Search } from "lucide-react";

import { CmsShell } from "@/components/app-shell/cms-shell";
import { Button } from "@/components/ui/button";

const ROWS = [
  { id: "BK-10293", title: "혁신의 길", qty: 120, stage: "출고준비" },
  { id: "BK-20411", title: "물류 최적화 실무", qty: 44, stage: "입고검수" },
  { id: "BK-30502", title: "재고관리 개론", qty: 18, stage: "반품접수" },
];

export default function ListPage() {
  return (
    <CmsShell title="목록 · 테이블">
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <section
          className="rounded-2xl border border-border bg-card p-4 shadow-sm"
          aria-label="검색 및 필터"
        >
          <div className="flex flex-col gap-3 lg:flex-row lg:items-end">
            <div className="grid flex-1 gap-3 sm:grid-cols-2">
              <label className="flex flex-col gap-1.5 text-sm font-medium">
                키워드
                <span className="relative">
                  <Search
                    className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
                    aria-hidden
                  />
                  <input
                    type="search"
                    placeholder="도서명 · 코드"
                    className="h-11 w-full rounded-[var(--radius-md)] border border-input bg-background pl-10 pr-3 text-sm outline-none ring-ring/50 focus-visible:ring-3"
                  />
                </span>
              </label>
              <label className="flex flex-col gap-1.5 text-sm font-medium">
                진행 단계
                <select className="h-11 w-full rounded-[var(--radius-md)] border border-input bg-background px-3 text-sm outline-none ring-ring/50 focus-visible:ring-3">
                  <option value="">전체</option>
                  <option value="prep">출고준비</option>
                  <option value="recv">입고검수</option>
                  <option value="ret">반품접수</option>
                </select>
              </label>
            </div>
            <div className="flex shrink-0 gap-2">
              <Button variant="default" type="button">
                조회
              </Button>
              <Button variant="outline" type="button">
                <Filter className="size-4" aria-hidden />
                고급 필터
              </Button>
            </div>
          </div>
          <p className="mt-3 text-xs text-muted-foreground">
            입력 필드는 가이드의 radius-md 를 따릅니다. 조회는 다크 필·아웃라인을
            함께 두어 주요 CTA 와 구분합니다.
          </p>
        </section>

        <div className="overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
          <table className="w-full border-collapse text-left text-sm">
            <thead>
              <tr className="bg-muted text-muted-foreground">
                <th scope="col" className="px-4 py-3 font-semibold">
                  코드
                </th>
                <th scope="col" className="px-4 py-3 font-semibold">
                  도서명
                </th>
                <th scope="col" className="px-4 py-3 font-semibold text-right">
                  수량
                </th>
                <th scope="col" className="px-4 py-3 font-semibold">
                  단계
                </th>
              </tr>
            </thead>
            <tbody>
              {ROWS.map((row) => (
                <tr
                  key={row.id}
                  className="border-t border-border hover:bg-muted/40"
                >
                  <td className="px-4 py-3 font-mono text-xs">{row.id}</td>
                  <td className="px-4 py-3">{row.title}</td>
                  <td className="px-4 py-3 text-right tabular-nums">{row.qty}</td>
                  <td className="px-4 py-3 text-muted-foreground">{row.stage}</td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr className="border-t border-border bg-secondary text-secondary-foreground">
                <td className="px-4 py-3 font-semibold" colSpan={2}>
                  합계
                </td>
                <td className="px-4 py-3 text-right text-base font-bold tabular-nums">
                  182
                </td>
                <td className="px-4 py-3 text-muted-foreground">데모 합산</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </CmsShell>
  );
}
