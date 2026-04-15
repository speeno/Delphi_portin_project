unit Seak05;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Buttons, Printers, QuickRpt, TFlatGroupBoxUnit,
  TFlatPanelUnit, TFlatButtonUnit, TFlatEditUnit, TFlatSpinEditUnit;

type
  TSeak50 = class(TForm)
    GroupBox1: TFlatGroupBox;
    StaticText1: TStaticText;
    StaticText2: TStaticText;
    StaticText3: TStaticText;
    StaticText4: TStaticText;
    SpinEdit1: TFlatSpinEditInteger;
    SpinEdit2: TFlatSpinEditInteger;
    SpinEdit3: TFlatSpinEditInteger;
    SpinEdit4: TFlatSpinEditInteger;
    GroupBox2: TFlatGroupBox;
    BitBtn101: TFlatButton;
    BitBtn100: TFlatButton;
    BitBtn102: TFlatButton;
    BitBtn103: TBitBtn;
    Button101: TFlatButton;
    FontDialog1: TFontDialog;
    RadioButton1: TRadioButton;
    RadioButton2: TRadioButton;
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure GroupBox1Click(Sender: TObject);
    procedure BitBtn101Click(Sender: TObject);
    procedure BitBtn102Click(Sender: TObject);
    procedure BitBtn103Click(Sender: TObject);
    procedure BitBtn100Click(Sender: TObject);
    procedure PrinTing(QPrint: TQuickRep);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seak50: TSeak50;

implementation

{$R *.DFM}

uses Base01, TcpLib;

procedure TSeak50.FormShow(Sender: TObject);
begin

  Sqlen :='Select Top,L11,L61,L62 From Gg_Magn Where '+'Gu'+'='+#39+'0'+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  SpinEdit3.Value:=StrToIntDef(SGrid.Cells[ 0,1],0);
  SpinEdit4.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
  SpinEdit1.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
  SpinEdit2.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);

  if SpinEdit2.Value=2970  Then begin
  RadioButton1.Checked:=True;
  RadioButton2.Checked:=False;
  end else begin
  RadioButton1.Checked:=False;
  RadioButton2.Checked:=True;
  end;
end;

procedure TSeak50.FormClose(Sender: TObject; var Action: TCloseAction);
begin

  Sqlen := 'UPDATE Gg_Magn SET '+
  'Top=@Top,L11=@L11,L61=@L61,L62=@L62 '+
  'WHERE Gu=''@Gu''';

  Translate(Sqlen, '@Gu',  '0');
  TransAuto(Sqlen, '@Top', FloatToStr(SpinEdit3.Value));
  TransAuto(Sqlen, '@L11', FloatToStr(SpinEdit4.Value));
  TransAuto(Sqlen, '@L61', FloatToStr(SpinEdit1.Value));
  TransAuto(Sqlen, '@L62', FloatToStr(SpinEdit2.Value));

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

end;

procedure TSeak50.GroupBox1Click(Sender: TObject);
begin
  if RadioButton1.Checked=True Then begin
  RadioButton2.Checked:=False;
  SpinEdit1.Value:=2100;
  SpinEdit2.Value:=2970; end else
  if RadioButton2.Checked=True Then begin
  RadioButton1.Checked:=False;
  SpinEdit1.Value:=2100;
  SpinEdit2.Value:=2794; end;
end;

procedure TSeak50.BitBtn100Click(Sender: TObject);
begin
  FontDialog1.Execute;
end;

procedure TSeak50.BitBtn101Click(Sender: TObject);
var
  Device : array[0 .. 255] of char;
  Driver : array[0 .. 255] of char;
  Port : array[0 .. 32] of char;
  hDMode : THandle;
  pDMode : PDevMode;
begin
{ Printer.GetPrinter(Device, Driver, Port, hDMode);
  if hDMode=0 then Exit;
  pDMode:=GlobalLock(hDMode);
  if pDMode=nil then Exit;
  pDMode^.dmFields     :=(pDMode^.dmFields)or(DM_PAPERLENGTH)or(DM_PAPERWIDTH);
  pDMode^.dmPaperSize  :=DMPAPER_USER;
  pDMode^.dmPaperWidth :=SpinEdit1.Value;
  pDMode^.dmPaperLength:=SpinEdit2.Value;
  GlobalUnlock(hDMode);
  Printer.SetPrinter(Device, Driver, Port, hDMode); }
  nPrnt:='1';
end;

procedure TSeak50.BitBtn102Click(Sender: TObject);
var
  Device : array[0 .. 255] of char;
  Driver : array[0 .. 255] of char;
  Port : array[0 .. 32] of char;
  hDMode : THandle;
  pDMode : PDevMode;
begin
{ Printer.GetPrinter(Device, Driver, Port, hDMode);
  if hDMode=0 then Exit;
  pDMode:=GlobalLock(hDMode);
  if pDMode=nil then Exit;
  pDMode^.dmFields     :=(pDMode^.dmFields)or(DM_PAPERLENGTH)or(DM_PAPERWIDTH);
  pDMode^.dmPaperSize  :=DMPAPER_USER;
  pDMode^.dmPaperWidth :=SpinEdit1.Value;
  pDMode^.dmPaperLength:=SpinEdit2.Value;
  GlobalUnlock(hDMode);
  Printer.SetPrinter(Device, Driver, Port, hDMode); }
  nPrnt:='2';
end;

procedure TSeak50.BitBtn103Click(Sender: TObject);
begin
  nPrnt:='0';
end;

procedure TSeak50.PrinTing(QPrint: TQuickRep);
begin
  QPrint.Font:=Seak50.FontDialog1.Font;
  QPrint.Page.LeftMargin  :=Seak50.SpinEdit4.Value;
  QPrint.Page.TopMargin   :=Seak50.SpinEdit3.Value;
  QPrint.Page.Length:=Seak50.SpinEdit2.Value/10;
  QPrint.Page.Width :=Seak50.SpinEdit1.Value/10;
  if Seak50.SpinEdit2.Value=2970 Then begin
  QPrint.Page.RightMargin :=05+05-Seak50.SpinEdit4.Value;
  QPrint.Page.BottomMargin:=10+10-Seak50.SpinEdit3.Value;
  end else begin
  QPrint.Page.RightMargin :=05+05-Seak50.SpinEdit4.Value;
  QPrint.Page.BottomMargin:=08+10-Seak50.SpinEdit3.Value;
  end;
  if nPrnt='1' Then QPrint.Print;
  if nPrnt='2' Then QPrint.Preview;
end;

end.
