import Link from "next/link";
import { BookOpen } from "lucide-react";

import { Button } from "@/components/ui/button";
import { ColorNotice } from "@/components/ui/color-notice";

export default function LoginPage() {
  return (
    <div className="grid min-h-dvh lg:grid-cols-2">
      <section className="relative hidden flex-col justify-between bg-secondary p-10 text-secondary-foreground lg:flex">
        <div>
          <div className="flex items-center gap-3">
            <span className="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-background/80 ring-1 ring-border">
              <BookOpen className="size-6 text-primary" aria-hidden />
            </span>
            <div>
              <p className="text-lg font-bold tracking-tight">북이오웍스</p>
              <p className="text-sm text-muted-foreground">
                도서물류 운영자 포털
              </p>
            </div>
          </div>
          <h2 className="mt-14 max-w-md text-2xl font-bold leading-snug tracking-tight">
            도서 물류의 흐름을 한곳에서,
            <br />
            출판·유통 업무를 더 빠르게.
          </h2>
          <p className="mt-4 max-w-md text-sm leading-relaxed text-muted-foreground">
            입고·출고부터 청구·입금, 재고·정산까지 — 익숙한 업무를 웹에서
            이어갑니다. 북이오웍스는 복잡한 물류를 한 포털로 정리해, 팀이
            오래 앉아도 부담 덜한 화면으로 일할 수 있게 돕습니다.
          </p>
        </div>
        <ColorNotice title="안내" tone="ok" className="bg-background/70">
          본 화면은 인증 로직 없이 레이아웃만 시연합니다.
        </ColorNotice>
      </section>

      <section className="flex flex-col justify-center px-6 py-12 sm:px-10">
        <div className="mx-auto w-full max-w-md space-y-8">
          <header className="space-y-2 lg:hidden">
            <div className="flex items-center gap-3">
              <span className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-secondary ring-1 ring-border">
                <BookOpen className="size-5 text-primary" aria-hidden />
              </span>
              <p className="text-lg font-bold">북이오웍스</p>
            </div>
          </header>

          <div>
            <h1 className="text-[28px] font-bold leading-[1.5] tracking-[-0.02em]">
              로그인
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              운영 계정으로 접속하여 대시보드를 확인하세요.
            </p>
          </div>

          <form className="space-y-4" aria-label="로그인 폼 데모">
            <label className="flex flex-col gap-2 text-sm font-medium">
              아이디
              <input
                autoComplete="username"
                className="h-11 rounded-[var(--radius-md)] border border-input bg-background px-3 text-sm outline-none ring-ring/50 focus-visible:ring-3"
                placeholder="demo.user"
              />
            </label>
            <label className="flex flex-col gap-2 text-sm font-medium">
              비밀번호
              <input
                type="password"
                autoComplete="current-password"
                className="h-11 rounded-[var(--radius-md)] border border-input bg-background px-3 text-sm outline-none ring-ring/50 focus-visible:ring-3"
                placeholder="••••••••"
              />
            </label>
            <Button
              variant="brand-primary"
              size="brand"
              type="submit"
              className="w-full"
            >
              로그인
            </Button>
            <Button variant="outline" type="button" className="w-full">
              비밀번호 찾기
            </Button>
          </form>

          <p className="text-center text-sm text-muted-foreground">
            <Link href="/" className="font-medium text-link underline-offset-4 hover:underline">
              샘플 안내로 돌아가기
            </Link>
          </p>
        </div>
      </section>
    </div>
  );
}
