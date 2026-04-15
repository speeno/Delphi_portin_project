unit Seak09;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Buttons, Mask, TFlatButtonUnit, TFlatNumberUnit,
  TFlatMaskEditUnit, TFlatEditUnit, TFlatComboBoxUnit, TFlatPanelUnit,
  Mylabel, TFlatCheckBoxUnit;

type
  TSeak90 = class(TForm)
    Panel200: TFlatPanel;
    CheckBox1: TFlatCheckBox;
    FlatPanel18: TFlatPanel;
    Label301: TmyLabel3d;
    Panel201: TFlatPanel;
    Panel202: TFlatPanel;
    Panel204: TFlatPanel;
    Edit201: TFlatNumber;
    Edit208: TFlatNumber;
    Edit209: TFlatNumber;
    Edit210: TFlatNumber;
    Edit202: TFlatNumber;
    Edit203: TFlatNumber;
    Edit204: TFlatNumber;
    Panel203: TFlatPanel;
    Edit205: TFlatNumber;
    Edit206: TFlatNumber;
    Edit207: TFlatNumber;
    Edit231: TFlatNumber;
    Edit232: TFlatNumber;
    FlatPanel4: TFlatPanel;
    FlatPanel9: TFlatPanel;
    Edit246: TFlatNumber;
    Edit224: TFlatNumber;
    Panel205: TFlatPanel;
    Panel207: TFlatPanel;
    Edit217: TFlatNumber;
    Panel211: TFlatPanel;
    Edit211: TFlatNumber;
    Edit212: TFlatNumber;
    Edit213: TFlatNumber;
    Edit218: TFlatNumber;
    Edit219: TFlatNumber;
    Edit220: TFlatNumber;
    Edit225: TFlatNumber;
    Panel206: TFlatPanel;
    Edit214: TFlatNumber;
    Edit215: TFlatNumber;
    Edit216: TFlatNumber;
    Edit221: TFlatNumber;
    Edit222: TFlatNumber;
    Edit223: TFlatNumber;
    Edit229: TFlatNumber;
    Edit233: TFlatNumber;
    Edit234: TFlatNumber;
    Edit235: TFlatNumber;
    FlatPanel2: TFlatPanel;
    FlatPanel3: TFlatPanel;
    Edit240: TFlatNumber;
    Edit241: TFlatNumber;
    Edit242: TFlatNumber;
    Edit243: TFlatNumber;
    Edit244: TFlatNumber;
    Edit245: TFlatNumber;
    CheckBox2: TFlatCheckBox;
    CheckBox3: TFlatCheckBox;
    FlatPanel19: TFlatPanel;
    Label302: TmyLabel3d;
    Panel208: TFlatPanel;
    Panel209: TFlatPanel;
    Panel215: TFlatPanel;
    Panel217: TFlatPanel;
    FlatPanel1: TFlatPanel;
    FlatPanel5: TFlatPanel;
    FlatPanel6: TFlatPanel;
    FlatPanel10: TFlatPanel;
    FlatPanel11: TFlatPanel;
    FlatPanel12: TFlatPanel;
    FlatPanel13: TFlatPanel;
    FlatPanel14: TFlatPanel;
    FlatPanel17: TFlatPanel;
    Edit247: TFlatNumber;
    Edit248: TFlatNumber;
    FlatPanel21: TFlatPanel;
    Edit261: TFlatNumber;
    Edit262: TFlatNumber;
    Edit263: TFlatNumber;
    FlatPanel22: TFlatPanel;
    FlatPanel23: TFlatPanel;
    Edit264: TFlatNumber;
    Edit265: TFlatNumber;
    Edit266: TFlatNumber;
    FlatPanel24: TFlatPanel;
    Panel213: TFlatPanel;
    Edit227: TFlatNumber;
    Panel212: TFlatPanel;
    Edit226: TFlatNumber;
    Panel216: TFlatPanel;
    Panel214: TFlatPanel;
    Edit228: TFlatNumber;
    Edit230: TFlatNumber;
    FlatPanel25: TFlatPanel;
    myLabel3d1: TmyLabel3d;
    FlatPanel26: TFlatPanel;
    myLabel3d2: TmyLabel3d;
    FlatPanel27: TFlatPanel;
    FlatPanel28: TFlatPanel;
    FlatPanel29: TFlatPanel;
    FlatPanel31: TFlatPanel;
    FlatPanel32: TFlatPanel;
    FlatPanel33: TFlatPanel;
    FlatPanel34: TFlatPanel;
    FlatPanel35: TFlatPanel;
    FlatPanel36: TFlatPanel;
    FlatPanel37: TFlatPanel;
    FlatPanel38: TFlatPanel;
    FlatPanel39: TFlatPanel;
    Edit301: TFlatNumber;
    Edit302: TFlatNumber;
    Edit303: TFlatNumber;
    Edit304: TFlatNumber;
    Edit305: TFlatNumber;
    Edit309: TFlatNumber;
    Edit306: TFlatNumber;
    Edit307: TFlatNumber;
    Edit308: TFlatNumber;
    Edit310: TFlatNumber;
    Edit311: TFlatNumber;
    Edit312: TFlatNumber;
    FlatPanel41: TFlatPanel;
    Edit901: TFlatMaskEdit;
    Edit902: TFlatNumber;
    FlatPanel40: TFlatPanel;
    FlatPanel30: TFlatPanel;
    Edit236: TFlatNumber;
    Edit237: TFlatNumber;
    Edit238: TFlatEdit;
    Edit239: TFlatEdit;
    FlatPanel7: TFlatPanel;
    FlatPanel8: TFlatPanel;
    FlatPanel15: TFlatPanel;
    Button301: TFlatButton;
    FlatPanel16: TFlatPanel;
    FlatPanel20: TFlatPanel;
    Edit313: TFlatNumber;
    Edit314: TFlatNumber;
    Edit315: TFlatNumber;
    Label9: TmyLabel3d;
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit111KeyPress(Sender: TObject; var Key: Char);
    procedure Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit112KeyPress(Sender: TObject; var Key: Char);
    procedure Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure BitBtn101Click(Sender: TObject);
    procedure BitBtn102Click(Sender: TObject);
    procedure Button300Click(St0,St1: String);
    procedure Button301Click(Sender: TObject);
    procedure Button302Click(St1: String);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seak90: TSeak90;

implementation

{$R *.DFM}

uses Base01, TcpLib;

procedure TSeak90.FormShow(Sender: TObject);
begin
//
end;

procedure TSeak90.FormClose(Sender: TObject; var Action: TCloseAction);
begin
//
end;

procedure TSeak90.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSeak90.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSeak90.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSeak90.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSeak90.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSeak90.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSeak90.BitBtn101Click(Sender: TObject);
begin
//
end;

procedure TSeak90.BitBtn102Click(Sender: TObject);
begin
//
end;

procedure TSeak90.Button300Click(St0,St1: String);
begin
  Button301Click(Self);
  Button302Click(St1);

  Sqlen:='Select Hcode,'+
         'Sum01,Sum02,Sum03,Sum04,Sum05,Sum06,Sum07,Sum08,Sum09,Sum10,'+
         'Sum11,Sum12,Sum13,Sum14,Sum15,Sum16,Sum17,Sum18,Sum19,Sum20,'+
         'Sum21,Sum22,Sum23,Sum24,Sum25,Sum26,Sum27,Sum28,Sum29,Sum30,'+
         'Sum31,Sum32,Sum33,Sum34,Sum35,Sum36,Sum37,Sum40,Sum41,Sum42,'+
         'Sum43,Sum44,Sum45,Sum46,Sum47,Sum48,Sum61,Sum62,Sum63,Sum64,'+
         'Sum65,Sum66,Sum51,Sum52,Sum53,Sum54,Sum55,Sum56,Sum57,Sum58,'+
         'Sum59,Sum67,Sum68,Gsusu,Vdate,Bigo1,Bigo2,Yesno '+
         'From T2_Ssub Where '+D_Select+
         'Gdate'+'>='+#39+St0+#39+' and '+
         'Gdate'+'<='+#39+St0+#39+' and '+
         'Hcode'+' ='+#39+St1+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  CheckBox1.Checked:=False;

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    Edit201.Value:=StrToIntDef(SGrid.Cells[ 1,List1],0);
    if CheckBox3.Checked=False then
    Edit202.Value:=StrToIntDef(SGrid.Cells[ 2,List1],0);
    Edit203.Value:=StrToIntDef(SGrid.Cells[ 3,List1],0);
    if CheckBox3.Checked=False then
    Edit204.Value:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    Edit205.Value:=StrToIntDef(SGrid.Cells[ 5,List1],0);
    if CheckBox3.Checked=False then
    Edit206.Value:=StrToIntDef(SGrid.Cells[ 6,List1],0);
    Edit207.Value:=StrToIntDef(SGrid.Cells[ 7,List1],0);
    Edit208.Value:=StrToIntDef(SGrid.Cells[ 8,List1],0);
    if CheckBox3.Checked=False then
    Edit209.Value:=StrToIntDef(SGrid.Cells[ 9,List1],0);
    Edit210.Value:=StrToIntDef(SGrid.Cells[10,List1],0);
    Edit211.Value:=StrToIntDef(SGrid.Cells[11,List1],0);
    if CheckBox3.Checked=False then
    Edit212.Value:=StrToIntDef(SGrid.Cells[12,List1],0);
    Edit213.Value:=StrToIntDef(SGrid.Cells[13,List1],0);
    Edit214.Value:=StrToIntDef(SGrid.Cells[14,List1],0);
    if CheckBox3.Checked=False then
    Edit215.Value:=StrToIntDef(SGrid.Cells[15,List1],0);
    Edit216.Value:=StrToIntDef(SGrid.Cells[16,List1],0);
    Edit217.Value:=StrToIntDef(SGrid.Cells[17,List1],0);
    if CheckBox3.Checked=False then
    Edit218.Value:=StrToIntDef(SGrid.Cells[18,List1],0);
    Edit219.Value:=StrToIntDef(SGrid.Cells[19,List1],0);
    if CheckBox3.Checked=False then
    Edit220.Value:=StrToIntDef(SGrid.Cells[20,List1],0);
    Edit221.Value:=StrToIntDef(SGrid.Cells[21,List1],0);
    if CheckBox3.Checked=False then
    Edit222.Value:=StrToIntDef(SGrid.Cells[22,List1],0);
    Edit223.Value:=StrToIntDef(SGrid.Cells[23,List1],0);
    if CheckBox3.Checked=False then
    Edit224.Value:=StrToIntDef(SGrid.Cells[24,List1],0);
    if CheckBox3.Checked=False then
    Edit225.Value:=StrToIntDef(SGrid.Cells[25,List1],0);
    Edit226.Value:=StrToIntDef(SGrid.Cells[26,List1],0);
    Edit227.Value:=StrToIntDef(SGrid.Cells[27,List1],0);
    Edit228.Value:=StrToIntDef(SGrid.Cells[28,List1],0);
    Edit229.Value:=StrToIntDef(SGrid.Cells[29,List1],0);
    Edit230.Value:=StrToIntDef(SGrid.Cells[30,List1],0);
    Edit231.Value:=StrToIntDef(SGrid.Cells[31,List1],0);
    Edit232.Value:=StrToIntDef(SGrid.Cells[32,List1],0);
    Edit233.Value:=StrToIntDef(SGrid.Cells[33,List1],0);
    if CheckBox3.Checked=False then
    Edit234.Value:=StrToIntDef(SGrid.Cells[34,List1],0);
    Edit235.Value:=StrToIntDef(SGrid.Cells[35,List1],0);
    Edit236.Value:=StrToIntDef(SGrid.Cells[36,List1],0);
    Edit237.Value:=StrToIntDef(SGrid.Cells[37,List1],0);

    if CheckBox3.Checked=False then
    Edit240.Value:=StrToIntDef(SGrid.Cells[38,List1],0);
    Edit241.Value:=StrToIntDef(SGrid.Cells[39,List1],0);
    if CheckBox3.Checked=False then
    Edit242.Value:=StrToIntDef(SGrid.Cells[40,List1],0);
    Edit243.Value:=StrToIntDef(SGrid.Cells[41,List1],0);
    if CheckBox3.Checked=False then
    Edit244.Value:=StrToIntDef(SGrid.Cells[42,List1],0);
    Edit245.Value:=StrToIntDef(SGrid.Cells[43,List1],0);
    Edit246.Value:=StrToIntDef(SGrid.Cells[44,List1],0);
    Edit247.Value:=StrToIntDef(SGrid.Cells[45,List1],0);
    if CheckBox3.Checked=False then
    Edit248.Value:=StrToIntDef(SGrid.Cells[46,List1],0);

    Edit261.Value:=StrToIntDef(SGrid.Cells[47,List1],0);
    if CheckBox3.Checked=False then
    Edit262.Value:=StrToIntDef(SGrid.Cells[48,List1],0);
    Edit263.Value:=StrToIntDef(SGrid.Cells[49,List1],0);
    Edit264.Value:=StrToIntDef(SGrid.Cells[50,List1],0);
    if CheckBox3.Checked=False then
    Edit265.Value:=StrToIntDef(SGrid.Cells[51,List1],0);
    Edit266.Value:=StrToIntDef(SGrid.Cells[52,List1],0);

    Edit301.Value:=StrToIntDef(SGrid.Cells[53,List1],0);
    if CheckBox3.Checked=False then
    Edit302.Value:=StrToIntDef(SGrid.Cells[54,List1],0);
    Edit303.Value:=StrToIntDef(SGrid.Cells[55,List1],0);
    Edit304.Value:=StrToIntDef(SGrid.Cells[56,List1],0);
    if CheckBox3.Checked=False then
    Edit305.Value:=StrToIntDef(SGrid.Cells[57,List1],0);
    Edit306.Value:=StrToIntDef(SGrid.Cells[58,List1],0);
    Edit307.Value:=StrToIntDef(SGrid.Cells[59,List1],0);
    if CheckBox3.Checked=False then
    Edit308.Value:=StrToIntDef(SGrid.Cells[60,List1],0);
    Edit309.Value:=StrToIntDef(SGrid.Cells[61,List1],0);

    Edit310.Text :=SGrid.Cells[62,List1];
    Edit312.Value:=StrToIntDef(SGrid.Cells[63,List1],0);

    Edit902.Value:=StrToIntDef(SGrid.Cells[64,List1],0);
    Edit901.Text :=SGrid.Cells[65,List1];

    Edit238.Text :=SGrid.Cells[66,List1];
    Edit239.Text :=SGrid.Cells[67,List1];
    if SGrid.Cells[68,List1]='1' then
    CheckBox1.Checked:=True else
    CheckBox1.Checked:=False;
  end;
end;

procedure TSeak90.Button301Click(Sender: TObject);
begin
  Edit201.Value:=0;
  Edit202.Value:=0;
  Edit203.Value:=0;
  Edit204.Value:=0;
  Edit205.Value:=0;
  Edit206.Value:=0;
  Edit207.Value:=0;
  Edit208.Value:=0;
  Edit209.Value:=0;
  Edit210.Value:=0;
  Edit211.Value:=0;
  Edit212.Value:=0;
  Edit213.Value:=0;
  Edit214.Value:=0;
  Edit215.Value:=0;
  Edit216.Value:=0;
  Edit217.Value:=0;
  Edit218.Value:=0;
  Edit219.Value:=0;
  Edit220.Value:=0;
  Edit221.Value:=0;
  Edit222.Value:=0;
  Edit223.Value:=0;
  Edit224.Value:=0;
  Edit225.Value:=0;
  Edit226.Value:=0;
  Edit227.Value:=0;
  Edit228.Value:=0;
  Edit229.Value:=0;
  Edit230.Value:=0;
  Edit231.Value:=0;
  Edit232.Value:=0;
  Edit233.Value:=0;
  Edit234.Value:=0;
  Edit235.Value:=0;
  Edit236.Value:=0;
  Edit237.Value:=0;
  Edit238.Text:='';
  Edit239.Text:='';
  Edit240.Value:=0;
  Edit241.Value:=0;
  Edit242.Value:=0;
  Edit243.Value:=0;
  Edit244.Value:=0;
  Edit245.Value:=0;
  Edit246.Value:=0;
  Edit247.Value:=0;
  Edit248.Value:=0;
  Edit261.Value:=0;
  Edit262.Value:=0;
  Edit263.Value:=0;
  Edit264.Value:=0;
  Edit265.Value:=0;
  Edit266.Value:=0;
  Edit301.Value:=0;
  Edit302.Value:=0;
  Edit303.Value:=0;
  Edit304.Value:=0;
  Edit305.Value:=0;
  Edit306.Value:=0;
  Edit307.Value:=0;
  Edit308.Value:=0;
  Edit309.Value:=0;
  Edit310.Value:=0;
  Edit311.Value:=0;
  Edit312.Value:=0;
  Edit313.Value:=0;
  Edit314.Value:=0;
  Edit315.Value:=0;
  Edit901.Text:='';
  Edit902.Value:=0;
end;

procedure TSeak90.Button302Click(St1: String);
begin
  Sqlen:='Select '+
         'Yes33,Yes34,Yes35,'+
         'Yes41,Yes42,Yes43,Yes44,Yes45,Yes48,Yes49,'+
         'Yes51,Yes52,Yes53,Yes54,Yes55,Yes56,Yes57,Yes58,Yes59,'+
         'Yes61,Yes62 '+
         'From G7_Ggeo Where '+D_Select+
         'Gcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    if SGrid.Cells[0,List1]='1' then begin
      Edit205.Enabled:=True;
      Edit205.ColorFlat:=clWhite;
      Edit206.Enabled:=True;
      Edit206.ColorFlat:=clWhite;
      Edit207.Enabled:=True;
      Edit207.ColorFlat:=$0080FFFF;
    end else begin
      Edit205.Enabled:=False;
      Edit205.ColorFlat:=clActiveBorder;
      Edit206.Enabled:=False;
      Edit206.ColorFlat:=clActiveBorder;
      Edit207.Enabled:=False;
      Edit207.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[1,List1]='1' then begin
      Edit208.Enabled:=True;
      Edit208.ColorFlat:=clWhite;
      Edit209.Enabled:=True;
      Edit209.ColorFlat:=clWhite;
      Edit210.Enabled:=True;
      Edit210.ColorFlat:=$0080FFFF;
    end else begin
      Edit208.Enabled:=False;
      Edit208.ColorFlat:=clActiveBorder;
      Edit209.Enabled:=False;
      Edit209.ColorFlat:=clActiveBorder;
      Edit210.Enabled:=False;
      Edit210.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[3,List1]='1' then begin
      Edit218.Enabled:=True;
      Edit218.ColorFlat:=clWhite;
      Edit220.Enabled:=True;
      Edit220.ColorFlat:=$0080FFFF;
    end else begin
      Edit218.Enabled:=False;
      Edit218.ColorFlat:=clActiveBorder;
      Edit220.Enabled:=False;
      Edit220.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[4,List1]='1' then begin
      Edit221.Enabled:=True;
      Edit221.ColorFlat:=clWhite;
      Edit222.Enabled:=True;
      Edit222.ColorFlat:=clWhite;
      Edit223.Enabled:=True;
      Edit223.ColorFlat:=$0080FFFF;
    end else begin
      Edit221.Enabled:=False;
      Edit221.ColorFlat:=clActiveBorder;
      Edit222.Enabled:=False;
      Edit222.ColorFlat:=clActiveBorder;
      Edit223.Enabled:=False;
      Edit223.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[5,List1]='1' then begin
      Edit240.Enabled:=True;
      Edit240.ColorFlat:=clWhite;
      Edit242.Enabled:=True;
      Edit242.ColorFlat:=clWhite;
    end else begin
      Edit240.Enabled:=False;
      Edit240.ColorFlat:=clActiveBorder;
      Edit242.Enabled:=False;
      Edit242.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[6,List1]='1' then begin
      Edit243.Enabled:=True;
      Edit243.ColorFlat:=clWhite;
      Edit244.Enabled:=True;
      Edit244.ColorFlat:=clWhite;
      Edit245.Enabled:=True;
      Edit245.ColorFlat:=$0080FFFF;
    end else begin
      Edit243.Enabled:=False;
      Edit243.ColorFlat:=clActiveBorder;
      Edit244.Enabled:=False;
      Edit244.ColorFlat:=clActiveBorder;
      Edit245.Enabled:=False;
      Edit245.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[7,List1]='1' then begin
      Edit233.Enabled:=True;
      Edit233.ColorFlat:=clWhite;
      Edit234.Enabled:=True;
      Edit234.ColorFlat:=clWhite;
      Edit235.Enabled:=True;
      Edit235.ColorFlat:=$0080FFFF;
    end else begin
      Edit233.Enabled:=False;
      Edit233.ColorFlat:=clActiveBorder;
      Edit234.Enabled:=False;
      Edit234.ColorFlat:=clActiveBorder;
      Edit235.Enabled:=False;
      Edit235.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[8,List1]='1' then begin
      Edit313.Enabled:=True;
      Edit313.ColorFlat:=clWhite;
      Edit314.Enabled:=True;
      Edit314.ColorFlat:=clWhite;
      Edit315.Enabled:=True;
      Edit315.ColorFlat:=$0080FFFF;
    end else begin
      Edit313.Enabled:=False;
      Edit313.ColorFlat:=clActiveBorder;
      Edit314.Enabled:=False;
      Edit314.ColorFlat:=clActiveBorder;
      Edit315.Enabled:=False;
      Edit315.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[10,List1]='1' then begin
      Edit225.Enabled:=True;
      Edit225.ColorFlat:=$0080FFFF;
    end else begin
      Edit225.Enabled:=False;
      Edit225.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[11,List1]='1' then begin
      Edit211.Enabled:=True;
      Edit211.ColorFlat:=clWhite;
      Edit212.Enabled:=True;
      Edit212.ColorFlat:=clWhite;
      Edit213.Enabled:=True;
      Edit213.ColorFlat:=$0080FFFF;
    end else begin
      Edit211.Enabled:=False;
      Edit211.ColorFlat:=clActiveBorder;
      Edit212.Enabled:=False;
      Edit212.ColorFlat:=clActiveBorder;
      Edit213.Enabled:=False;
      Edit213.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[12,List1]='1' then begin
      Edit214.Enabled:=True;
      Edit214.ColorFlat:=clWhite;
      Edit215.Enabled:=True;
      Edit215.ColorFlat:=clWhite;
      Edit216.Enabled:=True;
      Edit216.ColorFlat:=$0080FFFF;
    end else begin
      Edit214.Enabled:=False;
      Edit214.ColorFlat:=clActiveBorder;
      Edit215.Enabled:=False;
      Edit215.ColorFlat:=clActiveBorder;
      Edit216.Enabled:=False;
      Edit216.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[13,List1]='1' then begin
      Edit231.Enabled:=True;
      Edit231.ColorFlat:=clWhite;
      Edit232.Enabled:=True;
      Edit232.ColorFlat:=clWhite;
      Edit224.Enabled:=True;
      Edit224.ColorFlat:=$0080FFFF;
    end else begin
      Edit231.Enabled:=False;
      Edit231.ColorFlat:=clActiveBorder;
      Edit232.Enabled:=False;
      Edit232.ColorFlat:=clActiveBorder;
      Edit224.Enabled:=False;
      Edit224.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[14,List1]='1' then begin
      Edit247.Enabled:=True;
      Edit247.ColorFlat:=clWhite;
      Edit248.Enabled:=True;
      Edit248.ColorFlat:=clWhite;
      Edit246.Enabled:=True;
      Edit246.ColorFlat:=$0080FFFF;
    end else begin
      Edit247.Enabled:=False;
      Edit247.ColorFlat:=clActiveBorder;
      Edit248.Enabled:=False;
      Edit248.ColorFlat:=clActiveBorder;
      Edit246.Enabled:=False;
      Edit246.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[15,List1]='1' then begin
      Edit301.Enabled:=True;
      Edit301.ColorFlat:=clWhite;
      Edit302.Enabled:=True;
      Edit302.ColorFlat:=clWhite;
      Edit303.Enabled:=True;
      Edit303.ColorFlat:=$0080FFFF;
    end else begin
      Edit301.Enabled:=False;
      Edit301.ColorFlat:=clActiveBorder;
      Edit302.Enabled:=False;
      Edit302.ColorFlat:=clActiveBorder;
      Edit303.Enabled:=False;
      Edit303.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[16,List1]='1' then begin
      Edit304.Enabled:=True;
      Edit304.ColorFlat:=clWhite;
      Edit305.Enabled:=True;
      Edit305.ColorFlat:=clWhite;
      Edit306.Enabled:=True;
      Edit306.ColorFlat:=$0080FFFF;
    end else begin
      Edit304.Enabled:=False;
      Edit304.ColorFlat:=clActiveBorder;
      Edit305.Enabled:=False;
      Edit305.ColorFlat:=clActiveBorder;
      Edit306.Enabled:=False;
      Edit306.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[17,List1]='1' then begin
      Edit307.Enabled:=True;
      Edit307.ColorFlat:=clWhite;
      Edit308.Enabled:=True;
      Edit308.ColorFlat:=clWhite;
      Edit309.Enabled:=True;
      Edit309.ColorFlat:=$0080FFFF;
    end else begin
      Edit307.Enabled:=False;
      Edit307.ColorFlat:=clActiveBorder;
      Edit308.Enabled:=False;
      Edit308.ColorFlat:=clActiveBorder;
      Edit309.Enabled:=False;
      Edit309.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[18,List1]='1' then begin
      Edit310.Enabled:=True;
      Edit310.ColorFlat:=clWhite;
      Edit311.Enabled:=True;
      Edit311.ColorFlat:=clWhite;
      Edit312.Enabled:=True;
      Edit312.ColorFlat:=$0080FFFF;
    end else begin
      Edit310.Enabled:=False;
      Edit310.ColorFlat:=clActiveBorder;
      Edit311.Enabled:=False;
      Edit311.ColorFlat:=clActiveBorder;
      Edit312.Enabled:=False;
      Edit312.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[19,List1]='1' then begin
      Edit261.Enabled:=True;
      Edit261.ColorFlat:=clWhite;
      Edit262.Enabled:=True;
      Edit262.ColorFlat:=clWhite;
      Edit263.Enabled:=True;
      Edit263.ColorFlat:=$0080FFFF;
    end else begin
      Edit261.Enabled:=False;
      Edit261.ColorFlat:=clActiveBorder;
      Edit262.Enabled:=False;
      Edit262.ColorFlat:=clActiveBorder;
      Edit263.Enabled:=False;
      Edit263.ColorFlat:=clActiveBorder;
    end;

    if SGrid.Cells[20,List1]='1' then begin
      Edit265.Enabled:=True;
      Edit265.ColorFlat:=clWhite;
      Edit266.Enabled:=True;
      Edit266.ColorFlat:=clWhite;
      Edit264.Enabled:=True;
      Edit264.ColorFlat:=$0080FFFF;
    end else begin
      Edit265.Enabled:=False;
      Edit265.ColorFlat:=clActiveBorder;
      Edit266.Enabled:=False;
      Edit266.ColorFlat:=clActiveBorder;
      Edit264.Enabled:=False;
      Edit264.ColorFlat:=clActiveBorder;
    end;

  end;
end;

end.
