unit Subu48;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  TFlatRadioButtonUnit, Grids, DBGridEh, ExtCtrls, TFlatPanelUnit,
  TFlatButtonUnit, StdCtrls, TFlatComboBoxUnit, Db, DBClient, Mylabel,
  TFlatEditUnit, dxCore, dxButtons, ComCtrls, TFlatProgressBarUnit,
  CornerButton;

type
  TSobo48 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    T1_Sub81: TClientDataSet;
    T1_Sub81ID: TFloatField;
    T1_Sub81GDATE: TStringField;
    T1_Sub81GCODE: TStringField;
    T1_Sub81GNAME: TStringField;
    T1_Sub81GTELS: TStringField;
    T1_Sub81CODE1: TStringField;
    T1_Sub81CODE2: TStringField;
    T1_Sub81CODE3: TStringField;
    T1_Sub81CODE4: TStringField;
    T1_Sub81CODE5: TStringField;
    T1_Sub81GOQUT: TFloatField;
    T1_Sub81GSQUT: TFloatField;
    T1_Sub81GSSUM: TFloatField;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    DBGrid101: TDBGridEh;
    Panel004: TFlatPanel;
    RadioButton6: TFlatRadioButton;
    RadioButton7: TFlatRadioButton;
    Button300: TFlatButton;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    Panel007: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar1: TProgressBar;
    dxButton1: TdxButton;
    T1_Sub81CHEK1: TStringField;
    T1_Sub81CHEK2: TStringField;
    T1_Sub81CHEK3: TStringField;
    T1_Sub81CHEK4: TStringField;
    T1_Sub81CHEK5: TStringField;
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
    procedure Button201Click(Sender: TObject);
    procedure Button709Click(Sender: TObject);
    procedure Button200Click(Sender: TObject);
    procedure Button300Click(Sender: TObject);
    procedure Button701Click(Sender: TObject);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DBGrid101Columns2UpdateData(Sender: TObject;
      var Text: String; var Value: Variant; var UseText, Handled: Boolean);
    procedure DBGrid101Columns3UpdateData(Sender: TObject;
      var Text: String; var Value: Variant; var UseText, Handled: Boolean);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo48: TSobo48;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo48.FormActivate(Sender: TObject);
begin
  nForm:='48';
  nSqry:=T1_Sub81;
end;

procedure TSobo48.FormShow(Sender: TObject);
begin
//
end;

procedure TSobo48.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo48:=nil;
  Base10.OpenExit(nSqry);
end;

procedure TSobo48.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button012Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button014Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button015Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button016Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button017Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button101Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo48.Button709Click(Sender: TObject);
var St1,St2: String;
begin

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;

  if S_Where2<>'' then
  St1:=St1+' and '+S_Where2;

  Sqlen := 'Select Gcode,Gname,Chek3,Scode as Yesno From G7_Ggeo '+
           'Where '+D_Open+St1+' Order By Gcode';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  nSqry.First;
  While nSqry.EOF=False do begin
    nSqry.Edit;

    if nSqry.FieldByName('Chek3').AsString='True' then
    nSqry.FieldByName('Chek3').AsString:='O' else
    nSqry.FieldByName('Chek3').AsString:='N';

    if nSqry.FieldByName('Yesno').AsString='Y' then
    nSqry.FieldByName('Yesno').AsString:='O' else
    nSqry.FieldByName('Yesno').AsString:='N';

    nSqry.Post;
    nSqry.Next;
  end;
  nSqry.First;

  DBGrid101.SetFocus;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo48.Button200Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    Bmark:=nSqry.GetBookmark; nSqry.DisableControls;
    nSqry.First;
    While nSqry.EOF=False do begin
      nSqry.Edit;
      if RadioButton6.Checked=True Then
      nSqry.FieldByName('Yesno').AsString:='O';
      if RadioButton7.Checked=True Then
      nSqry.FieldByName('Yesno').AsString:='N';
      nSqry.Post;
      nSqry.Next;
    end;
    nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
    nSqry.First;
  end;
  DBGrid101.SetFocus;
end;

procedure TSobo48.Button300Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    Bmark:=nSqry.GetBookmark; nSqry.DisableControls;
    nSqry.First;
    While nSqry.EOF=False do begin

      Sqlen := 'UPDATE G7_Ggeo SET Scode=''@Yesno'' '+
      ' WHERE Gcode=''@Gcode'' ';

      if nSqry.FieldByName('Yesno').AsString='O' then
      Translate(Sqlen, '@Yesno', 'Y') else
      Translate(Sqlen, '@Yesno', 'N');
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

      nSqry.Next;
    end;

    nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
    nSqry.First;
    ShowMessage('저장완료');
  end;
  DBGrid101.SetFocus;
end;

procedure TSobo48.Button701Click(Sender: TObject);
begin
//
end;

procedure TSobo48.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo48.DBGrid101Columns2UpdateData(Sender: TObject;
  var Text: String; var Value: Variant; var UseText, Handled: Boolean);
begin
  if nSqry.Active=True Then begin
     Sqlen := 'UPDATE G7_Ggeo SET Chek3=''@Chek3'' '+
     ' WHERE Gcode=''@Gcode'' ';

     if nSqry.FieldByName('Chek3').AsString<>'O' then
     Translate(Sqlen, '@Chek3', 'True') else
     Translate(Sqlen, '@Chek3', 'False');
     Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
     Base10.Socket.RunSQL(Sqlen);
     Base10.Socket.BusyLoop;
     if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
  end;
end;

procedure TSobo48.DBGrid101Columns3UpdateData(Sender: TObject;
  var Text: String; var Value: Variant; var UseText, Handled: Boolean);
begin
  if nSqry.Active=True Then begin
     Sqlen := 'UPDATE G7_Ggeo SET Scode=''@Yesno'' '+
     ' WHERE Gcode=''@Gcode'' ';

     if nSqry.FieldByName('Yesno').AsString<>'O' then
     Translate(Sqlen, '@Yesno', 'Y') else
     Translate(Sqlen, '@Yesno', 'N');
     Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
     Base10.Socket.RunSQL(Sqlen);
     Base10.Socket.BusyLoop;
     if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
  end;
end;

end.
