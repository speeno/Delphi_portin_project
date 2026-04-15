object Sobo42_1: TSobo42_1
  Left = 71
  Top = 120
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '입금현황(2)'
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
    Width = 872
    Height = 46
    Color = 14416873
    TabOrder = 0
    UseDockManager = True
    object Label101: TmyLabel3d
      Left = 201
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
    object Button101: TFlatButton
      Left = 816
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
      TabOrder = 4
      Visible = False
      OnClick = Button101Click
    end
    object Button201: TFlatButton
      Left = 840
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
      TabOrder = 5
      Visible = False
      OnClick = Button201Click
    end
    object Panel101: TFlatPanel
      Left = 24
      Top = 12
      Width = 78
      Height = 22
      Caption = '거래일자'
      ParentColor = True
      TabOrder = 6
      UseDockManager = True
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
      TabOrder = 7
      Visible = False
    end
    object Panel102: TFlatPanel
      Left = 392
      Top = 12
      Width = 78
      Height = 22
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 9
      UseDockManager = True
    end
    object Edit108: TFlatEdit
      Left = 472
      Top = 12
      Width = 169
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
    object Button700: TFlatButton
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
      TabOrder = 10
      OnClick = Button700Click
    end
    object Edit107: TFlatEdit
      Left = 472
      Top = 12
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
      TabOrder = 2
      Visible = False
    end
    object Edit101: TFlatComboBox
      Left = 104
      Top = 12
      Width = 97
      Height = 23
      Color = clWindow
      DropDownCount = 9
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ItemHeight = 15
      Items.Strings = (
        '2020.12'
        '2020.11'
        '2020.10'
        '2020.09'
        '2020.08'
        '2020.07'
        '2020.06'
        '2020.05'
        '2020.04'
        '2020.03'
        '2020.02'
        '2020.01'
        '2019.12'
        '2019.11'
        '2019.10'
        '2019.09'
        '2019.08'
        '2019.07'
        '2019.06'
        '2019.05'
        '2019.04'
        '2019.03'
        '2019.02'
        '2019.01'
        '2018.12'
        '2018.11'
        '2018.10'
        '2018.09'
        '2018.08'
        '2018.07'
        '2018.06'
        '2018.05'
        '2018.04'
        '2018.03'
        '2018.02'
        '2018.01'
        '2017.12'
        '2017.11'
        '2017.10'
        '2017.09'
        '2017.08'
        '2017.07'
        '2017.06'
        '2017.05'
        '2017.04'
        '2017.03'
        '2017.02'
        '2017.01'
        '2016.12'
        '2016.11'
        '2016.10'
        '2016.09'
        '2016.08'
        '2016.07'
        '2016.06'
        '2016.05'
        '2016.04'
        '2016.03'
        '2016.02'
        '2016.01'
        '2015.12'
        '2015.11'
        '2015.10'
        '2015.09'
        '2015.08'
        '2015.07'
        '2015.06'
        '2015.05'
        '2015.04'
        '2015.03'
        '2015.02'
        '2015.01'
        '2014.12'
        '2014.11'
        '2014.10'
        '2014.09'
        '2014.08'
        '2014.07'
        '2014.06'
        '2014.05'
        '2014.04'
        '2014.03'
        '2014.02'
        '2014.01'
        '2013.12'
        '2013.11'
        '2013.10'
        '2013.09'
        '2013.08'
        '2013.07'
        '2013.06'
        '2013.05'
        '2013.04'
        '2013.03'
        '2013.02'
        '2013.01'
        '2012.12'
        '2012.11'
        '2012.10'
        '2012.09'
        '2012.08'
        '2012.07'
        '2012.06'
        '2012.05'
        '2012.04'
        '2012.03'
        '2012.02'
        '2012.01'
        '2011.12'
        '2011.11'
        '2011.10'
        '2011.09'
        '2011.08'
        '2011.07'
        '2011.06'
        '2011.05'
        '2011.04'
        '2011.03'
        '2011.02'
        '2011.01'
        '2010.12'
        '2010.11'
        '2010.10'
        '2010.09'
        '2010.08'
        '2010.07'
        '2010.06'
        '2010.05'
        '2010.04'
        '2010.03'
        '2010.02'
        '2010.01'
        '2009.12'
        '2009.11'
        '2009.10'
        '2009.09'
        '2009.08'
        '2009.07'
        '2009.06'
        '2009.05'
        '2009.04'
        '2009.03'
        '2009.02'
        '2009.01'
        '2008.12'
        '2008.11'
        '2008.10'
        '2008.09'
        '2008.08'
        '2008.07'
        '2008.06'
        '2008.05'
        '2008.04'
        '2008.03'
        '2008.02'
        '2008.01'
        '2007.12'
        '2007.11'
        '2007.10'
        '2007.09'
        '2007.08'
        '2007.07'
        '2007.06'
        '2007.05'
        '2007.04'
        '2007.03'
        '2007.02'
        '2007.01')
      ParentFont = False
      TabOrder = 0
      Text = '2010.12'
      ItemIndex = -1
      OnChange = Edit101Change
      OnKeyDown = Edit113KeyDown
      OnKeyPress = Edit113KeyPress
    end
    object Edit102: TFlatComboBox
      Left = 216
      Top = 12
      Width = 97
      Height = 23
      Color = clWindow
      DropDownCount = 9
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ItemHeight = 15
      Items.Strings = (
        '2020.12'
        '2020.11'
        '2020.10'
        '2020.09'
        '2020.08'
        '2020.07'
        '2020.06'
        '2020.05'
        '2020.04'
        '2020.03'
        '2020.02'
        '2020.01'
        '2019.12'
        '2019.11'
        '2019.10'
        '2019.09'
        '2019.08'
        '2019.07'
        '2019.06'
        '2019.05'
        '2019.04'
        '2019.03'
        '2019.02'
        '2019.01'
        '2018.12'
        '2018.11'
        '2018.10'
        '2018.09'
        '2018.08'
        '2018.07'
        '2018.06'
        '2018.05'
        '2018.04'
        '2018.03'
        '2018.02'
        '2018.01'
        '2017.12'
        '2017.11'
        '2017.10'
        '2017.09'
        '2017.08'
        '2017.07'
        '2017.06'
        '2017.05'
        '2017.04'
        '2017.03'
        '2017.02'
        '2017.01'
        '2016.12'
        '2016.11'
        '2016.10'
        '2016.09'
        '2016.08'
        '2016.07'
        '2016.06'
        '2016.05'
        '2016.04'
        '2016.03'
        '2016.02'
        '2016.01'
        '2015.12'
        '2015.11'
        '2015.10'
        '2015.09'
        '2015.08'
        '2015.07'
        '2015.06'
        '2015.05'
        '2015.04'
        '2015.03'
        '2015.02'
        '2015.01'
        '2014.12'
        '2014.11'
        '2014.10'
        '2014.09'
        '2014.08'
        '2014.07'
        '2014.06'
        '2014.05'
        '2014.04'
        '2014.03'
        '2014.02'
        '2014.01'
        '2013.12'
        '2013.11'
        '2013.10'
        '2013.09'
        '2013.08'
        '2013.07'
        '2013.06'
        '2013.05'
        '2013.04'
        '2013.03'
        '2013.02'
        '2013.01'
        '2012.12'
        '2012.11'
        '2012.10'
        '2012.09'
        '2012.08'
        '2012.07'
        '2012.06'
        '2012.05'
        '2012.04'
        '2012.03'
        '2012.02'
        '2012.01'
        '2011.12'
        '2011.11'
        '2011.10'
        '2011.09'
        '2011.08'
        '2011.07'
        '2011.06'
        '2011.05'
        '2011.04'
        '2011.03'
        '2011.02'
        '2011.01'
        '2010.12'
        '2010.11'
        '2010.10'
        '2010.09'
        '2010.08'
        '2010.07'
        '2010.06'
        '2010.05'
        '2010.04'
        '2010.03'
        '2010.02'
        '2010.01'
        '2009.12'
        '2009.11'
        '2009.10'
        '2009.09'
        '2009.08'
        '2009.07'
        '2009.06'
        '2009.05'
        '2009.04'
        '2009.03'
        '2009.02'
        '2009.01'
        '2008.12'
        '2008.11'
        '2008.10'
        '2008.09'
        '2008.08'
        '2008.07'
        '2008.06'
        '2008.05'
        '2008.04'
        '2008.03'
        '2008.02'
        '2008.01'
        '2007.12'
        '2007.11'
        '2007.10'
        '2007.09'
        '2007.08'
        '2007.07'
        '2007.06'
        '2007.05'
        '2007.04'
        '2007.03'
        '2007.02'
        '2007.01')
      ParentFont = False
      TabOrder = 1
      Text = '2010.12'
      ItemIndex = -1
      OnChange = Edit101Change
      OnKeyDown = Edit113KeyDown
      OnKeyPress = Edit113KeyPress
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
      TabOrder = 8
      Visible = False
    end
    object dxButton1: TdxButton
      Left = 800
      Top = 8
      Width = 63
      Height = 30
      OnClick = Button101Click
      Caption = '검색'
      TabOrder = 11
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
  object Panel002: TFlatPanel
    Left = 24
    Top = 53
    Width = 872
    Height = 446
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object DBGrid101: TDBGridEh
      Left = 1
      Top = 1
      Width = 870
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
      OnEnter = DBGrid101Enter
      OnExit = DBGrid101Exit
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      OnTitleClick = DBGrid101TitleClick
      Columns = <
        item
          Alignment = taCenter
          EditButtons = <>
          FieldName = 'SDATE'
          Footer.Value = '합계'
          Footer.ValueType = fvtStaticText
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '년월'
          Width = 82
        end
        item
          Color = 12056530
          EditButtons = <>
          FieldName = 'GSUMX'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '전일미수'
          Width = 95
        end
        item
          EditButtons = <>
          FieldName = 'GOSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '당월금액'
          Width = 95
        end
        item
          EditButtons = <>
          FieldName = 'GBSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '세액'
          Width = 95
        end
        item
          EditButtons = <>
          FieldName = 'GPSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '당월합계'
          Width = 95
        end
        item
          EditButtons = <>
          FieldName = 'GSSUM'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '합계금액'
          Width = 95
        end
        item
          Alignment = taCenter
          EditButtons = <>
          FieldName = 'GDATE'
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '입금일'
          Width = 82
        end
        item
          EditButtons = <>
          FieldName = 'GSUSU'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '입금액'
          Width = 95
        end
        item
          Color = 11861755
          EditButtons = <>
          FieldName = 'GSUMY'
          Footer.ValueType = fvtSum
          Footers = <>
          Title.Alignment = taCenter
          Title.Caption = '당월미수액'
          Width = 95
        end>
    end
  end
  object Panel007: TFlatPanel
    Left = 24
    Top = 502
    Width = 872
    Height = 29
    Color = clInfoBk
    TabOrder = 2
    UseDockManager = True
    object ProgressBar0: TFlatProgressBar
      Left = 464
      Top = 5
      Width = 399
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
      Left = 360
      Top = 5
      Width = 97
      Height = 19
      Caption = '검색진행'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object ProgressBar1: TProgressBar
      Left = 464
      Top = 5
      Width = 393
      Height = 18
      Min = 0
      Max = 100
      TabOrder = 3
    end
  end
  object DataSource1: TDataSource
    DataSet = T4_Sub21
    OnDataChange = DataSource1DataChange
    Left = 42
    Top = 94
  end
  object DataSource2: TDataSource
    DataSet = Base10.T4_Sub22
    OnDataChange = DataSource2DataChange
    Left = 74
    Top = 94
  end
  object T4_Sub21: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 42
    Top = 126
    object T4_Sub21ID: TFloatField
      FieldName = 'ID'
    end
    object T4_Sub21SDATE: TStringField
      FieldName = 'SDATE'
      Size = 7
    end
    object T4_Sub21GDATE: TStringField
      FieldName = 'GDATE'
      EditMask = '!0000.!90.90;1; '
      Size = 10
    end
    object T4_Sub21HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object T4_Sub21HNAME: TStringField
      FieldName = 'HNAME'
      Size = 50
    end
    object T4_Sub21GUBUN: TStringField
      FieldName = 'GUBUN'
      Size = 4
    end
    object T4_Sub21GSUMX: TFloatField
      FieldName = 'GSUMX'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub21GOSUM: TFloatField
      FieldName = 'GOSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub21GBSUM: TFloatField
      FieldName = 'GBSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub21GPSUM: TFloatField
      FieldName = 'GPSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub21GSSUM: TFloatField
      FieldName = 'GSSUM'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub21GSUSU: TFloatField
      FieldName = 'GSUSU'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
    object T4_Sub21GSUMY: TFloatField
      FieldName = 'GSUMY'
      DisplayFormat = '###,###,###0'
      EditFormat = '#########0'
    end
  end
end
