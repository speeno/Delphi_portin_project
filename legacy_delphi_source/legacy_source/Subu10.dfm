object Sobo10: TSobo10
  Left = 200
  Top = 120
  BorderIcons = [biSystemMenu]
  BorderStyle = bsSingle
  Caption = '로그인'
  ClientHeight = 160
  ClientWidth = 284
  Color = clBtnFace
  Font.Charset = ANSI_CHARSET
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
  object myLabel3d1: TmyLabel3d
    Left = 58
    Top = 16
    Width = 51
    Height = 16
    Alignment = taRightJustify
    Caption = '사용자'
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = '굴림'
    Font.Style = [fsBold]
    ParentColor = False
    ParentFont = False
    Transparent = True
    AShadeLTSet = False
  end
  object myLabel3d2: TmyLabel3d
    Left = 58
    Top = 48
    Width = 51
    Height = 16
    Alignment = taRightJustify
    Caption = '아이디'
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = '굴림'
    Font.Style = [fsBold]
    ParentColor = False
    ParentFont = False
    Transparent = True
    AShadeLTSet = False
  end
  object myLabel3d3: TmyLabel3d
    Left = 41
    Top = 80
    Width = 68
    Height = 16
    Alignment = taRightJustify
    Caption = '비밀번호'
    Font.Charset = ANSI_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = '굴림'
    Font.Style = [fsBold]
    ParentColor = False
    ParentFont = False
    Transparent = True
    AShadeLTSet = False
  end
  object Edit100: TFlatComboBox
    Left = 120
    Top = 12
    Width = 121
    Height = 23
    Color = clWindow
    DropDownCount = 9
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clBlack
    Font.Height = -15
    Font.Name = '굴림'
    Font.Style = [fsBold]
    ItemHeight = 15
    ParentFont = False
    TabOrder = 1
    ItemIndex = -1
  end
  object Edit101: TFlatEdit
    Left = 120
    Top = 44
    Width = 121
    Height = 21
    ColorFlat = clWhite
    ImeName = '한국어(한글) (MS-IME98)'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clBlack
    Font.Height = -15
    Font.Name = '굴림'
    Font.Style = [fsBold]
    ParentFont = False
    TabOrder = 2
  end
  object Edit102: TFlatEdit
    Left = 120
    Top = 76
    Width = 121
    Height = 22
    ColorFlat = clWhite
    ImeName = '한국어(한글) (MS-IME98)'
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clBlack
    Font.Height = -16
    Font.Name = '굴림'
    Font.Style = [fsBold]
    ParentFont = False
    PasswordChar = '*'
    TabOrder = 0
    OnKeyPress = Edit102KeyPress
  end
  object Button101: TFlatButton
    Left = 40
    Top = 112
    Width = 89
    Height = 25
    Caption = '확인'
    Glyph.Data = {
      06020000424D0602000000000000760000002800000028000000140000000100
      0400000000009001000000000000000000001000000000000000000000000000
      80000080000000808000800000008000800080800000C0C0C000808080000000
      FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333333333
      33333333333333333333333333333333333333333333333333333333FFFFFFF3
      33333333333388888883333333333338888888F3333333333334444444833333
      33333338F33338F3333333333334EFEFE483333333333338F33338F333333333
      3334FEFEF483333333333338F33338F3333333333334EFEFE483333333333338
      F33338F3333333333334FEFEF483333333333338FFFFF8F3333333333334EFEF
      E4333333333333388888883333333333333444444433333333333333338FF333
      333333333333330333333333333333333888FF33333333333333300033333333
      3333333388888333333333333333000003333333333333333333333333333333
      33333333333333333333333333F3333333333333333333333333333333333333
      3833333333333333333330333333333333333333F33333333333333333333333
      3333333333F33F38333333333333333333303333333333333833833333333333
      3333303303333333333333333333333333333333333333333333333333333333
      33333333333333333333}
    Layout = blGlyphLeft
    NumGlyphs = 2
    TabOrder = 3
    OnClick = Button101Click
  end
  object Button102: TFlatButton
    Left = 152
    Top = 112
    Width = 89
    Height = 25
    Caption = '종료'
    Glyph.Data = {
      06020000424D0602000000000000760000002800000028000000140000000100
      0400000000009001000000000000000000001000000000000000000000000000
      80000080000000808000800000008000800080800000C0C0C000808080000000
      FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF00333333333333
      33333333333333333333333333333333333333333333333333333333FFFFFFF3
      33333333333388888883333333333338888888F3333333333334444444833333
      33333338F33338F3333333333334EFEFE483333333333338F33338F333333333
      3334FEFEF483333333333338F33338F3333333333334EFEFE483333333333338
      F33338F3333333333334FEFEF483333333333338FFFFF8F3333333333334EFEF
      E4333333333333388888883333333333333444444433333333333333338FF333
      333333333333330333333333333333333888FF33333333333333300033333333
      3333333388888333333333333333000003333333333333333333333333333333
      33333333333333333333333333F3333333333333333333333333333333333333
      3833333333333333333330333333333333333333F33333333333333333333333
      3333333333F33F38333333333333333333303333333333333833833333333333
      3333303303333333333333333333333333333333333333333333333333333333
      33333333333333333333}
    Layout = blGlyphLeft
    NumGlyphs = 2
    TabOrder = 4
    ModalResult = 7
    OnClick = Button201Click
  end
end
