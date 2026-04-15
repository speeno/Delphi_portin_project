unit Subu42_1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ToolEdit, DBClient,
  DBGridEh, dxCore, dxButtons, CornerButton;

type
  TSobo42_1 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    Button101: TFlatButton;
    ProgressBar1: TProgressBar;
    Button201: TFlatButton;
    Panel101: TFlatPanel;
    DateEdit1: TDateEdit;
    Panel102: TFlatPanel;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Button700: TFlatButton;
    Edit101: TFlatComboBox;
    Edit102: TFlatComboBox;
    DateEdit2: TDateEdit;
    Label101: TmyLabel3d;
    T4_Sub21: TClientDataSet;
    T4_Sub21ID: TFloatField;
    T4_Sub21GDATE: TStringField;
    T4_Sub21HCODE: TStringField;
    T4_Sub21HNAME: TStringField;
    T4_Sub21GUBUN: TStringField;
    T4_Sub21GSUMX: TFloatField;
    T4_Sub21GOSUM: TFloatField;
    T4_Sub21GBSUM: TFloatField;
    T4_Sub21GSSUM: TFloatField;
    T4_Sub21GSUSU: TFloatField;
    T4_Sub21GSUMY: TFloatField;
    T4_Sub21SDATE: TStringField;
    T4_Sub21GPSUM: TFloatField;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    dxButton1: TdxButton;
    DBGrid101: TDBGridEh;
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
    procedure Edit101Change(Sender: TObject);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit111KeyPress(Sender: TObject; var Key: Char);
    procedure Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit112KeyPress(Sender: TObject; var Key: Char);
    procedure Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit113KeyPress(Sender: TObject; var Key: Char);
    procedure Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
    procedure Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101Exit(Sender: TObject);
    procedure DBGrid201Exit(Sender: TObject);
    procedure DBGrid101Enter(Sender: TObject);
    procedure DBGrid201Enter(Sender: TObject);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101TitleClick(Column: TColumnEh);
    procedure DBGrid201TitleClick(Column: TColumnEh);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure Button700Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo42_1: TSobo42_1;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo42_1.FormActivate(Sender: TObject);
begin
  nForm:='42_1';
  nSqry:=T4_Sub21;
//mSqry:=Base10.T4_Sub22;
end;

procedure TSobo42_1.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"',Date);
end;

procedure TSobo42_1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo42_1:=nil;
  Base10.OpenExit(nSqry);
//Base10.OpenExit(mSqry);
end;

procedure TSobo42_1.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('42');
end;

procedure TSobo42_1.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('42');
end;

procedure TSobo42_1.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo42_1.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo42_1.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('42-01');
end;

procedure TSobo42_1.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('42-02');
end;

procedure TSobo42_1.Button016Click(Sender: TObject);
begin
  Tong40.print_42_02(Self);
end;

procedure TSobo42_1.Button017Click(Sender: TObject);
begin
{ Tong40.print_42_02(Self); }
end;

procedure TSobo42_1.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont4(DBGrid101);
end;

procedure TSobo42_1.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Button101Click(Sender: TObject);
var St1,St2: String;
begin
//if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  DataSource1.Enabled:=False;

  Refresh;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39;

  if Edit107.Text<>'' Then
  St1:=St1+' and '+'Hcode'+' ='+#39+Edit107.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  St2:=' Order By Gdate';

  Sqlen := 'Select Gdate,Sum26,Sum27,Sum28 From T2_Ssub Where '+D_Select+St1+St2;

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

    St2:=SGrid.Cells[ 0,List1];
    if nSqry.Locate('Sdate',St2,[loCaseInsensitive])=False then begin
      nSqry.Append;
      nSqry.FieldByName('Sdate').Value:=St2;
    end;

    nSqry.Edit;
    nSqry.FieldByName('GsumX').AsFloat:=
    nSqry.FieldByName('GsumX').AsFloat+ StrToIntDef(SGrid.Cells[ 1,List1],0);
    nSqry.FieldByName('Gosum').AsFloat:=
    nSqry.FieldByName('Gosum').AsFloat+ StrToIntDef(SGrid.Cells[ 2,List1],0);
    nSqry.FieldByName('Gbsum').AsFloat:=
    nSqry.FieldByName('Gbsum').AsFloat+ StrToIntDef(SGrid.Cells[ 3,List1],0);
    nSqry.FieldByName('Gpsum').AsFloat:=
    nSqry.FieldByName('Gpsum').AsFloat+ StrToIntDef(SGrid.Cells[ 2,List1],0)+ StrToIntDef(SGrid.Cells[ 3,List1],0);
    nSqry.FieldByName('Gssum').AsFloat:=
    nSqry.FieldByName('Gssum').AsFloat+ StrToIntDef(SGrid.Cells[ 1,List1],0)+
                                        StrToIntDef(SGrid.Cells[ 2,List1],0)+
                                        StrToIntDef(SGrid.Cells[ 3,List1],0);
    nSqry.FieldByName('GsumY').AsFloat:=
    nSqry.FieldByName('GsumY').AsFloat+ StrToIntDef(SGrid.Cells[ 1,List1],0)+
                                        StrToIntDef(SGrid.Cells[ 2,List1],0)+
                                        StrToIntDef(SGrid.Cells[ 3,List1],0);

    nSqry.Post;
  end;

  St1:='Sdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Sdate'+'<='+#39+Edit102.Text+#39;

  if Edit107.Text<>'' Then
  St1:=St1+' and '+'Hcode'+' ='+#39+Edit107.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  St2:=' Order By Sdate';

  Sqlen := 'Select Sdate,Gdate,Gssum From T5_Ssub Where '+D_Select+St1+St2;

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

    St2:=SGrid.Cells[ 0,List1];
    if nSqry.Locate('Sdate',St2,[loCaseInsensitive])=False then begin
      nSqry.Append;
      nSqry.FieldByName('Sdate').Value:=St2;
    end;
    nSqry.Edit;
    if nSqry.FieldByName('Gdate').AsString='' then
    nSqry.FieldByName('Gdate').AsString:=SGrid.Cells[ 1,List1];
    nSqry.FieldByName('Gsusu').AsFloat:=
    nSqry.FieldByName('Gsusu').AsFloat +StrToIntDef(SGrid.Cells[ 2,List1],0);
    nSqry.FieldByName('GsumY').AsFloat:=
    nSqry.FieldByName('GsumY').AsFloat -StrToIntDef(SGrid.Cells[ 2,List1],0);
    nSqry.Post;
  end;

  nSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo42_1.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo42_1.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit107.Focused=True)and(Edit107.SelStart=05)and(Length(Trim(Edit107.Text))=05))or
    ((Edit108.Focused=True)and(Edit108.SelStart=50)and(Length(Trim(Edit108.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo42_1.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo42_1.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo42_1.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo42_1.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo42_1.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo42_1.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo42_1.Edit113KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    Edits: TFlatComboBox;
begin
  Hands:=Edit101.Handle;
  Edits:=Edit101;
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

procedure TSobo42_1.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit101;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo42_1.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if Edit108.Focused=True Then begin
       Edit107.Text:='';
    if Edit108.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit108.Text;
    Seak80.FilterTing(Edit108.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seak80.ShowModal=mrOK Then begin
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo42_1.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo42_1.DBGrid101Exit(Sender: TObject);
begin
//
end;

procedure TSobo42_1.DBGrid201Exit(Sender: TObject);
begin
//
end;

procedure TSobo42_1.DBGrid101Enter(Sender: TObject);
begin
//
end;

procedure TSobo42_1.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo42_1.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo42_1.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo42_1.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo42_1.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo42_1.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo42_1.DBGrid201TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(mSqry,Column);
end;

procedure TSobo42_1.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo42_1.DataSource2DataChange(Sender: TObject; Field: TField);
var St1: String;
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo42_1.Button700Click(Sender: TObject);
begin
    Seak80.Edit1.Text:='';
    Seak80.FilterTing('');
    if Seak80.Query1.RecordCount=1 Then begin
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
    end;
end;

end.
