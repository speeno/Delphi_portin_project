"""Explicit Delphi class → visual/render strategy for dfm2web.

Keeps heuristics in `normalizer` as fallback; this map is the first source of truth
for known legacy/custom controls that need stable web approximations.
"""

from __future__ import annotations

# Merged into normalizer.ALIASES at import time (single place to extend).
EXTRA_ALIASES: dict[str, set[str]] = {
    # --- Tier A: core input / selection ---
    'checkbox': {'TFlatCheckBox'},
    'button': {'TCornerButton', 'TToolButton', 'TSpeedButton'},
    'grid': {'TImVarGrid'},
    'statusbar': {'TStatusBar'},
    'radiogroup': {'TRadioGroup'},
    'number': {'TFlatSpinEditFloat', 'TFlatSpinEditInteger', 'TSpinEdit', 'TUpDown'},
    'radio': {'TFlatRadioButton'},
    'combobox': {'TFlatComboBox', 'TComboBox'},
    'label': {'TStaticText'},
    'group': {'TFlatGroupBox'},
    # --- Tier B: containers / chrome ---
    'toolbar': {'TToolBar'},
    'tabcontrol': {'TPageControl'},
    'tabsheet': {'TTabSheet'},
    'image': {'TImage', 'TPaintBox'},
    'textarea': {'TRxRichEdit', 'TRichEdit'},
    'listview': {'TListView'},
    'listbox': {'TFileListBox', 'TCheckListBox'},
    'panel': {'TWebBrowser', 'TShape'},
}

# Classes that produce no DOM output; kept in form.json / meta only.
EXTRA_NONVISUAL: set[str] = {
    # --- Tier C: non-visual / dialogs ---
    'TImageList', 'TTimer', 'TPopupMenu', 'TMenuItem',
    'TOpenDialog', 'TSaveDialog', 'TFontDialog',
    'TZMySqlQuery',
    'TIdFTP', 'TIdAntiFreeze',
    'TComTerminal', 'TComPort',
    'TEmail',
    # --- Tier D: FastReport ---
    'TfrReport', 'TfrDBDataSet', 'TfrUserDataset',
    'TfrOLEObject', 'TfrRichObject', 'TfrRoundRectObject',
    'TfrCheckBoxObject', 'TfrBarCodeObject', 'TfrShapeObject',
    'TfrDialogControls', 'TfrCrossObject',
    'TfrTextExport', 'TfrCSVExport', 'TfrRTFExport',
    'TfrHTMExport', 'TfrHTML2Export', 'TfrOLEExcelExport',
    'TfrBMPExport', 'TfrJPEGExport', 'TfrTIFFExport',
    'TfrRtfAdvExport',
}
