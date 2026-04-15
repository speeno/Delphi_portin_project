object Seok10: TSeok10
  Left = 192
  Top = 107
  AutoScroll = False
  BorderIcons = [biSystemMenu]
  Caption = '지점관리'
  ClientHeight = 243
  ClientWidth = 756
  Color = clBtnFace
  Font.Charset = HANGEUL_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = '굴림'
  Font.Style = [fsBold]
  OldCreateOrder = False
  Position = poScreenCenter
  OnClose = FormClose
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 12
  object Panel001: TFlatPanel
    Left = 0
    Top = 0
    Width = 121
    Height = 243
    ParentColor = True
    Align = alLeft
    TabOrder = 0
    UseDockManager = True
    object Button101: TFlatButton
      Left = 8
      Top = 72
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
      TabOrder = 0
      ModalResult = 1
      Visible = False
    end
    object Button102: TFlatButton
      Left = 8
      Top = 144
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
      TabOrder = 1
      ModalResult = 2
      Visible = False
    end
    object BitBtn101: TBitBtn
      Left = 22
      Top = 68
      Width = 75
      Height = 25
      Caption = '추가'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림체'
      Font.Style = [fsBold]
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
      Left = 22
      Top = 140
      Width = 75
      Height = 25
      Cancel = True
      Caption = '삭제'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림체'
      Font.Style = [fsBold]
      ParentFont = False
      TabOrder = 3
      OnClick = BitBtn102Click
      Glyph.Data = {
        DE010000424DDE01000000000000760000002800000024000000120000000100
        0400000000006801000000000000000000001000000000000000000000000000
        80000080000000808000800000008000800080800000C0C0C000808080000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333333333
        333333333333333333333333000033338833333333333333333F333333333333
        0000333911833333983333333388F333333F3333000033391118333911833333
        38F38F333F88F33300003339111183911118333338F338F3F8338F3300003333
        911118111118333338F3338F833338F3000033333911111111833333338F3338
        3333F8330000333333911111183333333338F333333F83330000333333311111
        8333333333338F3333383333000033333339111183333333333338F333833333
        00003333339111118333333333333833338F3333000033333911181118333333
        33338333338F333300003333911183911183333333383338F338F33300003333
        9118333911183333338F33838F338F33000033333913333391113333338FF833
        38F338F300003333333333333919333333388333338FFF830000333333333333
        3333333333333333333888330000333333333333333333333333333333333333
        0000}
      NumGlyphs = 2
    end
  end
  object Panel002: TFlatPanel
    Left = 120
    Top = 0
    Width = 636
    Height = 243
    ParentColor = True
    Align = alRight
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGrid
      Left = 1
      Top = 1
      Width = 634
      Height = 241
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      ImeName = '한국어(한글)'
      Options = [dgEditing, dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgCancelOnExit]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      Columns = <
        item
          Expanded = False
          FieldName = 'JUBUN'
          Title.Alignment = taCenter
          Title.Caption = '지역'
          Width = 80
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GNAME'
          Font.Charset = HANGEUL_CHARSET
          Font.Color = clBlack
          Font.Height = -12
          Font.Name = '굴림'
          Font.Style = [fsBold]
          Title.Alignment = taCenter
          Title.Caption = '지점명'
          Title.Font.Charset = HANGEUL_CHARSET
          Title.Font.Color = clBlack
          Title.Font.Height = -12
          Title.Font.Name = '굴림체'
          Title.Font.Style = [fsBold]
          Width = 150
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'ONAME'
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 60
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GDATE'
          PickList.Strings = (
            '시내'
            '지방'
            '지방물류'
            '시내외'
            '지방외')
          Title.Alignment = taCenter
          Title.Caption = '구분'
          Width = 60
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GNUM1'
          Title.Alignment = taCenter
          Title.Caption = '번호'
          Width = 60
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'GBIGO'
          Title.Alignment = taCenter
          Title.Caption = '출고정지'
          Width = 185
          Visible = True
        end>
    end
  end
  object DataSource1: TDataSource
    DataSet = Query1
    Left = 48
    Top = 176
  end
  object Query1: TClientDataSet
    Aggregates = <>
    Params = <>
    BeforeClose = Query1BeforeClose
    BeforePost = Query1BeforePost
    OnNewRecord = Query1NewRecord
    Left = 80
    Top = 176
    object Query1ID: TFloatField
      FieldName = 'ID'
    end
    object Query1SCODE: TStringField
      FieldName = 'SCODE'
      Size = 1
    end
    object Query1GCODE: TStringField
      FieldName = 'GCODE'
      Size = 5
    end
    object Query1GNAME: TStringField
      FieldName = 'GNAME'
      Size = 15
    end
    object Query1ONAME: TStringField
      FieldName = 'ONAME'
      Size = 40
    end
    object Query1GDATE: TStringField
      FieldName = 'GDATE'
      Size = 10
    end
    object Query1GNUM1: TStringField
      FieldName = 'GNUM1'
      Size = 10
    end
    object Query1JUBUN: TStringField
      FieldName = 'JUBUN'
      Size = 15
    end
    object Query1GBIGO: TStringField
      FieldName = 'GBIGO'
      Size = 40
    end
  end
end
