object Seek70: TSeek70
  Left = 200
  Top = 232
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '신간발행'
  ClientHeight = 401
  ClientWidth = 614
  Color = clBtnFace
  Font.Charset = HANGEUL_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = '굴림'
  Font.Style = [fsBold]
  OldCreateOrder = False
  Position = poScreenCenter
  OnActivate = FormActivate
  OnClose = FormClose
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 12
  object Panel100: TFlatPanel
    Left = 8
    Top = 8
    Width = 601
    Height = 65
    Color = clInfoBk
    TabOrder = 0
    UseDockManager = True
    object Panel101: TFlatPanel
      Left = 16
      Top = 7
      Width = 73
      Height = 22
      Caption = '도서코드'
      ParentColor = True
      TabOrder = 0
      UseDockManager = True
    end
    object Edit1: TFlatEdit
      Left = 96
      Top = 7
      Width = 73
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 1
      OnKeyPress = Edit1KeyPress
    end
    object Panel102: TFlatPanel
      Left = 184
      Top = 7
      Width = 73
      Height = 22
      Caption = '전표구분'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object Edit2: TFlatEdit
      Left = 264
      Top = 7
      Width = 25
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 3
    end
    object Panel103: TFlatPanel
      Left = 304
      Top = 7
      Width = 73
      Height = 22
      Caption = '단  가'
      ParentColor = True
      TabOrder = 4
      UseDockManager = True
    end
    object Edit3: TFlatNumber
      Left = 384
      Top = 7
      Width = 65
      Height = 21
      Digits = 0
      Max = 99999
      FormatStr = '%5.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 5
      Text = '0'
    end
    object Panel104: TFlatPanel
      Left = 16
      Top = 36
      Width = 73
      Height = 22
      Caption = '도 서 명'
      ParentColor = True
      TabOrder = 6
      UseDockManager = True
    end
    object Edit4: TFlatEdit
      Left = 96
      Top = 36
      Width = 353
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 7
      OnKeyPress = Edit4KeyPress
    end
  end
  object Panel201: TFlatPanel
    Left = 8
    Top = 76
    Width = 601
    Height = 285
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid1: TDBGrid
      Left = 1
      Top = 1
      Width = 599
      Height = 283
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      ImeName = '한국어(한글)'
      Options = [dgEditing, dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgConfirmDelete, dgCancelOnExit]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnKeyDown = DBGrid1KeyDown
      OnKeyPress = DBGrid1KeyPress
      OnTitleClick = DBGrid1TitleClick
      Columns = <
        item
          Expanded = False
          FieldName = 'SNAME'
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '구분'
          Width = 60
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'JUBUN'
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '지역'
          Width = 40
          Visible = True
        end
        item
          Color = 11861755
          Expanded = False
          FieldName = 'GCODE'
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 40
          Visible = True
        end
        item
          Color = 12056530
          Expanded = False
          FieldName = 'GNAME'
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '거래처명'
          Width = 152
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GJISA'
          Title.Alignment = taCenter
          Title.Caption = '지점'
          Width = 120
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GTEL2'
          ReadOnly = True
          Title.Alignment = taCenter
          Title.Caption = '전화번호'
          Width = 70
          Visible = True
        end
        item
          Color = 12106750
          Expanded = False
          FieldName = 'GQUT1'
          Title.Alignment = taCenter
          Title.Caption = '부수'
          Width = 45
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GRAT1'
          Title.Alignment = taCenter
          Title.Caption = '비율'
          Width = 35
          Visible = True
        end>
    end
  end
  object Button101: TFlatButton
    Left = 176
    Top = 368
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
    TabOrder = 3
    ModalResult = 1
    Visible = False
  end
  object Button102: TFlatButton
    Left = 320
    Top = 368
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
    TabOrder = 4
    ModalResult = 2
    Visible = False
  end
  object BitBtn102: TBitBtn
    Left = 336
    Top = 368
    Width = 75
    Height = 25
    Caption = '취소'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clWindowText
    Font.Height = -12
    Font.Name = '굴림체'
    Font.Style = [fsBold]
    ParentFont = False
    TabOrder = 5
    Kind = bkCancel
  end
  object BitBtn101: TBitBtn
    Left = 192
    Top = 368
    Width = 75
    Height = 25
    Caption = '실행'
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
  object DataSource1: TDataSource
    DataSet = Query1
    Left = 424
    Top = 368
  end
  object Query1: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 456
    Top = 368
    object Query1SNAME: TStringField
      FieldName = 'SNAME'
      Size = 10
    end
    object Query1GUBUN: TStringField
      FieldName = 'GUBUN'
      Size = 5
    end
    object Query1JUBUN: TStringField
      FieldName = 'JUBUN'
      Size = 6
    end
    object Query1PUBUN: TStringField
      FieldName = 'PUBUN'
      Size = 2
    end
    object Query1SCODE: TStringField
      FieldName = 'SCODE'
      Size = 1
    end
    object Query1GCODE: TStringField
      FieldName = 'GCODE'
      Size = 5
    end
    object Query1OCODE: TStringField
      FieldName = 'OCODE'
      Size = 5
    end
    object Query1GNAME: TStringField
      FieldName = 'GNAME'
      Size = 24
    end
    object Query1GPOSA: TStringField
      FieldName = 'GPOSA'
      Size = 10
    end
    object Query1GTEL1: TStringField
      FieldName = 'GTEL1'
      Size = 4
    end
    object Query1GTEL2: TStringField
      FieldName = 'GTEL2'
      Size = 9
    end
    object Query1GADD1: TStringField
      FieldName = 'GADD1'
      Size = 44
    end
    object Query1GADD2: TStringField
      FieldName = 'GADD2'
      Size = 44
    end
    object Query1GQUT1: TFloatField
      FieldName = 'GQUT1'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object Query1GRAT1: TSmallintField
      FieldName = 'GRAT1'
    end
    object Query1GJISA: TStringField
      FieldName = 'GJISA'
      Size = 15
    end
  end
end
