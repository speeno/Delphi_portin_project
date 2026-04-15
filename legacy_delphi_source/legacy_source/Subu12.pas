unit Subu12;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, TFlatCheckBoxUnit,
  dxCore, dxButtons, CornerButton;

type
  TSobo12 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel003: TFlatPanel;
    Panel004: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    Panel100: TFlatPanel;
    Panel101: TFlatPanel;
    Panel103: TFlatPanel;
    Panel102: TFlatPanel;
    Panel105: TFlatPanel;
    Panel106: TFlatPanel;
    Panel107: TFlatPanel;
    Panel109: TFlatPanel;
    Panel108: TFlatPanel;
    Panel110: TFlatPanel;
    Panel112: TFlatPanel;
    Panel114: TFlatPanel;
    Panel111: TFlatPanel;
    Panel116: TFlatPanel;
    Panel118: TFlatPanel;
    Panel125: TFlatPanel;
    Panel200: TFlatPanel;
    Panel201: TFlatPanel;
    Panel202: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    DBGrid101: TDBGrid;
    DBGrid201: TDBGrid;
    Button104: TFlatButton;
    Label100: TmyLabel3d;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    Label103: TmyLabel3d;
    Label104: TmyLabel3d;
    Label105: TmyLabel3d;
    Label106: TmyLabel3d;
    Label107: TmyLabel3d;
    Label108: TmyLabel3d;
    Label109: TmyLabel3d;
    Label110: TmyLabel3d;
    Label200: TmyLabel3d;
    Edit101: TFlatComboBox;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Edit106: TFlatEdit;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Edit109: TFlatEdit;
    Edit110: TFlatEdit;
    Edit111: TFlatEdit;
    Edit112: TFlatEdit;
    Edit113: TFlatEdit;
    Edit114: TFlatEdit;
    Edit115: TFlatEdit;
    Edit116: TFlatEdit;
    Edit117: TFlatEdit;
    Edit118: TFlatNumber;
    Edit119: TFlatNumber;
    Edit120: TFlatNumber;
    Edit121: TFlatNumber;
    Edit122: TFlatNumber;
    Edit123: TFlatNumber;
    Edit124: TFlatNumber;
    Edit125: TFlatEdit;
    Edit201: TFlatEdit;
    Edit202: TFlatEdit;
    Panel126: TFlatPanel;
    Edit126: TFlatEdit;
    Panel127: TFlatPanel;
    Edit127: TFlatEdit;
    CheckBox1: TFlatCheckBox;
    Label300: TmyLabel3d;
    Label301: TmyLabel3d;
    Panel129: TFlatPanel;
    CheckBox2: TFlatCheckBox;
    Edit129: TFlatEdit;
    CornerButton2: TCornerButton;
    CornerButton3: TCornerButton;
    CornerButton4: TCornerButton;
    Label002: TmyLabel3d;
    Label003: TmyLabel3d;
    Label309: TmyLabel3d;
    Button000: TdxButton;
    Button101: TdxButton;
    Button102: TdxButton;
    Button103: TdxButton;
    Button201: TdxButton;
    Button202: TdxButton;
    Button203: TdxButton;
    procedure FormPaint(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Button001Click(Sender: TObject);
    procedure Button002Click(Sender: TObject);
    procedure Button003Click(Sender: TObject);
    procedure Button004Click(Sender: TObject);
    procedure Button005Click(Sender: TObject);
    procedure Button006Click(Sender: TObject);
    procedure Button007Click(Sender: TObject);
    procedure Button008Click(Sender: TObject);
    procedure Button009Click(Sender: TObject);
    procedure Button010Click(Sender: TObject);
    procedure Button011Click(Sender: TObject);
    procedure Button012Click(Sender: TObject);
    procedure Button013Click(Sender: TObject);
    procedure Button014Click(Sender: TObject);
    procedure Button015Click(Sender: TObject);
    procedure Button016Click(Sender: TObject);
    procedure Button017Click(Sender: TObject);
    procedure Button018Click(Sender: TObject);
    procedure Button019Click(Sender: TObject);
    procedure Button020Click(Sender: TObject);
    procedure Button021Click(Sender: TObject);
    procedure Button022Click(Sender: TObject);
    procedure Button023Click(Sender: TObject);
    procedure Button024Click(Sender: TObject);
    procedure Button101Click(Sender: TObject);
    procedure Button102Click(Sender: TObject);
    procedure Button103Click(Sender: TObject);
    procedure Button104Click(Sender: TObject);
    procedure Button201Click(Sender: TObject);
    procedure Button202Click(Sender: TObject);
    procedure Button203Click(Sender: TObject);
    procedure Edit101Exit(Sender: TObject);
    procedure Edit101Change(Sender: TObject);
    procedure Edit101KeyPress(Sender: TObject; var Key: Char);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit102KeyPress(Sender: TObject; var Key: Char);
    procedure Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit111KeyPress(Sender: TObject; var Key: Char);
    procedure Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit112KeyPress(Sender: TObject; var Key: Char);
    procedure Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit113KeyPress(Sender: TObject; var Key: Char);
    procedure Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
    procedure Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101DblClick(Sender: TObject);
    procedure DBGrid101Enter(Sender: TObject);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101Exit(Sender: TObject);
    procedure DBGrid201Exit(Sender: TObject);
    procedure DBGrid101TitleClick(Column: TColumn);
    procedure DBGrid201TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure SeachClick(Str1,Str2: String);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo12: TSobo12;

implementation

{$R *.DFM}

uses Chul, Base01, Subu19, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo12.FormPaint(Sender: TObject);
begin
{ Button023Click(Self);
  Button024Click(Self); }
  Sobo12.OnPaint:=Nil;
  Sobo12.OnShow:=FormShow;
  FormShow(Self);
end;

procedure TSobo12.FormActivate(Sender: TObject);
begin
  nForm:='12';
  nSqry:=Base10.T1_Sub21;
  mSqry:=Base10.T1_Sub22;
end;

procedure TSobo12.FormShow(Sender: TObject);
begin
  Refresh;
  Application.CreateForm(TSobo19, Sobo19);
  Sobo19.ShowModal;
  Sobo19.Edit100.ItemIndex:=Sobo19.Edit000.ItemIndex;
  Label300.Caption:=Sobo19.Edit102.Text;
  Label301.Caption:=Sobo19.Edit103.Text;
//SeachClick(Sobo19.Edit100.Text,Sobo19.Edit101.Text);
  SeachClick('','');
  Sobo19.Free;
  if Label300.Caption='' then Sobo19.Edit102.Text:='';
end;

procedure TSobo12.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo12:=nil;
  nSqry.AfterScroll:=nil;
  mSqry.AfterScroll:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo12.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo12.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_12_01(Self);
  end;
end;

procedure TSobo12.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo12.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX0(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo12.Button013Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX0(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo12.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('12-01');
end;

procedure TSobo12.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('12-02');
end;

procedure TSobo12.Button016Click(Sender: TObject);
begin
  Tong40.print_12_01(Self);
end;

procedure TSobo12.Button017Click(Sender: TObject);
begin
  Tong40.print_12_02(Self);
end;

procedure TSobo12.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo12.Button022Click(Sender: TObject);
begin
  nSqry.SaveToFile('.\Data\G2_Ggwo.cds');
end;

procedure TSobo12.Button023Click(Sender: TObject);
begin
  Edit101.Text := nSqry.FieldByName('Sname').AsString;
  Edit102.Text := nSqry.FieldByName('Jubun').AsString;
  Edit103.Text := nSqry.FieldByName('Gcode').AsString;
  Edit104.Text := nSqry.FieldByName('Ocode').AsString;
  Edit105.Text := nSqry.FieldByName('Gname').AsString;
  Edit106.Text := nSqry.FieldByName('Gposa').AsString;
  Edit107.Text := nSqry.FieldByName('Gnumb').AsString;
  Edit108.Text := nSqry.FieldByName('Guper').AsString;
  Edit109.Text := nSqry.FieldByName('Gjomo').AsString;
  Edit110.Text := nSqry.FieldByName('Gpper').AsString;
  Edit111.Text := nSqry.FieldByName('Gpost').AsString;
  Edit112.Text := nSqry.FieldByName('Gtel1').AsString;
  Edit113.Text := nSqry.FieldByName('Gtel2').AsString;
  Edit114.Text := nSqry.FieldByName('Gfax1').AsString;
  Edit115.Text := nSqry.FieldByName('Gfax2').AsString;
  Edit116.Text := nSqry.FieldByName('Gadd1').AsString;
  Edit117.Text := nSqry.FieldByName('Gadd2').AsString;
  Edit118.Value:= nSqry.FieldByName('Grat1').AsFloat;
  Edit119.Value:= nSqry.FieldByName('Grat2').AsFloat;
  Edit120.Value:= nSqry.FieldByName('Grat3').AsFloat;
  Edit121.Value:= nSqry.FieldByName('Grat4').AsFloat;
  Edit122.Value:= nSqry.FieldByName('Grat5').AsFloat;
  Edit123.Value:= nSqry.FieldByName('Grat6').AsFloat;
  Edit124.Value:= nSqry.FieldByName('Gqut1').AsFloat;
  Edit125.Text := nSqry.FieldByName('Gbigo').AsString;
  Edit126.Text := nSqry.FieldByName('Name1').AsString;
  Edit127.Text := nSqry.FieldByName('Name2').AsString;
  Edit129.Text := nSqry.FieldByName('Email').AsString;
  if nSqry.FieldByName('Yesno').AsString='True' then
  CheckBox1.Checked:=True else
  CheckBox1.Checked:=False;
  if nSqry.FieldByName('Grat9').AsString='1' then
  CheckBox2.Checked:=True else
  CheckBox2.Checked:=False;
end;

procedure TSobo12.Button024Click(Sender: TObject);
begin
  Edit201.Text := mSqry.FieldByName('Gcode').AsString;
  Edit202.Text := mSqry.FieldByName('Gname').AsString;
end;

procedure TSobo12.Button101Click(Sender: TObject);
begin
  if nSqry.State=dsInsert Then Button102Click(Self);
  nSqry.Insert;
  nSqry.FieldByName('Gcode').AsString := '';
  Edit101.SetFocus;
  Edit103.Enabled:=True;
end;

procedure TSobo12.Button102Click(Sender: TObject);
var MeDlg: Integer;
    St1,St2,Sq1,Sq2,Sq3: String;
begin
MeDlg := MessageDlg('저장 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin
  if Edit103.Enabled=True Then Edit101Exit(Self);
  if nSqry.State=dsInsert Then begin

    Sqlon := 'INSERT INTO G2_Ggwo '+
    '( Gubun, Jubun, Gcode, Ocode, Gname, Gposa, '+
    '  Gnumb, Guper, Gjomo, Gtel1, Gtel2, Gfax1, '+
    '  Gfax2, Gpost, Gadd1, Gadd2, Gpper, Gbigo, '+
    '  Yesno, Name1, Name2, Email, Hcode, '+
    '  Grat1, Grat2, Grat3, Grat4, Grat5, Grat6, '+
    '  Grat7, Grat8, Grat9, Gqut1 ) VALUES ';
    Sq1 :=
    '(''@Gubun'',''@Jubun'',''@Gcode'',''@Ocode'',''@Gname'',''@Gposa'', '+
    ' ''@Gnumb'',''@Guper'',''@Gjomo'',''@Gtel1'',''@Gtel2'',''@Gfax1'', ';
    Sq2 :=
    ' ''@Gfax2'',''@Gpost'',''@Gadd1'',''@Gadd2'',''@Gpper'',''@Gbigo'', '+
    ' ''@Yesno'',''@Name1'',''@Name2'',''@Email'',''@Hcode'', ';
    Sq3 :=
    '   @Grat1  ,  @Grat2  ,  @Grat3  ,  @Grat4  ,  @Grat5  ,  @Grat6  , '+
    '   @Grat7  ,  @Grat8  ,  @Grat9  ,  @Gqut1  )';

    St1 := 'Select Gcode From G2_Gbun Where '+D_Select+'Gname=''@Gname'' and Hcode=''@Hcode'' ';
    Translate(St1, '@Gname', Edit101.Text);
    Translate(St1, '@Hcode', '');
    St2 := Base10.Seek_Name(St1);

    Translate(Sq1, '@Gubun', St2);
    Translate(Sq1, '@Jubun', Edit102.Text);
    Translate(Sq1, '@Gcode', Edit103.Text);
    Translate(Sq1, '@Ocode', Edit104.Text);
    Translate(Sq1, '@Gname', Edit105.Text);
    Translate(Sq1, '@Gposa', Edit106.Text);
    Translate(Sq1, '@Gnumb', Edit107.Text);
    Translate(Sq1, '@Guper', Edit108.Text);
    Translate(Sq1, '@Gjomo', Edit109.Text);
    Translate(Sq1, '@Gtel1', Edit112.Text);
    Translate(Sq1, '@Gtel2', Edit113.Text);
    Translate(Sq1, '@Gfax1', Edit114.Text);
    Translate(Sq2, '@Gfax2', Edit115.Text);
    Translate(Sq2, '@Gpost', Edit111.Text);
    Translate(Sq2, '@Gadd1', Edit116.Text);
    Translate(Sq2, '@Gadd2', Edit117.Text);
    Translate(Sq2, '@Gpper', Edit110.Text);
    Translate(Sq2, '@Gbigo', Edit125.Text);
    Translate(Sq2, '@Name1', Edit126.Text);
    Translate(Sq2, '@Name2', Edit127.Text);
    Translate(Sq2, '@Email', Edit129.Text);
    Translate(Sq2, '@Hcode', Label300.Caption);

    TransAuto(Sq3, '@Grat1', FloatToStr(Edit118.Value));
    TransAuto(Sq3, '@Grat2', FloatToStr(Edit119.Value));
    TransAuto(Sq3, '@Grat3', FloatToStr(Edit120.Value));
    TransAuto(Sq3, '@Grat4', FloatToStr(Edit121.Value));
    TransAuto(Sq3, '@Grat5', FloatToStr(Edit122.Value));
    TransAuto(Sq3, '@Grat6', FloatToStr(Edit123.Value));
    TransAuto(Sq3, '@Grat7', '0');
    TransAuto(Sq3, '@Grat8', '0');
    TransAuto(Sq3, '@Gqut1', FloatToStr(Edit124.Value));

    if CheckBox1.Checked=True then
    Translate(Sq2, '@Yesno', 'True') else
    Translate(Sq2, '@Yesno', 'False');

    if CheckBox2.Checked=True then
    TransAuto(Sq3, '@Grat9', '1') else
    TransAuto(Sq3, '@Grat9', '0');

    Sqlen:=Sqlon+Sq1+Sq2+Sq3;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Insert);
      nSqry.Cancel;
      DBGrid101.SetFocus;
      Edit103.Enabled:=False;
      Exit;
    end;

    Base10.InSert_ID(nSqry,'G2_GGWO_ID_GEN');
  end else begin

    Sq1 := 'UPDATE G2_Ggwo SET '+
    'Gubun=''@Gubun'',Jubun=''@Jubun'',Gcode=''@Gcode'',Ocode=''@Ocode'', '+
    'Gname=''@Gname'',Gposa=''@Gposa'',Gnumb=''@Gnumb'',Guper=''@Guper'', '+
    'Gjomo=''@Gjomo'',Gtel1=''@Gtel1'',Gtel2=''@Gtel2'',Gfax1=''@Gfax1'', ';
    Sq2 :=
    'Gfax2=''@Gfax2'',Gpost=''@Gpost'',Gadd1=''@Gadd1'',Gadd2=''@Gadd2'', '+
    'Gpper=''@Gpper'',Gbigo=''@Gbigo'',Grat1=  @Grat1  ,Grat2=  @Grat2  , '+
    'Yesno=''@Yesno'',Name1=''@Name1'',Name2=''@Name2'',Email=''@Email'', ';
    Sq3 :=
    'Grat3=  @Grat3  ,Grat4=  @Grat4  ,Grat5=  @Grat5  ,Grat6=  @Grat6  , '+
    'Grat7=  @Grat7  ,Grat8=  @Grat8  ,Grat9=  @Grat9  ,Gqut1=  @Gqut1    '+
    'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';

    St1 := 'Select Gcode From G2_Gbun Where '+D_Select+'Gname=''@Gname'' and Hcode=''@Hcode'' ';
    Translate(St1, '@Gname', Edit101.Text);
    Translate(St1, '@Hcode', '');
    St2 := Base10.Seek_Name(St1);

    Translate(Sq1, '@Gubun', St2);
    Translate(Sq1, '@Jubun', Edit102.Text);
    Translate(Sq1, '@Gcode', Edit103.Text);
    Translate(Sq1, '@Ocode', Edit104.Text);
    Translate(Sq1, '@Gname', Edit105.Text);
    Translate(Sq1, '@Gposa', Edit106.Text);
    Translate(Sq1, '@Gnumb', Edit107.Text);
    Translate(Sq1, '@Guper', Edit108.Text);
    Translate(Sq1, '@Gjomo', Edit109.Text);
    Translate(Sq1, '@Gtel1', Edit112.Text);
    Translate(Sq1, '@Gtel2', Edit113.Text);
    Translate(Sq1, '@Gfax1', Edit114.Text);
    Translate(Sq2, '@Gfax2', Edit115.Text);
    Translate(Sq2, '@Gpost', Edit111.Text);
    Translate(Sq2, '@Gadd1', Edit116.Text);
    Translate(Sq2, '@Gadd2', Edit117.Text);
    Translate(Sq2, '@Gpper', Edit110.Text);
    Translate(Sq2, '@Gbigo', Edit125.Text);
    TransAuto(Sq2, '@Grat1', FloatToStr(Edit118.Value));
    TransAuto(Sq2, '@Grat2', FloatToStr(Edit119.Value));
    Translate(Sq2, '@Name1', Edit126.Text);
    Translate(Sq2, '@Name2', Edit127.Text);
    Translate(Sq2, '@Email', Edit129.Text);
    Translate(Sq3, '@Hcode', Label300.Caption);

    TransAuto(Sq3, '@Grat3', FloatToStr(Edit120.Value));
    TransAuto(Sq3, '@Grat4', FloatToStr(Edit121.Value));
    TransAuto(Sq3, '@Grat5', FloatToStr(Edit122.Value));
    TransAuto(Sq3, '@Grat6', FloatToStr(Edit123.Value));
    TransAuto(Sq3, '@Grat7', '0');
    TransAuto(Sq3, '@Grat8', '0');
    TransAuto(Sq3, '@Gqut1', FloatToStr(Edit124.Value));
    Translate(Sq3, '@Gcode', Edit103.Text);

    if CheckBox1.Checked=True then
    Translate(Sq2, '@Yesno', 'True') else
    Translate(Sq2, '@Yesno', 'False');

    if CheckBox2.Checked=True then
    TransAuto(Sq3, '@Grat9', '1') else
    TransAuto(Sq3, '@Grat9', '0');

    Sqlen:=Sq1+Sq2+Sq3;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Update);
      nSqry.Cancel;
      DBGrid101.SetFocus;
      Edit103.Enabled:=False;
      Exit;
    end;  

  end;

  St1 := 'Select Gcode From G2_Gbun Where '+D_Select+'Gname=''@Gname'' and Hcode=''@Hcode'' ';
  Translate(St1, '@Gname', Edit101.Text);
  Translate(St1, '@Hcode', '');
  St2 := Base10.Seek_Name(St1);

  nSqry.Edit;
  nSqry.FieldByName('Gubun').AsString := St2;
  nSqry.FieldByName('Sname').AsString := Edit101.Text;
  nSqry.FieldByName('Jubun').AsString := Edit102.Text;
  nSqry.FieldByName('Gcode').AsString := Edit103.Text;
  nSqry.FieldByName('Ocode').AsString := Edit104.Text;
  nSqry.FieldByName('Gname').AsString := Edit105.Text;
  nSqry.FieldByName('Gposa').AsString := Edit106.Text;
  nSqry.FieldByName('Gnumb').AsString := Edit107.Text;
  nSqry.FieldByName('Guper').AsString := Edit108.Text;
  nSqry.FieldByName('Gjomo').AsString := Edit109.Text;
  nSqry.FieldByName('Gpper').AsString := Edit110.Text;
  nSqry.FieldByName('Gpost').AsString := Edit111.Text;
  nSqry.FieldByName('Gtel1').AsString := Edit112.Text;
  nSqry.FieldByName('Gtel2').AsString := Edit113.Text;
  nSqry.FieldByName('Gtels').AsString := Edit112.Text+'-'+Edit113.Text;
  nSqry.FieldByName('Gfax1').AsString := Edit114.Text;
  nSqry.FieldByName('Gfax2').AsString := Edit115.Text;
  nSqry.FieldByName('Gfaxs').AsString := Edit114.Text+'-'+Edit115.Text;
  nSqry.FieldByName('Gadd1').AsString := Edit116.Text;
  nSqry.FieldByName('Gadd2').AsString := Edit117.Text;
  nSqry.FieldByName('Gadds').AsString := Edit116.Text+' '+Edit117.Text;
  nSqry.FieldByName('Grat1').Value    := Edit118.Text;
  nSqry.FieldByName('Grat2').Value    := Edit119.Text;
  nSqry.FieldByName('Grat3').Value    := Edit120.Text;
  nSqry.FieldByName('Grat4').Value    := Edit121.Text;
  nSqry.FieldByName('Grat5').Value    := Edit122.Text;
  nSqry.FieldByName('Grat6').Value    := Edit123.Text;
  nSqry.FieldByName('Gqut1').Value    := Edit124.Text;
  nSqry.FieldByName('Gbigo').AsString := Edit125.Text;
  nSqry.FieldByName('Name1').AsString := Edit126.Text;
  nSqry.FieldByName('Name2').AsString := Edit127.Text;
  nSqry.FieldByName('Email').AsString := Edit129.Text;

  if CheckBox1.Checked=True then
  nSqry.FieldByName('Yesno').AsString := 'True' else
  nSqry.FieldByName('Yesno').AsString := 'False';

  if CheckBox2.Checked=True then
  nSqry.FieldByName('Grat9').AsString := '1' else
  nSqry.FieldByName('Grat9').AsString := '0';

  nSqry.Post;
  DBGrid101.SetFocus;
  Edit103.Enabled:=False;
end;
mrNo: begin
  nSqry.Cancel;
  DBGrid101.SetFocus;
  Edit103.Enabled:=False;
end; end;
end;

procedure TSobo12.Button103Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin

  Sqlen := 'DELETE FROM G2_Ggwo WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
  Translate(Sqlen, '@Gcode', Edit103.Text);
  Translate(Sqlen, '@Hcode', Label300.Caption);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then begin
    ShowMessage(E_Delete);
    DBGrid101.SetFocus;
    Exit;
  end;  

  if nSqry.IsEmpty=False Then nSqry.Delete;
  DBGrid101.SetFocus;
  Edit103.Enabled:=False;
end; end;
end;

procedure TSobo12.Button104Click(Sender: TObject);
begin
  Cpost:='12';
  Subu00.Post_Show(Self);
{ if Edit111.Text='' Then begin
  SelectNext(ActiveControl as TWinControl, True, True); Exit; end;
  Seak40.Edit1.Text:=Edit111.Text;
  Seak40.FilterTing(Edit111.Text);
  if Seak40.Query1.IsEmpty=True Then Exit;
  if Seak40.Query1.RecordCount=1 Then begin
     SelectNext(ActiveControl as TWinControl, True, True);
     Edit112.Text:=Seak40.Query1Dddd.Value;
     Edit114.Text:=Seak40.Query1Dddd.Value;
     Edit111.Text:=Seak40.Query1Post.Value;
     Edit116.Text:=Copy(Seak40.Query1Addr.Value,1,44);
  end else
  if Seak40.ShowModal=mrOK Then begin
     SelectNext(ActiveControl as TWinControl, True, True);
     Edit112.Text:=Seak40.Query1Dddd.Value;
     Edit114.Text:=Seak40.Query1Dddd.Value;
     Edit111.Text:=Seak40.Query1Post.Value;
     Edit116.Text:=Copy(Seak40.Query1Addr.Value,1,44);
  end; }
end;

procedure TSobo12.Button201Click(Sender: TObject);
begin
  mSqry.Insert;
  mSqry.FieldByName('Gcode').AsString := '';
  Edit201.SetFocus;
end;

procedure TSobo12.Button202Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('저장 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin
  if mSqry.State=dsInsert Then begin

    Sqlen := 'INSERT INTO G2_Gbun ( Gcode, Gname, Hcode ) VALUES '+
             '(''@Gcode'',''@Gname'',''@Hcode'')';

    Translate(Sqlen, '@Gcode', Edit201.Text);
    Translate(Sqlen, '@Gname', Edit202.Text);
    Translate(Sqlen, '@Hcode', '');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Insert);
      mSqry.Cancel;
      DBGrid201.SetFocus;
      Exit;
    end;

    Base10.InSert_ID(mSqry,'G2_GBUN_ID_GEN');
  end else begin

    Sqlen := 'UPDATE G2_Gbun SET Gcode=''@Gcode'',Gname=''@Gname'' '+
             'WHERE ID=@ID and Hcode=''@Hcode'' ';

    Translate(Sqlen, '@Gcode', Edit201.Text);
    Translate(Sqlen, '@Gname', Edit202.Text);
    Translate(Sqlen, '@Hcode', '');
    TransAuto(Sqlen, '@ID', mSqry.FieldByName('ID').AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Update);
      mSqry.Cancel;
      DBGrid201.SetFocus;
      Exit;
    end;

  end;
  mSqry.Edit;
  mSqry.FieldByName('Gcode').AsString := Edit201.Text;
  mSqry.FieldByName('Gname').AsString := Edit202.Text;
  mSqry.Post;
  DBGrid201.SetFocus;
end;
mrNo: begin
  mSqry.Cancel;
  DBGrid201.SetFocus;
end; end;
end;

procedure TSobo12.Button203Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin

  Sqlen := 'DELETE FROM G2_Gbun WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
  Translate(Sqlen, '@Gcode', Edit201.Text);
  Translate(Sqlen, '@Hcode', '');
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then begin
    ShowMessage(E_Delete);
    DBGrid201.SetFocus;
    Exit;
  end;  

  if mSqry.IsEmpty=False Then mSqry.Delete;
  DBGrid201.SetFocus;
end; end;
end;

procedure TSobo12.Edit101Exit(Sender: TObject);
var St1,St2: String;
begin
  if Edit103.Text='' Then begin
    ShowMessage('코드를 입력하세요.');
    Edit103.SetFocus; Exit;
  end else begin
    St1 := 'Select Gcode From G2_Ggwo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(St1, '@Gcode', Edit103.Text);
    Translate(St1, '@Hcode', Label300.Caption);
    St2 := Base10.Seek_Name(St1);

    if St2<>'' Then begin
    ShowMessage('코드가 이미 등록되어있습니다. 다시 입력하세요.');
    Edit103.SetFocus; Exit;
    end;
  end;
end;

procedure TSobo12.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=06))or
    ((Edit103.Focused=True)and(Edit103.SelStart=05)and(Length(Trim(Edit103.Text))=05))or
    ((Edit104.Focused=True)and(Edit104.SelStart=05)and(Length(Trim(Edit104.Text))=05))or
    ((Edit105.Focused=True)and(Edit105.SelStart=50)and(Length(Trim(Edit105.Text))=50))or
    ((Edit106.Focused=True)and(Edit106.SelStart=30)and(Length(Trim(Edit106.Text))=30))or
    ((Edit107.Focused=True)and(Edit107.SelStart=12)and(Length(Trim(Edit107.Text))=12))or
    ((Edit108.Focused=True)and(Edit108.SelStart=30)and(Length(Trim(Edit108.Text))=30))or
    ((Edit109.Focused=True)and(Edit109.SelStart=30)and(Length(Trim(Edit109.Text))=30))or
    ((Edit110.Focused=True)and(Edit110.SelStart=20)and(Length(Trim(Edit110.Text))=20))or
    ((Edit112.Focused=True)and(Edit112.SelStart=04)and(Length(Trim(Edit112.Text))=04))or
    ((Edit113.Focused=True)and(Edit113.SelStart=20)and(Length(Trim(Edit113.Text))=20))or
    ((Edit114.Focused=True)and(Edit114.SelStart=04)and(Length(Trim(Edit114.Text))=04))or
    ((Edit115.Focused=True)and(Edit115.SelStart=20)and(Length(Trim(Edit115.Text))=20))or
    ((Edit116.Focused=True)and(Edit116.SelStart=90)and(Length(Trim(Edit116.Text))=90))or
    ((Edit117.Focused=True)and(Edit117.SelStart=90)and(Length(Trim(Edit117.Text))=90))or
    ((Edit118.Focused=True)and(Edit118.SelStart=03)and(Length(Trim(Edit118.Text))=03))or
    ((Edit119.Focused=True)and(Edit119.SelStart=03)and(Length(Trim(Edit119.Text))=03))or
    ((Edit120.Focused=True)and(Edit120.SelStart=03)and(Length(Trim(Edit120.Text))=03))or
    ((Edit121.Focused=True)and(Edit121.SelStart=03)and(Length(Trim(Edit121.Text))=03))or
    ((Edit122.Focused=True)and(Edit122.SelStart=03)and(Length(Trim(Edit122.Text))=03))or
    ((Edit123.Focused=True)and(Edit123.SelStart=03)and(Length(Trim(Edit123.Text))=03))or
    ((Edit124.Focused=True)and(Edit124.SelStart=04)and(Length(Trim(Edit124.Text))=04))or
    ((Edit125.Focused=True)and(Edit125.SelStart=50)and(Length(Trim(Edit125.Text))=50))or
    ((Edit126.Focused=True)and(Edit126.SelStart=50)and(Length(Trim(Edit126.Text))=50))or
    ((Edit127.Focused=True)and(Edit127.SelStart=50)and(Length(Trim(Edit127.Text))=50))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit111.Focused=True)and(Edit111.SelStart=07)and(Length(Trim(Edit111.Text))=07))Then begin
      Button104Click(Self);
  end;
end;

procedure TSobo12.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo12.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo12.Edit102KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Button102Click(Self);
    DBGrid101.SetFocus;
  end;
end;

procedure TSobo12.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then begin
    Button102Click(Self);
    DBGrid101.SetFocus;
  end;
end;

procedure TSobo12.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo12.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo12.Edit112KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    DGrid: TDBGrid;
    Edits: TFlatComboBox;
begin
  Hands:=Edit101.Handle;
  Edits:=Edit101;
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

procedure TSobo12.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit101;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo12.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Button202Click(Self);
    DBGrid201.SetFocus;
  end;
end;

procedure TSobo12.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then begin
    Button202Click(Self);
    DBGrid201.SetFocus;
  end;
end;

procedure TSobo12.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  if Edit111.Focused=True Then
     Button104Click(Self);
end;

procedure TSobo12.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo12.DBGrid101DblClick(Sender: TObject);
begin
  nSqry.Edit;
  if nSqry.FieldByName('Scode').AsString<>'' Then
     nSqry.FieldByName('Scode').AsString:='' else
     nSqry.FieldByName('Scode').AsString:='O';
  nSqry.Post;

  Sqlen := 'UPDATE G2_Ggwo SET Scode=''@Scode'' '+
           'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
  Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
  Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
  Translate(Sqlen, '@Hcode', Label300.Caption);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
end;

procedure TSobo12.DBGrid101Enter(Sender: TObject);
begin
  if nSqry.State=dsInsert Then Button102Click(Self);
end;

procedure TSobo12.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo12.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_RETURN Then Edit101.SetFocus;
  if Key=VK_INSERT Then Button101Click(Self);
  if Key=VK_DELETE Then Button103Click(Self);
  end;
end;

procedure TSobo12.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo12.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_RETURN Then Edit201.SetFocus;
  if Key=VK_INSERT Then Button201Click(Self);
  if Key=VK_DELETE Then Button203Click(Self);
  end;
end;

procedure TSobo12.DBGrid101Exit(Sender: TObject);
begin
//
end;

procedure TSobo12.DBGrid201Exit(Sender: TObject);
var St1: String;
begin
  Edit101.Items.Clear;
  St1:='Hcode'+'='+#39+''+#39;
  Sqlen := 'Select * From G2_Gbun Where '+D_Select+St1+' Order By Gcode';
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    List1:=0;
    T00:=Base10.Socket.ClientData('1');
    while List1 < T00-1 do begin
      List1:=List1+1;
      Edit101.Items.Add(Base10.Socket.GetData(List1, 3));
    end;
  end;
end;

procedure TSobo12.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo12.DBGrid201TitleClick(Column: TColumn);
begin
//
end;

procedure TSobo12.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo12.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo12.SeachClick(Str1,Str2: String);
var St1: String;
begin
  Tong40.Show;
  Tong40.Update;

  T00:=0;
  nSqry:=Base10.T1_Sub21;
  mSqry:=Base10.T1_Sub22;

  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);

  St1:=Str1+' Like '+#39+'%'+Str2+'%'+#39;

  if Lower='1' then
  St1:='Lower('+Str1+') like '+'Lower('+#39+'%'+Str2+'%'+#39+')';

  if Str2='' then
  St1:=Str1+' = '+#39+''+#39;

  if Str1='' then
  St1:='Gcode'+' Like '+#39+'%'+''+'%'+#39;

  St1:='Hcode'+'='+#39+Label300.Caption+#39+' and '+St1;

  Sqlen := 'Select * From G2_Ggwo Where '+D_Select+St1+' Order By Gcode';
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  St1:='Hcode'+'='+#39+''+#39;

  Sqlen := 'Select * From G2_Gbun Where '+D_Select+St1+' Order By Gcode';
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(mSqry)
  else ShowMessage(E_Open);

  mSqry.First;
  Edit101.Items.Clear;
  While mSqry.EOF=False do begin
    Edit101.Items.Add(mSqry.FieldByName('Gname').AsString);
    mSqry.Next;
  end;

  nSqry.First;
  Bmark:=nSqry.GetBookmark; nSqry.DisableControls;
  While nSqry.EOF=False do begin

    St1:=nSqry.FieldByName('Gubun').Value;
    if mSqry.Locate('Gcode',St1,[loCaseInsensitive])=True then
    St1:=mSqry.FieldByName('Gname').Value;

    nSqry.Edit;
    nSqry.FieldByName('Sname').Value:=St1;
    nSqry.FieldByName('Gtels').Value:=nSqry.FieldByName('Gtel1').Value+
                                  '-'+nSqry.FieldByName('Gtel2').Value;
    nSqry.FieldByName('Gfaxs').Value:=nSqry.FieldByName('Gfax1').Value+
                                  '-'+nSqry.FieldByName('Gfax2').Value;
    nSqry.FieldByName('Gadds').Value:=nSqry.FieldByName('Gadd1').Value+
                                  ' '+nSqry.FieldByName('Gadd2').Value;
    nSqry.Post;
    nSqry.Next;
  end;
  nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;

  if Base10.Database.Database='book_07_db' then
  nSqry.IndexName := 'IDX'+'GNAME'+'DOWN';
  mSqry.First;
  nSqry.First;
  mSqry.AfterScroll:=Base10.T1_Sub22AfterScroll;
  nSqry.AfterScroll:=Base10.T1_Sub21AfterScroll;
  Button023Click(Self);
  Button024Click(Self);
  ProgressBar1.Position:=0;

  Tong40.Hide;
{ Tong40.Free; }
end;

end.
