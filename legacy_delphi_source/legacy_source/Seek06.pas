unit Seek06;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit;

type
  TSeek60 = class(TForm)
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
    Query1SCODE: TStringField;
    Query1GCODE: TStringField;
    Query1GNAME: TStringField;
    Query1ONAME: TStringField;
    Query1GDATE: TStringField;
    Query1CLAS1: TFloatField;
    Query1CLAS2: TFloatField;
    Query1CLAS3: TFloatField;
    Query1GSUM1: TFloatField;
    Query1GSUM2: TFloatField;
    Query1GSUM3: TFloatField;
    Query1HCODE: TStringField;
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
  Seek60: TSeek60;

implementation

{$R *.DFM}

uses Base01, TcpLib;

procedure TSeek60.FilterSing(Str,Sth:String);
var St1,St2: String;
begin
  Edit3.Text:=Sth;

  St1:='Gcode'+'='+#39+Str+#39;
  St1:='Hcode'+'='+#39+Sth+#39+' and '+'('+St1+')';

  St2:=' Order By Gcode';
  St1:=St1+St2;
  if Button001.Caption='2' Then begin

    Sqlen := 'Select * From H2_Gbun Where '+D_Select+St1;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(Query1)
    else ShowMessage(E_Open);
    Query1.First;

  end else begin

    Sqlen := 'Select * From H1_Gbun Where '+D_Select+St1;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(Query1)
    else ShowMessage(E_Open);
    Query1.First;

  end;
end;

procedure TSeek60.FilterTing(Str,Sth:String);
var St1,St2: String;
begin
  Base10.OpenExit(Query1);
  Base10.OpenShow(Query1);

  if Str='' Then Exit;
  Edit3.Text:=Sth;

  St1:='Gcode'+' like '+#39+Str+'%'+#39+' Or '+
       'Gname'+' like '+#39+Str+'%'+#39;
  if Lower='1' then
  St1:='Lower(Gcode)'+' like '+'Lower('+#39+'%'+Str+'%'+#39+')'+' Or '+
       'Lower(Gname)'+' like '+'Lower('+#39+'%'+Str+'%'+#39+')';
  St1:='Hcode'+'='+#39+Sth+#39+' and '+'('+St1+')';

  if Str < '9____' Then
  St2:=' Order By Gcode' else
  St2:=' Order By Gname';
  St1:=St1+St2;

  if Button001.Caption='2' Then begin

    Sqlen := 'Select * From H2_Gbun Where '+D_Select+St1;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(Query1)
    else ShowMessage(E_Open);
    Query1.First;

  end else begin

    Sqlen := 'Select * From H1_Gbun Where '+D_Select+St1;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(Query1)
    else ShowMessage(E_Open);
    Query1.First;

  end;
end;

procedure TSeek60.FilterSeek(Str,Sth:String);
begin
//
end;

procedure TSeek60.Edit1KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  FilterTing(Edit1.Text,Edit3.Text);
end;

procedure TSeek60.Button001Click(Sender: TObject);
begin
  FilterTing(Edit1.Text,Edit3.Text);
end;

procedure TSeek60.DBGrid101DblClick(Sender: TObject);
begin
  ModalResult:=mrOK;
end;

procedure TSeek60.Edit1Enter(Sender: TObject);
begin
  FilterTing(Edit1.Text,Edit3.Text);
end;

procedure TSeek60.FormShow(Sender: TObject);
begin
  DBGrid101.SetFocus;
end;

end.
