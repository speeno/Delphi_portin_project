unit Subu19_1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  TFlatButtonUnit, StdCtrls, TFlatEditUnit, TFlatComboBoxUnit, Mylabel,
  ExtCtrls, TFlatPanelUnit;

type
  TSobo19_1 = class(TForm)
    Panel100: TFlatPanel;
    Label100: TmyLabel3d;
    ED_Gubun_Name: TFlatComboBox;
    ED_Field_Name: TFlatComboBox;
    ED_Content: TFlatEdit;
    Button101: TFlatButton;
    Button102: TFlatButton;
    procedure FormActivate(Sender: TObject);
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
    procedure ED_Gubun_NameKeyPress(Sender: TObject; var Key: Char);
    procedure ED_ContentKeyPress(Sender: TObject; var Key: Char);
    procedure ED_ContentKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure FormShow(Sender: TObject);
  private
    { Private declarations }
  public
    procedure Set_Option(fForm: string);
  end;

var
  Sobo19_1: TSobo19_1;

implementation

{$R *.DFM}

uses Base01, Seak08;

procedure TSobo19_1.FormActivate(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button012Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button014Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button015Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button016Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button017Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button101Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo19_1.ED_Gubun_NameKeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  begin
    Key:=#0;
    SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo19_1.ED_ContentKeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  begin
    Key:=#0;
    ModalResult:=mrOK;
  end;
end;

procedure TSobo19_1.ED_ContentKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo19_1.Set_Option(fForm: string);
var
  Save : LongInt;
  St0,St1:Integer;
  St8:array [0..21] of String;
  St9:array [0..21] of String;
begin
  ED_Gubun_Name.Items.Clear;
  ED_Field_Name.Items.Clear;

  if nForm='14' Then
  begin
     St8[00]:='';      St9[00]:='전    체';
     St8[01]:='Gubun'; St9[01]:='도서분류';
     St8[02]:='Jubun'; St9[02]:='도서처리';
     St8[03]:='Gcode'; St9[03]:='도서코드';
     St8[04]:='Gname'; St9[04]:='도 서 명';
     St8[05]:='Gjeja'; St9[05]:='저 자 명';
     St8[06]:='Gdabi'; St9[06]:='단    위';
     St8[07]:='Gdang'; St9[07]:='단    가';
     St8[08]:='Gisbn'; St9[08]:='ISBN번호';
     St8[09]:='Gbjil'; St9[09]:='도 서 질';
     St8[10]:='Gbigo'; St9[10]:='비    고';
     St1:=10;
  end;

  for St0:=0 to St1 do
  begin
    ED_Field_Name.Items.Add(St8[St0]);
    ED_Gubun_Name.Items.Add(St9[St0]);
  end;
  ED_Gubun_Name.ItemIndex := 4;
end;
procedure TSobo19_1.FormShow(Sender: TObject);
begin
  ED_Content.SetFocus;
end;

end.
