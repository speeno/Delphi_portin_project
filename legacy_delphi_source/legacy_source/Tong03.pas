unit Tong03;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Buttons, ExtCtrls, Grids, Registry, TFlatEditUnit, TFlatPanelUnit;

type
  TTong30 = class(TForm)
    Panel1: TFlatPanel;
    Panel2: TFlatPanel;
    Panel3: TFlatPanel;
    StringGrid1: TStringGrid;
    StaticText1: TStaticText;
    btnJG: TSpeedButton;
    btnDH: TSpeedButton;
    btnLC: TSpeedButton;
    btnJP: TSpeedButton;
    btnDW: TSpeedButton;
    btnGT: TSpeedButton;
    btnHJ: TSpeedButton;
    Label1: TLabel;
    Edit1: TFlatEdit;
    procedure FormCreate(Sender: TObject);
    procedure btnJGClick(Sender: TObject);
    procedure btnDHClick(Sender: TObject);
    procedure btnLCClick(Sender: TObject);
    procedure btnJPClick(Sender: TObject);
    procedure btnDWClick(Sender: TObject);
    procedure btnGTClick(Sender: TObject);
    procedure btnHJClick(Sender: TObject);
    procedure StringGrid1DblClick(Sender: TObject);
    procedure StringGrid1SelectCell(Sender: TObject; ACol, ARow: Integer; var CanSelect: Boolean);
    procedure StaticText1DblClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    procedure MakeChar(fi,fl,si,sl : Integer);
    procedure ClearGrid;
    procedure ShowGrid;
  end;

var
  Tong30: TTong30;
  S : TStringList;

implementation

{$R *.DFM}

procedure TTong30.MakeChar(fi,fl,si,sl : Integer);
var i,j : Integer;
begin
  for i:=fi to fl do
    for j:=si to sl do
      s.Add(Char(i) + Char(j));
end;

procedure TTong30.ClearGrid;
var i,j : Integer;
begin
  S.Clear;
  // StringList Clear
  for i:=0 to StringGrid1.ColCount - 1 do
    for j:=0 to StringGrid1.RowCount - 1 do
      StringGrid1.Cells[i,j] := '';
end;

procedure TTong30.ShowGrid;
var i, j, a : Integer;
begin
  StringGrid1.RowCount := (s.Count div 14) + 1;
  a := 0;

  for i:=1 to (s.Count div 14) do begin
    for j:=1 to 14 do begin
      StringGrid1.Cells[j-1,i-1] := s.Strings[a];
      inc(a);
    end;
  end;
  // 전체 s의 행 개수에서 위에서 그리드에 안넣은 개수
  for i:=1 to (s.Count - ((s.Count div 14) * 14)) do
    StringGrid1.Cells[i-1,s.Count div 14] := s.Strings[a + i - 1];
end;

procedure TTong30.FormCreate(Sender: TObject);
begin
  // 처음에 전각문자를 표시
  S := TStringList.Create;
  btnJGClick(Sender);
end;

procedure TTong30.btnJGClick(Sender: TObject);
begin
  ClearGrid;
  MakeChar(163,163,161,254);
  ShowGrid;
end;

procedure TTong30.btnDHClick(Sender: TObject);
begin
  ClearGrid;
  MakeChar(161,162,161,229);
  ShowGrid;
end;

procedure TTong30.btnLCClick(Sender: TObject);
begin
  ClearGrid;
  MakeChar(166,166,161,228);
  MakeChar(168,169,177,254);
  ShowGrid;
end;

procedure TTong30.btnJPClick(Sender: TObject);
begin
  ClearGrid;
  MakeChar(170,170,161,245);
  MakeChar(171,171,161,246);
  ShowGrid;
end;

procedure TTong30.btnDWClick(Sender: TObject);
begin
  ClearGrid;
  MakeChar(167,167,161,239);
  MakeChar(165,165,161,170);
  MakeChar(165,165,176,185);
  ShowGrid;
end;

procedure TTong30.btnGTClick(Sender: TObject);
begin
  ClearGrid;
  MakeChar(165,165,193,216);
  MakeChar(165,165,225,248);
  MakeChar(168,168,161,175);
  MakeChar(169,169,161,176);
  MakeChar(172,172,161,193);
  MakeChar(172,172,209,241);
  ShowGrid;
end;

procedure TTong30.btnHJClick(Sender: TObject);
begin
  ClearGrid;
  MakeChar(202,253,161,254);
  ShowGrid;
end;

procedure TTong30.StringGrid1DblClick(Sender: TObject);
begin
  Edit1.Text := Edit1.Text+StaticText1.Caption;
end;

procedure TTong30.StringGrid1SelectCell(Sender: TObject; ACol, ARow: Integer; var CanSelect: Boolean);
var a,b : Char;
begin
  StaticText1.Caption := StringGrid1.Cells[ACol,ARow];
  if StaticText1.Caption <> '' then begin
    a := StaticText1.Caption[1];
    b := StaticText1.Caption[2];
  end else begin
    a := Char(0);
    b := Char(0);
  end;
{ Edit1.Text := Format('코드값 : %d+%d',[ord(a),ord(b)]); }
end;

procedure TTong30.StaticText1DblClick(Sender: TObject);
var MyDir: String;
    reg: TRegistry;
begin
{ MyDir:=GetCurrentdir;
  reg := TRegistry.Create;
  reg.RootKey := HKEY_LOCAL_MACHINE;
  reg.LazyWrite := false;
  reg.OpenKey('Software\Microsoft\Windows\CurrentVersion\Run',false);
  reg.WriteString('scktsrvr', MyDir+'\scktsrvr.exe');
  reg.CloseKey;
  reg.free;
  ShowMessage('scktsrvr.exe 등록되었습니다.'); }
end;

end.
