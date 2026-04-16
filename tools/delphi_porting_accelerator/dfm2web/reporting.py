"""Aggregate conversion quality reports for a batch output directory."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterator


def _iter_nodes(node: dict[str, Any]) -> Iterator[dict[str, Any]]:
    yield node
    for ch in node.get('children') or []:
        yield from _iter_nodes(ch)


def write_porting_reports(batch_root: Path) -> None:
    """Write reports under ``batch_root/reports/`` for all ``*/<Form>.form.json``."""
    reports = batch_root / 'reports'
    reports.mkdir(parents=True, exist_ok=True)

    per_form: list[dict[str, Any]] = []
    class_unsupported = Counter()
    total_nodes = 0
    unsupported_nodes = 0
    approximated_nodes = 0
    nodes_with_events = 0
    nodes_with_bindings = 0
    total_event_entries = 0
    total_binding_entries = 0

    for sub in sorted(p for p in batch_root.iterdir() if p.is_dir()):
        form_files = list(sub.glob('*.form.json'))
        if not form_files:
            continue
        form_path = form_files[0]
        data = json.loads(form_path.read_text(encoding='utf-8'))
        u_count = 0
        a_count = 0
        n_total = 0
        ev_n = 0
        bd_n = 0
        ev_e = 0
        bd_e = 0
        for n in _iter_nodes(data):
            n_total += 1
            if n.get('visualType') == 'unsupported':
                u_count += 1
                class_unsupported[str(n.get('className', ''))] += 1
            if n.get('approximated'):
                a_count += 1
            ev = n.get('events') or {}
            if ev:
                ev_n += 1
                ev_e += len(ev)
            bd = n.get('bindings') or {}
            if bd:
                bd_n += 1
                bd_e += len(bd)
        ratio = (u_count / n_total) if n_total else 0.0
        per_form.append({
            'folder': sub.name,
            'form_json': str(form_path.relative_to(batch_root)),
            'node_count': n_total,
            'unsupported_node_count': u_count,
            'unsupported_ratio': round(ratio, 4),
            'approximated_node_count': a_count,
            'nodes_with_events': ev_n,
            'event_handler_count': ev_e,
            'nodes_with_bindings': bd_n,
            'binding_key_count': bd_e,
        })
        total_nodes += n_total
        unsupported_nodes += u_count
        approximated_nodes += a_count
        nodes_with_events += ev_n
        nodes_with_bindings += bd_n
        total_event_entries += ev_e
        total_binding_entries += bd_e

    ratio_payload = {
        'batch_root': str(batch_root),
        'form_count': len(per_form),
        'total_nodes': total_nodes,
        'unsupported_nodes': unsupported_nodes,
        'overall_unsupported_ratio': round((unsupported_nodes / total_nodes), 4) if total_nodes else 0.0,
        'approximated_nodes': approximated_nodes,
        'unsupported_class_counts': dict(class_unsupported.most_common()),
        'per_form': per_form,
    }
    (reports / 'unsupported_component_ratio.json').write_text(
        json.dumps(ratio_payload, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )

    coverage = {
        'batch_root': str(batch_root),
        'nodes_with_events': nodes_with_events,
        'total_event_handlers_in_dfm': total_event_entries,
        'nodes_with_bindings': nodes_with_bindings,
        'total_binding_keys_in_dfm': total_binding_entries,
        'note': 'HTML data-delphi-event-* / data-delphi-binding-* mirror these when nodes are rendered visible; '
        'verify with spot checks or DOM tests.',
    }
    (reports / 'event_binding_coverage.json').write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )

    histogram = [
        {'className': cls, 'count': cnt}
        for cls, cnt in class_unsupported.most_common()
    ]
    (reports / 'unsupported_class_histogram.json').write_text(
        json.dumps(histogram, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )

    lines = [
        '# Porting batch summary',
        '',
        f'- Output root: `{batch_root}`',
        f'- Forms: **{len(per_form)}**',
        f'- Total normalized nodes: **{total_nodes}**',
        f'- Unsupported (visual) nodes: **{unsupported_nodes}** '
        f'({ratio_payload["overall_unsupported_ratio"]:.1%})',
        f'- Approximated nodes: **{approximated_nodes}**',
        '',
        '## Top unsupported classes',
        '',
    ]
    for cls, cnt in class_unsupported.most_common(15):
        lines.append(f'- `{cls}`: {cnt}')
    lines.extend([
        '',
        '## Event / binding inventory',
        '',
        f'- Nodes with ≥1 event: **{nodes_with_events}** (handler entries: {total_event_entries})',
        f'- Nodes with ≥1 binding key: **{nodes_with_bindings}** (keys: {total_binding_entries})',
        '',
        'See `reports/unsupported_component_ratio.json` and `reports/event_binding_coverage.json`.',
        '',
    ])
    (reports / 'porting_summary.md').write_text('\n'.join(lines), encoding='utf-8')
