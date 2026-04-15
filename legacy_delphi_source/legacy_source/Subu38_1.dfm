object Sobo38_1: TSobo38_1
  Left = 71
  Top = 120
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '운임관리-택배'
  ClientHeight = 533
  ClientWidth = 901
  Color = clBtnFace
  Font.Charset = ANSI_CHARSET
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
    Height = 47
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
    Top = 52
    Width = 21
    Height = 447
    Cursor = crArrow
    BevelColor = clBlue
    BevelWidth = 1
    MouseDownColor = clBlue
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
    Top = 12
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
    Top = 224
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
    Height = 45
    Color = 14416873
    TabOrder = 0
    UseDockManager = True
    object dxButton1: TdxButton
      Left = 392
      Top = 8
      Width = 63
      Height = 30
      OnClick = Button709Click
      Caption = '검색'
      TabOrder = 0
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
    object Panel101: TFlatPanel
      Left = 16
      Top = 12
      Width = 78
      Height = 22
      Caption = '거래일자'
      ParentColor = True
      TabOrder = 1
      UseDockManager = True
    end
    object Edit101: TFlatMaskEdit
      Left = 96
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
      TabOrder = 2
      Text = '1999.01.01'
      OnChange = Edit101Change
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object DateEdit1: TDateEdit
      Left = 193
      Top = 12
      Width = 19
      Height = 22
      BorderStyle = bsNone
      ImeName = 'Microsoft IME 2003'
      NumGlyphs = 2
      StartOfWeek = Sun
      TabOrder = 3
      OnAcceptDate = DateEdit1AcceptDate
      OnButtonClick = DateEdit1ButtonClick
    end
  end
  object Panel007: TFlatPanel
    Left = 24
    Top = 502
    Width = 873
    Height = 29
    Color = clInfoBk
    TabOrder = 2
    UseDockManager = True
    object ProgressBar0: TFlatProgressBar
      Left = 528
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
      Left = 424
      Top = 5
      Width = 97
      Height = 19
      Caption = '검색진행'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object ProgressBar1: TProgressBar
      Left = 528
      Top = 5
      Width = 335
      Height = 18
      Min = 0
      Max = 100
      TabOrder = 3
    end
  end
  object Panel002: TFlatPanel
    Left = 24
    Top = 53
    Width = 873
    Height = 446
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGridEh
      Left = 1
      Top = 1
      Width = 871
      Height = 444
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
      FooterFont.Color = clWindowText
      FooterFont.Height = -12
      FooterFont.Name = '굴림'
      FooterFont.Style = [fsBold]
      FooterRowCount = 1
      ImeName = '한국어 입력 시스템 (IME 2000)'
      Options = [dgEditing, dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgConfirmDelete, dgCancelOnExit]
      ParentFont = False
      ParentShowHint = False
      ShowHint = True
      SumList.Active = True
      SumList.VirtualRecords = True
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      UseMultiTitle = True
      VTitleMargin = 4
      OnEnter = Button709Click
      OnExit = DBGrid101Exit
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      Columns = <
        item
          EditButtons = <>
          FieldName = 'GCODE'
          Footer.Value = '합계'
          Footer.ValueType = fvtStaticText
          Footers = <>
          ReadOnly = True
          Title.Caption = '코드'
          Width = 50
        end
        item
          EditButtons = <>
          FieldName = 'GNAME'
          Footers = <>
          ReadOnly = True
          Title.Caption = '출판사명'
          Width = 180
        end
        item
          EditButtons = <>
          FieldName = 'GQUT5'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '택배|大'
          Width = 70
        end
        item
          EditButtons = <>
          FieldName = 'GQUT6'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '택배|中'
          Width = 70
          WordWrap = True
        end
        item
          EditButtons = <>
          FieldName = 'GQUT7'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '택배|小'
          Width = 70
        end
        item
          Color = 11861755
          EditButtons = <>
          FieldName = 'GQUT8'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Caption = '택배|기타'
          Width = 70
        end
        item
          Checkboxes = False
          EditButtons = <>
          Footers = <>
          Title.Caption = '비고'
          Width = 324
        end>
    end
  end
  object DataSource1: TDataSource
    DataSet = T3_Sub82
    OnDataChange = DataSource1DataChange
    Left = 34
    Top = 126
  end
  object DataSource2: TDataSource
    Left = 66
    Top = 126
  end
  object T3_Sub82: TClientDataSet
    Aggregates = <>
    Params = <>
    BeforeClose = T3_Sub82BeforeClose
    BeforePost = T3_Sub82BeforePost
    Left = 34
    Top = 158
    object T3_Sub82ID: TFloatField
      FieldName = 'ID'
    end
    object T3_Sub82GCODE: TStringField
      FieldName = 'GCODE'
      Size = 10
    end
    object T3_Sub82GDATE: TStringField
      FieldName = 'GDATE'
      EditMask = '!0000.!90.90;1; '
      Size = 10
    end
    object T3_Sub82GNAME: TStringField
      FieldName = 'GNAME'
      Size = 100
    end
    object T3_Sub82NAME1: TStringField
      FieldName = 'NAME1'
      Size = 30
    end
    object T3_Sub82GQUT5: TFloatField
      FieldName = 'GQUT5'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub82GQUT6: TFloatField
      FieldName = 'GQUT6'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub82GQUT7: TFloatField
      FieldName = 'GQUT7'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub82GQUT8: TFloatField
      FieldName = 'GQUT8'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub82GQUT9: TFloatField
      FieldName = 'GQUT9'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub82GSQUT: TFloatField
      FieldName = 'GSQUT'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub82GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T3_Sub82MEMO1: TBlobField
      FieldName = 'MEMO1'
      BlobType = ftBlob
    end
    object T3_Sub82MEMO2: TMemoField
      FieldName = 'MEMO2'
      BlobType = ftMemo
    end
  end
end
