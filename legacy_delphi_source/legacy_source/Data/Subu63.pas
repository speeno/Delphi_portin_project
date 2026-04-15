unit Subu63;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ImGridClass, ImGrid,
  ImColGrid, ImVarGrid, TFlatCheckBoxUnit, ToolEdit, DBClient, dxCore,
  dxButtons, CornerButton;

type
  TSobo63 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    Panel101: TFlatPanel;
    Panel102: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Button201: TFlatButton;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatMaskEdit;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Edit106: TFlatEdit;
    DBGrid101: TImVarGrid;
    DateEdit1: TDateEdit;
    DateEdit2: TDateEdit;
    Button700: TFlatButton;
    Button701: TFlatButton;
    CheckBox2: TFlatCheckBox;
    T6_Sub31: TClientDataSet;
    T6_Sub31GUBUN: TStringField;
    T6_Sub31SNAME: TStringField;
    T6_Sub31GCODE: TStringField;
    T6_Sub31GNAME: TStringField;
    T6_Sub31AQUT1: TFloatField;
    T6_Sub31AQUT2: TFloatField;
    T6_Sub31AQUTS: TFloatField;
    T6_Sub31BQUT1: TFloatField;
    T6_Sub31BQUT2: TFloatField;
    T6_Sub31BQUTS: TFloatField;
    T6_Sub31CQUT1: TFloatField;
    T6_Sub31CQUT2: TFloatField;
    T6_Sub31CQUTS: TFloatField;
    T6_Sub31DQUT1: TFloatField;
    T6_Sub31DQUT2: TFloatField;
    T6_Sub31DQUTS: TFloatField;
    T6_Sub31EQUT1: TFloatField;
    T6_Sub31EQUT2: TFloatField;
    T6_Sub31EQUTS: TFloatField;
    T6_Sub31FQUT1: TFloatField;
    T6_Sub31FQUT2: TFloatField;
    T6_Sub31FQUTS: TFloatField;
    T6_Sub31GQUT1: TFloatField;
    T6_Sub31GQUT2: TFloatField;
    T6_Sub31GQUTS: TFloatField;
    T6_Sub31HQUT1: TFloatField;
    T6_Sub31HQUT2: TFloatField;
    T6_Sub31HQUTS: TFloatField;
    T6_Sub31IQUT1: TFloatField;
    T6_Sub31IQUT2: TFloatField;
    T6_Sub31IQUTS: TFloatField;
    T6_Sub31JQUT1: TFloatField;
    T6_Sub31JQUT2: TFloatField;
    T6_Sub31JQUTS: TFloatField;
    T6_Sub31KQUT1: TFloatField;
    T6_Sub31KQUT2: TFloatField;
    T6_Sub31KQUTS: TFloatField;
    T6_Sub31LQUT1: TFloatField;
    T6_Sub31LQUT2: TFloatField;
    T6_Sub31LQUTS: TFloatField;
    T6_Sub31SQUT1: TFloatField;
    T6_Sub31SQUT2: TFloatField;
    T6_Sub31SQUTS: TFloatField;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    dxButton1: TdxButton;
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
    procedure Button301Click(Sender: TObject);
    procedure Edit101Change(Sender: TObject);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit111KeyPress(Sender: TObject; var Key: Char);
    procedure Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
    procedure Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101TitleClick(Column: TColumn);
    procedure DBGrid201TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit2ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button700Click(Sender: TObject);
    procedure Button701Click(Sender: TObject);
  private
    { Private declarations }
    procedure ApplyCellHoles;
  public
    { Public declarations }
  end;

var
  Sobo63: TSobo63;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo63.FormActivate(Sender: TObject);
begin
  nForm:='63';
  nSqry:=T6_Sub31;
//mSqry:=T6_Sub42;
end;

procedure TSobo63.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo63.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo63:=nil;
  Base10.OpenExit(nSqry);
//Base10.OpenExit(mSqry);
end;

procedure TSobo63.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo63.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     if Seak20.ShowModal=mrOK then begin
     Button301Click(Self);
     Button015Click(Self);
     end;
  end;   
end;

procedure TSobo63.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo63.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnM0(oSqry,ProgressBar1);
end;

procedure TSobo63.Button013Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnM0(oSqry,ProgressBar1);
end;

procedure TSobo63.Button014Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button015Click(Sender: TObject);
var A01,A02,B01,B02,C01,C02,D01,D02,E01,E02,F01,F02: Double;
    G01,G02,H01,H02,I01,I02,J01,J02,K01,K02,L01,L02,S01,S02: Double;
begin
  A01:=0; A02:=0;
  B01:=0; B02:=0;
  C01:=0; C02:=0;
  D01:=0; D02:=0;
  E01:=0; E02:=0;
  F01:=0; F02:=0;
  G01:=0; G02:=0;
  H01:=0; H02:=0;
  I01:=0; I02:=0;
  J01:=0; J02:=0;
  K01:=0; K02:=0;
  L01:=0; L02:=0;
  S01:=0; S02:=0;
  if nSqry.Active=True Then begin
     nSqry.First;
     While nSqry.EOF=False do begin
       A01:=A01+nSqry.FieldByName('Aquts').AsFloat;
       B01:=B01+nSqry.FieldByName('Bquts').AsFloat;
       C01:=C01+nSqry.FieldByName('Cquts').AsFloat;
       D01:=D01+nSqry.FieldByName('Dquts').AsFloat;
       E01:=E01+nSqry.FieldByName('Equts').AsFloat;
       F01:=F01+nSqry.FieldByName('Fquts').AsFloat;
       G01:=G01+nSqry.FieldByName('Gquts').AsFloat;
       H01:=H01+nSqry.FieldByName('Hquts').AsFloat;
       I01:=I01+nSqry.FieldByName('Iquts').AsFloat;
       J01:=J01+nSqry.FieldByName('Jquts').AsFloat;
       K01:=K01+nSqry.FieldByName('Kquts').AsFloat;
       L01:=L01+nSqry.FieldByName('Lquts').AsFloat;
       S01:=S01+nSqry.FieldByName('Squts').AsFloat;
       nSqry.Next;
     end;
     DBGrid101.Columns[ 1].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',A01);
     DBGrid101.Columns[ 2].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',B01);
     DBGrid101.Columns[ 3].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',C01);
     DBGrid101.Columns[ 4].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',D01);
     DBGrid101.Columns[ 5].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',E01);
     DBGrid101.Columns[ 6].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',F01);
     DBGrid101.Columns[ 7].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',G01);
     DBGrid101.Columns[ 8].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',H01);
     DBGrid101.Columns[ 9].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',I01);
     DBGrid101.Columns[10].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',J01);
     DBGrid101.Columns[11].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',K01);
     DBGrid101.Columns[12].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',L01);
     DBGrid101.Columns[13].Footer.Field.DisplayNullAs:=FormatFloat('###,###,##0',S01);
  end;
end;

procedure TSobo63.Button016Click(Sender: TObject);
begin
  Tong40.print_63_01(Self);
end;

procedure TSobo63.Button017Click(Sender: TObject);
begin
  Tong40.print_63_02(Self);
end;

procedure TSobo63.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button101Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6,St7: String;
begin

  Base10.OpenShow(Base10.H2_Gbun);
  Sqlen := 'Select Hcode,Scode,Gcode,Gname,Jubun,Gdate From H2_Gbun Where '+D_Open;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.H2_Gbun)
  else ShowMessage(E_Open);

  Base10.OpenShow(Base10.T1_Gbun);
  Sqlen := 'Select Hcode,Gcode,Gjisa,Jubun,Gname From T1_Gbun Where '+D_Open;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.T1_Gbun)
  else ShowMessage(E_Open);

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;

  St2:='X';

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+St2+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Hcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Hcode'+'<='+#39+Edit105.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  if(CheckBox2.Checked=True)then
  St1:=St1+' and ((Gjisa<>'+#39+'방문출고'+#39+' and Gcode<>'+#39+'00002'+#39+'))';
//St1:=St1+' and (Gjisa<>'+#39+'방문출고'+#39+')';

  {-S1_Ssub-}
  Sqlen :=
  'Select Hcode,substring(Gdate,1,7),Sum(Gsqut)as Gsqut '+
  'From S1_Ssub Where '+D_Select+St1+
  'Group By Hcode,substring(Gdate,1,7) ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  ProgressBar1.Max:=SGrid.RowCount-1;
  While SGrid.RowCount-1 > List1 do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  List1:=List1+1;

    T01:=StrToInt64Def(SGrid.Cells[ 2,List1],0);

    St3:=SGrid.Cells[ 0,List1];
    St4:='';
    St5:='';
    St6:=Copy(SGrid.Cells[ 1,List1],6,2);
    St7:='';

    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin
      if Base10.G7_Ggeo.Locate('Gcode',St3,[loCaseInsensitive])=true then
      St7:=Base10.G7_Ggeo.FieldByName('Gname').AsString;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St7;
    end;

    nSqry.Edit;
    if St6='01' Then begin
      nSqry.FieldByName('Aquts').AsFloat:=nSqry.FieldByName('Aquts').AsFloat+T01;
    end else
    if St6='02' Then begin
      nSqry.FieldByName('Bquts').AsFloat:=nSqry.FieldByName('Bquts').AsFloat+T01;
    end else
    if St6='03' Then begin
      nSqry.FieldByName('Cquts').AsFloat:=nSqry.FieldByName('Cquts').AsFloat+T01;
    end else
    if St6='04' Then begin
      nSqry.FieldByName('Dquts').AsFloat:=nSqry.FieldByName('Dquts').AsFloat+T01;
    end else
    if St6='05' Then begin
      nSqry.FieldByName('Equts').AsFloat:=nSqry.FieldByName('Equts').AsFloat+T01;
    end else
    if St6='06' Then begin
      nSqry.FieldByName('Fquts').AsFloat:=nSqry.FieldByName('Fquts').AsFloat+T01;
    end else
    if St6='07' Then begin
      nSqry.FieldByName('Gquts').AsFloat:=nSqry.FieldByName('Gquts').AsFloat+T01;
    end else
    if St6='08' Then begin
      nSqry.FieldByName('Hquts').AsFloat:=nSqry.FieldByName('Hquts').AsFloat+T01;
    end else
    if St6='09' Then begin
      nSqry.FieldByName('Iquts').AsFloat:=nSqry.FieldByName('Iquts').AsFloat+T01;
    end else
    if St6='10' Then begin
      nSqry.FieldByName('Jquts').AsFloat:=nSqry.FieldByName('Jquts').AsFloat+T01;
    end else
    if St6='11' Then begin
      nSqry.FieldByName('Kquts').AsFloat:=nSqry.FieldByName('Kquts').AsFloat+T01;
    end else
    if St6='12' Then begin
      nSqry.FieldByName('Lquts').AsFloat:=nSqry.FieldByName('Lquts').AsFloat+T01;
    end;
      nSqry.FieldByName('Squts').AsFloat:=nSqry.FieldByName('Squts').AsFloat+T01;
    nSqry.Post;
  end;

  Button301Click(Self);
  Button015Click(Self);

  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo63.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo63.Button301Click(Sender: TObject);
begin
  Button201Click(Self);

if nSqry.Active=True Then begin
  DBGrid101.ClearText;
  DBGrid101.DataRowCount:=nSqry.RecordCount;
  nSqry.First;
  While nSqry.EOF=False do begin
    DBGrid101.Cells[0,nSqry.RecNo-1]:=nSqry.FieldByName('Gname').AsString;
    if nSqry.FieldByName('Aquts').AsString<>'' then
    DBGrid101.Cells[1,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Aquts').AsFloat);
    if nSqry.FieldByName('Bquts').AsString<>'' then
    DBGrid101.Cells[2,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Bquts').AsFloat);
    if nSqry.FieldByName('Cquts').AsString<>'' then
    DBGrid101.Cells[3,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Cquts').AsFloat);
    if nSqry.FieldByName('Dquts').AsString<>'' then
    DBGrid101.Cells[4,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Dquts').AsFloat);
    if nSqry.FieldByName('Equts').AsString<>'' then
    DBGrid101.Cells[5,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Equts').AsFloat);
    if nSqry.FieldByName('Fquts').AsString<>'' then
    DBGrid101.Cells[6,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Fquts').AsFloat);
    if nSqry.FieldByName('Gquts').AsString<>'' then
    DBGrid101.Cells[7,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Gquts').AsFloat);
    if nSqry.FieldByName('Hquts').AsString<>'' then
    DBGrid101.Cells[8,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Hquts').AsFloat);
    if nSqry.FieldByName('Iquts').AsString<>'' then
    DBGrid101.Cells[9,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Iquts').AsFloat);
    if nSqry.FieldByName('Jquts').AsString<>'' then
    DBGrid101.Cells[10,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Jquts').AsFloat);
    if nSqry.FieldByName('Kquts').AsString<>'' then
    DBGrid101.Cells[11,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Kquts').AsFloat);
    if nSqry.FieldByName('Lquts').AsString<>'' then
    DBGrid101.Cells[12,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Lquts').AsFloat);
    if nSqry.FieldByName('Squts').AsString<>'' then
    DBGrid101.Cells[13,nSqry.RecNo-1]:=FormatFloat('###,###,##0',nSqry.FieldByName('Squts').AsFloat);
    nSqry.Next;
  end;

  ApplyCellHoles;
end;
end;

procedure TSobo63.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit104.Focused=True)and(Edit104.SelStart=50)and(Length(Trim(Edit104.Text))=50))or
    ((Edit106.Focused=True)and(Edit106.SelStart=50)and(Length(Trim(Edit106.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo63.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo63.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo63.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo63.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo63.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if(Edit104.Focused=True)Then begin
       Edit103.Text:='';
    if Edit104.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit104.Text;
    Seak80.FilterTing(Edit104.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seak80.Query1Gcode.AsString;
      Edit104.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seak80.Query1Gcode.AsString;
      Edit104.Text:=Seak80.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if(Edit106.Focused=True)Then begin
       Edit105.Text:='';
    if Edit106.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit106.Text;
    Seak80.FilterTing(Edit106.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit105.Text:=Seak80.Query1Gcode.AsString;
      Edit106.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit105.Text:=Seak80.Query1Gcode.AsString;
      Edit106.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo63.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo63.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo63.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo63.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo63.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo63.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo63.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo63.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo63.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo63.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo63.DateEdit2ButtonClick(Sender: TObject);
begin
  DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo63.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo63.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo63.Button700Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit104.Text;
  if Edit104.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit104.Text);
  if Seak80.Query1.RecordCount=1 Then begin
    Edit103.Text:=Seak80.Query1Gcode.AsString;
    Edit104.Text:=Seak80.Query1Gname.AsString;
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit103.Text:=Seak80.Query1Gcode.AsString;
    Edit104.Text:=Seak80.Query1Gname.AsString;
  end;
end;

procedure TSobo63.Button701Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit106.Text;
  if Edit106.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit106.Text);
  if Seak80.Query1.RecordCount=1 Then begin
    Edit105.Text:=Seak80.Query1Gcode.AsString;
    Edit106.Text:=Seak80.Query1Gname.AsString;
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit105.Text:=Seak80.Query1Gcode.AsString;
    Edit106.Text:=Seak80.Query1Gname.AsString;
  end;
end;

procedure TSobo63.ApplyCellHoles;
var
  ACol, ARow : integer;
  Value1, Value2 : string;
begin
  with DBGrid101 do
  begin
    for ACol := 0 to DataColCount -1 do
      for ARow := 0 to DataRowCount-1 do
        BodyHoles[ACol, ARow] := [];

    for ACol := 0 to 0 do
      for ARow := 0 to DataRowCount-1 do
      begin
        Value1 := trim( Cells[ACol, ARow] );
        Value2 := trim( Cells[ACol, ARow+1] );
        if (Value1 = Value2)
        then BodyHoles[ACol, ARow] := BodyHoles[ACol, ARow] + [imchBottom];
      end;
  end;
end;

end.
