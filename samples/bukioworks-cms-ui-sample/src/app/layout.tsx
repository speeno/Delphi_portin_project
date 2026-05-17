import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "북이오웍스 · 도서물류 운영 샘플",
  description:
    "북이오웍스 디자인 가이드와 buk.io 브랜드 톤을 반영한 소개 페이지 및 CMS 레이아웃 데모",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="min-h-dvh antialiased">{children}</body>
    </html>
  );
}
