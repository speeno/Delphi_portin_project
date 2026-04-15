unit Subu19;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  TFlatButtonUnit, StdCtrls, TFlatEditUnit, TFlatComboBoxUnit, Mylabel,
  ExtCtrls, TFlatPanelUnit;

type
  TSobo19 = class(TForm)
    Panel100: TFlatPanel;
    Label100: TmyLabel3d;
    Edit000: TFlatComboBox;
    Edit100: TFlatComboBox;
    Edit101: TFlatEdit;
    Button101: TFlatButton;
    Button102: TFlatButton;
    Label101: TmyLabel3d;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
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
    procedure Edit000KeyPress(Sender: TObject; var Key: Char);
    procedure Edit000KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit101KeyPress(Sender: TObject; var Key: Char);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit103KeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo19: TSobo19;

implementation

{$R *.DFM}

uses Base01, Seak08;

procedure TSobo19.FormActivate(Sender: TObject);
begin
//
end;

procedure TSobo19.FormShow(Sender: TObject);
var
 Save : LongInt;
 St0,St1:Integer;
 St8:array [0..21] of String;
 St9:array [0..21] of String;
begin
  {Show}
  if BorderStyle=bsNone then Exit;
  Save:=GetWindowLong(Handle,gwl_Style);
  if (Save and ws_Caption)=ws_Caption then begin
    case BorderStyle of
      bsSingle,
      bsSizeable : SetWindowLong(Handle,gwl_Style,Save and
        (not(ws_Caption)) or ws_border);
      bsDialog : SetWindowLong(Handle,gwl_Style,Save and
        (not(ws_Caption)) or ds_modalframe or ws_dlgframe);
    end;
    Height:=Height-getSystemMetrics(sm_cyCaption);
    Refresh;
  end;

  Edit000.Items.Clear;
  Edit100.Items.Clear;
  if nForm='11' Then begin
     St8[00]:='';      St9[00]:='전    체';
     St8[01]:='Gubun'; St9[01]:='거래처구분';
     St8[02]:='Jubun'; St9[02]:='거래처지역';
     St8[03]:='Gcode'; St9[03]:='거래처코드';
     St8[04]:='Gname'; St9[04]:='거래처명';
     St8[05]:='Gposa'; St9[05]:='대표자명';
     St8[06]:='Gnumb'; St9[06]:='사업자번호';
     St8[07]:='Guper'; St9[07]:='업    태';
     St8[08]:='Gjomo'; St9[08]:='종    목';
     St8[09]:='Gtel2'; St9[09]:='전화번호';
     St8[10]:='Gfax2'; St9[10]:='팩스번호';
     St8[11]:='Gpost'; St9[11]:='우편번호';
     St8[12]:='Gadd1'; St9[12]:='주    소';
     St8[13]:='Gbigo'; St9[13]:='비    고';
     St8[14]:='_____'; St9[14]:='거래처지점';
     St1:=14;
  end;
  if nForm='12' Then begin
     St8[00]:='';      St9[00]:='전    체';
     St8[01]:='Gubun'; St9[01]:='입고처구분';
     St8[02]:='Jubun'; St9[02]:='입고처지역';
     St8[03]:='Gcode'; St9[03]:='입고처코드';
     St8[04]:='Gname'; St9[04]:='입고처명';
     St8[05]:='Gposa'; St9[05]:='대표자명';
     St8[06]:='Gnumb'; St9[06]:='사업자번호';
     St8[07]:='Guper'; St9[07]:='업    태';
     St8[08]:='Gjomo'; St9[08]:='종    목';
     St8[09]:='Gtel2'; St9[09]:='전화번호';
     St8[10]:='Gfax2'; St9[10]:='팩스번호';
     St8[11]:='Gpost'; St9[11]:='우편번호';
     St8[12]:='Gadd1'; St9[12]:='주    소';
     St8[13]:='Gbigo'; St9[13]:='비    고';
     St1:=13;
  end;
  if nForm='13' Then begin
     St8[00]:='';      St9[00]:='전    체';
     St8[01]:='Gubun'; St9[01]:='저자구분';
     St8[02]:='Data1'; St9[02]:='등록일자';
     St8[03]:='Gcode'; St9[03]:='저자코드';
     St8[04]:='Gposa'; St9[04]:='저 자 명';
     St8[05]:='Gname'; St9[05]:='직 장 명';
     St8[06]:='Gjice'; St9[06]:='직    책';
     St8[07]:='Gscho'; St9[07]:='출신학교';
     St8[08]:='Gnumb'; St9[08]:='사업자번호';
     St8[09]:='Gnum1'; St9[09]:='주민등록';
     St8[10]:='Gnum2'; St9[10]:='계좌번호';
     St8[11]:='Gtel2'; St9[11]:='전화번호';
     St8[12]:='Gfax2'; St9[12]:='팩스번호';
     St8[13]:='Gbigo'; St9[13]:='비    고';
     St1:=13;
  end;
  if nForm='14' Then begin
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
  if nForm='15' Then begin
     St8[00]:='';      St9[00]:='전    체';
     St8[01]:='Gubun'; St9[01]:='구    분';
     St8[02]:='Jubun'; St9[02]:='거래처지역';
     St8[03]:='Gcode'; St9[03]:='거래처코드';
     St8[04]:='Gname'; St9[04]:='거래처명';
     St8[05]:='Gposa'; St9[05]:='대표자명';
     St8[06]:='Gnumb'; St9[06]:='사업자번호';
     St8[07]:='Guper'; St9[07]:='업    태';
     St8[08]:='Gjomo'; St9[08]:='종    목';
     St8[09]:='Gtel2'; St9[09]:='전화번호';
     St8[10]:='Gfax2'; St9[10]:='팩스번호';
     St8[11]:='Gpost'; St9[11]:='우편번호';
     St8[12]:='Gadd1'; St9[12]:='주    소';
     St8[13]:='Gbigo'; St9[13]:='비    고';
     St1:=13;
  end;
  if nForm='46' Then begin
     St8[00]:='';      St9[00]:='전    체';
     St8[01]:='Gnumb'; St9[01]:='어음번호';
     St8[02]:='Scode'; St9[02]:='처리코드';
     St8[03]:='Gname'; St9[03]:='발 행 처';
     St8[04]:='Gposa'; St9[04]:='발 행 인';
     St8[05]:='Date1'; St9[05]:='발행일자';
     St8[06]:='Date2'; St9[06]:='받은일자';
     St8[07]:='Date3'; St9[07]:='지급일자';
     St8[08]:='Name1'; St9[08]:='지 급 처';
     St8[09]:='Gbang'; St9[09]:='지급은행';
     St8[10]:='Name2'; St9[10]:='지급지점';
     St8[11]:='Date4'; St9[11]:='만기일자';
     St8[12]:='Gssum'; St9[12]:='금    액';
     St8[13]:='Grat1'; St9[13]:='할 인 율';
     St8[14]:='Gosum'; St9[14]:='할인금액';
     St8[15]:='Gbigo'; St9[15]:='비    고';
     St1:=15;
  end;

  for St0:=0 to St1 do begin
  Edit100.Items.Add(St8[St0]);
  Edit000.Items.Add(St9[St0]);
  end;
  Edit000.ItemIndex:=0;
end;

procedure TSobo19.FormClose(Sender: TObject; var Action: TCloseAction);
begin
{ Release;
  Action:=caFree;
  Sobo19:=nil; }
end;

procedure TSobo19.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button012Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button014Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button015Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button016Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button017Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button101Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo19.Edit000KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    Edits: TFlatComboBox;
begin
  Hands:=Edit000.Handle;
  Edits:=Edit000;
  if Key=#13 Then begin
    if Edits.DropDownCount=9 Then Edits.DropDownCount:=8 else
    if Edits.DropDownCount=8 Then Edits.DropDownCount:=9;
    if Edits.DropDownCount=9 Then begin
      Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
    end else
    if Edits.DropDownCount=8 Then begin
      Key:=#0; SendMessage(Hands, cb_ShowDropDown, 1, 0);
    end;
  end;
end;

procedure TSobo19.Edit000KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit000;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo19.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; ModalResult:=mrOK;
  end;
end;

procedure TSobo19.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo19.Edit103KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    if Edit103.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit103.Text;
    Seak80.FilterTing(Edit103.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      Edit102.Text:=Seak80.Query1Gcode.AsString;
      Edit103.Text:=Seak80.Query1Gname.AsString;
      if Base10.Database.Database<>'chul_02_db' then begin
      Key:=#0; ModalResult:=mrOK;
      end;
    end else
    if Seak80.ShowModal=mrOK Then begin
      Edit102.Text:=Seak80.Query1Gcode.AsString;
      Edit103.Text:=Seak80.Query1Gname.AsString;
      if Base10.Database.Database<>'chul_02_db' then begin
      Key:=#0; ModalResult:=mrOK;
      end;
    end;
    end;
  end;
end;

end.
