unit Subu36;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ToolEdit, DBClient,
  DBGridEh, CornerButton, dxCore, dxButtons;

type
  TSobo36 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel007: TFlatPanel;
    Panel101: TFlatPanel;
    Panel104: TFlatPanel;
    Panel102: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Button201: TFlatButton;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    DateEdit1: TDateEdit;
    Button700: TFlatButton;
    Panel003: TFlatPanel;
    Panel301: TFlatPanel;
    Panel305: TFlatPanel;
    Panel302: TFlatPanel;
    Edit305: TFlatEdit;
    Edit302: TFlatEdit;
    Edit301: TFlatEdit;
    Edit304: TFlatEdit;
    Button701: TFlatButton;
    Panel304: TFlatPanel;
    Panel303: TFlatPanel;
    Panel306: TFlatPanel;
    Edit303: TFlatEdit;
    Edit306: TFlatEdit;
    Panel307: TFlatPanel;
    Edit307: TFlatEdit;
    Panel308: TFlatPanel;
    Edit308: TFlatNumber;
    BitBtn101: TBitBtn;
    BitBtn102: TBitBtn;
    BitBtn103: TBitBtn;
    BitBtn104: TBitBtn;
    BitBtn105: TBitBtn;
    Edit300: TFlatEdit;
    BitBtn106: TBitBtn;
    T3_Sub61: TClientDataSet;
    T3_Sub61ID: TFloatField;
    T3_Sub61GDATE: TStringField;
    T3_Sub61SCODE: TStringField;
    T3_Sub61GCODE: TStringField;
    T3_Sub61GNAME: TStringField;
    T3_Sub61HCODE: TStringField;
    T3_Sub61HNAME: TStringField;
    T3_Sub61NAME1: TStringField;
    T3_Sub61NAME2: TStringField;
    T3_Sub61GNUMB: TStringField;
    T3_Sub61GBIGO: TStringField;
    T3_Sub61GQUT1: TFloatField;
    T3_Sub62: TClientDataSet;
    T3_Sub62ID: TFloatField;
    T3_Sub62GDATE: TStringField;
    T3_Sub62SCODE: TStringField;
    T3_Sub62GCODE: TStringField;
    T3_Sub62GNAME: TStringField;
    T3_Sub62HCODE: TStringField;
    T3_Sub62HNAME: TStringField;
    T3_Sub62NAME1: TStringField;
    T3_Sub62NAME2: TStringField;
    T3_Sub62GNUMB: TStringField;
    T3_Sub62GBIGO: TStringField;
    T3_Sub62GQUT1: TFloatField;
    T3_Sub61GQUT2: TFloatField;
    T3_Sub62GQUT2: TFloatField;
    Panel309: TFlatPanel;
    Edit309: TFlatNumber;
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
    procedure DBGrid101Enter(Sender: TObject);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101TitleClick(Column: TColumnEh);
    procedure DBGrid201TitleClick(Column: TColumnEh);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button700Click(Sender: TObject);
    procedure Button701Click(Sender: TObject);
    procedure BitBtn101Click(Sender: TObject);
    procedure BitBtn102Click(Sender: TObject);
    procedure BitBtn103Click(Sender: TObject);
    procedure BitBtn104Click(Sender: TObject);
    procedure BitBtn105Click(Sender: TObject);
    procedure BitBtn106Click(Sender: TObject);

    procedure T3_Sub61AfterCancel(DataSet: TDataSet);
    procedure T3_Sub61AfterScroll(DataSet: TDataSet);
    procedure T3_Sub61AfterPost(DataSet: TDataSet);
    procedure T3_Sub61AfterDelete(DataSet: TDataSet);
    procedure T3_Sub61BeforePost(DataSet: TDataSet);
    procedure T3_Sub61BeforeClose(DataSet: TDataSet);
    procedure T3_Sub61NewRecord(DataSet: TDataSet);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo36: TSobo36;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib, Subu20, Seok02,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo36.FormActivate(Sender: TObject);
begin
  nForm:='36';
  nSqry:=T3_Sub61;
  mSqry:=T3_Sub62;
end;

procedure TSobo36.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo36.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo36:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo36.Button001Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end; }
end;

procedure TSobo36.Button002Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Button015Click(Self);
  end; }
end;

procedure TSobo36.Button003Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo36.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo36.Button011Click(Sender: TObject);
begin
{ Tong20.DBGridSaveHtml(DBGrid201, Caption); }
end;

procedure TSobo36.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo36.Button013Click(Sender: TObject);
begin
{ oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1); }
end;

procedure TSobo36.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('36-01');
end;

procedure TSobo36.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('36-02');
end;

procedure TSobo36.Button016Click(Sender: TObject);
begin
  Tong40.print_36_01(Self);
end;

procedure TSobo36.Button017Click(Sender: TObject);
begin
{ Tong40.print_36_02(Self); }
end;

procedure TSobo36.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont4(DBGrid101);
end;

procedure TSobo36.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Button101Click(Sender: TObject);
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

  St1:='Gdate'+'='+#39+Edit101.Text+#39;
  if Edit107.Text<>'' Then
  St1:=St1+' and '+'Hcode'+' ='+#39+Edit107.Text+#39;
  if Edit102.Text<>'' Then
  St1:=St1+' and '+'Gname'+' ='+#39+Edit103.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  St2:=' Order By Gdate,Hcode,Gname';

  {-H1_Ssub-}
  Sqlen := 'Select * From T6_Ssub Where '+D_Select+St1+St2;

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

  //if nSqry.FieldByName('Gcode').AsString<>'' then
  //nSqry.FieldByName('Gname').Value:=Base10.Seek_Hname(nSqry.FieldByName('Gcode').AsString,nSqry.FieldByName('Hcode').AsString);

    nSqry.Post;
    nSqry.Next;
  end;

  nSqry.First;
  Tong20.Srart_36_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=T3_Sub61BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo36.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo36.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit103.Focused=True)and(Edit103.SelStart=50)and(Length(Trim(Edit103.Text))=50))or
    ((Edit108.Focused=True)and(Edit108.SelStart=50)and(Length(Trim(Edit108.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo36.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo36.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo36.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo36.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo36.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo36.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo36.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
      Button101Click(Self);
  end;
end;

procedure TSobo36.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo36.Edit114KeyPress(Sender: TObject; var Key: Char);
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
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if(Edit103.Focused=True)Then begin
  {    Edit102.Text:='';
    if Edit103.Text<>'' Then begin
    Seek10.Edit1.Text:=Edit103.Text;
    Seek10.FilterTing(Edit103.Text,Edit107.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      Edit102.Text:=Seek10.Query1Gcode.AsString;
      Edit103.Text:=Seek10.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seek10.ShowModal=mrOK Then begin
      Edit102.Text:=Seek10.Query1Gcode.AsString;
      Edit103.Text:=Seek10.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else }
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo36.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo36.DBGrid101Exit(Sender: TObject);
begin
  Base10.T4_Sub31BeforeClose(Base10.T4_Sub31);
end;

procedure TSobo36.DBGrid101Enter(Sender: TObject);
begin
//
end;

procedure TSobo36.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=0 Then begin
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
    end else
    if SIndexs=4 Then begin
      if nSqry.FieldByName('Gname').AsString='' Then Exit;
      Seek10.Edit1.Text:=nSqry.FieldByName('Gname').AsString;
      Seek10.FilterTing(nSqry.FieldByName('Gname').AsString,nSqry.FieldByName('Hcode').AsString);
      if Seek10.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Gcode').Value:=Seek10.Query1Gcode.Value;
        nSqry.FieldByName('Gname').Value:=Seek10.Query1Gname.Value;
        SIndexs:=SIndexs+0;
      end else
      if Seek10.ShowModal=mrOK Then begin
        nSqry.FieldByName('Gcode').Value:=Seek10.Query1Gcode.Value;
        nSqry.FieldByName('Gname').Value:=Seek10.Query1Gname.Value;
        SIndexs:=SIndexs+0;
      end else
        SIndexs:=SIndexs+0;
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end;
end;

procedure TSobo36.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    if SIndexs=7 Then begin
      nSqry.Append; DBGrid101.SelectedIndex:=0;
    end;
  end;
  if sColumn=False Then begin
    if nSqry.IsEmpty=False Then
    if Key=VK_DELETE Then T3_Sub61AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo36.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo36.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo36.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo36.DBGrid201TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(mSqry,Column);
end;

procedure TSobo36.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo36.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo36.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo36.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo36.Button700Click(Sender: TObject);
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

procedure TSobo36.Button701Click(Sender: TObject);
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

procedure TSobo36.BitBtn101Click(Sender: TObject);
begin
  Edit300.Text:='';
  Edit301.Text:='';
  Edit302.Text:='';
  Edit303.Text:='';
  Edit304.Text:='';
  Edit305.Text:='';
  Edit306.Text:='';
  Edit307.Text:='';
  Edit308.Value:=0;
  Edit309.Value:=0;
  Edit301.SetFocus;
end;

procedure TSobo36.BitBtn102Click(Sender: TObject);
begin
  Edit300.Text:=nSqry.FieldByName('ID').AsString;
  Edit301.Text:=nSqry.FieldByName('Hcode').AsString;
  Edit302.Text:=nSqry.FieldByName('Hname').AsString;
  Edit303.Text:=nSqry.FieldByName('Gnumb').AsString;
  Edit304.Text:=nSqry.FieldByName('Name1').AsString;
  Edit305.Text:=nSqry.FieldByName('Gname').AsString;
  Edit306.Text:=nSqry.FieldByName('Name2').AsString;
  Edit307.Text:=nSqry.FieldByName('Gbigo').AsString;
  Edit308.Value:=nSqry.FieldByName('Gqut1').AsFloat;
  Edit309.Value:=nSqry.FieldByName('Gqut2').AsFloat;
  Edit301.SetFocus;
end;

procedure TSobo36.BitBtn103Click(Sender: TObject);
begin
  T3_Sub61AfterDelete(nSqry);
  BitBtn101Click(Self);
  Edit301.SetFocus;
end;

procedure TSobo36.BitBtn104Click(Sender: TObject);
begin
if Edit301.Text<>'' then begin
  if Edit300.Text='' then begin
  nSqry.Append;
  nSqry.FieldByName('Hcode').AsString:=Edit301.Text;
  nSqry.FieldByName('Hname').AsString:=Edit302.Text;
  nSqry.FieldByName('Gnumb').AsString:=Edit303.Text;
  nSqry.FieldByName('Name1').AsString:=Edit304.Text;
  nSqry.FieldByName('Gname').AsString:=Edit305.Text;
  nSqry.FieldByName('Name2').AsString:=Edit306.Text;
  nSqry.FieldByName('Gbigo').AsString:=Edit307.Text;
  nSqry.FieldByName('Gqut1').AsFloat:=Edit308.Value;
  nSqry.FieldByName('Gqut2').AsFloat:=Edit309.Value;
  nSqry.Post;
  end else begin
  nSqry.Edit;
  nSqry.FieldByName('Hcode').AsString:=Edit301.Text;
  nSqry.FieldByName('Hname').AsString:=Edit302.Text;
  nSqry.FieldByName('Gnumb').AsString:=Edit303.Text;
  nSqry.FieldByName('Name1').AsString:=Edit304.Text;
  nSqry.FieldByName('Gname').AsString:=Edit305.Text;
  nSqry.FieldByName('Name2').AsString:=Edit306.Text;
  nSqry.FieldByName('Gbigo').AsString:=Edit307.Text;
  nSqry.FieldByName('Gqut1').AsFloat:=Edit308.Value;
  nSqry.FieldByName('Gqut2').AsFloat:=Edit309.Value;
  nSqry.Post;
  end;
  BitBtn101Click(Self);
  Edit301.SetFocus;
end else begin
  ShowMessage('출판사를 등록해 주세요.');
  Edit301.SetFocus;
end;
end;

procedure TSobo36.BitBtn105Click(Sender: TObject);
begin
  BitBtn101Click(Self);
  Edit301.SetFocus;
end;

procedure TSobo36.BitBtn106Click(Sender: TObject);
begin
//if nSqry.Active=True Then
{ if Seok20.ShowModal=mrOK Then begin
    Seok20.Query1.First;
    While Seok20.Query1.EOF=False do begin
      if Seok20.Query1.FieldByName('Code5').AsString='O' then begin
        nSqry.Append;
        nSqry.FieldByName('Hcode').AsString:=Seok20.Query1.FieldByName('Hcode').AsString;
        nSqry.FieldByName('Hname').AsString:=Seok20.Query1.FieldByName('Hname').AsString;
        nSqry.FieldByName('Gnumb').AsString:=Seok20.Query1.FieldByName('Gnumb').AsString;
        nSqry.FieldByName('Name1').AsString:=Seok20.Query1.FieldByName('Name1').AsString;
        nSqry.FieldByName('Gname').AsString:=Seok20.Query1.FieldByName('Gname').AsString;
        nSqry.FieldByName('Name2').AsString:=Seok20.Query1.FieldByName('Name2').AsString;
        nSqry.FieldByName('Gbigo').AsString:=Seok20.Query1.FieldByName('Gbigo').AsString;
        nSqry.FieldByName('Gqut1').AsString:=Seok20.Query1.FieldByName('Gqut1').AsString;
        nSqry.FieldByName('Gqut2').AsString:=Seok20.Query1.FieldByName('Gqut2').AsString;
        nSqry.Post;
      end;
      Seok20.Query1.Next;
    end;
  end; }
end;

//--반품수거--//
procedure TSobo36.T3_Sub61AfterCancel(DataSet: TDataSet);
begin
  T3_Sub61AfterScroll(T3_Sub61);
end;

procedure TSobo36.T3_Sub61AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T3_Sub61.FieldByName('Gdate').AsString;
{ Gqut1:=-T3_Sub61.FieldByName('Gqut1').AsFloat;
  Gqut2:=-T3_Sub61.FieldByName('Gqut2').AsFloat; }
end;

procedure TSobo36.T3_Sub61AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TSobo36.T3_Sub61AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    Sqlen := 'DELETE FROM T6_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
    TransAuto(Sqlen, '@ID',    T3_Sub61ID.AsString);
    Translate(Sqlen, '@Gdate', T3_Sub61Gdate.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T3_Sub61.Delete;

  end; end;

end;

procedure TSobo36.T3_Sub61BeforePost(DataSet: TDataSet);
begin

  if(T3_Sub61.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO T6_Ssub '+
    '(Gdate, Hcode, Gcode, Gname, Name1, Name2, Gnumb, Gbigo, Gqut1, Gqut2) VALUES '+
    '(''@Gdate'',''@Hcode'',''@Gcode'',''@Gname'',''@Name1'',''@Name2'',''@Gnumb'',''@Gbigo'', @Gqut1 , @Gqut2 )';

    Translate(Sqlen, '@Gdate', T3_Sub61Gdate.AsString);
    Translate(Sqlen, '@Hcode', T3_Sub61Hcode.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub61Gcode.AsString);
    Translate(Sqlen, '@Gname', T3_Sub61Gname.AsString);
    Translate(Sqlen, '@Name1', T3_Sub61Name1.AsString);
    Translate(Sqlen, '@Name2', T3_Sub61Name2.AsString);
    Translate(Sqlen, '@Gnumb', T3_Sub61Gnumb.AsString);
    Translate(Sqlen, '@Gbigo', T3_Sub61Gbigo.AsString);
    TransAuto(Sqlen, '@Gqut1', T3_Sub61Gqut1.AsString);
    TransAuto(Sqlen, '@Gqut2', T3_Sub61Gqut2.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'T6_SSUB_ID_GEN');

  end else begin

    Sqlen := 'UPDATE T6_Ssub SET '+
    'Gdate=''@Gdate'',Hcode=''@Hcode'',Gcode=''@Gcode'',Gname=''@Gname'','+
    'Name1=''@Name1'',Name2=''@Name2'',Gnumb=''@Gnumb'',Gbigo=''@Gbigo'',Gqut1= @Gqut1, Gqut2= @Gqut2 '+
    'WHERE ID=@ID and Gdate=''@Sdate''';

    Translate(Sqlen, '@Gdate', T3_Sub61Gdate.AsString);
    Translate(Sqlen, '@Hcode', T3_Sub61Hcode.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub61Gcode.AsString);
    Translate(Sqlen, '@Gname', T3_Sub61Gname.AsString);
    Translate(Sqlen, '@Name1', T3_Sub61Name1.AsString);
    Translate(Sqlen, '@Name2', T3_Sub61Name2.AsString);
    Translate(Sqlen, '@Gnumb', T3_Sub61Gnumb.AsString);
    Translate(Sqlen, '@Gbigo', T3_Sub61Gbigo.AsString);
    TransAuto(Sqlen, '@Gqut1', T3_Sub61Gqut1.AsString);
    TransAuto(Sqlen, '@Gqut2', T3_Sub61Gqut2.AsString);
    TransAuto(Sqlen, '@ID',    T3_Sub61ID.AsString);
    Translate(Sqlen, '@Sdate', Gdate);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TSobo36.T3_Sub61BeforeClose(DataSet: TDataSet);
begin
  With T3_Sub61 do
  if(State in dsEditModes)Then Post;
end;

procedure TSobo36.T3_Sub61NewRecord(DataSet: TDataSet);
begin
  T3_Sub61Gqut1.Value:=0;
  T3_Sub61Gqut2.Value:=0;
  T3_Sub61Gdate.Value:=Sobo36.Edit101.Text;
end;

end.
