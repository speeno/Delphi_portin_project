import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Delphi Porting Accelerator',
  description: 'DFM 기반 화면을 Next.js/FastAPI로 포팅하기 위한 예시 프로젝트',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
