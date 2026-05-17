"use client";

import type { ReactNode } from "react";

import { SampleHeader } from "@/components/app-shell/sample-header";
import { SampleSidebar } from "@/components/app-shell/sample-sidebar";

export function CmsShell({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <div className="flex min-h-dvh w-full bg-background text-foreground">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-card focus:px-4 focus:py-2 focus:text-sm focus:shadow-lg"
      >
        본문으로 건너뛰기
      </a>
      <SampleSidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <SampleHeader title={title} />
        <main id="main" className="flex-1 overflow-auto px-6 py-6">
          {children}
        </main>
      </div>
    </div>
  );
}
