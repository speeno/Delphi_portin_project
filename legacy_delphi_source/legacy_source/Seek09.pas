unit Seek09;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit;

type
  TSeek90 = class(TForm)
    Panel100: TFlatPanel;
    Panel201: TFlatPanel;
    Panel101: TFlatPanel;
    Edit1: TFlatEdit;
    Button001: TFlatSpeedButton;
    Button101: TFlatButton;
    Button102: TFlatButton;
    BitBtn101: TBitBtn;
    BitBtn102: TBitBtn;
    DBGrid101: TDBGrid;
    DataSource1: TDataSource;
    Query1: TClientDataSet;
    Query1ID: TFloatField;
    Query1GCODE: TStringField;
    Query1GNAME: TStringField;
    Query1GUBUN: TStringField;
    Edit3: TFlatEdit;
    procedure FilterSing(Str,Sth:String);
    procedure FilterTing(Str,Sth:String);
    procedure FilterSeek(Str,Sth:String);
    procedure Edit1KeyPress(Sender: TObject; var Key: Char);
    procedure Button001Click(Sender: TObject);
    procedure DBGrid101DblClick(Sender: TObject);
    procedure Edit1Enter(Sender: TObject);
    procedure FormShow(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seek90: TSeek90;

implementation

{$R *.DFM}

uses Base01, TcpLib;

procedure TSeek90.FilterSing(Str,Sth:String);
var St1,St2: String;
begin

  St1:='Gcode'+'='+#39+Str+#39;
  St2:=' Order By Gcode';
  St1:=St1+St2;

  Sqlen := 'Select * From T8_Gbun Where '+D_Select+St1;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Query1)
  else ShowMessage(E_Open);
  Query1.First;
end;

procedure TSeek90.FilterTing(Str,Sth:String);
var St1,St2: String;
begin
  Base10.OpenExit(Query1);
  Base10.OpenShow(Query1);

  St1:='Gcode'+' like '+#39+Str+'%'+#39+' Or '+
       'Gname'+' like '+#39+Str+'%'+#39;
  if Lower='1' then
  St1:='Lower(Gcode)'+' like '+'Lower('+#39+'%'+Str+'%'+#39+')'+' Or '+
       'Lower(Gname)'+' like '+'Lower('+#39+'%'+Str+'%'+#39+')';

  if Str < '9____' Then
  St2:=' Order By Gcode' else
  St2:=' Order By Gname';
  St1:=St1+St2;

  Sqlen := 'Select * From T8_Gbun Where '+D_Select+St1;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Query1)
  else ShowMessage(E_Open);
  Query1.First;
end;

procedure TSeek90.FilterSeek(Str,Sth:String);
var St1: String;
begin
//
end;

procedure TSeek90.Edit1KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  FilterTing(Edit1.Text,Edit3.Text);
end;

procedure TSeek90.Button001Click(Sender: TObject);
begin
  FilterTing(Edit1.Text,Edit3.Text);
end;

procedure TSeek90.DBGrid101DblClick(Sender: TObject);
begin
  ModalResult:=mrOK;
end;

procedure TSeek90.Edit1Enter(Sender: TObject);
begin
  FilterTing(Edit1.Text,Edit3.Text);
end;

procedure TSeek90.FormShow(Sender: TObject);
begin
  DBGrid101.SetFocus;
end;

end.
