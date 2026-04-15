unit Subu39_5;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ToolEdit, DBClient,
  CornerButton, DBGridEh, dxCore, dxButtons;

type
  TSobo39_5 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    Panel101: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Label101: TmyLabel3d;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatMaskEdit;
    Panel104: TFlatPanel;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Button201: TFlatButton;
    Panel102: TFlatPanel;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Edit106: TFlatEdit;
    Label102: TmyLabel3d;
    DateEdit1: TDateEdit;
    DateEdit2: TDateEdit;
    Button700: TFlatButton;
    Button701: TFlatButton;
    Button702: TFlatButton;
    T3_Sub01: TClientDataSet;
    T3_Sub01ID: TFloatField;
    T3_Sub01GDATE: TStringField;
    T3_Sub01GUBUN: TStringField;
    T3_Sub01GCODE: TStringField;
    T3_Sub01HCODE: TStringField;
    T3_Sub01GNAME: TStringField;
    T3_Sub01GSQUT: TFloatField;
    T3_Sub01GBIGO: TStringField;
    T3_Sub01SCODE: TStringField;
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
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit2ButtonClick(Sender: TObject);
    procedure DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button700Click(Sender: TObject);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure T3_Sub01AfterCancel(DataSet: TDataSet);
    procedure T3_Sub01AfterScroll(DataSet: TDataSet);
    procedure T3_Sub01AfterPost(DataSet: TDataSet);
    procedure T3_Sub01AfterDelete(DataSet: TDataSet);
    procedure T3_Sub01BeforePost(DataSet: TDataSet);
    procedure T3_Sub01BeforeClose(DataSet: TDataSet);
    procedure T3_Sub01NewRecord(DataSet: TDataSet);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo39_5: TSobo39_5;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo39_5.FormActivate(Sender: TObject);
begin
  nForm:='39_5';
  nSqry:=T3_Sub01;
//mSqry:=T3_Sub01;
end;

procedure TSobo39_5.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo39_5.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo39_5:=nil;
  Base10.OpenExit(nSqry);
//Base10.OpenExit(mSqry);
end;

procedure TSobo39_5.Button001Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end; }
end;

procedure TSobo39_5.Button002Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_52_01(Self);
  end; }
end;

procedure TSobo39_5.Button003Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo39_5.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('52');
end;

procedure TSobo39_5.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('52');
end;

procedure TSobo39_5.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo39_5.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo39_5.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('52-01');
end;

procedure TSobo39_5.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('52-02');
end;

procedure TSobo39_5.Button016Click(Sender: TObject);
begin
  Tong40.print_39_11(Self);
end;

procedure TSobo39_5.Button017Click(Sender: TObject);
begin
{ Tong40.print_52_02(Self); }
end;

procedure TSobo39_5.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont4(DBGrid101);
end;

procedure TSobo39_5.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Button101Click(Sender: TObject);
var St1,St2: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;

  Scode:='P';
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Scode'+' ='+#39+Scode+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Gcode'+'<='+#39+Edit105.Text+#39;

  St2:=' Order By Gdate,Gcode';

  {-Sg_Csum-}
  Sqlen := 'Select * From Sb_Csum Where '+D_Select+St1+St2;

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

    if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    St2:=Base10.G4_Book.FieldByName('Gname').AsString;

    if St2='' then
    St2:=Base10.Seek_Code(nSqry.FieldByName('Gcode').AsString,'B',Edit107.Text);

    nSqry.FieldByName('Gname').Value:=St2;

    nSqry.Post;
    nSqry.Next;
  end;

  nSqry.First;
//Tong20.Srart_52_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=T3_Sub01BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo39_5.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo39_5.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit108.Focused=True)and(Edit108.SelStart=50)and(Length(Trim(Edit108.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo39_5.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo39_5.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo39_5.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo39_5.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo39_5.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo39_5.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo39_5.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo39_5.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo39_5.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
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
    end;
  end else
  if(Edit104.Focused=True)Then begin
       Edit103.Text:='';
    if Edit104.Text<>'' Then begin
    Seek40.Edit1.Text:=Edit104.Text;
    Seek40.FilterTing(Edit104.Text,Edit107.Text);
    if Seek40.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek40.Query1Gcode.AsString;
      Edit104.Text:=Seek40.Query1Gname.AsString;
    end else
    if Seek40.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek40.Query1Gcode.AsString;
      Edit104.Text:=Seek40.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if(Edit106.Focused=True)Then begin
       Edit105.Text:='';
    if Edit106.Text<>'' Then begin
    Seek40.Edit1.Text:=Edit106.Text;
    Seek40.FilterTing(Edit106.Text,Edit107.Text);
    if Seek40.Query1.RecordCount=1 Then begin
      Edit105.Text:=Seek40.Query1Gcode.AsString;
      Edit106.Text:=Seek40.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seek40.ShowModal=mrOK Then begin
      Edit105.Text:=Seek40.Query1Gcode.AsString;
      Edit106.Text:=Seek40.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo39_5.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo39_5.DBGrid101Exit(Sender: TObject);
begin
  T3_Sub01BeforeClose(T3_Sub01);
end;

procedure TSobo39_5.DBGrid201Exit(Sender: TObject);
begin
//
end;

procedure TSobo39_5.DBGrid101Enter(Sender: TObject);
begin
  T3_Sub01AfterScroll(T3_Sub01);
end;

procedure TSobo39_5.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo39_5.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
    St1,St2,St3,St4: String;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=1 Then begin
      if nSqry.FieldByName('Gcode').AsString='' Then Exit;
      Seek40.Edit1.Text:=nSqry.FieldByName('Gcode').AsString;
      Seek40.FilterTing(nSqry.FieldByName('Gcode').AsString,Edit107.Text);
      if Seek40.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek40.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek40.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
      if Seek40.ShowModal=mrOK Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek40.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek40.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end;
end;

procedure TSobo39_5.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    if SIndexs=3 Then begin
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
    if Key=VK_DELETE Then T3_Sub01AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo39_5.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo39_5.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo39_5.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo39_5.DBGrid201TitleClick(Column: TColumnEh);
begin
//
end;

procedure TSobo39_5.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo39_5.DataSource2DataChange(Sender: TObject; Field: TField);
begin
//
end;

procedure TSobo39_5.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo39_5.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo39_5.DateEdit2ButtonClick(Sender: TObject);
begin
  DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo39_5.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo39_5.Button700Click(Sender: TObject);
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

procedure TSobo39_5.Button701Click(Sender: TObject);
begin
  Seek40.Edit1.Text:=Edit104.Text;
  if Edit104.Text='' then
  Seek40.FilterTing('',Edit107.Text) else
  Seek40.FilterTing(Edit104.Text,Edit107.Text);
  if Seek40.Query1.RecordCount=1 Then begin
    Edit103.Text:=Seek40.Query1Gcode.AsString;
    Edit104.Text:=Seek40.Query1Gname.AsString;
  end else
  if Seek40.ShowModal=mrOK Then begin
    Edit103.Text:=Seek40.Query1Gcode.AsString;
    Edit104.Text:=Seek40.Query1Gname.AsString;
  end;
end;

procedure TSobo39_5.Button702Click(Sender: TObject);
begin
  Seek40.Edit1.Text:=Edit106.Text;
  if Edit106.Text='' then
  Seek40.FilterTing('',Edit107.Text) else
  Seek40.FilterTing(Edit106.Text,Edit107.Text);
  if Seek40.Query1.RecordCount=1 Then begin
    Edit105.Text:=Seek40.Query1Gcode.AsString;
    Edit106.Text:=Seek40.Query1Gname.AsString;
  end else
  if Seek40.ShowModal=mrOK Then begin
    Edit105.Text:=Seek40.Query1Gcode.AsString;
    Edit106.Text:=Seek40.Query1Gname.AsString;
  end;
end;

//--원장변경--//
procedure TSobo39_5.T3_Sub01AfterCancel(DataSet: TDataSet);
begin
  T3_Sub01AfterScroll(T3_Sub01);
end;

procedure TSobo39_5.T3_Sub01AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T3_Sub01.FieldByName('Gdate').AsString;
  Gsqut:=-T3_Sub01.FieldByName('Gsqut').AsFloat;
end;

procedure TSobo39_5.T3_Sub01AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TSobo39_5.T3_Sub01AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM Sb_Csum WHERE ID=@ID ';
      TransAuto(Sqlen, '@ID',    T3_Sub01ID.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end else begin
      Sqlen := 'UPDATE Sb_Csum SET Scode=''@Scode'' WHERE ID=@ID ';
      TransAuto(Sqlen, '@ID',    T3_Sub01ID.AsString);
      Translate(Sqlen, '@Scode', '4');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end;

    T3_Sub01.Delete;

  end; end;

end;

procedure TSobo39_5.T3_Sub01BeforePost(DataSet: TDataSet);
begin

  if(T3_Sub01.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO Sb_Csum '+
    '(Gdate, Scode, Gcode, Hcode, Gubun, Gbigo, Gsqut) VALUES '+
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Gubun'',''@Gbigo'',  @Gsqut  )';

    Translate(Sqlen, '@Gdate', T3_Sub01Gdate.AsString);
    Translate(Sqlen, '@Scode', T3_Sub01Scode.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub01Gcode.AsString);
    Translate(Sqlen, '@Hcode', T3_Sub01Hcode.AsString);
    Translate(Sqlen, '@Gubun', T3_Sub01Gubun.AsString);
    Translate(Sqlen, '@Gbigo', T3_Sub01Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T3_Sub01Gsqut.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'SB_CSUM_ID_GEN');

  end else begin

    Sqlen := 'UPDATE Sb_Csum SET '+
    'Gdate=''@Gdate'',Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
    'Gubun=''@Gubun'',Gbigo=''@Gbigo'',Gsqut=  @Gsqut  '+
    'WHERE ID=@ID ';

    Translate(Sqlen, '@Gdate', T3_Sub01Gdate.AsString);
    Translate(Sqlen, '@Scode', T3_Sub01Scode.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub01Gcode.AsString);
    Translate(Sqlen, '@Hcode', T3_Sub01Hcode.AsString);
    Translate(Sqlen, '@Gubun', T3_Sub01Gubun.AsString);
    Translate(Sqlen, '@Gbigo', T3_Sub01Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T3_Sub01Gsqut.AsString);
    TransAuto(Sqlen, '@ID',    T3_Sub01ID.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TSobo39_5.T3_Sub01BeforeClose(DataSet: TDataSet);
begin
  With T3_Sub01 do
  if(State in dsEditModes)Then Post;
end;

procedure TSobo39_5.T3_Sub01NewRecord(DataSet: TDataSet);
begin
  T3_Sub01Hcode.Value:=Sobo39_5.Edit107.Text;
  T3_Sub01Gubun.Value:='파기';
  T3_Sub01Scode.Value:='P';
  T3_Sub01Gsqut.Value:=0;
  if Gdate<>'' Then
  T3_Sub01Gdate.Value:=Gdate else
  T3_Sub01Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

end.
