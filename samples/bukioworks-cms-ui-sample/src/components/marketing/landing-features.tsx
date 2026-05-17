import Image from "next/image";
import Link from "next/link";
import { BookMarked, PackageSearch, Users } from "lucide-react";

import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const CARDS = [
  {
    title: "재고·입출고 한눈에",
    body: "발주·입고·출고·반품 이벤트를 테이블 중심으로 묶어, 현장과 사무실이 같은 숫자를 봅니다.",
    icon: PackageSearch,
  },
  {
    title: "역할 기반 협업",
    body: "창고·영업·관리자 권한을 분리해 실수를 줄이고, 알림은 가이드의 Vivid 블록 규칙을 따릅니다.",
    icon: Users,
  },
  {
    title: "콘텐츠와 물류 연결",
    body: "도서 메타·바코드·세트 구성 정보를 물류 상태와 인접 배치해 검색 비용을 줄입니다.",
    icon: BookMarked,
  },
] as const;

export function LandingFeatures() {
  return (
    <section
      id="features"
      className="scroll-mt-24 border-t border-border bg-background py-16 sm:py-20"
    >
      <div className="mx-auto max-w-6xl space-y-12 px-4 sm:px-6">
        <header className="max-w-2xl space-y-3">
          <h2 className="text-2xl font-bold tracking-tight">
            왜 북이오웍스인가
          </h2>
          <p className="text-base font-medium text-muted-foreground">
            Light Section 톤(연한 라임·스카이 배경)으로 정보를 나누고, 중요한
            알림만 Vivid로 올립니다. 아이콘 그리드는 가이드의 24×24 라인 기준을
            따릅니다.
          </p>
        </header>

        <div className="grid gap-8 lg:grid-cols-2 lg:items-center">
          <div className="grid gap-4 sm:grid-cols-2">
            <article className="rounded-3xl border border-border bg-secondary p-6 shadow-sm">
              <div className="relative aspect-[4/3] overflow-hidden rounded-2xl bg-card">
                <Image
                  src="/marketing/illustration-collaboration.png"
                  alt="협업과 연결을 표현한 북이오 일러스트"
                  fill
                  className="object-cover"
                  sizes="(min-width: 640px) 45vw, 100vw"
                />
              </div>
              <p className="mt-4 text-sm font-semibold">
                원격과 현장이 같은 목표를 향해
              </p>
              <p className="mt-2 text-sm text-muted-foreground">
                창 위의 하이파이브 장면은 서비스 소개 영역에서 브랜드 감성을
                유지합니다.
              </p>
            </article>
            <article className="rounded-3xl border border-border bg-accent p-6 shadow-sm">
              <div className="relative aspect-[4/3] overflow-hidden rounded-2xl bg-card">
                <Image
                  src="/marketing/illustration-book-home.png"
                  alt="책과 집을 결합한 북이오 일러스트"
                  fill
                  className="object-cover"
                  sizes="(min-width: 640px) 45vw, 100vw"
                />
              </div>
              <p className="mt-4 text-sm font-semibold">
                기록과 물류를 한 구조로
              </p>
              <p className="mt-2 text-sm text-muted-foreground">
                책·창고·데이터를 하나의 화면 언어로 묶는 것이 북이오웍스의 목표입니다.
              </p>
            </article>
          </div>

          <div className="space-y-5">
            {CARDS.map(({ title, body, icon: Icon }) => (
              <article
                key={title}
                className="flex gap-4 rounded-2xl border border-border bg-card p-5 shadow-sm"
              >
                <span className="inline-flex size-12 shrink-0 items-center justify-center rounded-2xl bg-muted">
                  <Icon className="size-6 text-primary" aria-hidden strokeWidth={2} />
                </span>
                <div>
                  <h3 className="text-lg font-bold">{title}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">{body}</p>
                </div>
              </article>
            ))}
            <div className="flex flex-wrap gap-3 pt-2">
              <Link
                href="/list"
                className={cn(
                  buttonVariants({ variant: "default", size: "default" }),
                  "h-11 rounded-[var(--radius-pill)] px-6 text-sm font-semibold",
                )}
              >
                목록·테이블 데모
              </Link>
              <Link
                href="/dashboard"
                className={cn(
                  buttonVariants({ variant: "outline", size: "default" }),
                  "h-11 rounded-[var(--radius-pill)] px-6 text-sm font-semibold",
                )}
              >
                대시보드 이동
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
