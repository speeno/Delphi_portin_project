"""Regression tests for resource-string ID resolution."""

import json
import tempfile
from pathlib import Path

from dfm2web.cli import convert_one
from dfm2web.string_resolve import apply_resource_strings, build_string_id_map


def _make_rc(tmp: Path, entries: dict[int, str]) -> Path:
    lines = ['STRINGTABLE', 'BEGIN']
    for sid, text in entries.items():
        lines.append(f'  {sid}, "{text}"')
    lines.append('END')
    rc = tmp / 'test.rc'
    rc.write_text('\n'.join(lines), encoding='utf-8')
    return rc


def test_apply_resource_strings_replaces_ids():
    id_map = {1001: '확인', 1002: '취소'}
    node = {
        'name': 'Btn1',
        'caption': 1001,
        'text': '',
        'hint': '1002',
        'children': [],
        'gridColumns': [],
    }
    unresolved = apply_resource_strings(node, id_map)
    assert node['caption'] == '확인'
    assert node['hint'] == '취소'
    assert unresolved == []


def test_unresolved_ids_reported():
    id_map = {1001: '확인'}
    node = {
        'name': 'Btn2',
        'caption': 9999,
        'text': '',
        'hint': '',
        'children': [],
        'gridColumns': [],
    }
    unresolved = apply_resource_strings(node, id_map)
    assert len(unresolved) == 1
    assert unresolved[0]['value'] == 9999
    assert unresolved[0]['field'] == 'caption'


def test_grid_column_caption_resolved():
    id_map = {2001: '코드', 2002: '이름'}
    node = {
        'name': 'Grid1',
        'caption': '',
        'text': '',
        'hint': '',
        'gridColumns': [
            {'caption': 2001, 'field': 'code'},
            {'caption': 2002, 'field': 'name'},
            {'caption': '정적캡션', 'field': 'static'},
        ],
        'children': [],
    }
    apply_resource_strings(node, id_map)
    assert node['gridColumns'][0]['caption'] == '코드'
    assert node['gridColumns'][1]['caption'] == '이름'
    assert node['gridColumns'][2]['caption'] == '정적캡션'


def test_build_string_id_map_from_rc_file():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        rc = _make_rc(tmp, {100: '안녕', 200: '세계'})
        id_map = build_string_id_map([rc])
        assert id_map[100] == '안녕'
        assert id_map[200] == '세계'


def test_convert_one_with_rc(tmp_path: Path):
    """End-to-end: DFM with numeric Caption + .rc → HTML contains resolved text."""
    dfm = tmp_path / 'Test.dfm'
    dfm.write_text(
        'object F: TForm\n'
        '  ClientWidth = 320\n'
        '  ClientHeight = 180\n'
        '  object Btn1: TButton\n'
        '    Left = 8\n'
        '    Top = 8\n'
        '    Width = 100\n'
        '    Height = 30\n'
        '    Caption = 1001\n'
        '  end\n'
        'end\n',
        encoding='utf-8',
    )
    rc = _make_rc(tmp_path, {1001: '확인'})
    rc_map = build_string_id_map([rc])
    out = tmp_path / 'out'
    convert_one(dfm, None, out, rc_id_map=rc_map)
    html = (out / 'F.html').read_text(encoding='utf-8')
    assert '확인' in html
    assert '1001' not in html

    meta = json.loads((out / 'F.meta.json').read_text(encoding='utf-8'))
    assert 'string_resolution' not in meta or meta['string_resolution']['unresolved_count'] == 0


def test_convert_one_without_rc_is_unchanged(tmp_path: Path):
    """Without --rc, numeric captions pass through unchanged (regression-safe)."""
    dfm = tmp_path / 'Test2.dfm'
    dfm.write_text(
        'object G: TForm\n'
        '  ClientWidth = 200\n'
        '  ClientHeight = 100\n'
        '  object Lbl1: TLabel\n'
        '    Left = 4\n'
        '    Top = 4\n'
        '    Width = 80\n'
        '    Height = 20\n'
        '    Caption = 5555\n'
        '  end\n'
        'end\n',
        encoding='utf-8',
    )
    out = tmp_path / 'out2'
    convert_one(dfm, None, out)
    html = (out / 'G.html').read_text(encoding='utf-8')
    assert '5555' in html
