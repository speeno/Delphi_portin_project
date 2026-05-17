import Image from "next/image";
import Link from "next/link";

import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function LandingHero() {
  return (
    <section className="relative overflow-hidden bg-muted/50">
      <div
        className="pointer-events-none absolute -right-24 top-1/2 size-[min(90vw,520px)] -translate-y-1/2 rounded-[32%] bg-[var(--vivid-lime)] opacity-35 blur-3xl"
        aria-hidden
      />
      <div className="relative mx-auto grid max-w-6xl items-center gap-10 px-4 py-14 sm:px-6 lg:grid-cols-2 lg:gap-14 lg:py-20">
        <div className="space-y-6">
          <p className="inline-flex rounded-full border border-border bg-card px-3 py-1 text-xs font-semibold text-muted-foreground shadow-sm">
            도서물류 운영자를 위한 북이오웍스
          </p>
          <h1 className="text-balance text-[28px] font-bold leading-[1.35] tracking-[-0.02em] sm:text-3xl lg:text-4xl">
            책의 흐름을 한 화면에서.
            <span className="block text-muted-foreground lg:mt-2 lg:text-3xl lg:font-bold">
              입고부터 반품까지, 팀이 같은 속도로 움직입니다.
            </span>
          </h1>
          <p className="max-w-xl text-base font-medium text-muted-foreground">
            <a
              href="https://buk.io/"
              className="font-semibold text-link underline-offset-4 hover:underline"
              target="_blank"
              rel="noreferrer"
            >
              buk.io
            </a>{" "}
            브랜드 일러스트와 동일한 라임·블랙 대비를 따르되, 운영 콘솔 구간은
            정보 밀도와 피로도를 우선합니다. 이 페이지는 서비스 소개(마케팅 톤)와
            CMS 레이아웃 데모로 이어지는 허브입니다.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/dashboard"
              className={cn(
                buttonVariants({ variant: "brand-primary", size: "brand" }),
              )}
            >
              운영 콘솔 체험하기
            </Link>
            <Link
              href="/login"
              className={cn(
                buttonVariants({ variant: "outline", size: "default" }),
                "h-11 rounded-[var(--radius-pill)] px-6 text-sm font-semibold",
              )}
            >
              로그인 화면 보기
            </Link>
          </div>
          <p className="text-xs text-muted-foreground">
            가이드: 한 화면에 라임 Primary Filled는 하나만 둡니다. 보조 행동은
            아웃라인·다크 필을 사용합니다.
          </p>
        </div>

        <div className="relative mx-auto w-full max-w-md lg:max-w-none">
          <div className="relative aspect-square overflow-hidden rounded-[clamp(16px,8vw,40px)] border border-border bg-card shadow-[10px_10px_0_0_var(--foreground)]">
            <Image
              src="/marketing/illustration-books-flow.png"
              alt="책과 노트북을 연결하는 북이오 스타일 일러스트"
              fill
              className="object-cover object-center"
              sizes="(min-width: 1024px) 480px, 90vw"
              priority
            />
          </div>
        </div>
      </div>
    </section>
  );
}
