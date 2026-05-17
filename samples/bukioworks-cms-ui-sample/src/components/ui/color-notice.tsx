import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

type Tone = "info" | "warn" | "ok";

const toneClass: Record<Tone, string> = {
  info: "border-border bg-accent text-accent-foreground",
  warn: "border-border bg-muted text-foreground",
  ok: "border-border bg-secondary text-foreground",
};

/**
 * 가이드 §6.3 Light Section — 운영자 화면에서는 Vivid 대신 Pale Sky·상태 파생 톤으로 안내 블록을 구성합니다.
 */
export function ColorNotice({
  title,
  children,
  tone = "info",
  className,
}: {
  title: string;
  children: ReactNode;
  tone?: Tone;
  className?: string;
}) {
  return (
    <section
      className={cn(
        "rounded-2xl border px-5 py-4 shadow-sm @container",
        toneClass[tone],
        className,
      )}
    >
      <p
        className={cn(
          "text-sm font-semibold",
          tone === "warn" && "text-status-warn",
          tone === "ok" && "text-status-ok",
          (tone === "info" || !tone) && "text-foreground",
        )}
      >
        {title}
      </p>
      <div className="mt-2 text-sm text-muted-foreground">{children}</div>
    </section>
  );
}
