"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookOpen,
  LayoutDashboard,
  ListOrdered,
  LogIn,
  Package,
  Settings,
} from "lucide-react";

import { cn } from "@/lib/utils";

const NAV = [
  { href: "/dashboard", label: "대시보드", icon: LayoutDashboard },
  { href: "/list", label: "목록 · 테이블", icon: ListOrdered },
  { href: "/settings", label: "설정 (예시)", icon: Settings },
] as const;

export function SampleSidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex w-[260px] shrink-0 flex-col border-r border-border bg-sidebar text-sidebar-foreground">
      <div className="flex shrink-0 items-center gap-3 border-b border-border px-4 py-4">
        <span className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-muted ring-1 ring-border">
          <BookOpen className="size-4 shrink-0 text-primary" aria-hidden />
        </span>
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold tracking-tight">
            북이오웍스
          </p>
          <p className="truncate text-[11px] leading-snug text-muted-foreground">
            운영 · 관리
          </p>
          <p className="truncate text-[11px] leading-snug text-muted-foreground">
            도서물류 CMS 샘플
          </p>
        </div>
      </div>

      <nav className="flex-1 space-y-1 p-3" aria-label="주 메뉴">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active =
            pathname === href || pathname.startsWith(`${href}/`);
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors",
                active
                  ? "bg-sidebar-accent text-sidebar-accent-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground",
              )}
            >
              <Icon className="size-6 shrink-0" aria-hidden strokeWidth={2} />
              <span>{label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-border p-3">
        <Link
          href="/login"
          className={cn(
            "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors",
            pathname === "/login"
              ? "bg-sidebar-accent text-sidebar-accent-foreground"
              : "text-muted-foreground hover:bg-muted hover:text-foreground",
          )}
        >
          <LogIn className="size-6 shrink-0" aria-hidden strokeWidth={2} />
          로그인 화면 데모
        </Link>
        <div className="mt-3 flex items-center gap-2 rounded-xl bg-muted/80 px-3 py-2 text-xs text-muted-foreground">
          <Package className="size-4 shrink-0 text-primary" aria-hidden />
          데모 데이터 · API 없음
        </div>
      </div>
    </aside>
  );
}
