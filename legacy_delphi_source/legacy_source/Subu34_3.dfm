object Sobo34_3: TSobo34_3
  Left = 71
  Top = 120
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '기간별재고원장(상세)-비품'
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
  object CornerButton1: TCornerButton
    Left = 4
    Top = 3
    Width = 21
    Height = 79
    Cursor = crArrow
    BevelColor = clRed
    BevelWidth = 1
    MouseDownColor = clRed
    Transparent = False
    CornerOptions = [cnTopLeft, cnBottomLeft]
    CornerSize = 10
  end
  object CornerButton2: TCornerButton
    Left = 4
    Top = 84
    Width = 21
    Height = 207
    Cursor = crArrow
    BevelColor = clBlue
    BevelWidth = 1
    MouseDownColor = clBlue
    Transparent = False
    CornerOptions = [cnTopLeft, cnBottomLeft]
    CornerSize = 10
  end
  object CornerButton3: TCornerButton
    Left = 4
    Top = 292
    Width = 21
    Height = 207
    Cursor = crArrow
    BevelColor = clTeal
    BevelWidth = 1
    MouseDownColor = clTeal
    Transparent = False
    CornerOptions = [cnTopLeft, cnBottomLeft]
    CornerSize = 10
  end
  object CornerButton9: TCornerButton
    Left = 4
    Top = 501
    Width = 21
    Height = 30
    Cursor = crArrow
    BevelColor = clBlack
    BevelWidth = 1
    MouseDownColor = clBlack
    Transparent = False
    CornerOptions = [cnTopLeft, cnBottomLeft]
    CornerSize = 10
  end
  object Label301: TmyLabel3d
    Left = 9
    Top = 27
    Width = 13
    Height = 26
    Caption = '조'#13#10'회'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clRed
    Font.Height = -13
    Font.Name = '굴림'
    Font.Style = []
    ParentColor = False
    ParentFont = False
    Transparent = True
    AShadeLTSet = False
  end
  object Label302: TmyLabel3d
    Left = 9
    Top = 160
    Width = 13
    Height = 52
    Caption = '검'#13#10'색'#13#10'자'#13#10'료'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clBlue
    Font.Height = -13
    Font.Name = '굴림'
    Font.Style = []
    ParentColor = False
    ParentFont = False
    Transparent = True
    AShadeLTSet = False
  end
  object Label303: TmyLabel3d
    Left = 9
    Top = 360
    Width = 13
    Height = 52
    Caption = '검'#13#10'색'#13#10'자'#13#10'료'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clTeal
    Font.Height = -13
    Font.Name = '굴림'
    Font.Style = []
    ParentColor = False
    ParentFont = False
    Transparent = True
    AShadeLTSet = False
  end
  object Label309: TmyLabel3d
    Left = 10
    Top = 505
    Width = 12
    Height = 24
    Caption = '상'#13#10'태'
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
  object Panel001: TFlatPanel
    Left = 24
    Top = 4
    Width = 873
    Height = 78
    Color = 14416873
    TabOrder = 0
    UseDockManager = True
    object Label101: TmyLabel3d
      Left = 220
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
    object Label102: TmyLabel3d
      Left = 553
      Top = 29
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
      Width = 87
      Height = 22
      Caption = '거래일자'
      ParentColor = True
      TabOrder = 8
      UseDockManager = True
    end
    object Panel102: TFlatPanel
      Left = 368
      Top = 12
      Width = 87
      Height = 53
      Caption = '도 서 명'
      ParentColor = True
      TabOrder = 9
      UseDockManager = True
    end
    object Button101: TFlatButton
      Left = 840
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
      NumGlyphs = 2
      TabOrder = 10
      Visible = False
      OnClick = Button101Click
    end
    object Button201: TFlatButton
      Left = 840
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
      TabOrder = 11
      Visible = False
      OnClick = Button201Click
    end
    object Edit101: TFlatMaskEdit
      Left = 104
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
    object Edit102: TFlatMaskEdit
      Left = 232
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
      TabOrder = 1
      Text = '1999.01.01'
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Edit104: TFlatEdit
      Left = 456
      Top = 12
      Width = 193
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 80
      ParentFont = False
      TabOrder = 5
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit106: TFlatEdit
      Left = 456
      Top = 44
      Width = 193
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 80
      ParentFont = False
      TabOrder = 7
      OnChange = Edit101Change
      OnKeyDown = Edit102KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit103: TFlatEdit
      Left = 456
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
      TabOrder = 4
      Visible = False
    end
    object Edit105: TFlatEdit
      Left = 456
      Top = 44
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
      TabOrder = 6
      Visible = False
    end
    object CheckBox2: TFlatCheckBox
      Left = 672
      Top = 15
      Width = 113
      Height = 17
      Caption = '본사출고->변경'
      Color = 14416873
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 12
      TabStop = True
      Visible = False
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object DateEdit1: TDateEdit
      Left = 201
      Top = 12
      Width = 19
      Height = 22
      BorderStyle = bsNone
      ImeName = 'Microsoft IME 2003'
      NumGlyphs = 2
      StartOfWeek = Sun
      TabOrder = 13
      OnAcceptDate = DateEdit1AcceptDate
      OnButtonClick = DateEdit1ButtonClick
    end
    object DateEdit2: TDateEdit
      Left = 329
      Top = 12
      Width = 19
      Height = 22
      BorderStyle = bsNone
      ImeName = 'Microsoft IME 2003'
      NumGlyphs = 2
      StartOfWeek = Sun
      TabOrder = 14
      OnAcceptDate = DateEdit2AcceptDate
      OnButtonClick = DateEdit2ButtonClick
    end
    object Button701: TFlatButton
      Left = 648
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
      TabOrder = 15
      OnClick = Button701Click
    end
    object Button702: TFlatButton
      Left = 648
      Top = 44
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
      TabOrder = 16
      OnClick = Button702Click
    end
    object dxButton1: TdxButton
      Left = 790
      Top = 15
      Width = 65
      Height = 50
      OnClick = Button101Click
      Caption = '검색'
      TabOrder = 17
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
    object Panel103: TFlatPanel
      Left = 16
      Top = 44
      Width = 87
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 18
      UseDockManager = True
    end
    object Edit108: TFlatEdit
      Left = 104
      Top = 44
      Width = 225
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
    object Edit107: TFlatEdit
      Left = 104
      Top = 44
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
    object Button700: TFlatButton
      Left = 328
      Top = 44
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
      TabOrder = 19
    end
  end
  object Panel002: TFlatPanel
    Left = 24
    Top = 85
    Width = 873
    Height = 206
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGridEh
      Left = 1
      Top = 1
      Width = 871
      Height = 204
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource2
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
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      ParentFont = False
      SumList.Active = True
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      TitleHeight = 10
      UseMultiTitle = True
      VTitleMargin = 5
      OnDblClick = Button007Click
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      OnTitleClick = DBGrid101TitleClick
      Columns = <
        item
          EditButtons = <>
          FieldName = 'GNAME'
          Footer.Value = '합계'
          Footer.ValueType = fvtStaticText
          Footers = <>
          Title.Caption = '분 류 명'
          Width = 309
        end
        item
          Color = 12056530
          EditButtons = <>
          FieldName = 'GSUSU'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '전재고'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'bBQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = ' 반품'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'GISUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '반입'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'aPSUM'
          Footers = <>
          Title.Caption = '파손'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'bPQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = ' 폐기'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'bPSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '변경'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'xSQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '기타'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'xSQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '기타'
          Width = 58
        end
        item
          Color = 11861755
          EditButtons = <>
          FieldName = 'GSSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '현재고'
          Width = 58
        end>
    end
  end
  object Panel003: TFlatPanel
    Left = 24
    Top = 293
    Width = 873
    Height = 206
    ParentColor = True
    TabOrder = 2
    UseDockManager = True
    object DBGrid201: TDBGridEh
      Left = 1
      Top = 1
      Width = 871
      Height = 204
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
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      ParentFont = False
      SumList.Active = True
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      TitleHeight = 10
      OnKeyDown = DBGrid201KeyDown
      OnKeyPress = DBGrid201KeyPress
      OnTitleClick = DBGrid201TitleClick
      Columns = <
        item
          EditButtons = <>
          FieldName = 'GNAME'
          Footer.Value = '합계'
          Footer.ValueType = fvtStaticText
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '도 서 명'
          Width = 309
        end
        item
          Color = 12056530
          EditButtons = <>
          FieldName = 'GSUSU'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '전재고'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'bBQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '반품'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'GISUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '반입'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'aPSUM'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '파손'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'bPQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '폐기'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'bPSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '변경'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'xSQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '기타'
          Width = 58
        end
        item
          EditButtons = <>
          FieldName = 'xSQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '기타'
          Width = 58
        end
        item
          Color = 11861755
          EditButtons = <>
          FieldName = 'GSSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '현재고'
          Width = 58
        end>
    end
  end
  object Panel007: TFlatPanel
    Left = 24
    Top = 502
    Width = 905
    Height = 29
    Color = clInfoBk
    TabOrder = 3
    UseDockManager = True
    object ProgressBar0: TFlatProgressBar
      Left = 536
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
      Left = 432
      Top = 5
      Width = 97
      Height = 19
      Caption = '검색진행'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object ProgressBar1: TProgressBar
      Left = 536
      Top = 5
      Width = 335
      Height = 18
      Min = 0
      Max = 100
      TabOrder = 3
    end
  end
  object DataSource1: TDataSource
    DataSet = T3_Sub41
    OnDataChange = DataSource1DataChange
    Left = 42
    Top = 126
  end
  object DataSource2: TDataSource
    DataSet = T3_Sub42
    OnDataChange = DataSource2DataChange
    Left = 74
    Top = 126
  end
  object T3_Sub41: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 42
    Top = 158
    object T3_Sub41GDATE: TStringField
      FieldName = 'GDATE'
      Size = 10
    end
    object T3_Sub41GUBUN: TStringField
      FieldName = 'GUBUN'
      Size = 10
    end
    object T3_Sub41GCODE: TStringField
      FieldName = 'GCODE'
      Size = 10
    end
    object T3_Sub41GNAME: TStringField
      FieldName = 'GNAME'
      Size = 100
    end
    object T3_Sub41GIQUT: TFloatField
      FieldName = 'GIQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GISUM: TFloatField
      FieldName = 'GISUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GOQUT: TFloatField
      FieldName = 'GOQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GOSUM: TFloatField
      FieldName = 'GOSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GJQUT: TFloatField
      FieldName = 'GJQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GJSUM: TFloatField
      FieldName = 'GJSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GBQUT: TFloatField
      FieldName = 'GBQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GBSUM: TFloatField
      FieldName = 'GBSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GPQUT: TFloatField
      FieldName = 'GPQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GPSUM: TFloatField
      FieldName = 'GPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GSUSU: TFloatField
      FieldName = 'GSUSU'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GSUMX: TFloatField
      FieldName = 'GSUMX'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41GSUMY: TFloatField
      FieldName = 'GSUMY'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41aBQUT: TFloatField
      FieldName = 'aBQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41aPQUT: TFloatField
      FieldName = 'aPQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41aPSUM: TFloatField
      FieldName = 'aPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41bBQUT: TFloatField
      FieldName = 'bBQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41bPQUT: TFloatField
      FieldName = 'bPQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41bPSUM: TFloatField
      FieldName = 'bPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub41xSQUT: TFloatField
      FieldName = 'xSQUT'
      DisplayFormat = '###,###,###0'
    end
  end
  object T3_Sub42: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 74
    Top = 158
    object T3_Sub42GDATE: TStringField
      FieldName = 'GDATE'
      Size = 10
    end
    object T3_Sub42GUBUN: TStringField
      FieldName = 'GUBUN'
      Size = 10
    end
    object T3_Sub42GCODE: TStringField
      FieldName = 'GCODE'
      Size = 10
    end
    object T3_Sub42GNAME: TStringField
      FieldName = 'GNAME'
      Size = 100
    end
    object T3_Sub42GIQUT: TFloatField
      FieldName = 'GIQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GISUM: TFloatField
      FieldName = 'GISUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GOQUT: TFloatField
      FieldName = 'GOQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GOSUM: TFloatField
      FieldName = 'GOSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GJQUT: TFloatField
      FieldName = 'GJQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GJSUM: TFloatField
      FieldName = 'GJSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GBQUT: TFloatField
      FieldName = 'GBQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GBSUM: TFloatField
      FieldName = 'GBSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GPQUT: TFloatField
      FieldName = 'GPQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GPSUM: TFloatField
      FieldName = 'GPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GSUSU: TFloatField
      FieldName = 'GSUSU'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GSUMX: TFloatField
      FieldName = 'GSUMX'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42GSUMY: TFloatField
      FieldName = 'GSUMY'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42aBQUT: TFloatField
      FieldName = 'aBQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42aPQUT: TFloatField
      FieldName = 'aPQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42aPSUM: TFloatField
      FieldName = 'aPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42bBQUT: TFloatField
      FieldName = 'bBQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42bPQUT: TFloatField
      FieldName = 'bPQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42bPSUM: TFloatField
      FieldName = 'bPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub42xSQUT: TFloatField
      FieldName = 'xSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
  end
end
