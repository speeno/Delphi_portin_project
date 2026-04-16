import json
from pathlib import Path

from dfm2web.cli import batch_convert
from dfm2web.reporting import write_porting_reports


def test_write_porting_reports_creates_files(tmp_path: Path) -> None:
    batch = tmp_path / 'batch'
    f1 = batch / 'FormA'
    f1.mkdir(parents=True)
    form_a = {
        'name': 'FormA',
        'visualType': 'form',
        'renderType': 'form',
        'supported': True,
        'approximated': False,
        'className': 'TFormA',
        'children': [
            {
                'name': 'X1',
                'visualType': 'unsupported',
                'renderType': 'panel',
                'supported': False,
                'approximated': False,
                'className': 'TFoo',
                'events': {'OnClick': 'FooClick'},
                'bindings': {'DataField': 'ID'},
                'children': [],
            },
            {
                'name': 'Y1',
                'visualType': 'panel',
                'renderType': 'panel',
                'supported': True,
                'approximated': False,
                'className': 'TPanel',
                'children': [],
            },
        ],
    }
    (f1 / 'FormA.form.json').write_text(json.dumps(form_a, ensure_ascii=False, indent=2), encoding='utf-8')

    write_porting_reports(batch)
    rep = batch / 'reports'
    assert (rep / 'unsupported_component_ratio.json').exists()
    assert (rep / 'event_binding_coverage.json').exists()
    assert (rep / 'porting_summary.md').exists()
    data = json.loads((rep / 'unsupported_component_ratio.json').read_text(encoding='utf-8'))
    assert data['total_nodes'] == 3
    assert data['unsupported_nodes'] == 1
    assert data['unsupported_class_counts'].get('TFoo') == 1


def test_batch_convert_writes_reports(tmp_path: Path) -> None:
    src = Path(__file__).resolve().parents[1] / 'examples' / 'source'
    batch_convert(src, tmp_path / 'out')
    rep = tmp_path / 'out' / 'reports'
    assert rep.is_dir()
    assert (rep / 'porting_summary.md').exists()
