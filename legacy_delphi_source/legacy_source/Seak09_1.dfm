object Seak90: TSeak90
  Left = 192
  Top = 107
  Width = 777
  Height = 274
  BorderIcons = [biSystemMenu]
  Caption = '계약내용'
  Color = clBtnFace
  Font.Charset = HANGEUL_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = '굴림'
  Font.Style = [fsBold]
  FormStyle = fsStayOnTop
  OldCreateOrder = False
  Position = poScreenCenter
  OnClose = FormClose
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 12
  object Panel001: TFlatPanel
    Left = 0
    Top = 8
    Width = 145
    Height = 201
    ParentColor = True
    Visible = False
    TabOrder = 0
    UseDockManager = True
    object Button102: TFlatButton
      Left = 24
      Top = 160
      Width = 105
      Height = 25
      Caption = '취소'
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000130B0000130B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333333333
        333333333333333333333333333333333333333FFF33FF333FFF339993370733
        999333777FF37FF377733339993000399933333777F777F77733333399970799
        93333333777F7377733333333999399933333333377737773333333333990993
        3333333333737F73333333333331013333333333333777FF3333333333910193
        333333333337773FF3333333399000993333333337377737FF33333399900099
        93333333773777377FF333399930003999333337773777F777FF339993370733
        9993337773337333777333333333333333333333333333333333333333333333
        3333333333333333333333333333333333333333333333333333}
      Layout = blGlyphLeft
      NumGlyphs = 2
      TabOrder = 0
      ModalResult = 2
      Visible = False
    end
    object Button101: TFlatButton
      Left = 24
      Top = 80
      Width = 105
      Height = 25
      Caption = '선택'
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000120B0000120B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00555555555555
        555555555555555555555555555555555555555555FF55555555555559055555
        55555555577FF5555555555599905555555555557777F5555555555599905555
        555555557777FF5555555559999905555555555777777F555555559999990555
        5555557777777FF5555557990599905555555777757777F55555790555599055
        55557775555777FF5555555555599905555555555557777F5555555555559905
        555555555555777FF5555555555559905555555555555777FF55555555555579
        05555555555555777FF5555555555557905555555555555777FF555555555555
        5990555555555555577755555555555555555555555555555555}
      Layout = blGlyphLeft
      NumGlyphs = 2
      TabOrder = 1
      ModalResult = 1
      Visible = False
    end
    object BitBtn101: TBitBtn
      Left = 38
      Top = 76
      Width = 75
      Height = 25
      Caption = '저장'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림체'
      Font.Style = [fsBold]
      ModalResult = 1
      ParentFont = False
      TabOrder = 2
      OnClick = BitBtn101Click
      Glyph.Data = {
        DE010000424DDE01000000000000760000002800000024000000120000000100
        0400000000006801000000000000000000001000000010000000000000000000
        80000080000000808000800000008000800080800000C0C0C000808080000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333333333
        3333333333333333333333330000333333333333333333333333F33333333333
        00003333344333333333333333388F3333333333000033334224333333333333
        338338F3333333330000333422224333333333333833338F3333333300003342
        222224333333333383333338F3333333000034222A22224333333338F338F333
        8F33333300003222A3A2224333333338F3838F338F33333300003A2A333A2224
        33333338F83338F338F33333000033A33333A222433333338333338F338F3333
        0000333333333A222433333333333338F338F33300003333333333A222433333
        333333338F338F33000033333333333A222433333333333338F338F300003333
        33333333A222433333333333338F338F00003333333333333A22433333333333
        3338F38F000033333333333333A223333333333333338F830000333333333333
        333A333333333333333338330000333333333333333333333333333333333333
        0000}
      NumGlyphs = 2
    end
    object BitBtn102: TBitBtn
      Left = 38
      Top = 156
      Width = 75
      Height = 25
      Caption = '취소'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림체'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 3
      OnClick = BitBtn102Click
      Kind = bkCancel
    end
  end
  object Panel002: TFlatPanel
    Left = 151
    Top = 8
    Width = 537
    Height = 201
    ParentColor = True
    Visible = False
    TabOrder = 1
    UseDockManager = True
    object Panel101: TFlatPanel
      Left = 8
      Top = 20
      Width = 90
      Height = 22
      Caption = '어음번호'
      ParentColor = True
      TabOrder = 15
      UseDockManager = True
    end
    object Panel103: TFlatPanel
      Left = 8
      Top = 52
      Width = 90
      Height = 22
      Caption = '발행처'
      ParentColor = True
      TabOrder = 17
      UseDockManager = True
    end
    object Panel102: TFlatPanel
      Left = 272
      Top = 20
      Width = 90
      Height = 22
      Caption = '처리코드'
      ParentColor = True
      TabOrder = 16
      UseDockManager = True
    end
    object Panel104: TFlatPanel
      Left = 272
      Top = 52
      Width = 90
      Height = 22
      Caption = '발행인'
      ParentColor = True
      TabOrder = 18
      UseDockManager = True
    end
    object Panel105: TFlatPanel
      Left = 8
      Top = 84
      Width = 90
      Height = 22
      Caption = '발행일자'
      ParentColor = True
      TabOrder = 19
      UseDockManager = True
    end
    object Panel106: TFlatPanel
      Left = 272
      Top = 84
      Width = 90
      Height = 22
      Caption = '받은일자'
      ParentColor = True
      TabOrder = 20
      UseDockManager = True
    end
    object Panel108: TFlatPanel
      Left = 272
      Top = 116
      Width = 90
      Height = 22
      Caption = '지급처'
      ParentColor = True
      TabOrder = 22
      UseDockManager = True
    end
    object Panel107: TFlatPanel
      Left = 8
      Top = 116
      Width = 90
      Height = 22
      Caption = '지급일자'
      ParentColor = True
      TabOrder = 21
      UseDockManager = True
    end
    object Panel109: TFlatPanel
      Left = 8
      Top = 148
      Width = 90
      Height = 22
      Caption = '지급은행'
      ParentColor = True
      TabOrder = 23
      UseDockManager = True
    end
    object Panel110: TFlatPanel
      Left = 272
      Top = 148
      Width = 90
      Height = 22
      Caption = '지급지점'
      ParentColor = True
      TabOrder = 24
      UseDockManager = True
    end
    object Panel112: TFlatPanel
      Left = 272
      Top = 180
      Width = 90
      Height = 22
      Caption = '금액'
      ParentColor = True
      TabOrder = 26
      UseDockManager = True
    end
    object Panel111: TFlatPanel
      Left = 8
      Top = 180
      Width = 90
      Height = 22
      Caption = '만기일자'
      ParentColor = True
      TabOrder = 25
      UseDockManager = True
    end
    object Panel113: TFlatPanel
      Left = 8
      Top = 212
      Width = 90
      Height = 22
      Caption = '할인율'
      ParentColor = True
      TabOrder = 27
      UseDockManager = True
    end
    object Panel115: TFlatPanel
      Left = 8
      Top = 244
      Width = 90
      Height = 22
      Caption = '비고'
      ParentColor = True
      TabOrder = 29
      UseDockManager = True
    end
    object Edit102: TFlatComboBox
      Left = 368
      Top = 20
      Width = 129
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
        '보 유 중'
        '할 인 필'
        '지 급 필'
        '배서유통'
        '부    도'
        '현 금 화'
        '결 재 됨')
      ParentFont = False
      TabOrder = 1
      ItemIndex = -1
      OnKeyDown = Edit112KeyDown
      OnKeyPress = Edit112KeyPress
    end
    object Edit101: TFlatEdit
      Left = 104
      Top = 20
      Width = 153
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 12
      ParentFont = False
      TabOrder = 0
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit103: TFlatEdit
      Left = 104
      Top = 52
      Width = 153
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 20
      ParentFont = False
      TabOrder = 2
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit104: TFlatEdit
      Left = 368
      Top = 52
      Width = 129
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 20
      ParentFont = False
      TabOrder = 3
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit108: TFlatEdit
      Left = 368
      Top = 116
      Width = 153
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 12
      ParentFont = False
      TabOrder = 7
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit109: TFlatEdit
      Left = 104
      Top = 148
      Width = 153
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 12
      ParentFont = False
      TabOrder = 8
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit110: TFlatEdit
      Left = 368
      Top = 148
      Width = 153
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 20
      ParentFont = False
      TabOrder = 9
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit115: TFlatEdit
      Left = 104
      Top = 244
      Width = 417
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
      TabOrder = 14
      OnKeyDown = Edit102KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit105: TFlatMaskEdit
      Left = 104
      Top = 84
      Width = 97
      Height = 22
      ColorFlat = clWhite
      AutoSize = False
      BorderStyle = bsNone
      Color = clWhite
      EditMask = '!9999.!99.99;1; '
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 10
      ParentFont = False
      TabOrder = 4
      Text = '1999.01.01'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Panel114: TFlatPanel
      Left = 272
      Top = 212
      Width = 90
      Height = 22
      Caption = '할인금액'
      ParentColor = True
      TabOrder = 28
      UseDockManager = True
    end
    object Edit106: TFlatMaskEdit
      Left = 368
      Top = 84
      Width = 97
      Height = 22
      ColorFlat = clWhite
      AutoSize = False
      BorderStyle = bsNone
      Color = clWhite
      EditMask = '!9999.!99.99;1; '
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 10
      ParentFont = False
      TabOrder = 5
      Text = '1999.01.01'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Edit107: TFlatMaskEdit
      Left = 104
      Top = 116
      Width = 97
      Height = 22
      ColorFlat = clWhite
      AutoSize = False
      BorderStyle = bsNone
      Color = clWhite
      EditMask = '!9999.!99.99;1; '
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 10
      ParentFont = False
      TabOrder = 6
      Text = '1999.01.01'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Edit111: TFlatMaskEdit
      Left = 104
      Top = 180
      Width = 97
      Height = 22
      ColorFlat = clWhite
      AutoSize = False
      BorderStyle = bsNone
      Color = clWhite
      EditMask = '!9999.!99.99;1; '
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 10
      ParentFont = False
      TabOrder = 10
      Text = '1999.01.01'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Edit112: TFlatNumber
      Left = 368
      Top = 180
      Width = 97
      Height = 22
      Digits = 0
      Max = 999999999
      FormatStr = '%9.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 11
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit113: TFlatNumber
      Left = 104
      Top = 212
      Width = 41
      Height = 22
      Digits = 0
      Max = 999
      FormatStr = '%3.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 12
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit114: TFlatNumber
      Left = 368
      Top = 212
      Width = 97
      Height = 22
      Digits = 0
      Max = 999999999
      FormatStr = '%9.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 13
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit3: TFlatEdit
      Left = 104
      Top = 4
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
      TabOrder = 30
      Visible = False
      OnKeyDown = Edit101KeyDown
    end
  end
  object Panel300: TFlatPanel
    Left = 1
    Top = 3
    Width = 767
    Height = 234
    Color = clInfoBk
    Enabled = False
    TabOrder = 2
    UseDockManager = True
    object Panel511: TFlatPanel
      Left = 536
      Top = 6
      Width = 65
      Height = 18
      Caption = '거래명세서'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 17
      UseDockManager = True
    end
    object Panel512: TFlatPanel
      Left = 536
      Top = 23
      Width = 65
      Height = 18
      Caption = '발행비외'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 18
      UseDockManager = True
    end
    object Panel521: TFlatPanel
      Left = 536
      Top = 46
      Width = 65
      Height = 35
      Caption = '책보호대'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 19
      UseDockManager = True
    end
    object Panel531: TFlatPanel
      Left = 536
      Top = 86
      Width = 65
      Height = 35
      Caption = '박스대'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 20
      UseDockManager = True
    end
    object Panel541: TFlatPanel
      Left = 536
      Top = 126
      Width = 65
      Height = 35
      Caption = '반품정리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 21
      UseDockManager = True
    end
    object Panel551: TFlatPanel
      Left = 536
      Top = 166
      Width = 65
      Height = 18
      Caption = '반품재고외'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 22
      UseDockManager = True
    end
    object Panel552: TFlatPanel
      Left = 536
      Top = 183
      Width = 65
      Height = 18
      Caption = '비품보관비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 23
      UseDockManager = True
    end
    object Edit311: TFlatNumber
      Left = 115
      Top = 6
      Width = 61
      Height = 35
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
    object Edit321: TFlatNumber
      Left = 115
      Top = 46
      Width = 134
      Height = 35
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
    object Edit331: TFlatNumber
      Left = 115
      Top = 86
      Width = 61
      Height = 35
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
      TabOrder = 26
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit341: TFlatNumber
      Left = 115
      Top = 126
      Width = 61
      Height = 35
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
      TabOrder = 27
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit411: TFlatNumber
      Left = 371
      Top = 6
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 28
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit412: TFlatNumber
      Left = 371
      Top = 23
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 29
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit421: TFlatNumber
      Left = 371
      Top = 46
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 30
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit422: TFlatNumber
      Left = 371
      Top = 63
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 31
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit431: TFlatNumber
      Left = 371
      Top = 86
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 32
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit432: TFlatNumber
      Left = 371
      Top = 103
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 33
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit441: TFlatNumber
      Left = 371
      Top = 126
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 34
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit442: TFlatNumber
      Left = 371
      Top = 143
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 35
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit451: TFlatNumber
      Left = 371
      Top = 166
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 36
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit452: TFlatNumber
      Left = 371
      Top = 183
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 37
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit511: TFlatNumber
      Left = 603
      Top = 6
      Width = 61
      Height = 35
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
      TabOrder = 38
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit521: TFlatNumber
      Left = 603
      Top = 46
      Width = 61
      Height = 35
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
      TabOrder = 39
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit531: TFlatNumber
      Left = 603
      Top = 86
      Width = 61
      Height = 35
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
      TabOrder = 40
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit541: TFlatNumber
      Left = 603
      Top = 126
      Width = 61
      Height = 35
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
      TabOrder = 41
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit551: TFlatNumber
      Left = 603
      Top = 166
      Width = 61
      Height = 35
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
    object Panel332: TFlatPanel
      Left = 176
      Top = 86
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 43
      UseDockManager = True
      object RadioButton331: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton332: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel342: TFlatPanel
      Left = 176
      Top = 126
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 44
      UseDockManager = True
      object RadioButton341: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton342: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel353: TFlatPanel
      Left = 115
      Top = 166
      Width = 134
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 45
      UseDockManager = True
      object RadioButton351: TRadioButton
        Left = 8
        Top = 9
        Width = 49
        Height = 17
        Caption = '시내'
        TabOrder = 0
      end
      object RadioButton352: TRadioButton
        Left = 56
        Top = 9
        Width = 74
        Height = 17
        Caption = '시내+지방'
        TabOrder = 1
      end
    end
    object Panel413: TFlatPanel
      Left = 432
      Top = 6
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 46
      UseDockManager = True
      object RadioButton411: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton412: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel423: TFlatPanel
      Left = 432
      Top = 46
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 47
      UseDockManager = True
      object RadioButton421: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton422: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel433: TFlatPanel
      Left = 432
      Top = 86
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 48
      UseDockManager = True
      object RadioButton431: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton432: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel443: TFlatPanel
      Left = 432
      Top = 126
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 49
      UseDockManager = True
      object RadioButton441: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton442: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel453: TFlatPanel
      Left = 432
      Top = 166
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 50
      UseDockManager = True
      object RadioButton451: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton452: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel513: TFlatPanel
      Left = 664
      Top = 6
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 51
      UseDockManager = True
      object RadioButton511: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton512: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel522: TFlatPanel
      Left = 664
      Top = 46
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 52
      UseDockManager = True
      object RadioButton521: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton522: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel532: TFlatPanel
      Left = 664
      Top = 86
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 53
      UseDockManager = True
      object RadioButton531: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton532: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel542: TFlatPanel
      Left = 664
      Top = 126
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 54
      UseDockManager = True
      object RadioButton541: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton542: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Panel553: TFlatPanel
      Left = 664
      Top = 166
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 55
      UseDockManager = True
      object RadioButton551: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
      end
      object RadioButton552: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
      end
    end
    object Edit238: TFlatEdit
      Left = 115
      Top = 207
      Width = 310
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
      TabOrder = 57
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit236: TFlatNumber
      Left = 427
      Top = 207
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
      TabOrder = 58
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel7: TFlatPanel
      Left = 48
      Top = 207
      Width = 65
      Height = 22
      Caption = '비고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 56
      UseDockManager = True
    end
    object FlatPanel18: TFlatPanel
      Left = 16
      Top = 3
      Width = 99
      Height = 201
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clBlue
      ColorShadow = clBlue
      TabOrder = 59
      UseDockManager = True
      object myLabel3d1: TmyLabel3d
        Left = 8
        Top = 42
        Width = 22
        Height = 126
        Caption = '배'#13#10'송'#13#10'계'#13#10'약'#13#10'내'#13#10'용'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlue
        Font.Height = -21
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object Panel311: TFlatPanel
      Left = 48
      Top = 6
      Width = 65
      Height = 18
      Caption = '①기본'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 0
      UseDockManager = True
    end
    object Panel312: TFlatPanel
      Left = 48
      Top = 23
      Width = 65
      Height = 18
      Caption = '계약부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 1
      UseDockManager = True
    end
    object Panel321: TFlatPanel
      Left = 48
      Top = 46
      Width = 65
      Height = 35
      Caption = '②기본금액'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 2
      UseDockManager = True
    end
    object Panel331: TFlatPanel
      Left = 48
      Top = 86
      Width = 65
      Height = 35
      Caption = '③초과부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 3
      UseDockManager = True
    end
    object Panel341: TFlatPanel
      Left = 48
      Top = 126
      Width = 65
      Height = 35
      Caption = '④지방부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 4
      UseDockManager = True
    end
    object Panel351: TFlatPanel
      Left = 48
      Top = 166
      Width = 65
      Height = 18
      Caption = '기본'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 5
      UseDockManager = True
    end
    object Panel352: TFlatPanel
      Left = 48
      Top = 183
      Width = 65
      Height = 18
      Caption = '계약부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clBlue
      TabOrder = 6
      UseDockManager = True
    end
    object FlatPanel1: TFlatPanel
      Left = 272
      Top = 3
      Width = 99
      Height = 201
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clGreen
      ColorShadow = clGreen
      TabOrder = 60
      UseDockManager = True
      object myLabel3d2: TmyLabel3d
        Left = 8
        Top = 42
        Width = 22
        Height = 126
        Caption = '물'#13#10'류'#13#10'계'#13#10'약'#13#10'내'#13#10'용'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clGreen
        Font.Height = -21
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object Panel411: TFlatPanel
      Left = 304
      Top = 6
      Width = 65
      Height = 18
      Caption = '⑤입출고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 7
      UseDockManager = True
    end
    object Panel412: TFlatPanel
      Left = 304
      Top = 23
      Width = 65
      Height = 18
      Caption = '기본부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 8
      UseDockManager = True
    end
    object Panel421: TFlatPanel
      Left = 304
      Top = 46
      Width = 65
      Height = 18
      Caption = '⑤-1입출고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 9
      UseDockManager = True
    end
    object Panel422: TFlatPanel
      Left = 304
      Top = 63
      Width = 65
      Height = 18
      Caption = '초과관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 10
      UseDockManager = True
    end
    object Panel431: TFlatPanel
      Left = 304
      Top = 86
      Width = 65
      Height = 18
      Caption = '⑥재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 11
      UseDockManager = True
    end
    object Panel432: TFlatPanel
      Left = 304
      Top = 103
      Width = 65
      Height = 18
      Caption = '기본부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 12
      UseDockManager = True
    end
    object Panel441: TFlatPanel
      Left = 304
      Top = 126
      Width = 65
      Height = 18
      Caption = '⑥-1재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 13
      UseDockManager = True
    end
    object Panel442: TFlatPanel
      Left = 304
      Top = 143
      Width = 65
      Height = 18
      Caption = '초과관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 14
      UseDockManager = True
    end
    object Panel451: TFlatPanel
      Left = 304
      Top = 166
      Width = 65
      Height = 18
      Caption = '⑦재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 15
      UseDockManager = True
    end
    object Panel452: TFlatPanel
      Left = 304
      Top = 183
      Width = 65
      Height = 18
      Caption = '관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 16
      UseDockManager = True
    end
  end
end
