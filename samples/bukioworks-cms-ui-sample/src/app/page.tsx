import Link from "next/link";

import { MarketingFooter } from "@/components/marketing/marketing-footer";
import { MarketingHeader } from "@/components/marketing/marketing-header";
import { LandingFeatures } from "@/components/marketing/landing-features";
import { LandingGuideShowcase } from "@/components/marketing/landing-guide-showcase";
import { LandingHero } from "@/components/marketing/landing-hero";
import { LandingReferenceStrip } from "@/components/marketing/landing-reference-strip";
import { LandingVividAlerts } from "@/components/marketing/landing-vivid-alerts";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function HomePage() {
  return (
    <div className="min-h-dvh bg-background text-foreground">
      <MarketingHeader />
      <main>
        <LandingHero />
        <LandingFeatures />
        <LandingGuideShowcase />
        <LandingVividAlerts />
        <LandingReferenceStrip />

        <section className="border-t border-border bg-secondary py-14">
          <div className="mx-auto flex max-w-6xl flex-col items-start gap-6 px-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
            <div className="space-y-2">
              <h2 className="text-xl font-bold tracking-tight">
                운영 화면으로 이동해 패턴을 확인하세요
              </h2>
              <p className="text-sm font-medium text-muted-foreground">
                대시보드·목록·설정 스켈레톤은 CMS 톤(차분한 서피스)을 유지합니다.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Link
                href="/dashboard"
                className={cn(
                  buttonVariants({ variant: "default", size: "default" }),
                  "h-11 rounded-[var(--radius-pill)] px-6 text-sm font-semibold",
                )}
              >
                CMS 대시보드
              </Link>
              <Link
                href="/settings"
                className={cn(
                  buttonVariants({ variant: "outline", size: "default" }),
                  "h-11 rounded-[var(--radius-pill)] px-6 text-sm font-semibold",
                )}
              >
                설정 스켈레톤
              </Link>
            </div>
          </div>
        </section>
      </main>
      <MarketingFooter />
    </div>
  );
}
