import Image from "next/image";

/**
 * buk.io 헤더·풋터 구조를 참고 이미지로 병기합니다 (실제 복제 아님).
 */
export function LandingReferenceStrip() {
  return (
    <section className="border-t border-border bg-muted/30 py-12">
      <div className="mx-auto max-w-6xl space-y-8 px-4 sm:px-6">
        <h2 className="text-lg font-bold text-muted-foreground">
          참고 레이아웃 (buk.io)
        </h2>
        <div className="grid gap-6 md:grid-cols-2">
          <figure className="overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
            <div className="relative aspect-[16/5] w-full bg-background">
              <Image
                src="/marketing/ref-header-bukio.png"
                alt="buk.io 헤더 구조 참고"
                fill
                className="object-cover object-top"
                sizes="(min-width: 768px) 45vw, 100vw"
              />
            </div>
            <figcaption className="px-4 py-3 text-xs text-muted-foreground">
              좌측 로고 · 중앙 탐색 · 우측 유틸리티 링크 패턴을 북이오웍스 마케팅
              헤더에 맞춰 단순화했습니다.
            </figcaption>
          </figure>
          <figure className="overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
            <div className="relative aspect-[16/9] w-full bg-muted">
              <Image
                src="/marketing/ref-footer-bukio.png"
                alt="buk.io 풋터 구조 참고"
                fill
                className="object-contain object-center p-2"
                sizes="(min-width: 768px) 45vw, 100vw"
              />
            </div>
            <figcaption className="px-4 py-3 text-xs text-muted-foreground">
              회색 배경 위 내비게이션과 회사 정보 정렬을 샘플 풋터에 반영했습니다.
            </figcaption>
          </figure>
        </div>
      </div>
    </section>
  );
}
