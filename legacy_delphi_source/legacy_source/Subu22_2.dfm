object Sobo22_2: TSobo22_2
  Left = 71
  Top = 120
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '가입고 현황'
  ClientHeight = 533
  ClientWidth = 901
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
    Width = 895
    Height = 78
    Color = 14416873
    TabOrder = 0
    UseDockManager = True
    object myLabel3d1: TmyLabel3d
      Left = 710
      Top = 64
      Width = 26
      Height = 12
      Caption = '전송'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clRed
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      Visible = False
      AStyle3D = Raised3d
      AShadeLTSet = False
    end
    object Label100: TmyLabel3d
      Left = 664
      Top = 27
      Width = 51
      Height = 16
      Caption = '지점명'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clRed
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      Visible = False
      AStyle3D = Resit3d
      AShadeLTSet = False
    end
    object Label101: TmyLabel3d
      Left = 228
      Top = 31
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
      Top = 28
      Width = 87
      Height = 22
      Caption = '거래일자'
      ParentColor = True
      TabOrder = 7
      UseDockManager = True
    end
    object Panel104: TFlatPanel
      Left = 24
      Top = 52
      Width = 90
      Height = 22
      Caption = '입고처코드'
      ParentColor = True
      Visible = False
      TabOrder = 10
      UseDockManager = True
    end
    object Panel105: TFlatPanel
      Left = 248
      Top = 52
      Width = 90
      Height = 22
      Caption = '입고처명'
      ParentColor = True
      Visible = False
      TabOrder = 11
      UseDockManager = True
    end
    object Panel102: TFlatPanel
      Left = 248
      Top = 4
      Width = 90
      Height = 22
      Caption = '거래구분'
      ParentColor = True
      Visible = False
      TabOrder = 8
      UseDockManager = True
    end
    object Panel103: TFlatPanel
      Left = 432
      Top = 4
      Width = 90
      Height = 22
      Caption = '전표번호'
      ParentColor = True
      Visible = False
      TabOrder = 9
      UseDockManager = True
    end
    object Button101: TFlatButton
      Left = 864
      Top = 16
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
      Layout = blGlyphLeft
      NumGlyphs = 2
      TabOrder = 12
      Visible = False
      OnClick = Button101Click
      BiDiMode = bdLeftToRight
      ParentBiDiMode = False
    end
    object Button201: TFlatButton
      Left = 864
      Top = 40
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
      TabOrder = 13
      Visible = False
      OnClick = Button201Click
    end
    object Edit101: TFlatMaskEdit
      Left = 112
      Top = 28
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
      Text = '2002.01.01'
      OnChange = Edit101Change
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Edit102_1: TFlatComboBox
      Left = 344
      Top = 4
      Width = 57
      Height = 23
      Style = csDropDownList
      Color = clWindow
      DropDownCount = 9
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ItemHeight = 15
      Items.Strings = (
        '입고'
        '반품')
      ParentFont = False
      TabOrder = 2
      Text = '입고'
      Visible = False
      ItemIndex = 0
      OnKeyDown = Edit112KeyDown
      OnKeyPress = Edit112KeyPress
    end
    object Edit103: TFlatEdit
      Left = 184
      Top = 52
      Width = 30
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 2
      ParentFont = False
      TabOrder = 3
      Visible = False
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit104: TFlatEdit
      Left = 120
      Top = 52
      Width = 56
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 5
      ParentFont = False
      TabOrder = 4
      Visible = False
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit105: TFlatEdit
      Left = 344
      Top = 52
      Width = 273
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
      TabOrder = 5
      Visible = False
      OnKeyDown = Edit102KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit106: TFlatComboBox
      Left = 632
      Top = 52
      Width = 113
      Height = 20
      Style = csDropDownList
      Color = clWindow
      DropDownCount = 9
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ItemHeight = 12
      ParentFont = False
      TabOrder = 6
      Visible = False
      ItemIndex = -1
      OnKeyDown = Edit113KeyDown
      OnKeyPress = Edit113KeyPress
    end
    object Edit109: TFlatEdit
      Left = 528
      Top = 4
      Width = 65
      Height = 22
      ColorFlat = clBtnFace
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 2
      ParentFont = False
      TabOrder = 14
      Visible = False
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Button901: TFlatButton
      Left = 592
      Top = 4
      Width = 25
      Height = 22
      Hint = '전표검색'
      Color = clBtnFace
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000130B0000130B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF0033333333B333
        333B33FF33337F3333F73BB3777BB7777BB3377FFFF77FFFF77333B000000000
        0B3333777777777777333330FFFFFFFF07333337F33333337F333330FFFFFFFF
        07333337F3FF3FFF7F333330F00F000F07333337F77377737F333330FFFFFFFF
        07333FF7F3FFFF3F7FFFBBB0F0000F0F0BB37777F7777373777F3BB0FFFFFFFF
        0BBB3777F3FF3FFF77773330F00F000003333337F773777773333330FFFF0FF0
        33333337F3FF7F37F3333330F08F0F0B33333337F7737F77FF333330FFFF003B
        B3333337FFFF77377FF333B000000333BB33337777777F3377FF3BB3333BB333
        3BB33773333773333773B333333B3333333B7333333733333337}
      Layout = blGlyphLeft
      NumGlyphs = 2
      ParentColor = False
      ParentShowHint = False
      ShowHint = True
      TabOrder = 15
      Visible = False
      OnClick = Button901Click
    end
    object Edit102: TFlatMaskEdit
      Left = 240
      Top = 28
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
      TabOrder = 1
      Text = '1999.01.01'
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object dxButton1: TdxButton
      Left = 416
      Top = 15
      Width = 55
      Height = 50
      OnClick = Button101Click
      Caption = '검색'
      TabOrder = 16
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
      Layout = blGlyphTop
    end
    object DateEdit1: TDateEdit
      Left = 209
      Top = 28
      Width = 19
      Height = 22
      BorderStyle = bsNone
      ImeName = 'Microsoft IME 2003'
      NumGlyphs = 2
      StartOfWeek = Sun
      TabOrder = 17
      OnAcceptDate = DateEdit1AcceptDate
      OnButtonClick = DateEdit1ButtonClick
    end
    object DateEdit2: TDateEdit
      Left = 337
      Top = 28
      Width = 19
      Height = 22
      BorderStyle = bsNone
      ImeName = 'Microsoft IME 2003'
      NumGlyphs = 2
      StartOfWeek = Sun
      TabOrder = 18
      OnAcceptDate = DateEdit2AcceptDate
      OnButtonClick = DateEdit2ButtonClick
    end
  end
  object Panel002: TFlatPanel
    Left = 2
    Top = 85
    Width = 895
    Height = 414
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGridEh
      Left = 1
      Top = 1
      Width = 893
      Height = 376
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      DrawMemoText = True
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      FooterColor = 16311512
      FooterFont.Charset = HANGEUL_CHARSET
      FooterFont.Color = clWindowText
      FooterFont.Height = -12
      FooterFont.Name = '굴림'
      FooterFont.Style = [fsBold]
      ImeName = '한국어 입력 시스템 (IME 2000)'
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgConfirmDelete, dgCancelOnExit]
      ParentFont = False
      ReadOnly = True
      RowLines = 3
      TabOrder = 1
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      Columns = <
        item
          EditButtons = <>
          FieldName = 'GNAME'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '출판사'
          Width = 150
        end
        item
          EditButtons = <>
          FieldName = 'GDATE'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '거래일자'
          Width = 75
        end
        item
          EditButtons = <>
          FieldName = 'SDATE'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '출고예정일'
          Width = 75
        end
        item
          EditButtons = <>
          FieldName = 'MEMO1'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '도서명 / 메모'
          Width = 250
        end
        item
          Color = 12056530
          EditButtons = <>
          FieldName = 'GSQUT'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '수  량'
          Width = 50
        end
        item
          EditButtons = <>
          FieldName = 'GDANG'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '단  가'
          Width = 50
        end
        item
          EditButtons = <>
          FieldName = 'GBIGO'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '담당자'
          Width = 80
        end
        item
          Checkboxes = True
          EditButtons = <>
          FieldName = 'CODE1'
          Footers = <>
          KeyList.Strings = (
            'O;On'
            'N;Off')
          Title.Alignment = taCenter
          Title.Caption = '신간'
          Width = 41
        end
        item
          Checkboxes = True
          EditButtons = <>
          FieldName = 'CODE2'
          Footers = <>
          KeyList.Strings = (
            'O;On'
            'N;Off')
          Title.Alignment = taCenter
          Title.Caption = '요청'
          Width = 41
        end
        item
          Checkboxes = True
          EditButtons = <>
          FieldName = 'CODE3'
          Footers = <>
          KeyList.Strings = (
            'O;On'
            'N;Off')
          Title.Alignment = taCenter
          Title.Caption = '수락'
          Width = 41
        end>
    end
    object StBar101: TStatusBar
      Left = 1
      Top = 377
      Width = 893
      Height = 18
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Text = '요청시간'
          Width = 92
        end
        item
          Bevel = pbRaised
          Width = 296
        end>
      SimplePanel = False
      UseSystemFont = False
    end
    object StBar102: TStatusBar
      Left = 1
      Top = 395
      Width = 893
      Height = 18
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Text = '수락시간'
          Width = 92
        end
        item
          Bevel = pbRaised
          Width = 296
        end>
      SimplePanel = False
      UseSystemFont = False
    end
  end
  object Panel007: TFlatPanel
    Left = 2
    Top = 502
    Width = 895
    Height = 29
    Color = clInfoBk
    TabOrder = 2
    UseDockManager = True
    object ProgressBar0: TFlatProgressBar
      Left = 552
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
      Left = 448
      Top = 5
      Width = 97
      Height = 19
      Caption = '검색진행'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object ProgressBar1: TProgressBar
      Left = 552
      Top = 5
      Width = 335
      Height = 18
      Min = 0
      Max = 100
      TabOrder = 3
    end
  end
  object Panel401: TFlatPanel
    Left = 304
    Top = 364
    Width = 305
    Height = 101
    Color = clAqua
    Visible = False
    TabOrder = 3
    UseDockManager = True
  end
  object DataSource1: TDataSource
    DataSet = T2_Sub21
    OnDataChange = DataSource1DataChange
    Left = 10
    Top = 126
  end
  object DataSource2: TDataSource
    OnDataChange = DataSource2DataChange
    Left = 42
    Top = 126
  end
  object T2_Sub21: TClientDataSet
    Aggregates = <>
    Params = <>
    BeforeClose = T2_Sub21BeforeClose
    BeforePost = T2_Sub21BeforePost
    AfterPost = T2_Sub21AfterPost
    AfterCancel = T2_Sub21AfterCancel
    BeforeScroll = T2_Sub21AfterScroll
    AfterScroll = T2_Sub21AfterScroll
    OnNewRecord = T2_Sub21NewRecord
    Left = 10
    Top = 158
    object T2_Sub21ID: TFloatField
      FieldName = 'ID'
    end
    object T2_Sub21IDNUM: TFloatField
      FieldName = 'IDNUM'
    end
    object T2_Sub21GDATE: TStringField
      FieldName = 'GDATE'
      EditMask = '!0000.!90.90;1; '
      Size = 10
    end
    object T2_Sub21SDATE: TStringField
      FieldName = 'SDATE'
      EditMask = '!0000.!90.90;1; '
      Size = 10
    end
    object T2_Sub21GCODE: TStringField
      FieldName = 'GCODE'
      Size = 5
    end
    object T2_Sub21GNAME: TStringField
      FieldName = 'GNAME'
      Size = 100
    end
    object T2_Sub21HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object T2_Sub21OCODE: TStringField
      DisplayWidth = 4
      FieldName = 'OCODE'
      Size = 1
    end
    object T2_Sub21BCODE: TStringField
      FieldName = 'BCODE'
      Size = 10
    end
    object T2_Sub21BNAME: TStringField
      FieldName = 'BNAME'
      Size = 100
    end
    object T2_Sub21GJEJA: TStringField
      FieldName = 'GJEJA'
      Size = 30
    end
    object T2_Sub21GUBUN: TStringField
      FieldName = 'GUBUN'
      Size = 4
    end
    object T2_Sub21JUBUN: TStringField
      FieldName = 'JUBUN'
      Size = 2
    end
    object T2_Sub21PUBUN: TStringField
      FieldName = 'PUBUN'
      Size = 4
    end
    object T2_Sub21GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub21QSQUT: TFloatField
      FieldName = 'QSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub21GDANG: TFloatField
      FieldName = 'GDANG'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub21GRAT1: TSmallintField
      FieldName = 'GRAT1'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub21GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub21JEAGO: TFloatField
      FieldName = 'JEAGO'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub21GBIGO: TStringField
      FieldName = 'GBIGO'
      Size = 50
    end
    object T2_Sub21YESNO: TStringField
      FieldName = 'YESNO'
      Size = 5
    end
    object T2_Sub21GJISA: TStringField
      FieldName = 'GJISA'
      Size = 30
    end
    object T2_Sub21MEMO1: TMemoField
      FieldName = 'MEMO1'
      BlobType = ftMemo
    end
    object T2_Sub21TIME1: TStringField
      FieldName = 'TIME1'
      Size = 50
    end
    object T2_Sub21TIME3: TStringField
      FieldName = 'TIME3'
      Size = 50
    end
    object T2_Sub21CODE1: TStringField
      FieldName = 'CODE1'
      Size = 2
    end
    object T2_Sub21CODE2: TStringField
      FieldName = 'CODE2'
      Size = 2
    end
    object T2_Sub21CODE3: TStringField
      FieldName = 'CODE3'
      Size = 2
    end
  end
  object T2_Sub22: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 42
    Top = 158
    object T2_Sub22ID: TFloatField
      FieldName = 'ID'
    end
    object T2_Sub22IDNUM: TFloatField
      FieldName = 'IDNUM'
    end
    object T2_Sub22GDATE: TStringField
      FieldName = 'GDATE'
      EditMask = '!0000.!90.90;1; '
      Size = 10
    end
    object T2_Sub22SCODE: TStringField
      FieldName = 'SCODE'
      Size = 1
    end
    object T2_Sub22GCODE: TStringField
      FieldName = 'GCODE'
      Size = 5
    end
    object T2_Sub22GNAME: TStringField
      FieldName = 'GNAME'
      Size = 100
    end
    object T2_Sub22HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object T2_Sub22OCODE: TStringField
      DisplayWidth = 4
      FieldName = 'OCODE'
      Size = 1
    end
    object T2_Sub22BCODE: TStringField
      FieldName = 'BCODE'
      Size = 10
    end
    object T2_Sub22BNAME: TStringField
      FieldName = 'BNAME'
      Size = 100
    end
    object T2_Sub22GJEJA: TStringField
      FieldName = 'GJEJA'
      Size = 30
    end
    object T2_Sub22GUBUN: TStringField
      FieldName = 'GUBUN'
      Size = 4
    end
    object T2_Sub22JUBUN: TStringField
      FieldName = 'JUBUN'
      Size = 2
    end
    object T2_Sub22PUBUN: TStringField
      FieldName = 'PUBUN'
      Size = 4
    end
    object T2_Sub22GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub22QSQUT: TFloatField
      FieldName = 'QSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub22GDANG: TFloatField
      FieldName = 'GDANG'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub22GRAT1: TSmallintField
      FieldName = 'GRAT1'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub22GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub22JEAGO: TFloatField
      FieldName = 'JEAGO'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T2_Sub22GBIGO: TStringField
      FieldName = 'GBIGO'
      Size = 50
    end
    object T2_Sub22YESNO: TStringField
      FieldName = 'YESNO'
      Size = 5
    end
    object T2_Sub22GJISA: TStringField
      FieldName = 'GJISA'
      Size = 30
    end
  end
end
