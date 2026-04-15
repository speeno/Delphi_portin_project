unit Seak08;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit;

type
  TSeak80 = class(TForm)
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
    Query1SNAME: TStringField;
    Query1GUBUN: TStringField;
    Query1JUBUN: TStringField;
    Query1PUBUN: TStringField;
    Query1SCODE: TStringField;
    Query1GCODE: TStringField;
    Query1OCODE: TStringField;
    Query1GNAME: TStringField;
    Query1GPOSA: TStringField;
    Query1GTEL1: TStringField;
    Query1GTEL2: TStringField;
    Query1GADD1: TStringField;
    Query1GADD2: TStringField;
    procedure FilterSing(Str:String);
    procedure FilterTing(Str:String);
    procedure FilterSeek(Str:String);
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
  Seak80: TSeak80;

implementation

{$R *.DFM}

uses Base01, TcpLib;

procedure TSeak80.FilterSing(Str:String);
var St1,St2: String;
begin
  Base10.OpenExit(Query1);
  Base10.OpenShow(Query1);

  St1:='Ocode'+'='+#39+Str+#39;
  if S_Where2<>'' then
  St1:=St1+' and '+'('+S_Where2+')';

  St2:=' Order By Gcode';
  St1:=St1+St2;

  Sqlen := 'Select Gubun,Jubun,Gcode,Ocode,Gname,Gposa,'+
           'Gtel1,Gtel2,Gadd1,Gadd2 From G7_Ggeo Where '+D_Select+St1;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Query1)
  else ShowMessage(E_Open);
  Query1.First;
end;

procedure TSeak80.FilterTing(Str:String);
var St1,St2: String;
begin
  Base10.OpenExit(Query1);
  Base10.OpenShow(Query1);

  Str:=Trim(Str);
//if Str='' Then Exit;

  St1:='Gcode'+' like '+#39+Str+'%'+#39+' Or '+
       'Gname'+' like '+#39+Str+'%'+#39+' Or '+
       'Gposa'+' like '+#39+Str+'%'+#39;
  if Lower='1' then
  St1:='Lower(Gcode)'+' like '+'Lower('+#39+'%'+Str+'%'+#39+')'+' Or '+
       'Lower(Gname)'+' like '+'Lower('+#39+'%'+Str+'%'+#39+')'+' Or '+
       'Lower(Gposa)'+' like '+'Lower('+#39+'%'+Str+'%'+#39+')';
  if S_Where2<>'' then
  St1:='('+St1+')'+' and '+'('+S_Where2+')';

  if Str < '9____' Then
  St2:=' Order By Gcode' else
  St2:=' Order By Gname';
  St1:=St1+St2;

  Sqlen := 'Select Gubun,Jubun,Gcode,Ocode,Gname,Gposa,'+
           'Gtel1,Gtel2,Gadd1,Gadd2 From G7_Ggeo Where '+D_Select+St1;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Query1)
  else ShowMessage(E_Open);
  Query1.First;
end;

procedure TSeak80.FilterSeek(Str:String);
begin
//
end;

procedure TSeak80.Edit1KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  FilterTing(Edit1.Text);
end;

procedure TSeak80.Button001Click(Sender: TObject);
begin
  FilterTing(Edit1.Text);
end;

procedure TSeak80.DBGrid101DblClick(Sender: TObject);
begin
  ModalResult:=mrOK;
end;

procedure TSeak80.Edit1Enter(Sender: TObject);
begin
  FilterTing(Edit1.Text);
end;

procedure TSeak80.FormShow(Sender: TObject);
begin
  DBGrid101.SetFocus;
end;

end.
