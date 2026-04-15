object Sobo45: TSobo45
  Left = 22
  Top = 104
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '청구서관리'
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
    Color = clAqua
    TabOrder = 0
    UseDockManager = True
    object Label101: TmyLabel3d
      Left = 561
      Top = 13
      Width = 15
      Height = 19
      Caption = '~'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -19
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Panel101: TFlatPanel
      Left = 16
      Top = 12
      Width = 90
      Height = 22
      Caption = '거래일자'
      ParentColor = True
      TabOrder = 3
      UseDockManager = True
    end
    object Button101: TFlatButton
      Left = 928
      Top = 0
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
      Top = 24
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
      EditMask = '!9999.!99;1; '
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 7
      ParentFont = False
      TabOrder = 0
      Text = '2000.01'
      OnChange = Edit101Change
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Panel105: TFlatPanel
      Left = 248
      Top = 12
      Width = 90
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 4
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
      MaxLength = 24
      ParentFont = False
      TabOrder = 2
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
      TabOrder = 1
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
      MaxLength = 24
      ParentFont = False
      TabOrder = 8
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
      TabOrder = 7
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
      TabOrder = 9
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
      TabOrder = 10
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
      TabOrder = 11
      OnClick = Button702Click
    end
    object Button709: TFlatButton
      Left = 848
      Top = 10
      Width = 65
      Height = 25
      Caption = '검색'
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
      TabOrder = 12
      OnClick = Button101Click
    end
  end
  object Panel002: TFlatPanel
    Left = 2
    Top = 52
    Width = 210
    Height = 519
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGrid
      Left = 1
      Top = 1
      Width = 208
      Height = 499
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource2
      ImeName = '한국어(한글)'
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgCancelOnExit]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnDblClick = DBGrid101DblClick
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      OnTitleClick = DBGrid101TitleClick
      Columns = <
        item
          Expanded = False
          FieldName = 'HCODE'
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 43
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'HNAME'
          Title.Alignment = taCenter
          Title.Caption = '출판사명'
          Width = 135
          Visible = True
        end>
    end
    object StBar101: TStatusBar
      Left = 1
      Top = 500
      Width = 208
      Height = 18
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Width = 190
        end
        item
          Width = 50
        end>
      ParentFont = True
      SimplePanel = False
      UseSystemFont = False
    end
  end
  object Panel003: TFlatPanel
    Left = 216
    Top = 52
    Width = 745
    Height = 313
    ParentColor = True
    TabOrder = 2
    UseDockManager = True
    object StBar201: TStatusBar
      Left = 1
      Top = 294
      Width = 743
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
          Width = 570
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
      Width = 743
      Height = 293
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
      OnDrawColumnCell = DBGrid201DrawColumnCell
      OnKeyDown = DBGrid201KeyDown
      OnKeyPress = DBGrid201KeyPress
      OnMouseMove = DBGrid201MouseMove
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
          Width = 60
        end
        item
          EditButtons = <>
          FieldName = 'GQUT2'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '출고내역|지방부수'
          Width = 60
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
          Width = 100
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
          Width = 144
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
      Left = 424
      Top = 5
      Width = 525
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
      Width = 521
      Height = 18
      Min = 0
      Max = 100
      TabOrder = 3
    end
  end
  object Panel200: TFlatPanel
    Left = 216
    Top = 368
    Width = 745
    Height = 203
    Color = clInfoBk
    TabOrder = 4
    UseDockManager = True
    object Panel201: TFlatPanel
      Left = 16
      Top = 12
      Width = 65
      Height = 22
      Caption = '출고부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 39
      UseDockManager = True
    end
    object Panel210: TFlatPanel
      Left = 496
      Top = 108
      Width = 65
      Height = 21
      Caption = '반품정리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 48
      UseDockManager = True
    end
    object Panel202: TFlatPanel
      Left = 16
      Top = 43
      Width = 65
      Height = 12
      Caption = '배송'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 40
      UseDockManager = True
    end
    object Panel204: TFlatPanel
      Left = 16
      Top = 108
      Width = 65
      Height = 22
      Caption = '지방부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 42
      UseDockManager = True
    end
    object Panel205: TFlatPanel
      Left = 496
      Top = 44
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
      TabOrder = 43
      UseDockManager = True
    end
    object Panel207: TFlatPanel
      Left = 416
      Top = 11
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
      TabOrder = 45
      UseDockManager = True
    end
    object Panel208: TFlatPanel
      Left = 256
      Top = 43
      Width = 65
      Height = 12
      Caption = '물류입출고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 46
      UseDockManager = True
    end
    object Edit201: TFlatNumber
      Left = 83
      Top = 12
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
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit208: TFlatNumber
      Left = 83
      Top = 108
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
      TabOrder = 10
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit209: TFlatNumber
      Left = 138
      Top = 108
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
      TabOrder = 11
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit210: TFlatNumber
      Left = 172
      Top = 108
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
      TabOrder = 12
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit217: TFlatNumber
      Left = 483
      Top = 12
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
      TabOrder = 2
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit224: TFlatNumber
      Left = 651
      Top = 108
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
      TabOrder = 30
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit227: TFlatNumber
      Left = 83
      Top = 172
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
      TabOrder = 35
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit202: TFlatNumber
      Left = 83
      Top = 44
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
      TabOrder = 4
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit203: TFlatNumber
      Left = 138
      Top = 44
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clBtnFace
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 5
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit204: TFlatNumber
      Left = 172
      Top = 44
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
      TabOrder = 6
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel213: TFlatPanel
      Left = 16
      Top = 172
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
      TabOrder = 51
      UseDockManager = True
    end
    object Panel211: TFlatPanel
      Left = 576
      Top = 11
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
      TabOrder = 49
      UseDockManager = True
    end
    object Panel203: TFlatPanel
      Left = 16
      Top = 76
      Width = 65
      Height = 22
      Caption = '추가부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 41
      UseDockManager = True
    end
    object Edit211: TFlatNumber
      Left = 563
      Top = 44
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
      TabOrder = 22
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit212: TFlatNumber
      Left = 618
      Top = 44
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
      TabOrder = 23
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit213: TFlatNumber
      Left = 652
      Top = 44
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
      TabOrder = 24
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit218: TFlatNumber
      Left = 323
      Top = 44
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
      TabOrder = 13
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit219: TFlatNumber
      Left = 378
      Top = 44
      Width = 33
      Height = 21
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clBtnFace
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 14
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit220: TFlatNumber
      Left = 412
      Top = 44
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
      TabOrder = 15
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit225: TFlatNumber
      Left = 643
      Top = 12
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
      TabOrder = 3
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit205: TFlatNumber
      Left = 83
      Top = 76
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
      TabOrder = 7
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit206: TFlatNumber
      Left = 138
      Top = 76
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
      TabOrder = 8
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit207: TFlatNumber
      Left = 172
      Top = 76
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
      TabOrder = 9
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel206: TFlatPanel
      Left = 496
      Top = 76
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
      TabOrder = 44
      UseDockManager = True
    end
    object Panel209: TFlatPanel
      Left = 256
      Top = 76
      Width = 65
      Height = 22
      Caption = '초과관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 47
      UseDockManager = True
    end
    object Panel212: TFlatPanel
      Left = 336
      Top = 172
      Width = 65
      Height = 22
      Caption = '전일미수금'
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 50
      UseDockManager = True
    end
    object Edit214: TFlatNumber
      Left = 563
      Top = 76
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
      TabOrder = 25
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit215: TFlatNumber
      Left = 618
      Top = 76
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
      TabOrder = 26
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit216: TFlatNumber
      Left = 652
      Top = 76
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
      TabOrder = 27
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit221: TFlatNumber
      Left = 323
      Top = 76
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
      TabOrder = 16
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit222: TFlatNumber
      Left = 378
      Top = 76
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
      TabOrder = 17
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit223: TFlatNumber
      Left = 412
      Top = 76
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
      TabOrder = 18
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit226: TFlatNumber
      Left = 403
      Top = 172
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
      TabOrder = 37
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel216: TFlatPanel
      Left = 496
      Top = 172
      Width = 65
      Height = 22
      Caption = '합계금액'
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 54
      UseDockManager = True
    end
    object Edit230: TFlatNumber
      Left = 563
      Top = 172
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
      TabOrder = 38
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel214: TFlatPanel
      Left = 176
      Top = 172
      Width = 65
      Height = 22
      Caption = 'V.A.T'
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 52
      UseDockManager = True
    end
    object Edit228: TFlatNumber
      Left = 243
      Top = 172
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
      TabOrder = 36
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel215: TFlatPanel
      Left = 256
      Top = 11
      Width = 65
      Height = 12
      Caption = '창고'
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
    object Edit229: TFlatNumber
      Left = 323
      Top = 12
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
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Button301: TFlatButton
      Left = 656
      Top = 160
      Width = 73
      Height = 33
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
      Layout = blGlyphLeft
      NumGlyphs = 2
      ParentColor = False
      TabOrder = 55
      OnClick = Button301Click
    end
    object Edit231: TFlatNumber
      Left = 563
      Top = 108
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
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit232: TFlatNumber
      Left = 618
      Top = 108
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
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel217: TFlatPanel
      Left = 256
      Top = 107
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
      TabOrder = 56
      UseDockManager = True
    end
    object Edit233: TFlatNumber
      Left = 323
      Top = 108
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
      TabOrder = 19
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit234: TFlatNumber
      Left = 378
      Top = 108
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
      TabOrder = 20
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit235: TFlatNumber
      Left = 411
      Top = 108
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
      TabOrder = 21
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel1: TFlatPanel
      Left = 256
      Top = 22
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
      TabOrder = 57
      UseDockManager = True
    end
    object FlatPanel2: TFlatPanel
      Left = 416
      Top = 22
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
      TabOrder = 58
      UseDockManager = True
    end
    object FlatPanel3: TFlatPanel
      Left = 576
      Top = 22
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
      TabOrder = 59
      UseDockManager = True
    end
    object FlatPanel4: TFlatPanel
      Left = 16
      Top = 54
      Width = 65
      Height = 12
      Caption = '기본계약'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 60
      UseDockManager = True
    end
    object FlatPanel5: TFlatPanel
      Left = 256
      Top = 54
      Width = 65
      Height = 12
      Caption = '기본관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 61
      UseDockManager = True
    end
    object FlatPanel6: TFlatPanel
      Left = 256
      Top = 118
      Width = 65
      Height = 12
      Caption = '재고보관비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clGreen
      TabOrder = 62
      UseDockManager = True
    end
    object FlatPanel7: TFlatPanel
      Left = 16
      Top = 140
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
      TabOrder = 63
      UseDockManager = True
    end
    object FlatPanel8: TFlatPanel
      Left = 336
      Top = 140
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
      TabOrder = 64
      UseDockManager = True
    end
    object Edit236: TFlatNumber
      Left = 83
      Top = 140
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
      TabOrder = 31
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit237: TFlatNumber
      Left = 403
      Top = 140
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
      TabOrder = 33
      Text = '0'
      OnEnter = Edit201Exit
      OnExit = Edit201Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit238: TFlatEdit
      Left = 162
      Top = 140
      Width = 161
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
      TabOrder = 32
    end
    object Edit239: TFlatEdit
      Left = 482
      Top = 140
      Width = 161
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
      TabOrder = 34
    end
    object CheckBox1: TFlatCheckBox
      Left = 648
      Top = 141
      Width = 89
      Height = 17
      Caption = '출판사Show'
      Color = clInfoBk
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 65
      TabStop = True
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
  end
  object Panel004: TFlatPanel
    Left = 216
    Top = 574
    Width = 745
    Height = 29
    Color = clInfoBk
    Visible = False
    TabOrder = 5
    UseDockManager = True
    object Label001: TmyLabel3d
      Left = 16
      Top = 5
      Width = 7
      Height = 19
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -19
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AStyle3D = Raised3d
      AShadeLTSet = False
    end
    object Label002: TmyLabel3d
      Left = 80
      Top = 5
      Width = 7
      Height = 19
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -19
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AStyle3D = Raised3d
      AShadeLTSet = False
    end
    object Label003: TmyLabel3d
      Left = 624
      Top = 5
      Width = 7
      Height = 19
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -19
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      Visible = False
      AStyle3D = Raised3d
      AShadeLTSet = False
    end
  end
  object DataSource1: TDataSource
    DataSet = Base10.T4_Sub51
    OnDataChange = DataSource1DataChange
    Left = 10
    Top = 126
  end
  object DataSource2: TDataSource
    DataSet = Base10.T4_Sub52
    OnDataChange = DataSource2DataChange
    Left = 42
    Top = 126
  end
end
