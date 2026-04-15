object Sobo26: TSobo26
  Left = 2162
  Top = 211
  ActiveControl = RadioButton3
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '출고접수현황'
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
  object Panel001: TFlatPanel
    Left = 2
    Top = 4
    Width = 959
    Height = 45
    Color = 14416873
    TabOrder = 0
    UseDockManager = True
    object Label101: TmyLabel3d
      Left = 556
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
      Width = 87
      Height = 22
      Caption = '거래일자'
      ParentColor = True
      TabOrder = 3
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
      TabOrder = 5
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
      TabOrder = 6
      Visible = False
      OnClick = Button201Click
    end
    object Edit101: TFlatMaskEdit
      Left = 112
      Top = 12
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
      TabOrder = 0
      Text = '1999.01.01'
      OnChange = Edit101Change
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Panel105: TFlatPanel
      Left = 248
      Top = 12
      Width = 87
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 4
      UseDockManager = True
    end
    object Edit103: TFlatEdit
      Left = 336
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
      TabOrder = 2
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit102: TFlatEdit
      Left = 336
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
      TabOrder = 1
      Visible = False
    end
    object Edit105: TFlatEdit
      Left = 568
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
      TabOrder = 8
      OnChange = Edit101Change
      OnKeyDown = Edit102KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit104: TFlatEdit
      Left = 568
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
      TabOrder = 7
      Visible = False
    end
    object RadioButton1: TFlatRadioButton
      Left = 808
      Top = 16
      Width = 49
      Height = 17
      Caption = '접수'
      TabOrder = 9
      OnClick = Button101Click
    end
    object RadioButton2: TFlatRadioButton
      Left = 856
      Top = 16
      Width = 49
      Height = 17
      Caption = '완료'
      TabOrder = 10
      OnClick = Button101Click
    end
    object RadioButton3: TFlatRadioButton
      Left = 904
      Top = 16
      Width = 49
      Height = 17
      Caption = '전체'
      Checked = True
      TabOrder = 11
      TabStop = True
      OnClick = Button101Click
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
      TabOrder = 12
      OnAcceptDate = DateEdit1AcceptDate
      OnButtonClick = DateEdit1ButtonClick
    end
    object Button701: TFlatButton
      Left = 536
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
      TabOrder = 13
      OnClick = Button701Click
    end
    object Button702: TFlatButton
      Left = 768
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
      TabOrder = 14
      OnClick = Button702Click
    end
  end
  object Panel002: TFlatPanel
    Left = 2
    Top = 56
    Width = 375
    Height = 513
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGridEh
      Left = 1
      Top = 1
      Width = 373
      Height = 511
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource2
      FooterColor = 16311512
      FooterFont.Charset = HANGEUL_CHARSET
      FooterFont.Color = clWindowText
      FooterFont.Height = -12
      FooterFont.Name = '굴림'
      FooterFont.Style = [fsBold]
      ImeName = '한국어 입력 시스템 (IME 2000)'
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnDblClick = DBGrid201DblClick
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      OnTitleClick = DBGrid101TitleClick
      Columns = <
        item
          EditButtons = <>
          FieldName = 'HCODE'
          Footers = <>
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 40
        end
        item
          EditButtons = <>
          FieldName = 'HNAME'
          Footers = <>
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '출판사명'
          Width = 118
        end
        item
          EditButtons = <>
          FieldName = 'GNAME'
          Footers = <>
          PickList.Strings = (
            '9')
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '거래처명'
          Width = 140
        end
        item
          Alignment = taCenter
          EditButtons = <>
          FieldName = 'YESNO'
          Footers = <>
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '배송'
          Width = 40
        end>
    end
  end
  object Panel003: TFlatPanel
    Left = 384
    Top = 316
    Width = 577
    Height = 253
    ParentColor = True
    TabOrder = 2
    UseDockManager = True
    object DBGrid201: TDBGridEh
      Left = 1
      Top = 1
      Width = 575
      Height = 251
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      FooterColor = 16311512
      FooterFont.Charset = HANGEUL_CHARSET
      FooterFont.Color = clRed
      FooterFont.Height = -12
      FooterFont.Name = '굴림'
      FooterFont.Style = [fsBold]
      FooterRowCount = 1
      ImeName = '한국어 입력 시스템 (IME 2000)'
      ParentFont = False
      PopupMenu = Subu00.PopupMenu1
      SumList.Active = True
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnDblClick = DBGrid201DblClick
      OnDrawColumnCell = DBGrid201DrawColumnCell
      OnKeyDown = DBGrid201KeyDown
      OnKeyPress = DBGrid201KeyPress
      OnTitleClick = DBGrid201TitleClick
      Columns = <
        item
          EditButtons = <>
          FieldName = 'JUBUN'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = 'No'
          Width = 30
        end
        item
          EditButtons = <>
          FieldName = 'PUBUN'
          Footer.Value = '합계'
          Footer.ValueType = fvtStaticText
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '구분'
          Width = 45
        end
        item
          ButtonStyle = cbsEllipsis
          EditButtons = <>
          FieldName = 'BNAME'
          Footers = <>
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '도서명'
          Width = 200
        end
        item
          EditButtons = <>
          FieldName = 'GDANG'
          Footers = <>
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '단가'
          Width = 50
        end
        item
          EditButtons = <>
          FieldName = 'QSQUT'
          Footers = <>
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '의뢰수량'
          Title.Font.Charset = HANGEUL_CHARSET
          Title.Font.Color = clWindowText
          Title.Font.Height = -11
          Title.Font.Name = '굴림'
          Title.Font.Style = [fsBold]
          Width = 50
        end
        item
          Color = 12056530
          EditButtons = <>
          FieldName = 'GSQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '출고수량'
          Title.Font.Charset = HANGEUL_CHARSET
          Title.Font.Color = clWindowText
          Title.Font.Height = -11
          Title.Font.Name = '굴림'
          Title.Font.Style = [fsBold]
          Width = 50
        end
        item
          Alignment = taCenter
          EditButtons = <>
          FieldName = 'GRAT1'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '비율'
          Width = 30
        end
        item
          Color = 11861755
          EditButtons = <>
          FieldName = 'GSSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '금액'
          Width = 82
        end>
    end
  end
  object Panel007: TFlatPanel
    Left = 2
    Top = 574
    Width = 959
    Height = 29
    Color = clInfoBk
    TabOrder = 3
    UseDockManager = True
    object ProgressBar0: TFlatProgressBar
      Left = 672
      Top = 5
      Width = 273
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
      Left = 568
      Top = 5
      Width = 97
      Height = 19
      Caption = '검색진행'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object ProgressBar1: TProgressBar
      Left = 672
      Top = 5
      Width = 272
      Height = 18
      Min = 0
      Max = 100
      TabOrder = 3
    end
    object Panel501: TFlatPanel
      Left = 264
      Top = 5
      Width = 87
      Height = 19
      Caption = '거래처명-검색'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = True
      TabOrder = 4
      UseDockManager = True
    end
    object Edit501: TFlatEdit
      Left = 352
      Top = 5
      Width = 169
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 50
      ParentFont = False
      TabOrder = 5
      OnKeyPress = Edit115KeyPress
    end
  end
  object Panel200: TFlatPanel
    Left = 384
    Top = 56
    Width = 577
    Height = 153
    Color = clInfoBk
    TabOrder = 4
    UseDockManager = True
    object Panel201: TFlatPanel
      Left = 16
      Top = 12
      Width = 90
      Height = 19
      Caption = '접수번호'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 4
      UseDockManager = True
    end
    object Panel207: TFlatPanel
      Left = 16
      Top = 90
      Width = 90
      Height = 53
      Caption = '메      모'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 6
      UseDockManager = True
    end
    object Edit207: TFlatEdit
      Left = 112
      Top = 90
      Width = 402
      Height = 17
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 90
      ParentFont = False
      TabOrder = 3
      OnChange = Edit101Change
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit208: TFlatEdit
      Left = 112
      Top = 108
      Width = 402
      Height = 17
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 90
      ParentFont = False
      TabOrder = 2
      OnChange = Edit101Change
      OnKeyPress = Edit111KeyPress
      OnKeyUp = Edit111KeyDown
    end
    object Panel202: TFlatPanel
      Left = 240
      Top = 12
      Width = 90
      Height = 19
      Caption = '접수일자'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 5
      UseDockManager = True
    end
    object Edit202: TFlatEdit
      Left = 336
      Top = 12
      Width = 225
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 24
      ParentFont = False
      ReadOnly = True
      TabOrder = 1
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit201: TFlatEdit
      Left = 112
      Top = 12
      Width = 105
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 5
      ParentFont = False
      ReadOnly = True
      TabOrder = 0
    end
    object Panel203: TFlatPanel
      Left = 16
      Top = 38
      Width = 90
      Height = 19
      Caption = '출판사코드'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 7
      UseDockManager = True
    end
    object Edit203: TFlatEdit
      Left = 112
      Top = 38
      Width = 105
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 5
      ParentFont = False
      ReadOnly = True
      TabOrder = 8
    end
    object Panel204: TFlatPanel
      Left = 240
      Top = 38
      Width = 90
      Height = 19
      Caption = '출판사명'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 9
      UseDockManager = True
    end
    object Edit204: TFlatEdit
      Left = 336
      Top = 38
      Width = 225
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 50
      ParentFont = False
      ReadOnly = True
      TabOrder = 10
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Panel205: TFlatPanel
      Left = 16
      Top = 64
      Width = 90
      Height = 19
      Caption = '서점코드'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 11
      UseDockManager = True
    end
    object Panel206: TFlatPanel
      Left = 240
      Top = 64
      Width = 90
      Height = 19
      Caption = '서 점 명'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 12
      UseDockManager = True
    end
    object Edit205: TFlatEdit
      Left = 112
      Top = 64
      Width = 105
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 5
      ParentFont = False
      ReadOnly = True
      TabOrder = 13
    end
    object Edit206: TFlatEdit
      Left = 336
      Top = 64
      Width = 225
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 50
      ParentFont = False
      ReadOnly = True
      TabOrder = 14
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Button401: TFlatButton
      Left = 520
      Top = 90
      Width = 41
      Height = 54
      Color = clInfoBk
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
      NumGlyphs = 2
      ParentColor = False
      TabOrder = 15
      OnClick = Button401Click
      BiDiMode = bdLeftToRight
      ParentBiDiMode = False
    end
    object Edit209: TFlatEdit
      Left = 112
      Top = 126
      Width = 100
      Height = 17
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 20
      ParentFont = False
      TabOrder = 16
      OnClick = Edit205Click
      OnEnter = Edit205Click
      OnExit = Edit205Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object StaticText1: TStaticText
      Left = 130
      Top = 129
      Width = 69
      Height = 13
      AutoSize = False
      Caption = '핸드폰번호'
      Color = clWhite
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clSilver
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 17
      OnClick = StaticText1Click
    end
    object Edit210: TFlatEdit
      Left = 216
      Top = 126
      Width = 100
      Height = 17
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 20
      ParentFont = False
      TabOrder = 18
      OnClick = Edit205Click
      OnEnter = Edit205Click
      OnExit = Edit205Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object StaticText2: TStaticText
      Left = 241
      Top = 129
      Width = 53
      Height = 13
      AutoSize = False
      Caption = '전화번호'
      Color = clWhite
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clSilver
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 19
      OnClick = StaticText2Click
    end
    object Edit211: TFlatEdit
      Left = 320
      Top = 126
      Width = 100
      Height = 17
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 30
      ParentFont = False
      TabOrder = 20
      OnClick = Edit205Click
      OnEnter = Edit205Click
      OnExit = Edit205Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object StaticText3: TStaticText
      Left = 345
      Top = 129
      Width = 56
      Height = 13
      AutoSize = False
      Caption = '받는사람'
      Color = clWhite
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clSilver
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 21
      OnClick = StaticText3Click
    end
    object Button400: TFlatButton
      Left = 81
      Top = 124
      Width = 25
      Height = 19
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
      Layout = blGlyphLeft
      NumGlyphs = 2
      TabOrder = 22
      OnClick = Button400Click
    end
    object Edit212: TFlatEdit
      Left = 425
      Top = 126
      Width = 72
      Height = 17
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 30
      ParentFont = False
      TabOrder = 23
      OnClick = Edit205Click
      OnEnter = Edit205Click
      OnExit = Edit205Exit
      OnKeyDown = Edit102KeyDown
    end
    object StaticText4: TStaticText
      Left = 435
      Top = 129
      Width = 56
      Height = 13
      AutoSize = False
      Caption = '우편번호'
      Color = clWhite
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clSilver
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 24
      OnClick = StaticText4Click
    end
    object Button403: TFlatButton
      Left = 496
      Top = 126
      Width = 18
      Height = 17
      Hint = '주소가져오기'
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
      ParentShowHint = False
      ShowHint = True
      TabOrder = 25
      OnClick = Button403Click
    end
  end
  object Panel300: TFlatPanel
    Left = 384
    Top = 211
    Width = 577
    Height = 63
    Color = clInfoBk
    TabOrder = 5
    UseDockManager = True
    object Panel301: TFlatPanel
      Left = 16
      Top = 9
      Width = 90
      Height = 19
      Caption = '도서코드'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 0
      UseDockManager = True
    end
    object Panel303: TFlatPanel
      Left = 16
      Top = 35
      Width = 90
      Height = 19
      Caption = '재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 1
      UseDockManager = True
    end
    object Edit303: TFlatEdit
      Left = 112
      Top = 35
      Width = 105
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 5
      ParentFont = False
      ReadOnly = True
      TabOrder = 2
    end
    object Edit301: TFlatEdit
      Left = 112
      Top = 9
      Width = 105
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 5
      ParentFont = False
      ReadOnly = True
      TabOrder = 3
    end
    object Panel302: TFlatPanel
      Left = 240
      Top = 9
      Width = 90
      Height = 19
      Caption = '도서명'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 4
      UseDockManager = True
    end
    object Panel304: TFlatPanel
      Left = 240
      Top = 35
      Width = 90
      Height = 19
      Caption = '비고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 5
      UseDockManager = True
    end
    object Edit304: TFlatEdit
      Left = 336
      Top = 35
      Width = 225
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 50
      ParentFont = False
      ReadOnly = True
      TabOrder = 6
    end
    object Edit302: TFlatEdit
      Left = 336
      Top = 9
      Width = 225
      Height = 19
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 80
      ParentFont = False
      ReadOnly = True
      TabOrder = 7
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
  end
  object Panel004: TFlatPanel
    Left = 384
    Top = 276
    Width = 577
    Height = 37
    Color = clInfoBk
    TabOrder = 6
    UseDockManager = True
    object Label401: TmyLabel3d
      Left = 16
      Top = 5
      Width = 56
      Height = 12
      Caption = '입력시간 :'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Label402: TmyLabel3d
      Left = 16
      Top = 21
      Width = 56
      Height = 12
      Caption = '접수시간 :'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Label403: TmyLabel3d
      Left = 288
      Top = 5
      Width = 72
      Height = 12
      Caption = '출력시간(1) :'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Label404: TmyLabel3d
      Left = 288
      Top = 21
      Width = 72
      Height = 12
      Caption = '출력시간(2) :'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Label411: TmyLabel3d
      Left = 80
      Top = 5
      Width = 5
      Height = 12
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Label412: TmyLabel3d
      Left = 80
      Top = 21
      Width = 5
      Height = 12
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Label413: TmyLabel3d
      Left = 368
      Top = 5
      Width = 5
      Height = 12
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Label414: TmyLabel3d
      Left = 368
      Top = 21
      Width = 5
      Height = 12
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
  end
  object DataSource1: TDataSource
    DataSet = Base10.T2_Sub61
    OnDataChange = DataSource1DataChange
    Left = 50
    Top = 126
  end
  object DataSource2: TDataSource
    DataSet = Base10.T2_Sub62
    OnDataChange = DataSource2DataChange
    Left = 158
    Top = 126
  end
end
