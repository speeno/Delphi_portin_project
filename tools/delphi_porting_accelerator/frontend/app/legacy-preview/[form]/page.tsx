import { notFound } from 'next/navigation';

import { Nav } from '@/components/Nav';
import { LegacyFormRenderer } from '@/components/LegacyFormRenderer';
import seak04 from '@/generated/forms/Seak40.form.json';
import subu36 from '@/generated/forms/Sobo36.form.json';

const FORMS = {
  Seak40: seak04,
  Sobo36: subu36,
} as const;

export default function LegacyPreviewPage({ params }: { params: { form: string } }) {
  const { form } = params;
  const selected = FORMS[form as keyof typeof FORMS];

  if (!selected) {
    notFound();
  }

  return (
    <main className="page-shell">
      <Nav />
      <LegacyFormRenderer form={selected as any} />
    </main>
  );
}
