unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Db, ZMySqlQuery, ZQuery, ZTransact, ZMySqlTr, ZConnect, ZMySqlCon, Grids,
  DBGrids, StdCtrls;

type
  TForm1 = class(TForm)
    Database: TZMySqlDatabase;
    Transact: TZMySqlTransact;
    ZMySqlTable1: TZMySqlTable;
    ZMySqlTable2: TZMySqlTable;
    ZMySqlQuery1: TZMySqlQuery;
    ZMySqlQuery2: TZMySqlQuery;
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    DBGrid1: TDBGrid;
    DBGrid2: TDBGrid;
    ZMySqlTable1gcode: TStringField;
    ZMySqlTable1gname: TStringField;
    ZMySqlTable2gcode: TStringField;
    ZMySqlTable2gname: TStringField;
    ZMySqlQuery1hcode: TStringField;
    ZMySqlQuery1gcode: TStringField;
    ZMySqlQuery1bcode: TStringField;
    ZMySqlQuery1bname: TStringField;
    ZMySqlQuery1hname: TStringField;
    ZMySqlQuery1gname: TStringField;
    ZMySqlQuery2hcode: TStringField;
    ZMySqlQuery2hname: TStringField;
    ZMySqlQuery2gcode: TStringField;
    ZMySqlQuery2gname: TStringField;
    ZMySqlQuery2bcode: TStringField;
    ZMySqlQuery2bname: TStringField;
    ZMySqlTable3: TZMySqlTable;
    ZMySqlTable3hcode: TStringField;
    ZMySqlTable3gcode: TStringField;
    ZMySqlTable3gname: TStringField;
    DataSource3: TDataSource;
    Button1: TButton;
    Edit1: TEdit;
    Edit2: TEdit;
    ZMySqlTable4: TZMySqlTable;
    ZMySqlTable5: TZMySqlTable;
    DataSource4: TDataSource;
    ZMySqlQuery3: TZMySqlQuery;
    ZMySqlTable5post: TStringField;
    ZMySqlTable5addr: TStringField;
    procedure Button1Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.DFM}

procedure TForm1.Button1Click(Sender: TObject);
begin
  if ZMySqlTable4.locate('hcode;gcode',VarArrayOf([Edit1.Text,Edit2.Text]),[loCaseInsensitive])=true then
  showmessage('1');
end;

end.
