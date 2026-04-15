unit Subu91;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, Tong07, CornerButton,
  dxCore, dxButtons, ToolEdit, DBGridEh, DBClient;

type
  TSobo91 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel003: TFlatPanel;
    Panel007: TFlatPanel;
    Panel101: TFlatPanel;
    Panel104: TFlatPanel;
    Panel105: TFlatPanel;
    Panel102: TFlatPanel;
    Panel103: TFlatPanel;
    Panel201: TFlatPanel;
    Panel203: TFlatPanel;
    Panel202: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Button201: TFlatButton;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatComboBox;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Edit201: TFlatEdit;
    Edit202: TFlatEdit;
    Edit203: TFlatEdit;
    Edit204: TFlatEdit;
    Panel106: TFlatPanel;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Panel401: TFlatPanel;
    Panel204: TFlatPanel;
    Label100: TmyLabel3d;
    Edit106: TFlatComboBox;
    Edit205: TFlatEdit;
    Edit206: TFlatEdit;
    Edit207: TFlatEdit;
    StaticText1: TStaticText;
    StaticText2: TStaticText;
    StaticText3: TStaticText;
    Button801: TFlatButton;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton3: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label303: TmyLabel3d;
    Label309: TmyLabel3d;
    DBGrid101: TDBGridEh;
    DateEdit1: TDateEdit;
    Button901: TFlatButton;
    Button701: TFlatButton;
    Button702: TFlatButton;
    dxButton1: TdxButton;
    Label103: TmyLabel3d;
    Label104: TmyLabel3d;
    Edit109: TFlatEdit;
    Edit208: TFlatEdit;
    StaticText4: TStaticText;
    Button802: TFlatButton;
    Button803: TFlatButton;
    T2_Sub11: TClientDataSet;
    T2_Sub11ID: TFloatField;
    T2_Sub11IDNUM: TFloatField;
    T2_Sub11GDATE: TStringField;
    T2_Sub11SCODE: TStringField;
    T2_Sub11GCODE: TStringField;
    T2_Sub11GNAME: TStringField;
    T2_Sub11HCODE: TStringField;
    T2_Sub11OCODE: TStringField;
    T2_Sub11BCODE: TStringField;
    T2_Sub11BNAME: TStringField;
    T2_Sub11GJEJA: TStringField;
    T2_Sub11GUBUN: TStringField;
    T2_Sub11JUBUN: TStringField;
    T2_Sub11PUBUN: TStringField;
    T2_Sub11GSQUT: TFloatField;
    T2_Sub11QSQUT: TFloatField;
    T2_Sub11GDANG: TFloatField;
    T2_Sub11GRAT1: TSmallintField;
    T2_Sub11GSSUM: TFloatField;
    T2_Sub11JEAGO: TFloatField;
    T2_Sub11GBIGO: TStringField;
    T2_Sub11YESNO: TStringField;
    T2_Sub11GJISA: TStringField;
    T2_Sub11GPOST: TStringField;
    T2_Sub11QPOST: TStringField;
    T2_Sub12: TClientDataSet;
    T2_Sub12ID: TFloatField;
    T2_Sub12IDNUM: TFloatField;
    T2_Sub12GDATE: TStringField;
    T2_Sub12SCODE: TStringField;
    T2_Sub12GCODE: TStringField;
    T2_Sub12GNAME: TStringField;
    T2_Sub12HCODE: TStringField;
    T2_Sub12OCODE: TStringField;
    T2_Sub12BCODE: TStringField;
    T2_Sub12BNAME: TStringField;
    T2_Sub12GJEJA: TStringField;
    T2_Sub12GUBUN: TStringField;
    T2_Sub12JUBUN: TStringField;
    T2_Sub12PUBUN: TStringField;
    T2_Sub12GSQUT: TFloatField;
    T2_Sub12QSQUT: TFloatField;
    T2_Sub12GDANG: TFloatField;
    T2_Sub12GRAT1: TSmallintField;
    T2_Sub12GSSUM: TFloatField;
    T2_Sub12JEAGO: TFloatField;
    T2_Sub12GBIGO: TStringField;
    T2_Sub12YESNO: TStringField;
    T2_Sub12GJISA: TStringField;
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
    procedure Button501Click(Sender: TObject);
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
    procedure Edit301KeyPress(Sender: TObject; var Key: Char);
    procedure Button801Click(Sender: TObject);
    procedure Button802Click(Sender: TObject);
    procedure Button803Click(Sender: TObject);
    procedure Edit205Click(Sender: TObject);
    procedure Edit205Exit(Sender: TObject);
    procedure StaticText1Click(Sender: TObject);
    procedure StaticText2Click(Sender: TObject);
    procedure StaticText3Click(Sender: TObject);
    procedure StaticText4Click(Sender: TObject);
    procedure T2_Sub11GSQUTChange(Sender: TField);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure Seek_Post(Sender: TObject);
    procedure T2_Sub11YESNOGetText(Sender: TField; var Text: String;
      DisplayText: Boolean);
    procedure T2_Sub11YESNOSetText(Sender: TField; const Text: String);
    procedure T2_Sub11AfterCancel(DataSet: TDataSet);
    procedure T2_Sub11AfterScroll(DataSet: TDataSet);
    procedure T2_Sub11AfterDelete(DataSet: TDataSet);
    procedure T2_Sub11AfterPost(DataSet: TDataSet);
    procedure T2_Sub11BeforePost(DataSet: TDataSet);
    procedure T2_Sub11NewRecord(DataSet: TDataSet);
    procedure T2_Sub11BeforeClose(DataSet: TDataSet);
  private
    { Private declarations }
  public
    Frame: TFrame;
    FTong07: TTong70;
    { Public declarations }
  protected
  //  procedure WndProc(var Msg: TMessage); override;
  end;

var
  Sobo91: TSobo91;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib, Subu20,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo91.FormActivate(Sender: TObject);
begin
  nForm:='91';
  nSqry:=T2_Sub11;
  mSqry:=T2_Sub12;
  tSqry:=T4_Sub81;
end;

procedure TSobo91.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo91.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo91:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Base10.OpenExit(tSqry);
end;

procedure TSobo91.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo91.Button002Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Button015Click(Self);
  end; }
end;

procedure TSobo91.Button003Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo91.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo91.Button005Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     Application.CreateForm(TSobo20, Sobo20);
     Sobo20.ShowModal;
  end;
end;

procedure TSobo91.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo91.Button007Click(Sender: TObject);
begin
  if nSqry.Active=True Then
     Button401Click(Self);
end;

procedure TSobo91.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo91.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo91.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo91.Button011Click(Sender: TObject);
begin
{ Tong20.DBGridSaveHtml(DBGrid201, Caption); }
end;

procedure TSobo91.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY0(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo91.Button013Click(Sender: TObject);
begin
{ oSqry:=mSqry;
  Base10.ColumnY1(oSqry,DBGrid201,ProgressBar1); }
end;

procedure TSobo91.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('21-01');
end;

procedure TSobo91.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('21-02');
end;

procedure TSobo91.Button016Click(Sender: TObject);
begin
  nSqry.First;
  While nSqry.EOF=False do begin
    if(nSqry.FieldByName('Yesno').AsString='1')or
      (nSqry.FieldByName('Yesno').AsString='0')then begin
    nSqry.Edit;
    nSqry.FieldByName('Yesno').AsString:='2';
    nSqry.Post;
    end;
    nSqry.Next;
  end;

  nSqry.First;
  if nSqry.RecordCount >= 1 then begin
    Sqlen := 'UPDATE S1_Ssub SET Time4= now() '+
    ' WHERE Gdate=''@Gdate'' and Gubun=''@Gubun'' and Jubun=''@Jubun'' '+
    '   and Scode=''@Scode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa'' '+
    '   and Ocode=''@Ocode'' and Hcode=''@Hcode'' ';

    Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
    Translate(Sqlen, '@Gubun', nSqry.FieldByName('Gubun').AsString);
    Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
    Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
    Translate(Sqlen, '@Ocode', nSqry.FieldByName('Ocode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Yesno', '2'   );

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
  end;

//if(nSqry.FieldByName('Hcode').AsString='122')and
  if(Base10.Database.Database='book_05_db')then begin
  Seek_Post(Self);
  nSqry.IndexName := 'IDX'+'QPOST'+'DOWN';
  Tong40.print_21_01(Self);
  nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  end else
  Tong40.print_21_01(Self);
end;

procedure TSobo91.Button017Click(Sender: TObject);
begin
  nSqry.First;
  While nSqry.EOF=False do begin
    if(nSqry.FieldByName('Yesno').AsString='1')or
      (nSqry.FieldByName('Yesno').AsString='0')then begin
    nSqry.Edit;
    nSqry.FieldByName('Yesno').AsString:='2';
    nSqry.Post;
    end;
    nSqry.Next;
  end;
  oSqry:=nSqry;

//if(nSqry.FieldByName('Hcode').AsString='122')and
  if(Base10.Database.Database='book_05_db')then begin
  Seek_Post(Self);
  nSqry.IndexName := 'IDX'+'QPOST'+'DOWN';
  Tong40.PrinTing00('21','2','','','','','','','','');
  nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  end else
  Tong40.PrinTing00('21','2','','','','','','','','');
end;

procedure TSobo91.Button018Click(Sender: TObject);
begin
  Seak60.ShowModal;
end;

procedure TSobo91.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo91.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo91.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont4(DBGrid101);
end;

procedure TSobo91.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo91.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo91.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo91.Button101Click(Sender: TObject);
var St1: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  if Base10.Seek_Hgeo('Z',Edit104.Text,Edit107.Text)='X' Then Exit;

  Sqlen := 'Select Grat9 From G5_Ggeo Where '+D_Select+'Hcode=''@Hcode'' and Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Hcode', '');
  Translate(Sqlen, '@Gcode', Edit104.Text);
  if Base10.Seek_Name(Sqlen)='1' then begin
     ShowMessage('출고정지된 거래처입니다. 다시 선택해 주십시오.');
     Edit104.SetFocus;
     Exit;
  end else begin

{ Sqlen := 'Select Gbigo From H2_Gbun Where '+D_Select+
           'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun'' ';
  if Copy(Edit104.Text,1,1)<>'9' then
  Translate(Sqlen, '@Hcode', '') else
  Translate(Sqlen, '@Hcode', Edit107.Text);
  Translate(Sqlen, '@Gcode', Edit104.Text);
  Translate(Sqlen, '@Gname', Base10.Seek_Jisa(Edit106.Text,'3'));
  Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(Edit106.Text,'4'));
  St1:=Base10.Seek_Name(Sqlen);
  if St1<>'' then begin
     ShowMessage('출고정지된 지점입니다. 다시 선택해 주십시오.'+#13+#13+St1);
     Edit106.SetFocus;
     Exit;
  end; }

  end;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.FieldByName('Gsqut').OnChange:=nil;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;

  Sqlen := 'Select * From S1_Ssub Where '+D_Select+
           'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
           'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
           'Scode=''@Scode'' and Gjisa=''@Gjisa'' and '+
           'Ocode=''@Ocode'' and Hcode=''@Hcode''';

  Translate(Sqlen, '@Gdate', Edit101.Text);
  Translate(Sqlen, '@Gubun', Edit102.Text);
  Translate(Sqlen, '@Jubun', Edit103.Text);
  Translate(Sqlen, '@Gcode', Edit104.Text);
  Translate(Sqlen, '@Ocode', 'B');
  Translate(Sqlen, '@Scode', 'Z');
  Translate(Sqlen, '@Gjisa', Edit106.Text);
  Translate(Sqlen, '@Hcode', Edit107.Text);

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
    nSqry.FieldByName('Gname').Value:=Edit105.Text;

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

  Button301Click(Self);

  if Base10.Database.Database='book_kb_db' then
  nSqry.IndexName := 'IDX'+'BCODE'+'DOWN'
  else
  nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  nSqry.First;
  Tong20.Srart_21_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=T2_Sub11BeforePost;
  nSqry.FieldByName('Gsqut').OnChange:=T2_Sub11GSQUTChange;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo91.Button201Click(Sender: TObject);
var X: Word;
begin
  Seek40.Edit2.Value:=0;
  Seek40.Edit1.Text:='';
  Seek40.FilterTing('',Edit107.Text);
{ Seek40.Query1.Close;
  Seek40.Query1.Open; }
  if Seek40.ShowModal=mrOK Then begin
    with Seek40.DBgrid101.SelectedRows do
    if Count > 0 then begin
      for X:=0 to Count-1 do begin
        if IndexOf(Items[X]) > -1 then begin
          Seek40.DBGrid101.Datasource.Dataset.Bookmark:=Items[X];
          nSqry.Append;
          Bcode:=Seek40.Query1Gcode.AsString;
          nSqry.FieldByName('Bcode').Value:=Bcode;
          nSqry.FieldByName('Gsqut').Value:=Seek40.Edit2.Value;

          Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G5_Ggeo '+
                   'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
          Translate(Sqlen, '@Gcode', Edit104.Text);
          Translate(Sqlen, '@Hcode', '');
          Base10.Socket.RunSQL(Sqlen);
          Base10.Socket.busyloop;
          if Base10.Socket.Body_Data <> 'NODATA' then begin
            Base10.Socket.MakeData;
            Tong20.PrinZing(Self);
            if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
          end else begin
          //--//
          Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G5_Ggeo '+
                   'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
          Translate(Sqlen, '@Gcode', Edit104.Text);
          Translate(Sqlen, '@Hcode', Edit107.Text);
          Base10.Socket.RunSQL(Sqlen);
          Base10.Socket.busyloop;
          if Base10.Socket.Body_Data <> 'NODATA' then begin
            Base10.Socket.MakeData;
            Tong20.PrinZing(Self);
            if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
          end;
          //--//
          end;

          Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Gname,Gjeja,Gdang,Scode From G4_Book '+
                   'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
          Translate(Sqlen, '@Gcode', nSqry.FieldByName('Bcode').AsString);
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          Base10.Socket.RunSQL(Sqlen);
          Base10.Socket.busyloop;
          if Base10.Socket.Body_Data <> 'NODATA' then begin
            Base10.Socket.MakeData;
            Tong20.PrinZing(Self);
            if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
            nSqry.FieldByName('Bname').Value:=Base10.Socket.GetData(1, 7);
            nSqry.FieldByName('Gjeja').Value:=Base10.Socket.GetData(1, 8);
            nSqry.FieldByName('Gdang').Value:=StrToIntDef(Base10.Socket.GetData(1, 9),0);
            nSqry.FieldByName('Jeago').AsFloat:=
            Tong20.PrinJing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,Edit107.Text,0);
          { if Base10.Socket.GetData(1,10)='' Then
            nSqry.FieldByName('Ocode').Value:='A'  else
            nSqry.FieldByName('Ocode').Value:=Base10.Socket.GetData(1,10); }
          end;

          Sqlen := 'Select Grat1,Gssum From G6_Ggeo '+
                   'Where '+D_Select+'Gcode=''@Gcode'' and Bcode=''@Bcode'' and Hcode=''@Hcode''';
          Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
          Translate(Sqlen, '@Bcode', nSqry.FieldByName('Bcode').AsString);
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
          Base10.Socket.RunSQL(Sqlen);
          Base10.Socket.busyloop;
          if Base10.Socket.Body_Data <> 'NODATA' then begin
            Base10.Socket.MakeData;
            nSqry.FieldByName('Grat1').Value:=StrToIntDef(Base10.Socket.GetData(1, 1),0);
            nSqry.FieldByName('Gdang').Value:=StrToIntDef(Base10.Socket.GetData(1, 2),0);
          end;

          Tong20.PrinYing(Self);
          nSqry.Post;
        end;
      end;
    end;
    nSqry.Last; DBGrid101.SetFocus;
  end;
end;

procedure TSobo91.Button301Click(Sender: TObject);
begin
  if Edit203.Visible=True then begin

    Edit203.Text:='';
    Edit204.Text:='';
    Edit205.Text:='';
    Edit206.Text:='';
    Edit207.Text:='';
    Edit208.Text:='';

    Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where '+D_Select+
             'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
             'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
             'Scode=''@Scode'' and Gjisa=''@Gjisa'' and '+
             'Hcode=''@Hcode'' and '+
             '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';
    Translate(Sqlen, '@Gdate', Edit101.Text);
    Translate(Sqlen, '@Gubun', Edit102.Text);
    Translate(Sqlen, '@Jubun', Edit103.Text);
    Translate(Sqlen, '@Gcode', Edit104.Text);
    Translate(Sqlen, '@Scode', 'Z');
    Translate(Sqlen, '@Gjisa', Edit106.Text);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Translate(Sqlen, '@Ocode', 'B');
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      Edit203.Text:=Base10.Socket.GetData(1, 1);
      Edit204.Text:=Base10.Socket.GetData(1, 2);
      Edit205.Text:=Base10.Socket.GetData(1, 3);
      Edit206.Text:=Base10.Socket.GetData(1, 4);
      Edit207.Text:=Base10.Socket.GetData(1, 5);
      Edit208.Text:=Base10.Socket.GetData(1, 6);
    end;

    Edit205Exit(Self);
  end;
end;

procedure TSobo91.Button401Click(Sender: TObject);
begin
  Panel401.Visible:=True;
  if Assigned(Frame) then
     FreeAndNil(Frame);
  FTong07 := TTong70.Create(Self);
  Frame := FTong07;
  Frame.Parent := Panel401;
  FTong07.Edit101.SetFocus;
  FTong07.FormShow(Self);
end;

procedure TSobo91.Button501Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6: String;
begin
{ Base10.OpenShow(tSqry);

  St1:='Gdate'+' ='+#39+Edit101.Text+#39+' and '+
       'Jubun'+' ='+#39+Edit103.Text+#39+' and '+
       'Gcode'+' ='+#39+Edit104.Text+#39+' and '+
       'Gjisa'+' ='+#39+Edit106.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Scode'+' ='+#39+'Z'+#39;

  St2:=' Group By Gcode,Gjisa';

  Sqlen := 'Select Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Gcode', Edit107.Text);
  St6:=Base10.Seek_Name(Sqlen);

  T02:=0;
  T03:=0;
  T04:=0;
  T05:=0;

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 2,List1],0);
    St3:=SGrid.Cells[ 0,List1];

    Sqlen := 'Select Gname From T1_Gbun Where '+D_Select+
             'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa''';
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Gjisa', SGrid.Cells[ 1,List1]);
    St4:=Base10.Seek_Name(Sqlen);

    if St4='' then
    if SGrid.Cells[ 1,List1]<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname''';
      Translate(Sqlen, '@Hcode', '');
      Translate(Sqlen, '@Scode', 'X');
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gname', SGrid.Cells[ 1,List1]);
      St4:=Base10.Seek_Name(Sqlen);
    end;

    if St4='' then begin
      Sqlen := 'Select Gubun From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', '');
      if Base10.Seek_Name(Sqlen)='01' then
      St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then
      St4:='지방';
    end;

    Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', '');
    St5:=Base10.Seek_Name(Sqlen);

    if St5='' then begin
    Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
    St5:=Base10.Seek_Name(Sqlen);
    end;

    if SGrid.Cells[ 1,List1]<>'' then
    St5:=SGrid.Cells[ 1,List1]+')'+St5;

    if St4='시내' then begin
      T03:=T03+1;
      St1:=FloatToStr(T03);
    end else begin
      T02:=T02+1;
      St1:=FloatToStr(T02);
    end;

    if tSqry.Locate('Gdate',St1,[loCaseInsensitive])=False then begin
      tSqry.Append;
      tSqry.FieldByName('Gdate').AsString:=St1;
      tSqry.FieldByName('Name1').AsString:=St6;
      tSqry.FieldByName('Name2').AsString:=Edit101.Text;
    end;

    tSqry.Edit;
    if St4='시내' then begin
      Sqlen :=
      'Select Gqut1,Gqut2 From T4_Ssub Where '+D_Select+
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
      'Select Gqut1,Gqut2 From T4_Ssub Where '+D_Select+
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
  Tong40.Print_21_02(Self); }
end;

procedure TSobo91.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit103.Focused=True)and(Edit103.SelStart=02)and(Length(Trim(Edit103.Text))=02))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit104.Focused=True)and(Edit104.SelStart=05)and(Length(Trim(Edit104.Text))=05))or
    ((Edit105.Focused=True)and(Edit105.SelStart=50)and(Length(Trim(Edit105.Text))=50))or
    ((Edit107.Focused=True)and(Edit107.SelStart=05)and(Length(Trim(Edit107.Text))=05))or
    ((Edit108.Focused=True)and(Edit108.SelStart=50)and(Length(Trim(Edit108.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo91.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo91.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo91.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo91.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo91.Edit112KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    DGrid: TDBGridEh;
    Edits: TFlatComboBox;
begin
  Hands:=Edit102.Handle;
  DGrid:=DBGrid101;
  Edits:=Edit102;
  if Key=#13 Then begin
    if Edits.DropDownCount=9 Then Edits.DropDownCount:=8 else
    if Edits.DropDownCount=8 Then Edits.DropDownCount:=9;
    if Edits.DropDownCount=9 Then begin
      if (Edits.Text='출고')or(Edits.Text='입고') Then begin
        DGrid.Columns.Items[0].PickList.Clear;
        DGrid.Columns.Items[0].PickList.Add('위탁');
        DGrid.Columns.Items[0].PickList.Add('현매');
        DGrid.Columns.Items[0].PickList.Add('매절');
        DGrid.Columns.Items[0].PickList.Add('증정');
        DGrid.Columns.Items[0].PickList.Add('납품');
        DGrid.Columns.Items[0].PickList.Add('특별');
        DGrid.Columns.Items[0].PickList.Add('기타');
        DGrid.Columns.Items[0].PickList.Add('신간');
      end else
      if Edits.Text='반품' Then begin
        DGrid.Columns.Items[0].PickList.Clear;
        DGrid.Columns.Items[0].PickList.Add('정품');
        DGrid.Columns.Items[0].PickList.Add('비품');
        DGrid.Columns.Items[0].PickList.Add('폐기');
      end;
      Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
    end else
    if Edits.DropDownCount=8 Then begin
      Key:=#0; SendMessage(Hands, cb_ShowDropDown, 1, 0);
    end;
  end;
end;

procedure TSobo91.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit102;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo91.Edit113KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    Edits: TFlatComboBox;
begin
  Hands:=Edit106.Handle;
  Edits:=Edit106;
  if Key=#13 Then begin
    if Edits.DropDownCount=9 Then Edits.DropDownCount:=8 else
    if Edits.DropDownCount=8 Then Edits.DropDownCount:=9;
    if Edits.DropDownCount=9 Then begin
      Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
      Button101Click(Self);
    end else
    if Edits.DropDownCount=8 Then begin
      Key:=#0; SendMessage(Hands, cb_ShowDropDown, 1, 0);
    end;
  end;
end;

procedure TSobo91.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit106;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo91.Edit114KeyPress(Sender: TObject; var Key: Char);
var Str,St1: String;
begin
  if Key=#13 Then begin
  if Edit107.Focused=True Then begin
       Edit108.Text:='';
    if Edit107.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit107.Text;
    Seak80.FilterTing(Edit107.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Edit104.SetFocus;
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Edit104.SetFocus;
    end;
    end;
  end else
  if(Edit104.Focused=True)or(Edit105.Focused=True)Then begin
    if Edit104.Focused=True Then begin
      Seek50.Edit1.Text:=Edit104.Text;
      Seek50.FilterTing(Edit104.Text,Edit107.Text);
      if Seek50.Query1.IsEmpty=True Then Exit;
    end;
    if Edit105.Focused=True Then begin
      Seek50.Edit1.Text:=Edit105.Text;
      Seek50.FilterTing(Edit105.Text,Edit107.Text);
      if Seek50.Query1.IsEmpty=True Then Exit;
    end;
    if Seek50.Query1.RecordCount=1 Then begin
      Edit104.Text:=Seek50.Query1Gcode.AsString;
      Edit105.Text:=Seek50.Query1Gname.AsString;
      Edit202.Text:=Seek50.Query1Gtel1.AsString+'-'+Seek50.Query1Gtel2.AsString;
    //Edit204.Text:=Seek50.Query1Gadd1.AsString+' '+Seek50.Query1Gadd2.AsString;

      Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+D_Select+
               'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
               'Gubun=''@Gubun'' and Jubun=''@Jubun'' and '+
               'Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and '+
               'Ocode=''@Ocode'' and Scode=''@Scode''';
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Translate(Sqlen, '@Gdate', Edit101.Text);
      Translate(Sqlen, '@Gubun', Edit102.Text);
      Translate(Sqlen, '@Jubun', Edit103.Text);
      Translate(Sqlen, '@Gcode', Edit104.Text);
      Translate(Sqlen, '@Gjisa', Edit106.Text);
      Translate(Sqlen, '@Ocode', 'B');
      Translate(Sqlen, '@Scode', 'Z');
      Str:=Base10.Seek_Name(Sqlen);

      if Str<>'' then begin
        Edit201.Text:=Edit104.Text+'-'+Copy(Edit101.Text,6,2)+Copy(Edit101.Text,9,2)+'-'+IntToStr(StrToIntDef(Str,0));
      end else begin
        Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+D_Select+
                 'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
                 'Gubun=''@Gubun''';

        Translate(Sqlen, '@Hcode', Edit107.Text);
        Translate(Sqlen, '@Gdate', Edit101.Text);
        Translate(Sqlen, '@Gubun', Edit102.Text);
        Str:=Base10.Seek_Name(Sqlen);

        Edit201.Text:=Edit104.Text+'-'+Copy(Edit101.Text,6,2)+Copy(Edit101.Text,9,2)+'-'+IntToStr(StrToIntDef(Str,0)+1);
      end;

      if Copy(Edit104.Text,1,1)='9' then
      St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
           'Hcode'+'='+#39+Edit107.Text+#39+' and '+
           'Scode'+'='+#39+'Z'+#39 else
      St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
           'Hcode'+'='+#39+''+#39+' and '+
           'Scode'+'='+#39+'Z'+#39;
      Edit106.Items.Clear;
      Sqlen := 'Select Gname,Jubun From H2_Gbun Where '+D_Select+St1+' Order By Oname,Gname';
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Label100.Visible:=True;
        Edit106.Visible:=True;
        List1:=0;
        T00:=Base10.Socket.ClientData('1');
        while List1 < T00-1 do begin
          List1:=List1+1;
          if Base10.Socket.GetData(List1, 2)='' then
          Edit106.Items.Add(Base10.Socket.GetData(List1, 1))
          else
          Edit106.Items.Add(Base10.Socket.GetData(List1, 2)+'|'+Base10.Socket.GetData(List1, 1))
        end;
        Edit106.SetFocus;
      end
      else begin
        Label100.Visible:=False;
        Edit106.Visible:=False;
        Button101Click(Self);
      end;

    end else
    if Seek50.ShowModal=mrOK Then begin
      Edit104.Text:=Seek50.Query1Gcode.AsString;
      Edit105.Text:=Seek50.Query1Gname.AsString;
      Edit202.Text:=Seek50.Query1Gtel1.AsString+'-'+Seek50.Query1Gtel2.AsString;
    //Edit204.Text:=Seek50.Query1Gadd1.AsString+' '+Seek50.Query1Gadd2.AsString;

      Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+D_Select+
               'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
               'Gubun=''@Gubun'' and Jubun=''@Jubun'' and '+
               'Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and '+
               'Ocode=''@Ocode'' and Scode=''@Scode''';
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Translate(Sqlen, '@Gdate', Edit101.Text);
      Translate(Sqlen, '@Gubun', Edit102.Text);
      Translate(Sqlen, '@Jubun', Edit103.Text);
      Translate(Sqlen, '@Gcode', Edit104.Text);
      Translate(Sqlen, '@Gjisa', Edit106.Text);
      Translate(Sqlen, '@Ocode', 'B');
      Translate(Sqlen, '@Scode', 'Z');
      Str:=Base10.Seek_Name(Sqlen);

      if Str<>'' then begin
        Edit201.Text:=Edit104.Text+'-'+Copy(Edit101.Text,6,2)+Copy(Edit101.Text,9,2)+'-'+IntToStr(StrToIntDef(Str,0));
      end else begin
        Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+D_Select+
                 'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
                 'Gubun=''@Gubun''';

        Translate(Sqlen, '@Hcode', Edit107.Text);
        Translate(Sqlen, '@Gdate', Edit101.Text);
        Translate(Sqlen, '@Gubun', Edit102.Text);
        Str:=Base10.Seek_Name(Sqlen);

        Edit201.Text:=Edit104.Text+'-'+Copy(Edit101.Text,6,2)+Copy(Edit101.Text,9,2)+'-'+IntToStr(StrToIntDef(Str,0)+1);
      end;

      if Copy(Edit104.Text,1,1)='9' then
      St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
           'Hcode'+'='+#39+Edit107.Text+#39+' and '+
           'Scode'+'='+#39+'Z'+#39 else
      St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
           'Hcode'+'='+#39+''+#39+' and '+
           'Scode'+'='+#39+'Z'+#39;
      Edit106.Items.Clear;
      Sqlen := 'Select Gname,Jubun From H2_Gbun Where '+D_Select+St1+' Order By Oname,Gname';
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Label100.Visible:=True;
        Edit106.Visible:=True;
        List1:=0;
        T00:=Base10.Socket.ClientData('1');
        while List1 < T00-1 do begin
          List1:=List1+1;
          if Base10.Socket.GetData(List1, 2)='' then
          Edit106.Items.Add(Base10.Socket.GetData(List1, 1))
          else
          Edit106.Items.Add(Base10.Socket.GetData(List1, 2)+'|'+Base10.Socket.GetData(List1, 1))
        end;
        Edit106.SetFocus;
      end
      else begin
        Label100.Visible:=False;
        Edit106.Visible:=False;
        Button101Click(Self);
      end;

    end;
  end;
  end;
end;

procedure TSobo91.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo91.DBGrid101Exit(Sender: TObject);
begin
  Base10.T2_Sub11BeforeClose(Base10.T2_Sub11);
end;

procedure TSobo91.DBGrid101Enter(Sender: TObject);
var DGrid: TDBGridEh;
begin
  DGrid:=DBGrid101;
  if Edit102.Text='출고' Then begin
    DGrid.Columns.Items[0].PickList.Clear;
    DGrid.Columns.Items[0].PickList.Add('위탁');
    DGrid.Columns.Items[0].PickList.Add('현매');
    DGrid.Columns.Items[0].PickList.Add('매절');
    DGrid.Columns.Items[0].PickList.Add('납품');
    DGrid.Columns.Items[0].PickList.Add('증정');
    DGrid.Columns.Items[0].PickList.Add('특별');
    DGrid.Columns.Items[0].PickList.Add('기타');
    DGrid.Columns.Items[0].PickList.Add('신간');
    DGrid.Columns.Items[0].PickList.Add(' 질 ');
  end else begin
    DGrid.Columns.Items[0].PickList.Clear;
    DGrid.Columns.Items[0].PickList.Add('정품');
    DGrid.Columns.Items[0].PickList.Add('비품');
    DGrid.Columns.Items[0].PickList.Add('폐기');
  end;
  DGrid.SelectedIndex:=0;
  if nSqry.Active=True Then begin
  if(nSqry.FieldByName('Gdate').AsString<>Edit101.Text)or
    (nSqry.FieldByName('Gubun').AsString<>Edit102.Text)or
    (nSqry.FieldByName('Jubun').AsString<>Edit103.Text)or
    (nSqry.FieldByName('Gcode').AsString<>Edit104.Text)or
    (nSqry.FieldByName('Gjisa').AsString<>Edit106.Text)or
    (nSqry.FieldByName('Hcode').AsString<>Edit107.Text)Then
     Button101Click(Self);
  end;
  T2_Sub11AfterScroll(T2_Sub11);
end;

procedure TSobo91.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=0 Then begin

      Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G5_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', Edit104.Text);
      Translate(Sqlen, '@Hcode', '');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        Tong20.PrinZing(Self);
        if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
        Tong20.PrinYing(Self);
      end else begin
      //--//
      Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G5_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', Edit104.Text);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        Tong20.PrinZing(Self);
        if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
        Tong20.PrinYing(Self);
      end;
      //--//
      end;

      Tong20.PrinRat1(Edit107.Text,Edit104.Text,'');

    end else
    if SIndexs=1 Then begin
         nSqry.FieldByName('Gname').AsString:=Edit105.Text;
      if nSqry.FieldByName('Bcode').AsString='' Then Exit;
      Seek40.Edit1.Text:=nSqry.FieldByName('Bcode').AsString;
      Seek40.FilterTing(nSqry.FieldByName('Bcode').AsString,Edit107.Text);
      if Seek40.Query1.RecordCount=1 Then begin
        Code1:=Seek40.Query1Gbjil.AsString;
      //nSqry.FieldByName('Ocode').Value:=Seek40.Query1Scode.Value;
        nSqry.FieldByName('Bcode').Value:=Seek40.Query1Gcode.Value;
        nSqry.FieldByName('Bname').Value:=Seek40.Query1Gname.Value;
        nSqry.FieldByName('Gjeja').Value:=Seek40.Query1Gjeja.Value;
        nSqry.FieldByName('Gdang').Value:=Seek40.Query1Gdang.Value;
        nSqry.FieldByName('Jeago').AsFloat:=
        Tong20.PrinJing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,Edit107.Text,0);
        SIndexs:=SIndexs+1;
      end else
      if Seek40.ShowModal=mrOK Then begin
        Code1:=Seek40.Query1Gbjil.AsString;
      //nSqry.FieldByName('Ocode').Value:=Seek40.Query1Scode.Value;
        nSqry.FieldByName('Bcode').Value:=Seek40.Query1Gcode.Value;
        nSqry.FieldByName('Bname').Value:=Seek40.Query1Gname.Value;
        nSqry.FieldByName('Gjeja').Value:=Seek40.Query1Gjeja.Value;
        nSqry.FieldByName('Gdang').Value:=Seek40.Query1Gdang.Value;
        nSqry.FieldByName('Jeago').AsFloat:=
        Tong20.PrinJing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,Edit107.Text,0);
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;
      if nSqry.FieldByName('Ocode').AsString='' Then
         nSqry.FieldByName('Ocode').AsString:='B';

      Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G4_Book '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Bcode').AsString);
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        Tong20.PrinZing(Self);
        if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
      end;

      Sqlen := 'Select Grat1,Gssum From G6_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Bcode=''@Bcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Bcode', nSqry.FieldByName('Bcode').AsString);
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        nSqry.FieldByName('Grat1').Value:=StrToIntDef(Base10.Socket.GetData(1, 1),0);
        nSqry.FieldByName('Gdang').Value:=StrToIntDef(Base10.Socket.GetData(1, 2),0);
      end;

      Tong20.PrinRat1(Edit107.Text,Edit104.Text,nSqry.FieldByName('Bcode').AsString);

      Tong20.PrinYing(Self);
    end else
    if SIndexs=3 Then begin
      Tong20.PrinYing(Self);
    //Tong20.PrinSing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,Edit107.Text,nSqry.FieldByName('Gsqut').Value);
      SIndexs:=SIndexs+1;
    end else
    if SIndexs=5 Then begin
      Tong20.PrinYing(Self);
      SIndexs:=SIndexs+1;
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end;
end;

procedure TSobo91.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    if SIndexs=0 Then begin
      DBGrid101.Columns.Items[SIndexs].Grid.EditorMode:=False;
      Keybd_event(VK_MENU,MapVirtualKey(VK_MENU,0),0,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),0,0);
      Keybd_event(VK_MENU,MapVirtualKey(VK_MENU,0),KEYEVENTF_KEYUP,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),KEYEVENTF_KEYUP,0);
    end else
    if SIndexs=7 Then begin
      if nSqry.FieldByName('Pubun').Value=' 질' Then begin
      Gdang:=nSqry.FieldByName('Gdang').Value;
      Seek40.Edit1.Text:=Code1;
      Seek40.FilterJing(Code1,Edit107.Text);
      Seek40.Edit2.Value:=nSqry.FieldByName('Gsqut').Value;
      if Code1='' Then begin
      if nSqry.FieldByName('Gubun').Value='반품' Then
        nSqry.FieldByName('Pubun').Value:='비품' else
        nSqry.FieldByName('Pubun').Value:='위탁'; end;
      While(Seek40.Query1.EOF=False)and(Code1<>'')do begin
      if nSqry.FieldByName('Gubun').Value='반품' Then
        nSqry.FieldByName('Pubun').Value:='비품' else
        nSqry.FieldByName('Pubun').Value:='위탁';
        nSqry.FieldByName('Gcode').Value:=Edit104.Text;
      { if Seek40.Query1Scode.AsString='' Then
        nSqry.FieldByName('Ocode').Value:='A'   else
        nSqry.FieldByName('Ocode').Value:=Seek40.Query1Scode.AsString; }
        nSqry.FieldByName('Bcode').Value:=Seek40.Query1Gcode.AsString;
        nSqry.FieldByName('Bname').Value:=Seek40.Query1Gname.AsString;
        nSqry.FieldByName('Gjeja').Value:=Seek40.Query1Gjeja.AsString;
        nSqry.FieldByName('Gdang').Value:=Seek40.Query1Gdang.AsFloat;
        nSqry.FieldByName('Gsqut').Value:=Seek40.Edit2.Value;
        nSqry.FieldByName('Jeago').AsFloat:=
        Tong20.PrinJing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,Edit107.Text,0);
        Pubun:=nSqry.FieldByName('Pubun').AsString;
        Gcode:=nSqry.FieldByName('Gcode').AsString;
        Ocode:=nSqry.FieldByName('Ocode').AsString;
        Bcode:=nSqry.FieldByName('Bcode').AsString;

        Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G5_Ggeo '+
                 'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
        Translate(Sqlen, '@Gcode', Edit104.Text);
        Translate(Sqlen, '@Hcode', '');
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.busyloop;
        if Base10.Socket.Body_Data <> 'NODATA' then begin
          Base10.Socket.MakeData;
          Tong20.PrinZing(Self);
          if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
        end else begin
        //--//
        Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G5_Ggeo '+
                 'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
        Translate(Sqlen, '@Gcode', Edit104.Text);
        Translate(Sqlen, '@Hcode', Edit107.Text);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.busyloop;
        if Base10.Socket.Body_Data <> 'NODATA' then begin
          Base10.Socket.MakeData;
          Tong20.PrinZing(Self);
          if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
        end;
        //--//
        end;

        Tong20.PrinRat1(Edit107.Text,Edit104.Text,'');

        Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G4_Book '+
                 'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
        Translate(Sqlen, '@Gcode', nSqry.FieldByName('Bcode').AsString);
        Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.busyloop;
        if Base10.Socket.Body_Data <> 'NODATA' then begin
          Base10.Socket.MakeData;
          Tong20.PrinZing(Self);
          if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
        end;

        Tong20.PrinRat1(Edit107.Text,Edit104.Text,nSqry.FieldByName('Bcode').AsString);

        Tong20.PrinYing(Self);
        nSqry.Append; DBGrid101.SelectedIndex:=0;
        Seek40.Query1.Next;
      end;
      DBGrid101.SelectedIndex:=0;
      end else
      nSqry.Append; DBGrid101.SelectedIndex:=0;
    end;
  end;
  if Key=VK_F2 Then Button016Click(Self);
  if Key=VK_F3 Then Button017Click(Self);
  if Key=VK_F5 Then Button007Click(Self);
  if Key=VK_F7 Then Seak70.ShowModal;
  if Key=VK_F9 Then Button201Click(Self);
  if sColumn=False Then begin
    if nSqry.IsEmpty=False Then
    if Key=VK_DELETE Then T2_Sub11AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo91.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo91.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo91.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo91.DBGrid201TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(mSqry,Column);
end;

procedure TSobo91.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo91.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo91.Edit301KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  Button801Click(Self);
end;

procedure TSobo91.Button801Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin

    Sqlen := 'Select Gbigo From S1_Memo Where '+D_Select+
             'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
             'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
             'Scode=''@Scode'' and Gjisa=''@Gjisa'' and '+
             'Hcode=''@Hcode'' and '+
             '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';
    Translate(Sqlen, '@Gdate', Edit101.Text);
    Translate(Sqlen, '@Gubun', Edit102.Text);
    Translate(Sqlen, '@Jubun', Edit103.Text);
    Translate(Sqlen, '@Gcode', Edit104.Text);
    Translate(Sqlen, '@Scode', 'Z');
    Translate(Sqlen, '@Gjisa', Edit106.Text);
    Translate(Sqlen, '@Hcode', Edit107.Text);
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
      '  and  Scode=''@Scode'' and Gjisa=''@Gjisa'' '+
      '  and  Hcode=''@Hcode'' and '+
      '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';

      Translate(Sqlen, '@Gdate', Edit101.Text);
      Translate(Sqlen, '@Gubun', Edit102.Text);
      Translate(Sqlen, '@Jubun', Edit103.Text);
      Translate(Sqlen, '@Gcode', Edit104.Text);
      Translate(Sqlen, '@Scode', 'Z');
      Translate(Sqlen, '@Gjisa', Edit106.Text);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Translate(Sqlen, '@Ocode', 'B');
      Translate(Sqlon, '@Gbigo', Edit203.Text);
      Translate(Sqlon, '@Sbigo', Edit204.Text);

      if StaticText1.Visible=True then
      Translate(Sqlon, '@Gtel1', '') else
      Translate(Sqlon, '@Gtel1', Edit205.Text);

      if StaticText2.Visible=True then
      Translate(Sqlon, '@Gtel2', '') else
      Translate(Sqlon, '@Gtel2', Edit206.Text);

      if StaticText3.Visible=True then
      Translate(Sqlon, '@Gname', '') else
      Translate(Sqlon, '@Gname', Edit207.Text);

      if StaticText4.Visible=True then
      Translate(Sqlon, '@Gpost', '') else
      Translate(Sqlon, '@Gpost', Edit208.Text);

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

      Translate(Sqlen, '@Gdate', Edit101.Text);
      Translate(Sqlen, '@Gubun', Edit102.Text);
      Translate(Sqlen, '@Jubun', Edit103.Text);
      Translate(Sqlen, '@Gcode', Edit104.Text);
      Translate(Sqlen, '@Scode', 'Z');
      Translate(Sqlen, '@Gjisa', Edit106.Text);
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Translate(Sqlen, '@Ocode', 'B');
      Translate(Sqlen, '@Gbigo', Edit203.Text);
      Translate(Sqlen, '@Sbigo', Edit204.Text);

      if StaticText1.Visible=True then
      Translate(Sqlen, '@Gtel1', '') else
      Translate(Sqlen, '@Gtel1', Edit205.Text);

      if StaticText2.Visible=True then
      Translate(Sqlen, '@Gtel2', '') else
      Translate(Sqlen, '@Gtel2', Edit206.Text);

      if StaticText3.Visible=True then
      Translate(Sqlen, '@Gname', '') else
      Translate(Sqlen, '@Gname', Edit207.Text);

      if StaticText4.Visible=True then
      Translate(Sqlen, '@Gpost', '') else
      Translate(Sqlen, '@Gpost', Edit208.Text);

      Base10.Socket.RunSQL(Sqlon+Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end;
    DBGrid101.SetFocus;
  end;
end;

procedure TSobo91.Button802Click(Sender: TObject);
var St1: String;
begin
  if nSqry.Active=True Then begin
  Sqlen := 'Select Gname,Gadd1,Gadd2,Gtel1,Gtel2,Gposa From G5_Ggeo Where '+D_Select+
           'Hcode=''@Hcode'' and Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Hcode', Edit107.Text);
  Translate(Sqlen, '@Gcode', Edit104.Text);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    St1:=Base10.Socket.GetData(1, 1);
    Translate(St1, '-택배', '');
    Translate(St1, '/택배', '');
    Translate(St1, '택배', '');
    if (Edit203.Text='')and(Base10.Socket.GetData(1, 2)<>'') then
    Edit203.Text:=Base10.Socket.GetData(1, 2);
    if (Edit204.Text='')and(Base10.Socket.GetData(1, 3)<>'') then
    Edit204.Text:=Base10.Socket.GetData(1, 3);
    if (Edit206.Text='')and(Base10.Socket.GetData(1, 5)<>'') then
    Edit206.Text:=Base10.Socket.GetData(1, 4)+'-'+Base10.Socket.GetData(1, 5);
    if (Edit207.Text='')and(Base10.Socket.GetData(1, 1)<>'') then
    Edit207.Text:=St1;
    Edit205Exit(Self);
  end else begin

  Sqlen := 'Select Gname,Gadd1,Gadd2,Gtel1,Gtel2,Gposa From G5_Ggeo Where '+D_Select+
           'Hcode=''@Hcode'' and Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Hcode', '');
  Translate(Sqlen, '@Gcode', Edit104.Text);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    St1:=Base10.Socket.GetData(1, 1);
    Translate(St1, '-택배', '');
    Translate(St1, '/택배', '');
    Translate(St1, '택배', '');
    if (Edit203.Text='')and(Base10.Socket.GetData(1, 2)<>'') then
    Edit203.Text:=Base10.Socket.GetData(1, 2);
    if (Edit204.Text='')and(Base10.Socket.GetData(1, 3)<>'') then
    Edit204.Text:=Base10.Socket.GetData(1, 3);
    if (Edit206.Text='')and(Base10.Socket.GetData(1, 5)<>'') then
    Edit206.Text:=Base10.Socket.GetData(1, 4)+'-'+Base10.Socket.GetData(1, 5);
    if (Edit207.Text='')and(Base10.Socket.GetData(1, 1)<>'') then
    Edit207.Text:=St1;
    Edit205Exit(Self);
  end;

  end;
  end;
end;

procedure TSobo91.Button803Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
  Cpost:='91';
  Subu00.Post_Show(Self);
  end;
end;

procedure TSobo91.Edit205Click(Sender: TObject);
begin
  if Edit205.Focused=True then
  StaticText1.Visible:=False;
  if Edit206.Focused=True then
  StaticText2.Visible:=False;
  if Edit207.Focused=True then
  StaticText3.Visible:=False;
  if Edit208.Focused=True then
  StaticText4.Visible:=False;
end;

procedure TSobo91.Edit205Exit(Sender: TObject);
begin
  StaticText1.Visible:=False;
  StaticText2.Visible:=False;
  StaticText3.Visible:=False;
  StaticText4.Visible:=False;
  if Edit205.Text='' then
  StaticText1.Visible:=True;
  if Edit206.Text='' then
  StaticText2.Visible:=True;
  if Edit207.Text='' then
  StaticText3.Visible:=True;
  if Edit208.Text='' then
  StaticText4.Visible:=True;
end;

procedure TSobo91.StaticText1Click(Sender: TObject);
begin
  StaticText1.Visible:=False;
  Edit205.SetFocus;
end;

procedure TSobo91.StaticText2Click(Sender: TObject);
begin
  StaticText2.Visible:=False;
  Edit206.SetFocus;
end;

procedure TSobo91.StaticText3Click(Sender: TObject);
begin
  StaticText3.Visible:=False;
  Edit207.SetFocus;
end;

procedure TSobo91.StaticText4Click(Sender: TObject);
begin
  StaticText4.Visible:=False;
  Edit208.SetFocus;
end;

procedure TSobo91.T2_Sub11GSQUTChange(Sender: TField);
begin
  if nSqry.FieldByName('Gubun').AsString = '출고' then
  if nSqry.FieldByName('Gsqut').AsFloat > 0 then begin
    if nSqry.FieldByName('Gsqut').AsFloat > nSqry.FieldByName('Jeago').AsFloat then begin
       ShowMessage('재고가 부족합니다. 확인하여 주세요.');
    end;
  end;
end;

procedure TSobo91.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo91.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo91.Button701Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit108.Text;
  if Edit108.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit108.Text);
  if Seak80.ShowModal=mrOK Then begin
    Edit107.Text:=Seak80.Query1Gcode.AsString;
    Edit108.Text:=Seak80.Query1Gname.AsString;
    Edit104.SetFocus;
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit107.Text:=Seak80.Query1Gcode.AsString;
    Edit108.Text:=Seak80.Query1Gname.AsString;
    Edit104.SetFocus;
  end;
end;

procedure TSobo91.Button702Click(Sender: TObject);
var Str,St1: String;
begin
  Seek50.Edit1.Text:=Edit105.Text;
  if Edit105.Text='' then
  Seek50.FilterTing('',Edit107.Text) else
  Seek50.FilterTing(Edit105.Text,Edit107.Text);
  if Seek50.ShowModal=mrOK Then begin
      Edit104.Text:=Seek50.Query1Gcode.AsString;
      Edit105.Text:=Seek50.Query1Gname.AsString;
      Edit202.Text:=Seek50.Query1Gtel1.AsString+'-'+Seek50.Query1Gtel2.AsString;
    //Edit204.Text:=Seek50.Query1Gadd1.AsString+' '+Seek50.Query1Gadd2.AsString;

      Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+D_Select+
               'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
               'Gubun=''@Gubun'' and Jubun=''@Jubun'' and '+
               'Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and '+
               'Ocode=''@Ocode'' and Scode=''@Scode''';
      Translate(Sqlen, '@Hcode', Edit107.Text);
      Translate(Sqlen, '@Gdate', Edit101.Text);
      Translate(Sqlen, '@Gubun', Edit102.Text);
      Translate(Sqlen, '@Jubun', Edit103.Text);
      Translate(Sqlen, '@Gcode', Edit104.Text);
      Translate(Sqlen, '@Gjisa', Edit106.Text);
      Translate(Sqlen, '@Ocode', 'B');
      Translate(Sqlen, '@Scode', 'Z');
      Str:=Base10.Seek_Name(Sqlen);

      if Str<>'' then begin
        Edit201.Text:=Edit104.Text+'-'+Copy(Edit101.Text,6,2)+Copy(Edit101.Text,9,2)+'-'+IntToStr(StrToIntDef(Str,0));
      end else begin
        Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+D_Select+
                 'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
                 'Gubun=''@Gubun''';

        Translate(Sqlen, '@Hcode', Edit107.Text);
        Translate(Sqlen, '@Gdate', Edit101.Text);
        Translate(Sqlen, '@Gubun', Edit102.Text);
        Str:=Base10.Seek_Name(Sqlen);

        Edit201.Text:=Edit104.Text+'-'+Copy(Edit101.Text,6,2)+Copy(Edit101.Text,9,2)+'-'+IntToStr(StrToIntDef(Str,0)+1);
      end;

      if Copy(Edit104.Text,1,1)='9' then
      St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
           'Hcode'+'='+#39+Edit107.Text+#39+' and '+
           'Scode'+'='+#39+'Z'+#39 else
      St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
           'Hcode'+'='+#39+''+#39+' and '+
           'Scode'+'='+#39+'Z'+#39;
      Edit106.Items.Clear;
      Sqlen := 'Select Gname,Jubun From H2_Gbun Where '+D_Select+St1+' Order By Oname,Gname';
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Label100.Visible:=True;
        Edit106.Visible:=True;
        List1:=0;
        T00:=Base10.Socket.ClientData('1');
        while List1 < T00-1 do begin
          List1:=List1+1;
          if Base10.Socket.GetData(List1, 2)='' then
          Edit106.Items.Add(Base10.Socket.GetData(List1, 1))
          else
          Edit106.Items.Add(Base10.Socket.GetData(List1, 2)+'|'+Base10.Socket.GetData(List1, 1))
        end;
        Edit106.SetFocus;
      end
      else begin
        Label100.Visible:=False;
        Edit106.Visible:=False;
        Button101Click(Self);
      end;
  end;
end;

procedure TSobo91.Seek_Post(Sender: TObject);
begin
  nSqry.BeforePost:=nil;
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
      nSqry.FieldByName('Gpost').AsString:=Trim(Copy(AutoFrx(Base10.Socket.GetData(1, 1)),1,10));
      nSqry.FieldByName('Qpost').AsString:=
      nSqry.FieldByName('Gcode').AsString+
      nSqry.FieldByName('Jubun').AsString+
      nSqry.FieldByName('Gjisa').AsString+
      Trim(Copy(AutoFrx(Base10.Socket.GetData(1, 1)),1,10))+
      Format('%09s',[FormatFloat('000000000',nSqry.FieldByName('ID').AsInteger)] );
    //Format('%09s',[FormatFloat('000000000',nSqry.FieldByName('Bcode').AsInteger)] );
      nSqry.Post;
    end;

    nSqry.Next;
  end;
  nSqry.First;
  DataSource1.Enabled:=True;
  nSqry.BeforePost:=T2_Sub11BeforePost;
end;

procedure TSobo91.T2_Sub11YESNOGetText(Sender: TField; var Text: String; DisplayText: Boolean);
begin
  Text:=Base10.LockCheck1(T2_Sub11.FieldByName('Yesno').AsString);
end;

procedure TSobo91.T2_Sub11YESNOSetText(Sender: TField; const Text: String);
begin
  T2_Sub11.FieldByName('Yesno').AsString:=Base10.LockCheck2(Text);
end;

procedure TSobo91.T2_Sub11AfterCancel(DataSet: TDataSet);
begin
  T2_Sub11AfterScroll(T2_Sub11);
end;

procedure TSobo91.T2_Sub11AfterScroll(DataSet: TDataSet);
begin
  Ocode:= T2_Sub11.FieldByName('Ocode').AsString;
  Pubun:= T2_Sub11.FieldByName('Pubun').AsString;
  Gsqut:=-T2_Sub11.FieldByName('Gsqut').AsFloat;
  Gssum:=-T2_Sub11.FieldByName('Gssum').AsFloat;
end;

procedure TSobo91.T2_Sub11AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TSobo91.T2_Sub11AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub11ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      //--//
    { if(T2_Sub11Ocode.AsString='B')and(T2_Sub11Gcode.AsString='00001')then begin

        Sqlen := 'DELETE FROM Sg_Csum WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';
        Translate(Sqlen, '@Scode', 'A');
        Translate(Sqlen, '@Gbigo', T2_Sub11ID.AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.BusyLoop;
        if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      end; }

    end else begin
      Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub11ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
      Translate(Sqlen, '@Scode', '1');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      //--//
    { if(T2_Sub11Ocode.AsString='B')and(T2_Sub11Gcode.AsString='00001')then begin

        Sqlen := 'DELETE FROM Sg_Csum WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';
        Translate(Sqlen, '@Scode', 'A');
        Translate(Sqlen, '@Gbigo', T2_Sub11ID.AsString);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.BusyLoop;
        if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

      end; }

    end;

    T2_Sub11.Delete;

  end; end;

end;

procedure TSobo91.T2_Sub11BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub11.State=dsInsert)Then begin

    Sqlon := 'INSERT INTO S1_Ssub '+
    '(Gdate, Scode, Gcode, Hcode, Ocode, Bcode, '+
    ' Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang, '+
    ' Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Ocode'',''@Bcode'', '+
    ' ''@Gubun'',''@Jubun'',''@Pubun'',''@Gbigo'',  @Gsqut  ,  @Gdang  , '+
    '   @Grat1  ,  @Gssum  ,  @Qsqut  ,  @Jeago  ,''@Yesno'',''@Gjisa'', now())';

    Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
    Translate(Sqlen, '@Scode', T2_Sub11Scode.AsString);
    Translate(Sqlen, '@Gcode', T2_Sub11Gcode.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub11Hcode.AsString);
    Translate(Sqlen, '@Ocode', T2_Sub11Ocode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub11Bcode.AsString);
    Translate(Sqlen, '@Gubun', T2_Sub11Gubun.AsString);
    Translate(Sqlen, '@Jubun', T2_Sub11Jubun.AsString);
    Translate(Sqlen, '@Pubun', T2_Sub11Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub11Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub11Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub11Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub11Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub11Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub11Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub11Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub11Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub11Gjisa.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S1_SSUB_ID_GEN');
    Base10.Update_Idnum(nSqry,'S1_SSUB_ID_NUM');

    //--//
  { if(T2_Sub11Ocode.AsString='B')and(T2_Sub11Gcode.AsString='00001')then begin

      Sqlen := 'INSERT INTO Sg_Csum '+
      '(Gdate, Scode, Gcode, Hcode, Gbigo, Gbsum) VALUES '+
      '(''@Gdate'',''@Scode'',''@Gcode'',''@Hcode'',''@Gbigo'',  @Gbsum  )';

      Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
      Translate(Sqlen, '@Scode', 'A');
      Translate(Sqlen, '@Gcode', T2_Sub11Bcode.AsString);
      Translate(Sqlen, '@Hcode', T2_Sub11Hcode.AsString);
      Translate(Sqlen, '@Gbigo', T2_Sub11ID.AsString   );
      TransAuto(Sqlen, '@Gbsum', T2_Sub11Gsqut.AsString);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end; }

  end else begin

    Sqlon := 'UPDATE S1_Ssub SET '+
    'Scode=''@Scode'',Gcode=''@Gcode'',Hcode=''@Hcode'',Ocode=''@Ocode'', '+
    'Bcode=''@Bcode'',Gubun=''@Gubun'',Jubun=''@Jubun'',Pubun=''@Pubun'', ';
    Sqlen :=
    'Gbigo=''@Gbigo'',Gsqut=  @Gsqut  ,Gdang=  @Gdang  ,Grat1=  @Grat1  , '+
    'Gssum=  @Gssum  ,Qsqut=  @Qsqut  ,Jeago=  @Jeago  ,Yesno=''@Yesno'', '+
    'Gjisa=''@Gjisa'' WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
    Translate(Sqlon, '@Scode', T2_Sub11Scode.AsString);
    Translate(Sqlon, '@Gcode', T2_Sub11Gcode.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub11Hcode.AsString);
    Translate(Sqlon, '@Ocode', T2_Sub11Ocode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub11Bcode.AsString);
    Translate(Sqlon, '@Gubun', T2_Sub11Gubun.AsString);
    Translate(Sqlon, '@Jubun', T2_Sub11Jubun.AsString);
    Translate(Sqlon, '@Pubun', T2_Sub11Pubun.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub11Gbigo.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub11Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub11Gdang.AsString);
    TransAuto(Sqlen, '@Grat1', T2_Sub11Grat1.AsString);
    TransAuto(Sqlen, '@Gssum', T2_Sub11Gssum.AsString);
    Translate(Sqlen, '@Yesno', T2_Sub11Yesno.AsString);
    TransAuto(Sqlen, '@Qsqut', T2_Sub11Qsqut.AsString);
    TransAuto(Sqlen, '@Jeago', T2_Sub11Jeago.AsString);
    Translate(Sqlen, '@Gjisa', T2_Sub11Gjisa.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub11ID.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    //--//
  { if(T2_Sub11Ocode.AsString='B')and(T2_Sub11Gcode.AsString='00001')then begin

      Sqlen := 'UPDATE Sg_Csum SET '+
      'Gdate=''@Gdate'',Gcode=''@Gcode'',Hcode=''@Hcode'', '+
      'Gbsum=  @Gbsum  WHERE Scode=''@Scode'' and Gbigo=''@Gbigo'' ';

      Translate(Sqlen, '@Gdate', T2_Sub11Gdate.AsString);
      Translate(Sqlen, '@Scode', 'A');
      Translate(Sqlen, '@Gcode', T2_Sub11Bcode.AsString);
      Translate(Sqlen, '@Hcode', T2_Sub11Hcode.AsString);
      Translate(Sqlen, '@Gbigo', T2_Sub11ID.AsString   );
      TransAuto(Sqlen, '@Gbsum', T2_Sub11Gsqut.AsString);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end; }

  end;

end;

procedure TSobo91.T2_Sub11NewRecord(DataSet: TDataSet);
begin
  T2_Sub11Scode.Value:='Z';
  T2_Sub11Gdate.Value:=Edit101.Text;
  T2_Sub11Gubun.Value:=Edit102.Text;
  T2_Sub11Jubun.Value:=Edit103.Text;
  T2_Sub11Gcode.Value:=Edit104.Text;
  T2_Sub11Gjisa.Value:=Edit106.Text;
  T2_Sub11Hcode.Value:=Edit107.Text;
  T2_Sub11Ocode.Value:='B';
  T2_Sub11Yesno.Value:='1';
  T2_Sub11Pubun.Value:=Pubun;
  if Pubun='' Then begin
  if Edit102.Text='출고' Then
  T2_Sub11Pubun.Value:='위탁';
  if Edit102.Text='반품' Then
  T2_Sub11Pubun.Value:='비품'; end;
  T2_Sub11Gsqut.Value:=0; T2_Sub11Gdang.Value:=0;
  T2_Sub11Grat1.Value:=0; T2_Sub11Gssum.Value:=0;
  T2_Sub11Jeago.Value:=0;
end;

procedure TSobo91.T2_Sub11BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub11 do
  if(State in dsEditModes)Then Post;
end;

end.
