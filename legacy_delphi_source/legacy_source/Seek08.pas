unit Seek08;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit;

type
  TSeek80 = class(TForm)
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
    Query1GPOSA: TStringField;
    Query1GPHON: TStringField;
    Query1GUBUN: TStringField;
    Query1GTELS: TStringField;
    Query1GTEL1: TStringField;
    Query1TEL2: TStringField;
    Query1GDATE: TStringField;
    Query1GSSUM: TFloatField;
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
  Seek80: TSeek80;

implementation

{$R *.DFM}

uses Base01, TcpLib;

procedure TSeek80.FilterSing(Str,Sth:String);
begin
//
end;

procedure TSeek80.FilterTing(Str,Sth:String);
var St1,St2: String;
begin
  Base10.OpenExit(Query1);
  Base10.OpenShow(Query1);

{ if Str='' Then Exit; }
  Edit3.Text:=Sth;

  St1:='Gcode'+' like '+#39+Str+'%'+#39+' Or '+
       'Gname'+' like '+#39+Str+'%'+#39;
  if Lower='1' then
  St1:='Lower(Gcode)'+' like '+'Lower('+#39+'%'+Str+'%'+#39+')'+' Or '+
       'Lower(Gname)'+' like '+'Lower('+#39+'%'+Str+'%'+#39+')';
//St1:='Hcode'+'='+#39+Sth+#39+' and '+'('+St1+')';

  if Str < '9____' Then
  St2:=' Order By Gcode' else
  St2:=' Order By Gname';
  St1:=St1+St2;

  Sqlen := 'Select Gcode,Gname,Gphon,Gtel1,Gtel2 From G8_Ggeo Where '+D_Select+St1;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Query1)
  else ShowMessage(E_Open);
  Query1.First;
end;

procedure TSeek80.FilterSeek(Str,Sth:String);
begin
//
end;

procedure TSeek80.Edit1KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  FilterTing(Edit1.Text,Edit3.Text);
end;

procedure TSeek80.Button001Click(Sender: TObject);
begin
  FilterTing(Edit1.Text,Edit3.Text);
end;

procedure TSeek80.DBGrid101DblClick(Sender: TObject);
begin
  ModalResult:=mrOK;
end;

procedure TSeek80.Edit1Enter(Sender: TObject);
begin
  FilterTing(Edit1.Text,Edit3.Text);
end;

procedure TSeek80.FormShow(Sender: TObject);
begin
  DBGrid101.SetFocus;
end;

end.
