import Image from "next/image";
import Link from "next/link";

import { cn } from "@/lib/utils";

const NAV = [
  { href: "#features", label: "서비스" },
  { href: "#guide", label: "디자인 시스템" },
  { href: "#notice", label: "공지 스타일" },
] as const;

export function MarketingHeader() {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between gap-6 px-4 sm:px-6">
        <Link
          href="/"
          className="flex shrink-0 items-center gap-2"
          aria-label="북이오웍스 홈"
        >
          <span className="relative block h-8 w-[140px] sm:w-[160px]">
            <Image
              src="/marketing/logo-wordmark.png"
              alt="bukio WORKS"
              fill
              className="object-contain object-left"
              sizes="160px"
              priority
            />
          </span>
        </Link>

        <nav
          className="hidden items-center gap-1 md:flex"
          aria-label="주요 섹션"
        >
          {NAV.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="rounded-lg px-3 py-2 text-sm font-semibold text-foreground hover:bg-muted"
            >
              {item.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2 sm:gap-4">
          <Link
            href="/dashboard"
            className={cn(
              "hidden text-sm font-semibold text-link underline-offset-4 hover:underline sm:inline",
            )}
          >
            CMS 체험
          </Link>
          <Link
            href="/login"
            className="text-sm font-semibold text-foreground hover:text-link"
          >
            로그인
          </Link>
        </div>
      </div>
    </header>
  );
}
