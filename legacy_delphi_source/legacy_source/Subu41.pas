unit Subu41;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ToolEdit,
  CornerButton, DBGridEh, dxCore, dxButtons;

type
  TSobo41 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Button201: TFlatButton;
    Panel101: TFlatPanel;
    Edit101: TFlatMaskEdit;
    DateEdit1: TDateEdit;
    Label101: TmyLabel3d;
    Edit102: TFlatMaskEdit;
    DateEdit2: TDateEdit;
    Panel102: TFlatPanel;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Button700: TFlatButton;
    Panel003: TFlatPanel;
    Panel301: TFlatPanel;
    Panel305: TFlatPanel;
    Panel302: TFlatPanel;
    Edit302: TFlatEdit;
    Edit301: TFlatEdit;
    Button701: TFlatButton;
    Panel304: TFlatPanel;
    Panel306: TFlatPanel;
    Edit306: TFlatEdit;
    Panel307: TFlatPanel;
    Edit305: TFlatNumber;
    BitBtn101: TBitBtn;
    BitBtn102: TBitBtn;
    BitBtn103: TBitBtn;
    BitBtn104: TBitBtn;
    BitBtn105: TBitBtn;
    Edit303: TFlatMaskEdit;
    Edit304: TFlatComboBox;
    Edit300: TFlatEdit;
    DateEdit3: TDateEdit;
    Edit307: TFlatComboBox;
    FlatPanel1: TFlatPanel;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    DBGrid101: TDBGridEh;
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
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit2ButtonClick(Sender: TObject);
    procedure DateEdit3ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit3AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button700Click(Sender: TObject);
    procedure Button701Click(Sender: TObject);
    procedure BitBtn101Click(Sender: TObject);
    procedure BitBtn102Click(Sender: TObject);
    procedure BitBtn103Click(Sender: TObject);
    procedure BitBtn104Click(Sender: TObject);
    procedure BitBtn105Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo41: TSobo41;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib, globalCommon,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo41.FormActivate(Sender: TObject);
begin
  nForm:='41';
  nSqry:=Base10.T4_Sub11;
  mSqry:=Base10.T4_Sub12;
end;

procedure TSobo41.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit303.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  SetMonth2Combo(TCombobox(Edit307));
end;

procedure TSobo41.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo41:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo41.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('41');
end;

procedure TSobo41.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('41');
end;

procedure TSobo41.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo41.Button011Click(Sender: TObject);
begin
{ Tong20.DBGridSaveHtml(DBGrid201, Caption); }
end;

procedure TSobo41.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo41.Button013Click(Sender: TObject);
begin
{ oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1); }
end;

procedure TSobo41.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('41-01');
end;

procedure TSobo41.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('41-02');
end;

procedure TSobo41.Button016Click(Sender: TObject);
begin
  Tong40.print_41_01(Self);
end;

procedure TSobo41.Button017Click(Sender: TObject);
begin
{ Tong40.print_41_02(Self); }
end;

procedure TSobo41.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont4(DBGrid101);
end;

procedure TSobo41.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Button101Click(Sender: TObject);
var St1,St2: String;
begin
//if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;

  St2:='X';

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39;

  if Edit107.Text<>'' Then
  St1:=St1+' and '+'Hcode'+' ='+#39+Edit107.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  St2:=' Order By Gdate,Hcode';

  {-T5_Ssub-}
  Sqlen := 'Select * From T5_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  nSqry.First;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    nSqry.Edit;

    Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Hcode').AsString);
    nSqry.FieldByName('Hname').Value:=Base10.Seek_Name(Sqlen);

    nSqry.Post;
    nSqry.Next;
  end;

  nSqry.First;
  Tong20.Srart_41_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=Base10.T4_Sub11BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo41.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo41.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit107.Focused=True)and(Edit107.SelStart=05)and(Length(Trim(Edit107.Text))=05))or
    ((Edit108.Focused=True)and(Edit108.SelStart=50)and(Length(Trim(Edit108.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo41.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo41.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo41.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo41.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo41.Edit112KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    Edits: TFlatComboBox;
begin
  Hands:=Edit304.Handle;
  Edits:=Edit304;
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

procedure TSobo41.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit304;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo41.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
      Button101Click(Self);
  end;    
end;

procedure TSobo41.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo41.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if Edit301.Focused=True Then begin
       Edit302.Text:='';
    if Edit301.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit301.Text;
    Seak80.FilterTing(Edit301.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit301.Text:=Seak80.Query1Gcode.AsString;
      Edit302.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit301.Text:=Seak80.Query1Gcode.AsString;
      Edit302.Text:=Seak80.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
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

procedure TSobo41.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo41.DBGrid101Exit(Sender: TObject);
begin
  Base10.T4_Sub11BeforeClose(Base10.T4_Sub11);
end;

procedure TSobo41.DBGrid201Exit(Sender: TObject);
begin
//
end;

procedure TSobo41.DBGrid101Enter(Sender: TObject);
begin
  Base10.T4_Sub11AfterScroll(Base10.T4_Sub11);
end;

procedure TSobo41.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo41.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sIndexs: Integer;
    sColumn: Boolean;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=1 Then begin
      if nSqry.FieldByName('Hcode').AsString='' Then Exit;
      Seak80.Edit1.Text:=nSqry.FieldByName('Hcode').AsString;
      Seak80.FilterTing(nSqry.FieldByName('Hcode').AsString);
      if Seak80.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Hcode').Value:=Seak80.Query1Gcode.Value;
        nSqry.FieldByName('Hname').Value:=Seak80.Query1Gname.Value;
        SIndexs:=SIndexs+1;
      end else
      if Seak80.ShowModal=mrOK Then begin
        nSqry.FieldByName('Hcode').Value:=Seak80.Query1Gcode.Value;
        nSqry.FieldByName('Hname').Value:=Seak80.Query1Gname.Value;
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end;
end;

procedure TSobo41.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sIndexs: Integer;
    sColumn: Boolean;
    MeDlg: Integer;
    St1,St2: String;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    if SIndexs=4 Then begin
      DBGrid101.Columns.Items[SIndexs].Grid.EditorMode:=False;
      Keybd_event(VK_MENU,MapVirtualKey(VK_MENU,0),0,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),0,0);
      Keybd_event(VK_MENU,MapVirtualKey(VK_MENU,0),KEYEVENTF_KEYUP,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),KEYEVENTF_KEYUP,0);
    end else
    if SIndexs=5 Then begin
      nSqry.Append; DBGrid101.SelectedIndex:=0;
    end;
  end;
  if sColumn=False Then begin
    if nSqry.IsEmpty=False Then
    if Key=VK_DELETE Then Base10.T4_Sub11AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo41.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo41.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo41.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo41.DBGrid201TitleClick(Column: TColumnEh);
begin
//
end;

procedure TSobo41.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo41.DataSource2DataChange(Sender: TObject; Field: TField);
begin
//
end;

procedure TSobo41.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo41.DateEdit2ButtonClick(Sender: TObject);
begin
  DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo41.DateEdit3ButtonClick(Sender: TObject);
begin
  DateEdit3.Date :=StrToDate(Edit303.Text);
end;

procedure TSobo41.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo41.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo41.DateEdit3AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit303.Text :=DateToStr(ADate);
end;

procedure TSobo41.Button700Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit108.Text;
  if Edit108.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit108.Text);
  if Seak80.Query1.RecordCount=1 Then begin
    Edit107.Text:=Seak80.Query1Gcode.AsString;
    Edit108.Text:=Seak80.Query1Gname.AsString;
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit107.Text:=Seak80.Query1Gcode.AsString;
    Edit108.Text:=Seak80.Query1Gname.AsString;
  end;
end;

procedure TSobo41.Button701Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit301.Text;
  if Edit301.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit301.Text);
  if Seak80.Query1.RecordCount=1 Then begin
    Edit301.Text:=Seak80.Query1Gcode.AsString;
    Edit302.Text:=Seak80.Query1Gname.AsString;
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit301.Text:=Seak80.Query1Gcode.AsString;
    Edit302.Text:=Seak80.Query1Gname.AsString;
  end;
end;

procedure TSobo41.BitBtn101Click(Sender: TObject);
begin
  Edit300.Text:='';
  Edit301.Text:='';
  Edit302.Text:='';
  Edit303.Text:=Edit101.Text;
  Edit304.ItemIndex:=0;
  Edit305.Value:=0;
  Edit306.Text:='';
  Edit303.SetFocus;
end;

procedure TSobo41.BitBtn102Click(Sender: TObject);
begin
  Edit300.Text:=nSqry.FieldByName('ID').AsString;
  Edit301.Text:=nSqry.FieldByName('Hcode').AsString;
  Edit302.Text:=nSqry.FieldByName('Hname').AsString;
  Edit303.Text:=nSqry.FieldByName('Gdate').AsString;
  Edit304.Text:=nSqry.FieldByName('Pubun').AsString;
  Edit305.Value:=nSqry.FieldByName('Gssum').AsFloat;
  Edit306.Text:=nSqry.FieldByName('Gbigo').AsString;
  Edit307.Text:=nSqry.FieldByName('Sdate').AsString;
  Edit303.SetFocus;
end;

procedure TSobo41.BitBtn103Click(Sender: TObject);
begin
  Base10.T4_Sub11AfterDelete(nSqry);
  BitBtn101Click(Self);
  Edit303.SetFocus;
end;

procedure TSobo41.BitBtn104Click(Sender: TObject);
begin
if Edit301.Text<>'' then begin
  if Edit300.Text='' then begin
  nSqry.Append;
  nSqry.FieldByName('Hcode').AsString:=Edit301.Text;
  nSqry.FieldByName('Hname').AsString:=Edit302.Text;
  nSqry.FieldByName('Gdate').AsString:=Edit303.Text;
  nSqry.FieldByName('Pubun').AsString:=Edit304.Text;
  nSqry.FieldByName('Gssum').AsFloat:=Edit305.Value;
  nSqry.FieldByName('Gbigo').AsString:=Edit306.Text;
  nSqry.FieldByName('Sdate').AsString:=Edit307.Text;
  nSqry.Post;
  end else begin
  nSqry.Edit;
  nSqry.FieldByName('Hcode').AsString:=Edit301.Text;
  nSqry.FieldByName('Hname').AsString:=Edit302.Text;
  nSqry.FieldByName('Gdate').AsString:=Edit303.Text;
  nSqry.FieldByName('Pubun').AsString:=Edit304.Text;
  nSqry.FieldByName('Gssum').AsFloat:=Edit305.Value;
  nSqry.FieldByName('Gbigo').AsString:=Edit306.Text;
  nSqry.FieldByName('Sdate').AsString:=Edit307.Text;
  nSqry.Post;
  end;
  BitBtn101Click(Self);
  Edit303.SetFocus;
end else begin
  ShowMessage('출판사를 등록해 주세요.');
  Edit303.SetFocus;
end;
end;

procedure TSobo41.BitBtn105Click(Sender: TObject);
begin
  BitBtn101Click(Self);
  Edit303.SetFocus;
end;

end.
