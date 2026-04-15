object Sobo46: TSobo46
  Left = 2338
  Top = 189
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '청구서출력'
  ClientHeight = 606
  ClientWidth = 964
  Color = clBtnFace
  Font.Charset = HANGEUL_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = '굴림'
  Font.Style = [fsBold]
  FormStyle = fsMDIChild
  OldCreateOrder = False
  Position = poMainFormCenter
  Visible = True
  OnActivate = FormActivate
  OnClose = FormClose
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 12
  object Panel200: TFlatPanel
    Left = -27
    Top = 284
    Width = 991
    Height = 288
    Color = clInfoBk
    Visible = False
    TabOrder = 4
    UseDockManager = True
    object Button301: TFlatButton
      Left = 912
      Top = 64
      Width = 73
      Height = 30
      Color = clLime
      Caption = '저장'
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000120B0000120B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333000000
        000033333377777777773333330FFFFFFFF03FF3FF7FF33F3FF700300000FF0F
        00F077F777773F737737E00BFBFB0FFFFFF07773333F7F3333F7E0BFBF000FFF
        F0F077F3337773F3F737E0FBFBFBF0F00FF077F3333FF7F77F37E0BFBF00000B
        0FF077F3337777737337E0FBFBFBFBF0FFF077F33FFFFFF73337E0BF0000000F
        FFF077FF777777733FF7000BFB00B0FF00F07773FF77373377373330000B0FFF
        FFF03337777373333FF7333330B0FFFF00003333373733FF777733330B0FF00F
        0FF03333737F37737F373330B00FFFFF0F033337F77F33337F733309030FFFFF
        00333377737FFFFF773333303300000003333337337777777333}
      Layout = blGlyphLeft
      NumGlyphs = 2
      ParentColor = False
      TabOrder = 62
    end
    object CheckBox1: TFlatCheckBox
      Left = 920
      Top = 37
      Width = 57
      Height = 25
      Caption = '출판사Show'
      Color = clInfoBk
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 72
      TabStop = True
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel201: TFlatPanel
      Left = 8
      Top = 30
      Width = 65
      Height = 12
      Caption = '당월총'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 46
      UseDockManager = True
    end
    object Panel210: TFlatPanel
      Left = 504
      Top = 31
      Width = 65
      Height = 21
      Caption = '반품정리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 55
      UseDockManager = True
    end
    object Panel202: TFlatPanel
      Left = 8
      Top = 62
      Width = 65
      Height = 12
      Caption = '배송'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 47
      UseDockManager = True
    end
    object Panel204: TFlatPanel
      Left = 8
      Top = 127
      Width = 65
      Height = 22
      Caption = '지방부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 49
      UseDockManager = True
    end
    object Edit201: TFlatNumber
      Left = 75
      Top = 31
      Width = 78
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 0
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit208: TFlatNumber
      Left = 75
      Top = 127
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 8
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit209: TFlatNumber
      Left = 130
      Top = 127
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 9
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit210: TFlatNumber
      Left = 164
      Top = 127
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 10
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit202: TFlatNumber
      Left = 75
      Top = 63
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 2
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit203: TFlatNumber
      Left = 130
      Top = 63
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clInactiveBorder
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 3
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit204: TFlatNumber
      Left = 164
      Top = 63
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 4
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel203: TFlatPanel
      Left = 8
      Top = 95
      Width = 65
      Height = 22
      Caption = '추가부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 48
      UseDockManager = True
    end
    object Edit205: TFlatNumber
      Left = 75
      Top = 95
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 5
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit206: TFlatNumber
      Left = 130
      Top = 95
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 6
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit207: TFlatNumber
      Left = 164
      Top = 95
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 7
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit231: TFlatNumber
      Left = 571
      Top = 31
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 34
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit232: TFlatNumber
      Left = 626
      Top = 31
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 35
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel4: TFlatPanel
      Left = 8
      Top = 73
      Width = 65
      Height = 12
      Caption = '기본계약'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 67
      UseDockManager = True
    end
    object FlatPanel9: TFlatPanel
      Left = 8
      Top = 41
      Width = 65
      Height = 12
      Caption = '출고부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 73
      UseDockManager = True
    end
    object FlatPanel15: TFlatPanel
      Left = 504
      Top = 94
      Width = 65
      Height = 12
      Caption = '반품재고및'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 79
      UseDockManager = True
    end
    object FlatPanel16: TFlatPanel
      Left = 504
      Top = 105
      Width = 65
      Height = 12
      Caption = '비품관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 80
      UseDockManager = True
    end
    object Edit246: TFlatNumber
      Left = 660
      Top = 95
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 37
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit224: TFlatNumber
      Left = 660
      Top = 31
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 36
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel205: TFlatPanel
      Left = 752
      Top = 95
      Width = 65
      Height = 22
      Caption = '책보호대'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 50
      UseDockManager = True
    end
    object Panel207: TFlatPanel
      Left = 8
      Top = 158
      Width = 65
      Height = 12
      Caption = '발 송 비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 52
      UseDockManager = True
    end
    object Edit217: TFlatNumber
      Left = 75
      Top = 159
      Width = 78
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 11
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel211: TFlatPanel
      Left = 752
      Top = 30
      Width = 65
      Height = 12
      Caption = '거래명세표'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 56
      UseDockManager = True
    end
    object Edit211: TFlatNumber
      Left = 819
      Top = 95
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 28
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit212: TFlatNumber
      Left = 874
      Top = 95
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 29
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit213: TFlatNumber
      Left = 908
      Top = 95
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 30
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit218: TFlatNumber
      Left = 323
      Top = 95
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 12
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit219: TFlatNumber
      Left = 378
      Top = 95
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clActiveBorder
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 13
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit220: TFlatNumber
      Left = 412
      Top = 95
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 14
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit225: TFlatNumber
      Left = 819
      Top = 31
      Width = 78
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 27
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel206: TFlatPanel
      Left = 752
      Top = 127
      Width = 65
      Height = 22
      Caption = '박 스 대'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 51
      UseDockManager = True
    end
    object Edit214: TFlatNumber
      Left = 819
      Top = 127
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 31
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit215: TFlatNumber
      Left = 874
      Top = 127
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 32
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit216: TFlatNumber
      Left = 908
      Top = 127
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 33
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit221: TFlatNumber
      Left = 323
      Top = 127
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 15
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit222: TFlatNumber
      Left = 378
      Top = 127
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 16
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit223: TFlatNumber
      Left = 412
      Top = 127
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 17
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit229: TFlatNumber
      Left = 323
      Top = 31
      Width = 78
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 1
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit233: TFlatNumber
      Left = 323
      Top = 63
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 24
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit234: TFlatNumber
      Left = 378
      Top = 63
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 25
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit235: TFlatNumber
      Left = 412
      Top = 63
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 26
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel2: TFlatPanel
      Left = 8
      Top = 169
      Width = 65
      Height = 12
      Caption = '(택배화물기타)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -9
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 65
      UseDockManager = True
    end
    object FlatPanel3: TFlatPanel
      Left = 752
      Top = 41
      Width = 65
      Height = 12
      Caption = '발행비외'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 66
      UseDockManager = True
    end
    object Edit240: TFlatNumber
      Left = 323
      Top = 159
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 18
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit241: TFlatNumber
      Left = 378
      Top = 159
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clActiveBorder
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 19
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit242: TFlatNumber
      Left = 412
      Top = 159
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 20
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit243: TFlatNumber
      Left = 323
      Top = 191
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 21
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit244: TFlatNumber
      Left = 378
      Top = 191
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 22
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit245: TFlatNumber
      Left = 412
      Top = 191
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 23
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object CheckBox2: TFlatCheckBox
      Left = 408
      Top = 45
      Width = 89
      Height = 17
      Caption = '계약내용조회'
      Color = clInfoBk
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 82
      TabStop = True
      Visible = False
    end
    object CheckBox3: TFlatCheckBox
      Left = 408
      Top = 33
      Width = 89
      Height = 17
      Caption = '계약내용적용'
      Checked = True
      Color = clInfoBk
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clTeal
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 83
      TabStop = True
    end
    object Panel208: TFlatPanel
      Left = 256
      Top = 94
      Width = 65
      Height = 12
      Caption = '⑤입출고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 53
      UseDockManager = True
    end
    object Panel209: TFlatPanel
      Left = 256
      Top = 126
      Width = 65
      Height = 12
      Caption = '⑤-1입출고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 54
      UseDockManager = True
    end
    object Panel215: TFlatPanel
      Left = 256
      Top = 30
      Width = 65
      Height = 12
      Caption = '월말'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 60
      UseDockManager = True
    end
    object Panel217: TFlatPanel
      Left = 256
      Top = 62
      Width = 65
      Height = 12
      Caption = '물류'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 63
      UseDockManager = True
    end
    object FlatPanel1: TFlatPanel
      Left = 256
      Top = 41
      Width = 65
      Height = 12
      Caption = '물류재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 64
      UseDockManager = True
    end
    object FlatPanel5: TFlatPanel
      Left = 256
      Top = 105
      Width = 65
      Height = 12
      Caption = '기본부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 68
      UseDockManager = True
    end
    object FlatPanel6: TFlatPanel
      Left = 256
      Top = 62
      Width = 65
      Height = 12
      Caption = '⑦재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 69
      UseDockManager = True
    end
    object FlatPanel10: TFlatPanel
      Left = 256
      Top = 137
      Width = 65
      Height = 12
      Caption = '초과관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 74
      UseDockManager = True
    end
    object FlatPanel11: TFlatPanel
      Left = 256
      Top = 158
      Width = 65
      Height = 12
      Caption = '⑥재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 75
      UseDockManager = True
    end
    object FlatPanel12: TFlatPanel
      Left = 256
      Top = 169
      Width = 65
      Height = 12
      Caption = '기본부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 76
      UseDockManager = True
    end
    object FlatPanel13: TFlatPanel
      Left = 256
      Top = 190
      Width = 65
      Height = 12
      Caption = '⑥-1재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 77
      UseDockManager = True
    end
    object FlatPanel14: TFlatPanel
      Left = 256
      Top = 201
      Width = 65
      Height = 12
      Caption = '초과관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 78
      UseDockManager = True
    end
    object FlatPanel17: TFlatPanel
      Left = 256
      Top = 73
      Width = 65
      Height = 12
      Caption = '관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 81
      UseDockManager = True
    end
    object Edit247: TFlatNumber
      Left = 571
      Top = 95
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 84
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit248: TFlatNumber
      Left = 626
      Top = 95
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 85
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel21: TFlatPanel
      Left = 8
      Top = 192
      Width = 65
      Height = 21
      Caption = '종당관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 86
      UseDockManager = True
    end
    object Edit261: TFlatNumber
      Left = 75
      Top = 191
      Width = 44
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 87
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit262: TFlatNumber
      Left = 120
      Top = 191
      Width = 43
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 88
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit263: TFlatNumber
      Left = 164
      Top = 191
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 89
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel23: TFlatPanel
      Left = 752
      Top = 64
      Width = 65
      Height = 21
      Caption = '프로그램비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 90
      UseDockManager = True
    end
    object Edit264: TFlatNumber
      Left = 819
      Top = 63
      Width = 44
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 91
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit265: TFlatNumber
      Left = 864
      Top = 63
      Width = 43
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 92
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit266: TFlatNumber
      Left = 908
      Top = 63
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 93
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel24: TFlatPanel
      Left = 672
      Top = 216
      Width = 313
      Height = 66
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = 12056530
      ColorHighLight = clBlack
      ColorShadow = clBlack
      TabOrder = 94
      UseDockManager = True
    end
    object Panel213: TFlatPanel
      Left = 680
      Top = 223
      Width = 65
      Height = 22
      Caption = '당월청구비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 58
      UseDockManager = True
    end
    object Edit227: TFlatNumber
      Left = 747
      Top = 223
      Width = 78
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 42
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel212: TFlatPanel
      Left = 680
      Top = 255
      Width = 65
      Height = 22
      Caption = '전일미수금'
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 57
      UseDockManager = True
    end
    object Edit226: TFlatNumber
      Left = 747
      Top = 255
      Width = 78
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 44
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel216: TFlatPanel
      Left = 832
      Top = 255
      Width = 65
      Height = 22
      Caption = '합계금액'
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 61
      UseDockManager = True
    end
    object Panel214: TFlatPanel
      Left = 832
      Top = 223
      Width = 65
      Height = 22
      Caption = '부가세'
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 59
      UseDockManager = True
    end
    object Edit228: TFlatNumber
      Left = 899
      Top = 223
      Width = 78
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 43
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit230: TFlatNumber
      Left = 899
      Top = 255
      Width = 78
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 45
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel18: TFlatPanel
      Left = 8
      Top = 3
      Width = 233
      Height = 22
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = clLime
      ColorHighLight = clLime
      ColorShadow = clLime
      TabOrder = 95
      UseDockManager = True
      object Label301: TmyLabel3d
        Left = 51
        Top = 3
        Width = 133
        Height = 16
        Caption = '배  송  업  무  비'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -16
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object FlatPanel41: TFlatPanel
      Left = 3
      Top = 216
      Width = 662
      Height = 66
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = 12056530
      ColorHighLight = clBlack
      ColorShadow = clBlack
      TabOrder = 96
      UseDockManager = True
    end
    object FlatPanel7: TFlatPanel
      Left = 8
      Top = 223
      Width = 65
      Height = 22
      Caption = '비고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 70
      UseDockManager = True
    end
    object Edit238: TFlatEdit
      Left = 74
      Top = 223
      Width = 335
      Height = 21
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 40
      ParentFont = False
      TabOrder = 39
    end
    object Edit236: TFlatNumber
      Left = 411
      Top = 223
      Width = 78
      Height = 21
      Digits = 0
      Min = -99999999.000064
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 38
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel8: TFlatPanel
      Left = 8
      Top = 255
      Width = 65
      Height = 22
      Caption = '참고사항'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 71
      UseDockManager = True
    end
    object Edit239: TFlatEdit
      Left = 74
      Top = 255
      Width = 335
      Height = 21
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 40
      ParentFont = False
      TabOrder = 41
    end
    object Edit237: TFlatNumber
      Left = 411
      Top = 255
      Width = 78
      Height = 21
      Digits = 0
      Min = -99999999.000064
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 40
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel19: TFlatPanel
      Left = 256
      Top = 3
      Width = 233
      Height = 22
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = 16744448
      ColorHighLight = 16744448
      ColorShadow = 16744448
      TabOrder = 97
      UseDockManager = True
      object Label302: TmyLabel3d
        Left = 51
        Top = 3
        Width = 133
        Height = 16
        Caption = '물  류  관  리  비'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -16
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object FlatPanel20: TFlatPanel
      Left = 504
      Top = 3
      Width = 233
      Height = 22
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clMaroon
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = 4227327
      ColorHighLight = 4227327
      ColorShadow = 4227327
      TabOrder = 98
      UseDockManager = True
      object myLabel3d1: TmyLabel3d
        Left = 51
        Top = 3
        Width = 133
        Height = 16
        Caption = '반  품  관  리  비'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -16
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object FlatPanel27: TFlatPanel
      Left = 504
      Top = 62
      Width = 65
      Height = 12
      Caption = '②분류해체'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 99
      UseDockManager = True
    end
    object FlatPanel32: TFlatPanel
      Left = 504
      Top = 73
      Width = 65
      Height = 12
      Caption = '및 입력비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 100
      UseDockManager = True
    end
    object Edit301: TFlatNumber
      Left = 571
      Top = 63
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 101
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit302: TFlatNumber
      Left = 626
      Top = 63
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 102
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit303: TFlatNumber
      Left = 660
      Top = 63
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 103
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel33: TFlatPanel
      Left = 504
      Top = 190
      Width = 65
      Height = 12
      Caption = '⑨기타'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 104
      UseDockManager = True
    end
    object FlatPanel35: TFlatPanel
      Left = 504
      Top = 126
      Width = 65
      Height = 12
      Caption = '④시내'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 105
      UseDockManager = True
    end
    object FlatPanel36: TFlatPanel
      Left = 504
      Top = 137
      Width = 65
      Height = 12
      Caption = '수거업무비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 106
      UseDockManager = True
    end
    object FlatPanel37: TFlatPanel
      Left = 504
      Top = 158
      Width = 65
      Height = 12
      Caption = '⑤지방'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 107
      UseDockManager = True
    end
    object FlatPanel38: TFlatPanel
      Left = 504
      Top = 169
      Width = 65
      Height = 12
      Caption = '수거업무비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 108
      UseDockManager = True
    end
    object FlatPanel39: TFlatPanel
      Left = 504
      Top = 201
      Width = 65
      Height = 12
      Caption = '관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 109
      UseDockManager = True
    end
    object Edit304: TFlatNumber
      Left = 571
      Top = 127
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 110
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit305: TFlatNumber
      Left = 626
      Top = 127
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 111
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit309: TFlatNumber
      Left = 660
      Top = 159
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 112
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit306: TFlatNumber
      Left = 660
      Top = 127
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 113
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit307: TFlatNumber
      Left = 571
      Top = 159
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 114
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit308: TFlatNumber
      Left = 626
      Top = 159
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 115
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit310: TFlatNumber
      Left = 571
      Top = 191
      Width = 54
      Height = 21
      Digits = 1
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 116
      Text = '0.0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit311: TFlatNumber
      Left = 626
      Top = 191
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 117
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit312: TFlatNumber
      Left = 660
      Top = 191
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 118
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel26: TFlatPanel
      Left = 752
      Top = 3
      Width = 233
      Height = 22
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = clYellow
      ColorHighLight = clYellow
      ColorShadow = clYellow
      TabOrder = 119
      UseDockManager = True
      object myLabel3d2: TmyLabel3d
        Left = 51
        Top = 3
        Width = 133
        Height = 16
        Caption = '기  타  관  리  비'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -16
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object FlatPanel22: TFlatPanel
      Left = 752
      Top = 158
      Width = 65
      Height = 12
      Caption = '⑨기타'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 120
      UseDockManager = True
    end
    object FlatPanel28: TFlatPanel
      Left = 752
      Top = 169
      Width = 65
      Height = 12
      Caption = '관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 121
      UseDockManager = True
    end
    object Edit313: TFlatNumber
      Left = 819
      Top = 159
      Width = 54
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 122
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit314: TFlatNumber
      Left = 874
      Top = 159
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 123
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit315: TFlatNumber
      Left = 908
      Top = 159
      Width = 77
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 124
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel30: TFlatPanel
      Left = 504
      Top = 223
      Width = 65
      Height = 22
      Caption = '입금일자'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 125
      UseDockManager = True
    end
    object Edit901: TFlatMaskEdit
      Left = 571
      Top = 223
      Width = 89
      Height = 21
      ColorFlat = clWhite
      AutoSize = False
      BorderStyle = bsNone
      Color = clWhite
      EditMask = '!9999.!99.99;1; '
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 10
      ParentFont = False
      TabOrder = 126
      Text = '1999.01.01'
      OnChange = Edit101Change
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Edit902: TFlatNumber
      Left = 571
      Top = 255
      Width = 89
      Height = 21
      Digits = 0
      Min = -99999999.000064
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 127
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel40: TFlatPanel
      Left = 504
      Top = 255
      Width = 65
      Height = 22
      Caption = '전월입금액'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 128
      UseDockManager = True
    end
  end
  object Panel003: TFlatPanel
    Left = 187
    Top = 52
    Width = 777
    Height = 237
    ParentColor = True
    Visible = False
    TabOrder = 3
    UseDockManager = True
    object StBar201: TStatusBar
      Left = 1
      Top = 218
      Width = 775
      Height = 18
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Text = '합계'
          Width = 42
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 600
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 112
        end
        item
          Width = 50
        end>
      ParentFont = True
      SimplePanel = False
      UseSystemFont = False
      Visible = False
    end
    object DBGrid201: TDBGridEh
      Left = 1
      Top = 1
      Width = 775
      Height = 217
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      FooterColor = 8454143
      FooterFont.Charset = HANGEUL_CHARSET
      FooterFont.Color = clWindowText
      FooterFont.Height = -12
      FooterFont.Name = '굴림'
      FooterFont.Style = [fsBold]
      FooterRowCount = 1
      ImeName = '한국어 입력 시스템 (IME 2000)'
      Options = [dgEditing, dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgCancelOnExit]
      ParentFont = False
      ParentShowHint = False
      ShowHint = True
      SumList.Active = True
      SumList.VirtualRecords = True
      TabOrder = 1
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      UseMultiTitle = True
      VTitleMargin = 4
      Columns = <
        item
          Alignment = taCenter
          Color = 12056530
          EditButtons = <>
          FieldName = 'GDATE'
          Footers = <>
          Title.Caption = '일자'
          Width = 30
        end
        item
          EditButtons = <>
          FieldName = 'GQUT1'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '출고내역|시내부수'
          Width = 56
        end
        item
          EditButtons = <>
          FieldName = 'GQUT2'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '출고내역|지방부수'
          Width = 56
          WordWrap = True
        end
        item
          EditButtons = <>
          FieldName = 'GQUT4'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '출고내역|보호대'
          Width = 50
        end
        item
          EditButtons = <>
          FieldName = 'GQUT3'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '출고내역|박스대'
          Width = 50
        end
        item
          EditButtons = <>
          FieldName = 'GQUT5'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '반품내역|총부수'
          Width = 56
        end
        item
          EditButtons = <>
          FieldName = 'NAME1'
          Footers = <>
          Title.Caption = '발송비내역|지역'
          Width = 100
        end
        item
          EditButtons = <>
          FieldName = 'NAME2'
          Footers = <>
          Title.Caption = '발송비내역|화물명'
          Width = 95
        end
        item
          ButtonStyle = cbsNone
          EditButtons = <>
          FieldName = 'GNAME'
          Footers = <>
          Layout = tlCenter
          PickList.Strings = (
            '0')
          ShowImageAndText = True
          Title.Caption = '발송비내역|서점명'
          Width = 100
        end
        item
          Alignment = taCenter
          ButtonStyle = cbsNone
          Checkboxes = False
          EditButtons = <>
          FieldName = 'GSQUT'
          Footers = <>
          PickList.Strings = (
            '1')
          ShowImageAndText = True
          Title.Caption = '발송비내역|건수'
          Width = 30
        end
        item
          ButtonStyle = cbsNone
          Color = 11861755
          EditButtons = <>
          FieldName = 'GSSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          PickList.Strings = (
            '2')
          ShowImageAndText = True
          Title.Caption = '발송비내역|발송비'
          Width = 80
          WordWrap = True
        end
        item
          Checkboxes = True
          EditButtons = <>
          FieldName = 'YESNO'
          Footers = <>
          KeyList.Strings = (
            '1;On'
            '0;Off')
          Title.Caption = '저장'
          Width = 29
        end>
    end
  end
  object Panel001: TFlatPanel
    Left = 2
    Top = 4
    Width = 959
    Height = 45
    Color = 14416873
    TabOrder = 0
    UseDockManager = True
    object Label101: TmyLabel3d
      Left = 564
      Top = 15
      Width = 12
      Height = 15
      Caption = '~'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Panel101: TFlatPanel
      Left = 24
      Top = 12
      Width = 82
      Height = 22
      Caption = '거래일자'
      ParentColor = True
      TabOrder = 4
      UseDockManager = True
    end
    object Button101: TFlatButton
      Left = 904
      Top = 8
      Width = 25
      Height = 25
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000130B0000130B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333333333
        333333333333333333FF33333333333330003FF3FFFFF3333777003000003333
        300077F777773F333777E00BFBFB033333337773333F7F33333FE0BFBF000333
        330077F3337773F33377E0FBFBFBF033330077F3333FF7FFF377E0BFBF000000
        333377F3337777773F3FE0FBFBFBFBFB039977F33FFFFFFF7377E0BF00000000
        339977FF777777773377000BFB03333333337773FF733333333F333000333333
        3300333777333333337733333333333333003333333333333377333333333333
        333333333333333333FF33333333333330003333333333333777333333333333
        3000333333333333377733333333333333333333333333333333}
      NumGlyphs = 2
      TabOrder = 6
      Visible = False
      OnClick = Button101Click
    end
    object Button201: TFlatButton
      Left = 928
      Top = 8
      Width = 25
      Height = 25
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000130B0000130B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333333333
        333333333333333333FF33333333333330003FF3FFFFF3333777003000003333
        300077F777773F333777E00BFBFB033333337773333F7F33333FE0BFBF000333
        330077F3337773F33377E0FBFBFBF033330077F3333FF7FFF377E0BFBF000000
        333377F3337777773F3FE0FBFBFBFBFB039977F33FFFFFFF7377E0BF00000000
        339977FF777777773377000BFB03333333337773FF733333333F333000333333
        3300333777333333337733333333333333003333333333333377333333333333
        333333333333333333FF33333333333330003333333333333777333333333333
        3000333333333333377733333333333333333333333333333333}
      NumGlyphs = 2
      TabOrder = 7
      Visible = False
      OnClick = Button201Click
    end
    object Edit100: TFlatMaskEdit
      Left = 112
      Top = 12
      Width = 97
      Height = 22
      ColorFlat = clWhite
      AutoSize = False
      BorderStyle = bsNone
      Color = clWhite
      EditMask = '!9999.!99;1; '
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 7
      ParentFont = False
      TabOrder = 1
      Text = '2000.01'
      Visible = False
      OnChange = Edit101Change
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Panel105: TFlatPanel
      Left = 256
      Top = 12
      Width = 81
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 5
      UseDockManager = True
    end
    object Edit103: TFlatEdit
      Left = 344
      Top = 12
      Width = 201
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 50
      ParentFont = False
      TabOrder = 3
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit102: TFlatEdit
      Left = 344
      Top = 12
      Width = 57
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 2
      Visible = False
    end
    object Edit105: TFlatEdit
      Left = 576
      Top = 12
      Width = 201
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 50
      ParentFont = False
      TabOrder = 9
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit104: TFlatEdit
      Left = 576
      Top = 12
      Width = 57
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 8
      Visible = False
    end
    object DateEdit1: TDateEdit
      Left = 209
      Top = 12
      Width = 19
      Height = 22
      BorderStyle = bsNone
      ImeName = 'Microsoft IME 2003'
      NumGlyphs = 2
      StartOfWeek = Sun
      TabOrder = 10
      Visible = False
      OnAcceptDate = DateEdit1AcceptDate
      OnButtonClick = DateEdit1ButtonClick
    end
    object Button701: TFlatButton
      Left = 544
      Top = 12
      Width = 20
      Height = 22
      Color = clBtnFace
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000120B0000120B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00555775777777
        57705557757777775FF7555555555555000755555555555F777F555555555550
        87075555555555F7577F5555555555088805555555555F755F75555555555033
        805555555555F755F75555555555033B05555555555F755F75555555555033B0
        5555555555F755F75555555555033B05555555555F755F75555555555033B055
        55555555F755F75555555555033B05555555555F755F75555555555033B05555
        555555F75FF75555555555030B05555555555F7F7F75555555555000B0555555
        5555F777F7555555555501900555555555557777755555555555099055555555
        5555777755555555555550055555555555555775555555555555}
      Layout = blGlyphLeft
      NumGlyphs = 2
      ParentColor = False
      TabOrder = 11
      OnClick = Button701Click
    end
    object Button702: TFlatButton
      Left = 776
      Top = 12
      Width = 20
      Height = 22
      Color = clBtnFace
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000120B0000120B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00555775777777
        57705557757777775FF7555555555555000755555555555F777F555555555550
        87075555555555F7577F5555555555088805555555555F755F75555555555033
        805555555555F755F75555555555033B05555555555F755F75555555555033B0
        5555555555F755F75555555555033B05555555555F755F75555555555033B055
        55555555F755F75555555555033B05555555555F755F75555555555033B05555
        555555F75FF75555555555030B05555555555F7F7F75555555555000B0555555
        5555F777F7555555555501900555555555557777755555555555099055555555
        5555777755555555555550055555555555555775555555555555}
      Layout = blGlyphLeft
      NumGlyphs = 2
      ParentColor = False
      TabOrder = 12
      OnClick = Button702Click
    end
    object Edit101: TFlatComboBox
      Left = 112
      Top = 12
      Width = 97
      Height = 23
      Color = clWindow
      DropDownCount = 9
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ItemHeight = 15
      Items.Strings = (
        '2020.12'
        '2020.11'
        '2020.10'
        '2020.09'
        '2020.08'
        '2020.07'
        '2020.06'
        '2020.05'
        '2020.04'
        '2020.03'
        '2020.02'
        '2020.01'
        '2019.12'
        '2019.11'
        '2019.10'
        '2019.09'
        '2019.08'
        '2019.07'
        '2019.06'
        '2019.05'
        '2019.04'
        '2019.03'
        '2019.02'
        '2019.01'
        '2018.12'
        '2018.11'
        '2018.10'
        '2018.09'
        '2018.08'
        '2018.07'
        '2018.06'
        '2018.05'
        '2018.04'
        '2018.03'
        '2018.02'
        '2018.01'
        '2017.12'
        '2017.11'
        '2017.10'
        '2017.09'
        '2017.08'
        '2017.07'
        '2017.06'
        '2017.05'
        '2017.04'
        '2017.03'
        '2017.02'
        '2017.01'
        '2016.12'
        '2016.11'
        '2016.10'
        '2016.09'
        '2016.08'
        '2016.07'
        '2016.06'
        '2016.05'
        '2016.04'
        '2016.03'
        '2016.02'
        '2016.01'
        '2015.12'
        '2015.11'
        '2015.10'
        '2015.09'
        '2015.08'
        '2015.07'
        '2015.06'
        '2015.05'
        '2015.04'
        '2015.03'
        '2015.02'
        '2015.01'
        '2014.12'
        '2014.11'
        '2014.10'
        '2014.09'
        '2014.08'
        '2014.07'
        '2014.06'
        '2014.05'
        '2014.04'
        '2014.03'
        '2014.02'
        '2014.01'
        '2013.12'
        '2013.11'
        '2013.10'
        '2013.09'
        '2013.08'
        '2013.07'
        '2013.06'
        '2013.05'
        '2013.04'
        '2013.03'
        '2013.02'
        '2013.01'
        '2012.12'
        '2012.11'
        '2012.10'
        '2012.09'
        '2012.08'
        '2012.07'
        '2012.06'
        '2012.05'
        '2012.04'
        '2012.03'
        '2012.02'
        '2012.01'
        '2011.12'
        '2011.11'
        '2011.10'
        '2011.09'
        '2011.08'
        '2011.07'
        '2011.06'
        '2011.05'
        '2011.04'
        '2011.03'
        '2011.02'
        '2011.01'
        '2010.12'
        '2010.11'
        '2010.10'
        '2010.09'
        '2010.08'
        '2010.07'
        '2010.06'
        '2010.05'
        '2010.04'
        '2010.03'
        '2010.02'
        '2010.01'
        '2009.12'
        '2009.11'
        '2009.10'
        '2009.09'
        '2009.08'
        '2009.07'
        '2009.06'
        '2009.05'
        '2009.04'
        '2009.03'
        '2009.02'
        '2009.01'
        '2008.12'
        '2008.11'
        '2008.10'
        '2008.09'
        '2008.08'
        '2008.07'
        '2008.06'
        '2008.05'
        '2008.04'
        '2008.03'
        '2008.02'
        '2008.01'
        '2007.12'
        '2007.11'
        '2007.10'
        '2007.09'
        '2007.08'
        '2007.07'
        '2007.06'
        '2007.05'
        '2007.04'
        '2007.03'
        '2007.02'
        '2007.01')
      ParentFont = False
      TabOrder = 0
      Text = '2010.12'
      ItemIndex = -1
      OnChange = Edit101Change
      OnKeyDown = Edit115KeyDown
      OnKeyPress = Edit115KeyPress
    end
    object dxButton1: TdxButton
      Left = 888
      Top = 8
      Width = 63
      Height = 30
      OnClick = Button101Click
      Caption = '검색'
      TabOrder = 13
      Glyph.Data = {
        36030000424D3603000000000000360000002800000010000000100000000100
        18000000000000030000610B0000610B0000000000000000000099FF99686568
        6666666666666666666666666666666666666666666666666666666666666666
        66183D6064687366666699FF99686568EAEAEA686568666666EAEAEAEAEAEAEA
        EAEAEAEAEAEAEAEAEAEAEAEAEAEA183D604D5A9151719864687399FF99686568
        666666666666666666666666666666666666666666666666666666183D604D5A
        914995E198D8F83C98E499FF99686568C8B3A4FFFFFFFFFFFFFFFFFFFFFFFFFF
        FFFFFFFFFFFFFFFF183D604D5A91468EDD98D8F83C98E466666699FF99686568
        C8B3A4F6F2F0F4EEEBF1EAE6AA8882AA8882AA8882AA88829B949A6394CA98D8
        F83C98E4EAEAEA66666699FF99686568C8B3A4F9F6F5E6D9D3AA8882F6E9C4FF
        EABDFFF2D5FCF5DEAA8882AFB0B63C98E4666666EAEAEA66666699FF99686568
        C8B3A4FCFBFAAA8882EFE0C0FFE1AFFFECCCFFF2DDFFFBF5FDFBF3AA8882FFFF
        FF666666EAEAEA66666699FF99686568C8B3A4FFFFFFAA8882FBECC3FFDBA6FF
        E9C7FFEFD8FFF4E2FFF1D7AA8882FFFFFF666666EAEAEA66666699FF99686568
        C8B3A4FFFFFFAA8882F9EEC9FFE6C2FFDFB3FFE8C6FFEAC9FFE4B2AA8882FFFF
        FF666666EAEAEA66666699FF99686568C8B3A4FFFFFFAA8882E9DCCBFEFEFBFF
        E8C6FFDAA3FFDFA9F9EBC2AA8882FFFFFF666666EAEAEA66666699FF99686568
        C8B3A4FFFFFFF6F2F0AA8882EBE0CEFAEFCAFCEDC3EFE0BFAA8882E6D9D3FFFF
        FF666666EAEAEA66666699FF99686568C8B3A4FFFFFFFFFFFFF6F2F0AA8882AA
        8882AA8882AA8882A16398B17CB1B17CB1663B66E8E7E8663A6699FF99686568
        C8B3A4FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDFDFDB686B5FFFFFFFFFF
        FF663C66666366663A6699FF99686568C8B3A4FFFFFFFFFFFFFFFFFFFFFFFFFF
        FFFFFFFFFFFFFFFFAB74ABB17CB1C096C0663C66663E6666396699FF99686568
        C8B3A4C8B3A4C8B3A4C8B3A4C8B3A4C8B3A4C8B3A4C8B3A4995D86BFA29EC0A4
        9F663C66D3C0D366616699FF9966666667676767676767676767676767676767
        6767676767676767674C67663B66673E67665466666566666666}
    end
  end
  object Panel007: TFlatPanel
    Left = 2
    Top = 574
    Width = 991
    Height = 29
    Color = clInfoBk
    TabOrder = 2
    UseDockManager = True
    object ProgressBar0: TFlatProgressBar
      Left = 424
      Top = 5
      Width = 426
      Height = 19
      Min = 0
      Max = 100
    end
    object Panel008: TFlatPanel
      Left = 8
      Top = 5
      Width = 97
      Height = 19
      Caption = '레코드'
      ParentColor = True
      TabOrder = 0
      UseDockManager = True
    end
    object Panel009: TFlatPanel
      Left = 112
      Top = 5
      Width = 97
      Height = 19
      ParentColor = True
      TabOrder = 1
      UseDockManager = True
    end
    object Panel010: TFlatPanel
      Left = 320
      Top = 5
      Width = 97
      Height = 19
      Caption = '검색진행'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object ProgressBar1: TProgressBar
      Left = 424
      Top = 5
      Width = 425
      Height = 18
      Min = 0
      Max = 100
      TabOrder = 3
    end
  end
  object Panel002: TFlatPanel
    Left = 2
    Top = 52
    Width = 959
    Height = 517
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGridEh
      Left = 1
      Top = 1
      Width = 848
      Height = 515
      Align = alLeft
      BorderStyle = bsNone
      DataSource = DataSource2
      FooterColor = 16311512
      FooterFont.Charset = HANGEUL_CHARSET
      FooterFont.Color = clWindowText
      FooterFont.Height = -12
      FooterFont.Name = '굴림'
      FooterFont.Style = [fsBold]
      ImeName = '한국어 입력 시스템 (IME 2000)'
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnDrawColumnCell = DBGrid101DrawColumnCell
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      Columns = <
        item
          EditButtons = <>
          FieldName = 'HCODE'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '출판사코드'
          Width = 70
        end
        item
          EditButtons = <>
          FieldName = 'HNAME'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '출판사명'
          Width = 230
        end
        item
          EditButtons = <>
          FieldName = 'BNAME'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '전화번호'
          Width = 150
        end
        item
          Alignment = taCenter
          EditButtons = <>
          FieldName = 'GBIGO'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '출력상태'
          Width = 70
        end
        item
          EditButtons = <>
          FieldName = 'GMEMO'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '출력일자'
          Width = 150
        end
        item
          Alignment = taCenter
          EditButtons = <>
          FieldName = 'BCODE'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '저장유무'
          Width = 70
        end
        item
          Checkboxes = True
          EditButtons = <>
          FieldName = 'YESNO'
          Footers = <>
          KeyList.Strings = (
            'O;On'
            'N;Off')
          Title.Alignment = taCenter
          Title.Caption = '선택'
          Width = 70
        end>
    end
    object FlatPanel25: TFlatPanel
      Left = 856
      Top = 1
      Width = 102
      Height = 515
      ParentColor = True
      ColorHighLight = clBtnFace
      ColorShadow = clBtnFace
      Align = alRight
      TabOrder = 1
      UseDockManager = True
      object RadioButton4: TFlatRadioButton
        Left = 32
        Top = 120
        Width = 41
        Height = 81
        Caption = '전체선택'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clWindowText
        Font.Height = -19
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentFont = False
        TabOrder = 0
        OnClick = RadioButton4Click
      end
      object RadioButton5: TFlatRadioButton
        Left = 32
        Top = 216
        Width = 41
        Height = 81
        Caption = '전체해제'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clWindowText
        Font.Height = -19
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentFont = False
        TabOrder = 1
        OnClick = RadioButton5Click
      end
    end
  end
  object DataSource1: TDataSource
    DataSet = T4_Sub61
    OnDataChange = DataSource1DataChange
    Left = 18
    Top = 94
  end
  object DataSource2: TDataSource
    DataSet = T4_Sub62
    OnDataChange = DataSource2DataChange
    Left = 50
    Top = 94
  end
  object T4_Sub61: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 18
    Top = 130
    object T4_Sub61ID: TFloatField
      FieldName = 'ID'
    end
    object T4_Sub61IDNUM: TFloatField
      FieldName = 'IDNUM'
    end
    object T4_Sub61GDATE: TStringField
      FieldName = 'GDATE'
      Size = 10
    end
    object T4_Sub61GCODE: TStringField
      FieldName = 'GCODE'
      Size = 5
    end
    object T4_Sub61GNAME: TStringField
      FieldName = 'GNAME'
      Size = 50
    end
    object T4_Sub61HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object T4_Sub61HNAME: TStringField
      FieldName = 'HNAME'
      Size = 50
    end
    object T4_Sub61NAME1: TStringField
      FieldName = 'NAME1'
      Size = 30
    end
    object T4_Sub61NAME2: TStringField
      FieldName = 'NAME2'
      Size = 30
    end
    object T4_Sub61GQUT1: TFloatField
      FieldName = 'GQUT1'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub61GQUT2: TFloatField
      FieldName = 'GQUT2'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub61GQUT3: TFloatField
      FieldName = 'GQUT3'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub61GQUT4: TFloatField
      FieldName = 'GQUT4'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub61GQUT5: TFloatField
      FieldName = 'GQUT5'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub61GQUT6: TFloatField
      FieldName = 'GQUT6'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub61GQUT7: TFloatField
      FieldName = 'GQUT7'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub61GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub61GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub61YESNO: TStringField
      FieldName = 'YESNO'
      Size = 5
    end
  end
  object T4_Sub62: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 50
    Top = 130
    object T4_Sub62ID: TFloatField
      FieldName = 'ID'
    end
    object T4_Sub62IDNUM: TFloatField
      FieldName = 'IDNUM'
    end
    object T4_Sub62GDATE: TStringField
      FieldName = 'GDATE'
      EditMask = '!0000.!90.90;1; '
      Size = 10
    end
    object T4_Sub62SCODE: TStringField
      FieldName = 'SCODE'
      Size = 1
    end
    object T4_Sub62GCODE: TStringField
      FieldName = 'GCODE'
      Size = 5
    end
    object T4_Sub62GNAME: TStringField
      FieldName = 'GNAME'
      Size = 50
    end
    object T4_Sub62HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object T4_Sub62HNAME: TStringField
      FieldName = 'HNAME'
      Size = 50
    end
    object T4_Sub62OCODE: TStringField
      DisplayWidth = 4
      FieldName = 'OCODE'
      Size = 1
    end
    object T4_Sub62BCODE: TStringField
      FieldName = 'BCODE'
      Size = 10
    end
    object T4_Sub62BNAME: TStringField
      FieldName = 'BNAME'
      Size = 100
    end
    object T4_Sub62GJEJA: TStringField
      FieldName = 'GJEJA'
      Size = 30
    end
    object T4_Sub62GUBUN: TStringField
      FieldName = 'GUBUN'
      Size = 4
    end
    object T4_Sub62JUBUN: TStringField
      FieldName = 'JUBUN'
      Size = 2
    end
    object T4_Sub62PUBUN: TStringField
      FieldName = 'PUBUN'
      Size = 4
    end
    object T4_Sub62TCODE: TStringField
      FieldName = 'TCODE'
      Size = 4
    end
    object T4_Sub62GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub62QSQUT: TFloatField
      FieldName = 'QSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub62GDANG: TFloatField
      FieldName = 'GDANG'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub62GRAT1: TSmallintField
      FieldName = 'GRAT1'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub62GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub62JEAGO: TFloatField
      FieldName = 'JEAGO'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub62GBIGO: TStringField
      FieldName = 'GBIGO'
      Size = 50
    end
    object T4_Sub62YESNO: TStringField
      FieldName = 'YESNO'
      Size = 5
    end
    object T4_Sub62GMEMO: TDateTimeField
      FieldName = 'GMEMO'
    end
  end
end
