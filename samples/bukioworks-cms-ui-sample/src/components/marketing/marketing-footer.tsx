import Image from "next/image";
import Link from "next/link";

const FOOTER_LINKS = [
  { href: "#", label: "고객센터" },
  { href: "#", label: "출판사 이용 안내" },
  { href: "#", label: "뷰어 앱 다운로드" },
  { href: "#", label: "이용약관" },
  { href: "#", label: "개인정보처리방침" },
] as const;

/**
 * buk.io 풋터 레이아웃을 참고한 샘플입니다. 실제 법적 문구는 서비스 운영 정책에 맞게 교체합니다.
 */
export function MarketingFooter() {
  return (
    <footer className="border-t border-border bg-muted">
      <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
        <div className="flex flex-col gap-8 lg:flex-row lg:items-start lg:justify-between">
          <div className="space-y-6">
            <Link href="/" className="inline-flex items-center gap-2">
              <span className="relative block h-10 w-10 overflow-hidden rounded-lg bg-[var(--vivid-lime)] ring-1 ring-border">
                <span className="absolute inset-0 flex items-center justify-center text-lg font-black text-primary">
                  b
                </span>
              </span>
              <span className="relative block h-8 w-[120px]">
                <Image
                  src="/marketing/logo-wordmark.png"
                  alt=""
                  fill
                  className="object-contain object-left"
                  sizes="120px"
                />
              </span>
            </Link>
            <nav aria-label="푸터 링크">
              <ul className="flex flex-wrap gap-x-6 gap-y-2">
                {FOOTER_LINKS.map((item) => (
                  <li key={item.label}>
                    <a
                      href={item.href}
                      className="text-sm font-semibold text-foreground hover:text-link"
                    >
                      {item.label}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          </div>

          <div className="flex gap-3 lg:pt-2">
            <a
              href="#"
              className="inline-flex size-10 items-center justify-center rounded-full border border-border bg-background text-muted-foreground hover:text-foreground"
              aria-label="Facebook"
            >
              <svg
                viewBox="0 0 24 24"
                className="size-5"
                fill="currentColor"
                aria-hidden
              >
                <path d="M24 12.073C24 5.446 18.627 0 12 0S0 5.446 0 12.073c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
              </svg>
            </a>
            <a
              href="#"
              className="inline-flex size-10 items-center justify-center rounded-full border border-border bg-background text-muted-foreground hover:text-foreground"
              aria-label="Instagram"
            >
              <svg
                viewBox="0 0 24 24"
                className="size-5"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                aria-hidden
              >
                <rect x="3" y="3" width="18" height="18" rx="5" />
                <circle cx="12" cy="12" r="4" />
                <circle cx="17.5" cy="6.5" r="1.5" fill="currentColor" stroke="none" />
              </svg>
            </a>
          </div>
        </div>

        <hr className="my-8 border-border" />

        <div className="flex flex-col gap-6 text-sm text-muted-foreground">
          <p>
            (주) 북이오 · 사업자등록번호: 123-86-45944 · 통신판매업 신고번호:
            제2025-성남분당B-0364호
          </p>
          <p>
            주소: 경기도 성남시 분당구 황새울로 216 · 문의:{" "}
            <a href="mailto:support@buk.io" className="font-medium text-link">
              support@buk.io
            </a>
          </p>
          <p className="text-xs">© {new Date().getFullYear()} 북이오 All rights reserved.</p>
          <p className="text-xs">
            본 푸터는 샘플 UI이며, 실제 도서물류관리프로그램과 동일하지 않을 수 있습니다.
          </p>
        </div>
      </div>
    </footer>
  );
}
