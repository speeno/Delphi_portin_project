import Link from 'next/link';

const links = [
  { href: '/', label: '홈' },
  { href: '/postcodes', label: 'Seak04 기능 화면' },
  { href: '/pickups', label: 'Subu36 기능 화면' },
  { href: '/legacy-preview/Seak40', label: 'Seak04 원본 폼 미리보기' },
  { href: '/legacy-preview/Sobo36', label: 'Subu36 원본 폼 미리보기' },
];

export function Nav() {
  return (
    <nav className="top-nav">
      {links.map((link) => (
        <Link className="nav-link" key={link.href} href={link.href}>
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
