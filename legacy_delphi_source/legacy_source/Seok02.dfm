object Seok20: TSeok20
  Left = 200
  Top = 198
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '거래명세서-천일'
  ClientHeight = 440
  ClientWidth = 770
  Color = clBtnFace
  Font.Charset = HANGEUL_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = '굴림'
  Font.Style = [fsBold]
  OldCreateOrder = False
  Position = poScreenCenter
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 12
  object Panel100: TFlatPanel
    Left = 8
    Top = 8
    Width = 753
    Height = 49
    Color = clInfoBk
    TabOrder = 0
    UseDockManager = True
    object Button001: TFlatSpeedButton
      Left = 328
      Top = 12
      Width = 25
      Height = 22
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
      OnClick = Button001Click
    end
    object Panel101: TFlatPanel
      Left = 24
      Top = 12
      Width = 90
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 0
      UseDockManager = True
    end
    object Edit1: TFlatEdit
      Left = 120
      Top = 12
      Width = 209
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
      OnEnter = Edit1Enter
      OnKeyPress = Edit1KeyPress
    end
  end
  object Panel201: TFlatPanel
    Left = 8
    Top = 60
    Width = 753
    Height = 341
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGridEh
      Left = 1
      Top = 1
      Width = 751
      Height = 339
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      FooterColor = clWindow
      FooterFont.Charset = HANGEUL_CHARSET
      FooterFont.Color = clWindowText
      FooterFont.Height = -12
      FooterFont.Name = '굴림'
      FooterFont.Style = [fsBold]
      ImeName = '한국어 입력 시스템 (IME 2000)'
      Options = [dgEditing, dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      Columns = <
        item
          EditButtons = <>
          FieldName = 'HCODE'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 50
        end
        item
          Color = 12056530
          EditButtons = <>
          FieldName = 'HNAME'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '출판사명'
          Width = 100
        end
        item
          Checkboxes = True
          EditButtons = <>
          FieldName = 'CODE5'
          Footers = <>
          KeyList.Strings = (
            'O;On'
            'N;Off')
          Title.Alignment = taCenter
          Title.Caption = '선택'
          Width = 33
        end
        item
          EditButtons = <>
          FieldName = 'GNUMB'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '운송장번호'
          Width = 100
        end
        item
          EditButtons = <>
          FieldName = 'NAME1'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '지역명'
          Width = 70
        end
        item
          EditButtons = <>
          FieldName = 'GNAME'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '거래처명'
          Width = 120
        end
        item
          EditButtons = <>
          FieldName = 'NAME2'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '화물명'
          Width = 80
        end
        item
          Color = 11861755
          EditButtons = <>
          FieldName = 'GSSUM'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '발송비'
          Width = 80
        end
        item
          EditButtons = <>
          FieldName = 'GBIGO'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '메모'
          Width = 80
        end>
    end
  end
  object Button101: TFlatButton
    Left = 248
    Top = 408
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
    TabOrder = 2
    ModalResult = 1
    Visible = False
  end
  object Button102: TFlatButton
    Left = 392
    Top = 408
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
    TabOrder = 3
    ModalResult = 2
    Visible = False
  end
  object BitBtn101: TBitBtn
    Left = 264
    Top = 408
    Width = 75
    Height = 25
    Caption = '선택'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clWindowText
    Font.Height = -12
    Font.Name = '굴림체'
    Font.Style = [fsBold]
    ModalResult = 1
    ParentFont = False
    TabOrder = 4
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
    Left = 408
    Top = 408
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
  object DataSource1: TDataSource
    DataSet = Query1
    Left = 552
    Top = 408
  end
  object Query1: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 584
    Top = 408
    object Query1ID: TFloatField
      FieldName = 'ID'
    end
    object Query1HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object Query1HNAME: TStringField
      FieldName = 'HNAME'
      Size = 50
    end
    object Query1GCODE: TStringField
      FieldName = 'GCODE'
      Size = 5
    end
    object Query1GNAME: TStringField
      FieldName = 'GNAME'
      Size = 50
    end
    object Query1NAME1: TStringField
      FieldName = 'NAME1'
    end
    object Query1NAME2: TStringField
      FieldName = 'NAME2'
    end
    object Query1GNUMB: TStringField
      FieldName = 'GNUMB'
    end
    object Query1GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object Query1GBIGO: TStringField
      FieldName = 'GBIGO'
      Size = 50
    end
    object Query1CODE5: TStringField
      FieldName = 'CODE5'
      Size = 5
    end
  end
end
