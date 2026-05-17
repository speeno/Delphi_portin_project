import Image from "next/image";

export function LandingGuideShowcase() {
  return (
    <section
      id="guide"
      className="scroll-mt-24 border-t border-border bg-muted/40 py-16 sm:py-20"
    >
      <div className="mx-auto max-w-6xl space-y-10 px-4 sm:px-6">
        <header className="max-w-3xl space-y-3">
          <h2 className="text-2xl font-bold tracking-tight">
            디자인 가이드와의 정렬
          </h2>
          <p className="text-base font-medium text-muted-foreground">
            아래 산출물은 저장소의{" "}
            <code className="rounded-md bg-card px-1.5 py-0.5 text-sm text-foreground ring-1 ring-border">
              docs/Design.md
            </code>{" "}
            및 PDF 원본과 같은 규칙을 시각적으로 요약합니다. CMS 화면에서는
            Vivid 사용을 최소화합니다.
          </p>
        </header>

        <div className="grid gap-6 lg:grid-cols-2">
          <figure className="overflow-hidden rounded-3xl border border-border bg-card shadow-sm">
            <div className="relative aspect-[16/10] w-full bg-secondary">
              <Image
                src="/marketing/guide-light-vivid.png"
                alt="Light Section과 Vivid Section 비교 가이드"
                fill
                className="object-contain p-4"
                sizes="(min-width: 1024px) 40vw, 90vw"
              />
            </div>
            <figcaption className="border-t border-border px-5 py-4 text-sm text-muted-foreground">
              Light Section은 안내·본문, Vivid Section은 NOTICE / IMPORTANT 한정.
            </figcaption>
          </figure>

          <figure className="overflow-hidden rounded-3xl border border-border bg-card shadow-sm">
            <div className="relative aspect-[16/10] w-full bg-secondary">
              <Image
                src="/marketing/guide-buttons.png"
                alt="Primary·Secondary 버튼 가이드"
                fill
                className="object-contain p-4"
                sizes="(min-width: 1024px) 40vw, 90vw"
              />
            </div>
            <figcaption className="border-t border-border px-5 py-4 text-sm text-muted-foreground">
              라임 필은 화면당 하나, 보조는 다크 필·아웃라인으로 위계를 만듭니다.
            </figcaption>
          </figure>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <figure className="overflow-hidden rounded-3xl border border-border bg-card shadow-sm">
            <div className="relative aspect-[16/10] w-full bg-background">
              <Image
                src="/marketing/icons-outline.png"
                alt="24×24 라인 아이콘 세트"
                fill
                className="object-contain object-center p-4"
                sizes="(min-width: 1024px) 45vw, 100vw"
              />
            </div>
            <figcaption className="border-t border-border px-5 py-4 text-sm text-muted-foreground">
              라인 아이콘은 표준 두께를 유지합니다.
            </figcaption>
          </figure>
          <figure className="overflow-hidden rounded-3xl border border-border bg-card shadow-sm">
            <div className="relative aspect-[16/10] w-full bg-background">
              <Image
                src="/marketing/icons-solid.png"
                alt="24×24 솔리드 아이콘 세트"
                fill
                className="object-contain object-center p-4"
                sizes="(min-width: 1024px) 45vw, 100vw"
              />
            </div>
            <figcaption className="border-t border-border px-5 py-4 text-sm text-muted-foreground">
              선택·강조 상태는 솔리드 변형으로 구분합니다.
            </figcaption>
          </figure>
        </div>
      </div>
    </section>
  );
}
