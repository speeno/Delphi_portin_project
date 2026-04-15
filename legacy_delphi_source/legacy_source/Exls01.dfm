object Exls10: TExls10
  Left = 260
  Top = 90
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = 'ÅÃ¹è ¼ÛÀå¹øÈ£  °¡Á®¿À±â'
  ClientHeight = 647
  ClientWidth = 1092
  Color = clBtnFace
  Font.Charset = HANGEUL_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = '±¼¸²'
  Font.Style = [fsBold]
  OldCreateOrder = False
  Position = poScreenCenter
  OnActivate = FormActivate
  OnClose = FormClose
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 12
  object Panel100: TFlatPanel
    Left = 0
    Top = 8
    Width = 1089
    Height = 569
    ParentColor = True
    TabOrder = 0
    UseDockManager = True
    object Panel102: TFlatPanel
      Left = 1
      Top = 25
      Width = 1087
      Height = 486
      ParentColor = True
      Align = alClient
      TabOrder = 0
      UseDockManager = True
      object DBGrid101: TDBGridEh
        Left = 1
        Top = 1
        Width = 1085
        Height = 484
        Align = alClient
        BorderStyle = bsNone
        DataSource = DataSource1
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clWindowText
        Font.Height = -12
        Font.Name = '±¼¸²Ã¼'
        Font.Style = [fsBold]
        FooterColor = clWindow
        FooterFont.Charset = HANGEUL_CHARSET
        FooterFont.Color = clWindowText
        FooterFont.Height = -12
        FooterFont.Name = '±¼¸²Ã¼'
        FooterFont.Style = [fsBold]
        Options = [dgTitles, dgIndicator, dgColLines, dgRowLines, dgTabs, dgAlwaysShowSelection, dgCancelOnExit, dgMultiSelect]
        ParentFont = False
        ReadOnly = True
        TabOrder = 0
        TitleFont.Charset = HANGEUL_CHARSET
        TitleFont.Color = clWindowText
        TitleFont.Height = -12
        TitleFont.Name = '±¼¸²Ã¼'
        TitleFont.Style = [fsBold]
        Columns = <
          item
            EditButtons = <>
            FieldName = 'HCODE'
            Footers = <>
            Title.Alignment = taCenter
            Title.Caption = 'ÄÚµå'
            Width = 60
          end
          item
            EditButtons = <>
            FieldName = 'HNAME'
            Footers = <>
            Title.Alignment = taCenter
            Title.Caption = 'ÃâÆÇ»ç¸í'
            Width = 180
          end
          item
            EditButtons = <>
            FieldName = 'NAME0'
            Footers = <>
            Title.Alignment = taCenter
            Title.Caption = 'ÃâÆÇ»ç¸í(¸ÅÄª)'
            Width = 180
          end
          item
            EditButtons = <>
            FieldName = 'NAME1'
            Footers = <>
            Title.Alignment = taCenter
            Title.Caption = '¹Þ´ÂºÐ'
            Width = 180
          end
          item
            EditButtons = <>
            FieldName = 'NAME2'
            Footers = <>
            Title.Alignment = taCenter
            Title.Caption = '¿î¼ÛÀå¹øÈ£'
            Width = 150
          end
          item
            Color = 12056530
            EditButtons = <>
            FieldName = 'GSQUT'
            Footers = <>
            Title.Alignment = taCenter
            Title.Caption = '¼ö·®'
            Width = 60
          end
          item
            EditButtons = <>
            FieldName = 'GDANG'
            Footers = <>
            Title.Alignment = taCenter
            Title.Caption = '´Ü°¡'
            Width = 60
          end
          item
            Color = 11861755
            EditButtons = <>
            FieldName = 'GSSUM'
            Footers = <>
            Title.Alignment = taCenter
            Title.Caption = '±Ý¾×'
            Width = 90
          end
          item
            Checkboxes = True
            EditButtons = <>
            FieldName = 'CODE1'
            Footers = <>
            KeyList.Strings = (
              'O;On'
              'N;Off')
            PickList.Strings = (
              '2')
            Title.Alignment = taCenter
            Title.Caption = 'ºÒ´É'
            Width = 40
          end
          item
            Checkboxes = True
            EditButtons = <>
            FieldName = 'CODE2'
            Footers = <>
            KeyList.Strings = (
              'O;On'
              'N;Off')
            Title.Alignment = taCenter
            Title.Caption = '¿Ï·á'
            Width = 40
          end>
      end
    end
    object Panel101: TFlatPanel
      Left = 1
      Top = 1
      Width = 1087
      Height = 24
      Caption = '¿¢¼¿ÀÚ·á'
      Color = clLime
      Align = alTop
      TabOrder = 1
      UseDockManager = True
    end
    object Panel103: TFlatPanel
      Left = 1
      Top = 511
      Width = 1087
      Height = 57
      ParentColor = True
      Align = alBottom
      TabOrder = 2
      UseDockManager = True
      object Panel300: TFlatPanel
        Left = 8
        Top = 16
        Width = 90
        Height = 22
        Caption = 'µî·ÏÀÏÀÚ'
        ParentColor = True
        TabOrder = 0
        UseDockManager = True
      end
      object Edit300: TFlatMaskEdit
        Left = 104
        Top = 16
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
        Font.Name = '±¼¸²'
        Font.Style = [fsBold]
        MaxLength = 10
        ParentFont = False
        ReadOnly = True
        TabOrder = 1
        Text = '2002.01.01'
      end
      object Edit301: TFlatEdit
        Left = 382
        Top = 9
        Width = 353
        Height = 18
        ColorFlat = clWhite
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -12
        Font.Name = '±¼¸²'
        Font.Style = [fsBold]
        MaxLength = 50
        ParentFont = False
        TabOrder = 2
        Visible = False
      end
      object Panel301: TFlatPanel
        Left = 304
        Top = 9
        Width = 73
        Height = 38
        Caption = '¸Þ¸ð'
        ParentColor = True
        Visible = False
        TabOrder = 3
        UseDockManager = True
      end
      object Edit302: TFlatEdit
        Left = 382
        Top = 29
        Width = 353
        Height = 18
        ColorFlat = clWhite
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -12
        Font.Name = '±¼¸²'
        Font.Style = [fsBold]
        MaxLength = 50
        ParentFont = False
        TabOrder = 4
        Visible = False
      end
      object Edit304: TFlatEdit
        Left = 830
        Top = 29
        Width = 113
        Height = 18
        ColorFlat = clWhite
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -12
        Font.Name = '±¼¸²'
        Font.Style = [fsBold]
        MaxLength = 20
        ParentFont = False
        TabOrder = 5
        Visible = False
      end
      object Edit303: TFlatEdit
        Left = 830
        Top = 9
        Width = 113
        Height = 18
        ColorFlat = clWhite
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -12
        Font.Name = '±¼¸²'
        Font.Style = [fsBold]
        MaxLength = 20
        ParentFont = False
        TabOrder = 6
        Visible = False
      end
      object Panel302: TFlatPanel
        Left = 752
        Top = 9
        Width = 73
        Height = 19
        Caption = 'ÀüÈ­¹øÈ£'
        ParentColor = True
        Visible = False
        TabOrder = 7
        UseDockManager = True
      end
      object Panel303: TFlatPanel
        Left = 752
        Top = 29
        Width = 73
        Height = 19
        Caption = 'ÇÚµåÆù'
        ParentColor = True
        Visible = False
        TabOrder = 8
        UseDockManager = True
      end
      object Button302: TdxButton
        Left = 936
        Top = 7
        Width = 121
        Height = 26
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -12
        Font.Name = '±¼¸²'
        Font.Style = [fsBold]
        ParentFont = False
        Visible = False
        OnClick = Button302Click
        Style.Theme = OfficeXP
        Caption = '°Å·¡Ã³¸ÞÄª'
        TabOrder = 10
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
      object Button303: TdxButton
        Left = 936
        Top = 23
        Width = 121
        Height = 26
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -12
        Font.Name = '±¼¸²'
        Font.Style = [fsBold]
        ParentFont = False
        Visible = False
        OnClick = Button303Click
        Style.Theme = OfficeXP
        Caption = 'µµ¼­¸ÞÄª'
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
      object DateEdit1: TDateEdit
        Left = 201
        Top = 16
        Width = 20
        Height = 23
        BorderStyle = bsNone
        NumGlyphs = 2
        StartOfWeek = Sun
        TabOrder = 12
        OnAcceptDate = DateEdit1AcceptDate
        OnButtonClick = DateEdit1ButtonClick
      end
      object Button301: TdxButton
        Left = 936
        Top = 15
        Width = 121
        Height = 26
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -12
        Font.Name = '±¼¸²'
        Font.Style = [fsBold]
        ParentFont = False
        OnClick = Button301Click
        Style.Theme = OfficeXP
        Caption = 'ÃâÆÇ»ç¸ÞÄª'
        TabOrder = 9
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
  end
  object Panel201: TFlatPanel
    Left = 0
    Top = 584
    Width = 1089
    Height = 57
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object Label1: TLabel
      Left = 8
      Top = 12
      Width = 90
      Height = 16
      Caption = '__________'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clRed
      Font.Height = -16
      Font.Name = '±¼¸²Ã¼'
      Font.Style = [fsBold]
      ParentFont = False
      Visible = False
    end
    object Edit001: TFlatEdit
      Left = 14
      Top = 5
      Width = 83
      Height = 18
      ColorFlat = clWhite
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '±¼¸²'
      Font.Style = [fsBold]
      MaxLength = 100
      ParentFont = False
      TabOrder = 0
      Visible = False
    end
    object Edit002: TFlatEdit
      Left = 102
      Top = 5
      Width = 83
      Height = 18
      ColorFlat = clWhite
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '±¼¸²'
      Font.Style = [fsBold]
      MaxLength = 100
      ParentFont = False
      TabOrder = 1
      Visible = False
    end
    object Button101: TdxButton
      Left = 353
      Top = 14
      Width = 160
      Height = 26
      OnClick = Button101Click
      Caption = 'ÀúÀå'
      TabOrder = 2
      Glyph.Data = {
        36030000424D3603000000000000360000002800000010000000100000000100
        18000000000000030000C30E0000C30E00000000000000000000FAFAFAFAFAFA
        FAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFA
        FAFAFAFAFAFAFAFAFAFA99999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999666666
        6666666666666666666666666666666666666666666666666666666666666666
        66666666666666999999666666E8DFDFE8DFDFE8DFDFE8DFDFE8DFDFE8DFDFE8
        DFDFE8DFDFE8DFDFE8DFDFE8DFDFE8DFDFE8DFDFE8DFDF666666666666E8DFDF
        FAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFA000033FAFA
        FA000033E8DFDF666666666666E8DFDFFAFAFA666666FAFAFA666666FAFAFAFA
        FAFAFAFAFAFAFAFAFAFAFA000033000033000033E8DFDF666666666666E8DFDF
        FAFAFAFAFAFA666666FAFAFAFAFAFA8181812D2D2D2D2D2DFAFAFA000033FAFA
        FA000033E8DFDF666666666666E8DFDFFAFAFAFAFAFA666666FAFAFAFAFAFA2D
        2D2D33CCFF0066992D2D2DFAFAFA000033000033E8DFDF666666666666E8DFDF
        FAFAFAFAFAFA666666FAFAFAFAFAFA2D2D2D00F2FF33CCFF0066992D2D2DFAFA
        FAFAFAFAE8DFDF666666666666E8DFDFFAFAFAFAFAFA666666FAFAFAFAFAFAFA
        FAFA2D2D2D00F2FF33CCFF0066992D2D2DFAFAFAE8DFDF666666666666E8DFDF
        FAFAFA666666FAFAFA666666FAFAFAFAFAFAFAFAFA2D2D2D00F2FF33CCFF0066
        992D2D2DFAFAFA666666666666E8DFDFFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAFA
        FAFAFAFAFAFAFAFA4C144C3476B14D63B12A3B842E2C2E835783666666E8DFDF
        E8DFDFE8DFDFE8DFDFE8DFDFE8DFDFE8DFDFE8DFDFE8DFDFB686B62D2D2D00F2
        FF4878C02E2C2E2C007199999966666666666666666666666666666666666666
        6666666666666666662E667F4A7F441A44441A443A12B22D0071999999999999
        999999999999999999999999999999999999999999999999815081948B94958C
        952A0072120076979297FAFAFAFAFAFAFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA
        FAFAFAFAFAFAFAFAD8BDD8BE93BEC39BC3E5D3E5F9F9F9FAFAFA}
    end
    object Button102: TdxButton
      Left = 553
      Top = 14
      Width = 160
      Height = 26
      OnClick = Button102Click
      Caption = '¿¢¼¿ÀÚ·áºÒ·¯¿À±â'
      TabOrder = 3
      Glyph.Data = {
        36030000424D3603000000000000360000002800000010000000100000000100
        18000000000000030000120B0000120B00000000000000000000FFFFFFFFFFFF
        FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC6C6C61A1A1A1A1A1A1B1B1B1A1A1A1B1B
        1B1B1B1B1C1C1C858585FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6D6D6DFFFFFF90
        9090D9D9D9D9D9D9DADADAE1E0E0E6E2E2DEDEDEDCDCDC565656FFFFFFFFFFFF
        FFFFFF6D6D6D6D6D6D6D6D6D6D6D6D989898FAFAFAFAFAFAFBFBFB8C92925884
        84C3BCBCFAFAFA545454FFFFFFFFFFFF6D6D6DFFFFFFFFFFFF6D6D6DFFFFFF97
        9797FAFAFA7474746E75752C9F9F02A6A60D5757E5E3E3585757FFFFFFFFFFFF
        6D6D6DFFFFFFFFFFFFFFFFFFFFFFFF989898FAFAFA9D9D9D7288881AB5B5019B
        9B017878E2E3E3595858FFFFFFFFFFFF6D6D6DFFFFFFFFFFFFFFFFFFFFFFFF97
        9797FAFAFAB0B0B0BAB6B696B2B2239C9CAEAEAEFAFAFA555555FFFFFFFFFFFF
        FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF989898FAFAFA8787876061615350505553
        53CAC8C8FAFAFA555555FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF98
        9898FAFAFA979797797979D8D8D87E7E7ECDCDCDFAFAFA555555FFFFFFE8E8F0
        575758FCFCFCFFFFFFFFFFFFFFFFFF979797FAFAFAD4D4D4C7C7C7F1F1F1C8C8
        C8EDEDEDFAFAFA535353F5F5FDB7B786282819848485FFFFFFFFFFFFFFFFFF9E
        9E9ED8D8D8DFDFDFD5D5D5CDCDCDE1E1E1DADADAC8C8C8646464B2B28AE5E510
        4747295C5C629F9F9FFFFFFFFFFFFFC2C2C2767676A7A7A7A0A0A09E9E9EA4A4
        A4A6A6A68B8B8B888888999967C9C93E9C9C0B58585249494CFFFFFFFFFFFFFF
        FFFFFFFFFFFFFFFFAC75AC693569B17CB1BF94BFFDFBFDBD91BD8F8F76BFBF1A
        C7C7019191071E1E21FFFFFFFFFFFF6D6D6DFFFFFFFFFFFFB889B86D6D6DFFFF
        FFC096C0FCF9FCBD91BDD4D4CBBDBD2FBFBF00C6C6006A6A06FFFFFF6D6D6D6D
        6D6D6D6D6D6D6D6D693269B17CB1C096C0C096C0C49CC4BB8EBBFFFFFFD3D3CE
        BFBF22BFBF22D6D6CCFFFFFFFFFFFF6D6D6DFFFFFFFFFFFFB685B6F1E7F1F2E9
        F2C096C0E4D1E4F9F4F9FFFFFFFFFFFFC8C8A8C8C8A8FFFFFFFFFFFFFFFFFFFF
        FFFFFFFFFFFFFFFFD8BDD8BE93BEC39BC3E5D3E5FEFDFEFFFFFF}
    end
    object Edit003: TFlatEdit
      Left = 14
      Top = 31
      Width = 83
      Height = 18
      ColorFlat = clWhite
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '±¼¸²'
      Font.Style = [fsBold]
      MaxLength = 100
      ParentFont = False
      TabOrder = 4
      Visible = False
    end
    object Edit004: TFlatEdit
      Left = 102
      Top = 31
      Width = 83
      Height = 18
      ColorFlat = clWhite
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '±¼¸²'
      Font.Style = [fsBold]
      MaxLength = 100
      ParentFont = False
      TabOrder = 5
      Visible = False
    end
  end
  object DataSource1: TDataSource
    DataSet = Em_Sub01
    Left = 24
    Top = 296
  end
  object Em_Sub01: TClientDataSet
    Aggregates = <>
    Params = <>
    Left = 56
    Top = 296
    object Em_Sub01HCODE: TStringField
      FieldName = 'HCODE'
      Size = 5
    end
    object Em_Sub01HNAME: TStringField
      FieldName = 'HNAME'
      Size = 50
    end
    object Em_Sub01NAME0: TStringField
      FieldName = 'NAME0'
      Size = 50
    end
    object Em_Sub01NAME1: TStringField
      FieldName = 'NAME1'
      Size = 80
    end
    object Em_Sub01NAME2: TStringField
      FieldName = 'NAME2'
      Size = 80
    end
    object Em_Sub01GSQUT: TFloatField
      FieldName = 'GSQUT'
    end
    object Em_Sub01GDANG: TFloatField
      FieldName = 'GDANG'
    end
    object Em_Sub01GSSUM: TFloatField
      FieldName = 'GSSUM'
    end
    object Em_Sub01GBIGO: TStringField
      FieldName = 'GBIGO'
      Size = 80
    end
    object Em_Sub01CODE1: TStringField
      FieldName = 'CODE1'
      Size = 3
    end
    object Em_Sub01CODE2: TStringField
      FieldName = 'CODE2'
      Size = 3
    end
  end
  object OpenDialog1: TOpenDialog
    Filter = 
      'Excel 4.0(*.xls)|*.xls|Excel 5.0(*.xls)|*.xls|Tabbed Text(*.txt)' +
      '|*.txt|Formula One[*.vts]|*.vts|¿¢¼¿|*.xls|*.xlsx|*.xlsx'
    FilterIndex = 6
    Left = 24
    Top = 264
  end
  object SaveDialog1: TSaveDialog
    Filter = 
      'Excel 4.0(*.xls)|*.xls|Excel 5.0(*.xls)|*.xls|Tabbed Text(*.txt)' +
      '|*.txt|Formula One[*.vts]|*.vts'
    Left = 56
    Top = 264
  end
end
