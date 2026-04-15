unit Seak04;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit;

type
  TSeak40 = class(TForm)
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
    Query1POST: TStringField;
    Query1ADDR: TStringField;
    Query1DDDD: TStringField;
    Query1DONG: TStringField;
    Query1CITY: TStringField;
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
  Seak40: TSeak40;

implementation

{$R *.DFM}

uses Base01;

procedure TSeak40.FilterSing(Str:String);
begin
//
end;

procedure TSeak40.FilterTing(Str:String);
var St1,St2: String;
begin
  Base10.OpenExit(Query1);
  Base10.OpenShow(Query1);

  if Str='' Then Exit;

  if Length(Str)<4 Then begin
    ShowMessage('한글2자,숫자4자 이상 입력하세요.');
    Exit;
  end;

  St1:='Post'+' like '+#39+'%'+Str+'%'+#39+' OR '+
       'Addr'+' like '+#39+'%'+Str+'%'+#39;
  if Str < '9____' Then
  St2:=' Order By Post' else
  St2:=' Order By Addr';
  St1:=St1+St2;

  Sqlen := 'Select Post,Addr,Dddd,Dong,City '+
           'From Gg_Post Where '+St1;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Query1)
  else ShowMessage(E_Open);
  Query1.First;
end;

procedure TSeak40.FilterSeek(Str:String);
begin
//
end;

procedure TSeak40.Edit1KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  FilterTing(Edit1.Text);
end;

procedure TSeak40.Button001Click(Sender: TObject);
begin
  FilterTing(Edit1.Text);
end;

procedure TSeak40.DBGrid101DblClick(Sender: TObject);
begin
  ModalResult:=mrOK;
end;

procedure TSeak40.Edit1Enter(Sender: TObject);
begin
  FilterTing(Edit1.Text);
end;

procedure TSeak40.FormShow(Sender: TObject);
begin
  DBGrid101.SetFocus;
end;

end.
