from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class HtmlRenderer:
    def __init__(self) -> None:
        self.unsupported: list[dict[str, Any]] = []

    def render_form(self, node: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
        css = self._base_css()
        title = self._escape(node.get('caption') or node['name'])
        body = self._render_node(node, is_root=True)
        html = f"""<!doctype html>
<html lang=\"ko\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""
        meta = {
            'form': node['name'],
            'title': node.get('caption') or node['name'],
            'unsupported_controls': self.unsupported,
        }
        return html, css, meta

    def write_outputs(
        self,
        output_dir: str | Path,
        node: dict[str, Any],
        pas_analysis: dict[str, Any] | None = None,
        *,
        unresolved_ids: list[dict[str, Any]] | None = None,
    ) -> None:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        html, css, meta = self.render_form(node)
        if unresolved_ids:
            meta['string_resolution'] = {
                'unresolved_count': len(unresolved_ids),
                'unresolved': unresolved_ids,
            }
        (out / f"{node['name']}.html").write_text(html, encoding='utf-8')
        (out / f"{node['name']}.css").write_text(css, encoding='utf-8')
        (out / f"{node['name']}.form.json").write_text(json.dumps(node, ensure_ascii=False, indent=2), encoding='utf-8')
        (out / f"{node['name']}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
        if pas_analysis is not None:
            (out / f"{node['name']}.pas_analysis.json").write_text(json.dumps(pas_analysis, ensure_ascii=False, indent=2), encoding='utf-8')
        (out / 'unsupported_controls.json').write_text(json.dumps(self.unsupported, ensure_ascii=False, indent=2), encoding='utf-8')

    def _render_node(self, node: dict[str, Any], is_root: bool = False) -> str:
        if not node.get('visible', True):
            return ''
        visual_type = node['visualType']
        render_type = node.get('renderType') or visual_type
        style = self._style(node, is_root)
        attrs = self._attrs(
            node,
            style,
            include_interactive=render_type not in {'checkbox', 'radio'},
            omit_id=render_type in {'checkbox', 'radio'},
        )
        caption = self._nl_to_br(self._escape(node.get('caption') or ''))
        children_html = ''.join(self._render_node(child) for child in node.get('children', []))

        if visual_type == 'unsupported':
            self.unsupported.append({
                'name': node['name'],
                'className': node['className'],
                'renderType': render_type,
                'approximated': bool(node.get('approximated')),
                'reason': 'unsupported_component',
            })
        if render_type in {'input', 'number', 'date'}:
            input_type = {'input': 'text', 'number': 'number', 'date': 'date'}[render_type]
            value = self._escape(str(node.get('text') or node.get('caption') or ''))
            extra = self._readonly_tabindex_attrs(node)
            return f'<input type="{input_type}" {attrs}{extra} value="{value}" />'
        if render_type == 'textarea':
            value = self._escape(str(node.get('text') or ''))
            extra = self._readonly_tabindex_attrs(node)
            return f'<textarea {attrs}{extra}>{value}</textarea>'
        if render_type == 'button':
            return f'<button {attrs}>{caption or self._escape(node["name"])}</button>'
        if render_type == 'label':
            return f'<div {attrs}>{caption}</div>'
        if render_type == 'progress':
            return f'<progress {attrs} max="100" value="25"></progress>'
        if render_type == 'grid':
            return self._render_grid(node, attrs)
        if render_type == 'group':
            return f'<fieldset {attrs}><legend>{caption}</legend>{children_html}</fieldset>'
        if render_type == 'radiogroup':
            return self._render_radiogroup(node, attrs, caption)
        if render_type == 'statusbar':
            return self._render_statusbar(node, attrs)
        if render_type == 'checkbox':
            return self._render_checkbox(node, attrs, caption)
        if render_type == 'radio':
            return self._render_radio(node, attrs, caption)
        if render_type == 'combobox':
            return self._render_combobox(node, attrs)
        if render_type == 'toolbar':
            return self._render_toolbar(node, attrs, children_html)
        if render_type == 'tabcontrol':
            return self._render_tabcontrol(node, attrs)
        if render_type == 'tabsheet':
            return self._render_tabsheet(node, attrs, caption, children_html)
        if render_type == 'image':
            return self._render_image(node, attrs, caption)
        if render_type == 'listview':
            return self._render_listview(node, attrs)
        if render_type == 'listbox':
            return self._render_listbox(node, attrs)
        tag = 'div'
        title_html = caption if render_type in {'form', 'panel'} and caption else ''
        unsupported_badge = ''
        if visual_type == 'unsupported':
            unsupported_badge = (
                f'<span class="legacy-unsupported-badge">{self._escape(node["className"])}'
                f' → {self._escape(str(render_type))}</span>'
            )
        return f'<{tag} {attrs}>{unsupported_badge}{title_html}{children_html}</{tag}>'

    def _render_grid(self, node: dict[str, Any], attrs: str) -> str:
        columns = node.get('gridColumns') or []
        if not columns:
            columns = [{'caption': f'Column {idx+1}', 'field': f'col{idx+1}'} for idx in range(3)]
        headers = ''.join(
            f'<th style="width:{max(48, self._num(col.get("width"), 120))}px">{self._escape(col.get("caption") or col.get("field") or "")}</th>'
            for col in columns
        )
        row_count = max(1, self._num(node.get('varGridRowCount'), 1))
        body_rows = []
        for _ in range(row_count):
            body_rows.append('<tr>' + ''.join('<td></td>' for _ in columns) + '</tr>')
        body = ''.join(body_rows)
        tfoot_cells = []
        has_footer = False
        for col in columns:
            footer = col.get('footer')
            if footer:
                has_footer = True
            tfoot_cells.append(f'<td>{self._escape(str(footer or ""))}</td>')
        tfoot = f'<tfoot><tr>{"".join(tfoot_cells)}</tr></tfoot>' if has_footer else ''
        return f'<table {attrs} role="grid"><thead><tr>{headers}</tr></thead><tbody>{body}</tbody>{tfoot}</table>'

    def _render_checkbox(self, node: dict[str, Any], attrs: str, caption: str) -> str:
        checked_raw = node.get('checked')
        if checked_raw is None:
            checked_raw = node.get('rawProps', {}).get('Checked', False)
        checked = ' checked' if checked_raw else ''
        dis = '' if node.get('enabled', True) else ' disabled'
        tab = self._tabindex_only(node)
        iid = self._escape(node['name'])
        lab = caption or self._escape(node['name'])
        return (
            f'<label {attrs} for="{iid}_cb"><input type="checkbox" id="{iid}_cb" '
            f'class="legacy-control checkbox {self._escape(node["className"])}"{checked}{dis}{tab} /> {lab}</label>'
        )

    def _render_radio(self, node: dict[str, Any], attrs: str, caption: str) -> str:
        checked_raw = node.get('rawProps', {}).get('Checked', False)
        checked = ' checked' if checked_raw else ''
        dis = '' if node.get('enabled', True) else ' disabled'
        tab = self._tabindex_only(node)
        lab = caption or self._escape(node['name'])
        grp = self._escape(node.get('rawProps', {}).get('GroupIndex', node['name']))
        iid = self._escape(node['name'])
        return (
            f'<label {attrs} for="{iid}_rb"><input type="radio" name="delphi-radio-{grp}" '
            f'id="{iid}_rb" class="legacy-control radio {self._escape(node["className"])}"'
            f'{checked}{dis}{tab} /> {lab}</label>'
        )

    def _render_radiogroup(self, node: dict[str, Any], attrs: str, caption: str) -> str:
        items = node.get('radioItems') or []
        cols = max(1, self._num(node.get('radioColumns'), 1))
        dis = '' if node.get('enabled', True) else ' disabled'
        if not items:
            inner = '<div class="legacy-radiogroup-empty">(항목 없음)</div>'
        else:
            cells = []
            for idx, item in enumerate(items):
                rid = f'{node["name"]}_opt{idx}'
                cells.append(
                    f'<label class="legacy-radio-option" for="{self._escape(rid)}">'
                    f'<input type="radio" name="{self._escape(node["name"])}" id="{self._escape(rid)}" value="{idx}"{dis} />'
                    f'<span>{self._escape(str(item))}</span></label>'
                )
            inner = (
                f'<div class="legacy-radiogroup-grid" '
                f'style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:6px 12px;">'
                f'{"".join(cells)}</div>'
            )
        leg = caption or self._escape(node['name'])
        return f'<fieldset {attrs}><legend>{leg}</legend>{inner}</fieldset>'

    def _render_statusbar(self, node: dict[str, Any], attrs: str) -> str:
        panels = node.get('statusPanels') or []
        if not panels:
            return f'<div {attrs} class="legacy-statusbar-empty"></div>'
        parts: list[str] = []
        for idx, p in enumerate(panels):
            w = max(24, self._num(p.get('Width'), 60))
            txt = self._escape(str(p.get('Text') or ''))
            parts.append(
                f'<span class="legacy-status-cell" style="flex:0 0 {w}px;overflow:hidden;'
                f'text-overflow:ellipsis;white-space:nowrap;border-right:1px solid #bfc5cc;padding:0 4px;">{txt}</span>'
            )
        inner = ''.join(parts)
        return f'<div {attrs}>{inner}</div>'

    def _render_combobox(self, node: dict[str, Any], attrs: str) -> str:
        items = node.get('comboboxItems') or []
        text = self._escape(str(node.get('text') or ''))
        dis = '' if node.get('enabled', True) else ' disabled'
        tab = self._tabindex_only(node)
        options = ''.join(
            f'<option value="{self._escape(it)}">{self._escape(it)}</option>'
            for it in items
        )
        if not options:
            options = f'<option value="">{text}</option>'
        return f'<select {attrs}{dis}{tab}>{options}</select>'

    def _render_toolbar(self, node: dict[str, Any], attrs: str, children_html: str) -> str:
        return f'<div {attrs} role="toolbar">{children_html}</div>'

    def _render_tabcontrol(self, node: dict[str, Any], attrs: str) -> str:
        children = node.get('children') or []
        tabs_html: list[str] = []
        panels_html: list[str] = []
        active = node.get('activePage') or ''
        for idx, child in enumerate(children):
            child_rt = child.get('renderType') or child.get('visualType')
            if child_rt == 'tabsheet':
                cap = self._escape(child.get('caption') or child['name'])
                is_active = child['name'] == active or (not active and idx == 0)
                active_cls = ' legacy-tab-active' if is_active else ''
                tabs_html.append(
                    f'<button class="legacy-tab-btn{active_cls}" '
                    f'data-tab="{self._escape(child["name"])}">{cap}</button>'
                )
                display = 'block' if is_active else 'none'
                child_content = ''.join(self._render_node(gc) for gc in child.get('children', []))
                panels_html.append(
                    f'<div class="legacy-tab-panel" data-tab-panel="{self._escape(child["name"])}" '
                    f'style="display:{display};position:relative;width:100%;flex:1;">{child_content}</div>'
                )
            else:
                panels_html.append(self._render_node(child))
        header = f'<div class="legacy-tab-header">{"".join(tabs_html)}</div>'
        body = ''.join(panels_html)
        return f'<div {attrs}>{header}{body}</div>'

    def _render_tabsheet(self, node: dict[str, Any], attrs: str, caption: str, children_html: str) -> str:
        return f'<div {attrs}>{caption}{children_html}</div>'

    def _render_image(self, node: dict[str, Any], attrs: str, caption: str) -> str:
        return (
            f'<div {attrs}>'
            f'<span style="color:#94a3b8;font-size:11px;">[Image: {caption or self._escape(node["name"])}]</span>'
            f'</div>'
        )

    def _render_listview(self, node: dict[str, Any], attrs: str) -> str:
        return f'<div {attrs} role="list"><span style="color:#94a3b8;font-size:11px;">[ListView]</span></div>'

    def _render_listbox(self, node: dict[str, Any], attrs: str) -> str:
        return f'<select {attrs} size="4" style="width:100%;height:100%;"></select>'

    def _attrs(
        self,
        node: dict[str, Any],
        style: str,
        *,
        include_interactive: bool = True,
        omit_id: bool = False,
    ) -> str:
        render_type = node.get('renderType') or node['visualType']
        attrs: dict[str, str] = {
            'class': f'legacy-control {node["visualType"]} {render_type} {node["className"]}',
            'style': style,
            'data-delphi-class': node['className'],
            'data-delphi-render': str(render_type),
        }
        if not omit_id:
            attrs['id'] = node['name']
        if node.get('hint'):
            attrs['title'] = self._escape(node['hint'])
        if include_interactive:
            if not node.get('enabled', True):
                attrs['disabled'] = 'disabled'
            if node.get('tabOrder') is not None and node.get('tabStop', True):
                attrs['tabindex'] = str(node['tabOrder'])
            elif not node.get('tabStop', True):
                attrs['tabindex'] = '-1'
        for event_name, handler_name in node.get('events', {}).items():
            attrs[f'data-delphi-event-{event_name[2:].lower()}'] = str(handler_name)
        for binding_name, binding_value in node.get('bindings', {}).items():
            if isinstance(binding_value, (str, int, float, bool)):
                attrs[f'data-delphi-binding-{binding_name.lower()}'] = self._escape(str(binding_value))
        return ' '.join(f'{key}="{value}"' for key, value in attrs.items())

    def _readonly_tabindex_attrs(self, node: dict[str, Any]) -> str:
        parts: list[str] = []
        if node.get('readOnly'):
            parts.append(' readonly')
        if node.get('tabOrder') is not None and node.get('tabStop', True):
            parts.append(f' tabindex="{node["tabOrder"]}"')
        elif not node.get('tabStop', True):
            parts.append(' tabindex="-1"')
        return ''.join(parts)

    def _tabindex_only(self, node: dict[str, Any]) -> str:
        if node.get('tabOrder') is not None and node.get('tabStop', True):
            return f' tabindex="{node["tabOrder"]}"'
        if not node.get('tabStop', True):
            return ' tabindex="-1"'
        return ''

    def _style(self, node: dict[str, Any], is_root: bool) -> str:
        render_type = node.get('renderType') or node['visualType']
        if is_root:
            pieces = [
                'position:relative',
                f'width:{self._num(node.get("width"), 800)}px',
                f'height:{self._num(node.get("height"), 600)}px',
                f'background:{node.get("color") or "#ececec"}',
                'overflow:hidden',
            ]
        else:
            align = node.get('align')
            if align == 'alClient':
                pieces = ['position:absolute', 'left:1px', 'top:1px', 'right:1px', 'bottom:1px']
            elif align == 'alTop':
                pieces = ['position:absolute', 'left:0', 'top:0', 'right:0', f'height:{self._num(node.get("height"), 28)}px']
            elif align == 'alBottom':
                pieces = ['position:absolute', 'left:0', 'bottom:0', 'right:0', f'height:{self._num(node.get("height"), 28)}px']
            elif align == 'alLeft':
                pieces = ['position:absolute', 'left:0', 'top:0', 'bottom:0', f'width:{self._num(node.get("width"), 120)}px']
            elif align == 'alRight':
                pieces = ['position:absolute', 'right:0', 'top:0', 'bottom:0', f'width:{self._num(node.get("width"), 120)}px']
            else:
                pieces = [
                    'position:absolute',
                    f'left:{self._num(node.get("left"), 0)}px',
                    f'top:{self._num(node.get("top"), 0)}px',
                    f'width:{self._num(node.get("width"), 120)}px',
                    f'height:{self._num(node.get("height"), 28)}px',
                ]
            if node.get('color'):
                pieces.append(f'background:{node["color"]}')
        font_height = node.get('fontHeight')
        if isinstance(font_height, int):
            pieces.append(f'font-size:{max(10, abs(font_height))}px')
        if node.get('fontName'):
            pieces.append(f'font-family:{node["fontName"]}, sans-serif')
        if node.get('fontColor'):
            pieces.append(f'color:{node["fontColor"]}')
        if render_type in {'panel', 'form', 'group', 'radiogroup'}:
            pieces.append('border:1px solid #bfc5cc')
        if render_type == 'statusbar':
            pieces.extend(
                [
                    'border:1px solid #bfc5cc',
                    'background:#ececec',
                    'display:flex',
                    'align-items:stretch',
                    'width:100%',
                    'font-size:11px',
                ]
            )
        if render_type in {'button', 'input', 'number', 'date', 'textarea', 'combobox'}:
            pieces.append('padding:2px 6px')
        if render_type == 'button':
            pieces.extend(['cursor:pointer', 'display:flex', 'align-items:center', 'justify-content:center'])
        if render_type in {'label', 'panel'}:
            pieces.extend(['display:flex', 'align-items:center', 'justify-content:center', 'white-space:pre-line'])
        if render_type == 'toolbar':
            pieces.extend(['display:flex', 'flex-direction:row', 'align-items:center', 'gap:2px', 'background:#ececec', 'border:1px solid #bfc5cc'])
        if render_type == 'tabcontrol':
            pieces.extend(['display:flex', 'flex-direction:column', 'border:1px solid #bfc5cc'])
        if render_type == 'image':
            pieces.extend(['border:1px solid #d1d5db', 'background:#f9fafb', 'display:flex', 'align-items:center', 'justify-content:center'])
        if render_type == 'radiogroup':
            pieces.append('padding:6px 8px')
        return ';'.join(pieces)

    def _base_css(self) -> str:
        return """
body { margin: 0; padding: 24px; font-family: Arial, sans-serif; background: #f5f7fb; }
.legacy-control { box-sizing: border-box; }
.legacy-control.table, table.legacy-control { border-collapse: collapse; background: white; }
.legacy-control th, .legacy-control td, table.legacy-control th, table.legacy-control td { border: 1px solid #a8b0bb; padding: 4px 6px; font-size: 12px; }
.legacy-control thead th { background: #e8eef8; }
.legacy-unsupported { border: 1px dashed #d32f2f; background: #fff5f5; color: #9a1f1f; padding: 4px 6px; }
.legacy-unsupported-badge { position: absolute; left: 2px; top: 2px; font-size: 10px; color: #9a1f1f; background: rgba(255, 245, 245, 0.9); border: 1px dashed #d32f2f; padding: 0 4px; }
button.legacy-control { background: linear-gradient(#fdfdfd, #dfe7ef); border: 1px solid #9aa6b2; }
input.legacy-control, textarea.legacy-control { border: 1px solid #9aa6b2; background: #ffffff; }
.legacy-radio-option { display: flex; align-items: center; gap: 4px; font-size: 12px; cursor: pointer; }
.legacy-radiogroup-empty { color: #64748b; font-size: 12px; padding: 4px; }
.legacy-tab-header { display: flex; gap: 0; background: #dfe7ef; border-bottom: 1px solid #bfc5cc; }
.legacy-tab-btn { padding: 4px 12px; border: 1px solid #bfc5cc; border-bottom: none; background: #ececec; cursor: pointer; font-size: 12px; }
.legacy-tab-btn.legacy-tab-active { background: #ffffff; font-weight: bold; }
""".strip()

    def _escape(self, value: str) -> str:
        return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    def _nl_to_br(self, value: str) -> str:
        return value.replace('\r\n', '<br/>').replace('\n', '<br/>')

    def _num(self, value: Any, default: int) -> int:
        if value is None:
            return default
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, (int, float)):
            return int(value)
        try:
            return int(str(value).strip())
        except (TypeError, ValueError):
            return default
