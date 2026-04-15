unit Subu96;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, TFlatRadioButtonUnit,
  ToolEdit, DBGridEh, DBClient;

type
  TSobo96 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel003: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    Panel101: TFlatPanel;
    Panel105: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Button201: TFlatButton;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
    Panel200: TFlatPanel;
    Panel201: TFlatPanel;
    Panel207: TFlatPanel;
    Edit207: TFlatEdit;
    Edit208: TFlatEdit;
    Panel202: TFlatPanel;
    Edit202: TFlatEdit;
    Edit201: TFlatEdit;
    Panel203: TFlatPanel;
    Edit203: TFlatEdit;
    Panel204: TFlatPanel;
    Edit204: TFlatEdit;
    Panel205: TFlatPanel;
    Panel206: TFlatPanel;
    Edit205: TFlatEdit;
    Edit206: TFlatEdit;
    Panel300: TFlatPanel;
    Panel301: TFlatPanel;
    Panel303: TFlatPanel;
    Edit303: TFlatEdit;
    Edit301: TFlatEdit;
    Panel302: TFlatPanel;
    Panel304: TFlatPanel;
    Edit304: TFlatEdit;
    Edit302: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Label101: TmyLabel3d;
    Button401: TFlatButton;
    RadioButton1: TFlatRadioButton;
    RadioButton2: TFlatRadioButton;
    RadioButton3: TFlatRadioButton;
    DateEdit1: TDateEdit;
    Button701: TFlatButton;
    Button702: TFlatButton;
    Edit209: TFlatEdit;
    Edit210: TFlatEdit;
    Edit211: TFlatEdit;
    StaticText1: TStaticText;
    StaticText2: TStaticText;
    StaticText3: TStaticText;
    Button400: TFlatButton;
    DBGrid101: TDBGridEh;
    DBGrid201: TDBGridEh;
    Panel004: TFlatPanel;
    Label401: TmyLabel3d;
    Label402: TmyLabel3d;
    Label403: TmyLabel3d;
    Label404: TmyLabel3d;
    Label411: TmyLabel3d;
    Label412: TmyLabel3d;
    Label413: TmyLabel3d;
    Label414: TmyLabel3d;
    Panel501: TFlatPanel;
    Edit501: TFlatEdit;
    Edit212: TFlatEdit;
    StaticText4: TStaticText;
    Button403: TFlatButton;
    T2_Sub61: TClientDataSet;
    T2_Sub61ID: TFloatField;
    T2_Sub61IDNUM: TFloatField;
    T2_Sub61GDATE: TStringField;
    T2_Sub61SCODE: TStringField;
    T2_Sub61GCODE: TStringField;
    T2_Sub61GNAME: TStringField;
    T2_Sub61HCODE: TStringField;
    T2_Sub61HNAME: TStringField;
    T2_Sub61OCODE: TStringField;
    T2_Sub61BCODE: TStringField;
    T2_Sub61BNAME: TStringField;
    T2_Sub61GJEJA: TStringField;
    T2_Sub61GUBUN: TStringField;
    T2_Sub61JUBUN: TStringField;
    T2_Sub61PUBUN: TStringField;
    T2_Sub61GSQUT: TFloatField;
    T2_Sub61QSQUT: TFloatField;
    T2_Sub61GDANG: TFloatField;
    T2_Sub61GRAT1: TSmallintField;
    T2_Sub61GSSUM: TFloatField;
    T2_Sub61JEAGO: TFloatField;
    T2_Sub61GBIGO: TStringField;
    T2_Sub61YESNO: TStringField;
    T2_Sub61GJISA: TStringField;
    T2_Sub61GPOST: TStringField;
    T2_Sub61QPOST: TStringField;
    T2_Sub61GMEMO: TDateTimeField;
    T2_Sub61TIME1: TDateTimeField;
    T2_Sub61TIME2: TDateTimeField;
    T2_Sub61TIME3: TDateTimeField;
    T2_Sub61TIME4: TDateTimeField;
    T2_Sub62: TClientDataSet;
    T2_Sub62ID: TFloatField;
    T2_Sub62IDNUM: TFloatField;
    T2_Sub62GDATE: TStringField;
    T2_Sub62SCODE: TStringField;
    T2_Sub62GCODE: TStringField;
    T2_Sub62GNAME: TStringField;
    T2_Sub62HCODE: TStringField;
    T2_Sub62HNAME: TStringField;
    T2_Sub62OCODE: TStringField;
    T2_Sub62BCODE: TStringField;
    T2_Sub62BNAME: TStringField;
    T2_Sub62GJEJA: TStringField;
    T2_Sub62GUBUN: TStringField;
    T2_Sub62JUBUN: TStringField;
    T2_Sub62PUBUN: TStringField;
    T2_Sub62GSQUT: TFloatField;
    T2_Sub62QSQUT: TFloatField;
    T2_Sub62GDANG: TFloatField;
    T2_Sub62GRAT1: TSmallintField;
    T2_Sub62GSSUM: TFloatField;
    T2_Sub62JEAGO: TFloatField;
    T2_Sub62GBIGO: TStringField;
    T2_Sub62YESNO: TStringField;
    T2_Sub62GMEMO: TDateTimeField;
    T2_Sub62GJISA: TStringField;
    T4_Sub81: TClientDataSet;
    T4_Sub81ID: TFloatField;
    T4_Sub81GDATE: TStringField;
    T4_Sub81SCODE: TStringField;
    T4_Sub81GCODE: TStringField;
    T4_Sub81GNAME: TStringField;
    T4_Sub81HCODE: TStringField;
    T4_Sub81HNAME: TStringField;
    T4_Sub81NAME1: TStringField;
    T4_Sub81NAME2: TStringField;
    T4_Sub81GSSUM: TFloatField;
    T4_Sub81GSUMX: TFloatField;
    T4_Sub81GSUMY: TFloatField;
    T4_Sub81GQUT1: TFloatField;
    T4_Sub81GQUT2: TFloatField;
    T4_Sub81GQUT3: TFloatField;
    T4_Sub81GQUT4: TFloatField;
    T4_Sub81GNUM1: TFloatField;
    T4_Sub81GNUM2: TFloatField;
    T2_Sub61ICODE: TFloatField;
    T2_Sub62ICODE: TFloatField;
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
    procedure Button401Click(Sender: TObject);
    procedure Button403Click(Sender: TObject);
    procedure Button501Click(Sender: TObject);
    procedure Button509Click(Sender: TObject);
    procedure Button601Click(Sender: TObject);
    procedure Button609Click(Sender: TObject);
    procedure Edit101Change(Sender: TObject);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit111KeyPress(Sender: TObject; var Key: Char);
    procedure Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit112KeyPress(Sender: TObject; var Key: Char);
    procedure Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit113KeyPress(Sender: TObject; var Key: Char);
    procedure Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit115KeyPress(Sender: TObject; var Key: Char);
    procedure Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
    procedure Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101TitleClick(Column: TColumnEh);
    procedure DBGrid201TitleClick(Column: TColumnEh);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure DBGrid201DblClick(Sender: TObject);
    procedure Delete_Seek(Sender: TObject);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure Edit205Click(Sender: TObject);
    procedure Edit205Exit(Sender: TObject);
    procedure StaticText1Click(Sender: TObject);
    procedure StaticText2Click(Sender: TObject);
    procedure StaticText3Click(Sender: TObject);
    procedure StaticText4Click(Sender: TObject);
    procedure DBGrid201DrawColumnCell(Sender: TObject; const Rect: TRect;
      DataCol: Integer; Column: TColumnEh; State: TGridDrawState);
    procedure Button400Click(Sender: TObject);
    procedure Seek_Post(Sender: TObject);
    procedure T2_Sub62YESNOGetText(Sender: TField; var Text: String;
      DisplayText: Boolean);
    procedure T2_Sub62YESNOSetText(Sender: TField; const Text: String);
    procedure T2_Sub61AfterCancel(DataSet: TDataSet);
    procedure T2_Sub61AfterScroll(DataSet: TDataSet);
    procedure T2_Sub61AfterPost(DataSet: TDataSet);
    procedure T2_Sub61AfterDelete(DataSet: TDataSet);
    procedure T2_Sub61BeforePost(DataSet: TDataSet);
    procedure T2_Sub61BeforeClose(DataSet: TDataSet);
    procedure T2_Sub61NewRecord(DataSet: TDataSet);
    procedure ColumnX1(TableX: TClientDataSet);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo96: TSobo96;

implementation

{$R *.DFM}

uses Chul, Base01, Tong01, Tong02, Tong04, TcpLib, Subu91,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo96.FormActivate(Sender: TObject);
begin
  nForm:='96';
  nSqry:=T2_Sub61;
  mSqry:=T2_Sub62;
  tSqry:=T4_Sub81;
end;

procedure TSobo96.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit101.SetFocus;
end;

procedure TSobo96.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo96:=nil;
  DataSource2.Enabled:=False;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Base10.OpenExit(tSqry);
end;

procedure TSobo96.Button001Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
     Seak10.ShowModal;
  end; }
end;

procedure TSobo96.Button002Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_26_02(Self);
  end; }
end;

procedure TSobo96.Button003Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo96.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button006Click(Sender: TObject);
begin
{ T00:=1;
  Button201Click(Self); }
end;

procedure TSobo96.Button007Click(Sender: TObject);
begin
{ T00:=0;
  Button201Click(Self); }
end;

procedure TSobo96.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo96.Button011Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo96.Button012Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo96.Button013Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo96.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('26-01');
end;

procedure TSobo96.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('26-02');
end;

procedure TSobo96.Button016Click(Sender: TObject);
begin
  Delete_Seek(Self);
  if(mSqry.FieldByName('Yesno').AsString='1')or
    (mSqry.FieldByName('Yesno').AsString='0')then begin
    Button609Click(Self);
    mSqry.Edit;
    mSqry.FieldByName('Yesno').AsString:='2';
    mSqry.Post;
  end;

  if Base10.Database.Database='chul_02_db' then begin
    Seek_Post(Self);
    nSqry.IndexName := 'IDX'+'GPOST'+'DOWN';
    Tong40.PrinTing00('24','1','','','','','','','','');
    nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  end else
  if(Base10.Database.Database='book_01_db')and(Base10.Database.Host='115.68.7.138')then begin
    Seek_Post(Self);
    nSqry.IndexName := 'IDX'+'GPOST'+'DOWN';
    Tong40.PrinTing00('24','1','','','','','','','','');
    nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  end else
    Tong40.PrinTing00('24','1','','','','','','','','');
end;

procedure TSobo96.Button017Click(Sender: TObject);
begin
  mSqry.First;
  While mSqry.EOF=False do begin
  Delete_Seek(Self);
  if(mSqry.FieldByName('Yesno').AsString='1')or
    (mSqry.FieldByName('Yesno').AsString='0')then begin
    Button609Click(Self);
    mSqry.Edit;
    mSqry.FieldByName('Yesno').AsString:='2';
    mSqry.Post;
  end;

  if Base10.Database.Database='chul_02_db' then begin
    Seek_Post(Self);
    nSqry.IndexName := 'IDX'+'GPOST'+'DOWN';
    Tong40.PrinTing00('24','1','','','','','','','','');
    nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  end else
  if(Base10.Database.Database='book_01_db')and(Base10.Database.Host='115.68.7.138')then begin
    Seek_Post(Self);
    nSqry.IndexName := 'IDX'+'GPOST'+'DOWN';
    Tong40.PrinTing00('24','1','','','','','','','','');
    nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  end else
    Tong40.PrinTing00('24','1','','','','','','','','');

  mSqry.Next;
  end;
end;

procedure TSobo96.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont3(DBGrid101,DBGrid201);
end;

procedure TSobo96.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo96.Button101Click(Sender: TObject);
var St1,St2,St3: String;
begin
//if Base10.Seek_Ggeo(Edit108.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);

  St2:='Z';

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit101.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+St2+#39;

  if D_Select<>'' then
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit101.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
      '(Scode'+' ='+#39+'Z'+#39+' or '+'Scode'+' ='+#39+'1'+#39+')';

  if (Edit104.Text<>'') Then
  St1:=St1+' and '+
       'Hcode'+'>='+#39+Edit102.Text+#39+' and '+
       'Hcode'+'<='+#39+Edit104.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  if RadioButton1.Checked=True Then
  St1:=St1+' and '+'Yesno'+'='+#39+'1'+#39;
  if RadioButton2.Checked=True Then
  St1:=St1+' and '+'Yesno'+'='+#39+'2'+#39;

  if Base10.Database.Database='book_kb_db' then
  St2:=' Order By Yesno Desc,Gdate,Hcode,Gmemo,Gcode,Gubun,Jubun,Gjisa,Bcode'
  else
  St2:=' Order By Yesno Desc,Gdate,Hcode,Gmemo,Gcode,Gubun,Jubun,Gjisa,ID';

  Sqlen := 'Select * From S1_Ssub Where '+D_Select+St1+St2;

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

    if Base10.G7_Ggeo.Locate('Gcode',nSqry.FieldByName('Hcode').AsString,[loCaseInsensitive])=true then
    nSqry.FieldByName('Hname').AsString:=Base10.G7_Ggeo.FieldByName('Gname').AsString;

  { if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Gname').AsString='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString; }

    if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Bcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Bname').AsString:=Base10.G4_Book.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Gjisa').AsString<>'' then
    nSqry.FieldByName('Gname').AsString:=Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'2')+
    nSqry.FieldByName('Gname').AsString+ Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'1');

    //------------------------------------------------------------------------//
    if nSqry.FieldByName('Hname').AsString='' then begin
    Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Hcode').AsString);
    nSqry.FieldByName('Hname').Value:=Base10.Seek_Name(Sqlen);
    end;

    if nSqry.FieldByName('Gname').AsString='' then begin
    Sqlen := 'Select Gname From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', '');
    nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
    end;

    if nSqry.FieldByName('Gname').AsString='' then begin
    Sqlen := 'Select Gname From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
    end;

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

    nSqry.FieldByName('Gmemo').AsString:=nSqry.FieldByName('Time1').AsString;
    if nSqry.FieldByName('Time3').AsString<>'' then
    nSqry.FieldByName('Gmemo').AsString:=nSqry.FieldByName('Time3').AsString;
    if nSqry.FieldByName('Time2').AsString<>'' then
    nSqry.FieldByName('Gmemo').AsString:=nSqry.FieldByName('Time2').AsString;

  { if nSqry.FieldByName('Gjisa').AsString<>'' then
    nSqry.FieldByName('Gname').AsString:=
    nSqry.FieldByName('Gjisa').AsString+')'+nSqry.FieldByName('Gname').AsString; }

    nSqry.Post;
    nSqry.Next;
  end;

  Button201Click(Self);

//nSqry.IndexName := 'IDX'+'BCODE'+'DOWN';
  nSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=T2_Sub61BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo96.Button201Click(Sender: TObject);
var St1,St2,St3,St4,St5: String;
begin
  nSqry.First;
  mSqry.First;
  While nSqry.EOF=False do begin
    St1:=nSqry.FieldByName('Hcode').AsString;
    St2:=nSqry.FieldByName('Gcode').AsString;
    St3:=nSqry.FieldByName('Scode').AsString;
    St4:=nSqry.FieldByName('Jubun').AsString;
    St5:=nSqry.FieldByName('Gjisa').AsString;
    if mSqry.Locate('Hcode;Gcode;Gjisa',VarArrayOf([St1,St2,St5]),[loCaseInsensitive])=False then begin
      mSqry.Append;
      mSqry.FieldByName('Hcode').AsString:=St1;
      mSqry.FieldByName('Gcode').AsString:=St2;
      mSqry.FieldByName('Scode').AsString:=St3;
      mSqry.FieldByName('Jubun').AsString:=St4;
      mSqry.FieldByName('Gjisa').AsString:=St5;
      mSqry.FieldByName('Gdate').AsString:=nSqry.FieldByName('Gdate').AsString;
      mSqry.FieldByName('Hname').AsString:=nSqry.FieldByName('Hname').AsString;
      mSqry.FieldByName('Gname').AsString:=nSqry.FieldByName('Gname').AsString;
      mSqry.FieldByName('Yesno').AsString:=nSqry.FieldByName('Yesno').AsString;
      mSqry.FieldByName('Gmemo').AsDateTime:=nSqry.FieldByName('Gmemo').AsDateTime;
      mSqry.FieldByName('Bname').AsString:=
      (nSqry.FieldByName('Gcode').AsString)+'-'+Copy(nSqry.FieldByName('Gdate').AsString,6,2)+
      Copy(nSqry.FieldByName('Gdate').AsString,9,2)+'-'+(nSqry.FieldByName('Idnum').AsString);
      mSqry.Post;
    end;
    nSqry.Next;
  end;
  nSqry.First;
//mSqry.IndexName := 'IDX'+'GMEMO'+'DOWN';
  mSqry.First;
end;

procedure TSobo96.Button301Click(Sender: TObject);
begin
  if Edit207.Visible=True then begin

    Edit207.Text:='';
    Edit208.Text:='';
    Edit209.Text:='';
    Edit210.Text:='';
    Edit211.Text:='';
    Edit212.Text:='';

    Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where '+D_Select+
             'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
             'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
             'Scode=''@Scode'' and Hcode=''@Hcode'' and '+
             'Gjisa=''@Gjisa'' and '+
             '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';
    Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
    Translate(Sqlen, '@Gubun', nSqry.FieldByName('Gubun').AsString);
    Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
    Translate(Sqlen, '@Ocode', 'B');
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      Edit207.Text:=Base10.Socket.GetData(1, 1);
      Edit208.Text:=Base10.Socket.GetData(1, 2);
      Edit209.Text:=Base10.Socket.GetData(1, 3);
      Edit210.Text:=Base10.Socket.GetData(1, 4);
      Edit211.Text:=Base10.Socket.GetData(1, 5);
      Edit212.Text:=Base10.Socket.GetData(1, 6);
    end;

    Edit205Exit(Self);
  end;
end;

procedure TSobo96.Button400Click(Sender: TObject);
var St1: String;
begin
  Sqlen := 'Select Gname,Gadd1,Gadd2,Gtel1,Gtel2 From G5_Ggeo Where '+D_Select+
           'Hcode=''@Hcode'' and Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
  Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    St1:=Base10.Socket.GetData(1, 1);
    Translate(St1, '-택배', '');
    if (Edit207.Text='')and(Base10.Socket.GetData(1, 2)<>'') then
    Edit207.Text:=Base10.Socket.GetData(1, 2);
    if (Edit208.Text='')and(Base10.Socket.GetData(1, 3)<>'') then
    Edit208.Text:=Base10.Socket.GetData(1, 3);
    if (Edit210.Text='')and(Base10.Socket.GetData(1, 5)<>'') then
    Edit210.Text:=Base10.Socket.GetData(1, 4)+'-'+Base10.Socket.GetData(1, 5);
    if (Edit211.Text='')and(Base10.Socket.GetData(1, 1)<>'') then
    Edit211.Text:=St1;
    Edit205Exit(Self);
  end else begin

  Sqlen := 'Select Gname,Gadd1,Gadd2,Gtel1,Gtel2 From G5_Ggeo Where '+D_Select+
           'Hcode=''@Hcode'' and Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Hcode', '');
  Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    St1:=Base10.Socket.GetData(1, 1);
    Translate(St1, '-택배', '');
    if (Edit207.Text='')and(Base10.Socket.GetData(1, 2)<>'') then
    Edit207.Text:=Base10.Socket.GetData(1, 2);
    if (Edit208.Text='')and(Base10.Socket.GetData(1, 3)<>'') then
    Edit208.Text:=Base10.Socket.GetData(1, 3);
    if (Edit210.Text='')and(Base10.Socket.GetData(1, 5)<>'') then
    Edit210.Text:=Base10.Socket.GetData(1, 4)+'-'+Base10.Socket.GetData(1, 5);
    if (Edit211.Text='')and(Base10.Socket.GetData(1, 1)<>'') then
    Edit211.Text:=St1;
    Edit205Exit(Self);
  end;

  end;
end;

procedure TSobo96.Button401Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin

    Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where '+D_Select+
             'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
             'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
             'Scode=''@Scode'' and Hcode=''@Hcode'' and '+
             'Gjisa=''@Gjisa'' and '+
             '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';
    Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
    Translate(Sqlen, '@Gubun', nSqry.FieldByName('Gubun').AsString);
    Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
    Translate(Sqlen, '@Ocode', 'B');
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin

      Sqlon :=
      'UPDATE S1_Memo SET Gbigo=''@Gbigo'' ,Sbigo=''@Sbigo'' ,Gtel1=''@Gtel1'','+
      ' Gtel2=''@Gtel2'' ,Gname=''@Gname'' ,Gpost=''@Gpost'' ,Time3= now()';
      Sqlen :=
      ' WHERE Gdate=''@Gdate'' and Gubun=''@Gubun'' '+
      '  and  Jubun=''@Jubun'' and Gcode=''@Gcode'' '+
      '  and  Scode=''@Scode'' and Hcode=''@Hcode'' '+
      '  and  Gjisa=''@Gjisa'' and '+
      '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';

      Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gubun', nSqry.FieldByName('Gubun').AsString);
      Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
      Translate(Sqlen, '@Ocode', 'B');
      Translate(Sqlon, '@Gbigo', Edit207.Text);
      Translate(Sqlon, '@Sbigo', Edit208.Text);

      if StaticText1.Visible=True then
      Translate(Sqlon, '@Gtel1', '') else
      Translate(Sqlon, '@Gtel1', Edit209.Text);

      if StaticText2.Visible=True then
      Translate(Sqlon, '@Gtel2', '') else
      Translate(Sqlon, '@Gtel2', Edit210.Text);

      if StaticText3.Visible=True then
      Translate(Sqlon, '@Gname', '') else
      Translate(Sqlon, '@Gname', Edit211.Text);

      if StaticText4.Visible=True then
      Translate(Sqlon, '@Gpost', '') else
      Translate(Sqlon, '@Gpost', Edit212.Text);

      Base10.Socket.RunSQL(Sqlon+Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end else begin

      Sqlon :=
      'INSERT INTO S1_Memo '+
      '(Gdate, Gubun, Jubun, Gcode, Scode, Gjisa, Hcode, '+
      ' Ocode, Gbigo, Sbigo, Gtel1, Gtel2, Gname, Gpost, Time1) VALUES ';
      Sqlen :=
      '(''@Gdate'',''@Gubun'',''@Jubun'',''@Gcode'',''@Scode'', '+
      ' ''@Gjisa'',''@Hcode'',''@Ocode'',''@Gbigo'',''@Sbigo'', '+
      ' ''@Gtel1'',''@Gtel2'',''@Gname'',''@Gpost'', now() )';

      Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gubun', nSqry.FieldByName('Gubun').AsString);
      Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
      Translate(Sqlen, '@Ocode', 'B');
      Translate(Sqlen, '@Gbigo', Edit207.Text);
      Translate(Sqlen, '@Sbigo', Edit208.Text);

      if StaticText1.Visible=True then
      Translate(Sqlen, '@Gtel1', '') else
      Translate(Sqlen, '@Gtel1', Edit209.Text);

      if StaticText2.Visible=True then
      Translate(Sqlen, '@Gtel2', '') else
      Translate(Sqlen, '@Gtel2', Edit210.Text);

      if StaticText3.Visible=True then
      Translate(Sqlen, '@Gname', '') else
      Translate(Sqlen, '@Gname', Edit211.Text);

      if StaticText4.Visible=True then
      Translate(Sqlen, '@Gpost', '') else
      Translate(Sqlen, '@Gpost', Edit212.Text);

      Base10.Socket.RunSQL(Sqlon+Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end;
  end;
end;

procedure TSobo96.Button403Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  Cpost:='96';
  Subu00.Post_Show(Self);
  end;
end;

procedure TSobo96.Button501Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6,St8,St9: String;
begin
  Base10.OpenShow(tSqry);

  Button509Click(Self);

  St1:='Gdate'+' ='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Yesno'+' ='+#39+'2'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'Z'+#39;

  St2:=' Group By Gcode,Gjisa';

  Sqlen := 'Select Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  if Base10.G7_Ggeo.Locate('Gcode',mSqry.FieldByName('Hcode').AsString,[loCaseInsensitive])=true then
  St6:=Base10.G7_Ggeo.FieldByName('Gname').AsString;

  if St6='' then begin
  Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Gcode', mSqry.FieldByName('Hcode').AsString);
  St6:=Base10.Seek_Name(Sqlen);
  end;

  T02:=0;
  T03:=0;
  T04:=0;
  T05:=0;

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    //-----셋트수량-----//
    T06:=0;
    T07:=0;
    T08:=0;
    RBand:=0;
    While YGrid.RowCount-1 > RBand do begin
    RBand:=RBand+1;
      if(YGrid.Cells[ 0,RBand]=mSqry.FieldByName('Hcode').AsString)and
        (YGrid.Cells[ 1,RBand]=SGrid.Cells[ 0,List1])and
        (YGrid.Cells[ 2,RBand]=SGrid.Cells[ 1,List1])then begin
      T06:=StrToIntDef(YGrid.Cells[ 5,RBand],0)-1;
      T07:=StrToIntDef(YGrid.Cells[ 6,RBand],0);
      T08:=T08+T06*T07;
      end;
    end;
    //-----셋트수량-----//

    T01:=StrToIntDef(SGrid.Cells[ 2,List1],0)+T08;
    St3:=SGrid.Cells[ 0,List1];
    St4:='';
    St5:='';
    St9:='';

  { Sqlen := 'Select Gname From T1_Gbun Where '+D_Select+
             'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun''';
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Gjisa', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
    Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
    St4:=Base10.Seek_Name(Sqlen);
    St5:=''; }

    if Base10.G7_Ggeo.Locate('Gcode',mSqry.FieldByName('Hcode').AsString,[loCaseInsensitive])=true then begin
      if Base10.G7_Ggeo.FieldByName('Yes35').AsString='2' then begin
      Sqlen := 'Select Gname,Bebon From T1_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun''';
      Translate(Sqlen, '@Hcode', '');
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gjisa', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1);
        St9:=Base10.Socket.GetData(1, 2);
      end;
      end;
    end;

    if St4='' then begin
      Sqlen := 'Select Gname,Bebon From T1_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun''';
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gjisa', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1);
        St9:=Base10.Socket.GetData(1, 2);
      end;
    end;

  { if St8='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
                                                                St8:='1';
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end;
    if St8='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Hcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
                                                                St8:='1';
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end; }

    if St8='' then begin
      Sqlen := 'Select Pubun From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', '');
      St8:=Base10.Seek_Name(Sqlen);
      if St8='03' then St9:='2';
    end;

    if St8='' then begin
      Sqlen := 'Select Pubun From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      St8:=Base10.Seek_Name(Sqlen);
      if St8='03' then St9:='2';
    end;

    St9:='';

   if St9='' then begin

    if St4='' then
    if SGrid.Cells[ 1,List1]<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
      if Copy(SGrid.Cells[ 0,List1],1,1)<>'9' then
      Translate(Sqlen, '@Hcode', '') else
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Scode', 'Z');
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gname', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
      St4:=Base10.Seek_Name(Sqlen);
    end;

    if St4='' then begin
    { if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
      end;

      if St4='' then
      if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Hcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
      end; }

      if St4='' then begin
      Sqlen := 'Select Gubun From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', '');
      if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then  St4:='지방';
      end;

      if St4='' then begin
      Sqlen := 'Select Gubun From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
      end;
    end;

  { if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then
    St5:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if St5='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Hcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then
    St5:=Base10.G1_Ggeo.FieldByName('Gname').AsString; }

    if St5='' then begin
    Sqlen := 'Select Gname From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', '');
    St5:=Base10.Seek_Name(Sqlen);
    end;

    if St5='' then begin
    Sqlen := 'Select Gname From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
    St5:=Base10.Seek_Name(Sqlen);
    end;

    if SGrid.Cells[ 1,List1]<>'' then
    St5:=Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'2')+
    St5+ Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'1');

    if St4='시내' then begin
      T03:=T03+1;
      St1:=FloatToStr(T03);
    end else begin
      T02:=T02+1;
      St1:=FloatToStr(T02);
    end;

    if tSqry.Locate('Gdate',St1,[loCaseInsensitive])=False then begin
      tSqry.Append;
      tSqry.FieldByName('Scode').AsString:=mSqry.FieldByName('Hcode').AsString;
      tSqry.FieldByName('Gdate').AsString:=St1;
      tSqry.FieldByName('Name1').AsString:=St6;
      tSqry.FieldByName('Name2').AsString:=mSqry.FieldByName('Gdate').AsString;
    end;

    tSqry.Edit;
    if St4='시내' then begin
      Sqlen :=
      'Select Sum(Gqut1)as Gqut1,Sum(Gqut2)as Gqut2,Sum(Gqut3)as Gqut3 From T4_Ssub Where '+D_Select+
      'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' ';
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gdate', mSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gjisa', SGrid.Cells[ 1,List1]);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        tSqry.FieldByName('Gqut1').AsString:=Base10.Socket.GetData(1, 1);;
      end else begin
        tSqry.FieldByName('Gqut1').AsString:='1';
      end;

      tSqry.FieldByName('Gcode').AsString:=St3;
      tSqry.FieldByName('Gname').AsString:=St5;
      tSqry.FieldByName('GsumX').AsFloat :=T01;
      T04:=T04+T01;
    end else begin
      Sqlen :=
      'Select Sum(Gqut1)as Gqut1,Sum(Gqut2)as Gqut2,Sum(Gqut3)as Gqut3 From T4_Ssub Where '+D_Select+
      'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' ';
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gdate', mSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gjisa', SGrid.Cells[ 1,List1]);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        tSqry.FieldByName('Gqut2').AsString:=Base10.Socket.GetData(1, 1);;
      end else begin
        tSqry.FieldByName('Gqut2').AsString:='1';
      end;

      tSqry.FieldByName('Hcode').AsString:=St3;
      tSqry.FieldByName('Hname').AsString:=St5;
      tSqry.FieldByName('GsumY').AsFloat :=T01;
      T05:=T05+T01;
    end;
    tSqry.Post;

   end;

  end;
  if tSqry.RecordCount > 0 then
  Tong40.Print_21_02(Self);
end;

procedure TSobo96.Button509Click(Sender: TObject);
var St1,St2,St3,St4,St8,St9: String;
begin

  St1:='S.Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'S.Gdate'+'<='+#39+Edit101.Text+#39+' and '+
       'S.Gubun'+' ='+#39+'출고'+#39+' and '+
       'S.Yesno'+' ='+#39+'2'+#39+' and '+
       'S.Ocode'+' ='+#39+'B'+#39+' and '+
       'S.Scode'+' ='+#39+'Z'+#39;
  if (Edit104.Text<>'') Then
  St1:=St1+' and '+
       'S.Hcode'+'>='+#39+Edit102.Text+#39+' and '+
       'S.Hcode'+'<='+#39+Edit104.Text+#39;

  St1:=St1+' and '+'Y.Grat8'+'> '+'1';

  if D_Select<>'' then
  St1:=St1+' and '+'('+'S.Check is null '+' or '+'S.Check'+'<>'+#39+'D'+#39+')';

  if D_Select<>'' then
  St1:=St1+' and '+'('+'Y.Check is null '+' or '+'Y.Check'+'<>'+#39+'D'+#39+')';

  Sqlen := 'Select S.Hcode,S.Gcode,S.Gjisa,S.Jubun,S.Bcode,Y.Grat8,S.Gsqut From S1_Ssub S, G4_Book Y '+
           'Where S.Hcode=Y.Hcode and S.Bcode=Y.Gcode and '+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(YGrid)
  else ShowMessage(E_Open);

end;

procedure TSobo96.Button601Click(Sender: TObject);
begin
  Sqlen := 'UPDATE S1_Ssub SET Yesno=''@Yesno'' ,Time4= now()'+
  ' WHERE '+D_Select+
  ' Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
  ' Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
  ' Scode=''@Scode'' and Hcode=''@Hcode'' and '+
  ' Gjisa=''@Gjisa'' ';

  Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
  Translate(Sqlen, '@Gubun', '출고');
  Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
  Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
  Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
  Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
  Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
  Translate(Sqlen, '@Yesno', '2');

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
end;

procedure TSobo96.Button609Click(Sender: TObject);
var p_Scode,p_Gdate,p_Hcode,p_Gcode,p_Gubun,p_Jubun,p_Gjisa: String;
begin
  nSqry.First;
  While nSqry.EOF=False do begin
    if(nSqry.FieldByName('Gdate').AsString=p_Gdate)and
      (nSqry.FieldByName('Hcode').AsString=p_Hcode)and
      (nSqry.FieldByName('Gcode').AsString=p_Gcode)and
      (nSqry.FieldByName('Gubun').AsString=p_Gubun)and
      (nSqry.FieldByName('Jubun').AsString=p_Jubun)and
      (nSqry.FieldByName('Gjisa').AsString=p_Gjisa)and(nSqry.EOF=False)Then begin
    end else begin
      p_Scode:=nSqry.FieldByName('Scode').AsString;
      p_Gdate:=nSqry.FieldByName('Gdate').AsString;
      p_Hcode:=nSqry.FieldByName('Hcode').AsString;
      p_Gcode:=nSqry.FieldByName('Gcode').AsString;
      p_Gubun:=nSqry.FieldByName('Gubun').AsString;
      p_Jubun:=nSqry.FieldByName('Jubun').AsString;
      p_Gjisa:=nSqry.FieldByName('Gjisa').AsString;
      Button601Click(Self);
    end;
    nSqry.Next;
  end;

{ St1:='';
  nSqry.First;
  While nSqry.EOF=False do begin
    if nSqry.FieldByName('Jubun').AsString<>St1 then begin
      St1:=nSqry.FieldByName('Jubun').AsString;
      Button601Click(Self);
    end;
    nSqry.Next;
  end; }
end;

procedure TSobo96.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit103.Focused=True)and(Edit103.SelStart=50)and(Length(Trim(Edit103.Text))=50))or
    ((Edit105.Focused=True)and(Edit105.SelStart=50)and(Length(Trim(Edit105.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo96.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo96.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo96.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo96.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo96.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo96.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo96.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo96.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo96.Edit115KeyPress(Sender: TObject; var Key: Char);
var St1: String;
begin
  if Key=#13 Then begin
    mSqry.Filtered:=False;
    if Edit501.Text<>'' then begin
    St1:='('+' Gname '+' like '+#39+'%'+Edit501.Text+'%'+#39+')';
    mSqry.Filter:=St1;
    mSqry.Filtered:=True;
    end;
    DataSource2.Enabled:=False;
    DataSource2.Enabled:=True;
  end;
end;

procedure TSobo96.Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo96.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if Edit103.Focused=True Then begin
       Edit102.Text:='';
    if Edit103.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit103.Text;
    Seak80.FilterTing(Edit103.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit102.Text:=Seak80.Query1Gcode.AsString;
      Edit103.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit102.Text:=Seak80.Query1Gcode.AsString;
      Edit103.Text:=Seak80.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if Edit105.Focused=True Then begin
       Edit104.Text:='';
    if Edit105.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit105.Text;
    Seak80.FilterTing(Edit105.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit104.Text:=Seak80.Query1Gcode.AsString;
      Edit105.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit104.Text:=Seak80.Query1Gcode.AsString;
      Edit105.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo96.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo96.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo96.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var St1: String;
begin
  if nSqry.Active=True Then begin
  if Key=VK_F2 Then begin
    Delete_Seek(Self);
    if(mSqry.FieldByName('Yesno').AsString='1')or
      (mSqry.FieldByName('Yesno').AsString='0')then begin
      Button609Click(Self);
      mSqry.Edit;
      mSqry.FieldByName('Yesno').AsString:='2';
      mSqry.Post;
    end;
    Tong40.PrinTing00('24','1','','','','','','','','');
  end;
  if Key=VK_F3 Then begin
    mSqry.First;
    While mSqry.EOF=False do begin
    Delete_Seek(Self);
    if(mSqry.FieldByName('Yesno').AsString='1')or
      (mSqry.FieldByName('Yesno').AsString='0')then begin
      Button609Click(Self);
      mSqry.Edit;
      mSqry.FieldByName('Yesno').AsString:='2';
      mSqry.Post;
    end;
    Tong40.PrinTing00('24','1','','','','','','','','');
    mSqry.Next;
    end;
  end;
  if Key=VK_F4 Then begin
      Button501Click(Self);
    if(mSqry.FieldByName('Yesno').AsString='1')or
      (mSqry.FieldByName('Yesno').AsString='0')then begin
      mSqry.Edit;
      mSqry.FieldByName('Yesno').AsString:='2';
      mSqry.Post;
    end;
  end;
  if Key=VK_F5 Then begin
    St1:='';
    mSqry.First;
    While mSqry.EOF=False do begin
    if St1<>mSqry.FieldByName('Hcode').AsString then begin
       St1:=mSqry.FieldByName('Hcode').AsString;
       Button501Click(Self);
    end;
    if(mSqry.FieldByName('Yesno').AsString='1')or
      (mSqry.FieldByName('Yesno').AsString='0')then begin
      mSqry.Edit;
      mSqry.FieldByName('Yesno').AsString:='2';
      mSqry.Post;
      end;
      mSqry.Next;
    end;
  end;
{ if Key=VK_F4 Then begin
    Tong40.PrinTing00('24','2','','','','','','','','');
  end;
  if Key=VK_F5 Then begin
    While mSqry.EOF=False do begin
    Tong40.PrinTing00('24','2','','','','','','','','');
    mSqry.Next;
    end;
  end; }
{ if Key=VK_F7 Then Seak70.ShowModal; }
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo96.DBGrid201KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid201.SelectedIndex;
  sColumn:=DBGrid201.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=5 Then begin
      Tong20.PrinYing(Self);
    end else
    if SIndexs=6 Then begin
      Tong20.PrinYing(Self);
    end;
    DBGrid201.SelectedIndex:=SIndexs+1;
    end;
  end;
  end;
end;

procedure TSobo96.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid201.SelectedIndex;
  sColumn:=DBGrid201.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    if SIndexs=1 Then begin
    { DBGrid201.Columns.Items[SIndexs].Grid.EditorMode:=False;
      Keybd_event(VK_MENU,MapVirtualKey(VK_MENU,0),0,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),0,0);
      Keybd_event(VK_MENU,MapVirtualKey(VK_MENU,0),KEYEVENTF_KEYUP,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),KEYEVENTF_KEYUP,0); }
    end else
    if SIndexs=7 Then begin
      nSqry.Append; DBGrid201.SelectedIndex:=0;
    end;
  end;
  if Key=VK_F2 Then begin
    Delete_Seek(Self);
    Button609Click(Self);
  //Tong40.PrinTing00('24','1','','','','','','','','');
  end;
  if sColumn=False Then begin
    if nSqry.IsEmpty=False Then
    if Key=VK_DELETE Then T2_Sub61AfterDelete(nSqry);
  //if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo96.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(mSqry,Column);
end;

procedure TSobo96.DBGrid201TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo96.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Edit301.Text:=nSqry.FieldByName('Bcode').AsString;
  Edit302.Text:=nSqry.FieldByName('Bname').AsString;
  Edit303.Text:=nSqry.FieldByName('Jeago').AsString;
  Edit304.Text:=nSqry.FieldByName('Gbigo').AsString;
  Edit202.Text:=nSqry.FieldByName('Gmemo').AsString+' - '+nSqry.FieldByName('Jubun').AsString;;
  Label411.Caption:=nSqry.FieldByName('Time1').AsString;
  Label412.Caption:=nSqry.FieldByName('Time2').AsString;
  Label413.Caption:=nSqry.FieldByName('Time3').AsString;
  Label414.Caption:=nSqry.FieldByName('Time4').AsString;
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);

  Button301Click(Self);
end;

procedure TSobo96.DataSource2DataChange(Sender: TObject; Field: TField);
var St1: String;
begin
  Edit201.Text:=mSqry.FieldByName('Bname').AsString;
//Edit202.Text:=mSqry.FieldByName('Gmemo').AsString+' - '+mSqry.FieldByName('Jubun').AsString;;
  Edit203.Text:=mSqry.FieldByName('Hcode').AsString;
  Edit204.Text:=mSqry.FieldByName('Hname').AsString;
  Edit205.Text:=mSqry.FieldByName('Gcode').AsString;
  Edit206.Text:=mSqry.FieldByName('Gname').AsString;
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);

  St1:='';
  St1:=St1+'Hcode'+'='+#39+mSqry.FieldByName('Hcode').AsString+#39+' and ';
  St1:=St1+'Gcode'+'='+#39+mSqry.FieldByName('Gcode').AsString+#39+' and ';
//St1:=St1+'Scode'+'='+#39+mSqry.FieldByName('Scode').AsString+#39+' and ';
//St1:=St1+'Jubun'+'='+#39+mSqry.FieldByName('Jubun').AsString+#39+' and ';
  St1:=St1+'Gjisa'+'='+#39+mSqry.FieldByName('Gjisa').AsString+#39;
  nSqry.Filter:=St1;
  nSqry.Filtered:=True;
  Tong20.Srart_26_01(Self);
end;

procedure TSobo96.DBGrid201DblClick(Sender: TObject);
begin
  if(nSqry.RecordCount>0)Then begin
  Subu00.Menu901Click(Self);
  Sobo91.Edit103.Text:=T2_Sub61.FieldByName('Jubun').AsString;
  Sobo91.Edit101.Text:=T2_Sub61.FieldByName('Gdate').AsString;
  Sobo91.Edit104.Text:=T2_Sub62.FieldByName('Gcode').AsString;
  Sobo91.Edit105.Text:=T2_Sub62.FieldByName('Gname').AsString;
  Sobo91.Edit107.Text:=T2_Sub62.FieldByName('Hcode').AsString;
  Sobo91.Edit108.Text:=T2_Sub62.FieldByName('Hname').AsString;
  Sobo91.Label100.Visible:=False;
  Sobo91.Edit106.Visible:=False;
  Sobo91.Edit106.Items.Clear;
  if T2_Sub61.FieldByName('Gjisa').AsString<>'' then begin
  Sobo91.Label100.Visible:=True;
  Sobo91.Edit106.Visible:=True;
  Sobo91.Edit106.Items.Add(T2_Sub61.FieldByName('Gjisa').AsString);
  Sobo91.Edit106.ItemIndex:=0;
  end;
  Sobo91.Button101Click(Self);
  end;
end;

procedure TSobo96.Delete_Seek(Sender: TObject);
var St1: String;
begin
{ if D_Select<>'' then begin
  St1:='';
  St1:=St1+'Hcode'+'='+#39+mSqry.FieldByName('Hcode').AsString+#39+' and ';
  St1:=St1+'Gcode'+'='+#39+mSqry.FieldByName('Gcode').AsString+#39+' and ';
  St1:=St1+'Scode'+'='+#39+'Z'+#39+' and ';
  St1:=St1+'Gjisa'+'='+#39+mSqry.FieldByName('Gjisa').AsString+#39;
  nSqry.Filter:=St1;
  nSqry.Filtered:=True;
  end; }
end;

procedure TSobo96.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo96.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo96.Button701Click(Sender: TObject);
begin
    Seak80.Edit1.Text:='';
    Seak80.FilterTing('');
    if Seak80.Query1.RecordCount=1 Then begin
      Edit102.Text:=Seak80.Query1Gcode.AsString;
      Edit103.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      Edit102.Text:=Seak80.Query1Gcode.AsString;
      Edit103.Text:=Seak80.Query1Gname.AsString;
    end;
end;

procedure TSobo96.Button702Click(Sender: TObject);
begin
    Seak80.Edit1.Text:='';
    Seak80.FilterTing('');
    if Seak80.Query1.RecordCount=1 Then begin
      Edit104.Text:=Seak80.Query1Gcode.AsString;
      Edit105.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      Edit104.Text:=Seak80.Query1Gcode.AsString;
      Edit105.Text:=Seak80.Query1Gname.AsString;
    end;
end;

procedure TSobo96.Edit205Click(Sender: TObject);
begin
  if Edit209.Focused=True then
  StaticText1.Visible:=False;
  if Edit210.Focused=True then
  StaticText2.Visible:=False;
  if Edit211.Focused=True then
  StaticText3.Visible:=False;
  if Edit212.Focused=True then
  StaticText4.Visible:=False;
end;

procedure TSobo96.Edit205Exit(Sender: TObject);
begin
  StaticText1.Visible:=False;
  StaticText2.Visible:=False;
  StaticText3.Visible:=False;
  StaticText4.Visible:=False;
  if Edit209.Text='' then
  StaticText1.Visible:=True;
  if Edit210.Text='' then
  StaticText2.Visible:=True;
  if Edit211.Text='' then
  StaticText3.Visible:=True;
  if Edit212.Text='' then
  StaticText4.Visible:=True;
end;

procedure TSobo96.StaticText1Click(Sender: TObject);
begin
  StaticText1.Visible:=False;
  Edit209.SetFocus;
end;

procedure TSobo96.StaticText2Click(Sender: TObject);
begin
  StaticText2.Visible:=False;
  Edit210.SetFocus;
end;

procedure TSobo96.StaticText3Click(Sender: TObject);
begin
  StaticText3.Visible:=False;
  Edit211.SetFocus;
end;

procedure TSobo96.StaticText4Click(Sender: TObject);
begin
  StaticText4.Visible:=False;
  Edit212.SetFocus;
end;

procedure TSobo96.DBGrid201DrawColumnCell(Sender: TObject;
  const Rect: TRect; DataCol: Integer; Column: TColumnEh;
  State: TGridDrawState);
begin
{ if D_Select<>'' then begin
  with (Sender as TDBGrid) do begin
    if(DBGrid201.SelectedRows.CurrentRowSelected = False) then begin
      if(Column.FieldName='JUBUN')or(Column.FieldName='PUBUN')or
        (Column.FieldName='BNAME')or(Column.FieldName='GDANG')then begin
      //(Column.FieldName='QSQUT')or(Column.FieldName='GSQUT')or
      //(Column.FieldName='GRAT1')or(Column.FieldName='GSSUM')then begin
        if nSqry.FieldByName('Scode').AsString='1'
        then Canvas.Brush.Color := clRed
        else Canvas.Brush.Color := clwhite;

        Canvas.Font.Color := Font.Color;
        DBGrid201.DefaultDrawColumnCell(Rect, DataCol, Column, State);
      end;
    end;
  end;
  end; }
end;

procedure TSobo96.Seek_Post(Sender: TObject);
begin
  nSqry.BeforePost:=nil;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;
  nSqry.First;
  While nSqry.EOF=False do begin
    Sqlen := 'Select Gpost From G4_Book '+
             'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Bcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      nSqry.Edit;
      if Base10.Database.Database='chul_02_db' then
      nSqry.FieldByName('Gpost').AsString:=Trim(Copy(AutoFrx(Base10.Socket.GetData(1, 1)),1,10))
      else
      nSqry.FieldByName('Gpost').AsString:=nSqry.FieldByName('Bcode').AsString;
    //Format('%09s',[FormatFloat('000000000',nSqry.FieldByName('Bcode').AsInteger)] );
      nSqry.Post;
    end;

    nSqry.Next;
  end;
  nSqry.First;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  nSqry.BeforePost:=T2_Sub61BeforePost;
end;

procedure TSobo96.T2_Sub62YESNOGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=Base10.LockCheck1(T2_Sub61.FieldByName('Yesno').AsString);
end;

procedure TSobo96.T2_Sub62YESNOSetText(Sender: TField; const Text: String);
begin
  T2_Sub61.FieldByName('Yesno').AsString:=Base10.LockCheck2(Text);
end;

procedure TSobo96.T2_Sub61AfterCancel(DataSet: TDataSet);
begin
  T2_Sub61AfterScroll(T2_Sub61);
end;

procedure TSobo96.T2_Sub61AfterScroll(DataSet: TDataSet);
begin
{ Ocode:= T2_Sub11.FieldByName('Ocode').AsString;
  Pubun:= T2_Sub11.FieldByName('Pubun').AsString;
  Gsqut:=-T2_Sub11.FieldByName('Gsqut').AsFloat;
  Gssum:=-T2_Sub11.FieldByName('Gssum').AsFloat; }
end;

procedure TSobo96.T2_Sub61AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TSobo96.T2_Sub61AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub61ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub61Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      //--//
    { if(T2_Sub61Ocode.AsString='B')and(T2_Sub61Gcode.AsString='00001')then begin

        Sqlen := 'DELETE FROM Sg_Csum WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';
        Translate(Sqlen, '@Scode', 'A');
        Translate(Sqlen, '@Gbigo', T2_Sub61ID.AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.BusyLoop;
        if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      end; }

    end else begin
      Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub61ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub61Gdate.AsString);
      Translate(Sqlen, '@Scode', '1');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      //--//
    { if(T2_Sub61Ocode.AsString='B')and(T2_Sub61Gcode.AsString='00001')then begin

        Sqlen := 'DELETE FROM Sg_Csum WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';
        Translate(Sqlen, '@Scode', 'A');
        Translate(Sqlen, '@Gbigo', T2_Sub61ID.AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.BusyLoop;
        if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      end; }

    end;

  //S2101:=S2101-T2_Sub61Gsqut.AsFloat;
  //S2102:=S2102-T2_Sub61Gssum.AsFloat;
    T2_Sub61.Delete;

  end; end;

end;

procedure TSobo96.T2_Sub61BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub61.State=dsInsert)Then begin

  { Sqlon := 'INSERT INTO S1_Ssub '+
    '(Gdate, Scode, Gcode, Hcode, Ocode, Bcode, '+
    ' Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang, '+
    ' Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Ocode'',''@Bcode'', '+
    ' ''@Gubun'',''@Jubun'',''@Pubun'',''@Gbigo'',  @Gsqut  ,  @Gdang  , '+
    '   @Grat1  ,  @Gssum  ,  @Qsqut  ,  @Jeago  ,''@Yesno'',''@Gjisa'')';

    Translate(Sqlen, '@Gdate', T2_Sub61Gdate.AsString);
    Translate(Sqlen, '@Scode', T2_Sub61Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub61Gcode.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub61Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub61Ocode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub61Bcode.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub61Gubun.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub61Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub61Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub61Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub61Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub61Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub61Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub61Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub61Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub61Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub61Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub61Gjisa.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S1_SSUB_ID_GEN');
    Base10.Update_Idnum(nSqry,'S1_SSUB_ID_NUM'); }

  //S2101:=S2101+T2_Sub61Gsqut.AsFloat;
  //S2102:=S2102+T2_Sub61Gssum.AsFloat;

  end else begin

    Sqlon := 'UPDATE S1_Ssub SET '+
    'Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'',Ocode=''@Ocode'', '+
    'Bcode=''@Bcode'',Gubun=''@Gubun'',Jubun=''@Jubun'',Pubun=''@Pubun'', ';
    Sqlen :=
    'Gbigo=''@Gbigo'',Gsqut=  @Gsqut  ,Gdang=  @Gdang  ,Grat1=  @Grat1  , '+
    'Gssum=  @Gssum  ,Qsqut=  @Qsqut  ,Jeago=  @Jeago  ,Yesno=''@Yesno'', '+
    'Gjisa=''@Gjisa'' WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', T2_Sub61Gdate.AsString);
    Translate(Sqlon, '@Scode', T2_Sub61Scode.AsString);
    Translate(Sqlon, '@Gcode', T2_Sub61Gcode.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub61Hcode.AsString);
    Translate(Sqlon, '@Ocode', T2_Sub61Ocode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub61Bcode.AsString);
    Translate(Sqlon, '@Gubun', T2_Sub61Gubun.AsString);
    Translate(Sqlon, '@Jubun', T2_Sub61Jubun.AsString);
    Translate(Sqlon, '@Pubun', T2_Sub61Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub61Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub61Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub61Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub61Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub61Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub61Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub61Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub61Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub61Gjisa.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub61ID.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  //S2101:=S2101+T2_Sub61Gsqut.AsFloat+Gsqut;
  //S2102:=S2102+T2_Sub61Gssum.AsFloat+Gssum;

  end;

end;

procedure TSobo96.T2_Sub61BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub61 do
  if(State in dsEditModes)Then Post;
end;

procedure TSobo96.T2_Sub61NewRecord(DataSet: TDataSet);
begin
{ T2_Sub61Gubun.Value:=Edit103.Text;
  T2_Sub61Bcode.Value:=Edit104.Text;
  T2_Sub61Ycode.Value:=Edit107.Text;
  T2_Sub61Gssum.Value:=0;
  if Gdate<>'' Then
  T2_Sub61Gdate.Value:=Gdate else
  T2_Sub61Gdate.Value:=FormatDateTime('yyyy"."mm"."dd',Date); }
end;

procedure TSobo96.ColumnX1(TableX: TClientDataSet);
var I: Integer;
  St1: Integer;
cFieldname: string;
  St8:array [0..21] of String;
  St9:array [0..21] of String;
  St0,St2,p_Idnum: Integer;
  p_Scode,p_Gdate,p_Gcode,p_Gubun,p_Jubun,p_Gjisa: String;
begin
  //텍배.xls
  if Base10.Database.Database='book_kb_db' then begin
    St0:=9;
    St8[00]:='Hname'; St9[00]:='출판사명';
    St8[01]:='Gdate'; St9[01]:='송화인연락처';
    St8[02]:='Hcode'; St9[02]:='송화인주소';
    St8[03]:='Gadds'; St9[03]:='주소';
  //St8[04]:='Gadd2'; St9[04]:='주소2';
    St8[04]:='Htels'; St9[04]:='핸드폰번호';
    St8[05]:='Gtels'; St9[05]:='전화번호';
    St8[06]:='Gtels'; St9[06]:='받는사람';
    St8[07]:='Gqut1'; St9[07]:='수량';
    St8[08]:='Gqut2'; St9[08]:='건수';
    if TableX.Active=True Then begin
       Application.CreateForm(TTong10, Tong10);
       St1:=1;
       T01:=0;
       TableX.First;
       for I := 0 to St0 - 1 do begin
         cFieldname:=St9[I];
         Tong10.F1Book1.TextRC[1,I+1]:=cFieldname;
         cFieldname:=St8[I];
         if I = 0 then
         Tong10.F1Book1.ColWidth[I+1]:=8*900
         else
         if I = 1 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 2 then
         Tong10.F1Book1.ColWidth[I+1]:=8*900
         else
         if I = 3 then
         Tong10.F1Book1.ColWidth[I+1]:=8*2500
         else
         if I = 4 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 5 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 6 then
         Tong10.F1Book1.ColWidth[I+1]:=8*900
         else
         if I = 7 then
         Tong10.F1Book1.ColWidth[I+1]:=8*200
         else
         if I = 8 then
         Tong10.F1Book1.ColWidth[I+1]:=8*200
         else
         Tong10.F1Book1.ColWidth[I+1]:=TableX.FieldByName(cFieldname).DisplayWidth*300;
       end;
       While TableX.EOF=False do begin

         St1:=St1+1;
         for I := 0 to St0 - 1 do begin
           cFieldname:=St8[I];
         { if TableX.FieldByName(cFieldname).DataType=ftString Then
           Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
           Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat; }
           if I = 0 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString;
           end else
           if I = 1 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='031-923-1212';
           end else
           if I = 2 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='경기 고양 일산서구 구산동 142-4';
           end else
           if I = 3 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit203.Text+' '+Edit204.Text;
           end else
           if I = 4 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit205.Text;
           end else
           if I = 5 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit206.Text;
           end else
           if I = 6 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit207.Text;
           end else
           if I = 7 then begin
             Tong10.F1Book1.NumberRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsInteger;
           end else
           if I = 8 then begin
             Tong10.F1Book1.NumberRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsInteger;
           end else begin
             Tong10.F1Book1.NumberRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsInteger;
           end;
         end;
         TableX.Next;
       end;
       Tong10.ShowModal;
    end;
  end else
  if Base10.Database.Database='chul_03_db' then begin
    St0:=12;
    St8[00]:='Hname'; St9[00]:='받으시는분';
    St8[01]:='Gdate'; St9[01]:='담당자';
    St8[02]:='Hcode'; St9[02]:='전화';
    St8[03]:='Gadds'; St9[03]:='핸드폰';
    St8[04]:='Htels'; St9[04]:='우편번호';
    St8[05]:='Gtels'; St9[05]:='주    소';
    St8[06]:='Gtels'; St9[06]:='수량';
    St8[07]:='Gqut1'; St9[07]:='품목';
    St8[08]:='Gqut2'; St9[08]:='운임타입';
    St8[09]:='Gqut3'; St9[09]:='지불조건';
    St8[10]:='Gqut4'; St9[10]:='출고번호';
    St8[11]:='Gqut5'; St9[11]:='특기사항';
    if TableX.Active=True Then begin
       Application.CreateForm(TTong10, Tong10);
       St1:=1;
       T01:=0;
       TableX.First;
       for I := 0 to St0 - 1 do begin
         cFieldname:=St9[I];
         Tong10.F1Book1.TextRC[1,I+1]:=cFieldname;
         cFieldname:=St8[I];
         if I = 0 then
         Tong10.F1Book1.ColWidth[I+1]:=8*800
         else
         if I = 1 then
         Tong10.F1Book1.ColWidth[I+1]:=8*300
         else
         if I = 2 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 3 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 4 then
         Tong10.F1Book1.ColWidth[I+1]:=8*300
         else
         if I = 5 then
         Tong10.F1Book1.ColWidth[I+1]:=8*2500
         else
         if I = 6 then
         Tong10.F1Book1.ColWidth[I+1]:=8*300
         else
         if I = 7 then
         Tong10.F1Book1.ColWidth[I+1]:=8*300
         else
         if I = 8 then
         Tong10.F1Book1.ColWidth[I+1]:=8*300
         else
         if I = 9 then
         Tong10.F1Book1.ColWidth[I+1]:=8*300
         else
         if I = 10 then
         Tong10.F1Book1.ColWidth[I+1]:=8*300
         else
         if I = 11 then
         Tong10.F1Book1.ColWidth[I+1]:=8*300
         else
         Tong10.F1Book1.ColWidth[I+1]:=TableX.FieldByName(cFieldname).DisplayWidth*300;
       end;
       While TableX.EOF=False do begin

         St1:=St1+1;
         for I := 0 to St0 - 1 do begin
           cFieldname:=St8[I];
         { if TableX.FieldByName(cFieldname).DataType=ftString Then
           Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
           Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat; }
           if I = 0 then begin
             p_Gcode:=Edit207.Text;
             Translate(p_Gcode, '?', '');
             Tong10.F1Book1.TextRC[St1,I+1]  :=p_Gcode;
           end else
           if I = 1 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='';
           end else
           if I = 2 then begin
             p_Gcode:=Edit206.Text;
             Translate(p_Gcode, '?', '');
             Tong10.F1Book1.TextRC[St1,I+1]  :=p_Gcode;
           end else
           if I = 3 then begin
             p_Gcode:=Edit205.Text;
             Translate(p_Gcode, '?', '');
             Tong10.F1Book1.TextRC[St1,I+1]  :=p_Gcode;
           end else
           if I = 4 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='';
           end else
           if I = 5 then begin
             p_Gcode:=Edit203.Text+' '+Edit204.Text;
             Translate(p_Gcode, '?', '');
             Translate(p_Gcode, '?', '');
             Translate(p_Gcode, '?', '');
             Tong10.F1Book1.TextRC[St1,I+1]  :=p_Gcode;
           end else
           if I = 6 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName('Gqut1').AsString;
           end else
           if I = 7 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='';
           end else
           if I = 8 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='';
           end else begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='';
           end;
         end;
         TableX.Next;
       end;
       Tong10.ShowModal;
    end;
  end else
  if Base10.Database.Database='chul_05_db' then begin
    St0:=9;
    St8[00]:='Hname'; St9[00]:='받는사람';
    St8[01]:='Gdate'; St9[01]:='';
    St8[02]:='Hcode'; St9[02]:='주소';
    St8[03]:='Gadds'; St9[03]:='전화번호';
    St8[04]:='Htels'; St9[04]:='핸드폰번호';
    St8[05]:='Gtels'; St9[05]:='수량';
    St8[06]:='Gtels'; St9[06]:='';
    St8[07]:='Gqut1'; St9[07]:='출판사';
    St8[08]:='Gqut2'; St9[08]:='메모';
    if TableX.Active=True Then begin
       Application.CreateForm(TTong10, Tong10);
       St1:=1;
       T01:=0;
       TableX.First;
       for I := 0 to St0 - 1 do begin
         cFieldname:=St9[I];
         Tong10.F1Book1.TextRC[1,I+1]:=cFieldname;
         cFieldname:=St8[I];
         if I = 0 then
         Tong10.F1Book1.ColWidth[I+1]:=8*900
         else
         if I = 1 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 2 then
         Tong10.F1Book1.ColWidth[I+1]:=8*900
         else
         if I = 3 then
         Tong10.F1Book1.ColWidth[I+1]:=8*2500
         else
         if I = 4 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 5 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 6 then
         Tong10.F1Book1.ColWidth[I+1]:=8*900
         else
         if I = 7 then
         Tong10.F1Book1.ColWidth[I+1]:=8*200
         else
         if I = 8 then
         Tong10.F1Book1.ColWidth[I+1]:=8*200
         else
         Tong10.F1Book1.ColWidth[I+1]:=TableX.FieldByName(cFieldname).DisplayWidth*300;
       end;
       While TableX.EOF=False do begin

         St1:=St1+1;
         for I := 0 to St0 - 1 do begin
           cFieldname:=St8[I];
         { if TableX.FieldByName(cFieldname).DataType=ftString Then
           Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
           Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat; }
           if I = 0 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString;
           end else
           if I = 1 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='031-923-1212';
           end else
           if I = 2 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='경기 고양 일산서구 구산동 142-4';
           end else
           if I = 3 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit203.Text+' '+Edit204.Text;
           end else
           if I = 4 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit205.Text;
           end else
           if I = 5 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit206.Text;
           end else
           if I = 6 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit207.Text;
           end else
           if I = 7 then begin
             Tong10.F1Book1.NumberRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsInteger;
           end else
           if I = 8 then begin
             Tong10.F1Book1.NumberRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsInteger;
           end else begin
             Tong10.F1Book1.NumberRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsInteger;
           end;
         end;
         TableX.Next;
       end;
       Tong10.ShowModal;
    end;
  end else begin
    St0:=9;
    St8[00]:='Hname'; St9[00]:='출판사명';
    St8[01]:='Gdate'; St9[01]:='송화인연락처';
    St8[02]:='Hcode'; St9[02]:='송화인주소';
    St8[03]:='Gadds'; St9[03]:='주소';
  //St8[04]:='Gadd2'; St9[04]:='주소2';
    St8[04]:='Htels'; St9[04]:='핸드폰번호';
    St8[05]:='Gtels'; St9[05]:='전화번호';
    St8[06]:='Gtels'; St9[06]:='받는사람';
    St8[07]:='Gqut1'; St9[07]:='수량';
    St8[08]:='Gqut2'; St9[08]:='건수';
    if TableX.Active=True Then begin
       Application.CreateForm(TTong10, Tong10);
       St1:=1;
       T01:=0;
       TableX.First;
       for I := 0 to St0 - 1 do begin
         cFieldname:=St9[I];
         Tong10.F1Book1.TextRC[1,I+1]:=cFieldname;
         cFieldname:=St8[I];
         if I = 0 then
         Tong10.F1Book1.ColWidth[I+1]:=8*900
         else
         if I = 1 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 2 then
         Tong10.F1Book1.ColWidth[I+1]:=8*900
         else
         if I = 3 then
         Tong10.F1Book1.ColWidth[I+1]:=8*2500
         else
         if I = 4 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 5 then
         Tong10.F1Book1.ColWidth[I+1]:=8*600
         else
         if I = 6 then
         Tong10.F1Book1.ColWidth[I+1]:=8*900
         else
         if I = 7 then
         Tong10.F1Book1.ColWidth[I+1]:=8*200
         else
         if I = 8 then
         Tong10.F1Book1.ColWidth[I+1]:=8*200
         else
         Tong10.F1Book1.ColWidth[I+1]:=TableX.FieldByName(cFieldname).DisplayWidth*300;
       end;
       While TableX.EOF=False do begin

         St1:=St1+1;
         for I := 0 to St0 - 1 do begin
           cFieldname:=St8[I];
         { if TableX.FieldByName(cFieldname).DataType=ftString Then
           Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString else
           Tong10.F1Book1.NumberRC[St1,I+1]:=TableX.FieldByName(cFieldname).AsFloat; }
           if I = 0 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsString;
           end else
           if I = 1 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='031-111-2222';
           end else
           if I = 2 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='경기도 ???(주소)';
           end else
           if I = 3 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit203.Text+' '+Edit204.Text;
           end else
           if I = 4 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit205.Text;
           end else
           if I = 5 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit206.Text;
           end else
           if I = 6 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :=Edit207.Text;
           end else
           if I = 7 then begin
             Tong10.F1Book1.NumberRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsInteger;
           end else
           if I = 8 then begin
             Tong10.F1Book1.NumberRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsInteger;
           end else begin
             Tong10.F1Book1.NumberRC[St1,I+1]  :=TableX.FieldByName(cFieldname).AsInteger;
           end;
         end;
         TableX.Next;
       end;
       Tong10.ShowModal;
    end;
  end;
end;

end.
