from dfm2web.models import DfmNode
from dfm2web.normalizer import classify, normalize_node


def test_known_classes_are_supported_visual_types() -> None:
    assert classify('TFlatCheckBox') == 'checkbox'
    assert classify('TCornerButton') == 'button'
    assert classify('TImVarGrid') == 'grid'
    assert classify('TStatusBar') == 'statusbar'
    assert classify('TRadioGroup') == 'radiogroup'


def test_radiogroup_items_strings_filters_property_lines() -> None:
    node = DfmNode(
        kind='object',
        name='RadioGroup1',
        class_name='TRadioGroup',
        props={
            'Left': 10,
            'Top': 6,
            'Width': 250,
            'Height': 175,
            'Caption': '선택항목',
            'Columns': 2,
            'Items.Strings': [
                '거 래 처 코 드',
                '입 고 처 코 드',
                'TabOrder = 0',
                'OnClick = Button201Click',
                '기 타',
            ],
        },
    )
    out = normalize_node(node, is_root=False)
    assert out['visualType'] == 'radiogroup'
    assert out['radioItems'] == ['거 래 처 코 드', '입 고 처 코 드', '기 타']
