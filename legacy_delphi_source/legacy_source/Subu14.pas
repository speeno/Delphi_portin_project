unit Subu14;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, TFlatCheckBoxUnit,
  dxCore, dxButtons, CornerButton;

type
  TSobo14 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel003: TFlatPanel;
    Panel004: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    Panel100: TFlatPanel;
    Panel101: TFlatPanel;
    Panel102: TFlatPanel;
    Panel103: TFlatPanel;
    Panel105: TFlatPanel;
    Panel106: TFlatPanel;
    Panel107: TFlatPanel;
    Panel108: TFlatPanel;
    Panel109: TFlatPanel;
    Panel110: TFlatPanel;
    Panel111: TFlatPanel;
    Panel112: TFlatPanel;
    Panel113: TFlatPanel;
    Panel119: TFlatPanel;
    Panel200: TFlatPanel;
    Panel201: TFlatPanel;
    Panel202: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    DBGrid101: TDBGrid;
    DBGrid201: TDBGrid;
    Button104: TFlatButton;
    Label100: TmyLabel3d;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    Label103: TmyLabel3d;
    Label104: TmyLabel3d;
    Label105: TmyLabel3d;
    Label106: TmyLabel3d;
    Label107: TmyLabel3d;
    Label200: TmyLabel3d;
    Edit101: TFlatComboBox;
    Edit102: TFlatComboBox;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Edit106: TFlatEdit;
    Edit107: TFlatComboBox;
    Edit108: TFlatEdit;
    Edit109: TFlatNumber;
    Edit110: TFlatEdit;
    Edit111: TFlatEdit;
    Edit112: TFlatNumber;
    Edit113: TFlatNumber;
    Edit114: TFlatNumber;
    Edit115: TFlatNumber;
    Edit116: TFlatNumber;
    Edit117: TFlatNumber;
    Edit118: TFlatNumber;
    Edit119: TFlatEdit;
    Edit201: TFlatEdit;
    Edit202: TFlatEdit;
    Panel120: TFlatPanel;
    Panel121: TFlatPanel;
    Edit120: TFlatEdit;
    Panel122: TFlatPanel;
    Edit121: TFlatMaskEdit;
    Edit122: TFlatMaskEdit;
    Panel124: TFlatPanel;
    Edit124: TFlatNumber;
    Label108: TmyLabel3d;
    Edit125: TFlatNumber;
    Label109: TmyLabel3d;
    Edit123: TFlatEdit;
    Panel123: TFlatPanel;
    Label300: TmyLabel3d;
    Label301: TmyLabel3d;
    Panel129: TFlatPanel;
    CheckBox2: TFlatCheckBox;
    Edit129: TFlatEdit;
    Edit130: TFlatNumber;
    Label110: TmyLabel3d;
    CheckBox1: TFlatCheckBox;
    CornerButton2: TCornerButton;
    CornerButton3: TCornerButton;
    CornerButton4: TCornerButton;
    Label002: TmyLabel3d;
    Label003: TmyLabel3d;
    Label309: TmyLabel3d;
    Button000: TdxButton;
    Button101: TdxButton;
    Button102: TdxButton;
    Button103: TdxButton;
    Button201: TdxButton;
    Button202: TdxButton;
    Button203: TdxButton;
    procedure FormPaint(Sender: TObject);
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
    procedure Button102Click(Sender: TObject);
    procedure Button103Click(Sender: TObject);
    procedure Button104Click(Sender: TObject);
    procedure Button201Click(Sender: TObject);
    procedure Button202Click(Sender: TObject);
    procedure Button203Click(Sender: TObject);
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
    procedure Edit115KeyPress(Sender: TObject; var Key: Char);
    procedure Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
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
    procedure SeachClick(Str1,Str2: String);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo14: TSobo14;

implementation

{$R *.DFM}

uses Chul, Base01, Subu19, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo14.FormPaint(Sender: TObject);
begin
{ Button023Click(Self);
  Button024Click(Self); }
  Sobo14.OnPaint:=Nil;
  Sobo14.OnShow:=FormShow;
  FormShow(Self);
end;

procedure TSobo14.FormActivate(Sender: TObject);
begin
  nForm:='14';
  nSqry:=Base10.T1_Sub41;
  mSqry:=Base10.T1_Sub42;
end;

procedure TSobo14.FormShow(Sender: TObject);
begin
  Refresh;
  if Base10.Database.Database='chul_02_db' then begin
    Application.CreateForm(TSobo19, Sobo19);
    Sobo19.Edit000.Visible:=True;
    Sobo19.Edit101.Visible:=True;
    Sobo19.ShowModal;
    Sobo19.Edit100.ItemIndex:=Sobo19.Edit000.ItemIndex;
    Label300.Caption:=Sobo19.Edit102.Text;
    Label301.Caption:=Sobo19.Edit103.Text;
    SeachClick(Sobo19.Edit100.Text,Sobo19.Edit101.Text);
    Sobo19.Edit000.Visible:=False;
    Sobo19.Edit101.Visible:=False;
    Sobo19.Free;
    if Base10.Seek_Ggeo(Label300.Caption)='X' Then Close;
  end else begin
    Application.CreateForm(TSobo19, Sobo19);
    Sobo19.ShowModal;
    Sobo19.Edit100.ItemIndex:=Sobo19.Edit000.ItemIndex;
    Label300.Caption:=Sobo19.Edit102.Text;
    Label301.Caption:=Sobo19.Edit103.Text;
    SeachClick(Sobo19.Edit100.Text,Sobo19.Edit101.Text);
    Sobo19.Free;
    if Base10.Seek_Ggeo(Label300.Caption)='X' Then Close;
  end;
end;

procedure TSobo14.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo14:=nil;
  nSqry.AfterScroll:=nil;
  mSqry.AfterScroll:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo14.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo14.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_14_01(Self);
  end;
end;

procedure TSobo14.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo14.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button007Click(Sender: TObject);
var St1: String;
begin
  St1:= InputBox('ISBN검색', 'ISBN를 입력 하세요.  ', '');
  if St1 <> '' then begin

    Tong40.Show;
    Tong40.Update;

    T00:=0;
    nSqry:=Base10.T1_Sub41;

    Base10.OpenShow(nSqry);

    Sqlen := 'Select * From G4_Book Where '+D_Select+
             'Hcode=''@Hcode'' and Gisbn=''@Gisbn''';

    Translate(Sqlen, '@Hcode', Label300.Caption);
    Translate(Sqlen, '@Gisbn', St1);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(nSqry)
    else ShowMessage(E_Open);

    nSqry.First;
    Bmark:=nSqry.GetBookmark; nSqry.DisableControls;
    While nSqry.EOF=False do begin

      St1:=nSqry.FieldByName('Gubun').Value;
      if mSqry.Locate('Gcode',St1,[loCaseInsensitive])=True then
      St1:=mSqry.FieldByName('Gname').Value;

   // if Str2<>'' then
   // Tong40.SetTring02('','9999.99.99','',nSqry.FieldByName('Gcode').Value,'',Label300.Caption);

      T00:=0;
      if sSqry.Locate('Gcode',nSqry.FieldByName('Gcode').Value,[loCaseInsensitive]) then
      T00:=sSqry.FieldByName('GsumY').AsFloat;

      nSqry.Edit;
      nSqry.FieldByName('Sname').Value:=St1;
      if nSqry.FieldByName('Scode').AsString='B' Then
      nSqry.FieldByName('Scode').Value:='창고' else
      nSqry.FieldByName('Scode').Value:='본사';

      nSqry.FieldByName('Gsqut').AsFloat:=T00;
      nSqry.FieldByName('Gssum').AsFloat:=nSqry.FieldByName('Gdang').AsFloat*T00;
      nSqry.Post;
      nSqry.Next;
    end;
    nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;

    nSqry.First;
    nSqry.AfterScroll:=Base10.T1_Sub41AfterScroll;
    Button023Click(Self);
    Button024Click(Self);
    ProgressBar1.Position:=0;

    Tong40.Hide;
  { Tong40.Free; }
  end;
end;

procedure TSobo14.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX0(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo14.Button013Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX0(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo14.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('14-01');
end;

procedure TSobo14.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('14-01');
end;

procedure TSobo14.Button016Click(Sender: TObject);
begin
  Tong40.print_14_01(Self);
end;

procedure TSobo14.Button017Click(Sender: TObject);
begin
  Tong40.print_14_02(Self);
end;

procedure TSobo14.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button022Click(Sender: TObject);
begin
  nSqry.SaveToFile('.\Data\G4_Book.cds');
end;

procedure TSobo14.Button023Click(Sender: TObject);
begin
  Edit101.Text := nSqry.FieldByName('Sname').AsString;
  Edit102.Text := nSqry.FieldByName('Jubun').AsString;
  Edit103.Text := nSqry.FieldByName('Gcode').AsString;
  Edit104.Text := nSqry.FieldByName('Ocode').AsString;
  Edit105.Text := nSqry.FieldByName('Gname').AsString;
  Edit106.Text := nSqry.FieldByName('Gjeja').AsString;
  Edit107.Text := nSqry.FieldByName('Scode').AsString;
  Edit108.Text := nSqry.FieldByName('Gdabi').AsString;
  Edit109.Value:= nSqry.FieldByName('Gdang').AsFloat;
  Edit110.Text := nSqry.FieldByName('Gisbn').AsString;
  Edit111.Text := nSqry.FieldByName('Gbjil').AsString;
  Edit112.Value:= nSqry.FieldByName('Gsqut').AsFloat;
  Edit113.Value:= nSqry.FieldByName('Grat1').AsFloat;
  Edit114.Value:= nSqry.FieldByName('Grat2').AsFloat;
  Edit115.Value:= nSqry.FieldByName('Grat3').AsFloat;
  Edit116.Value:= nSqry.FieldByName('Grat4').AsFloat;
  Edit117.Value:= nSqry.FieldByName('Grat5').AsFloat;
  Edit118.Value:= nSqry.FieldByName('Grat6').AsFloat;
  Edit130.Value:= nSqry.FieldByName('Grat8').AsFloat;
  Edit119.Text := nSqry.FieldByName('Gbigo').AsString;
  Edit120.Text := nSqry.FieldByName('Gnumb').AsString;
  Edit121.Text := nSqry.FieldByName('Date1').AsString;
  Edit122.Text := nSqry.FieldByName('Date2').AsString;
  Edit123.Text := nSqry.FieldByName('Gpost').AsString;
  Edit129.Text := nSqry.FieldByName('Name2').AsString;
  Edit124.Value:= nSqry.FieldByName('Gpage').AsFloat;
  Edit125.Value:= nSqry.FieldByName('Gpan1').AsFloat;
  if nSqry.FieldByName('Yesno').AsString='True' then
  CheckBox1.Checked:=True else
  CheckBox1.Checked:=False;
  if nSqry.FieldByName('Grat9').AsString='1' then
  CheckBox2.Checked:=True else
  CheckBox2.Checked:=False;
end;

procedure TSobo14.Button024Click(Sender: TObject);
begin
  Edit201.Text := mSqry.FieldByName('Gcode').AsString;
  Edit202.Text := mSqry.FieldByName('Gname').AsString;
end;

procedure TSobo14.Button101Click(Sender: TObject);
begin
  if nSqry.State=dsInsert Then Button102Click(Self);
  nSqry.Insert;
  nSqry.FieldByName('Gcode').AsString := '';
  Edit101.SetFocus;
  Edit103.Enabled:=True;
end;

procedure TSobo14.Button102Click(Sender: TObject);
var MeDlg: Integer;
    St1,St2,Sq1,Sq2,Sq3: String;
begin
MeDlg := MessageDlg('저장 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin
  if Edit103.Enabled=True Then Edit101Exit(Self);
  if nSqry.State=dsInsert Then begin

    Sqlon := 'INSERT INTO G4_Book '+
    '( Gubun, Jubun, Gcode, Ocode, Gname, Gjeja, '+
    '  Gnumb, Date1, Date2, Gpost, Gpage, Gpan1, '+
    '  Scode, Gdabi, Gbigo, Gisbn, Gbjil, Gdang, '+
    '  Name2, Grat1, Grat2, Grat3, Grat4, Grat5, '+
    '  Grat6, Grat8, Grat9, Yesno, Hcode) VALUES ';
    Sq1 :=
    '(''@Gubun'',''@Jubun'',''@Gcode'',''@Ocode'',''@Gname'',''@Gjeja'', '+
    ' ''@Gnumb'',''@Date1'',''@Date2'',''@Gpost'',  @Gpage  ,  @Gpan1  , ';
    Sq2 :=
    ' ''@Scode'',''@Gdabi'',''@Gbigo'',''@Gisbn'',''@Gbjil'',  @Gdang  , '+
    ' ''@Name2'',  @Grat1  ,  @Grat2  ,  @Grat3  ,  @Grat4  ,  @Grat5  , '+
    '   @Grat6  ,  @Grat8  ,  @Grat9  ,''@Yesno'',''@Hcode'' )';

    St1 := 'Select Gcode From G4_Gbun Where '+D_Select+'Gname=''@Gname'' and Hcode=''@Hcode'' ';
    Translate(St1, '@Gname', Edit101.Text);
    Translate(St1, '@Hcode', Label300.Caption);
    St2 := Base10.Seek_Name(St1);

    Translate(Sq1, '@Gubun', St2);
    Translate(Sq1, '@Jubun', Edit102.Text);
    Translate(Sq1, '@Gcode', Edit103.Text);
    Translate(Sq1, '@Ocode', Edit104.Text);
    Translate(Sq1, '@Gname', Edit105.Text);
    Translate(Sq1, '@Gjeja', Edit106.Text);
    Translate(Sq1, '@Gnumb', Edit120.Text);
    Translate(Sq1, '@Date1', Edit121.Text);
    Translate(Sq1, '@Date2', Edit122.Text);
    Translate(Sq1, '@Gpost', Edit123.Text);
    TransAuto(Sq1, '@Gpage', FloatToStr(Edit124.Value));
    TransAuto(Sq1, '@Gpan1', FloatToStr(Edit125.Value));
    if Edit107.Text='본사' Then
    Translate(Sq2, '@Scode', 'A') else
    Translate(Sq2, '@Scode', 'B');
    Translate(Sq2, '@Gdabi', Edit108.Text);
    TransAuto(Sq2, '@Gdang', FloatToStr(Edit109.Value));
    Translate(Sq2, '@Gisbn', Edit110.Text);
    Translate(Sq2, '@Gbjil', Edit111.Text);
    TransAuto(Sq2, '@Grat1', FloatToStr(Edit113.Value));
    TransAuto(Sq2, '@Grat2', FloatToStr(Edit114.Value));
    TransAuto(Sq2, '@Grat3', FloatToStr(Edit115.Value));
    TransAuto(Sq2, '@Grat4', FloatToStr(Edit116.Value));
    TransAuto(Sq2, '@Grat5', FloatToStr(Edit117.Value));
    TransAuto(Sq2, '@Grat6', FloatToStr(Edit118.Value));
    TransAuto(Sq2, '@Grat8', FloatToStr(Edit130.Value));
    Translate(Sq2, '@Gbigo', Edit119.Text);
    Translate(Sq2, '@Name2', Edit129.Text);
    Translate(Sq2, '@Hcode', Label300.Caption);

    if CheckBox1.Checked=True then
    Translate(Sq2, '@Yesno', 'True') else
    Translate(Sq2, '@Yesno', 'False');

    if CheckBox2.Checked=True then
    TransAuto(Sq2, '@Grat9', '1') else
    TransAuto(Sq2, '@Grat9', '0');

    Sqlen:=Sqlon+Sq1+Sq2;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Insert);
      nSqry.Cancel;
      DBGrid101.SetFocus;
      Edit103.Enabled:=False;
      Exit;
    end;

    Base10.InSert_ID(nSqry,'G4_BOOK_ID_GEN');
  end else begin

    Sqlon := 'UPDATE G4_Book SET '+
    'Gubun=''@Gubun'',Jubun=''@Jubun'',Gcode=''@Gcode'',Ocode=''@Ocode'', '+
    'Gname=''@Gname'',Gjeja=''@Gjeja'',Scode=''@Scode'',Gdabi=''@Gdabi'', ';
    Sqlen :=
    'Gnumb=''@Gnumb'',Date1=''@Date1'',Date2=''@Date2'',Gpost=''@Gpost'', '+
    'Name2=''@Name2'',Gpage=  @Gpage  ,Gpan1=  @Gpan1  , '+
    'Gbigo=''@Gbigo'',Gisbn=''@Gisbn'',Gbjil=''@Gbjil'',Gdang=  @Gdang  , ';
    Sq1 :=
    'Grat1=  @Grat1  ,Grat2=  @Grat2  ,Grat3=  @Grat3  ,Grat4=  @Grat4  , '+
    'Grat5=  @Grat5  ,Grat6=  @Grat6  ,Grat8=  @Grat8  ,Grat9=  @Grat9  , '+
    'Yesno=''@Yesno'' WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';

    St1 := 'Select Gcode From G4_Gbun Where '+D_Select+'Gname=''@Gname'' and Hcode=''@Hcode'' ';
    Translate(St1, '@Gname', Edit101.Text);
    Translate(St1, '@Hcode', Label300.Caption);
    St2 := Base10.Seek_Name(St1);

    Translate(Sqlon, '@Gubun', St2);
    Translate(Sqlon, '@Jubun', Edit102.Text);
    Translate(Sqlon, '@Gcode', Edit103.Text);
    Translate(Sqlon, '@Ocode', Edit104.Text);
    Translate(Sqlon, '@Gname', Edit105.Text);
    Translate(Sqlon, '@Gjeja', Edit106.Text);
    if Edit107.Text='본사' Then
    Translate(Sqlon, '@Scode', 'A') else
    Translate(Sqlon, '@Scode', 'B');
    Translate(Sqlon, '@Gdabi', Edit108.Text);
    Translate(Sqlen, '@Gnumb', Edit120.Text);
    Translate(Sqlen, '@Date1', Edit121.Text);
    Translate(Sqlen, '@Date2', Edit122.Text);
    Translate(Sqlen, '@Gpost', Edit123.Text);
    Translate(Sqlen, '@Name2', Edit129.Text);
    TransAuto(Sqlen, '@Gpage', FloatToStr(Edit124.Value));
    TransAuto(Sqlen, '@Gpan1', FloatToStr(Edit125.Value));
    TransAuto(Sqlen, '@Gdang', FloatToStr(Edit109.Value));
    Translate(Sqlen, '@Gisbn', Edit110.Text);
    Translate(Sqlen, '@Gbjil', Edit111.Text);
    TransAuto(Sq1,   '@Grat1', FloatToStr(Edit113.Value));
    TransAuto(Sq1,   '@Grat2', FloatToStr(Edit114.Value));
    TransAuto(Sq1,   '@Grat3', FloatToStr(Edit115.Value));
    TransAuto(Sq1,   '@Grat4', FloatToStr(Edit116.Value));
    TransAuto(Sq1,   '@Grat5', FloatToStr(Edit117.Value));
    TransAuto(Sq1,   '@Grat6', FloatToStr(Edit118.Value));
    TransAuto(Sq1,   '@Grat8', FloatToStr(Edit130.Value));
    Translate(Sqlen, '@Gbigo', Edit119.Text);
    Translate(Sq1,   '@Gcode', Edit103.Text);
    Translate(Sq1,   '@Hcode', Label300.Caption);

    if CheckBox1.Checked=True then
    Translate(Sq1,   '@Yesno', 'True') else
    Translate(Sq1,   '@Yesno', 'False');

    if CheckBox2.Checked=True then
    TransAuto(Sq1,   '@Grat9', '1') else
    TransAuto(Sq1,   '@Grat9', '0');

    Sqlen:=Sqlon+Sqlen+Sq1;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Update);
      nSqry.Cancel;
      DBGrid101.SetFocus;
      Edit103.Enabled:=False;
      Exit;
    end;  

  end;

  St1 := 'Select Gcode From G4_Gbun Where '+D_Select+'Gname=''@Gname'' and Hcode=''@Hcode'' ';
  Translate(St1, '@Gname', Edit101.Text);
  Translate(St1, '@Hcode', Label300.Caption);
  St2 := Base10.Seek_Name(St1);

  nSqry.Edit;
  nSqry.FieldByName('Gubun').AsString := St2;
  nSqry.FieldByName('Sname').AsString := Edit101.Text;
  nSqry.FieldByName('Jubun').AsString := Edit102.Text;
  nSqry.FieldByName('Gcode').AsString := Edit103.Text;
  nSqry.FieldByName('Ocode').AsString := Edit104.Text;
  nSqry.FieldByName('Gname').AsString := Edit105.Text;
  nSqry.FieldByName('Gjeja').AsString := Edit106.Text;
  if Edit107.Text='' Then
  nSqry.FieldByName('Scode').AsString := '본사' else
  nSqry.FieldByName('Scode').AsString := Edit107.Text;
  nSqry.FieldByName('Gdabi').AsString := Edit108.Text;
  nSqry.FieldByName('Gdang').Value    := Edit109.Text;
  nSqry.FieldByName('Gisbn').AsString := Edit110.Text;
  nSqry.FieldByName('Gbjil').AsString := Edit111.Text;
  nSqry.FieldByName('Gsqut').Value    := Edit112.Text;
  nSqry.FieldByName('Grat1').Value    := Edit113.Text;
  nSqry.FieldByName('Grat2').Value    := Edit114.Text;
  nSqry.FieldByName('Grat3').Value    := Edit115.Text;
  nSqry.FieldByName('Grat4').Value    := Edit116.Text;
  nSqry.FieldByName('Grat5').Value    := Edit117.Text;
  nSqry.FieldByName('Grat6').Value    := Edit118.Text;
  nSqry.FieldByName('Grat8').Value    := Edit130.Text;
  nSqry.FieldByName('Gbigo').AsString := Edit119.Text;
  nSqry.FieldByName('Gnumb').AsString := Edit120.Text;
  nSqry.FieldByName('Date1').AsString := Edit121.Text;
  nSqry.FieldByName('Date2').AsString := Edit122.Text;
  nSqry.FieldByName('Gpost').AsString := Edit123.Text;
  nSqry.FieldByName('Name2').AsString := Edit129.Text;
  nSqry.FieldByName('Gpage').Value    := Edit124.Text;
  nSqry.FieldByName('Gpan1').Value    := Edit125.Text;

  if CheckBox1.Checked=True then
  nSqry.FieldByName('Yesno').AsString := 'True' else
  nSqry.FieldByName('Yesno').AsString := 'False';

  if CheckBox2.Checked=True then
  nSqry.FieldByName('Grat9').AsString := '1' else
  nSqry.FieldByName('Grat9').AsString := '0';

  nSqry.Post;
  DBGrid101.SetFocus;
  Edit103.Enabled:=False;
end;
mrNo: begin
  nSqry.Cancel;
  DBGrid101.SetFocus;
  Edit103.Enabled:=False;
end; end;
end;

procedure TSobo14.Button103Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin

  Sqlen := 'DELETE FROM G4_Book WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
  Translate(Sqlen, '@Gcode', Edit103.Text);
  Translate(Sqlen, '@Hcode', Label300.Caption);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then begin
    ShowMessage(E_Delete);
    DBGrid101.SetFocus;
    Exit;
  end;  

  if nSqry.IsEmpty=False Then nSqry.Delete;
  DBGrid101.SetFocus;
  Edit103.Enabled:=False;
end; end;
end;

procedure TSobo14.Button104Click(Sender: TObject);
begin
//
end;

procedure TSobo14.Button201Click(Sender: TObject);
begin
  mSqry.Insert;
  mSqry.FieldByName('Gcode').AsString := '';
  Edit201.SetFocus;
end;

procedure TSobo14.Button202Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('저장 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin
  if mSqry.State=dsInsert Then begin

    Sqlen := 'INSERT INTO G4_Gbun ( Gcode, Gname, Hcode ) VALUES '+
             '(''@Gcode'',''@Gname'',''@Hcode'')';

    Translate(Sqlen, '@Gcode', Edit201.Text);
    Translate(Sqlen, '@Gname', Edit202.Text);
    Translate(Sqlen, '@Hcode', Label300.Caption);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Insert);
      mSqry.Cancel;
      DBGrid201.SetFocus;
      Exit;
    end;

    Base10.InSert_ID(mSqry,'G4_GBUN_ID_GEN');
  end else begin

    Sqlen := 'UPDATE G4_Gbun SET Gcode=''@Gcode'',Gname=''@Gname'' '+
             'WHERE ID=@ID and Hcode=''@Hcode'' ';

    Translate(Sqlen, '@Gcode', Edit201.Text);
    Translate(Sqlen, '@Gname', Edit202.Text);
    Translate(Sqlen, '@Hcode', Label300.Caption);
    TransAuto(Sqlen, '@ID', mSqry.FieldByName('ID').AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Update);
      mSqry.Cancel;
      DBGrid201.SetFocus;
      Exit;
    end;

  end;
  mSqry.Edit;
  mSqry.FieldByName('Gcode').AsString := Edit201.Text;
  mSqry.FieldByName('Gname').AsString := Edit202.Text;
  mSqry.Post;
  DBGrid201.SetFocus;
end;
mrNo: begin
  mSqry.Cancel;
  DBGrid201.SetFocus;
end; end;
end;

procedure TSobo14.Button203Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin

  Sqlen := 'DELETE FROM G4_Gbun WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
  Translate(Sqlen, '@Gcode', Edit201.Text);
  Translate(Sqlen, '@Hcode', Label300.Caption);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then begin
    ShowMessage(E_Delete);
    DBGrid201.SetFocus;
    Exit;
  end;  

  if mSqry.IsEmpty=False Then mSqry.Delete;
  DBGrid201.SetFocus;
end; end;
end;

procedure TSobo14.Edit101Exit(Sender: TObject);
var St1,St2: String;
begin
  if Edit103.Text='' Then begin
    ShowMessage('코드를 입력하세요.');
    Edit103.SetFocus; Exit;
  end else begin
    St1 := 'Select Gcode From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(St1, '@Gcode', Edit103.Text);
    Translate(St1, '@Hcode', Label300.Caption);
    St2 := Base10.Seek_Name(St1);

    if St2<>'' Then begin
    ShowMessage('코드가 이미 등록되어있습니다. 다시 입력하세요.');
    Edit103.SetFocus; Exit;
    end;
  end;
end;

procedure TSobo14.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit103.Focused=True)and(Edit103.SelStart=10)and(Length(Trim(Edit103.Text))=10))or
    ((Edit104.Focused=True)and(Edit104.SelStart=10)and(Length(Trim(Edit104.Text))=10))or
    ((Edit105.Focused=True)and(Edit105.SelStart=80)and(Length(Trim(Edit105.Text))=80))or
    ((Edit106.Focused=True)and(Edit106.SelStart=30)and(Length(Trim(Edit106.Text))=30))or
    ((Edit108.Focused=True)and(Edit108.SelStart=05)and(Length(Trim(Edit108.Text))=05))or
    ((Edit109.Focused=True)and(Edit109.SelStart=08)and(Length(Trim(Edit110.Text))=08))or
    ((Edit110.Focused=True)and(Edit110.SelStart=20)and(Length(Trim(Edit110.Text))=20))or
    ((Edit111.Focused=True)and(Edit111.SelStart=06)and(Length(Trim(Edit111.Text))=06))or
    ((Edit112.Focused=True)and(Edit112.SelStart=15)and(Length(Trim(Edit112.Text))=15))or
    ((Edit113.Focused=True)and(Edit113.SelStart=03)and(Length(Trim(Edit113.Text))=03))or
    ((Edit114.Focused=True)and(Edit114.SelStart=03)and(Length(Trim(Edit114.Text))=03))or
    ((Edit115.Focused=True)and(Edit115.SelStart=03)and(Length(Trim(Edit115.Text))=03))or
    ((Edit116.Focused=True)and(Edit116.SelStart=03)and(Length(Trim(Edit116.Text))=03))or
    ((Edit117.Focused=True)and(Edit117.SelStart=03)and(Length(Trim(Edit117.Text))=03))or
    ((Edit118.Focused=True)and(Edit118.SelStart=03)and(Length(Trim(Edit118.Text))=03))or
    ((Edit130.Focused=True)and(Edit130.SelStart=03)and(Length(Trim(Edit130.Text))=03))or
    ((Edit120.Focused=True)and(Edit120.SelStart=20)and(Length(Trim(Edit120.Text))=20))or
    ((Edit121.Focused=True)and(Edit121.SelStart=10)and(Length(Trim(Edit121.Text))=10))or
    ((Edit122.Focused=True)and(Edit122.SelStart=10)and(Length(Trim(Edit122.Text))=10))or
    ((Edit123.Focused=True)and(Edit123.SelStart=20)and(Length(Trim(Edit123.Text))=20))or
    ((Edit124.Focused=True)and(Edit124.SelStart=10)and(Length(Trim(Edit124.Text))=10))or
    ((Edit125.Focused=True)and(Edit125.SelStart=10)and(Length(Trim(Edit125.Text))=10))or
    ((Edit119.Focused=True)and(Edit119.SelStart=50)and(Length(Trim(Edit119.Text))=50))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo14.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo14.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo14.Edit102KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Button102Click(Self);
    DBGrid101.SetFocus;
  end;
end;

procedure TSobo14.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then begin
    Button102Click(Self);
    DBGrid101.SetFocus;
  end;
end;

procedure TSobo14.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo14.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo14.Edit112KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    DGrid: TDBGrid;
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

procedure TSobo14.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit101;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo14.Edit113KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    DGrid: TDBGrid;
    Edits: TFlatComboBox;
begin
  Hands:=Edit102.Handle;
  Edits:=Edit102;
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

procedure TSobo14.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit102;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo14.Edit114KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    DGrid: TDBGrid;
    Edits: TFlatComboBox;
begin
  Hands:=Edit107.Handle;
  Edits:=Edit107;
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

procedure TSobo14.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit107;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo14.Edit115KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Button202Click(Self);
    DBGrid201.SetFocus;
  end;
end;

procedure TSobo14.Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then begin
    Button202Click(Self);
    DBGrid201.SetFocus;
  end;
end;

procedure TSobo14.DBGrid101DblClick(Sender: TObject);
begin
{ nSqry.Edit;
  if nSqry.FieldByName('Scode').AsString<>'' Then
     nSqry.FieldByName('Scode').AsString:='' else
     nSqry.FieldByName('Scode').AsString:='O';
  nSqry.Post;

  Sqlen := 'UPDATE G4_Book SET Scode=''@Scode'' '+
           'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
  Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
  Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
  Translate(Sqlen, '@Hcode', Label300.Caption);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update); }
end;

procedure TSobo14.DBGrid101Enter(Sender: TObject);
begin
  if nSqry.State=dsInsert Then Button102Click(Self);
end;

procedure TSobo14.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo14.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_RETURN Then Edit101.SetFocus;
  if Key=VK_INSERT Then Button101Click(Self);
  if Key=VK_DELETE Then Button103Click(Self);
  end;
end;

procedure TSobo14.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo14.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_RETURN Then Edit201.SetFocus;
  if Key=VK_INSERT Then Button201Click(Self);
  if Key=VK_DELETE Then Button203Click(Self);
  end;
end;

procedure TSobo14.DBGrid101Exit(Sender: TObject);
begin
//
end;

procedure TSobo14.DBGrid201Exit(Sender: TObject);
var St1: String;
begin
  Edit101.Items.Clear;
  St1:='Hcode'+'='+#39+Label300.Caption+#39;
  Sqlen := 'Select * From G4_Gbun Where '+D_Select+St1+' Order By Gcode';
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    List1:=0;
    T00:=Base10.Socket.ClientData('1');
    while List1 < T00-1 do begin
      List1:=List1+1;
      Edit101.Items.Add(Base10.Socket.GetData(List1, 3));
    end;
  end;
end;

procedure TSobo14.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo14.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo14.SeachClick(Str1,Str2: String);
var St1: String;
begin
  if Base10.Seek_Ggeo(Label300.Caption)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  T00:=0;
  nSqry:=Base10.T1_Sub41;
  mSqry:=Base10.T1_Sub42;

  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);

  St1:=Str1+' Like '+#39+'%'+Str2+'%'+#39;

  if Lower='1' then
  St1:='Lower('+Str1+') like '+'Lower('+#39+'%'+Str2+'%'+#39+')';

  if Str2='' then
  St1:=Str1+' = '+#39+''+#39;

  if Str1='' then
  St1:='Gcode'+' Like '+#39+'%'+''+'%'+#39;

  St1:='Hcode'+'='+#39+Label300.Caption+#39+' and '+St1;

  if Label300.Caption='122' then
  Sqlen := 'Select Hcode,Gubun,Gcode,Gname,Gdang,Gisbn,Gpost From G4_Book Where '+D_Select+St1+' Order By Gcode'
  else
  Sqlen := 'Select * From G4_Book Where '+D_Select+St1+' Order By Gcode';

//if Label300.Caption='122' then
//Sqlen := Sqlen+' LIMIT 0,2000 ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  St1:='Hcode'+'='+#39+Label300.Caption+#39;

  Sqlen := 'Select ID,Gcode,Gname From G4_Gbun Where '+D_Select+St1+' Order By Gcode';
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(mSqry)
  else ShowMessage(E_Open);

  mSqry.First;
  Edit101.Items.Clear;
  While mSqry.EOF=False do begin
    Edit101.Items.Add(mSqry.FieldByName('Gname').AsString);
    mSqry.Next;
  end;

 if Label300.Caption<>'122' then begin
  if(Str1='')and(Str2='')then
  Tong40.SetTring02('','9999.99.99','','','',Label300.Caption);

  nSqry.First;
  ProgressBar1.Max:=nSqry.RecordCount;
  Bmark:=nSqry.GetBookmark; nSqry.DisableControls;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    St1:=nSqry.FieldByName('Gubun').AsString;
    if mSqry.Locate('Gcode',St1,[loCaseInsensitive])=True then
    St1:=mSqry.FieldByName('Gname').AsString;

    if Str2<>'' then
    Tong40.SetTring02('','9999.99.99','',nSqry.FieldByName('Gcode').Value,'',Label300.Caption);

    T00:=0;
    if sSqry.Locate('Gcode',nSqry.FieldByName('Gcode').Value,[loCaseInsensitive]) then
    T00:=sSqry.FieldByName('GsumY').AsFloat;

    nSqry.Edit;
    nSqry.FieldByName('Sname').Value:=St1;
    if nSqry.FieldByName('Scode').AsString='B' Then
    nSqry.FieldByName('Scode').Value:='창고' else
    nSqry.FieldByName('Scode').Value:='본사';

    nSqry.FieldByName('Gsqut').AsFloat:=T00;
    nSqry.FieldByName('Gssum').AsFloat:=nSqry.FieldByName('Gdang').AsFloat*T00;
    nSqry.Post;
    nSqry.Next;
  end;
  nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
 end;

  mSqry.First;
  nSqry.First;
  mSqry.AfterScroll:=Base10.T1_Sub42AfterScroll;
  nSqry.AfterScroll:=Base10.T1_Sub41AfterScroll;
  Button023Click(Self);
  Button024Click(Self);
  ProgressBar1.Position:=0;

  Tong40.Hide;
{ Tong40.Free; }
end;

end.
