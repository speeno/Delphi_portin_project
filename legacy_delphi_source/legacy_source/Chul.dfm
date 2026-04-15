object Subu00: TSubu00
  Left = 2248
  Top = 211
  Width = 780
  Height = 480
  BorderIcons = [biSystemMenu, biMinimize]
  Caption = '도서물류관리프로그램'
  Color = clBtnFace
  Font.Charset = HANGEUL_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = '굴림'
  Font.Style = [fsBold]
  FormStyle = fsMDIForm
  Menu = MainMenu1
  OldCreateOrder = False
  Scaled = False
  WindowState = wsMaximized
  OnClose = FormClose
  OnShow = FormShow
  PixelsPerInch = 96
  TextHeight = 12
  object ToolBar: TToolBar
    Left = 0
    Top = 0
    Width = 1353
    Height = 41
    Align = alNone
    BorderWidth = 1
    ButtonHeight = 35
    ButtonWidth = 53
    EdgeBorders = [ebLeft, ebTop, ebRight, ebBottom]
    EdgeOuter = esNone
    Flat = True
    Font.Charset = HANGEUL_CHARSET
    Font.Color = clWindowText
    Font.Height = -11
    Font.Name = '휴먼모음T'
    Font.Style = []
    Images = ToolbarImages1
    Indent = 3
    ParentFont = False
    ParentShowHint = False
    ShowCaptions = True
    ShowHint = True
    TabOrder = 0
    Wrapable = False
    object ToolButton01: TToolButton
      Left = 3
      Top = 0
      AutoSize = True
      Caption = '자료찾기'
      ImageIndex = 0
      OnClick = ToolButton01Click
    end
    object ToolButton02: TToolButton
      Left = 50
      Top = 0
      AutoSize = True
      Caption = '자료검색'
      ImageIndex = 1
      OnClick = ToolButton02Click
    end
    object ToolButton03: TToolButton
      Left = 97
      Top = 0
      AutoSize = True
      Caption = '자료정렬'
      ImageIndex = 2
      OnClick = ToolButton03Click
    end
    object ToolButton91: TToolButton
      Left = 144
      Top = 0
      Width = 8
      ImageIndex = 0
      Style = tbsSeparator
    end
    object ToolButton04: TToolButton
      Left = 152
      Top = 0
      AutoSize = True
      Caption = '자료변환'
      ImageIndex = 3
      OnClick = ToolButton04Click
    end
    object ToolButton05: TToolButton
      Left = 199
      Top = 0
      AutoSize = True
      Caption = '자료교체'
      ImageIndex = 4
      OnClick = ToolButton05Click
    end
    object ToolButton92: TToolButton
      Left = 246
      Top = 0
      Width = 8
      ImageIndex = 0
      Style = tbsSeparator
    end
    object ToolButton06: TToolButton
      Left = 254
      Top = 0
      AutoSize = True
      Caption = '내용전체'
      ImageIndex = 5
      OnClick = ToolButton06Click
    end
    object ToolButton07: TToolButton
      Left = 301
      Top = 0
      AutoSize = True
      Caption = '내용각각'
      ImageIndex = 6
      OnClick = ToolButton07Click
    end
    object ToolButton93: TToolButton
      Left = 348
      Top = 0
      Width = 8
      ImageIndex = 0
      Style = tbsSeparator
    end
    object ToolButton08: TToolButton
      Left = 356
      Top = 0
      AutoSize = True
      Caption = '상단조정'
      ImageIndex = 7
      OnClick = ToolButton08Click
    end
    object ToolButton09: TToolButton
      Left = 403
      Top = 0
      AutoSize = True
      Caption = '하단조정'
      ImageIndex = 8
      OnClick = ToolButton09Click
    end
    object ToolButton94: TToolButton
      Left = 450
      Top = 0
      Width = 8
      ImageIndex = 0
      Style = tbsSeparator
      Visible = False
    end
    object ToolButton10: TToolButton
      Left = 458
      Top = 0
      Caption = '상단HTML'
      ImageIndex = 9
      Visible = False
      OnClick = ToolButton10Click
    end
    object ToolButton11: TToolButton
      Left = 511
      Top = 0
      Caption = '하단HTML'
      ImageIndex = 10
      Visible = False
      OnClick = ToolButton11Click
    end
    object ToolButton95: TToolButton
      Left = 564
      Top = 0
      Width = 8
      Caption = 'ToolButton95'
      ImageIndex = 0
      Style = tbsSeparator
    end
    object ToolButton12: TToolButton
      Left = 572
      Top = 0
      AutoSize = True
      Caption = '상단엑셀'
      ImageIndex = 11
      OnClick = ToolButton12Click
    end
    object ToolButton13: TToolButton
      Left = 619
      Top = 0
      AutoSize = True
      Caption = '하단엑셀'
      ImageIndex = 12
      OnClick = ToolButton13Click
    end
    object ToolButton96: TToolButton
      Left = 666
      Top = 0
      Width = 8
      ImageIndex = 0
      Style = tbsSeparator
    end
    object ToolButton14: TToolButton
      Left = 674
      Top = 0
      AutoSize = True
      Caption = '상단워드'
      ImageIndex = 13
      OnClick = ToolButton14Click
    end
    object ToolButton15: TToolButton
      Left = 721
      Top = 0
      AutoSize = True
      Caption = '하단워드'
      ImageIndex = 14
      OnClick = ToolButton15Click
    end
    object ToolButton97: TToolButton
      Left = 768
      Top = 0
      Width = 8
      ImageIndex = 0
      Style = tbsSeparator
    end
    object ToolButton16: TToolButton
      Tag = 2
      Left = 776
      Top = 0
      AutoSize = True
      Caption = '상단출력'
      ImageIndex = 15
      OnClick = ToolButton16Click
    end
    object ToolButton17: TToolButton
      Left = 823
      Top = 0
      AutoSize = True
      Caption = '하단출력'
      ImageIndex = 16
      OnClick = ToolButton17Click
    end
    object ToolButton98: TToolButton
      Left = 870
      Top = 0
      Width = 8
      Caption = 'ToolButton98'
      ImageIndex = 0
      Style = tbsSeparator
    end
    object ToolButton18: TToolButton
      Left = 878
      Top = 0
      AutoSize = True
      Caption = '출력셋팅'
      ImageIndex = 17
      OnClick = ToolButton18Click
    end
    object ToolButton19: TToolButton
      Left = 925
      Top = 0
      AutoSize = True
      Caption = '화면출력'
      ImageIndex = 18
      OnClick = ToolButton19Click
    end
    object ToolButton20: TToolButton
      Left = 972
      Top = 0
      Caption = '프린터셋업'
      ImageIndex = 19
      OnClick = ToolButton20Click
    end
    object ToolButton99: TToolButton
      Left = 1025
      Top = 0
      Width = 8
      Caption = 'ToolButton99'
      ImageIndex = 0
      Style = tbsSeparator
    end
    object ToolButton21: TToolButton
      Left = 1033
      Top = 0
      AutoSize = True
      Caption = '문자폰트'
      ImageIndex = 20
      OnClick = ToolButton21Click
    end
    object ToolButton22: TToolButton
      Left = 1080
      Top = 0
      AutoSize = True
      Caption = '검색이동'
      ImageIndex = 21
      OnClick = ToolButton22Click
    end
    object ToolButton23: TToolButton
      Left = 1127
      Top = 0
      AutoSize = True
      Caption = '컴퓨터IP'
      ImageIndex = 22
      OnClick = ToolButton23Click
    end
    object ToolButton24: TToolButton
      Left = 1175
      Top = 0
      AutoSize = True
      Caption = '특수문자'
      ImageIndex = 23
      OnClick = ToolButton24Click
    end
  end
  object StringGrid1: TStringGrid
    Left = 296
    Top = 49
    Width = 68
    Height = 28
    ColCount = 1
    FixedCols = 0
    RowCount = 1
    FixedRows = 0
    GridLineWidth = 0
    ScrollBars = ssNone
    TabOrder = 1
    Visible = False
    ColWidths = (
      64)
  end
  object StringGrid2: TStringGrid
    Left = 368
    Top = 49
    Width = 68
    Height = 28
    ColCount = 1
    FixedCols = 0
    RowCount = 1
    FixedRows = 0
    GridLineWidth = 0
    ScrollBars = ssNone
    TabOrder = 2
    Visible = False
    ColWidths = (
      64)
  end
  object WebBrowser1: TWebBrowser
    Left = 136
    Top = 80
    Width = 0
    Height = 25
    TabOrder = 3
    OnNewWindow2 = WebBrowser1NewWindow2
    ControlData = {
      4C00000000000000950200000000000000000000000000000000000000000000
      000000004C000000000000000000000001000000E0D057007335CF11AE690800
      2B2E126208000000000000004C0000000114020000000000C000000000000046
      8000000000000000000000000000000000000000000000000000000000000000
      00000000000000000100000000000000000000000000000000000000}
  end
  object MainMenu1: TMainMenu
    AutoHotkeys = maManual
    Left = 8
    Top = 48
    object Menu200: TMenuItem
      Caption = '출고관리'
      object Menu207: TMenuItem
        Caption = '출고접수관리'
        OnClick = Menu207Click
      end
      object Menu206: TMenuItem
        Caption = '출고접수현황'
        OnClick = Menu206Click
      end
      object Menu208: TMenuItem
        Caption = '출고택배관리'
        OnClick = Menu208Click
      end
      object Menu509_2: TMenuItem
        Caption = '출고검증관리'
        GroupIndex = 1
        OnClick = Menu509_2Click
      end
      object Menu509_3: TMenuItem
        Caption = '출고검증관리(개별)'
        GroupIndex = 1
        OnClick = Menu509_3Click
      end
      object Menu291: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu201: TMenuItem
        Caption = '거래명세서'
        GroupIndex = 1
        OnClick = Menu201Click
      end
      object Menu202: TMenuItem
        Caption = '입고명세서'
        GroupIndex = 1
        OnClick = Menu202Click
      end
      object Menu203: TMenuItem
        Caption = '반품명세서'
        GroupIndex = 1
        OnClick = Menu203Click
      end
      object Menu202_0: TMenuItem
        Caption = '신간가입고 관리'
        GroupIndex = 1
        object Menu202_1: TMenuItem
          Caption = '가입고요청서'
          OnClick = Menu202_1Click
        end
        object Menu202_2: TMenuItem
          Caption = '가입고현황'
          OnClick = Menu202_2Click
        end
      end
      object Menu293: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu209: TMenuItem
        Caption = '신간발행'
        GroupIndex = 1
        OnClick = Menu209Click
      end
      object Menu292: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu308: TMenuItem
        Caption = '전송자료받기(FTP)'
        GroupIndex = 1
        OnClick = Menu308Click
      end
    end
    object Menu900: TMenuItem
      Caption = '택배관리'
      object Menu907: TMenuItem
        Caption = '출고접수관리'
        OnClick = Menu907Click
      end
      object Menu906: TMenuItem
        Caption = '출고접수현황'
        OnClick = Menu906Click
      end
      object Menu908: TMenuItem
        Caption = '출고택배관리'
        OnClick = Menu908Click
      end
      object Menu991: TMenuItem
        Caption = '-'
      end
      object Menu901: TMenuItem
        Caption = '기타명세서'
        OnClick = Menu901Click
      end
      object Menu992: TMenuItem
        Caption = '-'
      end
      object Menu909: TMenuItem
        Caption = '출고내역서'
        OnClick = Menu909Click
      end
      object Menu903: TMenuItem
        Caption = '일별 출고내역서'
        OnClick = Menu903Click
      end
    end
    object Menu300: TMenuItem
      Caption = '재고원장'
      object Menu301: TMenuItem
        Caption = '도서별수불원장'
        GroupIndex = 1
        OnClick = Menu301Click
      end
      object Menu303: TMenuItem
        Caption = '기간별재고원장'
        GroupIndex = 1
        OnClick = Menu303Click
      end
      object Menu304_0: TMenuItem
        Caption = '기간별재고(세분)'
        GroupIndex = 1
        object Menu304_2: TMenuItem
          Caption = '기간별재고원장(정품)'
          OnClick = Menu304_2Click
        end
        object Menu304_3: TMenuItem
          Caption = '기간별재고원장(비품)'
          OnClick = Menu304_3Click
        end
        object Menu304_4: TMenuItem
          Caption = '기간별재고원장(폐기)'
          OnClick = Menu304_4Click
        end
      end
      object Menu593: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu302: TMenuItem
        Caption = '기간별평균재고'
        GroupIndex = 1
        OnClick = Menu302Click
      end
      object Menu302_1: TMenuItem
        Caption = '출판사재고현황'
        GroupIndex = 1
        OnClick = Menu302_1Click
      end
      object Menu304_1: TMenuItem
        Caption = '재고 및 재고금액'
        GroupIndex = 1
        OnClick = Menu304_1Click
      end
    end
    object Menu700: TMenuItem
      Caption = '재고관리'
      object Menu502: TMenuItem
        Caption = '정품재고(변경)'
        GroupIndex = 1
        OnClick = Menu502Click
      end
      object Menu501: TMenuItem
        Caption = '반품재고(변경)'
        GroupIndex = 1
        OnClick = Menu501Click
      end
      object Menu393: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu204: TMenuItem
        Caption = '반품재고(정품입고)-재생'
        GroupIndex = 1
        OnClick = Menu204Click
      end
      object Menu205: TMenuItem
        Caption = '반품재고(반품입고)-해체'
        GroupIndex = 1
        OnClick = Menu205Click
      end
      object Menu392: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu304: TMenuItem
        Caption = '정품재고(폐기)'
        GroupIndex = 1
        OnClick = Menu304Click
      end
      object Menu305: TMenuItem
        Caption = '반품재고(폐기)'
        GroupIndex = 1
        OnClick = Menu305Click
      end
      object Menu391: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu359: TMenuItem
        Caption = '폐기재고(파기)'
        GroupIndex = 1
        OnClick = Menu359Click
      end
      object Menu394: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu319: TMenuItem
        Caption = '반품재고입력-자체운영'
        GroupIndex = 1
        OnClick = Menu319Click
      end
      object Menu329: TMenuItem
        Caption = '반품재고현황-자체운영'
        GroupIndex = 1
        OnClick = Menu329Click
      end
    end
    object Menu400: TMenuItem
      Caption = '발송비/입금관리'
      object N1: TMenuItem
        Caption = '발송비관리'
        GroupIndex = 1
        object Menu403: TMenuItem
          Caption = '발송비내역'
          GroupIndex = 1
          OnClick = Menu403Click
        end
        object Menu404: TMenuItem
          Caption = '발송비현황'
          GroupIndex = 1
          OnClick = Menu404Click
        end
      end
      object N2: TMenuItem
        Caption = '반 품 수 거'
        GroupIndex = 1
        object Menu306: TMenuItem
          Caption = '반품수거내역'
          OnClick = Menu306Click
        end
        object Menu307: TMenuItem
          Caption = '반품수거현황'
          OnClick = Menu307Click
        end
      end
      object Menu204_9: TMenuItem
        Caption = '명세서 발송건수'
        GroupIndex = 1
        Visible = False
        OnClick = Menu204_9Click
      end
      object Menu493: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu405: TMenuItem
        Caption = '청구서관리'
        GroupIndex = 1
        OnClick = Menu405Click
      end
      object Menu406: TMenuItem
        Caption = '청구서출력'
        GroupIndex = 1
        OnClick = Menu406Click
      end
      object Menu409: TMenuItem
        Caption = '세금계산서'
        GroupIndex = 1
        OnClick = Menu409Click
      end
      object Menu494: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu308_1: TMenuItem
        Caption = '운임관리-택배'
        GroupIndex = 1
        OnClick = Menu308_1Click
      end
      object Menu405_1: TMenuItem
        Caption = '청구서관리-택배'
        GroupIndex = 1
        OnClick = Menu405_1Click
      end
      object Menu491: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu402_0: TMenuItem
        Caption = '입금관리'
        GroupIndex = 1
        object Menu401: TMenuItem
          Caption = '입금내역'
          GroupIndex = 1
          OnClick = Menu401Click
        end
        object Menu402: TMenuItem
          Caption = '입금현황(1)'
          GroupIndex = 1
          OnClick = Menu402Click
        end
        object Menu402_1: TMenuItem
          Caption = '입금현황(2)'
          GroupIndex = 1
          OnClick = Menu402_1Click
        end
      end
      object Menu407: TMenuItem
        Caption = '청구금액(년월)'
        GroupIndex = 1
        OnClick = Menu407Click
      end
      object Menu492: TMenuItem
        Caption = '-'
        GroupIndex = 1
      end
      object Menu309: TMenuItem
        Caption = '출고내역서'
        GroupIndex = 1
        OnClick = Menu309Click
      end
      object Menu310: TMenuItem
        Caption = '메세지(팝업창)'
        GroupIndex = 1
        OnClick = Menu310Click
      end
    end
    object Menu500: TMenuItem
      Caption = '내역서관리'
      object Menu503: TMenuItem
        Caption = '일별 출고내역서'
        OnClick = Menu503Click
      end
      object Menu504: TMenuItem
        Caption = '일별 입고내역서'
        OnClick = Menu504Click
      end
      object Menu505: TMenuItem
        Caption = '일별 반품내역서'
        OnClick = Menu505Click
      end
      object Menu509_1: TMenuItem
        Caption = '일별 내역서(요약)'
        OnClick = Menu509_1Click
      end
      object Menu591: TMenuItem
        Caption = '-'
      end
      object Menu506: TMenuItem
        Caption = '기간별출고내역서'
        OnClick = Menu506Click
      end
      object Menu507: TMenuItem
        Caption = '기간별입고내역서'
        OnClick = Menu507Click
      end
      object Menu508: TMenuItem
        Caption = '기간별반품내역서'
        OnClick = Menu508Click
      end
      object Menu592: TMenuItem
        Caption = '-'
      end
      object Menu509: TMenuItem
        Caption = '기간별택배내역서'
        OnClick = Menu509Click
      end
    end
    object Menu600: TMenuItem
      Caption = '통계관리'
      object Menu601: TMenuItem
        Caption = '도서별판매'
        OnClick = Menu601Click
      end
      object Menu602: TMenuItem
        Caption = '거래처판매'
        OnClick = Menu602Click
      end
      object Menu691: TMenuItem
        Caption = '-'
      end
      object Menu607: TMenuItem
        Caption = '도서별년말집계'
        OnClick = Menu607Click
      end
      object Menu608: TMenuItem
        Caption = '거래처년말집계'
        OnClick = Menu608Click
      end
      object Menu692: TMenuItem
        Caption = '-'
      end
      object Menu605: TMenuItem
        Caption = '출판사별판매(1)'
        OnClick = Menu605Click
      end
      object Menu606: TMenuItem
        Caption = '출판사별판매(2)'
        OnClick = Menu606Click
      end
      object Menu693: TMenuItem
        Caption = '-'
      end
      object Menu603: TMenuItem
        Caption = '출판사월별집계(1)'
        OnClick = Menu603Click
      end
      object Menu604: TMenuItem
        Caption = '출판사월별집계(2)'
        OnClick = Menu604Click
      end
    end
    object Menu800: TMenuItem
      Caption = '반품관리'
      object Menu801: TMenuItem
        Caption = '반품명세서'
        OnClick = Menu801Click
      end
      object Menu891: TMenuItem
        Caption = '-'
      end
      object Menu802: TMenuItem
        Caption = '반품재고원장'
        OnClick = Menu802Click
      end
      object Menu803: TMenuItem
        Caption = '반품재고현황'
        OnClick = Menu803Click
      end
      object Menu892: TMenuItem
        Caption = '-'
      end
      object Menu804: TMenuItem
        Caption = '일자별 반품내역서'
        OnClick = Menu804Click
      end
      object Menu805: TMenuItem
        Caption = '기간별 반품내역서'
        OnClick = Menu805Click
      end
    end
    object Menu100: TMenuItem
      Caption = '기초관리'
      object Menu107: TMenuItem
        Caption = '출판사관리'
        OnClick = Menu107Click
      end
      object Menu107_1: TMenuItem
        Caption = '출판사관리-택배'
        OnClick = Menu107_1Click
      end
      object Menu102: TMenuItem
        Caption = '입고처관리'
        OnClick = Menu102Click
      end
      object Menu408: TMenuItem
        Caption = '출판사관리(설정)'
        OnClick = Menu408Click
      end
      object Menu194: TMenuItem
        Caption = '-'
      end
      object Menu101: TMenuItem
        Caption = '거래처관리-통합'
        OnClick = Menu101Click
      end
      object Menu105: TMenuItem
        Caption = '거래처관리-개별'
        OnClick = Menu105Click
      end
      object Menu191: TMenuItem
        Caption = '-'
      end
      object Menu104: TMenuItem
        Caption = '도서관리'
        OnClick = Menu104Click
      end
      object Menu108: TMenuItem
        Caption = '종당관리(도서)'
        OnClick = Menu108Click
      end
      object Menu106: TMenuItem
        Caption = '특별관리'
        OnClick = Menu106Click
      end
      object Menu192: TMenuItem
        Caption = '-'
      end
      object Menu103: TMenuItem
        Caption = '지역분류(시내+지방)'
        OnClick = Menu103Click
      end
      object Menu103_1: TMenuItem
        Caption = '출고증정렬'
        Visible = False
        OnClick = Menu103_1Click
      end
      object Menu110: TMenuItem
        Caption = '환경설정'
        OnClick = Menu110Click
      end
      object Menu193: TMenuItem
        Caption = '-'
      end
      object Menu109: TMenuItem
        Caption = 'E&xit'
        OnClick = Menu109Click
      end
    end
  end
  object PopupMenu1: TPopupMenu
    Left = 40
    Top = 48
    object Menu011: TMenuItem
      Caption = '추가'
      OnClick = Menu011Click
    end
    object Menu012: TMenuItem
      Caption = '등록'
      OnClick = Menu012Click
    end
    object Menu013: TMenuItem
      Caption = '삭제'
      OnClick = Menu013Click
    end
  end
  object OpenDialog1: TOpenDialog
    Filter = 
      'Excel 4.0(*.xls)|*.xls|Excel 5.0(*.xls)|*.xls|Tabbed Text(*.txt)' +
      '|*.txt|Formula One[*.vts]|*.vts'
    Left = 72
    Top = 48
  end
  object SaveDialog1: TSaveDialog
    Filter = 
      'Excel 4.0(*.xls)|*.xls|Excel 5.0(*.xls)|*.xls|Tabbed Text(*.txt)' +
      '|*.txt|Formula One[*.vts]|*.vts'
    Left = 104
    Top = 48
  end
  object PrintDialog1: TPrintDialog
    Options = [poPageNums, poSelection]
    PrintToFile = True
    Left = 136
    Top = 48
  end
  object PrinterSetupDialog1: TPrinterSetupDialog
    Left = 168
    Top = 48
  end
  object ToolbarImages: TImageList
    Left = 200
    Top = 48
    Bitmap = {
      494C010118001D00040010001000FFFFFFFFFF10FFFFFFFFFFFFFFFF424D3600
      0000000000003600000028000000400000008000000001002000000000000080
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000007B7B7B00000000007B7B
      7B0000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000007B7B7B00000000007B7B
      7B0000000000000000000000000000000000FFFFFF000000000000000000FFFF
      FF000000000000000000FFFFFF00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBD
      BD0000000000000000000000000000000000000000007B7B7B00000000007B7B
      7B0000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      000000000000000000007B7B7B00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000C6C6C600C6C6C600000000000000000000000000C6C6C600C6C6C600C6C6
      C600C6C6C6008484840000000000000000000000000000000000000000000000
      0000000000007B7B7B007B7B7B007B7B7B007B7B7B007B7B7B007B7B7B007B7B
      7B0000000000000000000000000000000000000000007B7B7B00000000007B7B
      7B0000000000000000000000000000000000FFFFFF0000000000000000000000
      000000000000FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000000000007B7B7B0000000000000000000000000000000000000000000000
      00007B7B7B000000000000000000000000000000000000000000000000000000
      0000C6C6C600C6C6C600C6C6C60000000000C6C6C600C6C6C600C6C6C600C6C6
      C600C6C6C6008484840000000000000000000000000000000000000000000000
      000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000FFFF00C6C6C600848484000000000084848400C6C6C600C6C6C600C6C6
      C600C6C6C6008484840000000000000000000000000000000000000000000000
      000000000000FFFFFF000000FF00FFFFFF00000000000000000000000000FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000FFFFFF000000000000000000FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000007B7B7B000000000000000000000000000000
      0000000000000000000000000000000000000000000000FFFF00000000000000
      000000FFFF000000000000000000C6C6C6000000000000000000000000000000
      0000C6C6C6008484840000000000000000000000000000000000000000000000
      000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF0000000000FFFFFF00FFFFFF00000000000000000000000000000000000000
      000000000000000000007B7B7B00000000000000000000000000000000007B7B
      7B0000000000000000000000000000000000000000008484840000FFFF008484
      840000FFFF00C6C6C6008484840000FFFF00C6C6C600C6C6C600C6C6C600C6C6
      C600C6C6C6008484840000000000000000000000000000000000000000000000
      000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      00007B7B7B00000000000000000000000000FFFFFF0000000000BDBDBD00FFFF
      FF0000000000FFFFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000000000008484840000FF
      FF0000FFFF008484840000FFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF008484840000000000000000000000000000000000000000000000
      000000000000FFFFFF008400000000000000000000000000000084000000FFFF
      FF000000000000000000000000000000000000000000000000007B7B7B000000
      0000000000007B7B7B000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000FFFF0000FFFF008484
      840000FFFF0000FFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF000000000000000000000000000000000000000000FFFF
      FF000000000000000000000000000000000000000000000000007B7B7B000000
      000000000000000000007B7B7B00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000007B7B7B0000000000000000007B7B7B000000
      0000000000000000000000000000000000000000000000000000848484008484
      840000FFFF0000FFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF000000000000000000000000000000000000000000FFFF
      FF00000000000000000000000000000000000000000000000000000000007B7B
      7B0000000000000000007B7B7B00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000008484840000FFFF000000
      000000FFFF000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF008400000000000000000000000000000084000000FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      00007B7B7B007B7B7B0000000000000000000000000000000000000000007B7B
      7B007B7B7B007B7B7B007B7B7B00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000FFFF00000000000000
      000000FFFF0000000000000000008484840000FFFF0000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000FFFF000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000007B7B
      7B007B7B7B007B7B7B007B7B7B00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00BDBDBD00BDBDBD000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00BDBDBD00BDBDBD000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF007B7B7B007B7B7B007B7B7B00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF0000000000000000000000000000000000C6C6
      C600C6C6C600C6C6C600C6C6C600C6C6C600C6C6C600C6C6C600C6C6C6000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF000000000000000000FFFFFF00000000000000
      0000FFFFFF000000000000000000FFFFFF00000000000000000000000000FFFF
      FF000000000000000000FFFFFF00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000C6C6C60000000000000000000000000000000000FFFFFF00BDBDBD00FFFF
      FF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFF
      FF00BDBDBD00FFFFFF00BDBDBD000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF007B7B7B007B7B7B007B7B7B007B7B7B0000FFFF0000FFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000C6C6C600C6C6
      C600C6C6C600C6C6C600C6C6C6000000FF000000FF000000FF00C6C6C600C6C6
      C600C6C6C60000000000000000000000000000000000BDBDBD00FFFFFF00BDBD
      BD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBD
      BD00FFFFFF000000FF00FFFFFF000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF0000FFFF000000FF0000FFFF00FFFF
      FF0000008400FF000000FF0000000000000000000000FFFFFF00000000000000
      0000FFFFFF000000000000000000FFFFFF00FFFFFF0000000000000000000000
      00000000000000000000FFFFFF00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000C6C6C600C6C6C600000000000000000000000000FFFFFF00BDBDBD00FFFF
      FF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFF
      FF00BDBDBD00FFFFFF00BDBDBD000000000000000000FFFFFF007B7B7B007B7B
      7B007B7B7B00FFFFFF00FFFFFF00FFFFFF0000FFFF000000FF000000FF0000FF
      FF00FF00000000008400FF0000000000000000000000FFFFFF00FFFF0000FFFF
      0000FFFF0000FFFF0000FFFF0000FFFFFF00FFFFFF0000000000FFFFFF000000
      FF00FFFFFF00FF000000FFFFFF00000000000000000000000000C6C6C600C6C6
      C600C6C6C600C6C6C600C6C6C600C6C6C600C6C6C600C6C6C600C6C6C6000000
      000000000000C6C6C60000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF0000FFFF000000FF0000FFFF0000FF
      FF00FF00000000008400FF0000000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF0000000000FFFFFF000000
      FF00FFFFFF00FF000000FFFFFF00000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000C6C6
      C600C6C6C6000000000000000000000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      000000000000000000007B7B7B007B7B7B0000FFFF000000FF000000FF000000
      FF0000FFFF0000000000000000000000000000000000FFFFFF00000000000000
      00000000000000000000FFFFFF00FFFFFF00FFFFFF0000000000FFFFFF00FFFF
      FF00FFFFFF00FF000000FFFFFF00000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      000000000000C6C6C60000000000000000000000000000000000000000000000
      0000FFFFFF0000000000000000000000000000000000FFFFFF0000000000FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      00007B7B7B00000000007B7B7B007B7B7B0000FFFF000000FF000000FF000000
      FF000000FF0000FFFF00000000000000000000000000FFFFFF00000000000000
      00000000000000000000FFFFFF00FFFFFF00FFFFFF0000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000FFFFFF00FF000000FF000000FF000000FF000000FF000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF000000000000000000000000000000000000000000000000007B7B7B007B7B
      7B00000000007B7B7B007B7B7B0000FFFF000000FF000000FF0000FFFF0000FF
      FF000000FF0000FFFF0000FFFF000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF000000000000000000FFFFFF000000000000000000000000000000
      000000000000000000000000000000000000000000007B7B7B00000000007B7B
      7B00000000007B7B7B007B7B7B0000FFFF000000FF0000FFFF007B7B7B000000
      FF0000FFFF000000FF0000FFFF007B7B7B0000000000FF000000FF000000FF00
      0000FF000000FF000000FF000000FF000000FF000000FF000000FF000000FF00
      0000FF000000FF000000FF000000000000000000000000000000000000000000
      000000000000FFFFFF00FF000000FF000000FF000000FF000000FF000000FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF0000000000FFFFFF00FFFFFF000000
      00000000000000000000000000000000000000000000000000007B7B7B000000
      0000000000007B7B7B007B7B7B007B7B7B0000FFFF0000FFFF007B7B7B0000FF
      FF0000FFFF0000FFFF0000FFFF007B7B7B0000000000BDBDBD00BDBDBD00FF00
      0000FF000000FF000000FF000000FF000000FF000000FF000000FF000000FF00
      0000FF000000BDBDBD00BDBDBD00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF0000000000BDBDBD00FFFFFF0000000000FFFFFF00000000000000
      000000000000000000000000000000000000000000007B7B7B00000000000000
      0000000000007B7B7B007B7B7B007B7B7B0000FFFF0000FFFF007B7B7B007B7B
      7B007B7B7B0000FFFF000000FF0000FFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000007B7B7B007B7B7B007B7B7B0000FFFF007B7B7B007B7B
      7B007B7B7B007B7B7B0000FFFF0000FFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000007B7B7B007B7B7B007B7B
      7B0000000000000000007B7B7B0000FFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000006B6B6B006B6B6B006B6B6B006B6B6B006B6B6B006B6B6B006B6B
      6B006B6B6B006B6B6B006B6B6B00000000000000000000000000000000000000
      00006B6B6B006B6B6B006B6B6B006B6B6B006B6B6B006B6B6B006B6B6B006B6B
      6B006B6B6B006B6B6B006B6B6B006B6B6B000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000181018000010180018101800181018001800180000101800181018001810
      18001810180018101800181018006B6B6B000000000000000000000000000000
      0000C6BDC600D6D6D600D6E7D600C6BDC600E7E7E700FFF7FF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF006B6B6B0000000000BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00BDBDBD00BDBDBD00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000039315A006B6BA50018104A0018104A0018104A0029106B0018106B002910
      7B0018216B0029106B00181018006B6B6B000000000000000000000000000000
      0000948C9400949C9400A59CA5007B8C7B00D6BDC600FFFFF700FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF006B6B6B0000000000BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00BDBDBD00BDBDBD000000000000000000BD000000BD000000BD00
      0000BD0000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000B5BD
      B50039215A004A4A6B00393139004A4A4A005A4A5A00948C9400B59CB500B5AD
      B500B5ADB500B5ADB500181018006B6B6B000000000000000000000000000000
      00006B6B6B005A000000180000001800000029000000F7F7F700390000003900
      00003900000039000000FFFFFF006B6B6B000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000BD000000FFFFFF000000
      00008484840000000000000000000000000000000000BDBD000000000000FFFF
      000000000000000000000000000000000000000000000000000000000000C600
      000029213900A59CB5004A1000004A4A4A005A6B5A00947B9400A5ADA500B5AD
      B500B5ADB500B5ADB500181018006B6B6B000000000000000000C60000000000
      0000947B7B00C61000006B6B6B00949C9400B5ADB500E7E7E700FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF006B6B6B0000000000FFFFFF00BDBDBD00FFFF
      FF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFF
      FF00BDBDBD00FFFFFF00BDBDBD000000000000000000BD000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF008484840000000000BDBD000000000000FFFF0000FFFF
      000000000000BD0000000000000000000000000000000000000000000000C600
      000000001800B5100000C60000005A5A5A007B6B7B006B7B7B00A58CA500B5AD
      B500B5ADB500B5ADB500181018006B6B6B000000000000000000C6000000B500
      0000E7ADB50094000000000000002900000029000000D6BDD600290000003900
      00003900000039000000FFFFFF006B6B6B0000000000BDBDBD00FFFFFF00BDBD
      BD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBD
      BD00FFFFFF000000FF00FFFFFF000000000000000000BD000000FFFFFF000000
      0000848484008484840000000000BDBD000000000000FFFF0000FFFF00000000
      0000FFFFFF00BD00000000000000000000000000000000000000C63129004A10
      18007B100000C6000000F7D6D60029101800948C7B007B7B7B00948C9400B5AD
      B500B5ADB500B5ADB500181018006B6B6B0000000000E7BDC600B5000000B54A
      3900C6000000A59C9400B5101800D6D6D600C6BDC600C6D6C600FFF7F700FFFF
      FF00FFFFFF00FFFFFF00FFFFFF006B6B6B0000000000FFFFFF00BDBDBD00FFFF
      FF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFFFF00BDBDBD00FFFF
      FF00BDBDBD00FFFFFF00BDBDBD000000000000000000BD000000FFFFFF00FFFF
      FF00FFFFFF0000000000BDBD000000000000FFFF0000FFFF0000000000000000
      000000000000BD00000000000000000000000000000000000000C60000000000
      0000D6313900A5000000D6BDD6006B101800A59CA500948C9400A59CA500A5AD
      B500B5ADB500B5ADB500181018006B6B6B0000000000C600000000000000E7E7
      F700C600000039000000C6313900D6BDD600E7F7F700F7E7F700F7FFFF00FFFF
      FF003900000039000000FFFFFF006B6B6B000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000BD000000FFFFFF000000
      0000848484000000000000000000FFFF0000FFFF000000000000FFFF0000FFFF
      000000000000BD000000000000000000000000000000E7BDC600C61000000000
      0000C61000007B6BA500B5ADA500C6000000005A0000187B0000006B0000186B
      0000B5ADB500B5ADB500181018006B6B6B0000000000C610000000000000B510
      00005A000000D6E7D6007B6B6B0029000000188C0000008C0000187B00000010
      5A00FFFFFF00FFFFFF00FFFFFF006B6B6B000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF000000000000000000000000000000000000000000BD000000FFFFFF00FFFF
      FF00FFFFFF0000000000FFFF0000FFFF000000000000FFFFFF0000000000FFFF
      000000000000BD000000000000000000000000000000E7BDC600E7ADC600F7D6
      D600F7BDD600C69CC600E7D6E700F7BDC60094AD4A007BBD5A00B5BD7B0018BD
      1800B5ADB500B5ADB500181018006B6B6B000000000000000000000000000000
      0000FFFFFF0039000000FFFFFF00F7D6B500FFD6A500FFADA500FFBDA5000000
      5A003900000039000000FFFFFF006B6B6B000000000000000000000000000000
      0000FFFFFF0000000000000000000000000000000000FFFFFF0000000000FFFF
      FF000000000000000000000000000000000000000000BD000000FFFFFF000000
      00008484840000000000000000000000000000000000FFFFFF00000000000000
      000000000000BD00000000000000000000000000000000000000000000000000
      00004A4A7B00C6ADFF00B5ADB5000000B500FFAD6B00FF9C7B00FFAD6B00FFAD
      7B00B5ADB500B5ADB500181018006B6B6B000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FF9C5A00FF8C6B00FF9C6B00FF8C5A000000
      5A00FFFFFF00FFFFFF00FFFFFF006B6B6B000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF000000000000000000000000000000000000000000BD000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00BD00000000000000000000000000000000000000000000000000
      00004A4A9400B5ADFF00B5ADB5000000A5000000B5000000A5000000B5000000
      A500B5ADB500B5ADB500181018006B6B6B000000000000000000000000000000
      0000FFFFFF0039000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF003900000039000000FFFFFF006B6B6B000000000000000000000000000000
      0000FFFFFF000000000000000000FFFFFF000000000000000000000000000000
      00000000000000000000000000000000000000000000BD000000FFFFFF00BD00
      0000BD000000FFFFFF00BD000000BD000000BD000000FFFFFF00BD000000BD00
      0000FFFFFF00BD00000000000000000000000000000000000000000000000000
      00004A4A7B00C6ADFF00B5ADB500B5ADB500B5ADB500B5ADB500B5ADB500B5AD
      B500B5ADB500B5ADB500181018006B6B6B000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF006B6B6B000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF0000000000FFFFFF00FFFFFF000000
      00000000000000000000000000000000000000000000BD000000BD000000BD00
      0000BD000000BD000000BD000000BD000000BD000000BD000000BD000000BD00
      0000BD000000BD00000000000000000000000000000000000000000000000000
      00004A4A9400B5BDFF00B5ADB500B5ADB500B5ADB500B5ADB500B5ADB500B5AD
      B500B5ADB500B5ADB500181018006B6B6B000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF0000000000FFFFFF0000000000000000000000000000000000000000000000
      0000FFFFFF0000000000BDBDBD00FFFFFF0000000000FFFFFF00000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00004A4A7B00C6ADFF0018106B0029107B0018216B0029106B0018106B002910
      7B0018216B0029106B0018101800000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000F7E7FF00E7E7FF00E7E7F700E7E7E700F7E7F700E7E7E700E7E7F700E7E7
      E700F7E7F700E7E7E70000000000000000000000000000000000000000000000
      00006B6B6B006B6B6B006B6B6B006B6B6B006B6B6B006B6B6B006B6B6B006B6B
      6B006B6B6B000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000008484
      8400848484008484840084848400848484008484840084848400848484008484
      8400848484008484840084848400000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000BDBDBD00BDBDBD007B7B7B007B7B7B007B7B7B00000000000000
      0000000000000000000000000000000000000000000000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000084848400000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000BDBD
      BD00BDBDBD007B7B7B000000000000000000000000007B7B7B007B7B7B007B7B
      7B00000000000000000000000000000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000084848400000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000BDBD
      0000BDBD0000BDBD000000000000000000000000000000000000BDBDBD00BDBD
      BD0000000000FFFFFF0000FF0000FFFFFF0000FF0000FFFFFF00000000007B7B
      7B007B7B7B000000000000000000000000000000000000000000FFFFFF000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF008484840000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000084848400000000000000000000000000848484008484
      84008484840084848400848484008484840000000000FFFF0000000000000000
      0000000000000000000000000000000000000000000000000000BDBDBD000000
      0000FFFFFF000000000000000000000000000000000000000000FFFFFF000000
      00007B7B7B000000000000000000000000000000000000000000FFFFFF000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF008484840000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000084848400000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000FFFF0000FFFF
      0000FFFF000000000000848484000000000000000000BDBDBD007B7B7B00FFFF
      FF00000000000000000000FF000000840000008400000000000000000000FFFF
      FF007B7B7B007B7B7B0000000000000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000FFFFFF000000
      00000000000000000000FFFFFF00000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000008484840000000000000000000000000000000000C6C6
      C600C6C6C600C6C6C60084848400FFFF000000000000FFFF0000FFFF0000FFFF
      00000000000000000000848484000000000000000000BDBDBD000000000000FF
      00000000000000FF00000084000000FF000000840000008400000000000000FF
      0000000000007B7B7B0000000000000000000000000000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      00000000000000000000FFFFFF00000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000084848400000000000000000000000000000000000000
      0000C6C6C60084848400FFFF000000000000FFFF0000FFFF0000FFFF00000000
      0000C6C6C600C6C6C600000000000000000000000000FFFFFF0000000000FFFF
      FF000000000000FF000000FF000000FF000000FF00000084000000000000FFFF
      FF00000000007B7B7B0000000000000000000000000000000000FFFFFF000000
      0000FFFFFF000000000000000000000000000000000000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000FFFFFF000000
      000000000000FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000000000000000000084848400000000000000000000000000000000000000
      000000000000FFFF000000000000FFFF0000FFFF0000FFFF0000000000000000
      00000000000000000000000000000000000000000000FFFFFF000000000000FF
      000000000000FFFFFF0000FF000000FF00000084000000FF00000000000000FF
      000000000000BDBDBD0000000000000000000000000000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      00000000000000000000FFFFFF00000000000000000000000000FFFFFF000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000084848400000000000000000000000000000000000000
      0000FFFF000000000000FFFF0000FFFF0000FFFF000000000000848484000000
      00000000000000000000000000000000000000000000FFFFFF007B7B7B00FFFF
      FF000000000000000000FFFFFF00FFFFFF0000FF00000000000000000000FFFF
      FF007B7B7B00BDBDBD0000000000000000000000000000000000FFFFFF000000
      0000FFFFFF0000000000000000000000000000000000FFFFFF00FFFFFF000000
      00000000000000000000FFFFFF00000000000000000000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF000000000000000000000000000000000000000000FFFF
      000000000000FFFF0000FFFF0000FFFF000000000000C6C6C600000000008484
      8400000000000000000000000000000000000000000000000000BDBDBD000000
      0000FFFFFF000000000000000000000000000000000000000000FFFFFF000000
      0000BDBDBD000000000000000000000000000000000000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000FFFF00000000
      0000FFFF0000FFFF0000FFFF000000000000C6C6C600C6C6C600C6C6C6000000
      0000848484000000000000000000000000000000000000000000FFFFFF00BDBD
      BD0000000000FFFFFF0000FF0000FFFFFF0000FF0000FFFFFF0000000000BDBD
      BD00BDBDBD000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000FF000000FF000000FF000000FF000000FF000000FF000000FF0000000000
      00000000000000000000000000000000000000000000FFFF000000000000FFFF
      0000FFFF0000FFFF0000000000000000000000000000C6C6C600C6C6C600C6C6
      C60000000000848484000000000000000000000000000000000000000000FFFF
      FF00BDBDBD007B7B7B000000000000000000000000007B7B7B00BDBDBD00BDBD
      BD00000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000FFFF0000FFFF
      0000FFFF00000000000000000000000000000000000000000000C6C6C600C6C6
      C600C6C6C6000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF00FFFFFF00FFFFFF00BDBDBD00BDBDBD00000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00000000000000
      0000000000000000000000000000FFFFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00000000000000
      FF000000FF000000FF0000000000FFFFFF000000000000000000000000000000
      FF000000FF000000FF000000FF000000FF000000FF000000FF00000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      FF000000FF000000FF000000FF000000FF000000FF000000FF00000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000BDBDBD00BDBDBD007B7B7B007B7B7B007B7B7B00000000000000
      000000000000000000000000000000000000000000000000000000000000FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00000000000000
      FF000000FF000000FF0000000000FFFFFF0000000000000000000000FF000000
      FF000000FF000000FF000000FF000000FF000000FF000000FF00000000000000
      84000000000000000000000000000000000000000000000000000000FF000000
      FF000000FF000000FF000000FF000000FF000000FF000000FF00000000000000
      840000000000000000000000000000000000000000000000000000000000BDBD
      BD00BDBDBD007B7B7B000000000000000000000000007B7B7B007B7B7B007B7B
      7B00000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00000000000000
      FF000000FF000000FF0000000000FFFFFF000000000000000000000084000000
      8400000084000000840000008400000084000000840000008400000000000000
      8400000084000000000000000000000000000000000000000000000084000000
      8400000084000000840000008400000084000000840000008400000000000000
      8400000084000000000000000000000000000000000000000000BDBDBD00BDBD
      BD0000000000FFFFFF000000FF00FFFFFF000000FF00FFFFFF00000000007B7B
      7B007B7B7B000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00000000000000
      0000000000000000000000000000FFFFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000084000000840000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000084000000840000000000000000000000000000000000BDBDBD000000
      0000FFFFFF000000000000000000000000000000000000000000FFFFFF000000
      00007B7B7B000000000000000000000000000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF0000000000000000007B7B7B000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF0000000000FFFF
      FF000000000000008400000084000000000000000000000000007B7B7B000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF0000000000FFFF
      FF000000000000008400000084000000000000000000BDBDBD007B7B7B00FFFF
      FF0000000000000000000000FF0000008400000084000000000000000000FFFF
      FF007B7B7B007B7B7B0000000000000000000000000000000000000000000000
      0000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF0000000000FFFFFF00FFFFFF00FFFFFF000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF0000000000FFFF
      FF00000000000000000000008400000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF0000000000FFFF
      FF00FFFFFF0000000000000084000000000000000000BDBDBD00000000000000
      FF00000000000000FF00000084000000FF000000840000008400000000000000
      FF00000000007B7B7B00000000000000000000000000FFFF0000FFFF0000FFFF
      000000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF000000
      00000000000000000000FFFFFF00FFFFFF000000000000000000000000000000
      0000FFFFFF00FFFFFF007B7B7B0000000000000000000000000000000000FFFF
      FF0000000000FFFFFF0000000000000000000000000000000000000000000000
      0000FFFFFF00FFFFFF007B7B7B0000000000000000000000000000000000BDBD
      BD00BDBDBD00FFFFFF00000000000000000000000000FFFFFF0000000000FFFF
      FF00000000000000FF000000FF000000FF000000FF000000840000000000FFFF
      FF00000000007B7B7B00000000000000000000000000FFFF0000FFFF0000FFFF
      00000000000000000000000000000000000000000000FFFFFF00000000000000
      0000000000000000000000000000FFFFFF000000000000000000000000000000
      0000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF0000000000FFFFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00FFFFFF00000000000000000000000000FFFFFF00000000000000
      FF0000000000FFFFFF000000FF000000FF00000084000000FF00000000000000
      FF0000000000BDBDBD00000000000000000000000000FFFF0000FFFF0000FFFF
      000000000000FFFF000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF007B7B7B0000000000000000000000
      000000000000FFFFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF00000000000000000000000000FFFFFF007B7B7B00FFFF
      FF000000000000000000FFFFFF00FFFFFF000000FF000000000000000000FFFF
      FF007B7B7B00BDBDBD0000000000000000000000000000000000000000000000
      000000000000FFFF000000000000000000000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF000000000000000000000000000000
      00000000000000000000000000000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF0000000000000000000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF0000000000FFFFFF0000000000000000000000000000000000BDBDBD000000
      0000FFFFFF000000000000000000000000000000000000000000FFFFFF000000
      0000BDBDBD00000000000000000000000000000000000000000000000000FFFF
      0000FFFF0000FFFF000000000000FFFF00000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF000000000000000000000000000000
      000000000000000000000000000000000000FFFFFF00FFFFFF007B7B7B000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000FFFFFF00000000000000000000000000FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000FFFFFF00BDBD
      BD0000000000FFFFFF000000FF00FFFFFF000000FF00FFFFFF0000000000BDBD
      BD00BDBDBD000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000FFFF00000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF0000000000000000000000000000000000000000000000000000000000FFFF
      FF00BDBDBD007B7B7B000000000000000000000000007B7B7B00BDBDBD00BDBD
      BD00000000000000000000000000000000000000000000000000000000000000
      000000000000FFFF0000FFFF0000FFFF00000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF007B7B7B0000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000FFFFFF00FFFFFF00FFFFFF00BDBDBD00BDBDBD00000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000FFFFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000FFFFFF00FFFFFF000000
      0000000000000000000000000000000000000000000000000000FFFFFF000000
      00000000000000000000000000000000000000000000BDBDBD00BDBDBD00BDBD
      BD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBDBD00BDBD
      BD00BDBDBD000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000000000000000000000FF
      FF0000FFFF0000FFFF00000000000000000000000000FFFFFF00FFFFFF00FFFF
      FF0000000000FF000000FF000000FF00000000000000FFFFFF00FFFFFF000000
      00000000FF000000FF000000FF000000000000000000BDBDBD00000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000BDBDBD00BDBDBD000000000000000000000000000000000000FFFF00BDBD
      BD0000FFFF00BDBDBD0000FFFF00BDBDBD0000FFFF00BDBDBD0000FFFF000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000FFFF0000FFFF0000FFFF000000000000000000000000
      00007B7B7B007B7B7B007B7B7B00000000000000000000000000FFFFFF00FFFF
      FF00FFFFFF0000000000FF00000000000000FFFFFF00FFFFFF00FFFFFF000000
      00000000FF000000FF000000FF00000000000000000000000000BDBDBD000000
      0000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00000000000000
      000000000000BDBDBD00BDBDBD00000000000000000000FFFF000000000000FF
      FF00BDBDBD0000FFFF00BDBDBD0000FFFF00BDBDBD0000FFFF00BDBDBD0000FF
      FF0000000000FFFFFF00FFFFFF0000000000000000000000FF000000FF000000
      FF00000000007B7B7B007B7B7B007B7B7B007B7B7B007B7B7B007B7B7B007B7B
      7B007B7B7B0000000000FFFFFF0000000000000000000000000000000000FFFF
      FF00FFFFFF00FFFFFF0000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      00000000FF000000FF000000FF00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000FFFFFF000000
      0000FFFFFF0000000000BDBDBD000000000000000000FFFFFF0000FFFF000000
      000000FFFF00BDBDBD0000FFFF00BDBDBD0000FFFF00BDBDBD0000FFFF00BDBD
      BD0000FFFF0000000000FFFFFF0000000000000000000000FF000000FF000000
      FF000000FF000000000000000000000000000000000000000000000000000000
      0000FFFFFF0000000000FFFFFF00000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00000000000000000000000000FFFFFF000000
      00000000000000000000000000000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF0000000000FFFF
      FF000000000000000000BDBDBD00000000000000000000FFFF00FFFFFF0000FF
      FF00000000000000000000000000000000000000000000000000000000000000
      00000000000000000000FFFFFF000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      0000FFFFFF0000000000FFFFFF00000000000000000000000000000000000000
      000000000000FFFFFF00000000007B7B7B0000FFFF007B7B7B0000000000FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000000000000000FFFFFF000000
      000000000000FFFFFF000000000000000000FFFFFF00FFFFFF00FFFFFF000000
      0000FFFFFF0000000000BDBDBD000000000000000000FFFFFF0000FFFF00FFFF
      FF0000FFFF00FFFFFF0000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      0000FFFFFF0000000000FFFFFF00000000000000000000000000000000000000
      000000000000000000000000000000FFFF0000FFFF0000FFFF0000000000FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000000000000000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      0000FFFFFF0000000000BDBDBD00000000000000000000FFFF00FFFFFF0000FF
      FF00FFFFFF0000FFFF0000000000FFFFFF000000000000000000000000000000
      00000000000000000000FFFFFF000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      0000FFFFFF0000000000FFFFFF00000000000000000000000000000000000000
      00000000000000000000000000007B7B7B0000FFFF007B7B7B0000000000FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF000000000000000000000000000000000000000000FFFFFF0000FFFF00FFFF
      FF0000FFFF00FFFFFF0000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF000000000000000000FFFFFF007B7B7B007B7B
      7B00FFFFFF007B7B7B007B7B7B00FFFFFF007B7B7B00FFFFFF00FFFFFF000000
      0000FFFFFF0000000000FFFFFF000000000000000000FFFF0000FFFF0000FFFF
      0000000000000000000000000000000000000000000000000000FFFFFF00FFFF
      FF0000000000FFFFFF00FFFFFF00FFFFFF00000000000000FF00000000000000
      0000FFFFFF000000000000000000000000000000000000000000FFFFFF000000
      000000000000000000000000FF00000000000000000000000000FFFFFF0000FF
      FF00FFFFFF0000FFFF0000000000FFFFFF000000000000000000000000000000
      00000000000000000000FFFFFF000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      0000FFFFFF0000000000FFFFFF000000000000000000FFFF0000FFFF0000FFFF
      00000000000000000000000000000000000000000000FFFFFF00FFFFFF000000
      00000000000000000000FFFFFF00FFFFFF00000000000000FF0000000000FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF0000000000000000000000FF0000000000000000007B7B7B00000000000000
      0000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF000000000000000000FFFFFF007B7B7B007B7B
      7B00FFFFFF007B7B7B007B7B7B007B7B7B00FFFFFF00FFFFFF00FFFFFF000000
      0000FFFFFF0000000000FFFFFF000000000000000000FFFF0000FFFF0000FFFF
      000000000000FFFF000000000000000000000000000000000000000000000000
      0000000000000000000000000000FFFFFF00000000000000000000000000FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF0000000000FFFFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000FFFFFF000000000000000000FFFFFF00FFFF
      FF000000000000000000000000000000000000000000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF000000
      0000FFFFFF0000000000FFFFFF00000000000000000000000000000000000000
      000000000000FFFF000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000FFFF
      FF00000000000000000000000000FFFFFF000000000000000000FFFFFF00FFFF
      FF0000000000FFFFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF0000000000FFFFFF0000000000000000000000000000000000FFFFFF000000
      0000FFFFFF0000000000FFFFFF0000000000FFFFFF0000000000FFFFFF000000
      0000FFFFFF00000000000000000000000000000000000000000000000000FFFF
      0000FFFF0000FFFF000000000000FFFF00000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF00000000000000000000000000FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF000000000000000000000000000000000000000000000000007B7B7B000000
      00007B7B7B00000000007B7B7B00000000007B7B7B00000000007B7B7B000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000FFFF00000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF00000000000000000000000000FFFF
      FF00FFFFFF00FFFFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000007B7B7B00000000007B7B7B000000
      00007B7B7B00000000007B7B7B00000000007B7B7B00000000007B7B7B000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000FFFF0000FFFF0000FFFF00000000000000000000000000000000
      00000000000000000000FFFFFF00FFFFFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000FFFFFF00424D3E000000000000003E000000
      2800000040000000800000000100010000000000000400000000000000000000
      000000000000000000000000FFFFFF0000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000FFFFFFFFFFFF8E00FFFFFFFFFFFF0600
      F183FFFFF0072600FBC7E001F0072600F9C7E001F0070600F807E001F0078E00
      FD8FE001F007DE00FC8FA001F007C600FC8F8001F007C201FE1FC001F0078803
      FE1F8001F0079C07FE1FC3FFF007C8E1FF3F97FFF007E040FF7FB67FF007F30C
      FFFFF7FFF007FFC0FFFFFFFFFFFFFFE180018000FFFFFFFF000000000000E00F
      000000000000C007000000000000800300000000000080030000000000008001
      0000000000008001000000000000C001E00700000000E001E007F4030000F003
      E007C8010000F00FE007A8000000F00FE00FD8000000F807E01FB8000000FFFF
      E03FFC00FFFFFFFFE07FFF8CFFFFFFFFFFFFF801F0008001FFFFF000F0000000
      FFE7F000F00000008003E000F00000008005E000C00000008003E000C0000000
      8003C00080000000800BD000A0000000800390008000E00780038000F000E007
      8003F000F000E0078003F000F000E0078003F000F000E00F8003F000F001E01F
      FFFFF001F003E03FFFFFF003F007E07FFFFFFFFF8000FFFFF83F8000A000FFFF
      E00F80009FFCFFC1C0078000901C8001800380009FFC800180038000901C8000
      000180009FFCC000000180009084E0000001800090FCF000000180009084E00F
      000180008002C007800380008000800380038000A00A0101C007800080000381
      E00F8000FFFF07C1F83FFFFFFFFFFFFF8000FFFFFFFFFFFF8000E01FE01FF83F
      C000C00FC00FE00FE00080078007C007F000000300038003F800000100018003
      FC008000800000010600C000C00000010700E000E00000010180F000F0000001
      0180F801F80100010060FC01F8018003C060FE01F8018003C060FF1FF807C007
      F044FFFFF807E00FF07EFFFFFC7FF83F8007FFFFFFE380000003801FFC418000
      000100008800C000801000000000E000000000000000F000000000000000F800
      800000000000FC00800000000000040000000000000006000000800000000180
      00008000000001C00000FC0000000000C001FC010001C060C001FC030001C060
      C007FC07000DF060E3FFFFFFD553F00600000000000000000000000000000000
      000000000000}
  end
  object Ping1: TPing
    Size = 56
    Timeout = 4000
    TTL = 64
    Flags = 0
    OnEchoRequest = Ping1EchoRequest
    OnEchoReply = Ping1EchoReply
    OnDnsLookupDone = Ping1DnsLookupDone
    Left = 232
    Top = 48
  end
  object Timer1: TTimer
    Left = 264
    Top = 48
  end
  object MDIWallpaper1: TMDIWallpaper
    Mode = wpCenter
    CustomX = 0
    CustomY = 0
    Left = 8
    Top = 80
  end
  object ApplicationEvents1: TApplicationEvents
    OnMessage = ApplicationEvents1Message
    Left = 104
    Top = 80
  end
  object PopupMenu2: TPopupMenu
    Left = 40
    Top = 80
    object Menu021: TMenuItem
      Caption = '추가'
      OnClick = Menu021Click
    end
    object Menu022: TMenuItem
      Caption = '등록'
      OnClick = Menu022Click
    end
    object Menu023: TMenuItem
      Caption = '삭제'
      OnClick = Menu023Click
    end
  end
  object ToolbarImages1: TImageList
    Left = 72
    Top = 80
    Bitmap = {
      494C010118001D00040010001000FFFFFFFFFF10FFFFFFFFFFFFFFFF424D3600
      0000000000003600000028000000400000008000000001002000000000000080
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000000000004A4A4A004A4A
      4A004A4A4A004A4A4A004A4A4A004A4A4A004A4A4A004A4A4A004A4A4A004A4A
      4A004A4A4A004A4A4A0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000800000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000048FFFF006BFFFF006BFF
      FF008EFFFF008EFFFF00B1FFFF00B1FFFF00F0FBFF00D4FFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF0000000000000000008000000080000000800000008000
      0000800000008000000080000000800000008000000080000000800000008000
      0000800000008000000080000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000008000
      0000FF000000800000000000000000000000FFFFFF0080808000808080008080
      8000808080008080800080808000808080008080800080808000808080008080
      8000808080008080800080808000000000000000000048FFFF0048FFFF006BFF
      FF006BFFFF008EFFFF008EFFFF00B1FFFF00B1FFFF00F0FBFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF0000000000000000008080000080800000808000008080
      0000808000008080000080800000808000008080000080800000808000008080
      0000808000008080000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000080000000FF00
      000000000000FF0000008000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C00080808000000000000000000025FFFF0048FFFF0048FF
      FF006BFFFF006BFFFF008EFFFF008EFFFF00B1FFFF00B1FFFF00F0FBFF00D4FF
      FF00FFFFFF00FFFFFF0000000000000000008080000080800000808000008080
      0000808000000000000000000000800000008000000080800000808000008080
      0000808000008080000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000080000000FF000000FF00
      0000FF000000FF000000FF00000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C00080808000000000000000000025FFFF0025FFFF004873
      FF002557FF000055FF006BFFFF008EFFFF000031960000257300001950000019
      5000FFFFFF00FFFFFF0000000000000000000000000080800000808000008080
      0000000000000000000080800000808000008080000080000000808000008080
      0000808000000000000000000000000000000000000000000000000000000000
      00000000000080000000800000000000000000000000FF00000000000000FF00
      00000000000000000000FF00000000000000FFFFFF00C0C0C000C0C0C0000000
      0000000000000000000000000000000000000000000000000000000000000000
      000080808000C0C0C00080808000000000000000000000FFFF0025FFFF0025FF
      FF004873FF0048FFFF006BFFFF006BFFFF008EFFFF0000319600002573009E9E
      9E00FFFFFF00D4FFFF0000000000000000000000000080800000808000008000
      0000000000008080000080800000808000008080000080800000800000008080
      0000808000000000000000000000000000000000000000000000000000000000
      000080000000FF000000FF000000800000000000000000000000FF000000FF00
      000000000000FF0000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C0008080800080808000C0C0C000C0C0C0000000000000000000000000008080
      8000C0C0C000C0C0C00080808000000000000000000000FFFF0000FFFF0025FF
      FF0025FFFF004873FF002557FF000055FF000049DC00003DB90000319600B1FF
      FF00B1FFFF00F0FBFF0000000000000000000000000000000000808000008000
      0000800000008080000080800000808000008080000080000000808000008080
      0000000000000000000000000000000000000000000000000000000000008000
      0000FF000000FF00000000000000FF000000800000000000000000000000FF00
      0000FF000000000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C00080808000C0C0C00000000000000000000000000080808000C0C0
      C000C0C0C000C0C0C00080808000000000000000000000DCDC0000FFFF0000FF
      FF0025FFFF006B8FFF0048FFFF0048FFFF000055FF000049DC00B6B6B6008EFF
      FF00B1FFFF00B1FFFF0000000000000000000000000000000000808000008000
      0000800000008080000080800000808000008080000080000000000000008080
      000000000000000000000000000000000000000000000000000000000000FF00
      000000000000FF000000FF00000000000000FF000000FF000000000000000000
      000000000000000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C00000000000000000000000000000000000C0C0C000C0C0
      C000C0C0C000C0C0C00080808000000000000000000000B9B90000DCDC0000FF
      FF0000FFFF0025FFFF00DADADA0048FFFF002557FF000055FF006BFFFF008EFF
      FF008EFFFF00B1FFFF0000000000000000000000000000000000000000008080
      0000800000008080000080800000808000008080000080000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000FF000000FF000000FF000000FF000000FF00000000000000000000000000
      000000000000000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C000000000000000000000000000C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C00080808000000000000000000000B9B90000B9B90000DC
      DC0000FFFF0000FFFF008EABFF006B8FFF004873FF00DADADA006BFFFF006BFF
      FF008EFFFF008EFFFF0000000000000000000000000000000000000000008080
      0000808000008080000080800000808000008080000000000000800000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000FF00000000000000FF0000000000000000000000000000000000
      000000000000000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C00000000000000000000000000000000000C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C0008080800000000000000000000096960000B9B90000B9
      B90000DCDC0000FFFF0000FFFF008EABFF006B8FFF0048FFFF0048FFFF006BFF
      FF006BFFFF008EFFFF0000000000000000000000000000000000000000000000
      0000800000008080000080800000808000000000000080000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000FF000000800000008000000080000000800000008000
      000000000000000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C00080808000000000000000000000000000C0C0C00000000000C0C0C000C0C0
      C000C0C0C000C0C0C000808080000000000000000000009696000096960000B9
      B90000B9B90000DCDC0000FFFF00D4E3FF00F2F2F20025FFFF0048FFFF0048FF
      FF006BFFFF006BFFFF0000000000000000000000000000000000000000000000
      0000808000008000000080000000800000008000000080800000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000080000000FF000000FF000000FF000000FF00
      000000000000000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C00000000000000000000000000080808000C0C0C0008080800000000000C0C0
      C000C0C0C000C0C0C00080808000000000000000000000737300009696000096
      960000B9B90000B9B90000DCDC0000FFFF0000FFFF0025FFFF0025FFFF0048FF
      FF0048FFFF006BFFFF0000000000000000000000000000000000000000000000
      0000000000008080000080800000808000008080000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000080000000FF000000FF00000000000000FF00
      000000000000000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C00080808000000000000000000000505000007373000096
      96000096960000B9B90000B9B90000DCDC0000FFFF0000FFFF0025FFFF000050
      50006BFFFF00FFFFFF0000000000000000000000000000000000000000000000
      0000000000008080000080800000808000008080000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000080000000FF00000000000000FF000000FF00
      000000000000000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C00080808000000000000000000000505000005050000073
      7300009696000096960000B9B90000B9B90000DCDC0000FFFF0000FFFF000050
      50006BFFFF000000000000000000000000000000000000000000000000000000
      0000000000000000000080800000808000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000080000000FF000000FF000000FF000000FF00
      000000000000000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C00080808000000000000000000000505000005050000050
      500000737300009696000096960000B9B90000B9B90000DCDC0000FFFF000050
      5000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000080800000808000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000080808000808080008080
      8000808080008080800000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000058585800A0A0A000A0A0
      A000000000000000000000000000000000006E6E6E004A4A4A004A4A4A004A4A
      4A004A4A4A0062626200CECECE00000000000000000000000000000000000000
      000000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000000000008080800080808000808080008080800080808000808080000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000B0B0B0009090900078787800707070005858
      5800A0A0A000A0A0A000A0A0A000000000009E9E9E00FFFFFF00F2F2F200E6E6
      E600DADADA009E9E9E00CECECE0080808000000000004A4A4A00000000000000
      000000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      000000000000C0C0C000C0C0C000C0C0C000C0C0C00080808000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000090888800C0C0C000B0B0B000B8B8B800C0C0C000A0A0A0007878
      78007070700058585800A0A0A000A0A0A00000000000DADADA00F2F2F200F2F2
      F200F2F2F200DADADA00626262003E3E3E008080800032323200262626000000
      000000000000000000000000000000000000FFFFFF00FFFFFF00000000000000
      0000FFFFFF00FFFFFF00FFFFFF008080800080808000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF0000000000C0C0C00080808000808080008080
      8000808080008080800080808000808080008080800080808000808080008080
      8000808080008080800080808000000000000000000000000000000000000000
      000000000000B8B8B800E8E8E800D0D0D000B8B8B800A0A0A000A0A0A0009090
      90007878780058585800A0A0A000000000000000000000000000000000009292
      92003E3E3E006E6E6E009E9E9E00AAAAAA009E9E9E003E3E3E003E3E3E000E0E
      0E0000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF000000
      000000008000FFFFFF00FFFFFF00FFFFFF00FFFFFF00C0C0C000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF0000000000FFFFFF00C0C0C000C0C0C00000FF
      0000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0
      C0000000000080808000C0C0C00000000000000000000000000000000000F8C8
      A000F8D0A800FFFFFF00E8E8E800FFFFFF00C0C0C000C0C0C000C0C0C0007070
      70007878780070707000A0A0A0000000000000000000808080003E3E3E00AAAA
      AA00C0C0C000E6E6E6009E9E9E00AAAAAA00AAAAAA003E3E3E003E3E3E004A4A
      4A00323232003E3E3E000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF000000FF0000008000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00C0C0
      C000FFFFFF00FFFFFF00FFFFFF0000000000FFFFFF00C0C0C000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00C0C0C000C0C0C0000000000000000000F0B08000F0B89000F8C0
      9800F8C8A000F8C8A800C0C0C00000FFFF00C0C0C000C0C0C000C0C0C00080FF
      FF00C0C0C00058585800A0A0A000000000004A4A4A00CECECE00DADADA00F2F2
      F20080808000AAAAAA00AAAAAA00C0C0C0009E9E9E003E3E3E003E3E3E003E3E
      3E003E3E3E003E3E3E002626260000000000FFFFFF00FFFFFF0080808000FFFF
      FF00FFFFFF00FFFF000000008000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00C0C0C000FFFFFF0000000000FFFFFF00C0C0C000800000008000
      0000800000008000000080000000800000008000000080000000800000008000
      000080000000FFFFFF00C0C0C00000000000F0A87000F0B07800F0B08000F0B8
      8800F0C09000F8C8A000F8D0A800F8D0B000C0C0C00080FFFF0080FFFF0080FF
      FF0080FFFF00000000000000000000000000F2F2F200C0C0C00092929200DADA
      DA00CECECE00C0C0C000C0C0C000E6E6E600AAAAAA003E3E3E003E3E3E003E3E
      3E003E3E3E003E3E3E003E3E3E002626260080808000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF000000FF0000008000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF0080808000FFFFFF00C0C0C000800000008000
      000080000000800000008000000080000000FFFF0000FFFF0000FFFF0000FFFF
      000080000000FFFFFF00C0C0C00000000000F0A06000F0A86800F0A87000F0B0
      8000F0B88800F0C09000F8C8A000F8D0A800F8D0B000F8E0C80080FFFF0080FF
      FF0080FFFF0080FFFF0080FFFF0000000000F2F2F200E6E6E600E6E6E600E6E6
      E600E6E6E600E6E6E600C0C0C000C0C0C000AAAAAA0032323200323232004A4A
      4A003E3E3E003E3E3E003E3E3E00000000000000000000000000000000000000
      00000000000000000000000000000000FF000000800000000000000000000000
      000000000000000000000000000000000000FFFFFF00C0C0C000800000008000
      000080000000FF00FF00FF00FF00FF00FF00FFFF0000FFFF0000FFFF0000FFFF
      000080000000FFFFFF00C0C0C00000000000E8985800F0A06000F0A06800F0A8
      7000F0B07800F0B88800F8C09800F8C8A000F8D0A800F8D0B000F8E0C80080FF
      FF0000000000000000000000000000000000F2F2F200F2F2F200E6E6E600C0C0
      C000C0C0C000DADADA00DADADA00F2F2F200E6E6E6009E9E9E003E3E3E003E3E
      3E004A4A4A003E3E3E003E3E3E000E0E0E000000000000000000000000000000
      0000000000000000000000000000000000000000FF0000008000000000000000
      000000000000000000000000000000000000FFFFFF00C0C0C000800000008000
      000080000000FF00FF00FF00FF00FF00FF00FFFF0000FFFF0000FFFF0000FFFF
      000080000000FFFFFF00C0C0C00000000000E8904800E8985000F0A05800F0A0
      6800F0A87000F0B07800F0B88800F8C09800F8C8A000F8D0A800F8D0B000F8E0
      C80000000000000000000000000000000000F2F2F200C0C0C000E6E6E600E6E6
      E600F2F2F200FFFFFF009E9E9E00CECECE00C0C0C000AAAAAA00C0C0C0009292
      9200323232003E3E3E003E3E3E000E0E0E000000000000000000000000000000
      00000000000000000000000000000000000000000000FFFF0000000080000000
      000000000000000000000000000000000000FFFFFF00C0C0C00080000000FF00
      0000FF000000FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00800000008000
      000080000000FFFFFF00C0C0C00000000000E8884000E8904800E8985000E898
      5800F0A06000F0A87000F0B07800F0B0800010101000F0C0900010101000D068
      680000000000000000000000000000000000F2F2F200F2F2F200F2F2F200AAAA
      AA006E6E6E00AAAAAA00AAAAAA004A4A4A004A4A4A00E6E6E600DADADA00E6E6
      E600F2F2F200323232003E3E3E000E0E0E000000000000000000000000000000
      00000000000000000000000000000000000000000000000000000000FF000000
      800000000000000000000000000000000000FFFFFF00C0C0C00080000000FF00
      0000FF000000FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00800000008000
      000080000000FFFFFF00C0C0C00000000000E8803000E8883800E8904000E890
      5000E8985800F0A0600010101000D0686800D0686800D0686800D06868000000
      000000000000000000000000000000000000DADADA00CECECE006E6E6E00F2F2
      F200FFFFFF00FFFFFF00F2F2F200E6E6E600AAAAAA0062626200C0C0C000C0C0
      C0003E3E3E006E6E6E003E3E3E000E0E0E000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000FFFFFF000000
      FF0000008000000000000000000000000000FFFFFF00C0C0C00080000000FF00
      0000FF000000FF000000FF000000800000008000000080000000800000008000
      000080000000FFFFFF00C0C0C00000000000E8782000E8803000E8883800E888
      4000E8904800E898500010101000D0006800D0686800D0686800D06868000000
      0000000000000000000000000000000000000000000000000000AAAAAA00CECE
      CE003E3E3E004A4A4A004A4A4A00808080009E9E9E003E3E3E000E0E0E00CECE
      CE006E6E6E00E6E6E600FFD4E3000E0E0E000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000FFFF
      FF000000FF00000080000000000000000000FFFFFF00C0C0C000800000008000
      0000800000008000000080000000800000008000000080000000800000008000
      000080000000FFFFFF00C0C0C00000000000E0701800E0782000E8802800E888
      38001010100068306800D000680000000000D000680010101000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000DADADA006E6E6E003E3E3E00262626003E3E3E00AAAAAA00F2F2F200F2F2
      F200C0C0C0000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF00000000000000000000000000FFFFFF00C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0C000C0C0
      C000C0C0C000C0C0C000C0C0C00000000000E0701800E0701800101010009800
      3000980000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000CECECE00C0C0C000FFFFFF00DADADA00C0C0C000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00000000000000000000000000680030000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000090909000909090009090
      900090909000909090009898980098989800A0A0A000A8A8A800B0B0B000B8B8
      B800C0C0C000C8C8C80000000000000000000000000090909000909090009090
      900090909000909090009898980098989800A0A0A000A8A8A800B0B0B000B8B8
      B800C0C0C000C8C8C80000000000000000000000000080808000808080008080
      8000808080008080800000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000068B8A8003898800048A8
      900060B0A00078B8A80088C8B800A0D0C800B0D8D000C8E8E000E0F0E800F0F8
      F800FFFFFF00FFFFFF0000000000000000000000000060A0F0002880E8004088
      E8005898F00068A8F00080B0F00098C0F800A8D0F800C0D8F800D8E8FF00E8F8
      FF00FFFFFF00FFFFFF0000000000000000006E6E6E004A4A4A004A4A4A004A4A
      4A004A4A4A0062626200CECECE00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000068B8A0003098800048A0
      900058B0980070B8A80080C0B80098D0C000B0D8D000C0E0D800D8F0E800E8F8
      F800FFFFFF00FFFFFF0000000000000000000000000060A0F0002878E8003888
      E8005090E80068A0F00078B0F00090B8F000A8C8F800B8D8F800D0E0FF00E8F0
      FF00F8FFFF00FFFFFF0000000000000000009E9E9E00FFFFFF00F2F2F200E6E6
      E600DADADA009E9E9E00CECECE0080808000000000004A4A4A00000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000BDBD
      0000BDBD0000BDBD000000000000000000000000000060B0A0002898800040A0
      880058A8980068B8A0009090900090C8C000A8D8C800B8E0D800D0E8E800E8F8
      F000F8FFFF00FFFFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000C8E0F800E0F0
      FF00F8F8FF00FFFFFF00000000000000000000000000DADADA00F2F2F200F2F2
      F200F2F2F200DADADA00626262003E3E3E008080800032323200262626000000
      0000000000000000000000000000000000000000000000000000848484008484
      84008484840084848400848484008484840000000000FFFF0000000000000000
      0000000000000000000000000000000000000000000060B0A0002890780038A0
      880050A8900068686800FFFFFF0068686800A0D0C800B8E0D000C8E8E000E0F0
      F000F0FFF800FFFFFF0000000000000000000000000088889000384040000060
      C800787870000068C8002828300080787800FFFFFF0000000000C0D8F800D8E8
      FF00F0F8FF00FFFFFF0000000000000000000000000000000000000000009292
      92003E3E3E006E6E6E009E9E9E00AAAAAA009E9E9E003E3E3E003E3E3E000E0E
      0E00000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000FFFF0000FFFF
      0000FFFF00000000000084848400000000000000000058B09800209078005050
      5000FFFFFF00C0C0C000C0C0C000D0D0D00098D0C000B0D8D000C8E0E000D8F0
      E800F0F8F800FFFFFF0000000000000000000000000018181800001850000070
      C80088B0B8000048400000A8FF000070B0000000280000000000B8D8F800D0E8
      FF00E8F0FF00FFFFFF00000000000000000000000000808080003E3E3E00AAAA
      AA00C0C0C000E6E6E6009E9E9E00AAAAAA00AAAAAA003E3E3E003E3E3E004A4A
      4A00323232003E3E3E000000000000000000000000000000000000000000C6C6
      C600C6C6C600C6C6C60084848400FFFF000000000000FFFF0000FFFF0000FFFF
      0000000000000000000084848400000000000000000060606000FFFFFF00C8C8
      C800C0C0C000C0C0C000C0C0C000E8E8E80028282800A8D8C800C0E0D800D8E8
      E800E8F8F000FFFFFF00000000000000000000000000403838000000000000A0
      F00050586000008880000070D00000A8FF000048B80000000000B8D0F800C8E0
      FF00E0F0FF00FFFFFF0000000000000000004A4A4A00CECECE00DADADA00F2F2
      F20080808000AAAAAA00AAAAAA00C0C0C0009E9E9E003E3E3E003E3E3E003E3E
      3E003E3E3E003E3E3E0026262600000000000000000000000000000000000000
      0000C6C6C60084848400FFFF000000000000FFFF0000FFFF0000FFFF00000000
      0000C6C6C600C6C6C6000000000000000000000000009098A000F0F0F800C8D0
      D800C0C0C000C0C0C000C0C0C000C0C0C000F8F8F800A0D0C800B8E0D800D0E8
      E000E0F0F000FFFFFF00000000000000000000000000000000003898A8001018
      10002050580050484000002018000078C8000060D00000000000B0D0F800C8E0
      F800D8E8FF00F8FFFF000000000000000000F2F2F200C0C0C00092929200DADA
      DA00CECECE00C0C0C000C0C0C000E6E6E600AAAAAA003E3E3E003E3E3E003E3E
      3E003E3E3E003E3E3E003E3E3E00262626000000000000000000000000000000
      000000000000FFFF000000000000FFFF0000FFFF0000FFFF0000000000000000
      00000000000000000000000000000000000090908000D8D00000B8A87800FFFF
      0000C8C8D000D0D0D000C0C8A800B8308000E8E8E80038383800B0D8D000C8E8
      E000D8F0E800F8FFFF0000000000000000000000000068400000B0D0E80070D8
      FF005060680088888000001800001080C00000B8FF0000000000A8C8F800C0D8
      F800D0E8FF00F0F8FF000000000000000000F2F2F200E6E6E600E6E6E600E6E6
      E600E6E6E600E6E6E600C0C0C000C0C0C000AAAAAA0032323200323232004A4A
      4A003E3E3E003E3E3E003E3E3E00000000000000000000000000000000000000
      0000FFFF000000000000FFFF0000FFFF0000FFFF000000000000848484000000
      0000000000000000000000000000000000009898880068581800705800006850
      000080705000D0C8C800F0F0F0008858600080804800F0F0F000B0D8D000C0E0
      D800D8F0E800F0FFFF0000000000000000000000000070707800403838007068
      6000282828008888880038482800101000005858500000000000A0C8F800B8D8
      F800D0E0FF00E8F8FF000000000000000000F2F2F200F2F2F200E6E6E600C0C0
      C000C0C0C000DADADA00DADADA00F2F2F200E6E6E6009E9E9E003E3E3E003E3E
      3E004A4A4A003E3E3E003E3E3E000E0E0E00000000000000000000000000FFFF
      000000000000FFFF0000FFFF0000FFFF000000000000C6C6C600000000008484
      840000000000000000000000000000000000A0A09000D8D0A000B0A800008868
      2000A8981000C0C0D000F8F8F800E0E0E0008080800090C8C000A8D8C800B8E0
      D800D0E8E000F0FFF800000000000000000028202000C0C8C80040404000D8D8
      D80060606000F0E0D80040404000F0F0F000D0D0D0000000000098C0F800B0D0
      F800C8E0F800E0F0FF000000000000000000F2F2F200C0C0C000E6E6E600E6E6
      E600F2F2F200FFFFFF009E9E9E00CECECE00C0C0C000AAAAAA00C0C0C0009292
      9200323232003E3E3E003E3E3E000E0E0E000000000000000000FFFF00000000
      0000FFFF0000FFFF0000FFFF000000000000C6C6C600C6C6C600C6C6C6000000
      0000848484000000000000000000000000004848000070700000008060006050
      280070701000585820005050500060B0A00078C0A80088C8B800A0D0C800B8D8
      D000C8E8E000E8F8F8000000000000000000000000007820000028000000C8C8
      C800B8B8B800D8D8D80040404000A0A0A000D0D0D0000000000098C0F800A8D0
      F800C0D8F800D8F0FF000000000000000000F2F2F200F2F2F200F2F2F200AAAA
      AA006E6E6E00AAAAAA00AAAAAA004A4A4A004A4A4A00E6E6E600DADADA00E6E6
      E600F2F2F200323232003E3E3E000E0E0E0000000000FFFF000000000000FFFF
      0000FFFF0000FFFF0000000000000000000000000000C6C6C600C6C6C600C6C6
      C600000000008484840000000000000000000000000058A89800008060008888
      8800505050003098800048A0900058B0980070B8A80088C0B80098D0C000B8E0
      D800C8E8E000E0F8F00000000000000000000000000028000000000000002828
      280040404000303030003030300010101000000000001010100090B8F000B0D0
      F800C0D8F800D8E8FF000000000000000000DADADA00CECECE006E6E6E00F2F2
      F200FFFFFF00FFFFFF00F2F2F200E6E6E600AAAAAA0062626200C0C0C000C0C0
      C0003E3E3E006E6E6E003E3E3E000E0E0E000000000000000000FFFF0000FFFF
      0000FFFF00000000000000000000000000000000000000000000C6C6C600C6C6
      C600C6C6C6000000000000000000000000000000000058A89800008060000080
      6800188870003098800040A0880058A8980068B8A00080C0B00090C8C0003098
      800060B0A000D8E8E8000000000000000000000000005898E8000068E0000068
      E0000068E0002078E8003080E8004890E80060A0F00078A8F00088B8F0002880
      E8004890E800D0E0F80000000000000000000000000000000000AAAAAA00CECE
      CE003E3E3E004A4A4A004A4A4A00808080009E9E9E003E3E3E000E0E0E00CECE
      CE006E6E6E00E6E6E600FFD4E3000E0E0E000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000058A89800008060000080
      6000108870002890780038A0880050A8900068B0A00078C0B00090C8B8003898
      800060B0A000000000000000000000000000000000005898E8000068E0000068
      E0000068E0001870E0003080E8004088E8005898F00070A8F00080B0F0003080
      E8004890E8000000000000000000000000000000000000000000000000000000
      0000DADADA006E6E6E003E3E3E00262626003E3E3E00AAAAAA00F2F2F200F2F2
      F200C0C0C0000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000058A89800008060000080
      600000886800209078003898800048A8900060B0A00070B8A80088C8B8002090
      780000000000000000000000000000000000000000005898E8000068E0000068
      E0000068E0001070E0002878E8003888E8005098E80068A0F00078B0F0002070
      E000000000000000000000000000000000000000000000000000000000000000
      000000000000CECECE00C0C0C000FFFFFF00DADADA00C0C0C000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000038343800383438003834
      3800383438003834380038343800383438003834380038343800383438003834
      3800383438003834380038343800000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000020FF2000000000000000
      00000000000000000000000000000000000058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00B0ACB000B0ACB000B0ACA000FFFFFF00FFFFFF00FFFF
      FF00FFE07800FFFFFF00383438000000000058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00B0ACB000B0ACB000B09CB000A0ACB000FFFFFF00FFFF
      FF00FFFFFF00FFFFFF0058585800000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000003868
      2000487830005890400068A050000000000000FF000020F8280038F8400050F0
      580068E8780078E09000000000000000000058585800FFE07800FFE09000FFE0
      7800FFD09000FFE07800FFE09000FFE07800FFD09000FFE07800FFE09000FFE0
      7800FFD09000FFE07800383438000000000058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00B0ACB000B0ACA000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF0058585800000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000098D8A8003058
      180040702800508038006098480000FF000010FF100028F8280040F0480050F0
      600068E8780080E0980098D8B0000000000058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF000000000000000000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFE07800FFFFFF00383438000000000058585800FFFFFF00FFFFFF00FFFF
      FF00585858000000000058585800FFFFFF005858580058585800000000005858
      5800FFFFFF00FFFFFF0058585800000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000BDBD
      0000BDBD0000BDBD000000000000000000000000000080E0980080E090002850
      10003860200048783000588840000000000018FF180028F8300040F0480058E8
      680070E8800088E09800A0D8B8000000000058585800FFFFFF00FFFFFF00B014
      7800C0149000FFFFFF009078E0003834580058489000B0247800C0149000B014
      7800FFE09000FFFFFF00383438000000000058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF005858780038244800788CD000FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF0058585800000000000000000000000000848484008484
      84008484840084848400848484008484840000000000FFFF0000000000000000
      0000000000000000000000000000000000000000000070E8800068E878000000
      0000000000000000000000000000000000000000000030F83800000000000000
      00002040000020400000284800002848000058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF006878B000A08CF000384858003824480058587800FFFF
      FF00FFE07800FFFFFF00383438000000000058585800FFFFFF00000000005858
      580058585800585858006868C000908CF00028244800383458009078E0005858
      5800FFFFFF00FFFFFF0058585800000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000FFFF0000FFFF
      0000FFFF000000000000848484000000000058E8680058F0600050F0600050F0
      60000000000048F0580000000000000000000000000000000000000000000000
      00000000000030581800386018003860200058585800FFFFFF00FFFFFF00E024
      A000E014B000E024A000E014B000B0BCFF00A09CF00038486800282448001814
      2800FFD09000FFFFFF00383438000000000058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00B0BCFF00909CE00038244800283448003848
      9000FFFFFF00FFFFFF005858580000000000000000000000000000000000C6C6
      C600C6C6C600C6C6C60084848400FFFF000000000000FFFF0000FFFF0000FFFF
      00000000000000000000848484000000000048F0500040F0480040F0480038F8
      400038F8400038F8400000000000000000000000000000000000000000000000
      00004070280048703000487830004878300058585800FFFFFF00FFFFFF00FFFF
      FF0018781800FFFFFF00187818007868C000B0BCFF003858A0002858A0002824
      480018242800FFFFFF00383438000000000058585800FFFFFF00585858005858
      58005858580058585800000000006868B000B0BCFF00908CF000181448001824
      380038489000FFFFFF0058585800000000000000000000000000000000000000
      0000C6C6C60084848400FFFF000000000000FFFF0000FFFF0000FFFF00000000
      0000C6C6C600C6C6C60000000000000000000000000028F8300028F8300028F8
      280020F828000000000000000000000000000000000000000000000000000000
      00005888400058884000589040000000000058585800FFFFFF00FFFFFF000078
      1800186828000078180018682800007818003858A000488CFF003858A0002858
      A0002824480018142800383438000000000058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00488CFF003858A0003858A0002824
      4800182438003848900058585800000000000000000000000000000000000000
      000000000000FFFF000000000000FFFF0000FFFF0000FFFF0000000000000000
      00000000000000000000000000000000000018FF180018FF180010FF180010FF
      100010FF10000000000000000000000000000000000000000000000000000000
      000068A0500068A8500068A858000000000058585800FFFFFF0018781800FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF003858A000489CFF003858
      A0002858A00028244800182428000000000058585800FFFFFF00FFFFFF005858
      580058585800585858005858580058585800B09CB000488CFF003858A0002858
      A000281448001824380058585800000000000000000000000000000000000000
      0000FFFF000000000000FFFF0000FFFF0000FFFF000000000000848484000000
      00000000000000000000000000000000000000FF000000FF000000FF000000FF
      0000000000000000000000000000000000000000000000000000000000005890
      40000000000070B06000000000000000000058585800FFFFFF00FFFFFF001878
      1800186828000078180018681800FFFFFF00FFFFFF00A01478003858A000488C
      FF003858A0002858A000282448001814280058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00489CFF003858
      A0002868A000282448001824380000000000000000000000000000000000FFFF
      000000000000FFFF0000FFFF0000FFFF000000000000C6C6C600000000008484
      8400000000000000000000000000000000000000000000000000000000000000
      000000FF000010FF100000000000000000000000000000000000487028005888
      400068A0500000000000000000000000000058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF003858
      A000489CFF003858A0002858A0002824480058585800FFFFFF00FFFFFF00FFFF
      FF0058587800B0ACB000FFFFFF00FFFFFF00B0ACB00058585800B09CB000488C
      FF003858A0002858A00018144800182438000000000000000000FFFF00000000
      0000FFFF0000FFFF0000FFFF000000000000C6C6C600C6C6C600C6C6C6000000
      00008484840000000000000000000000000000000000000000000000000018FF
      200020F8280030F8380038F84000000000000000000030581000406828005080
      38006098480070B05800000000000000000058585800FFFFFF00FFFFFF00FFFF
      FF009068680090686800B08C9000FFFFFF00C09CB000C09CB000B0ACB000FFFF
      FF003858A000488CFF003858A0002858A00058585800FFFFFF00FFFFFF00FFFF
      FF005858780058585800B0ACB000FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00488CFF003858A0003858A0002824480000000000FFFF000000000000FFFF
      0000FFFF0000FFFF0000000000000000000000000000C6C6C600C6C6C600C6C6
      C6000000000084848400000000000000000000000000000000000000000038F8
      400040F0500050F0580058F06000000000002040000028501000386820004878
      30000000000068A85800000000000000000058585800FFFFFF00FFFFFF00FFFF
      FF001814280018142800B08C9000FFFFFF00FFFFFF00B0ACB000FFFFFF00FFFF
      FF00FFE078003858A000489CFF003858A00058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00488CFF003858A0002858A0000000000000000000FFFF0000FFFF
      0000FFFF00000000000000000000000000000000000000000000C6C6C600C6C6
      C600C6C6C6000000000000000000000000000000000000000000000000000000
      000060E8700068E8780078E0880080E090002040000028480000386018000000
      0000000000000000000000000000000000005858580058585800585858005858
      5800585858005858580058585800585858005858580058585800585858005858
      580058585800585858003858A000488CFF0058585800FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF00489CFF003858A0000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000080E0900088E0A00098D8A800A0D8B800A0D8B80020400000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000488CFF000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000A8FFFF0088F8FF0070F8
      FF0050F8FF0030F0FF0010F0FF00404858000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000055555500555555005555550055555500000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000055555500555555005555550055555500000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000B8FFFF0098FFFF0078F8
      FF0060F8FF0040F8FF0020F0FF00384858000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000005555
      5500FFFFFF00FFFFFF00FFFFFF003300FF003300CC00C0C0C000CCCCCC005555
      5500000000000000000000000000000000000000000000000000000000005555
      5500FFFFFF00FFFFFF00FFFFFF003300FF003300CC00C0C0C000CCCCCC005555
      5500000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000001818FF00000000000000
      000000000000000000000000000000000000E0FFFF00C0FFFF00A8FFFF0088F8
      FF0068F8FF0050F8FF0030687800385868000000000000000000000000000000
      000000000000000000000000000000000000000000000000000055555500FFFF
      FF00F0FBFF00FFFFFF00F0FBFF003300FF00DDDDDD00F0FBFF00F0FBFF00DDDD
      DD00C0C0C000000000000000000000000000000000000000000055555500FFFF
      FF00F0FBFF00FFFFFF00F0FBFF00FFCCCC00DDDDDD00F0FBFF00F0FBFF00DDDD
      DD00C0C0C0000000000000000000000000000000000000000000000000001800
      7000200088002000A0002800B800000000000000FF001818FF003838FF005050
      FF006868FF008888FF000000000000000000F0FFFF00D0FFFF00B0FFFF0098F8
      FF0078F8FF0058F8FF0000FF0000386070000000000000000000000000000000
      0000000000000000000000000000000000000000000055555500FFFFFF00F0FB
      FF00FFFFFF00FFFFFF00F0FBFF00F0FBFF003300FF00F0FBFF00F0FBFF00F0FB
      FF00F0FBFF00CCCCCC0000000000000000000000000055555500FFFFFF00F0FB
      FF00FFFFFF00FFFFFF003300FF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00F0FBFF00CCCCCC0000000000000000000000000000000000A8A8FF001800
      680020008000200098002800B0000000FF000000FF002020FF003838FF005858
      FF007070FF008888FF00A8A8FF000000000000E8F80010D0E80010C0D80018B0
      C000704800007048000028FF280018FF18000000000000000000000000000068
      E0000000000000000000000000000000000000000000FFFFFF00F0FBFF00FFFF
      FF00FFFFFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00FFCCCC00F0FBFF00F0FB
      FF00F0FBFF00DDDDDD00555555000000000000000000FFFFFF00F0FBFF00FFFF
      FF00FFFFFF003300FF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00F0FBFF00DDDDDD00555555000000000000000000A0A0FF00A0A0FF001800
      600018007000200090002000A800000000000000FF002020FF004040FF005858
      FF007878FF009090FF00A8A8FF000000000000F0FF0000E0F000886028008058
      200078501800704800007048000050FF50000000000000000000000000000000
      00000000000000000000000000000000000055555500F0FBFF00FFFFFF00FFFF
      FF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00FFCCCC00F0FB
      FF00F0FBFF00F0FBFF00C0C0C0000000000055555500F0FBFF00FFFFFF00FFFF
      FF00F0FBFF00FFCCCC00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00F0FBFF00F0FBFF00C0C0C00000000000000000008888FF008080FF000000
      000000000000000000000000000000000000000000002828FF00000000000000
      0000180078001800700018006000180060000000000000E8FF00A8886000A080
      5000987848000000FF008868300090FF900080FF800000000000000000000000
      00002880E800000000000000000000000000FFFFFF00F0FBFF00FFFFFF00FFFF
      FF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF003300FF00F0FB
      FF00F0FBFF00F0FBFF00DDDDDD0055555500FFFFFF00F0FBFF00FFFFFF00FFFF
      FF003300FF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00F0FBFF00F0FBFF00DDDDDD00555555007070FF006868FF006868FF006060
      FF00000000005858FF0000000000000000000000000000000000000000000000
      0000000000002000800018007800180068000000000000000000000000005050
      FF003838FF002020FF00A8886000A08058000000000000000000000000000000
      000070B8F800000000000000000000000000FFFFFF00F0FBFF00FFCCCC00FFCC
      CC00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00FFCC
      CC00F0FBFF00F0FBFF00A4A0A00055555500FFFFFF00F0FBFF00FFCCCC00FFCC
      CC00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00FFCC
      CC00F0FBFF00F0FBFF00A4A0A000555555005858FF005050FF005050FF004848
      FF004040FF004040FF0000000000000000000000000000000000000000000000
      00002800A80020009800200090002000800000000000000000009090FF007878
      FF006060FF004040FF00C8B09800C0A88800C0A0800000000000000000000000
      000000000000000000000000000000000000FFFFFF0000000000FFFFFF00F0FB
      FF00F0FBFF00F0FBFF003300FF00F0FBFF003300FF00F0FBFF00F0FBFF00FFCC
      CC00F0FBFF00F0FBFF00C0C0C00055555500FFFFFF0000000000FFFFFF00F0FB
      FF00F0FBFF00F0FBFF003300FF00F0FBFF003300FF00F0FBFF00F0FBFF00FFCC
      CC00F0FBFF00F0FBFF00C0C0C00055555500000000003838FF003030FF003030
      FF002828FF000000000000000000000000000000000000000000000000000000
      00002800C0002800B0002000A000000000000000000000000000B8B8FF009898
      FF008080FF006868FF005050FF00000000000000000000000000000000000000
      000000000000000000000000000000000000FFFFFF000000000000000000F0FB
      FF00F0FBFF00F0FBFF00FFCCCC00F0FBFF00FFCCCC00F0FBFF00F0FBFF00FFCC
      CC0000000000F0FBFF00C0C0C00055555500FFFFFF000000000000000000F0FB
      FF00F0FBFF00F0FBFF00FFCCCC00F0FBFF00FFCCCC00F0FBFF00F0FBFF00FFCC
      CC0000000000F0FBFF00C0C0C000555555002020FF001818FF001818FF001010
      FF001010FF000000000000000000000000000000000000000000000000000000
      00002800C8002800C8002800B80000000000000000000000000000000000C0C0
      FF00A8A8FF009090FF007878FF006060FF0000000000B0FFFF0098FFFF0078F8
      FF0060F8FF0040F8FF0028F0FF00404858006666660000000000FFCCCC00FFCC
      CC00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00FFCC
      CC00FFCCCC00F0FBFF00CCCCCC00000000006666660000000000FFCCCC00FFCC
      CC00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00FFCC
      CC00FFCCCC00F0FBFF00CCCCCC00000000000000FF000000FF000000FF000000
      FF00000000000000000000000000000000000000000000000000000000002800
      C000000000002800C8000000000000000000000000000000000000000000E8E8
      FF00D0D0FF00B8B8FF009898FF008080FF00D8FFFF00C0FFFF00A0FFFF0088F8
      FF0068F8FF0050F8FF0030F0FF004048580077777700FFFFFF00F0FBFF00FFFF
      FF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00F0FBFF00F0FBFF00A4A0A0000000000077777700FFFFFF00F0FBFF00FFFF
      FF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00F0FBFF00F0FBFF00A4A0A000000000000000000000000000000000000000
      00000000FF001818FF00000000000000000000000000000000002000A0002800
      B0002800C0000000000000000000000000000000000000000000000000000000
      0000F0F0FF00D8D8FF000000000000000000E8FFFF00C8FFFF00B0FFFF0090F8
      FF0078F8FF0058F8FF0030687800385060000000000099999900F0FBFF00FFFF
      FF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00F0FBFF00CCCCCC0055555500000000000000000099999900F0FBFF00FFFF
      FF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00F0FBFF00CCCCCC0055555500000000000000000000000000000000002020
      FF002828FF003838FF004040FF00000000000000000020008000200090002000
      A0002800B0002800C00000000000000000000000000000000000000000000000
      000000000000000000000000000000000000E8FFFF00D8FFFF00B8FFFF00A0FF
      FF0080F8FF0068F8FF0030708000385868000000000000000000F0FBFF00FFFF
      FF00FFFFFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00CCCCCC005555550000000000000000000000000000000000F0FBFF00FFFF
      FF00FFFFFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FBFF00F0FB
      FF00CCCCCC005555550000000000000000000000000000000000000000004040
      FF005050FF005858FF006060FF00000000001800600018007000200080002000
      9000000000002800B00000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000F0FF0000E0F00010C8E00018B8
      C80020A0B8002890A00028788800306878000000000000000000000000006666
      6600F0FBFF00FFFFFF00FFFFFF00F0FBFF00F0FBFF00DDDDDD00F0FBFF00A4A0
      A000555555000000000000000000000000000000000000000000000000006666
      6600F0FBFF00FFFFFF00FFFFFF00F0FBFF00F0FBFF00DDDDDD00F0FBFF00A4A0
      A000555555000000000000000000000000000000000000000000000000000000
      00007070FF007878FF008080FF009090FF001800600018006000180070000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000E8FF0010D8E80010C0
      D800000000000000000000000000000000000000000000000000000000000000
      00007777770055555500F0FBFF00DDDDDD00DDDDDD00A4A0A000555555000000
      0000000000000000000000000000000000000000000000000000000000000000
      00007777770055555500F0FBFF00DDDDDD00DDDDDD00A4A0A000555555000000
      0000000000000000000000000000000000000000000000000000000000000000
      00009090FF009898FF00A8A8FF00A8A8FF00A8A8FF0018006000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000444444004444440044444400444444000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000444444000000
      000077777700DDDDDD0000000000000000000000000000000000000000000000
      00000000000040485800404858004048580038F0FF0000000000000000000000
      0000000000000000000000000000000000000000000000000000000000008EFF
      FF008EFFFF008EFFFF00B1FFFF00B1FFFF00D4FFFF00D4FFFF00FFFFFF00FFFF
      FF00FFFFFF00FFFFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000006699CC006699CC0099CCFF0099CCFF000000000044444400DDDD
      DD00FFFFFF00DDDDDD0000000000000000000000000000000000000000000000
      000038F0FF00A8F8FF0098F8FF007878780080F0FF0078F0FF0038F0FF000000
      00000000000000000000000000000000000000000000FFE2B100FFE2B1006BFF
      FF008EFFFF008EFFFF008EFFFF00B1FFFF00B1FFFF00D4FFFF00D4FFFF00FFFF
      FF00FFFFFF00FFFFFF0000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000444444004444
      44006699CC00000000000000000099CCFF0099CCFF0000000000DDDDDD00DDDD
      DD00A4A0A000DDDDDD00000000000000000000000000000000000000000048F0
      FF00B8F8FF00A8F8FF00A0F8FF0090F8FF0088F0FF0078F0FF0070F0FF0068F0
      FF0038F0FF0000000000000000000000000000000000FFD48E00FFE2B1006BFF
      FF006BFFFF008EFFFF008EFFFF008EFFFF00B1FFFF00B1FFFF00D4FFFF00D4FF
      FF00FFFFFF00FFFFFF0000000000000000000000000000000000000000007088
      9800708098006878900000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000FF999900FF99
      9900000000002222220099CCFF00FFFFFF00DDDDDD00DDDDDD00DDDDDD00DDDD
      DD00A4A0A000DDDDDD000000000000000000000000000000000060F0FF00C8FF
      FF00B8F8FF00B0F8FF00A0F8FF0098F8FF0088F8FF0080F0FF0070F0FF0068F0
      FF0068F0FF0068F0FF0038F0FF000000000000000000FFC66B00FFD48E0048FF
      FF006BFFFF00FF25AA009600620050003200FE00FE00B900B90073007300C0C0
      C000D4FFFF00FFFFFF000000000000000000000000000000000000E8FF0000E0
      F80000E0F00000D8E80000D0E000000000000000000000000000000000008888
      FF00A0A0FF00B8B8FF00D0D0FF000000000000000000FFCCCC00FFCCCC00FFCC
      CC00FF9999004444440000000000DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDD
      DD00777777000000000000000000000000000000000000000000D8FFFF00D0FF
      FF00C0FFFF00B8F8FF00A8F8FF00A0F8FF0090F8FF0080F0FF0078F0FF0068F0
      FF0068F0FF0068F0FF0068F0FF000000000000000000FFC66B00FFC66B0048FF
      FF0048FFFF00FF6BC600FF25AA0096006200FF48FF00FE00FE00B900B9007300
      7300D4FFFF00D4FFFF000000000000000000000000000000000000E8F8000000
      0000000000000000000000C8D8000000000000000000000000005050FF006868
      FF008888FF00A0A0FF00B8B8FF002800A800FFFFFF00FFCCCC00FFCCCC00FFCC
      CC00FFCCCC000000000044444400DDDDDD00DDDDDD00DDDDDD00DDDDDD000000
      0000999999000000000000000000000000000000000088F0FF00A0A0A000D0FF
      FF00C8F8FF00B8F8FF00B0F8FF00A0F8FF0098F8FF0088F8FF0080F0FF0070F0
      FF0068F0FF0068F0FF00000000000000000000000000FFAA0000FFC66B0025FF
      FF0048FFFF00FFB1E200FF6BC600FF25AA00FF6BFF00FF48FF00FE00FE00B900
      B900B1FFFF00D4FFFF0000000000000000000090680000805800B8FFB8001060
      3800105028000000000000C8D8000000000000000000000000003838FF005050
      FF006868FF008888FF00A0A0FF002000980044444400FFCCCC00FFCCCC00FFCC
      CC00FFFFFF0000000000DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDDDD00FFFF
      FF00FFFFFF00DDDDDD0000000000000000000000000078787800A0A0A000A0A0
      A000A0A0A000C0FFFF00B0F8FF00A8F8FF0098F8FF0090F8FF0080F0FF0078F0
      FF0068F0FF0000000000000000000000000000000000FFAA0000FFAA000000FE
      FE0025FFFF0025FFFF0025FFFF006BFFFF00FFB1FF00FF6BFF008EFFFF008EFF
      FF00B1FFFF00B1FFFF00000000000000000070FF700080FF800098FF9800B0FF
      B000C8FFC8000000000000C0D0005058680000000000000000002020FF003838
      FF005050FF006868FF008888FF002000880000000000FFFFFF00FFCCCC00FFFF
      FF0099999900DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDD
      DD00A4A0A000DDDDDD00000000000000000000000000A0A0A000A0A0A0007878
      780078787800A0A0A000B8F8FF00B0F8FF00A0F8FF0090F8FF0088F0FF0078F0
      FF0038F0FF0000000000000000000000000000000000DC920000FFAA000000FE
      FE0000FEFE0025FFFF0048FFFF0048FFFF00FFD4FF00FFB1FF006BFFFF008EFF
      FF008EFFFF00B1FFFF00000000000000000050FF500068FF680080FF800090FF
      9000A8FFA8000000000000B8C80000B0C00000A8B800404858000000FF002020
      FF003838FF005050FF006868FF00180078000000000000000000000000000000
      0000FFFFFF00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDD
      DD00A4A0A000DDDDDD00000000000000000048404000A0A0A000503800005038
      00005038000050380000C0FFFF00B0F8FF00A8F8FF0098F8FF0090F8FF0080F0
      FF000000000000000000000000000000000000000000DC920000DC92000000DC
      DC0000FEFE0000FEFE0025FFFF0048FFFF0048FFFF006BFFFF006BFFFF008EFF
      FF008EFFFF008EFFFF00000000000000000030FF300048FF480060FF600078FF
      780090FF900000000000000000000000000000A8B000404050000000FF000000
      FF002020FF003838FF005050FF00180060000000000000000000000000000000
      0000FFFFFF00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDD
      DD0055555500DDDDDD0000000000000000000000000000000000906800009068
      000098982000D8C0580000000000B8F8FF00A8F8FF00A0F8FF0090F8FF0038F0
      FF000000000000000000000000000000000000000000B97A0000DC92000000B9
      B90000DCDC0000FEFE00C0C0C000F2F2F20048FFFF0048FFFF006BFFFF006BFF
      FF008EFFFF008EFFFF00000000000000000018FF180030FF300040FF400058FF
      580070FF700000000000000000000000000000A0B00038404800000000000000
      FF000000FF002020FF003838FF00000000000000000000000000000000000000
      0000FFFFFF00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDDDD00DDDDDD00FFFF
      FF00FFFFFF00000000000000000000000000000000000000000090680000D8A8
      2000D8C05800D8C0580000000000B8F8FF00B0F8FF00A0F8FF0098F8FF000000
      00000000000000000000000000000000000000000000B97A0000B97A00000096
      960000B9B90000DCDC0000000000F2F2F20025FFFF0048FFFF0048FFFF000073
      73008EFFFF00FFFFFF00000000000000000000FF000010FF100028FF280040FF
      400050FF50000000000000000000000000000098A80030384000000000000000
      0000008088002830380000000000000000000000000000000000000000000000
      0000FFFFFF00DDDDDD00DDDDDD00DDDDDD00DDDDDD00FFFFFF00FFFFFF000000
      000000000000000000000000000000000000000000000000000000000000D8A8
      2000D8C0580000000000D0FFFF00C0FFFF00B8F8FF00A8F8FF0038F0FF000000
      0000000000000000000000000000000000000000000096620000B97A00000073
      73000096960000B9B90000000000F2F2F20000FEFE0025FFFF0048FFFF000073
      73008EFFFF000000000000000000000000000000000000FF000000FF000020FF
      2000000000000000000000000000000000000098A00000909800283038002830
      3800007888002830380000000000000000000000000000000000000000000000
      0000FFFFFF00DDDDDD00DDDDDD00FFFFFF00FFFFFF0000000000000000000000
      000000000000000000000000000000000000000000000000000048404000E8E8
      2800E8E82800484040000000000000000000B8F8FF00B0F8FF00000000000000
      00000000000000000000000000000000000000000000734A0000966200000050
      5000007373000096960000000000F2F2F20000FEFE0000FEFE0025FFFF000073
      7300000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000889800008090000080
      8800007880000000000000000000000000000000000000000000000000000000
      0000FFFFFF00FFFFFF00FFFFFF00000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000E8E82800FFFF
      6800FFFF6800E8E8280000000000000000000000000000000000000000000000
      00000000000000000000000000000000000000000000734A0000734A00000050
      5000005050000073730000000000F2F2F20000DCDC0000FEFE0025FFFF00FFC6
      6B00000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000FFFFFF000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000000000000000000000000000FFFF
      6800FFFF68000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000050320000734A0000734A
      000096620000B97A00000000000000000000DC920000FFAA0000FFAA0000FFC6
      6B00000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      000000000000000000000000000000000000424D3E000000000000003E000000
      2800000040000000800000000100010000000000000400000000000000000000
      000000000000000000000000FFFFFF0000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      0000000000000000000000000000000000000000000000000000000000000000
      00000000000000000000000000000000C003FFFFFFF7000080030001FCE30000
      80030003F9C1000080030603FF81000080038C07F981000080038807F0C30000
      8003C00FE06700008003C02FA03F00008003E03FB07500008003E05F58F30000
      8003F0BFFC0F00008003F03FFE0F00008003F87FFE0F00008003F87FFE0F0000
      8007FCFFFE0F0000800FFCFFFFF5000083FF0000C007FF8F01FF0000C007FE01
      00BF0000F81FF800801F00000000F801E00F00000000E0018003000000008001
      000100000000000700000000000000010000FE7F000000070000FF3F00000007
      0000FF9F000000070000FFCF0000000F0000FFC70000001FC000FFE30000003F
      F007FFF3000003FFF83FFFFF00008FFFFFFF8003800383FFFFFF8003800301FF
      FFC18003800300BF800180030003801F800180030003E00F8000800300038003
      C000800300030001E000800300030000F000000300030000E00F000300030000
      C00700030003000080030003000300000101800300030000038180038003C000
      07C180078007F007FFFF800F800FF83FFFFF8001FFFFFFFFFFBF00010001FFFF
      E10300010001FFC1C00100010001800181010001000180019FB0000100018000
      0BF800010001C00003F000010001E00087F100010001F00007F100010001E00F
      0FEB00000001C007F3C7000000008003E183000000000101E10B000000000381
      F01F0000000007C1F03FFFFFFFFEFFFF80FFFC3FFC3FFFFF80FFE00FE00FFFBF
      00FFC007C007E10300FF80038003C00100EF80018001810100FF000100019FB0
      8077000000000BF8E0F70000000003F0C07F0000000087F1C1FF0000000007F1
      E080000100010FEBE00000010001F3C7F30080018001E183FF00C003C003E10B
      FF00E007E007F01FFF8FF01FF01FF03FFE1BFFFFE003FFFFFC01F87F8003FFFF
      F001F01F8003FFFFC001E0078003E3FF8001C0018003C1E10001C0018003DDC0
      00018003800305C000018007800304C00001800780030400C001000F80030700
      F001800F80030721F003801F80030733F00FC01F80078F03F03FC33F8007FF87
      F0FFC3FF8007FFFFF3FFE7FF800FFFFF00000000000000000000000000000000
      000000000000}
  end
  object Timer2: TTimer
    Enabled = False
    Interval = 50
    OnTimer = Timer2Timer
    Left = 136
    Top = 80
  end
end
