unit Subu40;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  TFlatButtonUnit, StdCtrls, TFlatEditUnit, Mylabel;

type
  TSobo40 = class(TForm)
    myLabel3d2: TmyLabel3d;
    Edit101: TFlatEdit;
    Button101: TFlatButton;
    Button102: TFlatButton;
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
    procedure Edit101KeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo40: TSobo40;

implementation

{$R *.DFM}

procedure TSobo40.FormActivate(Sender: TObject);
begin
//
end;

procedure TSobo40.FormShow(Sender: TObject);
begin
  Edit101.Text:='';
  Edit101.SetFocus;
end;

procedure TSobo40.FormClose(Sender: TObject; var Action: TCloseAction);
begin
//
end;

procedure TSobo40.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button012Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button014Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button015Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button016Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button017Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button101Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo40.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  ModalResult:=mrOK;
end;

end.
