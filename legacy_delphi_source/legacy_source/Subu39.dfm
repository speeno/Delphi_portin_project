object Sobo39: TSobo39
  Left = 22
  Top = 90
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '출고내역서'
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
    Left = 2
    Top = 53
    Width = 322
    Height = 516
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGridEh
      Left = 1
      Top = 1
      Width = 320
      Height = 514
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
      Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
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
          EditButtons = <>
          FieldName = 'HCODE'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 45
        end
        item
          EditButtons = <>
          FieldName = 'HNAME'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '출판사명'
          Width = 150
        end
        item
          Color = 11861755
          EditButtons = <>
          FieldName = 'GSQUT'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '건수'
          Width = 46
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
          Width = 46
        end>
    end
  end
  object Panel003: TFlatPanel
    Left = 328
    Top = 173
    Width = 545
    Height = 396
    ParentColor = True
    TabOrder = 2
    UseDockManager = True
    object DBGrid201: TDBGridEh
      Left = 1
      Top = 1
      Width = 543
      Height = 394
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
      SumList.Active = True
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      OnDrawColumnCell = DBGrid201DrawColumnCell
      OnKeyDown = DBGrid201KeyDown
      OnKeyPress = DBGrid201KeyPress
      OnTitleClick = DBGrid201TitleClick
      Columns = <
        item
          EditButtons = <>
          FieldName = 'GCODE'
          Footer.Value = '합계'
          Footer.ValueType = fvtStaticText
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Width = 45
        end
        item
          ButtonStyle = cbsEllipsis
          EditButtons = <>
          FieldName = 'GNAME'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '거래처명'
          Width = 170
        end
        item
          EditButtons = <>
          FieldName = 'JUBUN'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '전표'
          Width = 30
        end
        item
          EditButtons = <>
          FieldName = 'GJEJA'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '지역'
          Width = 100
        end
        item
          EditButtons = <>
          FieldName = 'GSQUT'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '수량'
          Width = 40
        end
        item
          Color = 11861755
          EditButtons = <>
          FieldName = 'GQUT1'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '덩이'
          Width = 40
        end
        item
          Color = 12056530
          EditButtons = <>
          FieldName = 'GQUT2'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '보호대'
          Width = 40
        end
        item
          EditButtons = <>
          FieldName = 'GQUT3'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '박스'
          Width = 40
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
  object Panel001: TFlatPanel
    Left = 2
    Top = 4
    Width = 959
    Height = 45
    Color = 14416873
    TabOrder = 0
    UseDockManager = True
    object Label101: TmyLabel3d
      Left = 564
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
      TabOrder = 5
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
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
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
    object Panel105: TFlatPanel
      Left = 256
      Top = 12
      Width = 87
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 8
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
      MaxLength = 50
      ParentFont = False
      TabOrder = 2
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
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
      MaxLength = 50
      ParentFont = False
      TabOrder = 4
      OnKeyDown = Edit102KeyDown
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
      TabOrder = 3
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
      StartOfWeek = Sun
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
    object dxButton1: TdxButton
      Left = 888
      Top = 8
      Width = 63
      Height = 30
      OnClick = Button101Click
      Caption = '검색'
      TabOrder = 12
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
    end
  end
  object Panel005: TFlatPanel
    Left = 877
    Top = 53
    Width = 84
    Height = 116
    Color = clInfoBk
    TabOrder = 4
    UseDockManager = True
    object RadioButton1: TFlatRadioButton
      Left = 16
      Top = 80
      Width = 49
      Height = 17
      Caption = '접수'
      TabOrder = 0
      OnClick = Button101Click
    end
    object RadioButton2: TFlatRadioButton
      Left = 16
      Top = 48
      Width = 49
      Height = 17
      Caption = '완료'
      TabOrder = 1
      OnClick = Button101Click
    end
    object RadioButton3: TFlatRadioButton
      Left = 16
      Top = 16
      Width = 49
      Height = 17
      Caption = '전체'
      Checked = True
      TabOrder = 2
      TabStop = True
      OnClick = Button101Click
    end
  end
  object Panel004: TFlatPanel
    Left = 877
    Top = 293
    Width = 84
    Height = 148
    Color = clInfoBk
    TabOrder = 5
    UseDockManager = True
    object RadioButton4: TFlatRadioButton
      Left = 16
      Top = 16
      Width = 49
      Height = 25
      Caption = '전체선택'
      TabOrder = 0
      OnClick = Button401Click
    end
    object RadioButton5: TFlatRadioButton
      Left = 16
      Top = 48
      Width = 49
      Height = 25
      Caption = '전체해제'
      TabOrder = 1
      OnClick = Button401Click
    end
    object RadioButton6: TFlatRadioButton
      Left = 16
      Top = 80
      Width = 49
      Height = 25
      Caption = '자동알람'
      TabOrder = 2
      OnClick = Button401Click
    end
    object RadioButton7: TFlatRadioButton
      Left = 16
      Top = 112
      Width = 49
      Height = 25
      Caption = '자동해체'
      TabOrder = 3
      OnClick = Button401Click
    end
  end
  object Panel006: TFlatPanel
    Left = 877
    Top = 173
    Width = 84
    Height = 116
    Color = clInfoBk
    TabOrder = 6
    UseDockManager = True
    object RadioButton8: TFlatRadioButton
      Left = 16
      Top = 48
      Width = 49
      Height = 25
      Caption = '구간'
      TabOrder = 0
    end
    object RadioButton9: TFlatRadioButton
      Left = 16
      Top = 80
      Width = 49
      Height = 25
      Caption = '신간'
      TabOrder = 1
    end
    object RadioButton0: TFlatRadioButton
      Left = 16
      Top = 16
      Width = 49
      Height = 25
      Caption = '전체'
      Checked = True
      TabOrder = 2
      TabStop = True
    end
  end
  object Panel011: TFlatPanel
    Left = 877
    Top = 445
    Width = 84
    Height = 124
    Color = clInfoBk
    TabOrder = 7
    UseDockManager = True
    object RadioButton12: TFlatRadioButton
      Left = 16
      Top = 48
      Width = 57
      Height = 25
      Caption = '출고증제외+'
      TabOrder = 0
    end
    object RadioButton11: TFlatRadioButton
      Left = 16
      Top = 16
      Width = 57
      Height = 25
      Caption = '출고증전체'
      Checked = True
      TabOrder = 1
      TabStop = True
    end
    object RadioButton13: TFlatRadioButton
      Left = 16
      Top = 80
      Width = 57
      Height = 25
      Caption = '출고증제외-'
      TabOrder = 2
    end
  end
  object Panel012: TFlatPanel
    Left = 328
    Top = 53
    Width = 545
    Height = 116
    Color = clInfoBk
    TabOrder = 8
    UseDockManager = True
    object myLabel3d1: TmyLabel3d
      Left = 160
      Top = 8
      Width = 34
      Height = 16
      Caption = '수량'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object myLabel3d2: TmyLabel3d
      Left = 256
      Top = 8
      Width = 34
      Height = 16
      Caption = '덩이'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object myLabel3d3: TmyLabel3d
      Left = 344
      Top = 8
      Width = 51
      Height = 16
      Caption = '보호대'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object myLabel3d4: TmyLabel3d
      Left = 448
      Top = 8
      Width = 34
      Height = 16
      Caption = '박스'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Label300: TmyLabel3d
      Left = 136
      Top = 73
      Width = 368
      Height = 13
      Caption = '----------------------------------------------'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlue
      Font.Height = -13
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AStyle3D = Resit3d
      AShadeLTSet = False
    end
    object Panel013: TFlatPanel
      Left = 40
      Top = 28
      Width = 81
      Height = 22
      Caption = '시내'
      ParentColor = True
      TabOrder = 0
      UseDockManager = True
    end
    object Edit201: TFlatNumber
      Left = 136
      Top = 28
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 1
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Edit202: TFlatNumber
      Left = 232
      Top = 28
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 2
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Edit203: TFlatNumber
      Left = 328
      Top = 28
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 3
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Edit204: TFlatNumber
      Left = 424
      Top = 28
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 4
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Panel014: TFlatPanel
      Left = 40
      Top = 52
      Width = 81
      Height = 22
      Caption = '지방'
      ParentColor = True
      TabOrder = 5
      UseDockManager = True
    end
    object Edit301: TFlatNumber
      Left = 136
      Top = 52
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 6
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Edit302: TFlatNumber
      Left = 232
      Top = 52
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 7
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Edit303: TFlatNumber
      Left = 328
      Top = 52
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 8
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Edit304: TFlatNumber
      Left = 424
      Top = 52
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 9
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Panel015: TFlatPanel
      Left = 40
      Top = 84
      Width = 81
      Height = 22
      Caption = '합계'
      ParentColor = True
      TabOrder = 10
      UseDockManager = True
    end
    object Edit401: TFlatNumber
      Left = 136
      Top = 84
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 11
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Edit402: TFlatNumber
      Left = 232
      Top = 84
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 12
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Edit403: TFlatNumber
      Left = 328
      Top = 84
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 13
      Text = '0'
      OnKeyPress = Edit111KeyPress
    end
    object Edit404: TFlatNumber
      Left = 424
      Top = 84
      Width = 81
      Height = 22
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 14
      Text = '0'
      OnKeyPress = Edit111KeyPress
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
    BeforeClose = T3_Sub91BeforeClose
    BeforePost = T3_Sub91BeforePost
    AfterPost = T3_Sub91AfterPost
    Left = 10
    Top = 158
    object T3_Sub91GDATE: TStringField
      FieldName = 'GDATE'
      EditMask = '!0000.!90.90;1; '
      Size = 10
    end
    object T3_Sub91SCODE: TStringField
      FieldName = 'SCODE'
      Size = 1
    end
    object T3_Sub91GCODE: TStringField
      FieldName = 'GCODE'
      Size = 5
    end
    object T3_Sub91GNAME: TStringField
      FieldName = 'GNAME'
      Size = 100
    end
    object T3_Sub91HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object T3_Sub91HNAME: TStringField
      FieldName = 'HNAME'
      Size = 50
    end
    object T3_Sub91GJEJA: TStringField
      FieldName = 'GJEJA'
      Size = 30
    end
    object T3_Sub91JUBUN: TStringField
      FieldName = 'JUBUN'
      Size = 2
    end
    object T3_Sub91GJISA: TStringField
      FieldName = 'GJISA'
      Size = 30
    end
    object T3_Sub91GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GQUT1: TFloatField
      FieldName = 'GQUT1'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GQUT2: TFloatField
      FieldName = 'GQUT2'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub91GQUT3: TFloatField
      FieldName = 'GQUT3'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
  end
  object T3_Sub92: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 42
    Top = 158
    object T3_Sub92GDATE: TStringField
      FieldName = 'GDATE'
      EditMask = '!0000.!90.90;1; '
      Size = 10
    end
    object T3_Sub92SCODE: TStringField
      FieldName = 'SCODE'
      Size = 1
    end
    object T3_Sub92GCODE: TStringField
      FieldName = 'GCODE'
      Size = 5
    end
    object T3_Sub92GNAME: TStringField
      FieldName = 'GNAME'
      Size = 100
    end
    object T3_Sub92HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object T3_Sub92HNAME: TStringField
      FieldName = 'HNAME'
      Size = 50
    end
    object T3_Sub92CODE5: TStringField
      FieldName = 'CODE5'
      Size = 4
    end
    object T3_Sub92GSQUT: TFloatField
      FieldName = 'GSQUT'
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
      Size = 100
    end
    object T3_Sub93GCODE: TStringField
      FieldName = 'GCODE'
      Size = 10
    end
    object T3_Sub93GNAME: TStringField
      FieldName = 'GNAME'
      Size = 100
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
end
