object Sobo55: TSobo55
  Left = 22
  Top = 104
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '일별 반품내역서'
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
      Left = 657
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
      TabOrder = 6
      UseDockManager = True
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
      Left = 368
      Top = 12
      Width = 90
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 7
      UseDockManager = True
    end
    object Edit104: TFlatEdit
      Left = 464
      Top = 12
      Width = 177
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
      TabOrder = 3
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit103: TFlatEdit
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
    object Edit106: TFlatEdit
      Left = 672
      Top = 12
      Width = 177
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
      OnKeyDown = Edit102KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit105: TFlatEdit
      Left = 672
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
      TabOrder = 8
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
      TabOrder = 9
      Visible = False
      OnClick = Button201Click
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
      StartOfWeek = Sun
      TabOrder = 11
      OnAcceptDate = DateEdit2AcceptDate
      OnButtonClick = DateEdit2ButtonClick
    end
    object Button701: TFlatButton
      Left = 640
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
      OnClick = Button701Click
    end
    object Button702: TFlatButton
      Left = 848
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
      OnClick = Button702Click
    end
    object Button709: TFlatButton
      Left = 880
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
      TabOrder = 14
      OnClick = Button101Click
    end
  end
  object Panel002: TFlatPanel
    Left = 2
    Top = 56
    Width = 567
    Height = 185
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGrid
      Left = 1
      Top = 1
      Width = 565
      Height = 165
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource2
      ImeName = '한국어(한글)'
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgConfirmDelete, dgCancelOnExit]
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
          Alignment = taCenter
          Expanded = False
          FieldName = 'GDATE'
          Title.Alignment = taCenter
          Title.Caption = '거래일자'
          Width = 80
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'HCODE'
          Title.Alignment = taCenter
          Title.Caption = '출판사코드'
          Width = 80
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'HNAME'
          Title.Alignment = taCenter
          Title.Caption = '출판사명'
          Width = 374
          Visible = True
        end>
    end
    object StBar101: TStatusBar
      Left = 1
      Top = 166
      Width = 565
      Height = 18
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Width = 546
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
    Top = 248
    Width = 959
    Height = 321
    ParentColor = True
    TabOrder = 2
    UseDockManager = True
    object DBGrid201: TDBGrid
      Left = 1
      Top = 1
      Width = 957
      Height = 301
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ImeName = '한국어(한글)'
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgRowSelect, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      ParentFont = False
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnDblClick = DBGrid201DblClick
      OnKeyDown = DBGrid201KeyDown
      OnKeyPress = DBGrid201KeyPress
      OnTitleClick = DBGrid201TitleClick
      Columns = <
        item
          Expanded = False
          FieldName = 'GCODE'
          Title.Alignment = taCenter
          Title.Caption = '거래처코드'
          Width = 70
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GNAME'
          Title.Alignment = taCenter
          Title.Caption = '거래처명'
          Width = 210
          Visible = True
        end
        item
          Alignment = taCenter
          Expanded = False
          FieldName = 'IDNUM'
          Title.Alignment = taCenter
          Title.Caption = 'No'
          Width = 50
          Visible = True
        end
        item
          Alignment = taCenter
          Expanded = False
          FieldName = 'PUBUN'
          Title.Alignment = taCenter
          Title.Caption = '출고구분'
          Width = 70
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'BCODE'
          Title.Alignment = taCenter
          Title.Caption = '도서코드'
          Width = 70
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'BNAME'
          Title.Alignment = taCenter
          Title.Caption = '도서명'
          Width = 210
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GDANG'
          Title.Alignment = taCenter
          Title.Caption = '정가'
          Width = 60
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GSQUT'
          Title.Alignment = taCenter
          Title.Caption = '수량'
          Width = 60
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GRAT1'
          Title.Alignment = taCenter
          Title.Caption = '비율'
          Width = 38
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GSSUM'
          Title.Alignment = taCenter
          Title.Caption = '금액'
          Width = 80
          Visible = True
        end>
    end
    object StBar201: TStatusBar
      Left = 1
      Top = 302
      Width = 957
      Height = 18
      Panels = <
        item
          Alignment = taCenter
          Bevel = pbRaised
          Text = '합계'
          Width = 81
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 616
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 122
        end
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 119
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
    Left = 576
    Top = 56
    Width = 385
    Height = 185
    Color = clInfoBk
    TabOrder = 4
    UseDockManager = True
    object Panel201: TFlatPanel
      Left = 32
      Top = 20
      Width = 90
      Height = 22
      Caption = '총 출판사수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 2
      UseDockManager = True
    end
    object Panel202: TFlatPanel
      Left = 32
      Top = 60
      Width = 90
      Height = 22
      Caption = '총 건수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 3
      UseDockManager = True
    end
    object Edit202: TFlatEdit
      Left = 128
      Top = 60
      Width = 225
      Height = 21
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
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
      Left = 128
      Top = 20
      Width = 225
      Height = 21
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 5
      ParentFont = False
      ReadOnly = True
      TabOrder = 0
    end
    object Panel203: TFlatPanel
      Left = 32
      Top = 100
      Width = 90
      Height = 22
      Caption = '총 권수'
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
    object Edit203: TFlatEdit
      Left = 128
      Top = 100
      Width = 225
      Height = 21
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 5
      ParentFont = False
      ReadOnly = True
      TabOrder = 5
    end
    object Panel204: TFlatPanel
      Left = 32
      Top = 140
      Width = 90
      Height = 22
      Caption = '총 금액'
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
    object Edit204: TFlatEdit
      Left = 128
      Top = 140
      Width = 225
      Height = 21
      ColorFlat = 15724527
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 5
      ParentFont = False
      ReadOnly = True
      TabOrder = 7
    end
  end
  object DataSource1: TDataSource
    DataSet = Base10.T5_Sub51
    OnDataChange = DataSource1DataChange
    Left = 10
    Top = 126
  end
  object DataSource2: TDataSource
    DataSet = Base10.T5_Sub52
    OnDataChange = DataSource2DataChange
    Left = 42
    Top = 126
  end
end
