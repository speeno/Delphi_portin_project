object Sobo17: TSobo17
  Left = 1975
  Top = 74
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '출판사관리'
  ClientHeight = 627
  ClientWidth = 917
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
  OnCreate = FormCreate
  OnPaint = FormPaint
  PixelsPerInch = 96
  TextHeight = 12
  object CornerButton2: TCornerButton
    Left = 4
    Top = 3
    Width = 21
    Height = 318
    Cursor = crArrow
    BevelColor = clBlue
    BevelWidth = 1
    MouseDownColor = clBlue
    Transparent = False
    CornerOptions = [cnTopLeft, cnBottomLeft]
    CornerSize = 10
  end
  object CornerButton3: TCornerButton
    Left = 4
    Top = 320
    Width = 21
    Height = 273
    Cursor = crArrow
    BevelColor = clTeal
    BevelWidth = 1
    MouseDownColor = clTeal
    Transparent = False
    CornerOptions = [cnTopLeft, cnBottomLeft]
    CornerSize = 10
  end
  object CornerButton4: TCornerButton
    Left = 4
    Top = 594
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
  object Label002: TmyLabel3d
    Left = 9
    Top = 104
    Width = 13
    Height = 65
    Caption = '출'#13#10'판'#13#10'사'#13#10'현'#13#10'황'
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
  object Label003: TmyLabel3d
    Left = 9
    Top = 424
    Width = 13
    Height = 52
    Caption = '계'#13#10'약'#13#10'내'#13#10'용'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clTeal
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
    Top = 598
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
    Width = 349
    Height = 317
    ParentColor = True
    TabOrder = 0
    UseDockManager = True
    object DBGrid101: TDBGrid
      Left = 1
      Top = 1
      Width = 347
      Height = 312
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
      OnDblClick = DBGrid101DblClick
      OnEnter = DBGrid101Enter
      OnExit = DBGrid101Exit
      OnKeyDown = DBGrid101KeyDown
      OnKeyPress = DBGrid101KeyPress
      OnTitleClick = DBGrid101TitleClick
      Columns = <
        item
          Expanded = False
          FieldName = 'GCODE'
          Font.Charset = HANGEUL_CHARSET
          Font.Color = clBlack
          Font.Height = -12
          Font.Name = '굴림'
          Font.Style = [fsBold]
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Title.Font.Charset = HANGEUL_CHARSET
          Title.Font.Color = clBlack
          Title.Font.Height = -12
          Title.Font.Name = '굴림체'
          Title.Font.Style = [fsBold]
          Width = 50
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
          Title.Caption = '출판사명'
          Title.Font.Charset = HANGEUL_CHARSET
          Title.Font.Color = clBlack
          Title.Font.Height = -12
          Title.Font.Name = '굴림체'
          Title.Font.Style = [fsBold]
          Width = 248
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'OCODE'
          Title.Alignment = taCenter
          Title.Caption = '^'
          Title.Font.Charset = HANGEUL_CHARSET
          Title.Font.Color = clBlack
          Title.Font.Height = -12
          Title.Font.Name = '굴림체'
          Title.Font.Style = [fsBold]
          Width = 16
          Visible = True
        end>
    end
    object StBar101: TStatusBar
      Left = 1
      Top = 313
      Width = 347
      Height = 3
      Panels = <
        item
          Alignment = taRightJustify
          Bevel = pbRaised
          Width = 340
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
    Left = 34
    Top = 384
    Width = 231
    Height = 113
    ParentColor = True
    TabOrder = 2
    UseDockManager = True
    object DBGrid201: TDBGrid
      Left = 1
      Top = 1
      Width = 229
      Height = 111
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
      OnExit = DBGrid201Exit
      OnKeyDown = DBGrid201KeyDown
      OnKeyPress = DBGrid201KeyPress
      Columns = <
        item
          Expanded = False
          FieldName = 'GCODE'
          Font.Charset = HANGEUL_CHARSET
          Font.Color = clBlack
          Font.Height = -12
          Font.Name = '굴림'
          Font.Style = [fsBold]
          Title.Alignment = taCenter
          Title.Caption = '코드'
          Title.Font.Charset = HANGEUL_CHARSET
          Title.Font.Color = clBlack
          Title.Font.Height = -12
          Title.Font.Name = '굴림체'
          Title.Font.Style = [fsBold]
          Width = 40
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
          Title.Caption = '출판사구분'
          Title.Font.Charset = HANGEUL_CHARSET
          Title.Font.Color = clBlack
          Title.Font.Height = -12
          Title.Font.Name = '굴림체'
          Title.Font.Style = [fsBold]
          Width = 159
          Visible = True
        end>
    end
  end
  object Panel004: TFlatPanel
    Left = 264
    Top = 384
    Width = 537
    Height = 113
    ParentColor = True
    TabOrder = 3
    UseDockManager = True
    object Label200: TmyLabel3d
      Left = 8
      Top = 8
      Width = 110
      Height = 21
      Caption = '출판사구분'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clRed
      Font.Height = -21
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AStyle3D = Resit3d
      AShadeLTSet = False
    end
    object Panel200: TFlatPanel
      Left = 255
      Top = 1
      Width = 281
      Height = 41
      ParentColor = True
      ColorHighLight = clBtnFace
      ColorShadow = clBtnFace
      TabOrder = 4
      UseDockManager = True
      object Button201: TFlatButton
        Left = 16
        Top = 8
        Width = 73
        Height = 25
        Color = clInfoBk
        Caption = '추가'
        Glyph.Data = {
          76010000424D7601000000000000760000002800000020000000100000000100
          04000000000000010000130B0000130B00001000000000000000000000000000
          800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
          FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333333333
          33333333FF33333333FF333993333333300033377F3333333777333993333333
          300033F77FFF3333377739999993333333333777777F3333333F399999933333
          33003777777333333377333993333333330033377F3333333377333993333333
          3333333773333333333F333333333333330033333333F33333773333333C3333
          330033333337FF3333773333333CC333333333FFFFF77FFF3FF33CCCCCCCCCC3
          993337777777777F77F33CCCCCCCCCC3993337777777777377333333333CC333
          333333333337733333FF3333333C333330003333333733333777333333333333
          3000333333333333377733333333333333333333333333333333}
        Layout = blGlyphLeft
        NumGlyphs = 2
        ParentColor = False
        TabOrder = 0
        OnClick = Button201Click
      end
      object Button202: TFlatButton
        Left = 104
        Top = 8
        Width = 73
        Height = 25
        Color = clInfoBk
        Caption = '등록'
        Glyph.Data = {
          76010000424D7601000000000000760000002800000020000000100000000100
          04000000000000010000120B0000120B00001000000000000000000000000000
          800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
          FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333000000
          000033333377777777773333330FFFFFFFF03FF3FF7FF33F3FF700300000FF0F
          00F077F777773F737737E00BFBFB0FFFFFF07773333F7F3333F7E0BFBF000FFF
          F0F077F3337773F3F737E0FBFBFBF0F00FF077F3333FF7F77F37E0BFBF00000B
          0FF077F3337777737337E0FBFBFBFBF0FFF077F33FFFFFF73337E0BF0000000F
          FFF077FF777777733FF7000BFB00B0FF00F07773FF77373377373330000B0FFF
          FFF03337777373333FF7333330B0FFFF00003333373733FF777733330B0FF00F
          0FF03333737F37737F373330B00FFFFF0F033337F77F33337F733309030FFFFF
          00333377737FFFFF773333303300000003333337337777777333}
        Layout = blGlyphLeft
        NumGlyphs = 2
        ParentColor = False
        TabOrder = 1
        OnClick = Button202Click
      end
      object Button203: TFlatButton
        Left = 192
        Top = 8
        Width = 73
        Height = 25
        Color = clInfoBk
        Caption = '삭제'
        Glyph.Data = {
          76010000424D7601000000000000760000002800000020000000100000000100
          04000000000000010000130B0000130B00001000000000000000000000000000
          800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
          FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333333333
          333333333333333333FF33333333333330003333333333333777333333333333
          300033FFFFFF3333377739999993333333333777777F3333333F399999933333
          3300377777733333337733333333333333003333333333333377333333333333
          3333333333333333333F333333333333330033333F33333333773333C3333333
          330033337F3333333377333CC3333333333333F77FFFFFFF3FF33CCCCCCCCCC3
          993337777777777F77F33CCCCCCCCCC399333777777777737733333CC3333333
          333333377F33333333FF3333C333333330003333733333333777333333333333
          3000333333333333377733333333333333333333333333333333}
        Layout = blGlyphLeft
        NumGlyphs = 2
        ParentColor = False
        TabOrder = 2
        OnClick = Button203Click
      end
    end
    object Panel201: TFlatPanel
      Left = 8
      Top = 44
      Width = 90
      Height = 22
      Caption = '구분코드'
      ParentColor = True
      TabOrder = 2
      UseDockManager = True
    end
    object Panel202: TFlatPanel
      Left = 8
      Top = 76
      Width = 90
      Height = 22
      Caption = '구 분 명'
      ParentColor = True
      TabOrder = 3
      UseDockManager = True
    end
    object Edit201: TFlatEdit
      Left = 104
      Top = 44
      Width = 65
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
      TabOrder = 0
      OnChange = Edit101Change
      OnKeyDown = Edit101KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit202: TFlatEdit
      Left = 104
      Top = 76
      Width = 209
      Height = 22
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 20
      ParentFont = False
      TabOrder = 1
      OnChange = Edit101Change
      OnKeyDown = Edit113KeyDown
      OnKeyPress = Edit113KeyPress
    end
  end
  object Panel007: TFlatPanel
    Left = 24
    Top = 595
    Width = 889
    Height = 29
    Color = clInfoBk
    TabOrder = 4
    UseDockManager = True
    object ProgressBar0: TFlatProgressBar
      Left = 424
      Top = 5
      Width = 336
      Height = 19
      Visible = False
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
      Visible = False
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
      Visible = False
    end
  end
  object Panel002: TFlatPanel
    Left = 376
    Top = 4
    Width = 537
    Height = 317
    ParentColor = True
    TabOrder = 1
    UseDockManager = True
    object Label100: TmyLabel3d
      Left = 8
      Top = 8
      Width = 100
      Height = 19
      Caption = '출판사현황'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clRed
      Font.Height = -19
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Label108: TmyLabel3d
      Left = 161
      Top = 65
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
    object Label109: TmyLabel3d
      Left = 377
      Top = 134
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
    object Label110: TmyLabel3d
      Left = 377
      Top = 157
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
    object Label101: TmyLabel3d
      Left = 48
      Top = 336
      Width = 52
      Height = 12
      Caption = '기본수량'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      Visible = False
      AShadeLTSet = False
    end
    object Label102: TmyLabel3d
      Left = 160
      Top = 336
      Width = 52
      Height = 12
      Caption = '기본금액'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      Visible = False
      AShadeLTSet = False
    end
    object Label103: TmyLabel3d
      Left = 256
      Top = 336
      Width = 52
      Height = 12
      Caption = '추가금액'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      Visible = False
      AShadeLTSet = False
    end
    object Label104: TmyLabel3d
      Left = 360
      Top = 336
      Width = 39
      Height = 12
      Caption = '미수금'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      Visible = False
      AShadeLTSet = False
    end
    object Label107: TmyLabel3d
      Left = 471
      Top = 98
      Width = 59
      Height = 12
      Caption = '담당/창고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      Transparent = True
      AShadeLTSet = False
    end
    object Panel100: TFlatPanel
      Left = 231
      Top = 1
      Width = 298
      Height = 41
      ParentColor = True
      ColorHighLight = clBtnFace
      ColorShadow = clBtnFace
      TabOrder = 45
      UseDockManager = True
      object Button101: TdxButton
        Left = 17
        Top = 6
        Width = 88
        Height = 26
        OnClick = Button101Click
        Caption = '새화면'
        TabOrder = 0
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
        Left = 113
        Top = 6
        Width = 88
        Height = 26
        OnClick = Button102Click
        Caption = '저장'
        TabOrder = 1
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
      object Button103: TdxButton
        Left = 209
        Top = 6
        Width = 88
        Height = 26
        OnClick = Button103Click
        Caption = '삭제'
        TabOrder = 2
        Glyph.Data = {
          36030000424D3603000000000000360000002800000010000000100000000100
          18000000000000030000120B0000120B00000000000000000000FFFFFFFFFFFF
          FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
          FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6D6D6DFFFFFF00000000
          0000000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
          6D6D6D6D6D6D6D6D6D6D6D6D808080FFFFFFFFFF00808000FFFFFFFFFF008080
          00000000000000FFFFFFFFFFFF6D6D6DFFFFFFFFFFFF6D6D6DFFFFFF808080FF
          FF00FFFFFF808000FFFF00FFFFFF808000000000808000000000FFFFFF6D6D6D
          FFFFFFFFFFFFFFFFFFFFFFFF808080808000808000000000808000FFFFFF8080
          00000000808000000000FFFFFF6D6D6DFFFFFFFFFFFFFFFFFFFFFFFF808080FF
          FFFFFFFF00808000000000000000000000000000808000000000FFFFFFFFFFFF
          FFFFFFFFFFFFFFFFFFFFFFFF808080FFFF00FFFFFF8080000000008080008080
          00808000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF80
          8080FFFF00FFFFFF000000808000FFFFFF808000808000000000FFFFFFE8E8F0
          575758FCFCFCFFFFFFFFFFFFFFFFFFFFFFFF808080808000808000FFFFFFFFFF
          00808000808000000000F5F5FDB7B786282819848485FFFFFFFFFFFFFFFFFFFF
          FFFFFFFFFF808080808080808080808080808080808080808080B2B28AE5E510
          4747295C5C629F9F9FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6D6D6DFFFF
          FFFFFFFFFFFFFFFFFFFF999967C9C93E9C9C0B58585249494CFFFFFFFFFFFFFF
          FFFFFFFFFFFFFFFFAC75AC693569B17CB1BF94BFFDFBFDBD91BD8F8F76BFBF1A
          C7C7019191071E1E21FFFFFFFFFFFF6D6D6DFFFFFFFFFFFFB889B86D6D6DFFFF
          FFC096C0FCF9FCBD91BDD4D4CBBDBD2FBFBF00C6C6006A6A06FFFFFF6D6D6D6D
          6D6D6D6D6D6D6D6D693269B17CB1C096C0C096C0C49CC4BB8EBBFFFFFFD3D3CE
          BFBF22BFBF22D6D6CCFFFFFFFFFFFF6D6D6DFFFFFFFFFFFFB685B6F1E7F1F2E9
          F2C096C0E4D1E4F9F4F9FFFFFFFFFFFFC8C8A8C8C8A8FFFFFFFFFFFFFFFFFFFF
          FFFFFFFFFFFFFFFFD8BDD8BE93BEC39BC3E5D3E5FEFDFEFFFFFF}
      end
    end
    object Panel101: TFlatPanel
      Left = 8
      Top = 41
      Width = 90
      Height = 19
      Caption = '출판사구분'
      ParentColor = True
      TabOrder = 29
      UseDockManager = True
    end
    object Panel103: TFlatPanel
      Left = 8
      Top = 64
      Width = 90
      Height = 19
      Caption = '출판사코드'
      ParentColor = True
      TabOrder = 31
      UseDockManager = True
    end
    object Panel102: TFlatPanel
      Left = 240
      Top = 41
      Width = 90
      Height = 19
      Caption = '출판사지역'
      ParentColor = True
      TabOrder = 30
      UseDockManager = True
    end
    object Panel105: TFlatPanel
      Left = 240
      Top = 64
      Width = 90
      Height = 19
      Caption = '출판사명'
      ParentColor = True
      TabOrder = 32
      UseDockManager = True
    end
    object Panel106: TFlatPanel
      Left = 8
      Top = 87
      Width = 90
      Height = 19
      Caption = '대 표 자'
      ParentColor = True
      TabOrder = 33
      UseDockManager = True
    end
    object Panel107: TFlatPanel
      Left = 240
      Top = 87
      Width = 90
      Height = 19
      Caption = '사업자번호'
      ParentColor = True
      TabOrder = 34
      UseDockManager = True
    end
    object Panel109: TFlatPanel
      Left = 240
      Top = 110
      Width = 90
      Height = 19
      Caption = '종     목'
      ParentColor = True
      TabOrder = 36
      UseDockManager = True
    end
    object Panel108: TFlatPanel
      Left = 8
      Top = 110
      Width = 90
      Height = 19
      Caption = '업     태'
      ParentColor = True
      TabOrder = 35
      UseDockManager = True
    end
    object Panel110: TFlatPanel
      Left = 8
      Top = 133
      Width = 90
      Height = 19
      Caption = '담 당 자'
      ParentColor = True
      TabOrder = 37
      UseDockManager = True
    end
    object Panel112: TFlatPanel
      Left = 240
      Top = 133
      Width = 90
      Height = 19
      Caption = '전화번호'
      ParentColor = True
      TabOrder = 38
      UseDockManager = True
    end
    object Panel114: TFlatPanel
      Left = 240
      Top = 156
      Width = 90
      Height = 19
      Caption = '팩스번호'
      ParentColor = True
      TabOrder = 40
      UseDockManager = True
    end
    object Panel111: TFlatPanel
      Left = 8
      Top = 156
      Width = 90
      Height = 19
      Caption = '우편번호'
      ParentColor = True
      TabOrder = 39
      UseDockManager = True
    end
    object Panel116: TFlatPanel
      Left = 8
      Top = 179
      Width = 90
      Height = 38
      Caption = '주소'
      ParentColor = True
      TabOrder = 41
      UseDockManager = True
    end
    object Panel119: TFlatPanel
      Left = 240
      Top = 244
      Width = 90
      Height = 19
      Caption = '보증금액'
      ParentColor = True
      TabOrder = 43
      UseDockManager = True
    end
    object Edit101: TFlatComboBox
      Left = 104
      Top = 41
      Width = 129
      Height = 20
      Color = clWindow
      DropDownCount = 9
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ItemHeight = 12
      ParentFont = False
      TabOrder = 0
      ItemIndex = -1
      OnChange = Edit101Change
      OnKeyDown = Edit112KeyDown
      OnKeyPress = Edit112KeyPress
    end
    object Edit102: TFlatEdit
      Left = 336
      Top = 41
      Width = 81
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 6
      ParentFont = False
      TabOrder = 1
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit103: TFlatEdit
      Left = 104
      Top = 64
      Width = 57
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Enabled = False
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 5
      ParentFont = False
      TabOrder = 2
      OnChange = Edit101Change
      OnExit = Edit101Exit
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit104: TFlatEdit
      Left = 176
      Top = 64
      Width = 57
      Height = 20
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -16
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 5
      ParentFont = False
      TabOrder = 3
      Visible = False
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit105: TFlatEdit
      Left = 336
      Top = 64
      Width = 193
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 50
      ParentFont = False
      TabOrder = 4
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit106: TFlatEdit
      Left = 104
      Top = 87
      Width = 113
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 30
      ParentFont = False
      TabOrder = 5
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit107: TFlatEdit
      Left = 336
      Top = 87
      Width = 129
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 12
      ParentFont = False
      TabOrder = 6
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit108: TFlatEdit
      Left = 104
      Top = 110
      Width = 113
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 30
      ParentFont = False
      TabOrder = 7
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit109: TFlatEdit
      Left = 336
      Top = 110
      Width = 113
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 30
      ParentFont = False
      TabOrder = 8
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit110: TFlatEdit
      Left = 104
      Top = 133
      Width = 113
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 20
      ParentFont = False
      TabOrder = 9
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit111: TFlatEdit
      Left = 104
      Top = 156
      Width = 89
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 7
      ParentFont = False
      TabOrder = 10
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit114KeyPress
    end
    object Edit112: TFlatEdit
      Left = 336
      Top = 133
      Width = 42
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 4
      ParentFont = False
      TabOrder = 11
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit113: TFlatEdit
      Left = 392
      Top = 133
      Width = 113
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 20
      ParentFont = False
      TabOrder = 12
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit114: TFlatEdit
      Left = 336
      Top = 156
      Width = 42
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 4
      ParentFont = False
      TabOrder = 13
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit115: TFlatEdit
      Left = 392
      Top = 156
      Width = 113
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 20
      ParentFont = False
      TabOrder = 14
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit116: TFlatEdit
      Left = 104
      Top = 179
      Width = 425
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 90
      ParentFont = False
      TabOrder = 15
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit117: TFlatEdit
      Left = 104
      Top = 198
      Width = 425
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 90
      ParentFont = False
      TabOrder = 16
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit118: TFlatEdit
      Left = 336
      Top = 290
      Width = 193
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 50
      ParentFont = False
      TabOrder = 24
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit102KeyPress
    end
    object Button104: TFlatButton
      Left = 192
      Top = 156
      Width = 25
      Height = 19
      Color = clBtnFace
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
      ParentColor = False
      TabOrder = 44
      OnClick = Button104Click
    end
    object Panel118: TFlatPanel
      Left = 240
      Top = 290
      Width = 90
      Height = 19
      Caption = '비고'
      ParentColor = True
      TabOrder = 42
      UseDockManager = True
    end
    object Edit119: TFlatNumber
      Left = 144
      Top = 348
      Width = 89
      Height = 21
      Digits = 0
      Max = 99999999
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 27
      Text = '0'
      Visible = False
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit120: TFlatNumber
      Left = 240
      Top = 348
      Width = 89
      Height = 21
      Digits = 0
      Max = 99999999
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 25
      Text = '0'
      Visible = False
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit121: TFlatNumber
      Left = 336
      Top = 348
      Width = 89
      Height = 21
      Digits = 0
      Max = 99999999
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 28
      Text = '0'
      Visible = False
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit122: TFlatNumber
      Left = 336
      Top = 244
      Width = 89
      Height = 19
      Digits = 0
      Max = 99999999
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 8
      ParentFont = False
      TabOrder = 20
      Text = '0'
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel123: TFlatPanel
      Left = 8
      Top = 290
      Width = 90
      Height = 19
      Caption = '세금계산서'
      ParentColor = True
      TabOrder = 46
      UseDockManager = True
    end
    object CheckBox1: TFlatCheckBox
      Left = 104
      Top = 293
      Width = 73
      Height = 15
      Caption = '발행유무'
      Color = clBtnFace
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 23
      TabStop = True
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel124: TFlatPanel
      Left = 240
      Top = 267
      Width = 90
      Height = 19
      Caption = '참고내용'
      ParentColor = True
      TabOrder = 47
      UseDockManager = True
    end
    object Edit124: TFlatComboBox
      Left = 8
      Top = 348
      Width = 129
      Height = 20
      Color = clWindow
      DropDownCount = 9
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ItemHeight = 12
      Items.Strings = (
        '(시내부수)만 추가한 부수'
        '(시내+지방)을 추가한 부수')
      ParentFont = False
      TabOrder = 26
      Text = '(시내부수)만 추가한 부수'
      Visible = False
      ItemIndex = 0
      OnKeyDown = Edit115KeyDown
      OnKeyPress = Edit115KeyPress
    end
    object Panel125: TFlatPanel
      Left = 8
      Top = 244
      Width = 90
      Height = 19
      Caption = '계약일자'
      ParentColor = True
      TabOrder = 48
      UseDockManager = True
    end
    object Edit123: TFlatMaskEdit
      Left = 104
      Top = 244
      Width = 97
      Height = 19
      ColorFlat = clWhite
      AutoSize = False
      BorderStyle = bsNone
      Color = clWhite
      EditMask = '!9999.!99.99;1; '
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 10
      ParentFont = False
      TabOrder = 19
      Text = '2002.01.01'
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
      ImeName = '한국어(한글) (MS-IME98)'
    end
    object Panel126: TFlatPanel
      Left = 8
      Top = 267
      Width = 90
      Height = 19
      Caption = '핸드폰번호'
      ParentColor = True
      TabOrder = 49
      UseDockManager = True
    end
    object Edit125: TFlatEdit
      Left = 104
      Top = 267
      Width = 129
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 20
      ParentFont = False
      TabOrder = 21
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit126: TFlatEdit
      Left = 336
      Top = 267
      Width = 193
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 50
      ParentFont = False
      TabOrder = 22
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object CheckBox2: TFlatCheckBox
      Left = 432
      Top = 44
      Width = 97
      Height = 15
      Caption = '자체반품재고'
      Color = clBtnFace
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 50
      TabStop = True
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object CheckBox3: TFlatCheckBox
      Left = 456
      Top = 247
      Width = 73
      Height = 15
      Caption = 'List별도'
      Color = clBtnFace
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clGreen
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentColor = False
      ParentFont = False
      TabOrder = 51
      TabStop = True
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel217: TFlatPanel
      Left = 8
      Top = 221
      Width = 90
      Height = 19
      Caption = '계좌번호'
      ParentColor = True
      TabOrder = 52
      UseDockManager = True
    end
    object Edit127_: TFlatEdit
      Left = 104
      Top = 221
      Width = 425
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 40
      ParentFont = False
      TabOrder = 18
      Visible = False
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit127: TFlatComboBox
      Left = 104
      Top = 220
      Width = 425
      Height = 20
      Color = clWindow
      DropDownCount = 9
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ItemHeight = 12
      ParentFont = False
      TabOrder = 17
      ItemIndex = -1
      OnKeyDown = Edit115KeyDown
      OnKeyPress = Edit115KeyPress
    end
    object Button000: TdxButton
      Left = 136
      Top = 7
      Width = 89
      Height = 26
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clRed
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = [fsBold]
      ParentFont = False
      Visible = False
      OnClick = FormShow
      Style.Theme = OfficeXP
      Caption = '검색'
      TabOrder = 53
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
    object Edit128: TFlatEdit
      Left = 472
      Top = 110
      Width = 57
      Height = 19
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = [fsBold]
      MaxLength = 10
      ParentFont = False
      TabOrder = 54
      OnChange = Edit101Change
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
  end
  object Panel238: TFlatPanel
    Left = 354
    Top = 599
    Width = 65
    Height = 22
    Caption = '비고'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clWindowText
    Font.Height = -12
    Font.Name = '굴림'
    Font.Style = []
    Color = clInfoBk
    ColorHighLight = clInfoBk
    TabOrder = 6
    UseDockManager = True
  end
  object Edit238: TFlatEdit
    Left = 421
    Top = 599
    Width = 404
    Height = 21
    ColorFlat = clWhite
    ImeName = '한국어(한글) (MS-IME98)'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clBlack
    Font.Height = -15
    Font.Name = '굴림'
    Font.Style = []
    MaxLength = 40
    ParentFont = False
    TabOrder = 7
    OnKeyDown = Edit111KeyDown
    OnKeyPress = Edit111KeyPress
  end
  object Edit236: TFlatNumber
    Left = 824
    Top = 599
    Width = 74
    Height = 21
    Digits = 0
    Max = 99999999.000064
    FormatStr = '%8.0n'
    ColorFlat = 8454143
    ImeName = '한국어(한글) (MS-IME98)'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = '굴림'
    Font.Style = []
    MaxLength = 8
    ParentFont = False
    TabOrder = 8
    Text = '0'
    OnKeyDown = Edit111KeyDown
    OnKeyPress = Edit111KeyPress
  end
  object Panel701: TFlatPanel
    Left = 24
    Top = 320
    Width = 665
    Height = 273
    ParentColor = True
    TabOrder = 9
    UseDockManager = True
    object Editor: TRxRichEdit
      Left = 1
      Top = 1
      Width = 663
      Height = 271
      Align = alClient
      BorderStyle = bsNone
      ImeName = 'Microsoft IME 2003'
      TabOrder = 0
    end
  end
  object Panel702: TFlatPanel
    Left = 688
    Top = 320
    Width = 225
    Height = 273
    ParentColor = True
    TabOrder = 10
    UseDockManager = True
    object Button701: TFlatButton
      Left = 10
      Top = 232
      Width = 95
      Height = 33
      Color = clAqua
      Caption = '수정/저장'
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000120B0000120B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333000000
        000033333377777777773333330FFFFFFFF03FF3FF7FF33F3FF700300000FF0F
        00F077F777773F737737E00BFBFB0FFFFFF07773333F7F3333F7E0BFBF000FFF
        F0F077F3337773F3F737E0FBFBFBF0F00FF077F3333FF7F77F37E0BFBF00000B
        0FF077F3337777737337E0FBFBFBFBF0FFF077F33FFFFFF73337E0BF0000000F
        FFF077FF777777733FF7000BFB00B0FF00F07773FF77373377373330000B0FFF
        FFF03337777373333FF7333330B0FFFF00003333373733FF777733330B0FF00F
        0FF03333737F37737F373330B00FFFFF0F033337F77F33337F733309030FFFFF
        00333377737FFFFF773333303300000003333337337777777333}
      Layout = blGlyphLeft
      NumGlyphs = 2
      ParentColor = False
      TabOrder = 0
      OnClick = Button701Click
    end
    object Button702: TFlatButton
      Left = 116
      Top = 232
      Width = 95
      Height = 33
      Color = clAqua
      Caption = '계약내용'
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000120B0000120B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333000000
        000033333377777777773333330FFFFFFFF03FF3FF7FF33F3FF700300000FF0F
        00F077F777773F737737E00BFBFB0FFFFFF07773333F7F3333F7E0BFBF000FFF
        F0F077F3337773F3F737E0FBFBFBF0F00FF077F3333FF7F77F37E0BFBF00000B
        0FF077F3337777737337E0FBFBFBFBF0FFF077F33FFFFFF73337E0BF0000000F
        FFF077FF777777733FF7000BFB00B0FF00F07773FF77373377373330000B0FFF
        FFF03337777373333FF7333330B0FFFF00003333373733FF777733330B0FF00F
        0FF03333737F37737F373330B00FFFFF0F033337F77F33337F733309030FFFFF
        00333377737FFFFF773333303300000003333337337777777333}
      Layout = blGlyphLeft
      NumGlyphs = 2
      ParentColor = False
      TabOrder = 1
      OnClick = Button702Click
    end
    object ToolBar1: TToolBar
      Left = 1
      Top = 25
      Width = 217
      Align = alNone
      AutoSize = True
      BorderWidth = 2
      Color = clBtnFace
      Flat = True
      Images = ToolbarImages
      Indent = 4
      ParentColor = False
      ParentShowHint = False
      ShowHint = True
      TabOrder = 2
      Wrapable = False
      object FontSize: TEdit
        Left = 4
        Top = 0
        Width = 26
        Height = 22
        Hint = 'Font Size|Select font size'
        ImeName = 'Microsoft IME 2003'
        TabOrder = 1
        Text = '0'
        OnChange = FontSizeChange
      end
      object UpDown1: TUpDown
        Left = 30
        Top = 0
        Width = 16
        Height = 22
        Associate = FontSize
        Min = 0
        Position = 0
        TabOrder = 2
        Wrap = False
      end
      object ToolButton10: TToolButton
        Left = 46
        Top = 0
        Width = 8
        ImageIndex = 7
        Style = tbsSeparator
      end
      object FontName: TComboBox
        Left = 54
        Top = 1
        Width = 147
        Height = 20
        Hint = 'Font Name|Select font name'
        Ctl3D = False
        DropDownCount = 10
        ImeName = 'Microsoft IME 2003'
        ItemHeight = 12
        ParentCtl3D = False
        TabOrder = 0
        OnChange = FontNameChange
      end
      object ToolButton11: TToolButton
        Left = 201
        Top = 0
        Width = 8
        ImageIndex = 8
        Style = tbsSeparator
      end
    end
    object ToolBar2: TToolBar
      Left = 1
      Top = 57
      Width = 139
      Align = alNone
      AutoSize = True
      BorderWidth = 2
      Color = clBtnFace
      Flat = True
      Images = ToolbarImages
      Indent = 4
      ParentColor = False
      ParentShowHint = False
      ShowHint = True
      TabOrder = 3
      Wrapable = False
      object UndoButton: TToolButton
        Left = 4
        Top = 0
        ImageIndex = 0
        OnClick = UndoButtonClick
      end
      object ToolButton1: TToolButton
        Left = 27
        Top = 0
        Width = 27
        ImageIndex = 7
        Style = tbsSeparator
      end
      object BoldButton: TToolButton
        Left = 54
        Top = 0
        Hint = 'Bold'
        ImageIndex = 4
        Style = tbsCheck
        OnClick = BoldButtonClick
      end
      object ItalicButton: TToolButton
        Left = 77
        Top = 0
        Hint = 'Italic'
        ImageIndex = 5
        Style = tbsCheck
        OnClick = ItalicButtonClick
      end
      object UnderlineButton: TToolButton
        Left = 100
        Top = 0
        Hint = 'Underline'
        ImageIndex = 6
        Style = tbsCheck
        OnClick = UnderlineButtonClick
      end
      object ToolButton16: TToolButton
        Left = 123
        Top = 0
        Width = 8
        ImageIndex = 12
        Style = tbsDivider
      end
    end
    object StandardToolBar: TToolBar
      Left = 1
      Top = 89
      Width = 139
      Align = alNone
      AutoSize = True
      BorderWidth = 2
      Color = clBtnFace
      Flat = True
      Images = ToolbarImages
      Indent = 4
      ParentColor = False
      ParentShowHint = False
      ShowHint = True
      TabOrder = 4
      Wrapable = False
      object BulletsButton: TToolButton
        Left = 4
        Top = 0
        Hint = 'Bullets|Enter bullet mode'
        ImageIndex = 10
        Style = tbsCheck
        OnClick = BulletsButtonClick
      end
      object ToolButton3: TToolButton
        Left = 27
        Top = 0
        Width = 27
        ImageIndex = 7
        Style = tbsSeparator
      end
      object LeftAlign: TToolButton
        Left = 54
        Top = 0
        Hint = 'Align Left'
        Grouped = True
        ImageIndex = 7
        Style = tbsCheck
        OnClick = LeftAlignClick
      end
      object CenterAlign: TToolButton
        Tag = 2
        Left = 77
        Top = 0
        Hint = 'Center'
        Grouped = True
        ImageIndex = 8
        Style = tbsCheck
        OnClick = CenterAlignClick
      end
      object RightAlign: TToolButton
        Tag = 1
        Left = 100
        Top = 0
        Hint = 'Align Right'
        Grouped = True
        ImageIndex = 9
        Style = tbsCheck
        OnClick = RightAlignClick
      end
      object ToolButton20: TToolButton
        Left = 123
        Top = 0
        Width = 8
        ImageIndex = 15
        Style = tbsDivider
      end
    end
    object FlatPanel27: TFlatPanel
      Left = 10
      Top = 3
      Width = 201
      Height = 22
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = clYellow
      ColorHighLight = clYellow
      ColorShadow = clYellow
      TabOrder = 5
      UseDockManager = True
      object Label305: TmyLabel3d
        Left = 24
        Top = 5
        Width = 150
        Height = 13
        Caption = '계 약 내 용  ( 메 모 장)'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -13
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
  end
  object Panel300: TFlatPanel
    Left = 24
    Top = 320
    Width = 889
    Height = 273
    Color = clInfoBk
    TabOrder = 5
    UseDockManager = True
    object Panel511: TFlatPanel
      Left = 664
      Top = 30
      Width = 65
      Height = 18
      Caption = '①전산업무'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 17
      UseDockManager = True
    end
    object Panel512: TFlatPanel
      Left = 664
      Top = 47
      Width = 65
      Height = 18
      Caption = '작업비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 18
      UseDockManager = True
    end
    object Panel521: TFlatPanel
      Left = 664
      Top = 110
      Width = 65
      Height = 35
      Caption = '③책보호대'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 19
      UseDockManager = True
    end
    object Panel531: TFlatPanel
      Left = 664
      Top = 150
      Width = 65
      Height = 35
      Caption = '④박스대'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 20
      UseDockManager = True
    end
    object Edit511: TFlatNumber
      Left = 731
      Top = 30
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 35
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit521: TFlatNumber
      Left = 731
      Top = 110
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 36
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit531: TFlatNumber
      Left = 731
      Top = 150
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 37
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit541: TFlatNumber
      Left = 515
      Top = 30
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 38
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit551: TFlatNumber
      Left = 515
      Top = 110
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 39
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel513: TFlatPanel
      Left = 792
      Top = 30
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 48
      UseDockManager = True
      object RadioButton511: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton512: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel522: TFlatPanel
      Left = 792
      Top = 110
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 49
      UseDockManager = True
      object RadioButton521: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton522: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel532: TFlatPanel
      Left = 792
      Top = 150
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 50
      UseDockManager = True
      object RadioButton531: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton532: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel542: TFlatPanel
      Left = 576
      Top = 30
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 51
      UseDockManager = True
      object RadioButton541: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton542: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel553: TFlatPanel
      Left = 576
      Top = 110
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 52
      UseDockManager = True
      object RadioButton551: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton552: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel301: TFlatPanel
      Left = 16
      Top = 3
      Width = 201
      Height = 22
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = clLime
      ColorHighLight = clLime
      ColorShadow = clLime
      TabOrder = 53
      UseDockManager = True
      object Label301: TmyLabel3d
        Left = 32
        Top = 3
        Width = 132
        Height = 16
        Caption = '배 송 계 약 내 용'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -16
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object Panel311: TFlatPanel
      Left = 16
      Top = 30
      Width = 65
      Height = 18
      Caption = '①기본부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 0
      UseDockManager = True
    end
    object Panel312: TFlatPanel
      Left = 16
      Top = 47
      Width = 65
      Height = 18
      Caption = '및 월정료'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 1
      UseDockManager = True
    end
    object Panel321: TFlatPanel
      Left = 16
      Top = 70
      Width = 65
      Height = 35
      Caption = '②기본금액'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 2
      UseDockManager = True
    end
    object Panel331: TFlatPanel
      Left = 16
      Top = 110
      Width = 65
      Height = 35
      Caption = '③초과부수'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 3
      UseDockManager = True
    end
    object Panel341: TFlatPanel
      Left = 16
      Top = 150
      Width = 65
      Height = 18
      Caption = '④지방'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 4
      UseDockManager = True
    end
    object Panel351: TFlatPanel
      Left = 16
      Top = 190
      Width = 65
      Height = 18
      Caption = '기본계약'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 5
      UseDockManager = True
    end
    object Panel352: TFlatPanel
      Left = 16
      Top = 207
      Width = 65
      Height = 18
      Caption = '설정'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 6
      UseDockManager = True
    end
    object Edit311: TFlatNumber
      Left = 83
      Top = 30
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 21
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit321: TFlatNumber
      Left = 83
      Top = 70
      Width = 134
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 22
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit331: TFlatNumber
      Left = 83
      Top = 110
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 23
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit341: TFlatNumber
      Left = 83
      Top = 150
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 24
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel332: TFlatPanel
      Left = 144
      Top = 110
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 40
      UseDockManager = True
      object RadioButton331: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton332: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel342: TFlatPanel
      Left = 144
      Top = 150
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 41
      UseDockManager = True
      object RadioButton341: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton342: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel353: TFlatPanel
      Left = 83
      Top = 190
      Width = 134
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 42
      UseDockManager = True
      object RadioButton351: TRadioButton
        Left = 8
        Top = 9
        Width = 49
        Height = 17
        Caption = '시내'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton352: TRadioButton
        Left = 56
        Top = 9
        Width = 74
        Height = 17
        Caption = '시내+지방'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Edit411: TFlatNumber
      Left = 299
      Top = 70
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 25
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit412: TFlatNumber
      Left = 299
      Top = 87
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 26
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit421: TFlatNumber
      Left = 299
      Top = 110
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 27
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit422: TFlatNumber
      Left = 299
      Top = 127
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 28
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit431: TFlatNumber
      Left = 299
      Top = 150
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 29
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit432: TFlatNumber
      Left = 299
      Top = 167
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 30
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit441: TFlatNumber
      Left = 299
      Top = 190
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 31
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit442: TFlatNumber
      Left = 299
      Top = 207
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 32
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit451: TFlatNumber
      Left = 299
      Top = 30
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 33
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit452: TFlatNumber
      Left = 299
      Top = 47
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 34
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel413: TFlatPanel
      Left = 360
      Top = 70
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 43
      UseDockManager = True
      object RadioButton411: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton412: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel423: TFlatPanel
      Left = 360
      Top = 110
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 44
      UseDockManager = True
      object RadioButton421: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton422: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel433: TFlatPanel
      Left = 360
      Top = 150
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 45
      UseDockManager = True
      object RadioButton431: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton432: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel443: TFlatPanel
      Left = 360
      Top = 190
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 46
      UseDockManager = True
      object RadioButton441: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton442: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel453: TFlatPanel
      Left = 360
      Top = 30
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 47
      UseDockManager = True
      object RadioButton451: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton452: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel302: TFlatPanel
      Left = 232
      Top = 3
      Width = 201
      Height = 22
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = 16744448
      ColorHighLight = 16744448
      ColorShadow = 16744448
      TabOrder = 54
      UseDockManager = True
      object Label302: TmyLabel3d
        Left = 32
        Top = 3
        Width = 132
        Height = 16
        Caption = '물 류 계 약 내 용'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -16
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object Panel411: TFlatPanel
      Left = 232
      Top = 70
      Width = 65
      Height = 18
      Caption = '②입출고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 7
      UseDockManager = True
    end
    object Panel412: TFlatPanel
      Left = 232
      Top = 87
      Width = 65
      Height = 18
      Caption = '월정관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 8
      UseDockManager = True
    end
    object Panel421: TFlatPanel
      Left = 232
      Top = 110
      Width = 65
      Height = 18
      Caption = '③입출고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 9
      UseDockManager = True
    end
    object Panel422: TFlatPanel
      Left = 232
      Top = 127
      Width = 65
      Height = 18
      Caption = '초과관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 10
      UseDockManager = True
    end
    object Panel431: TFlatPanel
      Left = 232
      Top = 150
      Width = 65
      Height = 18
      Caption = '④재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 11
      UseDockManager = True
    end
    object Panel432: TFlatPanel
      Left = 232
      Top = 167
      Width = 65
      Height = 18
      Caption = '기본관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 12
      UseDockManager = True
    end
    object Panel441: TFlatPanel
      Left = 232
      Top = 190
      Width = 65
      Height = 18
      Caption = '⑤재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 13
      UseDockManager = True
    end
    object Panel442: TFlatPanel
      Left = 232
      Top = 207
      Width = 65
      Height = 18
      Caption = '초과관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 14
      UseDockManager = True
    end
    object Panel451: TFlatPanel
      Left = 232
      Top = 30
      Width = 65
      Height = 18
      Caption = '①정품재고'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 15
      UseDockManager = True
    end
    object Panel452: TFlatPanel
      Left = 232
      Top = 47
      Width = 65
      Height = 18
      Caption = '월보관비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 16
      UseDockManager = True
    end
    object Panel613: TFlatPanel
      Left = 144
      Top = 230
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 55
      UseDockManager = True
      object RadioButton611: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton612: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Edit611: TFlatNumber
      Left = 83
      Top = 230
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 56
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel612: TFlatPanel
      Left = 16
      Top = 230
      Width = 65
      Height = 18
      Caption = '⑤도서종당'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 57
      UseDockManager = True
    end
    object Edit612: TFlatNumber
      Left = 83
      Top = 247
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 58
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit621: TFlatNumber
      Left = 731
      Top = 70
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 61
      Text = '0'
      Visible = False
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit622: TFlatNumber
      Left = 731
      Top = 70
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 62
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Panel623: TFlatPanel
      Left = 792
      Top = 70
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 63
      UseDockManager = True
      object RadioButton621: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton622: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Panel621: TFlatPanel
      Left = 664
      Top = 70
      Width = 65
      Height = 18
      Caption = '②전산프로'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 59
      UseDockManager = True
    end
    object Panel622: TFlatPanel
      Left = 664
      Top = 87
      Width = 65
      Height = 18
      Caption = '그램관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 60
      UseDockManager = True
    end
    object FlatPanel1: TFlatPanel
      Left = 664
      Top = 3
      Width = 201
      Height = 22
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = clYellow
      ColorHighLight = clYellow
      ColorShadow = clYellow
      TabOrder = 64
      UseDockManager = True
      object Label304: TmyLabel3d
        Left = 32
        Top = 3
        Width = 132
        Height = 16
        Caption = '기 타 관 련 내 용'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -16
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object FlatPanel2: TFlatPanel
      Left = 448
      Top = 3
      Width = 201
      Height = 22
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      Color = 4227327
      ColorHighLight = 4227327
      ColorShadow = 4227327
      TabOrder = 65
      UseDockManager = True
      object Label303: TmyLabel3d
        Left = 32
        Top = 3
        Width = 132
        Height = 16
        Caption = '반 품 계 약 내 용'
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -16
        Font.Name = '굴림'
        Font.Style = [fsBold]
        ParentColor = False
        ParentFont = False
        Transparent = True
        AStyle3D = Resit3d
        AShadeLTSet = False
      end
    end
    object Edit561: TFlatNumber
      Left = 515
      Top = 70
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 66
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit571: TFlatNumber
      Left = 515
      Top = 150
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 67
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object Edit581: TFlatNumber
      Left = 515
      Top = 190
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -15
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 68
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel11: TFlatPanel
      Left = 576
      Top = 70
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 69
      UseDockManager = True
      object RadioButton561: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton562: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object FlatPanel13: TFlatPanel
      Left = 576
      Top = 150
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 70
      UseDockManager = True
      object RadioButton571: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton572: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object FlatPanel14: TFlatPanel
      Left = 576
      Top = 190
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 71
      UseDockManager = True
      object RadioButton581: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton582: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object FlatPanel3: TFlatPanel
      Left = 448
      Top = 30
      Width = 65
      Height = 18
      Caption = '①월정'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 72
      UseDockManager = True
    end
    object FlatPanel4: TFlatPanel
      Left = 448
      Top = 47
      Width = 65
      Height = 18
      Caption = '관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 73
      UseDockManager = True
    end
    object FlatPanel5: TFlatPanel
      Left = 448
      Top = 70
      Width = 65
      Height = 18
      Caption = '②분류(해체)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 74
      UseDockManager = True
    end
    object FlatPanel6: TFlatPanel
      Left = 448
      Top = 87
      Width = 65
      Height = 18
      Caption = '및 입력비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 75
      UseDockManager = True
    end
    object FlatPanel7: TFlatPanel
      Left = 448
      Top = 110
      Width = 65
      Height = 18
      Caption = '③재고및'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 76
      UseDockManager = True
    end
    object FlatPanel8: TFlatPanel
      Left = 448
      Top = 127
      Width = 65
      Height = 18
      Caption = '비품보관비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 77
      UseDockManager = True
    end
    object FlatPanel9: TFlatPanel
      Left = 448
      Top = 150
      Width = 65
      Height = 18
      Caption = '④시내'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 78
      UseDockManager = True
    end
    object FlatPanel15: TFlatPanel
      Left = 448
      Top = 167
      Width = 65
      Height = 18
      Caption = '수거업무비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 79
      UseDockManager = True
    end
    object FlatPanel16: TFlatPanel
      Left = 448
      Top = 190
      Width = 65
      Height = 18
      Caption = '⑤지방'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 80
      UseDockManager = True
    end
    object FlatPanel17: TFlatPanel
      Left = 448
      Top = 207
      Width = 65
      Height = 18
      Caption = '수거업무비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 81
      UseDockManager = True
    end
    object FlatPanel18: TFlatPanel
      Left = 448
      Top = 230
      Width = 65
      Height = 18
      Caption = '⑥적재공간'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 82
      UseDockManager = True
    end
    object FlatPanel19: TFlatPanel
      Left = 448
      Top = 247
      Width = 65
      Height = 18
      Caption = '운영비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 83
      UseDockManager = True
    end
    object Edit591: TFlatNumber
      Left = 515
      Top = 230
      Width = 61
      Height = 18
      Digits = 1
      Max = 99.9
      FormatStr = '%2.1n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 4
      ParentFont = False
      TabOrder = 84
      Text = '0.0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel20: TFlatPanel
      Left = 576
      Top = 230
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 85
      UseDockManager = True
      object RadioButton591: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton592: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object FlatPanel21: TFlatPanel
      Left = 16
      Top = 167
      Width = 65
      Height = 18
      Caption = '직송비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 86
      UseDockManager = True
    end
    object FlatPanel10: TFlatPanel
      Left = 232
      Top = 230
      Width = 65
      Height = 18
      Caption = '⑨기타'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 87
      UseDockManager = True
    end
    object FlatPanel12: TFlatPanel
      Left = 232
      Top = 247
      Width = 65
      Height = 18
      Caption = '관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 88
      UseDockManager = True
    end
    object Edit491: TFlatNumber
      Left = 299
      Top = 230
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 89
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel22: TFlatPanel
      Left = 360
      Top = 230
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 90
      UseDockManager = True
      object RadioButton491: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton492: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object FlatPanel23: TFlatPanel
      Left = 16
      Top = 247
      Width = 65
      Height = 18
      Caption = '관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      Alignment = taLeftJustify
      TabOrder = 91
      UseDockManager = True
    end
    object FlatPanel24: TFlatPanel
      Left = 664
      Top = 190
      Width = 65
      Height = 18
      Caption = '⑨기타'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clOlive
      Alignment = taLeftJustify
      TabOrder = 92
      UseDockManager = True
    end
    object FlatPanel25: TFlatPanel
      Left = 664
      Top = 207
      Width = 65
      Height = 18
      Caption = '관리비'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      ColorShadow = clOlive
      Alignment = taLeftJustify
      TabOrder = 93
      UseDockManager = True
    end
    object Edit481: TFlatNumber
      Left = 731
      Top = 190
      Width = 61
      Height = 35
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = clWhite
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 94
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel26: TFlatPanel
      Left = 792
      Top = 190
      Width = 73
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      ColorHighLight = clInfoBk
      TabOrder = 95
      UseDockManager = True
      object RadioButton481: TRadioButton
        Left = 8
        Top = 1
        Width = 57
        Height = 17
        Caption = '청   구'
        TabOrder = 0
        OnClick = RadioButtonClick
      end
      object RadioButton482: TRadioButton
        Left = 8
        Top = 17
        Width = 57
        Height = 17
        Caption = '미청구'
        TabOrder = 1
        OnClick = RadioButtonClick
      end
    end
    object Button302: TFlatButton
      Left = 770
      Top = 232
      Width = 95
      Height = 33
      Color = clAqua
      Caption = '메모장'
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000120B0000120B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333000000
        000033333377777777773333330FFFFFFFF03FF3FF7FF33F3FF700300000FF0F
        00F077F777773F737737E00BFBFB0FFFFFF07773333F7F3333F7E0BFBF000FFF
        F0F077F3337773F3F737E0FBFBFBF0F00FF077F3333FF7F77F37E0BFBF00000B
        0FF077F3337777737337E0FBFBFBFBF0FFF077F33FFFFFF73337E0BF0000000F
        FFF077FF777777733FF7000BFB00B0FF00F07773FF77373377373330000B0FFF
        FFF03337777373333FF7333330B0FFFF00003333373733FF777733330B0FF00F
        0FF03333737F37737F373330B00FFFFF0F033337F77F33337F733309030FFFFF
        00333377737FFFFF773333303300000003333337337777777333}
      Layout = blGlyphLeft
      NumGlyphs = 2
      ParentColor = False
      TabOrder = 96
      OnClick = Button302Click
    end
    object Button301: TFlatButton
      Left = 666
      Top = 232
      Width = 95
      Height = 33
      Color = clAqua
      Caption = '수정/저장'
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000120B0000120B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333000000
        000033333377777777773333330FFFFFFFF03FF3FF7FF33F3FF700300000FF0F
        00F077F777773F737737E00BFBFB0FFFFFF07773333F7F3333F7E0BFBF000FFF
        F0F077F3337773F3F737E0FBFBFBF0F00FF077F3333FF7F77F37E0BFBF00000B
        0FF077F3337777737337E0FBFBFBFBF0FFF077F33FFFFFF73337E0BF0000000F
        FFF077FF777777733FF7000BFB00B0FF00F07773FF77373377373330000B0FFF
        FFF03337777373333FF7333330B0FFFF00003333373733FF777733330B0FF00F
        0FF03333737F37737F373330B00FFFFF0F033337F77F33337F733309030FFFFF
        00333377737FFFFF773333303300000003333337337777777333}
      Layout = blGlyphLeft
      NumGlyphs = 2
      ParentColor = False
      TabOrder = 97
      OnClick = Button301Click
    end
    object Edit592: TFlatNumber
      Left = 515
      Top = 247
      Width = 61
      Height = 18
      Digits = 0
      Max = 99999999.000064
      FormatStr = '%8.0n'
      ColorFlat = 8454143
      ImeName = '한국어(한글) (MS-IME98)'
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clWindowText
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      MaxLength = 8
      ParentFont = False
      TabOrder = 98
      Text = '0'
      OnKeyDown = Edit111KeyDown
      OnKeyPress = Edit111KeyPress
    end
    object FlatPanel28: TFlatPanel
      Left = 664
      Top = 190
      Width = 201
      Height = 35
      Font.Charset = HANGEUL_CHARSET
      Font.Color = clBlack
      Font.Height = -12
      Font.Name = '굴림'
      Font.Style = []
      ParentColor = True
      Visible = False
      Alignment = taLeftJustify
      TabOrder = 99
      UseDockManager = True
      object Label901: TmyLabel3d
        Left = 9
        Top = 12
        Width = 40
        Height = 12
        Caption = '시작일:'
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
      object Label902: TmyLabel3d
        Left = 113
        Top = 12
        Width = 40
        Height = 12
        Caption = '종료일:'
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
      object Label903: TmyLabel3d
        Left = 95
        Top = 10
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
      object Edit901: TFlatComboBox
        Left = 52
        Top = 8
        Width = 37
        Height = 20
        Color = clWindow
        DropDownCount = 9
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -12
        Font.Name = '굴림'
        Font.Style = []
        ItemHeight = 12
        MaxLength = 2
        ParentFont = False
        TabOrder = 0
        ItemIndex = -1
        OnKeyDown = Edit115KeyDown
        OnKeyPress = Edit115KeyPress
      end
      object Edit902: TFlatComboBox
        Left = 156
        Top = 8
        Width = 37
        Height = 19
        Color = clWindow
        DropDownCount = 9
        Font.Charset = HANGEUL_CHARSET
        Font.Color = clBlack
        Font.Height = -11
        Font.Name = '굴림'
        Font.Style = []
        ItemHeight = 11
        MaxLength = 2
        ParentFont = False
        TabOrder = 1
        ItemIndex = -1
        OnKeyDown = Edit115KeyDown
        OnKeyPress = Edit115KeyPress
      end
    end
  end
  object DataSource1: TDataSource
    DataSet = Base10.T1_Sub71
    OnDataChange = DataSource1DataChange
    Left = 42
    Top = 126
  end
  object DataSource2: TDataSource
    DataSet = Base10.T1_Sub72
    OnDataChange = DataSource2DataChange
    Left = 74
    Top = 126
  end
  object ToolbarImages: TImageList
    Left = 42
    Top = 94
    Bitmap = {
      494C01010B000E00040010001000FFFFFFFFFF10FFFFFFFFFFFFFFFF424D3600
      0000000000003600000028000000400000004000000001002000000000000040
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000008400000084000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000840000000000000000000000840000000000000000000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000840000000000000000000000840000000000000084000000000000000000
      0000840000000000000000000000000000007F7F7F0000000000000000000000
      0000000000007F7F7F0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000FFFF0000FFFF0000FFFF00000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000840000000000000000000000840000000000000084000000000000000000
      0000840000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000848484008484840084848400000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000840000000000000000000000000000000000000000000000000000000000
      0000000000008400000084000000840000000000000084000000000000000000
      0000840000000000000000000000000000000000000000000000000000000000
      00007F7F7F000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000840000008400
      0000840000008400000084000000000000000000000000000000000000000000
      0000840000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000840000000000000084000000840000008400
      000000000000000000000000000000000000000000007F7F7F00000000000000
      00007F7F7F000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000840000008400
      0000840000008400000000000000000000000000000000000000000000000000
      0000000000008400000000000000000000000000000000000000000000000000
      0000000000000000000000000000840000000000000084000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000840000008400
      0000840000000000000000000000000000000000000000000000000000000000
      0000000000008400000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000007F7F
      7F00000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      0000000000000000000000000000000000000000000000000000840000008400
      0000000000008400000000000000000000000000000000000000000000000000
      0000000000008400000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF000000000000000000000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000840000000000
      0000000000000000000084000000840000000000000000000000000000000000
      0000840000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      FF007F7F7F000000000000000000000000000000000000000000000000007F7F
      7F000000FF000000000000000000000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000008400000084000000840000008400
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      FF000000FF000000FF00000000000000000000000000000000000000FF000000
      FF000000FF000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF000000000000000000000000000000000000000000FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      FF000000FF000000000000000000000000000000000000000000000000000000
      FF000000FF000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      FF00000000000000FF007F7F7F0000000000000000007F7F7F000000FF000000
      00000000FF000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000FF000000FF000000FF000000FF00000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000424D3E000000000000003E000000
      2800000040000000400000000100010000000000000200000000000000000000
      000000000000000000000000FFFFFF0000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000FFFFFFFFFFFF0000FFFFFFFFFFFF0000
      FFFFFFFF8FFF0000C007C0078C030000FFFFFFFF8FFF0000F83FF807FFFF0000
      FFFFFFFFFFFF0000C007C0078FFF0000FFFFFFFF8C030000F01FF8078FFF0000
      FFFFFFFFFFFF0000C007C007FFFF0000FFFFFFFF8FFF0000F83FF8078C030000
      FFFFFFFF8FFF0000FFFFFFFFFFFF0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
      FFFFFFFFE00FFFFFFFFFFFFFFFFFC007F00F81FFF83FFFFFF8C7E3FFF39FC03F
      F8C7F1FFF39FFFFFF8C7F8FFF39FC007F80FFC7FF39FFFFFF8C7FE3FF39FC03F
      F8C7FF1FF39FFFFFF8C7FF8FF39FC007F00FFF03E10FFFFFFFFFFFFFFFFFC03F
      FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC007FFFFF9FF
      2020BFEBFFFFF6CF72710005FFFFF6B703037E31FFFFF6B7A7237E35FFF7F8B7
      A7A70006C1F7FE8F87877FEAC3FBFE3FCF8F8014C7FBFF7FCFCFC00ACBFBFE3F
      FFFFE001DCF7FEBFE7E7E007FF0FFC9FE3C7F007FFFFFDDFE7E7F003FFFFFDDF
      E997F803FFFFFDDFFC3FFFFFFFFFFFFF00000000000000000000000000000000
      000000000000}
  end
  object FontDialog1: TFontDialog
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -12
    Font.Name = '굴림'
    Font.Style = [fsBold]
    MinFontSize = 0
    MaxFontSize = 0
    Left = 74
    Top = 94
  end
  object Query0: TZMySqlQuery
    Database = Base10.Database
    Transaction = Base10.Transact
    CachedUpdates = False
    ShowRecordTypes = [ztModified, ztInserted, ztUnmodified]
    Options = [doHourGlass, doAutoFillDefs, doUseRowId]
    LinkOptions = [loAlwaysResync]
    Constraints = <>
    ExtraOptions = [moStoreResult]
    Macros = <>
    RequestLive = False
    Left = 74
    Top = 62
  end
end
