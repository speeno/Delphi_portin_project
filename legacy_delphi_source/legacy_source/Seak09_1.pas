unit Seak09;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Buttons, Mask, TFlatButtonUnit, TFlatNumberUnit,
  TFlatMaskEditUnit, TFlatEditUnit, TFlatComboBoxUnit, TFlatPanelUnit,
  Mylabel;

type
  TSeak90 = class(TForm)
    Panel001: TFlatPanel;
    Button102: TFlatButton;
    Button101: TFlatButton;
    BitBtn101: TBitBtn;
    BitBtn102: TBitBtn;
    Panel002: TFlatPanel;
    Panel101: TFlatPanel;
    Panel103: TFlatPanel;
    Panel102: TFlatPanel;
    Panel104: TFlatPanel;
    Panel105: TFlatPanel;
    Panel106: TFlatPanel;
    Panel108: TFlatPanel;
    Panel107: TFlatPanel;
    Panel109: TFlatPanel;
    Panel110: TFlatPanel;
    Panel112: TFlatPanel;
    Panel111: TFlatPanel;
    Panel113: TFlatPanel;
    Panel115: TFlatPanel;
    Edit102: TFlatComboBox;
    Edit101: TFlatEdit;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit108: TFlatEdit;
    Edit109: TFlatEdit;
    Edit110: TFlatEdit;
    Edit115: TFlatEdit;
    Edit105: TFlatMaskEdit;
    Panel114: TFlatPanel;
    Edit106: TFlatMaskEdit;
    Edit107: TFlatMaskEdit;
    Edit111: TFlatMaskEdit;
    Edit112: TFlatNumber;
    Edit113: TFlatNumber;
    Edit114: TFlatNumber;
    Edit3: TFlatEdit;
    Panel300: TFlatPanel;
    Panel311: TFlatPanel;
    Panel312: TFlatPanel;
    Panel321: TFlatPanel;
    Panel331: TFlatPanel;
    Panel341: TFlatPanel;
    Panel351: TFlatPanel;
    Panel352: TFlatPanel;
    Panel411: TFlatPanel;
    Panel412: TFlatPanel;
    Panel421: TFlatPanel;
    Panel422: TFlatPanel;
    Panel431: TFlatPanel;
    Panel432: TFlatPanel;
    Panel441: TFlatPanel;
    Panel442: TFlatPanel;
    Panel451: TFlatPanel;
    Panel452: TFlatPanel;
    Panel511: TFlatPanel;
    Panel512: TFlatPanel;
    Panel521: TFlatPanel;
    Panel531: TFlatPanel;
    Panel541: TFlatPanel;
    Panel551: TFlatPanel;
    Panel552: TFlatPanel;
    Edit311: TFlatNumber;
    Edit321: TFlatNumber;
    Edit331: TFlatNumber;
    Edit341: TFlatNumber;
    Edit411: TFlatNumber;
    Edit412: TFlatNumber;
    Edit421: TFlatNumber;
    Edit422: TFlatNumber;
    Edit431: TFlatNumber;
    Edit432: TFlatNumber;
    Edit441: TFlatNumber;
    Edit442: TFlatNumber;
    Edit451: TFlatNumber;
    Edit452: TFlatNumber;
    Edit511: TFlatNumber;
    Edit521: TFlatNumber;
    Edit531: TFlatNumber;
    Edit541: TFlatNumber;
    Edit551: TFlatNumber;
    Panel332: TFlatPanel;
    RadioButton331: TRadioButton;
    RadioButton332: TRadioButton;
    Panel342: TFlatPanel;
    RadioButton341: TRadioButton;
    RadioButton342: TRadioButton;
    Panel353: TFlatPanel;
    RadioButton351: TRadioButton;
    RadioButton352: TRadioButton;
    Panel413: TFlatPanel;
    RadioButton411: TRadioButton;
    RadioButton412: TRadioButton;
    Panel423: TFlatPanel;
    RadioButton421: TRadioButton;
    RadioButton422: TRadioButton;
    Panel433: TFlatPanel;
    RadioButton431: TRadioButton;
    RadioButton432: TRadioButton;
    Panel443: TFlatPanel;
    RadioButton441: TRadioButton;
    RadioButton442: TRadioButton;
    Panel453: TFlatPanel;
    RadioButton451: TRadioButton;
    RadioButton452: TRadioButton;
    Panel513: TFlatPanel;
    RadioButton511: TRadioButton;
    RadioButton512: TRadioButton;
    Panel522: TFlatPanel;
    RadioButton521: TRadioButton;
    RadioButton522: TRadioButton;
    Panel532: TFlatPanel;
    RadioButton531: TRadioButton;
    RadioButton532: TRadioButton;
    Panel542: TFlatPanel;
    RadioButton541: TRadioButton;
    RadioButton542: TRadioButton;
    Panel553: TFlatPanel;
    RadioButton551: TRadioButton;
    RadioButton552: TRadioButton;
    FlatPanel7: TFlatPanel;
    Edit238: TFlatEdit;
    Edit236: TFlatNumber;
    FlatPanel18: TFlatPanel;
    myLabel3d1: TmyLabel3d;
    FlatPanel1: TFlatPanel;
    myLabel3d2: TmyLabel3d;
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure FilterTing(Str,Sth:String);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit111KeyPress(Sender: TObject; var Key: Char);
    procedure Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit112KeyPress(Sender: TObject; var Key: Char);
    procedure Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure BitBtn101Click(Sender: TObject);
    procedure BitBtn102Click(Sender: TObject);
    procedure Button300Click(Str1: String);
    procedure RadioButtonClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seak90: TSeak90;

implementation

{$R *.DFM}

uses Base01, TcpLib;

procedure TSeak90.FormShow(Sender: TObject);
begin
  Edit311.Height:=35;
  Edit321.Height:=35;
  Edit331.Height:=35;
  Edit341.Height:=35;
  Edit511.Height:=35;
  Edit521.Height:=35;
  Edit531.Height:=35;
  Edit541.Height:=35;
  Edit551.Height:=35;
//Edit101.SetFocus;
end;

procedure TSeak90.FormClose(Sender: TObject; var Action: TCloseAction);
begin
//
end;

procedure TSeak90.FilterTing(Str,Sth:String);
var St1: String;
begin
  if Str='' Then Str:='0';
  St1:='ID'+'='+Str;
  St1:='Hcode'+'='+#39+Sth+#39+' and '+'('+St1+')';
  Edit3.Text:=Sth;

  Sqlen :=
  'Select Gnumb,Scode,Gname,Gposa,Date1,Date2,Date3,'+
  ' Name1,Gbang,Name2,Date4,Gssum,Grat1,Gosum,Gbigo '+
  'From H4_Iyeo Where '+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeGrid(SGrid);

    Idnum:=StrToIntDef(Str,0);
    Edit101.Text :=SGrid.Cells[ 0,1];
    Edit102.Text :=SGrid.Cells[ 1,1];
    Edit103.Text :=SGrid.Cells[ 2,1];
    Edit104.Text :=SGrid.Cells[ 3,1];
    Edit105.Text :=SGrid.Cells[ 4,1];
    Edit106.Text :=SGrid.Cells[ 5,1];
    Edit107.Text :=SGrid.Cells[ 6,1];
    Edit108.Text :=SGrid.Cells[ 7,1];
    Edit109.Text :=SGrid.Cells[ 8,1];
    Edit110.Text :=SGrid.Cells[ 9,1];
    Edit111.Text :=SGrid.Cells[10,1];
    Edit112.Value:=StrToIntDef(SGrid.Cells[11,1],0);
    Edit113.Value:=StrToIntDef(SGrid.Cells[12,1],0);
    Edit114.Value:=StrToIntDef(SGrid.Cells[13,1],0);
    Edit115.Text :=SGrid.Cells[14,1];
  end else begin

    Idnum:=0;
    Edit101.Text :=''; Edit102.Text :=''; Edit103.Text :=''; Edit104.Text :='';
    Edit105.Text :=''; Edit106.Text :=''; Edit107.Text :=''; Edit108.Text :='';
    Edit109.Text :=''; Edit110.Text :=''; Edit111.Text :=''; Edit112.Value:=0;
    Edit113.Value:=0;  Edit114.Value:=0;  Edit115.Text :='';
    Edit103.Text :=oSqry.FieldByName('Gname').AsString;
    Edit106.Text :=oSqry.FieldByName('Gdate').AsString;
    Edit112.Value:=oSqry.FieldByName('Gssum').AsFloat;
  end;
end;

procedure TSeak90.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSeak90.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSeak90.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSeak90.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSeak90.Edit112KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    Edits: TFlatComboBox;
begin
  Edits:=Edit102; Hands:=Edit102.Handle;
  if Key=#13 Then begin
    if Edits.DropDownCount=9 Then Edits.DropDownCount:=8 else
    if Edits.DropDownCount=8 Then Edits.DropDownCount:=9;
    if Edits.DropDownCount=9 Then begin
      Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
    end else
    if Edits.DropDownCount=8 Then begin
      Key:=#0; SendMessage(Hands, cb_ShowDropDown, 1, 0);
    end;
  end;
end;

procedure TSeak90.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit102;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSeak90.BitBtn101Click(Sender: TObject);
var Str: String;
begin
  if Idnum=0 Then begin

    Sqlon :='INSERT INTO H4_Iyeo '+
    '(Gnumb, Gname, Gposa, Date1, Date2, Date3, '+
    ' Date4, Gbang, Name1, Name2, Scode, Gbigo, '+
    ' Grat1, Gssum, Gosum, Hcode) VALUES ';
    Sqlen :=
    '(''@Gnumb'',''@Gname'',''@Gposa'',''@Date1'',''@Date2'',''@Date3'', '+
    ' ''@Date4'',''@Gbang'',''@Name1'',''@Name2'',''@Scode'',''@Gbigo'', '+
    '   @Grat1  ,  @Gssum  ,  @Gosum  ,''@Hcode'')';

    Translate(Sqlen, '@Gnumb', Edit101.Text);
    Translate(Sqlen, '@Scode', Edit102.Text);
    Translate(Sqlen, '@Gname', Edit103.Text);
    Translate(Sqlen, '@Gposa', Edit104.Text);
    Translate(Sqlen, '@Date1', Edit105.Text);
    Translate(Sqlen, '@Date2', Edit106.Text);
    Translate(Sqlen, '@Date3', Edit107.Text);
    Translate(Sqlen, '@Name1', Edit108.Text);
    Translate(Sqlen, '@Gbang', Edit109.Text);
    Translate(Sqlen, '@Name2', Edit110.Text);
    Translate(Sqlen, '@Date4', Edit111.Text);
    TransAuto(Sqlen, '@Gssum', FloatToStr(Edit112.Value));
    TransAuto(Sqlen, '@Grat1', FloatToStr(Edit113.Value));
    TransAuto(Sqlen, '@Gosum', FloatToStr(Edit114.Value));
    Translate(Sqlen, '@Gbigo', Edit115.Text);
    Translate(Sqlen, '@Hcode', Edit3.Text);

    Sqlen:=Sqlon+Sqlen;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Idnum:=0;

    Str := 'Select gen_id(' + 'H4_IYEO_ID_GEN' +',0),Count(*) From G0_Gbun';
    Str := 'Select LAST_INSERT_ID()';
    Base10.Socket.RunSQL(Str);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      Idnum := StrToIntDef(Base10.Socket.GetData(1, 1),0);
    end;

  end else begin

    Sqlon := 'UPDATE H4_Iyeo SET '+
    'Gnumb=''@Gnumb'',Gname=''@Gname'',Gposa=''@Gposa'',Date1=''@Date1'','+
    'Date2=''@Date2'',Date3=''@Date3'',Date4=''@Date4'',Gbang=''@Gbang'',';
    Sqlen :=
    'Name1=''@Name1'',Name2=''@Name2'',Scode=''@Scode'',Gbigo=''@Gbigo'','+
    'Grat1=  @Grat1  ,Gssum=  @Gssum  ,Gosum=  @Gosum  ,Hcode=''@Hcode'' '+
    'WHERE ID=@ID';

    Translate(Sqlon, '@Gnumb', Edit101.Text);
    Translate(Sqlen, '@Scode', Edit102.Text);
    Translate(Sqlon, '@Gname', Edit103.Text);
    Translate(Sqlon, '@Gposa', Edit104.Text);
    Translate(Sqlon, '@Date1', Edit105.Text);
    Translate(Sqlon, '@Date2', Edit106.Text);
    Translate(Sqlon, '@Date3', Edit107.Text);
    Translate(Sqlen, '@Name1', Edit108.Text);
    Translate(Sqlon, '@Gbang', Edit109.Text);
    Translate(Sqlen, '@Name2', Edit110.Text);
    Translate(Sqlon, '@Date4', Edit111.Text);
    TransAuto(Sqlen, '@Gssum', FloatToStr(Edit112.Value));
    TransAuto(Sqlen, '@Grat1', FloatToStr(Edit113.Value));
    TransAuto(Sqlen, '@Gosum', FloatToStr(Edit114.Value));
    Translate(Sqlen, '@Gbigo', Edit115.Text);
    Translate(Sqlen, '@Hcode', Edit3.Text);
    TransAuto(Sqlen, '@ID', FloatToStr(Idnum));

    Sqlen:=Sqlon+Sqlen;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
end;

procedure TSeak90.BitBtn102Click(Sender: TObject);
begin
//
end;

procedure TSeak90.RadioButtonClick(Sender: TObject);
begin
  if RadioButton331.Checked=True then begin
    Edit331.Enabled:=True;
    Edit331.ColorFlat:=clWhite;
  end else begin
    Edit331.Value:=0;
    Edit331.Enabled:=False;
    Edit331.ColorFlat:=clActiveBorder;
  end;
  if RadioButton341.Checked=True then begin
    Edit341.Enabled:=True;
    Edit341.ColorFlat:=clWhite;
  end else begin
    Edit341.Value:=0;
    Edit341.Enabled:=False;
    Edit341.ColorFlat:=clActiveBorder;
  end;

  if RadioButton411.Checked=True then begin
    Edit411.Enabled:=True;
    Edit411.ColorFlat:=clWhite;
    Edit412.Enabled:=True;
    Edit412.ColorFlat:=$0080FFFF;
  end else begin
    Edit411.Value:=0;
    Edit411.Enabled:=False;
    Edit411.ColorFlat:=clActiveBorder;
    Edit412.Value:=0;
    Edit412.Enabled:=False;
    Edit412.ColorFlat:=clActiveBorder;
  end;
  if RadioButton421.Checked=True then begin
    Edit421.Enabled:=True;
    Edit421.ColorFlat:=clWhite;
    Edit422.Enabled:=True;
    Edit422.ColorFlat:=$0080FFFF;
  end else begin
    Edit421.Value:=0;
    Edit421.Enabled:=False;
    Edit421.ColorFlat:=clActiveBorder;
    Edit422.Value:=0;
    Edit422.Enabled:=False;
    Edit422.ColorFlat:=clActiveBorder;
  end;
  if RadioButton431.Checked=True then begin
    Edit431.Enabled:=True;
    Edit431.ColorFlat:=clWhite;
    Edit432.Enabled:=True;
    Edit432.ColorFlat:=$0080FFFF;
  end else begin
    Edit431.Value:=0;
    Edit431.Enabled:=False;
    Edit431.ColorFlat:=clActiveBorder;
    Edit432.Value:=0;
    Edit432.Enabled:=False;
    Edit432.ColorFlat:=clActiveBorder;
  end;
  if RadioButton441.Checked=True then begin
    Edit441.Enabled:=True;
    Edit441.ColorFlat:=clWhite;
    Edit442.Enabled:=True;
    Edit442.ColorFlat:=$0080FFFF;
  end else begin
    Edit441.Value:=0;
    Edit441.Enabled:=False;
    Edit441.ColorFlat:=clActiveBorder;
    Edit442.Value:=0;
    Edit442.Enabled:=False;
    Edit442.ColorFlat:=clActiveBorder;
  end;
  if RadioButton451.Checked=True then begin
    Edit451.Enabled:=True;
    Edit451.ColorFlat:=clWhite;
    Edit452.Enabled:=True;
    Edit452.ColorFlat:=$0080FFFF;
  end else begin
    Edit451.Value:=0;
    Edit451.Enabled:=False;
    Edit451.ColorFlat:=clActiveBorder;
    Edit452.Value:=0;
    Edit452.Enabled:=False;
    Edit452.ColorFlat:=clActiveBorder;
  end;

  if RadioButton511.Checked=True then begin
    Edit511.Enabled:=True;
    Edit511.ColorFlat:=clWhite;
  end else begin
    Edit511.Value:=0;
    Edit511.Enabled:=False;
    Edit511.ColorFlat:=clActiveBorder;
  end;
  if RadioButton521.Checked=True then begin
    Edit521.Enabled:=True;
    Edit521.ColorFlat:=clWhite;
  end else begin
    Edit521.Value:=0;
    Edit521.Enabled:=False;
    Edit521.ColorFlat:=clActiveBorder;
  end;
  if RadioButton531.Checked=True then begin
    Edit531.Enabled:=True;
    Edit531.ColorFlat:=clWhite;
  end else begin
    Edit531.Value:=0;
    Edit531.Enabled:=False;
    Edit531.ColorFlat:=clActiveBorder;
  end;
  if RadioButton541.Checked=True then begin
    Edit541.Enabled:=True;
    Edit541.ColorFlat:=clWhite;
  end else begin
    Edit541.Value:=0;
    Edit541.Enabled:=False;
    Edit541.ColorFlat:=clActiveBorder;
  end;
  if RadioButton551.Checked=True then begin
    Edit551.Enabled:=True;
    Edit551.ColorFlat:=clWhite;
  end else begin
    Edit551.Value:=0;
    Edit551.Enabled:=False;
    Edit551.ColorFlat:=clActiveBorder;
  end;
end;

procedure TSeak90.Button300Click(Str1: String);
begin
  {-G7_Ggeo-}
  Sqlen := 'Select '+
  'Sum02,Sum04,Sum06,Sum09,Sum12,Sum15,Sum18,Sum19,Sum21,Sum22,Sum25,Sum32,Sum33,'+
  'Sum34,Sum38,Sum39,Sum40,Sum41,Sum42,Yes33,Yes34,Yes35,Yes41,Yes42,Yes43,Yes44,'+
  'Yes45,Yes51,Yes52,Yes53,Yes54,Yes55,Sum36,Bigo1 '+
  'From G7_Ggeo Where Gcode'+'='+#39+Str1+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  if SGrid.Cells[19,1]='1' then
  RadioButton331.Checked:=True else
  RadioButton332.Checked:=True;

  if SGrid.Cells[20,1]='1' then
  RadioButton341.Checked:=True else
  RadioButton342.Checked:=True;

  if SGrid.Cells[21,1]='1' then
  RadioButton351.Checked:=True else
  RadioButton352.Checked:=True;

  if SGrid.Cells[22,1]='1' then
  RadioButton411.Checked:=True else
  RadioButton412.Checked:=True;

  if SGrid.Cells[23,1]='1' then
  RadioButton421.Checked:=True else
  RadioButton422.Checked:=True;

  if SGrid.Cells[24,1]='1' then
  RadioButton431.Checked:=True else
  RadioButton432.Checked:=True;

  if SGrid.Cells[25,1]='1' then
  RadioButton441.Checked:=True else
  RadioButton442.Checked:=True;

  if SGrid.Cells[26,1]='1' then
  RadioButton451.Checked:=True else
  RadioButton452.Checked:=True;

  if SGrid.Cells[27,1]='1' then
  RadioButton511.Checked:=True else
  RadioButton512.Checked:=True;

  if SGrid.Cells[28,1]='1' then
  RadioButton521.Checked:=True else
  RadioButton522.Checked:=True;

  if SGrid.Cells[29,1]='1' then
  RadioButton531.Checked:=True else
  RadioButton532.Checked:=True;

  if SGrid.Cells[30,1]='1' then
  RadioButton541.Checked:=True else
  RadioButton542.Checked:=True;

  if SGrid.Cells[31,1]='1' then
  RadioButton551.Checked:=True else
  RadioButton552.Checked:=True;

  Edit311.Value:=StrToIntDef(SGrid.Cells[ 0,1],0);
  Edit321.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
  Edit331.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
  Edit341.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);

  Edit411.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
  Edit412.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
  Edit421.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
  Edit422.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);
  Edit431.Value:=StrToIntDef(SGrid.Cells[14,1],0);
  Edit432.Value:=StrToIntDef(SGrid.Cells[15,1],0);
  Edit441.Value:=StrToIntDef(SGrid.Cells[16,1],0);
  Edit442.Value:=StrToIntDef(SGrid.Cells[17,1],0);
  Edit451.Value:=StrToIntDef(SGrid.Cells[12,1],0);
  Edit452.Value:=StrToIntDef(SGrid.Cells[13,1],0);

  Edit511.Value:=StrToIntDef(SGrid.Cells[10,1],0);
  Edit521.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
  Edit531.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
  Edit541.Value:=StrToIntDef(SGrid.Cells[11,1],0);
  Edit551.Value:=StrToIntDef(SGrid.Cells[18,1],0);

  Edit236.Value:=StrToIntDef(SGrid.Cells[32,1],0);
  Edit238.Text :=SGrid.Cells[33,1];

  RadioButtonClick(Self);
end;

end.
