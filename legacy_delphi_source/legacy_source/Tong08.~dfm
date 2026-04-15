object Tong80: TTong80
  Left = 192
  Top = 107
  Width = 696
  Height = 480
  Caption = 'Tong80'
  Color = clBtnFace
  Font.Charset = ANSI_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = '굴림'
  Font.Style = [fsBold]
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 12
  object ComTerminal: TComTerminal
    Left = 47
    Top = 8
    Width = 201
    Height = 41
    Color = clBlack
    Columns = 2
    ComPort = ComPort
    Emulation = teVT100orANSI
    Font.Charset = EASTEUROPE_CHARSET
    Font.Color = clWhite
    Font.Height = -12
    Font.Name = 'Fixedsys'
    Font.Style = []
    ImeName = '한국어 입력 시스템 (IME 2000)'
    Rows = 2
    ScrollBars = ssBoth
    TabOrder = 0
    Visible = False
    OnStrRecieved = ComTerminalStrRecieved
  end
  object ComPort: TComPort
    BaudRate = br9600
    Port = 'COM1'
    Parity.Bits = prNone
    StopBits = sbOneStopBit
    DataBits = dbEight
    Events = [evRxChar, evTxEmpty, evRxFlag, evRing, evBreak, evCTS, evDSR, evError, evRLSD, evRx80Full]
    FlowControl.OutCTSFlow = True
    FlowControl.OutDSRFlow = False
    FlowControl.ControlDTR = dtrEnable
    FlowControl.ControlRTS = rtsHandshake
    FlowControl.XonXoffOut = False
    FlowControl.XonXoffIn = False
    OnRxChar = ComPortRxChar
    Left = 8
    Top = 12
  end
end
