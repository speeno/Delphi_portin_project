unit Subu38_2;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ToolEdit, dxCore,
  dxButtons, DBGridEh, CornerButton, DBClient;

type
  TSobo38_2 = class(TForm)
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
    T3_Sub81: TClientDataSet;
    T3_Sub81ID: TFloatField;
    T3_Sub81GDATE: TStringField;
    T3_Sub81GCODE: TStringField;
    T3_Sub81GNAME: TStringField;
    T3_Sub81GUBUN: TStringField;
    T3_Sub81GSQUT: TFloatField;
    T3_Sub81GDANG: TFloatField;
    T3_Sub81GSSUM: TFloatField;
    T3_Sub81GBIGO: TStringField;
    T3_Sub82: TClientDataSet;
    T3_Sub82GCODE: TStringField;
    T3_Sub82GNAME: TStringField;
    T3_Sub82GUBUN: TStringField;
    T3_Sub81HCODE: TStringField;
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
    procedure T3_Sub81AfterCancel(DataSet: TDataSet);
    procedure T3_Sub81AfterScroll(DataSet: TDataSet);
    procedure T3_Sub81AfterPost(DataSet: TDataSet);
    procedure T3_Sub81AfterDelete(DataSet: TDataSet);
    procedure T3_Sub81BeforePost(DataSet: TDataSet);
    procedure T3_Sub81BeforeClose(DataSet: TDataSet);
    procedure T3_Sub81NewRecord(DataSet: TDataSet);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo38_2: TSobo38_2;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo38_2.FormActivate(Sender: TObject);
begin
  nForm:='38_2';
  nSqry:=T3_Sub81;
  mSqry:=T3_Sub82;
end;

procedure TSobo38_2.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo38_2.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo38_2:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo38_2.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo38_2.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_24_01(Self);
  end;
end;

procedure TSobo38_2.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo38_2.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('24');
end;

procedure TSobo38_2.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('24');
end;

procedure TSobo38_2.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo38_2.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo38_2.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('24-01');
end;

procedure TSobo38_2.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('24-02');
end;

procedure TSobo38_2.Button016Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Tong40.print_38_02(Self);
end;

procedure TSobo38_2.Button017Click(Sender: TObject);
begin
{ Tong40.print_24_02(Self); }
end;

procedure TSobo38_2.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button021Click(Sender: TObject);
begin
//Tong20.DBGridFont2(DBGrid101,StBar101);
end;

procedure TSobo38_2.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Button101Click(Sender: TObject);
var St1,St2: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Base10.OpenShow(T3_Sub82);
  Sqlen := 'Select Gcode,Gname,Gubun From T8_Gbun ';
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(T3_Sub82)
  else ShowMessage(E_Open);


  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;

  Scode:='Z';
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39;

  St2:=' Order By Gdate,Gcode';

  {-S1_Ssub-}
  Sqlen := 'Select * From T8_Ssub Where '+D_Select+St1+St2;

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

    if T3_Sub82.Locate('Gcode',nSqry.FieldByName('Gcode').AsString,[loCaseInsensitive])=True then begin
    nSqry.FieldByName('Gname').AsString:=T3_Sub82.FieldByName('Gname').AsString;
    nSqry.FieldByName('Gubun').AsString:=T3_Sub82.FieldByName('Gubun').AsString;
    end;

    nSqry.Post;
    nSqry.Next;
  end;

  nSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=T3_Sub81BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo38_2.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo38_2.Edit101Change(Sender: TObject);
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

procedure TSobo38_2.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo38_2.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo38_2.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo38_2.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo38_2.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo38_2.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo38_2.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo38_2.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo38_2.Edit114KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo38_2.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo38_2.DBGrid101Exit(Sender: TObject);
begin
  T3_Sub81BeforeClose(T3_Sub81);
end;

procedure TSobo38_2.DBGrid201Exit(Sender: TObject);
begin
//
end;

procedure TSobo38_2.DBGrid101Enter(Sender: TObject);
begin
  T3_Sub81AfterScroll(T3_Sub81);
end;

procedure TSobo38_2.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo38_2.DBGrid101KeyPress(Sender: TObject; var Key: Char);
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
    //if nSqry.FieldByName('Gcode').AsString='' Then Exit;
      Seek90.Edit1.Text:=nSqry.FieldByName('Gcode').AsString;
      Seek90.FilterTing(nSqry.FieldByName('Gcode').AsString,'');
      if Seek90.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek90.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek90.Query1Gname.AsString;
        nSqry.FieldByName('Gubun').AsString:=Seek90.Query1Gubun.AsString;

        if Seek90.Query1Gcode.AsString='111' then begin
          Sqlen := 'Select Dang11 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='112' then begin
          Sqlen := 'Select Dang12 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='121' then begin
          Sqlen := 'Select Dang13 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='122' then begin
          Sqlen := 'Select Dang14 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='123' then begin
          Sqlen := 'Select Dang15 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='124' then begin
          Sqlen := 'Select Dang16 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='131' then begin
          Sqlen := 'Select Dang17 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='141' then begin
          Sqlen := 'Select Dang18 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='211' then begin
          Sqlen := 'Select Dang21 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='212' then begin
          Sqlen := 'Select Dang22 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='213' then begin
          Sqlen := 'Select Dang23 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='311' then begin
          Sqlen := 'Select Dang24 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='321' then begin
          Sqlen := 'Select Dang25 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='322' then begin
          Sqlen := 'Select Dang26 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='411' then begin
          Sqlen := 'Select Dang27 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='511' then begin
          Sqlen := 'Select Dang28 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end;

        SIndexs:=SIndexs+2;
      end else
      if Seek90.ShowModal=mrOK Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek90.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek90.Query1Gname.AsString;
        nSqry.FieldByName('Gubun').AsString:=Seek90.Query1Gubun.AsString;

        if Seek90.Query1Gcode.AsString='111' then begin
          Sqlen := 'Select Dang11 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='112' then begin
          Sqlen := 'Select Dang12 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='121' then begin
          Sqlen := 'Select Dang13 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='122' then begin
          Sqlen := 'Select Dang14 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='123' then begin
          Sqlen := 'Select Dang15 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='124' then begin
          Sqlen := 'Select Dang16 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='131' then begin
          Sqlen := 'Select Dang17 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='141' then begin
          Sqlen := 'Select Dang18 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='211' then begin
          Sqlen := 'Select Dang21 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='212' then begin
          Sqlen := 'Select Dang22 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='213' then begin
          Sqlen := 'Select Dang23 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='311' then begin
          Sqlen := 'Select Dang24 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='321' then begin
          Sqlen := 'Select Dang25 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='322' then begin
          Sqlen := 'Select Dang26 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='411' then begin
          Sqlen := 'Select Dang27 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end else
        if Seek90.Query1Gcode.AsString='511' then begin
          Sqlen := 'Select Dang28 From G7_Ssub Where '+D_Select+'Hcode=''@Hcode'' ';
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          nSqry.FieldByName('Gdang').Value:=StrToFloat(Base10.Seek_Name(Sqlen));
        end;

        SIndexs:=SIndexs+2;
      end else
        SIndexs:=SIndexs-1;
    end else
    if SIndexs=4 Then begin
      nSqry.FieldByName('Gssum').AsFloat:=
      nSqry.FieldByName('Gsqut').AsFloat*nSqry.FieldByName('Gdang').AsFloat;
      SIndexs:=SIndexs+1;
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end;
end;

procedure TSobo38_2.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
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
    if Key=VK_DELETE Then T3_Sub81AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo38_2.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo38_2.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo38_2.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo38_2.DBGrid201TitleClick(Column: TColumnEh);
begin
//
end;

procedure TSobo38_2.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo38_2.DataSource2DataChange(Sender: TObject; Field: TField);
begin
//
end;

procedure TSobo38_2.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo38_2.DateEdit2ButtonClick(Sender: TObject);
begin
  DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo38_2.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo38_2.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo38_2.Button700Click(Sender: TObject);
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

//--폐기(정품)--//
procedure TSobo38_2.T3_Sub81AfterCancel(DataSet: TDataSet);
begin
  T3_Sub81AfterScroll(T3_Sub81);
end;

procedure TSobo38_2.T3_Sub81AfterScroll(DataSet: TDataSet);
begin
  Gdate:= T3_Sub81.FieldByName('Gdate').AsString;
  Gcode:= T3_Sub81.FieldByName('Gcode').AsString;
  Gsqut:=-T3_Sub81.FieldByName('Gsqut').AsFloat;
  Gdang:=-T3_Sub81.FieldByName('Gdang').AsFloat;
  Gssum:=-T3_Sub81.FieldByName('Gssum').AsFloat;
end;

procedure TSobo38_2.T3_Sub81AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TSobo38_2.T3_Sub81AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

      Sqlen := 'DELETE FROM T8_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T3_Sub81ID.AsString);
      Translate(Sqlen, '@Gdate', T3_Sub81Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    T3_Sub81.Delete;

  end; end;

end;

procedure TSobo38_2.T3_Sub81BeforePost(DataSet: TDataSet);
begin

  if(T3_Sub81.State=dsInsert)Then begin

    Sqlen := 'INSERT INTO T8_Ssub '+
    '(Hcode, Gdate, Gcode, Gsqut, Gdang, Gssum, Gbigo) VALUES '+
    '(''@Hcode'',''@Gdate'',''@Gcode'', @Gsqut , @Gdang , @Gssum ,''@Gbigo'')';

    Translate(Sqlen, '@Hcode', T3_Sub81Hcode.AsString);
    Translate(Sqlen, '@Gdate', T3_Sub81Gdate.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub81Gcode.AsString);
    TransAuto(Sqlen, '@Gsqut', T3_Sub81Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T3_Sub81Gdang.AsString);
    TransAuto(Sqlen, '@Gssum', T3_Sub81Gssum.AsString);
    Translate(Sqlen, '@Gbigo', T3_Sub81Gbigo.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'T8_SSUB_ID_GEN');

  end else begin

    Sqlen := 'UPDATE T8_Ssub SET '+
    'Hcode=''@Hcode'',Gdate=''@Gdate'',Gcode=''@Gcode'', '+
    'Gsqut=  @Gsqut  ,Gdang=  @Gdang  ,Gssum=  @Gssum  ,Gbigo=''@Gbigo'' '+
    'WHERE ID=@ID and Gdate=''@Sdate''';

    Translate(Sqlen, '@Hcode', T3_Sub81Hcode.AsString);
    Translate(Sqlen, '@Gdate', T3_Sub81Gdate.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub81Gcode.AsString);
    TransAuto(Sqlen, '@Gsqut', T3_Sub81Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T3_Sub81Gdang.AsString);
    TransAuto(Sqlen, '@Gssum', T3_Sub81Gssum.AsString);
    Translate(Sqlen, '@Gbigo', T3_Sub81Gbigo.AsString);
    TransAuto(Sqlen, '@ID',    T3_Sub81ID.AsString);
    Translate(Sqlen, '@Sdate', Gdate);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TSobo38_2.T3_Sub81BeforeClose(DataSet: TDataSet);
begin
  With T3_Sub81 do
  if(State in dsEditModes)Then Post;
end;

procedure TSobo38_2.T3_Sub81NewRecord(DataSet: TDataSet);
begin
  T3_Sub81Hcode.Value:=Edit107.Text;
  T3_Sub81Gcode.Value:='';
  T3_Sub81Gname.Value:='';
  T3_Sub81Gubun.Value:='';
  T3_Sub81Gsqut.Value:=0;
  T3_Sub81Gdang.Value:=0;
  T3_Sub81Gssum.Value:=0;
  if Gdate<>'' Then
  T3_Sub81Gdate.Value:=Gdate else
  T3_Sub81Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

end.
