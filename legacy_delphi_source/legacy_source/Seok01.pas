unit Seok01;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Buttons, Mask, TFlatButtonUnit, TFlatNumberUnit,
  TFlatMaskEditUnit, TFlatEditUnit, TFlatPanelUnit, Grids, DBGrids, Db,
  DBClient;

type
  TSeok10 = class(TForm)
    Panel001: TFlatPanel;
    Button101: TFlatButton;
    Button102: TFlatButton;
    BitBtn101: TBitBtn;
    BitBtn102: TBitBtn;
    Panel002: TFlatPanel;
    DBGrid101: TDBGrid;
    DataSource1: TDataSource;
    Query1: TClientDataSet;
    Query1ID: TFloatField;
    Query1SCODE: TStringField;
    Query1GCODE: TStringField;
    Query1GNAME: TStringField;
    Query1ONAME: TStringField;
    Query1GDATE: TStringField;
    Query1JUBUN: TStringField;
    Query1GBIGO: TStringField;
    Query1GNUM1: TStringField;
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit111KeyPress(Sender: TObject; var Key: Char);
    procedure Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure BitBtn101Click(Sender: TObject);
    procedure BitBtn102Click(Sender: TObject);
    procedure Query1NewRecord(DataSet: TDataSet);
    procedure Query1BeforePost(DataSet: TDataSet);
    procedure Query1BeforeClose(DataSet: TDataSet);
    procedure Query1AfterDelete(DataSet: TDataSet);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seok10: TSeok10;

implementation

{$R *.DFM}

uses Base01, TcpLib, Subu11;

procedure TSeok10.FormShow(Sender: TObject);
var St1,St2: String;
begin
  Query1.BeforePost:=nil;
  Base10.OpenShow(Query1);

  if Copy(oSqry.FieldByName('Gcode').AsString,1,1)<>'9' then
  St1:='Scode'+'='+#39+'X'+#39+' and '+
       'Hcode'+'='+#39+''+#39+' and '+
       'Gcode'+'='+#39+oSqry.FieldByName('Gcode').AsString+#39 else
  St1:='Scode'+'='+#39+'X'+#39+' and '+
       'Hcode'+'='+#39+oSqry.FieldByName('Hcode').AsString+#39+' and '+
       'Gcode'+'='+#39+oSqry.FieldByName('Gcode').AsString+#39;
  St2:=' Order By Oname,Gname';

  Sqlen :='Select * From H2_Gbun Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Query1)
  else ShowMessage(E_Open);
  Query1.First;
  Query1.BeforePost:=Query1BeforePost;

  DBGrid101.SetFocus;
end;

procedure TSeok10.FormClose(Sender: TObject; var Action: TCloseAction);
begin
//
end;

procedure TSeok10.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSeok10.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSeok10.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSeok10.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSeok10.BitBtn101Click(Sender: TObject);
begin
  Query1.Append;
  DBGrid101.SetFocus;
end;

procedure TSeok10.BitBtn102Click(Sender: TObject);
begin
  Query1AfterDelete(Query1);
end;

procedure TSeok10.Query1NewRecord(DataSet: TDataSet);
begin
  Query1Scode.Value:='X';
  Query1Gcode.Value:=oSqry.FieldByName('Gcode').AsString;
end;

procedure TSeok10.Query1AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM H2_Gbun WHERE ID=@ID';
    TransAuto(Sqlen, '@ID',    Query1ID.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    Query1.Delete;

  end; end;

end;

procedure TSeok10.Query1BeforePost(DataSet: TDataSet);
begin

  if(Query1.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO H2_Gbun '+
    '(Hcode, Scode, Gcode, Gname, Oname, Gdate, Gnum1, Jubun, Gbigo) VALUES '+
    '(''@Hcode'',''@Scode'',''@Gcode'',''@Gname'',''@Oname'',''@Gdate'',''@Gnum1'',''@Jubun'',''@Gbigo'')';

    if Copy(oSqry.FieldByName('Gcode').AsString,1,1)<>'9' then
    Translate(Sqlen, '@Hcode', '') else
    Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Scode', Query1Scode.AsString);
    Translate(Sqlen, '@Gcode', Query1Gcode.AsString);
    Translate(Sqlen, '@Gname', Query1Gname.AsString);
    Translate(Sqlen, '@Oname', Query1Oname.AsString);
    Translate(Sqlen, '@Gdate', Query1Gdate.AsString);
    Translate(Sqlen, '@Gnum1', Query1Gnum1.AsString);
    Translate(Sqlen, '@Jubun', Query1Jubun.AsString);
    Translate(Sqlen, '@Gbigo', Query1Gbigo.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(Query1,'H2_GBUN_ID_GEN');

  end else begin

    Sqlen := 'UPDATE H2_Gbun SET '+
    'Hcode=''@Hcode'',Scode=''@Scode'',Gcode=''@Gcode'',Gname=''@Gname'', '+
    'Oname=''@Oname'',Gnum1=''@Gnum1'',Gdate=''@Gdate'',Jubun=''@Jubun'',Gbigo=''@Gbigo''  '+
    'WHERE ID=@ID ';

    if Copy(oSqry.FieldByName('Gcode').AsString,1,1)<>'9' then
    Translate(Sqlen, '@Hcode', '') else
    Translate(Sqlen, '@Hcode', oSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Scode', Query1Scode.AsString);
    Translate(Sqlen, '@Gcode', Query1Gcode.AsString);
    Translate(Sqlen, '@Gname', Query1Gname.AsString);
    Translate(Sqlen, '@Oname', Query1Oname.AsString);
    Translate(Sqlen, '@Gdate', Query1Gdate.AsString);
    Translate(Sqlen, '@Gnum1', Query1Gnum1.AsString);
    Translate(Sqlen, '@Jubun', Query1Jubun.AsString);
    Translate(Sqlen, '@Gbigo', Query1Gbigo.AsString);
    TransAuto(Sqlen, '@ID',    Query1ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TSeok10.Query1BeforeClose(DataSet: TDataSet);
begin
  With Query1 do
  if(State in dsEditModes)Then Post;
end;

end.
