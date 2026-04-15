object Sobo66: TSobo66
  Left = 200
  Top = 120
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '거래처출고현황'
  ClientHeight = 533
  ClientWidth = 772
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
    Width = 767
    Height = 78
    Color = clInfoBk
    TabOrder = 0
    UseDockManager = True
    object Label101: TmyLabel3d
      Left = 225
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
    object Label102: TmyLabel3d
      Left = 329
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
      Visible = False
      AShadeLTSet = False
    end
    object Panel101: TFlatPanel
      Left = 16
      Top = 12
      Width = 90
      Height = 22
      Caption = '거래일자'
      ParentColor = True
      TabOrder = 12
      UseDockManager = True
    end
    object Panel102: TFlatPanel
      Left = 16
      Top = 44
      Width = 90
      Height = 22
      Caption = '거래처명'
      ParentColor = True
      TabOrder = 14
      UseDockManager = True
    end
    object Button101: TFlatButton
      Left = 736
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
      TabOrder = 15
      Visible = False
      OnClick = Button101Click
    end
    object Button201: TFlatButton
      Left = 736
      Top = 48
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
      TabOrder = 16
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
    object Edit102: TFlatMaskEdit
      Left = 240
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
      Left = 222
      Top = 44
      Width = 129
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
      TabOrder = 5
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit106: TFlatEdit
      Left = 355
      Top = 44
      Width = 129
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
      TabOrder = 7
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit108: TFlatEdit
      Left = 488
      Top = 44
      Width = 129
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
      TabOrder = 9
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit110: TFlatEdit
      Left = 621
      Top = 44
      Width = 129
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
      TabOrder = 11
      OnChange = Edit101Change
      OnKeyDown = Edit102KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit103: TFlatEdit
      Left = 222
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
      TabOrder = 4
      Visible = False
    end
    object Edit105: TFlatEdit
      Left = 355
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
    object Edit107: TFlatEdit
      Left = 488
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
      TabOrder = 8
      Visible = False
    end
    object Edit109: TFlatEdit
      Left = 621
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
      TabOrder = 10
      Visible = False
    end
    object Panel103: TFlatPanel
      Left = 368
      Top = 12
      Width = 90
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 13
      UseDockManager = True
    end
    object Edit112: TFlatEdit
      Left = 464
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
      MaxLength = 40
      ParentFont = False
      TabOrder = 3
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit111: TFlatEdit
      Left = 464
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
    object DateEdit1: TDateEdit
      Left = 209
      Top = 12
      Width = 19
      Height = 22
      BorderStyle = bsNone
      ImeName = 'Microsoft IME 2003'
      NumGlyphs = 2
      TabOrder = 17
      OnAcceptDate = DateEdit1AcceptDate
      OnButtonClick = DateEdit1ButtonClick
    end
    object DateEdit2: TDateEdit
      Left = 337
      Top = 12
      Width = 19
      Height = 22
      BorderStyle = bsNone
      ImeName = 'Microsoft IME 2003'
      NumGlyphs = 2
      TabOrder = 18
      OnAcceptDate = DateEdit2AcceptDate
      OnButtonClick = DateEdit2ButtonClick
    end
    object Button700: TFlatButton
      Left = 656
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
      TabOrder = 19
      OnClick = Button700Click
    end
    object Button701: TFlatButton
      Left = 331
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
      TabOrder = 20
      OnClick = Button701Click
    end
    object Button702: TFlatButton
      Left = 464
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
      TabOrder = 21
      OnClick = Button702Click
    end
    object Button703: TFlatButton
      Left = 597
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
      TabOrder = 22
      OnClick = Button703Click
    end
    object Button704: TFlatButton
      Left = 730
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
      TabOrder = 23
      OnClick = Button704Click
    end
    object Button709: TFlatButton
      Left = 686
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
      TabOrder = 24
      OnClick = Button101Click
    end
    object CheckBox2: TFlatCheckBox
      Left = 120
      Top = 47
      Width = 89
      Height = 17
      Caption = '본사출고제외'
      Color = clInfoBk
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -11
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 25
      TabStop = True
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
  end
  object Panel002: TFlatPanel
    Left = 2
    Top = 85
    Width = 767
    Height = 206
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGrid
      Left = 1
      Top = 1
      Width = 765
      Height = 186
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource2
      ImeName = '한국어(한글)'
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnDblClick = Button007Click
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      OnTitleClick = DBGrid101TitleClick
      Columns = <
        item
          Expanded = False
          FieldName = 'GNAME'
          Title.Alignment = taCenter
          Title.Caption = '도서분류'
          Width = 208
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GIQUT'
          Title.Alignment = taCenter
          Title.Caption = '출고'
          Width = 65
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GISUM'
          Title.Alignment = taCenter
          Title.Caption = '반품'
          Width = 65
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GOQUT'
          Title.Alignment = taCenter
          Title.Caption = '출고'
          Width = 65
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GOSUM'
          Title.Alignment = taCenter
          Title.Caption = '반품'
          Width = 65
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GJQUT'
          Title.Alignment = taCenter
          Title.Caption = '출고'
          Width = 65
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GJSUM'
          Title.Alignment = taCenter
          Title.Caption = '반품'
          Width = 65
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GBQUT'
          Title.Alignment = taCenter
          Title.Caption = '출고'
          Width = 65
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GBSUM'
          Title.Alignment = taCenter
          Title.Caption = '반품'
          Width = 65
          Visible = True
        end>
    end
    object StBar101: TStatusBar
      Left = 1
      Top = 187
      Width = 765
      Height = 18
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Text = '합  계'
          Width = 220
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
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
    Left = 2
    Top = 293
    Width = 767
    Height = 206
    ParentColor = True
    TabOrder = 2
    UseDockManager = True
    object DBGrid201: TDBGrid
      Left = 1
      Top = 1
      Width = 765
      Height = 186
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      ImeName = '한국어(한글)'
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnKeyDown = DBGrid201KeyDown
      OnKeyPress = DBGrid201KeyPress
      OnTitleClick = DBGrid201TitleClick
      Columns = <
        item
          Expanded = False
          FieldName = 'GNAME'
          Title.Alignment = taCenter
          Title.Caption = '도 서 명'
          Width = 208
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GIQUT'
          Title.Alignment = taCenter
          Title.Caption = '출고'
          Width = 65
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GISUM'
          Title.Alignment = taCenter
          Title.Caption = '반품'
          Width = 65
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GOQUT'
          Title.Alignment = taCenter
          Title.Caption = '출고'
          Width = 65
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GOSUM'
          Title.Alignment = taCenter
          Title.Caption = '반품'
          Width = 65
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GJQUT'
          Title.Alignment = taCenter
          Title.Caption = '출고'
          Width = 65
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GJSUM'
          Title.Alignment = taCenter
          Title.Caption = '반품'
          Width = 65
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GBQUT'
          Title.Alignment = taCenter
          Title.Caption = '출고'
          Width = 65
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GBSUM'
          Title.Alignment = taCenter
          Title.Caption = '반품'
          Width = 65
          Visible = True
        end>
    end
    object StBar201: TStatusBar
      Left = 1
      Top = 187
      Width = 765
      Height = 18
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Text = '합  계'
          Width = 220
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 66
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
    Top = 502
    Width = 767
    Height = 29
    Color = clInfoBk
    TabOrder = 3
    UseDockManager = True
    object ProgressBar0: TFlatProgressBar
      Left = 424
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
      Width = 335
      Height = 18
      Min = 0
      Max = 100
      TabOrder = 3
    end
  end
  object DataSource1: TDataSource
    DataSet = Base10.T6_Sub61
    OnDataChange = DataSource1DataChange
    Left = 10
    Top = 126
  end
  object DataSource2: TDataSource
    DataSet = Base10.T6_Sub62
    OnDataChange = DataSource2DataChange
    Left = 42
    Top = 126
  end
end
