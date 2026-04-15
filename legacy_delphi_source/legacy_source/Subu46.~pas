unit Subu46;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, DBGridEh, ToolEdit,
  DBClient, TFlatCheckBoxUnit, TFlatRadioButtonUnit, dxCore, dxButtons;

type
  TSobo46 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
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
    Edit100: TFlatMaskEdit;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Label101: TmyLabel3d;
    DateEdit1: TDateEdit;
    Button701: TFlatButton;
    Button702: TFlatButton;
    Edit101: TFlatComboBox;
    DBGrid101: TDBGridEh;
    FlatPanel25: TFlatPanel;
    RadioButton4: TFlatRadioButton;
    RadioButton5: TFlatRadioButton;
    T4_Sub61: TClientDataSet;
    T4_Sub61ID: TFloatField;
    T4_Sub61IDNUM: TFloatField;
    T4_Sub61GDATE: TStringField;
    T4_Sub61GCODE: TStringField;
    T4_Sub61GNAME: TStringField;
    T4_Sub61HCODE: TStringField;
    T4_Sub61HNAME: TStringField;
    T4_Sub61NAME1: TStringField;
    T4_Sub61NAME2: TStringField;
    T4_Sub61GQUT1: TFloatField;
    T4_Sub61GQUT2: TFloatField;
    T4_Sub61GQUT3: TFloatField;
    T4_Sub61GQUT4: TFloatField;
    T4_Sub61GSQUT: TFloatField;
    T4_Sub61GSSUM: TFloatField;
    T4_Sub61YESNO: TStringField;
    T4_Sub62: TClientDataSet;
    T4_Sub62ID: TFloatField;
    T4_Sub62IDNUM: TFloatField;
    T4_Sub62GDATE: TStringField;
    T4_Sub62SCODE: TStringField;
    T4_Sub62GCODE: TStringField;
    T4_Sub62GNAME: TStringField;
    T4_Sub62HCODE: TStringField;
    T4_Sub62HNAME: TStringField;
    T4_Sub62OCODE: TStringField;
    T4_Sub62BCODE: TStringField;
    T4_Sub62BNAME: TStringField;
    T4_Sub62GJEJA: TStringField;
    T4_Sub62GUBUN: TStringField;
    T4_Sub62JUBUN: TStringField;
    T4_Sub62PUBUN: TStringField;
    T4_Sub62TCODE: TStringField;
    T4_Sub62GSQUT: TFloatField;
    T4_Sub62QSQUT: TFloatField;
    T4_Sub62GDANG: TFloatField;
    T4_Sub62GRAT1: TSmallintField;
    T4_Sub62GSSUM: TFloatField;
    T4_Sub62JEAGO: TFloatField;
    T4_Sub62GBIGO: TStringField;
    T4_Sub62YESNO: TStringField;
    T4_Sub62GMEMO: TDateTimeField;
    T4_Sub61GQUT5: TFloatField;
    T4_Sub61GQUT6: TFloatField;
    T4_Sub61GQUT7: TFloatField;
    dxButton1: TdxButton;
    Panel003: TFlatPanel;
    StBar201: TStatusBar;
    DBGrid201: TDBGridEh;
    Panel200: TFlatPanel;
    Button301: TFlatButton;
    CheckBox1: TFlatCheckBox;
    Panel201: TFlatPanel;
    Panel210: TFlatPanel;
    Panel202: TFlatPanel;
    Panel204: TFlatPanel;
    Edit201: TFlatNumber;
    Edit208: TFlatNumber;
    Edit209: TFlatNumber;
    Edit210: TFlatNumber;
    Edit202: TFlatNumber;
    Edit203: TFlatNumber;
    Edit204: TFlatNumber;
    Panel203: TFlatPanel;
    Edit205: TFlatNumber;
    Edit206: TFlatNumber;
    Edit207: TFlatNumber;
    Edit231: TFlatNumber;
    Edit232: TFlatNumber;
    FlatPanel4: TFlatPanel;
    FlatPanel9: TFlatPanel;
    FlatPanel15: TFlatPanel;
    FlatPanel16: TFlatPanel;
    Edit246: TFlatNumber;
    Edit224: TFlatNumber;
    Panel205: TFlatPanel;
    Panel207: TFlatPanel;
    Edit217: TFlatNumber;
    Panel211: TFlatPanel;
    Edit211: TFlatNumber;
    Edit212: TFlatNumber;
    Edit213: TFlatNumber;
    Edit218: TFlatNumber;
    Edit219: TFlatNumber;
    Edit220: TFlatNumber;
    Edit225: TFlatNumber;
    Panel206: TFlatPanel;
    Edit214: TFlatNumber;
    Edit215: TFlatNumber;
    Edit216: TFlatNumber;
    Edit221: TFlatNumber;
    Edit222: TFlatNumber;
    Edit223: TFlatNumber;
    Edit229: TFlatNumber;
    Edit233: TFlatNumber;
    Edit234: TFlatNumber;
    Edit235: TFlatNumber;
    FlatPanel2: TFlatPanel;
    FlatPanel3: TFlatPanel;
    Edit240: TFlatNumber;
    Edit241: TFlatNumber;
    Edit242: TFlatNumber;
    Edit243: TFlatNumber;
    Edit244: TFlatNumber;
    Edit245: TFlatNumber;
    CheckBox2: TFlatCheckBox;
    CheckBox3: TFlatCheckBox;
    Panel208: TFlatPanel;
    Panel209: TFlatPanel;
    Panel215: TFlatPanel;
    Panel217: TFlatPanel;
    FlatPanel1: TFlatPanel;
    FlatPanel5: TFlatPanel;
    FlatPanel6: TFlatPanel;
    FlatPanel10: TFlatPanel;
    FlatPanel11: TFlatPanel;
    FlatPanel12: TFlatPanel;
    FlatPanel13: TFlatPanel;
    FlatPanel14: TFlatPanel;
    FlatPanel17: TFlatPanel;
    Edit247: TFlatNumber;
    Edit248: TFlatNumber;
    FlatPanel21: TFlatPanel;
    Edit261: TFlatNumber;
    Edit262: TFlatNumber;
    Edit263: TFlatNumber;
    FlatPanel23: TFlatPanel;
    Edit264: TFlatNumber;
    Edit265: TFlatNumber;
    Edit266: TFlatNumber;
    FlatPanel24: TFlatPanel;
    Panel213: TFlatPanel;
    Edit227: TFlatNumber;
    Panel212: TFlatPanel;
    Edit226: TFlatNumber;
    Panel216: TFlatPanel;
    Panel214: TFlatPanel;
    Edit228: TFlatNumber;
    Edit230: TFlatNumber;
    FlatPanel18: TFlatPanel;
    Label301: TmyLabel3d;
    FlatPanel41: TFlatPanel;
    FlatPanel7: TFlatPanel;
    Edit238: TFlatEdit;
    Edit236: TFlatNumber;
    FlatPanel8: TFlatPanel;
    Edit239: TFlatEdit;
    Edit237: TFlatNumber;
    FlatPanel19: TFlatPanel;
    Label302: TmyLabel3d;
    FlatPanel20: TFlatPanel;
    myLabel3d1: TmyLabel3d;
    FlatPanel27: TFlatPanel;
    FlatPanel32: TFlatPanel;
    Edit301: TFlatNumber;
    Edit302: TFlatNumber;
    Edit303: TFlatNumber;
    FlatPanel33: TFlatPanel;
    FlatPanel35: TFlatPanel;
    FlatPanel36: TFlatPanel;
    FlatPanel37: TFlatPanel;
    FlatPanel38: TFlatPanel;
    FlatPanel39: TFlatPanel;
    Edit304: TFlatNumber;
    Edit305: TFlatNumber;
    Edit309: TFlatNumber;
    Edit306: TFlatNumber;
    Edit307: TFlatNumber;
    Edit308: TFlatNumber;
    Edit310: TFlatNumber;
    Edit311: TFlatNumber;
    Edit312: TFlatNumber;
    FlatPanel26: TFlatPanel;
    myLabel3d2: TmyLabel3d;
    FlatPanel22: TFlatPanel;
    FlatPanel28: TFlatPanel;
    Edit313: TFlatNumber;
    Edit314: TFlatNumber;
    Edit315: TFlatNumber;
    FlatPanel30: TFlatPanel;
    Edit901: TFlatMaskEdit;
    Edit902: TFlatNumber;
    FlatPanel40: TFlatPanel;
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
    procedure Edit115KeyPress(Sender: TObject; var Key: Char);
    procedure Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
    procedure Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101TitleClick(Column: TColumn);
    procedure DBGrid201TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);

    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure RadioButton4Click(Sender: TObject);
    procedure RadioButton5Click(Sender: TObject);
    procedure DBGrid101DrawColumnCell(Sender: TObject; const Rect: TRect;
      DataCol: Integer; Column: TColumnEh; State: TGridDrawState);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo46: TSobo46;
  S_Date: String;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib, globalCommon,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo46.FormActivate(Sender: TObject);
begin
  nForm:='46';
  nSqry:=T4_Sub61;
  mSqry:=T4_Sub62;
end;

procedure TSobo46.FormShow(Sender: TObject);
begin
  T00:=0;
//  Edit101.Text:=FormatDateTime('yyyy"."mm"',Date);
  SetMonth2Combo(TCombobox(Edit101));
  Application.HintHidePause:=10000;
end;

procedure TSobo46.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo46:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Application.HintHidePause:=5000;
end;

procedure TSobo46.Button001Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
     Seak10.ShowModal;
  end; }
end;

procedure TSobo46.Button002Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_45_02(Self);
  end; }
end;

procedure TSobo46.Button003Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo46.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo46.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo46.Button006Click(Sender: TObject);
begin
{ T00:=1;
  Button201Click(Self); }
end;

procedure TSobo46.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo46.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('24');
end;

procedure TSobo46.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('24');
end;

procedure TSobo46.Button010Click(Sender: TObject);
begin
//Button811Click(Self);
//Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo46.Button011Click(Sender: TObject);
begin
//Button812Click(Self);
//Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo46.Button012Click(Sender: TObject);
begin
  oSqry:=mSqry;
//Base10.ColumnX1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo46.Button013Click(Sender: TObject);
begin
  oSqry:=nSqry;
//Base10.ColumnX9(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo46.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('46-01');
end;

procedure TSobo46.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('46-02');
end;

procedure TSobo46.Button016Click(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    mSqry.First;
    While mSqry.EOF=False do begin
      if(mSqry.FieldByName('Bcode').AsString='완료')and
        (mSqry.FieldByName('Yesno').AsString='O'   )then begin
        Button201Click(Self);
        Tong40.print_46_01(Self);
      end;
      mSqry.Next;
    end;
    mSqry.First;
  end;
end;

procedure TSobo46.Button017Click(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    mSqry.First;
    While mSqry.EOF=False do begin
      if(mSqry.FieldByName('Bcode').AsString='완료')and
        (mSqry.FieldByName('Yesno').AsString='O'   )then begin
        Button201Click(Self);
        Tong40.print_46_02(Self);
      end;
      mSqry.Next;
    end;
    mSqry.First;
  end;
end;

procedure TSobo46.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo46.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo46.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo46.Button021Click(Sender: TObject);
begin
//Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo46.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo46.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo46.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo46.Button101Click(Sender: TObject);
begin
//if Base10.Seek_Ggeo(Edit108.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);

  Sqlen := 'Select Gcode,Gname,Gtel1,Gtel2,Jumin,Giqut,Gisum,Yes35,Gssum From G7_Ggeo Where '+D_Open;

  if (Edit104.Text<>'') Then
  Sqlen:=Sqlen+
         ' and '+'Gcode'+'>='+#39+Edit102.Text+#39+
         ' and '+'Gcode'+'<='+#39+Edit104.Text+#39;

  if S_Where2<>'' then
  Sqlen:=Sqlen+' and '+S_Where2;

  Sqlen:=Sqlen+' Order By Gcode';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    mSqry.Append;
    mSqry.FieldByName('Gdate').AsString:=Edit101.Text;
    mSqry.FieldByName('Hcode').AsString:=SGrid.Cells[ 0,List1];
    mSqry.FieldByName('Hname').AsString:=SGrid.Cells[ 1,List1];
    mSqry.FieldByName('Bname').AsString:=SGrid.Cells[ 2,List1]+'-'+SGrid.Cells[ 3,List1];
    mSqry.FieldByName('Yesno').AsString:='N';
    mSqry.Post;
  end;

  Sqlen := 'Select Hcode,Chek1,Chek2,Yesno From T2_Ssub '+
           'Where '+D_Select+'Gdate=''@Gdate'' and Yesno=''@Yesno'' ';
  Translate(Sqlen, '@Gdate', Edit101.Text);
  Translate(Sqlen, '@Yesno', '1');

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    if mSqry.Locate('Hcode',SGrid.Cells[ 0,List1],[loCaseInsensitive])=True then begin
      mSqry.Edit;
      mSqry.FieldByName('Gbigo').AsString:=SGrid.Cells[ 1,List1];
      mSqry.FieldByName('Gmemo').AsString:=SGrid.Cells[ 2,List1];
      if SGrid.Cells[ 3,List1]='1' then
      mSqry.FieldByName('Bcode').AsString:='완료';
      mSqry.Post;
    end;
  end;

  nSqry.First;
  mSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo46.Button201Click(Sender: TObject);
var St1,St2,St3: String;
    St9: Integer;
begin
  Base10.OpenShow(nSqry);
  Bmark:=nSqry.GetBookmark; nSqry.DisableControls;

  Edit201.Value:=0;
  Edit202.Value:=0;
  Edit203.Value:=0;
  Edit204.Value:=0;
  Edit205.Value:=0;
  Edit206.Value:=0;
  Edit207.Value:=0;
  Edit208.Value:=0;
  Edit209.Value:=0;
  Edit210.Value:=0;
  Edit211.Value:=0;
  Edit212.Value:=0;
  Edit213.Value:=0;
  Edit214.Value:=0;
  Edit215.Value:=0;
  Edit216.Value:=0;
  Edit217.Value:=0;
  Edit218.Value:=0;
  Edit219.Value:=0;
  Edit220.Value:=0;
  Edit221.Value:=0;
  Edit222.Value:=0;
  Edit223.Value:=0;
  Edit224.Value:=0;
  Edit225.Value:=0;
  Edit226.Value:=0;
  Edit227.Value:=0;
  Edit228.Value:=0;
  Edit229.Value:=0;
  Edit230.Value:=0;
  Edit231.Value:=0;
  Edit232.Value:=0;
  Edit233.Value:=0;
  Edit234.Value:=0;
  Edit235.Value:=0;
  Edit236.Value:=0;
  Edit237.Value:=0;
  Edit238.Text:='';
  Edit239.Text:='';
  Edit240.Value:=0;
  Edit241.Value:=0;
  Edit242.Value:=0;
  Edit243.Value:=0;
  Edit244.Value:=0;
  Edit245.Value:=0;
  Edit246.Value:=0;
  Edit247.Value:=0;
  Edit248.Value:=0;
  Edit261.Value:=0;
  Edit262.Value:=0;
  Edit263.Value:=0;
  Edit264.Value:=0;
  Edit265.Value:=0;
  Edit266.Value:=0;
  Edit301.Value:=0;
  Edit302.Value:=0;
  Edit303.Value:=0;
  Edit304.Value:=0;
  Edit305.Value:=0;
  Edit306.Value:=0;
  Edit307.Value:=0;
  Edit308.Value:=0;
  Edit309.Value:=0;
  Edit310.Value:=0;
  Edit311.Value:=0;
  Edit312.Value:=0;
  Edit313.Value:=0;
  Edit314.Value:=0;
  Edit315.Value:=0;
  Edit901.Text:='';
  Edit902.Value:=0;

  St1:='Gdate'+'>='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Gdate'+'<='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;

  Sqlen := 'Select Hcode,'+
           'Sum01,Sum02,Sum03,Sum04,Sum05,Sum06,Sum07,Sum08,Sum09,Sum10,'+
           'Sum11,Sum12,Sum13,Sum14,Sum15,Sum16,Sum17,Sum18,Sum19,Sum20,'+
           'Sum21,Sum22,Sum23,Sum24,Sum25,Sum26,Sum27,Sum28,Sum29,Sum30,'+
           'Sum31,Sum32,Sum33,Sum34,Sum35,Sum36,Sum37,Sum40,Sum41,Sum42,'+
           'Sum43,Sum44,Sum45,Sum46,Sum47,Sum48,Sum61,Sum62,Sum63,Sum64,'+
           'Sum65,Sum66,Sum51,Sum52,Sum53,Sum54,Sum55,Sum56,Sum57,Sum58,'+
           'Sum59,Sum67,Sum68,Sum69,Gsusu,Vdate,Bigo1,Bigo2,Yesno '+
           ' From T2_Ssub Where '+D_Select+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    Edit201.Value:=StrToIntDef(SGrid.Cells[ 1,List1],0);
    Edit202.Value:=StrToIntDef(SGrid.Cells[ 2,List1],0);
    Edit203.Value:=StrToIntDef(SGrid.Cells[ 3,List1],0);
    Edit204.Value:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    Edit205.Value:=StrToIntDef(SGrid.Cells[ 5,List1],0);
    Edit206.Value:=StrToIntDef(SGrid.Cells[ 6,List1],0);
    Edit207.Value:=StrToIntDef(SGrid.Cells[ 7,List1],0);
    Edit208.Value:=StrToIntDef(SGrid.Cells[ 8,List1],0);
    Edit209.Value:=StrToIntDef(SGrid.Cells[ 9,List1],0);
    Edit210.Value:=StrToIntDef(SGrid.Cells[10,List1],0);
    Edit211.Value:=StrToIntDef(SGrid.Cells[11,List1],0);
    Edit212.Value:=StrToIntDef(SGrid.Cells[12,List1],0);
    Edit213.Value:=StrToIntDef(SGrid.Cells[13,List1],0);
    Edit214.Value:=StrToIntDef(SGrid.Cells[14,List1],0);
    Edit215.Value:=StrToIntDef(SGrid.Cells[15,List1],0);
    Edit216.Value:=StrToIntDef(SGrid.Cells[16,List1],0);
    Edit217.Value:=StrToIntDef(SGrid.Cells[17,List1],0);
    Edit218.Value:=StrToIntDef(SGrid.Cells[18,List1],0);
    Edit219.Value:=StrToIntDef(SGrid.Cells[19,List1],0);
    Edit220.Value:=StrToIntDef(SGrid.Cells[20,List1],0);
    Edit221.Value:=StrToIntDef(SGrid.Cells[21,List1],0);
    Edit222.Value:=StrToIntDef(SGrid.Cells[22,List1],0);
    Edit223.Value:=StrToIntDef(SGrid.Cells[23,List1],0);
    Edit224.Value:=StrToIntDef(SGrid.Cells[24,List1],0);
    Edit225.Value:=StrToIntDef(SGrid.Cells[25,List1],0);
    Edit226.Value:=StrToIntDef(SGrid.Cells[26,List1],0);
    Edit227.Value:=StrToIntDef(SGrid.Cells[27,List1],0);
    Edit228.Value:=StrToIntDef(SGrid.Cells[28,List1],0);
    Edit229.Value:=StrToIntDef(SGrid.Cells[29,List1],0);
    Edit230.Value:=StrToIntDef(SGrid.Cells[30,List1],0);
    Edit231.Value:=StrToIntDef(SGrid.Cells[31,List1],0);
    Edit232.Value:=StrToIntDef(SGrid.Cells[32,List1],0);
    Edit233.Value:=StrToIntDef(SGrid.Cells[33,List1],0);
    Edit234.Value:=StrToIntDef(SGrid.Cells[34,List1],0);
    Edit235.Value:=StrToIntDef(SGrid.Cells[35,List1],0);
    Edit236.Value:=StrToIntDef(SGrid.Cells[36,List1],0);
    Edit237.Value:=StrToIntDef(SGrid.Cells[37,List1],0);
    Edit240.Value:=StrToIntDef(SGrid.Cells[38,List1],0);
    Edit241.Value:=StrToIntDef(SGrid.Cells[39,List1],0);
    Edit242.Value:=StrToIntDef(SGrid.Cells[40,List1],0);
    Edit243.Value:=StrToIntDef(SGrid.Cells[41,List1],0);
    Edit244.Value:=StrToIntDef(SGrid.Cells[42,List1],0);
    Edit245.Value:=StrToIntDef(SGrid.Cells[43,List1],0);
    Edit246.Value:=StrToIntDef(SGrid.Cells[44,List1],0);
    Edit247.Value:=StrToIntDef(SGrid.Cells[45,List1],0);
    Edit248.Value:=StrToIntDef(SGrid.Cells[46,List1],0);
    Edit261.Value:=StrToIntDef(SGrid.Cells[47,List1],0);
    Edit262.Value:=StrToIntDef(SGrid.Cells[48,List1],0);
    Edit263.Value:=StrToIntDef(SGrid.Cells[49,List1],0);
    Edit264.Value:=StrToIntDef(SGrid.Cells[50,List1],0);
    Edit265.Value:=StrToIntDef(SGrid.Cells[51,List1],0);
    Edit266.Value:=StrToIntDef(SGrid.Cells[52,List1],0);

    Edit301.Value:=StrToIntDef(SGrid.Cells[53,List1],0);
    Edit302.Value:=StrToIntDef(SGrid.Cells[54,List1],0);
    Edit303.Value:=StrToIntDef(SGrid.Cells[55,List1],0);
    Edit304.Value:=StrToIntDef(SGrid.Cells[56,List1],0);
    Edit305.Value:=StrToIntDef(SGrid.Cells[57,List1],0);
    Edit306.Value:=StrToIntDef(SGrid.Cells[58,List1],0);
    Edit307.Value:=StrToIntDef(SGrid.Cells[59,List1],0);
    Edit308.Value:=StrToIntDef(SGrid.Cells[60,List1],0);
    Edit309.Value:=StrToIntDef(SGrid.Cells[61,List1],0);

    Edit310.Text :=SGrid.Cells[62,List1];
    Edit312.Value:=StrToIntDef(SGrid.Cells[63,List1],0);

    Edit315.Value:=StrToIntDef(SGrid.Cells[64,List1],0);

    Edit902.Value:=StrToIntDef(SGrid.Cells[65,List1],0);
    Edit901.Text :=SGrid.Cells[66,List1];

    Edit238.Text :=SGrid.Cells[67,List1];
    Edit239.Text :=SGrid.Cells[68,List1];
  end;

  for St9 := 1 to 31 do begin
    if St9=1  then St3:='01';
    if St9=2  then St3:='02';
    if St9=3  then St3:='03';
    if St9=4  then St3:='04';
    if St9=5  then St3:='05';
    if St9=6  then St3:='06';
    if St9=7  then St3:='07';
    if St9=8  then St3:='08';
    if St9=9  then St3:='09';
    if St9=10 then St3:='10';
    if St9=11 then St3:='11';
    if St9=12 then St3:='12';
    if St9=13 then St3:='13';
    if St9=14 then St3:='14';
    if St9=15 then St3:='15';
    if St9=16 then St3:='16';
    if St9=17 then St3:='17';
    if St9=18 then St3:='18';
    if St9=19 then St3:='19';
    if St9=20 then St3:='20';
    if St9=21 then St3:='21';
    if St9=22 then St3:='22';
    if St9=23 then St3:='23';
    if St9=24 then St3:='24';
    if St9=25 then St3:='25';
    if St9=26 then St3:='26';
    if St9=27 then St3:='27';
    if St9=28 then St3:='28';
    if St9=29 then St3:='29';
    if St9=30 then St3:='30';
    if St9=31 then St3:='31';
    nSqry.Append;
    nSqry.FieldByName('Gdate').AsString:=St3;
    nSqry.FieldByName('Hcode').AsString:='';
    nSqry.FieldByName('Yesno').AsString:='0';
    nSqry.Post;
  end;

  St1:='Gdate'+'>='+#39+mSqry.FieldByName('Gdate').AsString+'.00'+#39+' and '+
       'Gdate'+'<='+#39+mSqry.FieldByName('Gdate').AsString+'.99'+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;

  Sqlen := 'Select Hcode,'+
           'Gdate,Gqut1,Gqut2,Gqut3,Gqut4,Name1,Name2,Gname,Gcode,Gsqut,Gssum,Yesno,Gqut5,Gqut6,Gqut7 '+
           ' From T3_Ssub Where '+D_Select+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    St3:=Copy(SGrid.Cells[ 1,List1],9,2);
    if nSqry.Locate('Gdate;Hcode',VarArrayOf([St3,'']),[loCaseInsensitive])=True then begin

      nSqry.Edit;

      if SGrid.Cells[ 2,List1]<>'0' then
      nSqry.FieldByName('Gqut1').AsString:=SGrid.Cells[ 2,List1];
      if SGrid.Cells[ 3,List1]<>'0' then
      nSqry.FieldByName('Gqut2').AsString:=SGrid.Cells[ 3,List1];
      if SGrid.Cells[ 4,List1]<>'0' then
      nSqry.FieldByName('Gqut3').AsString:=SGrid.Cells[ 4,List1];
      if SGrid.Cells[ 5,List1]<>'0' then
      nSqry.FieldByName('Gqut4').AsString:=SGrid.Cells[ 5,List1];
      if SGrid.Cells[ 6,List1]<>'' then
      nSqry.FieldByName('Name1').AsString:=SGrid.Cells[ 6,List1];
      if SGrid.Cells[ 7,List1]<>'' then
      nSqry.FieldByName('Name2').AsString:=SGrid.Cells[ 7,List1];
      if SGrid.Cells[ 8,List1]<>'' then
      nSqry.FieldByName('Gname').AsString:=SGrid.Cells[ 8,List1];
      if SGrid.Cells[ 9,List1]<>'' then
      nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 9,List1];
      if SGrid.Cells[10,List1]<>'0' then
      nSqry.FieldByName('Gsqut').AsString:=SGrid.Cells[10,List1];
      if SGrid.Cells[11,List1]<>'0' then
      nSqry.FieldByName('Gssum').AsString:=SGrid.Cells[11,List1];
      if SGrid.Cells[13,List1]<>'0' then
      nSqry.FieldByName('Gqut5').AsString:=SGrid.Cells[13,List1];
      if SGrid.Cells[14,List1]<>'0' then
      nSqry.FieldByName('Gqut6').AsString:=SGrid.Cells[14,List1];
      if SGrid.Cells[15,List1]<>'0' then
      nSqry.FieldByName('Gqut7').AsString:=SGrid.Cells[15,List1];
      nSqry.FieldByName('Yesno').AsString:='0';
      if SGrid.Cells[12,List1]='1' then
      nSqry.FieldByName('Yesno').AsString:=SGrid.Cells[12,List1];
      nSqry.Post;
    end;
  end;

  nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
end;

procedure TSobo46.Edit101Change(Sender: TObject);
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

procedure TSobo46.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo46.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo46.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo46.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo46.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo46.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo46.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo46.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo46.Edit115KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo46.Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit101;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo46.Edit114KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo46.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo46.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo46.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo46.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo46.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo46.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo46.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo46.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo46.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo46.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text+'.01');
end;

procedure TSobo46.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=Copy(DateToStr(ADate),1,7);
end;

procedure TSobo46.Button701Click(Sender: TObject);
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

procedure TSobo46.Button702Click(Sender: TObject);
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

procedure TSobo46.RadioButton4Click(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    Bmark:=mSqry.GetBookmark; mSqry.DisableControls;
    mSqry.First;
    While mSqry.EOF=False do begin
      mSqry.Edit;
      mSqry.FieldByName('Yesno').AsString:='O';
      mSqry.Post;
      mSqry.Next;
    end;
    mSqry.GotoBookmark(Bmark); mSqry.FreeBookmark(Bmark); mSqry.EnableControls;
    mSqry.First;
  end;
end;

procedure TSobo46.RadioButton5Click(Sender: TObject);
begin
  if mSqry.Active=True Then begin
    Bmark:=mSqry.GetBookmark; mSqry.DisableControls;
    mSqry.First;
    While mSqry.EOF=False do begin
      mSqry.Edit;
      mSqry.FieldByName('Yesno').AsString:='N';
      mSqry.Post;
      mSqry.Next;
    end;
    mSqry.GotoBookmark(Bmark); mSqry.FreeBookmark(Bmark); mSqry.EnableControls;
    mSqry.First;
  end;
end;

procedure TSobo46.DBGrid101DrawColumnCell(Sender: TObject;
  const Rect: TRect; DataCol: Integer; Column: TColumnEh;
  State: TGridDrawState);
begin
  with (Sender as TDBGridEh) do begin
    if(DBGrid101.SelectedRows.CurrentRowSelected = False) then begin
      if(Column.FieldName='HCODE')or(Column.FieldName='HNAME')or
        (Column.FieldName='BNAME')or(Column.FieldName='GBIGO')or
        (Column.FieldName='GMEMO')or(Column.FieldName='BCODE')or
        (Column.FieldName='YESNO')then begin
        if DataSource.DataSet.RecNo mod 2 = 0
        then Canvas.Brush.Color := $00F8FFC6
        else Canvas.Brush.Color := clwhite;

        Canvas.Font.Color := Font.Color;
        DBGrid101.DefaultDrawColumnCell(Rect, DataCol, Column, State);
      end;
    end;
  end;
end;

end.
