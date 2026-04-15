unit Subu10;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Buttons, IniFiles, Mylabel, TFlatButtonUnit, TFlatEditUnit,
  TFlatComboBoxUnit, DIMime;

type
  TSobo10 = class(TForm)
    myLabel3d1: TmyLabel3d;
    myLabel3d2: TmyLabel3d;
    myLabel3d3: TmyLabel3d;
    Edit100: TFlatComboBox;
    Edit101: TFlatEdit;
    Edit102: TFlatEdit;
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
    procedure Edit102KeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo10: TSobo10;

implementation

{$R *.DFM}

uses Base01, TcpLib;

procedure TSobo10.FormActivate(Sender: TObject);
begin
//
end;

procedure TSobo10.FormShow(Sender: TObject);
var SetupIni : TIniFile;
begin
  SetupIni := TIniFile.Create(GetExecPath + 'Config.Ini');
  With SetupIni do
  begin
    Edit100.Text:=ReadString('Client', 'Uses', '');
    Edit101.Text:=MimeDecodeString(ReadString('Client', 'UserName', ''));
  end;
  SetupIni.Free;
end;

procedure TSobo10.FormClose(Sender: TObject; var Action: TCloseAction);
var SetupIni : TIniFile;
begin
  SetupIni := TIniFile.Create(GetExecPath + 'Config.Ini');
  With SetupIni do
  begin
    WriteString('Client', 'Uses', Edit100.Text);
    WriteString('Client', 'UserName', MimeEncodeString(Edit101.Text));
    WriteString('Client', 'Password', MimeEncodeString(Edit102.Text));
  end;
  SetupIni.Free;
end;

procedure TSobo10.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button012Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button014Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button015Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button016Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button017Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Button101Click(Sender: TObject);
var SetupIni : TIniFile;
    St1,St2:String;
begin
{ SetupIni := TIniFile.Create(GetExecPath + 'Config.Ini');
  With SetupIni do begin
    St1:=MimeDecodeString(ReadString('Client', 'UserName', ''));
    St2:=MimeDecodeString(ReadString('Client', 'Password', ''));
  end;
  SetupIni.Free; }

  if(Edit101.Text='')or(Edit102.Text='')then begin
    ModalResult:=mrNone;
    ShowMessage('ID,PASSWORD를 입력해 주십시오.');
    Exit;
  end;

{ if Sqlen<>'0' then begin
    if(St1=Edit101.Text)and(St2=Edit102.Text)then
    ModalResult:=mrOK else
    ShowMessage('ID,PASSWORD가 틀립니다.'+#13+'확인해 주십시오.');
  end else
    ModalResult:=mrOK; }

  if(Logn1='')and(Logn2='')and(Logn3='')then begin
    Logn1:=Edit100.Text;
    Logn2:=Edit101.Text;
    Logn3:=Edit102.Text;
  end;

  ModalResult:=mrOK;
end;

procedure TSobo10.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo10.Edit102KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; Button101Click(Self);
  end;
end;

end.
