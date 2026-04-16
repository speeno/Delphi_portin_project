import json
from pathlib import Path

from dfm2web.cli import convert_one
from dfm2web.parser import DfmParser


def test_convert_examples(tmp_path: Path) -> None:
    src = Path(__file__).resolve().parents[1] / 'examples' / 'source'
    convert_one(src / 'Seak04.dfm', src / 'Seak04.pas', tmp_path / 'seak04')
    convert_one(src / 'Subu36.dfm', src / 'Subu36.pas', tmp_path / 'subu36')
    assert (tmp_path / 'seak04' / 'Seak40.html').exists()
    assert (tmp_path / 'seak04' / 'Seak40.form.json').exists()
    assert (tmp_path / 'subu36' / 'Sobo36.html').exists()
    assert (tmp_path / 'subu36' / 'Sobo36.form.json').exists()

    seak_form = json.loads((tmp_path / 'seak04' / 'Seak40.form.json').read_text(encoding='utf-8'))
    subu_form = json.loads((tmp_path / 'subu36' / 'Sobo36.form.json').read_text(encoding='utf-8'))

    def walk_names(node: dict) -> set[str]:
        names = {node['name']}
        for child in node.get('children', []):
            names.update(walk_names(child))
        return names

    seak_names = walk_names(seak_form)
    subu_names = walk_names(subu_form)

    assert {'Button101', 'Button102', 'BitBtn101', 'BitBtn102'}.issubset(seak_names)
    assert {'Panel003', 'Panel007'}.issubset(subu_names)

    unsupported = json.loads((tmp_path / 'subu36' / 'unsupported_controls.json').read_text(encoding='utf-8'))
    assert all('renderType' in item for item in unsupported)


def test_parser_handles_end_angle_on_single_line() -> None:
    text = """object F: TForm
  ClientWidth = 320
  ClientHeight = 180
  object Grid1: TDBGridEh
    Left = 8
    Top = 8
    Width = 300
    Height = 120
    Columns = <
      item
        FieldName = 'CODE'
        Title.Caption = '코드'
      end>
  end
  object BtnAfter: TButton
    Left = 8
    Top = 140
    Width = 100
    Height = 24
    Caption = '확인'
  end
end
"""
    root = DfmParser().parse(text)
    assert root.children[0].name == 'Grid1'
    assert root.children[1].name == 'BtnAfter'
