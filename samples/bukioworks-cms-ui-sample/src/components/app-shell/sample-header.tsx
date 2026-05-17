"use client";

import Link from "next/link";
import { BookOpen } from "lucide-react";

export function SampleHeader({ title }: { title: string }) {
  return (
    <header className="sticky top-0 z-10 flex h-16 shrink-0 items-center justify-between gap-4 border-b border-border bg-background/95 px-6 backdrop-blur-sm">
      <div className="flex min-w-0 items-start gap-2.5">
        <span className="inline-flex size-8 shrink-0 items-center justify-center rounded-xl bg-muted ring-1 ring-border">
          <BookOpen className="size-4 shrink-0 text-primary" aria-hidden />
        </span>
        <div className="min-w-0">
          <p className="truncate text-xs font-medium uppercase tracking-wide text-muted-foreground">
            북이오웍스 · 운영자 화면 레이아웃 샘플
          </p>
          <h1 className="truncate text-xl font-bold tracking-tight">{title}</h1>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <Link
          href="/"
          className="text-sm font-medium text-link underline-offset-4 hover:underline"
        >
          샘플 안내
        </Link>
      </div>
    </header>
  );
}
