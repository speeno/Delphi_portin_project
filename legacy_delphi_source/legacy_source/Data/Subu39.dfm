object Sobo39: TSobo39
  Left = 43
  Top = 94
  BorderStyle = bsSingle
  Caption = '출고증관리'
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
  object Panel002: TFlatPanel
    Left = 222
    Top = 64
    Width = 369
    Height = 505
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGrid
      Left = 1
      Top = 1
      Width = 367
      Height = 484
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      ImeName = '한국어(한글)'
      Options = [dgEditing, dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnEnter = DBGrid101Enter
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      OnTitleClick = DBGrid101TitleClick
      Columns = <
        item
          Expanded = False
          FieldName = 'GCODE'
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 40
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GNAME'
          Title.Alignment = taCenter
          Title.Caption = '거래처명'
          Width = 150
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GOQUT'
          Title.Alignment = taCenter
          Title.Caption = '수량'
          Width = 48
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GBQUT'
          Title.Alignment = taCenter
          Title.Caption = '박스'
          Width = 48
          Visible = True
        end
        item
          Expanded = False
          Width = 48
          Visible = True
        end>
    end
    object StBar101: TStatusBar
      Left = 1
      Top = 485
      Width = 367
      Height = 19
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Width = 350
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
    Left = 592
    Top = 64
    Width = 369
    Height = 505
    ParentColor = True
    TabOrder = 2
    UseDockManager = True
    object DBGrid201: TDBGrid
      Left = 1
      Top = 1
      Width = 367
      Height = 484
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource2
      ImeName = '한국어(한글)'
      Options = [dgEditing, dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnEnter = DBGrid201Enter
      OnKeyDown = DBGrid201KeyDown
      OnKeyPress = DBGrid201KeyPress
      OnTitleClick = DBGrid201TitleClick
      Columns = <
        item
          Expanded = False
          FieldName = 'GCODE'
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 40
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GNAME'
          Title.Alignment = taCenter
          Title.Caption = '거래처명'
          Width = 150
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GOSUM'
          Title.Alignment = taCenter
          Title.Caption = '수량'
          Width = 48
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GBSUM'
          Title.Alignment = taCenter
          Title.Caption = '박스'
          Width = 48
          Visible = True
        end
        item
          Expanded = False
          Width = 48
          Visible = True
        end>
    end
    object StBar201: TStatusBar
      Left = 1
      Top = 485
      Width = 367
      Height = 19
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Width = 350
        end
        item
          Width = 50
        end>
      ParentFont = True
      SimplePanel = False
      UseSystemFont = False
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
      Left = 616
      Top = 5
      Width = 336
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
      Left = 512
      Top = 5
      Width = 97
      Height = 19
      Caption = '검색진행'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object ProgressBar1: TProgressBar
      Left = 616
      Top = 5
      Width = 335
      Height = 18
      Min = 0
      Max = 100
      TabOrder = 3
    end
  end
  object Panel001: TFlatPanel
    Left = 2
    Top = 4
    Width = 959
    Height = 37
    Color = clInfoBk
    TabOrder = 0
    UseDockManager = True
    object Label101: TmyLabel3d
      Left = 481
      Top = 9
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
      Left = 8
      Top = 8
      Width = 90
      Height = 22
      Caption = '거래일자'
      ParentColor = True
      TabOrder = 5
      UseDockManager = True
    end
    object Edit101: TFlatMaskEdit
      Left = 104
      Top = 8
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
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Button101: TFlatButton
      Left = 896
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
    object Button301: TFlatButton
      Left = 688
      Top = 6
      Width = 97
      Height = 25
      Caption = '불러오기'
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
      TabOrder = 8
      Visible = False
      OnClick = Button301Click
    end
    object Button401: TFlatButton
      Left = 792
      Top = 6
      Width = 97
      Height = 25
      Caption = '저장하기'
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
      TabOrder = 9
      Visible = False
      OnClick = Button401Click
    end
    object Panel105: TFlatPanel
      Left = 216
      Top = 8
      Width = 90
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 10
      UseDockManager = True
    end
    object Edit103: TFlatEdit
      Left = 312
      Top = 8
      Width = 169
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
      OnKeyPress = Edit114KeyPress
    end
    object Edit105: TFlatEdit
      Left = 496
      Top = 8
      Width = 169
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
      TabOrder = 4
      OnKeyDown = Edit102KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit102: TFlatEdit
      Left = 312
      Top = 8
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
    object Edit104: TFlatEdit
      Left = 496
      Top = 8
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
      TabOrder = 3
      Visible = False
    end
  end
  object Panel102: TFlatPanel
    Left = 222
    Top = 45
    Width = 368
    Height = 17
    Caption = '서울'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clYellow
    Font.Height = -12
    Font.Name = '굴림'
    Font.Style = [fsBold]
    Color = clTeal
    TabOrder = 4
    UseDockManager = True
  end
  object Panel103: TFlatPanel
    Left = 592
    Top = 45
    Width = 369
    Height = 17
    Caption = '지방'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clYellow
    Font.Height = -12
    Font.Name = '굴림'
    Font.Style = [fsBold]
    Color = clTeal
    TabOrder = 5
    UseDockManager = True
  end
  object Panel004: TFlatPanel
    Left = 2
    Top = 45
    Width = 215
    Height = 524
    ParentColor = True
    TabOrder = 6
    UseDockManager = True
    object DBGrid301: TDBGrid
      Left = 1
      Top = 1
      Width = 213
      Height = 504
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource3
      ImeName = '한국어(한글)'
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgCancelOnExit]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      OnTitleClick = DBGrid101TitleClick
      Columns = <
        item
          Expanded = False
          FieldName = 'HCODE'
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 40
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'HNAME'
          Title.Alignment = taCenter
          Title.Caption = '출판사명'
          Width = 142
          Visible = True
        end>
    end
    object StatusBar1: TStatusBar
      Left = 1
      Top = 505
      Width = 213
      Height = 18
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Width = 195
        end
        item
          Width = 50
        end>
      ParentFont = True
      SimplePanel = False
      UseSystemFont = False
    end
  end
  object DataSource1: TDataSource
    DataSet = T3_Sub91
    OnDataChange = DataSource1DataChange
    Left = 10
    Top = 126
  end
  object DataSource2: TDataSource
    DataSet = T3_Sub92
    OnDataChange = DataSource2DataChange
    Left = 42
    Top = 126
  end
  object T3_Sub91: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 10
    Top = 158
    object T3_Sub91SCODE: TStringField
      FieldName = 'SCODE'
      Size = 1
    end
    object T3_Sub91GDATE: TStringField
      FieldName = 'GDATE'
      Size = 10
    end
    object T3_Sub91GUBUN: TStringField
      FieldName = 'GUBUN'
      Size = 10
    end
    object T3_Sub91GCODE: TStringField
      FieldName = 'GCODE'
      Size = 10
    end
    object T3_Sub91GNAME: TStringField
      FieldName = 'GNAME'
      Size = 40
    end
    object T3_Sub91GIQUT: TFloatField
      FieldName = 'GIQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GISUM: TFloatField
      FieldName = 'GISUM'
      EditFormat = '#########0'
    end
    object T3_Sub91GOQUT: TFloatField
      FieldName = 'GOQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GOSUM: TFloatField
      FieldName = 'GOSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GJQUT: TFloatField
      FieldName = 'GJQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GJSUM: TFloatField
      FieldName = 'GJSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GBQUT: TFloatField
      FieldName = 'GBQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GBSUM: TFloatField
      FieldName = 'GBSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GPQUT: TFloatField
      FieldName = 'GPQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GPSUM: TFloatField
      FieldName = 'GPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GSUSU: TFloatField
      FieldName = 'GSUSU'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GSUMX: TFloatField
      FieldName = 'GSUMX'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GSUMY: TFloatField
      FieldName = 'GSUMY'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
  end
  object T3_Sub92: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 42
    Top = 158
    object T3_Sub92SCODE: TStringField
      FieldName = 'SCODE'
      Size = 1
    end
    object T3_Sub92GDATE: TStringField
      FieldName = 'GDATE'
      Size = 10
    end
    object T3_Sub92GUBUN: TStringField
      FieldName = 'GUBUN'
      Size = 10
    end
    object T3_Sub92GCODE: TStringField
      FieldName = 'GCODE'
      Size = 10
    end
    object T3_Sub92GNAME: TStringField
      FieldName = 'GNAME'
      Size = 40
    end
    object T3_Sub92GIQUT: TFloatField
      FieldName = 'GIQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GISUM: TFloatField
      FieldName = 'GISUM'
      EditFormat = '#########0'
    end
    object T3_Sub92GOQUT: TFloatField
      FieldName = 'GOQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GOSUM: TFloatField
      FieldName = 'GOSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GJQUT: TFloatField
      FieldName = 'GJQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GJSUM: TFloatField
      FieldName = 'GJSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GBQUT: TFloatField
      FieldName = 'GBQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GBSUM: TFloatField
      FieldName = 'GBSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GPQUT: TFloatField
      FieldName = 'GPQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GPSUM: TFloatField
      FieldName = 'GPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GSUSU: TFloatField
      FieldName = 'GSUSU'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GSUMX: TFloatField
      FieldName = 'GSUMX'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub92GSUMY: TFloatField
      FieldName = 'GSUMY'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
  end
  object T3_Sub93: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 74
    Top = 158
    object T3_Sub93SCODE: TStringField
      FieldName = 'SCODE'
      Size = 1
    end
    object T3_Sub93BCODE: TStringField
      FieldName = 'BCODE'
      Size = 10
    end
    object T3_Sub93BNAME: TStringField
      FieldName = 'BNAME'
      Size = 40
    end
    object T3_Sub93GCODE: TStringField
      FieldName = 'GCODE'
      Size = 10
    end
    object T3_Sub93GNAME: TStringField
      FieldName = 'GNAME'
      Size = 40
    end
    object T3_Sub93GIQUT: TFloatField
      FieldName = 'GIQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GISUM: TFloatField
      FieldName = 'GISUM'
      EditFormat = '#########0'
    end
    object T3_Sub93GOQUT: TFloatField
      FieldName = 'GOQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GOSUM: TFloatField
      FieldName = 'GOSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GJQUT: TFloatField
      FieldName = 'GJQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GJSUM: TFloatField
      FieldName = 'GJSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GBQUT: TFloatField
      FieldName = 'GBQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GBSUM: TFloatField
      FieldName = 'GBSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GPQUT: TFloatField
      FieldName = 'GPQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GPSUM: TFloatField
      FieldName = 'GPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GSUSU: TFloatField
      FieldName = 'GSUSU'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GSUMX: TFloatField
      FieldName = 'GSUMX'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub93GSUMY: TFloatField
      FieldName = 'GSUMY'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
  end
  object DataSource3: TDataSource
    DataSet = T3_Sub90
    OnDataChange = DataSource1DataChange
    Left = 106
    Top = 126
  end
  object T3_Sub90: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 106
    Top = 158
  end
end
