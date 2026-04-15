object Exls70: TExls70
  Left = 71
  Top = 120
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '출판사명 매칭관리'
  ClientHeight = 533
  ClientWidth = 1048
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
    Width = 1017
    Height = 45
    Color = 14416873
    TabOrder = 0
    UseDockManager = True
    object dxButton1: TdxButton
      Left = 472
      Top = 8
      Width = 63
      Height = 30
      OnClick = Button101Click
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
  end
  object Panel007: TFlatPanel
    Left = 24
    Top = 502
    Width = 1017
    Height = 29
    Color = clInfoBk
    TabOrder = 1
    UseDockManager = True
    object ProgressBar0: TFlatProgressBar
      Left = 672
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
      Left = 568
      Top = 5
      Width = 97
      Height = 19
      Caption = '검색진행'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object ProgressBar1: TProgressBar
      Left = 672
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
    Width = 1017
    Height = 446
    ParentColor = True
    TabOrder = 2
    UseDockManager = True
    object DBGrid101: TDBGridEh
      Left = 1
      Top = 1
      Width = 1015
      Height = 444
      Align = alClient
      BorderStyle = bsNone
      DataSource = DataSource1
      FooterColor = 16311512
      FooterFont.Charset = HANGEUL_CHARSET
      FooterFont.Color = clWindowText
      FooterFont.Height = -12
      FooterFont.Name = '굴림'
      FooterFont.Style = [fsBold]
      ImeName = '한국어 입력 시스템 (IME 2000)'
      TabOrder = 0
      TitleFont.Charset = HANGEUL_CHARSET
      TitleFont.Color = clWindowText
      TitleFont.Height = -12
      TitleFont.Name = '굴림'
      TitleFont.Style = [fsBold]
      UseMultiTitle = True
      VTitleMargin = 6
      OnDrawColumnCell = DBGrid101DrawColumnCell
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      Columns = <
        item
          EditButtons = <>
          FieldName = 'HCODE'
          Footers = <>
          ReadOnly = True
          Title.Caption = '출판사코드'
          Width = 100
        end
        item
          EditButtons = <>
          FieldName = 'HNAME'
          Footers = <>
          ReadOnly = True
          Title.Caption = '출판사명'
          Width = 300
        end
        item
          EditButtons = <>
          FieldName = 'NAME0'
          Footers = <>
          Title.Caption = '출판사(매칭)'
          Width = 300
        end>
    end
  end
  object DataSource1: TDataSource
    DataSet = Tm_Sms07
    OnDataChange = DataSource1DataChange
    Left = 34
    Top = 126
  end
  object DataSource2: TDataSource
    Left = 66
    Top = 126
  end
  object Tm_Sms07: TClientDataSet
    Aggregates = <>
    Params = <>
    BeforeClose = Tm_Sms07BeforeClose
    BeforePost = Tm_Sms07BeforePost
    AfterPost = Tm_Sms07AfterPost
    Left = 34
    Top = 158
    object Tm_Sms07ID: TFloatField
      FieldName = 'ID'
    end
    object Tm_Sms07HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object Tm_Sms07HNAME: TStringField
      FieldName = 'HNAME'
      Size = 80
    end
    object Tm_Sms07NAME0: TStringField
      FieldName = 'NAME0'
      Size = 80
    end
  end
end
