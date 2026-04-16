from __future__ import annotations

from typing import Any

from .class_strategies import EXTRA_ALIASES, EXTRA_NONVISUAL
from .models import DfmNode


ALIASES = {
    'form': {'TForm'},
    'panel': {'TPanel', 'TFlatPanel'},
    'label': {'TLabel', 'TmyLabel3d'},
    'button': {'TButton', 'TFlatButton', 'TFlatSpeedButton', 'TBitBtn', 'TdxButton'},
    'input': {'TEdit', 'TFlatEdit', 'TFlatMaskEdit'},
    'number': {'TFlatNumber'},
    'date': {'TDateEdit'},
    'textarea': {'TMemo'},
    'checkbox': {'TCheckBox'},
    'radio': {'TRadioButton'},
    'group': {'TGroupBox'},
    'grid': {'TDBGrid', 'TDBGridEh', 'TStringGrid'},
    'progress': {'TProgressBar', 'TFlatProgressBar'},
    'statusbar': set(),
    'radiogroup': set(),
    'combobox': set(),
    'toolbar': set(),
    'tabcontrol': set(),
    'tabsheet': set(),
    'image': set(),
    'listview': set(),
    'listbox': set(),
}

for _vt, _classes in EXTRA_ALIASES.items():
    ALIASES.setdefault(_vt, set()).update(_classes)

NON_VISUAL_PREFIXES = ('TClientDataSet', 'TDataSource', 'TStringField', 'TFloatField', 'TIntegerField')
NON_VISUAL_EXACT: set[str] = set(EXTRA_NONVISUAL)

APPROX_CLASS_ALIASES = {
    'TcxButton': 'button',
    'TcxLabel': 'label',
    'TcxTextEdit': 'input',
    'TcxDateEdit': 'date',
    'TcxMemo': 'textarea',
    'TcxCheckBox': 'checkbox',
    'TcxRadioButton': 'radio',
    'TSplitter': 'panel',
}

COLOR_MAP = {
    'clBtnFace': '#ececec',
    'clInfoBk': '#fdf8d7',
    'clWindowText': '#111111',
    'clBlack': '#000000',
    'clWhite': '#ffffff',
    'clBlue': '#0047ab',
    'clRed': '#c00000',
}


def classify(class_name: str) -> str:
    for visual_type, classes in ALIASES.items():
        if class_name in classes:
            return visual_type
    if class_name in NON_VISUAL_EXACT or class_name.startswith(NON_VISUAL_PREFIXES):
        return 'nonvisual'
    return 'unsupported'


def _to_int(value: Any, default: int) -> int:
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


def _to_bool(value: Any, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    lowered = str(value).strip().lower()
    if lowered in {'false', '0', 'no'}:
        return False
    if lowered in {'true', '1', 'yes'}:
        return True
    return default


def _approximate_render_type(class_name: str) -> tuple[str, str]:
    if class_name in APPROX_CLASS_ALIASES:
        return APPROX_CLASS_ALIASES[class_name], 'class_alias'
    lowered = class_name.lower()
    if 'button' in lowered:
        return 'button', 'name_heuristic'
    if 'label' in lowered:
        return 'label', 'name_heuristic'
    if 'grid' in lowered:
        return 'grid', 'name_heuristic'
    if 'memo' in lowered:
        return 'textarea', 'name_heuristic'
    if 'date' in lowered:
        return 'date', 'name_heuristic'
    if 'check' in lowered:
        return 'checkbox', 'name_heuristic'
    if 'radio' in lowered:
        return 'radio', 'name_heuristic'
    if 'edit' in lowered or 'input' in lowered:
        return 'input', 'name_heuristic'
    if 'progress' in lowered:
        return 'progress', 'name_heuristic'
    if 'group' in lowered:
        return 'group', 'name_heuristic'
    return 'panel', 'fallback_panel'


def _resolve_rendering(class_name: str, is_root: bool) -> tuple[str, str, bool]:
    visual_type = 'form' if is_root else classify(class_name)
    if visual_type == 'unsupported':
        render_type, strategy = _approximate_render_type(class_name)
        return visual_type, render_type, strategy != 'fallback_panel'
    return visual_type, visual_type, False


def _extract_bindings(raw: dict[str, Any]) -> dict[str, Any]:
    important_keys = {
        'DataSource',
        'DataSet',
        'DataField',
        'KeyField',
        'ListField',
        'LookupDataSet',
        'LookupField',
        'LookupKeyFields',
        'LookupResultField',
        'CommandText',
        'SQL',
        'TableName',
        'StoredProcName',
    }
    bindings: dict[str, Any] = {}
    for key, value in raw.items():
        if value in (None, '', [], {}):
            continue
        if key in important_keys or key.startswith('Data'):
            bindings[key] = value
    return bindings


def _is_plausible_radio_item_line(s: str) -> bool:
    s = str(s).strip()
    if not s or len(s) > 120:
        return False
    lowered = s.lower()
    if lowered.startswith('object ') or lowered.startswith('end'):
        return False
    # Reject Delphi property lines accidentally merged into Items.Strings
    if '=' in s:
        before_eq = s.split('=', 1)[0].strip()
        if before_eq and before_eq.replace('_', '').isalnum() and before_eq[0].isalpha():
            return False
    return True


def _extract_radio_items(raw: dict[str, Any]) -> list[str]:
    items = raw.get('Items.Strings')
    if not isinstance(items, list):
        return []
    out: list[str] = []
    for it in items:
        if isinstance(it, str) and _is_plausible_radio_item_line(it):
            out.append(it.strip())
    return out


def _extract_combobox_items(raw: dict[str, Any]) -> list[str]:
    items = raw.get('Items.Strings') or raw.get('Items')
    if not isinstance(items, list):
        return []
    return [str(it).strip() for it in items if isinstance(it, str) and str(it).strip()]


def _extract_status_panels(raw: dict[str, Any]) -> list[dict[str, Any]]:
    panels = raw.get('Panels')
    if not isinstance(panels, list):
        return []
    return [p for p in panels if isinstance(p, dict)]


def _grid_columns_from_imvar(raw: dict[str, Any]) -> list[dict[str, Any]]:
    cols = raw.get('ColumnInfo.Columns')
    if not isinstance(cols, list) or not cols:
        return []
    out: list[dict[str, Any]] = []
    for idx, col in enumerate(cols):
        if not isinstance(col, dict):
            continue
        cap = ''
        caps = col.get('Captions.Strings')
        if isinstance(caps, list):
            for c in caps:
                if isinstance(c, str) and c.strip() and c.strip() not in {'(', ')'}:
                    cap = c.strip()
                    break
        elif isinstance(caps, str) and caps.strip() not in {'(', ')'}:
            cap = caps.strip()
        disp = col.get('Footer.Field.DisplayNullAs')
        if isinstance(disp, str) and disp.strip():
            cap = cap or disp.strip()
        def_cell = _to_int(raw.get('AxisInfo.Horizontal.DefaultCellSize'), 80)
        out.append({
            'field': f'col{idx + 1}',
            'caption': cap or f'Col {idx + 1}',
            'width': _to_int(col.get('Width'), def_cell),
            'footer': col.get('Footer.Value'),
            'footer_type': col.get('Footer.ValueType'),
            'color': col.get('Color'),
        })
    return out


def is_visual(class_name: str) -> bool:
    return classify(class_name) != 'nonvisual'


def _sanitize_raw_props(raw: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, value in raw.items():
        if isinstance(value, str) and len(value) > 240:
            sanitized[key] = value[:240] + "...<trimmed>"
        else:
            sanitized[key] = value
    return sanitized


def normalize_node(node: DfmNode, is_root: bool = False) -> dict[str, Any]:
    visual_type, render_type, approximated = _resolve_rendering(node.class_name, is_root)
    raw = node.props
    width = _to_int(raw.get('ClientWidth') or raw.get('Width'), 120)
    height = _to_int(raw.get('ClientHeight') or raw.get('Height'), 28)
    children_visual = [normalize_node(child) for child in node.children if is_visual(child.class_name)]
    children_nonvisual = [child.to_dict() for child in node.children if not is_visual(child.class_name)]
    events = {key: value for key, value in raw.items() if key.startswith('On')}
    bindings = _extract_bindings(raw)
    columns = []
    if isinstance(raw.get('Columns'), list):
        for col in raw['Columns']:
            columns.append({
                'field': col.get('FieldName'),
                'caption': col.get('Title.Caption') or col.get('FieldName') or '',
                'width': _to_int(col.get('Width'), 120),
                'footer': col.get('Footer.Value'),
                'footer_type': col.get('Footer.ValueType'),
                'color': col.get('Color'),
            })
    if not columns and node.class_name == 'TImVarGrid':
        columns = _grid_columns_from_imvar(raw)
    radio_items = _extract_radio_items(raw) if visual_type == 'radiogroup' else []
    radio_columns = _to_int(raw.get('Columns'), 1) if visual_type == 'radiogroup' else None
    status_panels = _extract_status_panels(raw) if visual_type == 'statusbar' else []
    combobox_items = _extract_combobox_items(raw) if visual_type == 'combobox' else []
    checked = _to_bool(raw.get('Checked', False), False) if visual_type == 'checkbox' else None
    read_only = _to_bool(raw.get('ReadOnly', False), False) if visual_type in {'input', 'number', 'date', 'textarea'} else None
    tab_stop = _to_bool(raw.get('TabStop', True), True)
    var_row_count = _to_int(raw.get('DataRowCount'), 1) if node.class_name == 'TImVarGrid' else None
    var_col_count = _to_int(raw.get('DataColCount'), 0) if node.class_name == 'TImVarGrid' else None
    spin_min = raw.get('MinValue') if visual_type == 'number' else None
    spin_max = raw.get('MaxValue') if visual_type == 'number' else None
    spin_increment = raw.get('Increment') if visual_type == 'number' else None
    active_page = raw.get('ActivePage') if visual_type == 'tabcontrol' else None
    return {
        'name': node.name,
        'kind': node.kind,
        'className': node.class_name,
        'visualType': visual_type,
        'renderType': render_type,
        'approximated': approximated,
        'supported': visual_type != 'unsupported',
        'caption': raw.get('Caption', ''),
        'text': raw.get('Text', ''),
        'hint': raw.get('Hint', ''),
        'left': _to_int(raw.get('Left'), 0),
        'top': _to_int(raw.get('Top'), 0),
        'width': width,
        'height': height,
        'align': raw.get('Align'),
        'visible': _to_bool(raw.get('Visible', True), True),
        'enabled': _to_bool(raw.get('Enabled', True), True),
        'tabStop': tab_stop,
        'tabOrder': raw.get('TabOrder'),
        'checked': checked,
        'readOnly': read_only,
        'radioItems': radio_items,
        'radioColumns': radio_columns,
        'statusPanels': status_panels,
        'comboboxItems': combobox_items,
        'spinMin': spin_min,
        'spinMax': spin_max,
        'spinIncrement': spin_increment,
        'activePage': active_page,
        'varGridRowCount': var_row_count,
        'varGridColCount': var_col_count,
        'color': COLOR_MAP.get(str(raw.get('Color')), raw.get('Color')),
        'fontName': raw.get('Font.Name'),
        'fontHeight': raw.get('Font.Height'),
        'fontColor': COLOR_MAP.get(str(raw.get('Font.Color')), raw.get('Font.Color')),
        'bindings': bindings,
        'rawProps': raw,
        'rawPropsPreview': _sanitize_raw_props(raw),
        'events': events,
        'gridColumns': columns,
        'children': children_visual,
        'nonVisualChildren': children_nonvisual,
    }
