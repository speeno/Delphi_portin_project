import Image from "next/image";

import { cn } from "@/lib/utils";

/**
 * 사이드바 등 심볼 전용 — 운영 `Logo` 의 symbol 과 동일 자산
 * (`/public/marketing/bukio-symbol-mark.png`, 말풍선형 b).
 */
export function LogoMark({ className }: { className?: string }) {
  return (
    <span
      className={cn("relative inline-block size-10 shrink-0", className)}
      aria-hidden
      data-sample="logo-mark"
    >
      <Image
        src="/marketing/bukio-symbol-mark.png"
        alt=""
        fill
        className="object-contain object-center"
        sizes="40px"
      />
    </span>
  );
}
