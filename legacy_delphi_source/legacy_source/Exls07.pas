unit Exls07;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit, Mask,
  TFlatMaskEditUnit, DBGridEh, dxCore, dxButtons, ComCtrls,
  TFlatProgressBarUnit, Mylabel, CornerButton;

type
  TExls70 = class(TForm)
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    Panel001: TFlatPanel;
    dxButton1: TdxButton;
    Panel007: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar1: TProgressBar;
    Panel002: TFlatPanel;
    DBGrid101: TDBGridEh;
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Tm_Sms07: TClientDataSet;
    Tm_Sms07ID: TFloatField;
    Tm_Sms07HCODE: TStringField;
    Tm_Sms07HNAME: TStringField;
    Tm_Sms07NAME0: TStringField;
    procedure FormActivate(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Button101Click(Sender: TObject);
    procedure Button102Click(Sender: TObject);
    procedure Button303Click(Sender: TObject);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101DrawColumnCell(Sender: TObject; const Rect: TRect;
      DataCol: Integer; Column: TColumnEh; State: TGridDrawState);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure Tm_Sms07AfterPost(DataSet: TDataSet);
    procedure Tm_Sms07BeforePost(DataSet: TDataSet);
    procedure Tm_Sms07BeforeClose(DataSet: TDataSet);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Exls70: TExls70;

implementation

{$R *.DFM}

uses Base01, TcpLib, Tong04;

procedure TExls70.FormActivate(Sender: TObject);
begin
  nForm:='E7';
  uSqry:=Tm_Sms07;
end;

procedure TExls70.FormShow(Sender: TObject);
begin
//
end;

procedure TExls70.FormClose(Sender: TObject; var Action: TCloseAction);
begin
//Base10.OpenExit(uSqry);
end;

procedure TExls70.Button101Click(Sender: TObject);
var St1,St2: String;
begin

  Tong40.Show;
  Tong40.Update;

  Refresh;
  uSqry.BeforePost:=nil;
  Base10.OpenShow(uSqry);
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;

  St1:=St1+' and '+'Gcode'+'< '+#39+'x'+#39;

  St1:=St1+' and '+' Not ( Gname'+' like '+#39+'%Á¾·á%'+#39+' )';

  if S_Where2<>'' then
  St1:=St1+' and '+S_Where2;

  Sqlen := 'Select Gcode as Hcode, Gname as Hname From G7_Ggeo '+
           'Where '+D_Open+St1+' Order By Gcode';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(uSqry)
  else ShowMessage(E_Open);

  uSqry.First;
  ProgressBar1.Max:=uSqry.RecordCount;
  While uSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
    uSqry.Edit;

    Sqlen := 'Select Hcode,Name0 From Sm_Ggeo '+
             'Where '+D_Select+'Gubun=''@Gubun'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gubun', '01');
    Translate(Sqlen, '@Hcode', uSqry.FieldByName('Hcode').AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      uSqry.FieldByName('Hcode').AsString:=Base10.Socket.GetData(1, 1);
      uSqry.FieldByName('Name0').AsString:=Base10.Socket.GetData(1, 2);
    end;

    uSqry.Post;
    uSqry.Next;
  end;
  uSqry.First;

  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  uSqry.BeforePost:=Tm_Sms07BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TExls70.Button102Click(Sender: TObject);
begin
//
end;

procedure TExls70.Button303Click(Sender: TObject);
begin
//
end;

procedure TExls70.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
{ if uSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=0 Then begin
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end; }
end;

procedure TExls70.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if uSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    uSqry.Edit;
    uSqry.Post;
    Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),0,0);
    Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),KEYEVENTF_KEYUP,0);
  end;
  if sColumn=False Then begin
  { if uSqry.IsEmpty=False Then
    if Key=VK_ESCAPE Then Edit202.SetFocus; }
  end; end;
end;

procedure TExls70.DBGrid101DrawColumnCell(Sender: TObject;
  const Rect: TRect; DataCol: Integer; Column: TColumnEh;
  State: TGridDrawState);
begin
  if (Rect.Top = DBGrid101.CellRect(DBGrid101.Col,DBGrid101.Row).Top) and (not (gdFocused in State) or not DBGrid101.Focused) then
  DBGrid101.Canvas.Brush.Color := clAqua;
  DBGrid101.DefaultDrawColumnCell(Rect,DataCol,Column,State);
end;

procedure TExls70.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(uSqry.RecNo)+'/'+IntToStr(uSqry.RecordCount);
end;

procedure TExls70.Tm_Sms07AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TExls70.Tm_Sms07BeforePost(DataSet: TDataSet);
begin

    Sqlen :=
    'Select * From Sm_Ggeo Where '+D_Select+'Gubun=''@Gubun'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gubun', '01');
    Translate(Sqlen, '@Hcode', uSqry.FieldByname('Hcode').AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin

      Sqlen := 'UPDATE Sm_Ggeo SET '+
               'Name0=''@Name0'' '+
               'WHERE Gubun=''@Gubun'' and Hcode=''@Hcode'' ';

      Translate(Sqlen, '@Gubun', '01');
      Translate(Sqlen, '@Hcode', uSqry.FieldByname('Hcode').AsString);
      Translate(Sqlen, '@Name0', uSqry.FieldByname('Name0').AsString);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end else begin

      Sqlen := 'INSERT INTO Sm_Ggeo '+
      '(Gubun, Hcode, Name0) VALUES '+
      '(''@Gubun'',''@Hcode'',''@Name0'' )';

      Translate(Sqlen, '@Gubun', '01');
      Translate(Sqlen, '@Hcode', uSqry.FieldByname('Hcode').AsString);
      Translate(Sqlen, '@Name0', uSqry.FieldByname('Name0').AsString);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    //Base10.Update_ID(uSqry,'Tm_Sms07_ID_GEN');

    end;

end;

procedure TExls70.Tm_Sms07BeforeClose(DataSet: TDataSet);
begin
  With Tm_Sms07 do
  if(State in dsEditModes)Then Post;
end;

end.
