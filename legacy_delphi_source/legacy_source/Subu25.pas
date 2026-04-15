unit Subu25;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ToolEdit, dxCore,
  dxButtons, DBGridEh, CornerButton;

type
  TSobo25 = class(TForm)
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
    DateEdit1: TDateEdit;
    DateEdit2: TDateEdit;
    Button700: TFlatButton;
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
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button700Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo25: TSobo25;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo25.FormActivate(Sender: TObject);
begin
  nForm:='25';
  nSqry:=Base10.T2_Sub51;
  mSqry:=Base10.T2_Sub52;
end;

procedure TSobo25.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo25.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo25:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo25.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo25.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_52_01(Self);
  end;
end;

procedure TSobo25.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo25.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('25');
end;

procedure TSobo25.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('25');
end;

procedure TSobo25.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo25.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo25.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('25-01');
end;

procedure TSobo25.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('25-02');
end;

procedure TSobo25.Button016Click(Sender: TObject);
begin
  Tong40.print_25_01(Self);
end;

procedure TSobo25.Button017Click(Sender: TObject);
begin
{ Tong40.print_25_02(Self); }
end;

procedure TSobo25.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button021Click(Sender: TObject);
begin
//Tong20.DBGridFont2(DBGrid101,StBar101);
end;

procedure TSobo25.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Button101Click(Sender: TObject);
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

  Scode:='X';
  St1:='Bdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Bdate'+'<='+#39+Edit102.Text+#39+' and '+
       '('+'Gdate is null '+')'+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Gubun'+' ='+#39+'반품'+#39+' and '+
       'Pubun'+' ='+#39+'비품'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+Scode+#39;

  St2:=' Order By Bdate,Bcode';

  {-S1_Ssub-}
  Sqlen := 'Select ID,Bdate as Gdate,Hcode,Gcode,Bcode,Gsqut,Gdang,Gssum,Gbigo '+
           'From S1_Ssub Where '+D_Select+St1+St2;

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

    if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Bcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Bname').AsString:=Base10.G4_Book.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Bname').AsString='' then begin
    Sqlen := 'Select Gname,Gjeja From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Bcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      nSqry.FieldByName('Bname').Value:=Base10.Socket.GetData(1, 1);
    //nSqry.FieldByName('Gjeja').Value:=Base10.Socket.GetData(1, 2);
    end;
    end;

    nSqry.Post;
    nSqry.Next;
  end;

  nSqry.First;
  Tong20.Srart_25_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=Base10.T2_Sub51BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo25.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo25.Edit101Change(Sender: TObject);
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

procedure TSobo25.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo25.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo25.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo25.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo25.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo25.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo25.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo25.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo25.Edit114KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo25.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo25.DBGrid101Exit(Sender: TObject);
begin
  Base10.T2_Sub51BeforeClose(Base10.T2_Sub51);
end;

procedure TSobo25.DBGrid201Exit(Sender: TObject);
begin
//
end;

procedure TSobo25.DBGrid101Enter(Sender: TObject);
begin
  Base10.T2_Sub51AfterScroll(Base10.T2_Sub51);
end;

procedure TSobo25.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo25.DBGrid101KeyPress(Sender: TObject; var Key: Char);
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
      if nSqry.FieldByName('Bcode').AsString='' Then Exit;
      Seek40.Edit1.Text:=nSqry.FieldByName('Bcode').AsString;
      Seek40.FilterTing(nSqry.FieldByName('Bcode').AsString,Edit107.Text);
      if Seek40.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Bcode').AsString:=Seek40.Query1Gcode.AsString;
        nSqry.FieldByName('Bname').AsString:=Seek40.Query1Gname.AsString;
        nSqry.FieldByName('Gdang').Value:=Seek40.Query1Gdang.Value;
        SIndexs:=SIndexs+1;
      end else
      if Seek40.ShowModal=mrOK Then begin
        nSqry.FieldByName('Bcode').AsString:=Seek40.Query1Gcode.AsString;
        nSqry.FieldByName('Bname').AsString:=Seek40.Query1Gname.AsString;
        nSqry.FieldByName('Gdang').Value:=Seek40.Query1Gdang.Value;
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;
    end else
    if SIndexs=3 Then begin
      nSqry.FieldByName('Gsqut').AsFloat:=-(nSqry.FieldByName('Gsqut').AsFloat);
      nSqry.FieldByName('Gssum').AsFloat:=
      nSqry.FieldByName('Gsqut').AsFloat*nSqry.FieldByName('Gdang').AsFloat;
      SIndexs:=SIndexs+1;
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end;
end;

procedure TSobo25.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    if SIndexs=6 Then begin
      nSqry.Append; DBGrid101.SelectedIndex:=0;
    end;
  end;
  if sColumn=False Then begin
    if nSqry.IsEmpty=False Then
    if Key=VK_DELETE Then Base10.T2_Sub51AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo25.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo25.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo25.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo25.DBGrid201TitleClick(Column: TColumnEh);
begin
//
end;

procedure TSobo25.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo25.DataSource2DataChange(Sender: TObject; Field: TField);
begin
//
end;

procedure TSobo25.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo25.DateEdit2ButtonClick(Sender: TObject);
begin
  DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo25.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo25.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo25.Button700Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit108.Text;
  if Edit108.Text='' then
  Seak80.FilterTing('') else
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
end;

end.
