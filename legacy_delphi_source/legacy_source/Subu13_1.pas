unit Subu13_1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, dxCore, dxButtons,
  CornerButton, DBClient;

type
  TSobo13_1 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Panel100: TFlatPanel;
    Edit102: TFlatEdit;
    Button101: TFlatButton;
    Panel101: TFlatPanel;
    Panel102: TFlatPanel;
    Edit101: TFlatEdit;
    Edit108: TFlatEdit;
    Edit107: TFlatEdit;
    Panel001: TFlatPanel;
    DBGrid101: TDBGrid;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    dxButton1: TdxButton;
    Button701: TFlatButton;
    Button702: TFlatButton;
    T3_Sub01: TClientDataSet;
    T3_Sub01ID: TFloatField;
    T3_Sub01GDATE: TStringField;
    T3_Sub01HCODE: TStringField;
    T3_Sub01SCODE: TStringField;
    T3_Sub01GCODE: TStringField;
    T3_Sub01GNAME: TStringField;
    T3_Sub01GJISA: TStringField;
    T3_Sub01BEBON: TStringField;
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
    procedure Edit101Exit(Sender: TObject);
    procedure Edit101Change(Sender: TObject);
    procedure Edit101KeyPress(Sender: TObject; var Key: Char);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit102KeyPress(Sender: TObject; var Key: Char);
    procedure Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit111KeyPress(Sender: TObject; var Key: Char);
    procedure Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit112KeyPress(Sender: TObject; var Key: Char);
    procedure Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit113KeyPress(Sender: TObject; var Key: Char);
    procedure Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
    procedure Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101DblClick(Sender: TObject);
    procedure DBGrid101Enter(Sender: TObject);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101Exit(Sender: TObject);
    procedure DBGrid201Exit(Sender: TObject);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
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
  Sobo13_1: TSobo13_1;

implementation

{$R *.DFM}

uses Chul, Base01, Subu19, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo13_1.FormActivate(Sender: TObject);
begin
  nForm:='13_1';
  nSqry:=T3_Sub01;
//mSqry:=T3_Sub01;
end;

procedure TSobo13_1.FormShow(Sender: TObject);
begin
//
end;

procedure TSobo13_1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo13_1:=nil;
  Base10.OpenExit(nSqry);
//Base10.OpenExit(mSqry);
end;

procedure TSobo13_1.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button012Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button014Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button015Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button016Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button017Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button101Click(Sender: TObject);
var St1,St2: String;
begin
//if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;
  Base10.OpenShow(nSqry);

  if Edit108.Text='' Then
     Edit107.Text:='';

  St2:=' Order By Gcode';

  if Edit107.Text='' Then
  St1:='Gcode'+' Like '+#39+'%'+''+'%'+#39+' and '+
       'Hcode'+' ='+#39+''+#39
  else
  St1:='Hcode'+' ='+#39+Edit107.Text+#39;

  Sqlen := 'Select Hcode,Gcode,Gname From G1_Ggeo Where '+D_Select+St1+St2;

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

    nSqry.Append;
    nSqry.FieldByName('Hcode').AsString:=SGrid.Cells[ 0,List1];
    nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 1,List1];
    nSqry.FieldByName('Gname').AsString:=SGrid.Cells[ 2,List1];
    nSqry.Post;

      if Edit107.Text='' Then
      St1:='Scode'+'='+#39+'X'+#39+' and '+
           'Gbigo'+'='+#39+''+#39+' and '+
           'Gcode'+'='+#39+SGrid.Cells[ 1,List1]+#39
      else
      St1:='Scode'+'='+#39+'X'+#39+' and '+
           'Gbigo'+'='+#39+''+#39+' and '+
           'Hcode'+'='+#39+Edit107.Text+#39+' and '+
           'Gcode'+'='+#39+SGrid.Cells[ 1,List1]+#39;

      Sqlen := 'Select Gname,Jubun From H2_Gbun Where '+D_Select+St1+' Order By Oname,Gname';
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.body_data <> 'ERROR' then
         Base10.Socket.MakeGrid(YGrid)
      else ShowMessage(E_Open);

      RBand:=0;
      While YGrid.RowCount-1 > RBand do begin
      RBand:=RBand+1;

      nSqry.Append;
      if YGrid.Cells[ 1,RBand]='' then
      nSqry.FieldByName('Gjisa').AsString:=YGrid.Cells[ 0,RBand] else
      nSqry.FieldByName('Gjisa').AsString:=YGrid.Cells[ 1,RBand]+'|'+YGrid.Cells[ 0,RBand];
      nSqry.FieldByName('Hcode').AsString:=SGrid.Cells[ 0,List1];
      nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 1,List1];
      nSqry.FieldByName('Gname').AsString:=SGrid.Cells[ 2,List1];
      nSqry.Post;
      end;
  end;


  if Edit107.Text='' Then
  St1:='Gcode'+' Like '+#39+'%'+''+'%'+#39+' and '+
       'Hcode'+' ='+#39+''+#39
  else
  St1:='Hcode'+' ='+#39+Edit107.Text+#39;

  Sqlen := 'Select Hcode,Gcode,Gjisa,Bebon From T0_Gbun Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    if nSqry.Locate('Hcode;Gcode;Gjisa',VarArrayOf([SGrid.Cells[ 0,List1],SGrid.Cells[ 1,List1],SGrid.Cells[ 2,List1]]),[loCaseInsensitive])=true then begin
      nSqry.Edit;
      nSqry.FieldByName('Bebon').AsString:=SGrid.Cells[ 3,List1];
      nSqry.Post;
    end;
  end;


  nSqry.First;
//Tong20.Srart_16_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=T3_Sub01BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo13_1.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Edit101Exit(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=05)and(Length(Trim(Edit101.Text))=05))or
    ((Edit102.Focused=True)and(Edit102.SelStart=50)and(Length(Trim(Edit102.Text))=50))or
    ((Edit107.Focused=True)and(Edit107.SelStart=50)and(Length(Trim(Edit107.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo13_1.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo13_1.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo13_1.Edit102KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then DBGrid101.SetFocus;
end;

procedure TSobo13_1.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo13_1.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo13_1.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo13_1.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo13_1.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo13_1.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo13_1.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo13_1.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if(Edit107.Focused=True)or(Edit108.Focused=True)Then begin
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
  if Edit102.Focused=True Then begin
    if Edit108.Text='' Then
       Edit107.Text:='';
       Edit101.Text:='';
    if Edit102.Text<>'' Then begin
    Seek10.Edit1.Text:=Edit102.Text;
    Seek10.FilterTing(Edit102.Text,Edit107.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit101.Text:=Seek10.Query1Gcode.AsString;
      Edit102.Text:=Seek10.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seek10.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit101.Text:=Seek10.Query1Gcode.AsString;
      Edit102.Text:=Seek10.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo13_1.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo13_1.DBGrid101DblClick(Sender: TObject);
begin
//
end;

procedure TSobo13_1.DBGrid101Enter(Sender: TObject);
begin
//
end;

procedure TSobo13_1.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    end;
  end;
  end;
end;

procedure TSobo13_1.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    if SIndexs=3 Then begin
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),0,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),KEYEVENTF_KEYUP,0);
    end;
  end;
  end;
end;

procedure TSobo13_1.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo13_1.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo13_1.DBGrid101Exit(Sender: TObject);
begin
//
end;

procedure TSobo13_1.DBGrid201Exit(Sender: TObject);
begin
//
end;

procedure TSobo13_1.Button701Click(Sender: TObject);
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

procedure TSobo13_1.Button702Click(Sender: TObject);
begin
//
end;

procedure TSobo13_1.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo13_1.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

//--원장변경--//
procedure TSobo13_1.T3_Sub01AfterCancel(DataSet: TDataSet);
begin
  T3_Sub01AfterScroll(T3_Sub01);
end;

procedure TSobo13_1.T3_Sub01AfterScroll(DataSet: TDataSet);
begin
//
end;

procedure TSobo13_1.T3_Sub01AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TSobo13_1.T3_Sub01AfterDelete(DataSet: TDataSet);
begin
//
end;

procedure TSobo13_1.T3_Sub01BeforePost(DataSet: TDataSet);
begin

  Sqlen := 'Select Count(*) From T0_Gbun Where '+D_Select+
           'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa''';
  Translate(Sqlen, '@Hcode', T3_Sub01Hcode.AsString);
  Translate(Sqlen, '@Gcode', T3_Sub01Gcode.AsString);
  Translate(Sqlen, '@Gjisa', T3_Sub01Gjisa.AsString);
  if Base10.Seek_Name(Sqlen)='0' then begin

    Sqlen := 'INSERT INTO T0_Gbun '+
    '(Hcode, Gcode, Gjisa, Bebon) VALUES '+
    '(''@Hcode'',''@Gcode'',''@Gjisa'',''@Bebon'')';

    Translate(Sqlen, '@Hcode', T3_Sub01Hcode.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub01Gcode.AsString);
    Translate(Sqlen, '@Gjisa', T3_Sub01Gjisa.AsString);
    Translate(Sqlen, '@Bebon', T3_Sub01Bebon.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  end else begin

    Sqlen := 'UPDATE T0_Gbun SET '+
    'Bebon=''@Bebon'' '+
    'WHERE Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa'' ';

    Translate(Sqlen, '@Hcode', T3_Sub01Hcode.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub01Gcode.AsString);
    Translate(Sqlen, '@Gjisa', T3_Sub01Gjisa.AsString);
    Translate(Sqlen, '@Bebon', T3_Sub01Bebon.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TSobo13_1.T3_Sub01BeforeClose(DataSet: TDataSet);
begin
  With T3_Sub01 do
  if(State in dsEditModes)Then Post;
end;

procedure TSobo13_1.T3_Sub01NewRecord(DataSet: TDataSet);
begin
//
end;

end.
