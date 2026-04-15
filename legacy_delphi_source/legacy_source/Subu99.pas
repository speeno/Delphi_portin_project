unit Subu99;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, TFlatRadioButtonUnit,
  DBGridEh, DBClient, ToolEdit, dxCore, dxButtons;

type
  TSobo99 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel002: TFlatPanel;
    Panel003: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Panel001: TFlatPanel;
    Panel101: TFlatPanel;
    Edit101: TFlatMaskEdit;
    T3_Sub91: TClientDataSet;
    T3_Sub92: TClientDataSet;
    Button101: TFlatButton;
    Button201: TFlatButton;
    T3_Sub93: TClientDataSet;
    T3_Sub93SCODE: TStringField;
    T3_Sub93BCODE: TStringField;
    T3_Sub93BNAME: TStringField;
    T3_Sub93GCODE: TStringField;
    T3_Sub93GNAME: TStringField;
    T3_Sub93GIQUT: TFloatField;
    T3_Sub93GISUM: TFloatField;
    T3_Sub93GOQUT: TFloatField;
    T3_Sub93GOSUM: TFloatField;
    T3_Sub93GJQUT: TFloatField;
    T3_Sub93GJSUM: TFloatField;
    T3_Sub93GBQUT: TFloatField;
    T3_Sub93GBSUM: TFloatField;
    T3_Sub93GPQUT: TFloatField;
    T3_Sub93GPSUM: TFloatField;
    T3_Sub93GSUSU: TFloatField;
    T3_Sub93GSQUT: TFloatField;
    T3_Sub93GSSUM: TFloatField;
    T3_Sub93GSUMX: TFloatField;
    T3_Sub93GSUMY: TFloatField;
    Panel105: TFlatPanel;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
    Label101: TmyLabel3d;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    DBGrid101: TDBGridEh;
    Panel005: TFlatPanel;
    RadioButton1: TFlatRadioButton;
    RadioButton2: TFlatRadioButton;
    RadioButton3: TFlatRadioButton;
    Panel004: TFlatPanel;
    RadioButton4: TFlatRadioButton;
    RadioButton5: TFlatRadioButton;
    RadioButton6: TFlatRadioButton;
    RadioButton7: TFlatRadioButton;
    T3_Sub91GDATE: TStringField;
    T3_Sub91SCODE: TStringField;
    T3_Sub91GCODE: TStringField;
    T3_Sub91GNAME: TStringField;
    T3_Sub91HCODE: TStringField;
    T3_Sub91HNAME: TStringField;
    T3_Sub91GJEJA: TStringField;
    T3_Sub91JUBUN: TStringField;
    T3_Sub91GSQUT: TFloatField;
    T3_Sub91GQUT1: TFloatField;
    T3_Sub91GQUT2: TFloatField;
    T3_Sub91GQUT3: TFloatField;
    T3_Sub91GJISA: TStringField;
    T3_Sub92GDATE: TStringField;
    T3_Sub92SCODE: TStringField;
    T3_Sub92GCODE: TStringField;
    T3_Sub92GNAME: TStringField;
    T3_Sub92HCODE: TStringField;
    T3_Sub92HNAME: TStringField;
    T3_Sub92CODE5: TStringField;
    T3_Sub92GSQUT: TFloatField;
    DateEdit1: TDateEdit;
    Button701: TFlatButton;
    Button702: TFlatButton;
    Panel006: TFlatPanel;
    RadioButton8: TFlatRadioButton;
    RadioButton9: TFlatRadioButton;
    RadioButton0: TFlatRadioButton;
    Panel011: TFlatPanel;
    RadioButton12: TFlatRadioButton;
    RadioButton11: TFlatRadioButton;
    RadioButton13: TFlatRadioButton;
    Panel012: TFlatPanel;
    Panel013: TFlatPanel;
    Edit201: TFlatNumber;
    Edit202: TFlatNumber;
    Edit203: TFlatNumber;
    Edit204: TFlatNumber;
    myLabel3d1: TmyLabel3d;
    myLabel3d2: TmyLabel3d;
    myLabel3d3: TmyLabel3d;
    myLabel3d4: TmyLabel3d;
    Panel014: TFlatPanel;
    Edit301: TFlatNumber;
    Edit302: TFlatNumber;
    Edit303: TFlatNumber;
    Edit304: TFlatNumber;
    Panel015: TFlatPanel;
    Edit401: TFlatNumber;
    Edit402: TFlatNumber;
    Edit403: TFlatNumber;
    Edit404: TFlatNumber;
    Label300: TmyLabel3d;
    DBGrid201: TDBGridEh;
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
    procedure Button301Click(Sender: TObject);
    procedure Button401Click(Sender: TObject);
    procedure Button501Click(Sender: TObject);
    procedure Button509Click(Sender: TObject);
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
    procedure T3_Sub91AfterPost(DataSet: TDataSet);
    procedure T3_Sub91BeforePost(DataSet: TDataSet);
    procedure T3_Sub91BeforeClose(DataSet: TDataSet);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure Srart_39_01(Sender: TObject);
    procedure DBGrid201DrawColumnCell(Sender: TObject; const Rect: TRect;
      DataCol: Integer; Column: TColumnEh; State: TGridDrawState);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo99: TSobo99;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo99.FormActivate(Sender: TObject);
begin
  nForm:='99';
  nSqry:=T3_Sub91;
  mSqry:=T3_Sub92;
  tSqry:=Base10.T4_Sub81;
end;

procedure TSobo99.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo99.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo99:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Base10.OpenExit(tSqry);
end;

procedure TSobo99.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('39');
end;

procedure TSobo99.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('39');
end;

procedure TSobo99.Button010Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo99.Button011Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo99.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  nSqry.Filtered:=False;
  Base10.ColumnY0(oSqry,DBGrid201,ProgressBar1);
  nSqry.Filtered:=True;
end;

procedure TSobo99.Button013Click(Sender: TObject);
var St1: String;
begin
  St1:='';
  St1:=St1+'Gjeja'+'<>'+#39+'시내'+#39;
  St1:=St1+' and '+' Not'+'('+'Gname'+' like '+#39+'%'+'택배'+'%'+#39+')';
  St1:=St1+' and '+' Not'+'('+'Gname'+' like '+#39+'%'+'천일'+'%'+#39+')';

  nSqry.IndexName := '';
  oSqry:=nSqry;
  nSqry.Filter:=St1;
  nSqry.Filtered:=False;
  nSqry.Filtered:=True;
  Base10.ColumnY0(oSqry,DBGrid201,ProgressBar1);
  nSqry.Filtered:=True;
  nSqry.Filtered:=False;

  mSqry.Last;
  mSqry.First;

//oSqry:=mSqry;
//Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo99.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('39-01');
end;

procedure TSobo99.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('39-02');
end;

procedure TSobo99.Button016Click(Sender: TObject);
begin
  mSqry.First;
  While mSqry.EOF=False do begin
//if(mSqry.FieldByName('Code4').AsString='2')and
  if(mSqry.FieldByName('Code5').AsString='O')then begin
    Button501Click(Self);
    if tSqry.RecordCount > 0 then
    Tong40.print_99_01(Self);
    end;
    mSqry.Next;
  end;
end;

procedure TSobo99.Button017Click(Sender: TObject);
begin
  mSqry.First;
  While mSqry.EOF=False do begin
//if(mSqry.FieldByName('Code4').AsString='2')and
  if(mSqry.FieldByName('Code5').AsString='O')then begin
    Button501Click(Self);
    if tSqry.RecordCount > 0 then
    Tong40.Print_21_02(Self);
    end;
    mSqry.Next;
  end;
end;

procedure TSobo99.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button021Click(Sender: TObject);
begin
//Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo99.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button101Click(Sender: TObject);
var St1,St2,St3,St4,St8,St9: String;
begin
  //if Base10.Seek_Ggeo(Edit108.Text)='X' Then Exit;

  Base10.OpenShow(Base10.H2_Gbun);
  Sqlen := 'Select Hcode,Scode,Gcode,Gname,Jubun,Gdate From H2_Gbun Where '+D_Open;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.H2_Gbun)
  else ShowMessage(E_Open);

  Base10.OpenShow(Base10.T1_Gbun);
  Sqlen := 'Select Hcode,Gcode,Gjisa,Jubun,Gname From T1_Gbun Where '+D_Open;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.T1_Gbun)
  else ShowMessage(E_Open);

  Base10.OpenShow(Base10.T4_Ssub);
  Sqlen := 'Select Hcode,Gcode,Gdate,Gjisa,Jubun,Gqut1,Gqut2,Gqut3 From T4_Ssub '+
           'Where '+D_Select+'Gdate=''@Gdate'' ';
  Translate(Sqlen, '@Gdate', Edit101.Text);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.T4_Ssub)
  else ShowMessage(E_Open);


  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);

  Button509Click(Self);

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit101.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'Z'+#39;
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

  if RadioButton8.Checked=True Then begin
  St1:=St1+' and '+'Pubun'+'<>'+#39+'신간'+#39;
  end else
  if RadioButton9.Checked=True Then begin
  St1:=St1+' and '+'Pubun'+'= '+#39+'신간'+#39;
  end;

  St2:=' Group By Hcode,Gcode,Gjisa,Jubun';

  Sqlen := 'Select Hcode,Gcode,Gjisa,Jubun,Sum(Gsqut)as Gsqut From S1_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  nSqry.First;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    T08:=0;
    St4:='';
    St8:='';
    St9:='';

  { if nSqry.FieldByName('Gjisa').AsString<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
      Translate(Sqlen, '@Hcode', '');
      Translate(Sqlen, '@Scode', 'Z');
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Gname', Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4'));
      St8:=Base10.Seek_Name(Sqlen);
    end;
    if St8='지방물류' then St9:='2'; }

    if nSqry.FieldByName('Gjisa').AsString<>'' then begin
      if Copy(nSqry.FieldByName('Gcode').AsString,1,1)<>'9' then
      if Base10.H2_Gbun.Locate('Hcode;Scode;Gcode;Gname;Jubun',VarArrayOf(['','Z',nSqry.FieldByName('Gcode').AsString,
      Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'),Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4')]),[loCaseInsensitive])=true then
        St8:=Base10.H2_Gbun.FieldByName('Gdate').AsString;
      if Copy(nSqry.FieldByName('Gcode').AsString,1,1)='9' then
      if Base10.H2_Gbun.Locate('Hcode;Scode;Gcode;Gname;Jubun',VarArrayOf([nSqry.FieldByName('Gcode').AsString,'Z',nSqry.FieldByName('Gcode').AsString,
      Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'),Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4')]),[loCaseInsensitive])=true then
        St8:=Base10.H2_Gbun.FieldByName('Gdate').AsString;
    end;
    if St8='지방물류' then St9:='2';

  { if St9='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then begin
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end;
    if St9='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then begin
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end; }

    if RadioButton11.Checked=True Then St9:='';
    if RadioButton13.Checked=True Then begin
      if St9='' then
      St9:='2' else
      St9:=''
    end;

   if St9<>'' then begin
    nSqry.Delete;
   end else begin
    nSqry.Edit;

    //-----셋트수량-----//
    T06:=0;
    T07:=0;
    T08:=0;
    RBand:=0;
    While YGrid.RowCount-1 > RBand do begin
    RBand:=RBand+1;
      if(YGrid.Cells[ 0,RBand]=nSqry.FieldByName('Hcode').AsString)and
        (YGrid.Cells[ 1,RBand]=nSqry.FieldByName('Gcode').AsString)and
        (YGrid.Cells[ 2,RBand]=nSqry.FieldByName('Gjisa').AsString)and
        (YGrid.Cells[ 3,RBand]=nSqry.FieldByName('Jubun').AsString)then begin
      T06:=StrToIntDef(YGrid.Cells[ 5,RBand],0)-1;
      T07:=StrToIntDef(YGrid.Cells[ 6,RBand],0);
      T08:=T08+T06*T07;
      end;
    end;
    nSqry.FieldByName('Gsqut').AsFloat:=nSqry.FieldByName('Gsqut').AsFloat+T08;
    //-----셋트수량-----//

    nSqry.FieldByName('Gdate').Value:=Edit101.Text;

    if Base10.G7_Ggeo.Locate('Gcode',nSqry.FieldByName('Hcode').AsString,[loCaseInsensitive])=true then
    nSqry.FieldByName('Hname').AsString:=Base10.G7_Ggeo.FieldByName('Gname').AsString;

  { if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Gname').AsString='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString; }

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

    if nSqry.FieldByName('Gname').Value='' then begin
    Sqlen := 'Select Gname From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
    end;

    if nSqry.FieldByName('Gjisa').AsString<>'' then
    nSqry.FieldByName('Gname').AsString:=Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'2')+
    nSqry.FieldByName('Gname').AsString+ Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'1');

  { Sqlen := 'Select Gname From T1_Gbun Where '+D_Select+
             'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun''';
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Gjisa', Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'));
    Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4'));
    St4:=Base10.Seek_Name(Sqlen);

    if St4='' then
    if nSqry.FieldByName('Gjisa').AsString<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
      Translate(Sqlen, '@Hcode', '');
      Translate(Sqlen, '@Scode', 'Z');
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Gname', Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4'));
      St4:=Base10.Seek_Name(Sqlen);
    end; }

    if Base10.G7_Ggeo.Locate('Gcode',nSqry.FieldByName('Hcode').AsString,[loCaseInsensitive])=true then begin
      if Base10.G7_Ggeo.FieldByName('Yes35').AsString='2' then begin
        if Base10.T1_Gbun.Locate('Hcode;Gcode;Gjisa;Jubun',VarArrayOf(['',nSqry.FieldByName('Gcode').AsString,
        Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'),Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4')]),[loCaseInsensitive])=true then begin
          St4:=Base10.T1_Gbun.FieldByName('Gname').AsString;
        end;
      end;
    end;

    if St4='' then
    if Base10.T1_Gbun.Locate('Hcode;Gcode;Gjisa;Jubun',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString,
    Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'),Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4')]),[loCaseInsensitive])=true then begin
      St4:=Base10.T1_Gbun.FieldByName('Gname').AsString;
    end;

    if St4='' then
    if nSqry.FieldByName('Gjisa').AsString<>'' then begin
      if Copy(nSqry.FieldByName('Gcode').AsString,1,1)<>'9' then
      if Base10.H2_Gbun.Locate('Hcode;Scode;Gcode;Gname;Jubun',VarArrayOf(['','Z',nSqry.FieldByName('Gcode').AsString,
      Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'),Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4')]),[loCaseInsensitive])=true then
        St4:=Base10.H2_Gbun.FieldByName('Gdate').AsString;
      if Copy(nSqry.FieldByName('Gcode').AsString,1,1)='9' then
      if Base10.H2_Gbun.Locate('Hcode;Scode;Gcode;Gname;Jubun',VarArrayOf([nSqry.FieldByName('Hcode').AsString,'Z',nSqry.FieldByName('Gcode').AsString,
      Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'),Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4')]),[loCaseInsensitive])=true then
        St4:=Base10.H2_Gbun.FieldByName('Gdate').AsString;
    end;

    if St4='' then begin
    { if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then begin
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
      end;

      if St4='' then
      if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then begin
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
      end; }

      if St4='' then begin
      Sqlen := 'Select Gubun From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Hcode', '');
      if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
      end;

      if St4='' then begin
      Sqlen := 'Select Gubun From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
      end;
    end;

    if St4='시내' then begin
      nSqry.FieldByName('Gjeja').AsString:='시내';
    end else begin
      nSqry.FieldByName('Gjeja').AsString:='지방';
    end;

  { Sqlen :=
    'Select Gqut1,Gqut2,Gqut3 From T4_Ssub Where '+D_Select+
    'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun'' ';
    Translate(Sqlen, '@Hcode', T3_Sub91Hcode.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub91Gcode.AsString);
    Translate(Sqlen, '@Gdate', T3_Sub91Gdate.AsString);
    Translate(Sqlen, '@Gjisa', T3_Sub91Gjisa.AsString);
    Translate(Sqlen, '@Jubun', T3_Sub91Jubun.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      nSqry.FieldByName('Gqut1').AsString:=Base10.Socket.GetData(1, 1);;
      nSqry.FieldByName('Gqut2').AsString:=Base10.Socket.GetData(1, 2);;
      nSqry.FieldByName('Gqut3').AsString:=Base10.Socket.GetData(1, 3);;
    end else begin
      nSqry.FieldByName('Gqut1').AsString:='1';
      nSqry.FieldByName('Gqut2').AsString:='2';
    end; }

    if Base10.T4_Ssub.Locate('Hcode;Gcode;Gdate;Gjisa;Jubun',VarArrayOf(['z'+T3_Sub91Hcode.AsString,T3_Sub91Gcode.AsString,
    T3_Sub91Gdate.AsString,T3_Sub91Gjisa.AsString,T3_Sub91Jubun.AsString]),[loCaseInsensitive])=true then begin
      nSqry.FieldByName('Gqut1').AsString:=Base10.T4_Ssub.FieldByName('Gqut1').AsString;
      nSqry.FieldByName('Gqut2').AsString:=Base10.T4_Ssub.FieldByName('Gqut2').AsString;
      nSqry.FieldByName('Gqut3').AsString:=Base10.T4_Ssub.FieldByName('Gqut3').AsString;
    end else begin
      nSqry.FieldByName('Gqut1').AsString:='1';
      nSqry.FieldByName('Gqut2').AsString:='2';
    end;

    nSqry.Post;
    nSqry.Next;
   end;
  end;

  Button201Click(Self);

  nSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=T3_Sub91BeforePost;

  Tong40.Hide;
{ Tong40.Free; }

end;

procedure TSobo99.Button201Click(Sender: TObject);
var St1,St2,St3,St4,St5: String;
begin
  nSqry.First;
  mSqry.First;
  While nSqry.EOF=False do begin
    St1:=nSqry.FieldByName('Hcode').AsString;
    St2:='';
    if mSqry.Locate('Hcode;Gcode',VarArrayOf([St1,St2]),[loCaseInsensitive])=False then begin
      mSqry.Append;
      mSqry.FieldByName('Hcode').AsString:=St1;
      mSqry.FieldByName('Gcode').AsString:=St2;
      mSqry.FieldByName('Code5').AsString:='N';
      mSqry.FieldByName('Gdate').AsString:=nSqry.FieldByName('Gdate').AsString;
      mSqry.FieldByName('Hname').AsString:=nSqry.FieldByName('Hname').AsString;
      mSqry.Post;
    end;
    nSqry.Next;
  end;
  nSqry.First;
  mSqry.First;
end;

procedure TSobo99.Button301Click(Sender: TObject);
begin
//
end;

procedure TSobo99.Button401Click(Sender: TObject);
begin
  if RadioButton6.Checked=True Then begin
  //Timer1.Enabled:=True;
  end else
  if RadioButton7.Checked=True Then begin
  //Timer1.Enabled:=False;
  end else begin
  //Timer1.Enabled:=False;
    if mSqry.Active=True Then begin
      Bmark:=mSqry.GetBookmark; mSqry.DisableControls;
      mSqry.First;
      While mSqry.EOF=False do begin
        mSqry.Edit;
        if RadioButton4.Checked=True Then
        mSqry.FieldByName('Code5').AsString:='O';
        if RadioButton5.Checked=True Then
        mSqry.FieldByName('Code5').AsString:='N';
        mSqry.Post;
        mSqry.Next;
      end;
      mSqry.GotoBookmark(Bmark); mSqry.FreeBookmark(Bmark); mSqry.EnableControls;
      mSqry.First;
    end;
  end;
end;

procedure TSobo99.Button501Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6,St8,St9: String;
    I1,I2,I3: integer;
    SearchRec : TSearchRec;
    ff1,ff2: Integer;
begin
  Base10.OpenShow(tSqry);

//Button509Click(Self);

  St1:='Gdate'+' ='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'Z'+#39;

  if RadioButton1.Checked=True Then
  St1:=St1+' and '+'Yesno'+'='+#39+'1'+#39;
  if RadioButton2.Checked=True Then
  St1:=St1+' and '+'Yesno'+'='+#39+'2'+#39;

  if RadioButton8.Checked=True Then begin
  St1:=St1+' and '+'Pubun'+'<>'+#39+'신간'+#39;
  end else
  if RadioButton9.Checked=True Then begin
  St1:=St1+' and '+'Pubun'+'= '+#39+'신간'+#39;
  end;

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
    St8:='';

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
        if Base10.T1_Gbun.Locate('Hcode;Gcode;Gjisa;Jubun',VarArrayOf(['',SGrid.Cells[ 0,List1],
        Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'),Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4')]),[loCaseInsensitive])=true then begin
          St4:=Base10.T1_Gbun.FieldByName('Gname').AsString;
          St9:=Base10.T1_Gbun.FieldByName('Bebon').AsString;
        end;
      end;
    end;

    if St4='' then
    if Base10.T1_Gbun.Locate('Hcode;Gcode;Gjisa;Jubun',VarArrayOf(['',SGrid.Cells[ 0,List1],
    Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'3'),Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'4')]),[loCaseInsensitive])=true then begin
      St4:=Base10.T1_Gbun.FieldByName('Gname').AsString;
      St9:=Base10.T1_Gbun.FieldByName('Bebon').AsString;
    end;
  { Sqlen := 'Select Gname,Bebon From T1_Gbun Where '+D_Select+
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
    end; }

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
      St8:=Base10.Seek_Name(Sqlen);
    end;
    if St8='지방물류' then St9:='2';

  { if St9='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end;
    if St9='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Hcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end; }

    if RadioButton11.Checked=True Then St9:='';
    if RadioButton13.Checked=True Then begin
      if St9='' then
      St9:='2' else
      St9:=''
    end;

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
      if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
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
      Translate(Sqlen, '@Hcode', 'z'+mSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gdate', mSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gjisa', SGrid.Cells[ 1,List1]);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        if Base10.Socket.GetData(1, 1)='' then
        tSqry.FieldByName('Gqut1').AsString:='1' else
        tSqry.FieldByName('Gqut1').AsString:=Base10.Socket.GetData(1, 1);
      end;

      tSqry.FieldByName('Gcode').AsString:=St3;
      tSqry.FieldByName('Gname').AsString:=St5;
      tSqry.FieldByName('GsumX').AsFloat :=T01;
      T04:=T04+T01;
    end else begin
      Sqlen :=
      'Select Sum(Gqut1)as Gqut1,Sum(Gqut2)as Gqut2,Sum(Gqut3)as Gqut3 From T4_Ssub Where '+D_Select+
      'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' ';
      Translate(Sqlen, '@Hcode', 'z'+mSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gdate', mSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gjisa', SGrid.Cells[ 1,List1]);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        if Base10.Socket.GetData(1, 1)='' then
        tSqry.FieldByName('Gqut2').AsString:='1' else
        tSqry.FieldByName('Gqut2').AsString:=Base10.Socket.GetData(1, 1);
      end;

      tSqry.FieldByName('Hcode').AsString:=St3;
      tSqry.FieldByName('Hname').AsString:=St5;
      tSqry.FieldByName('GsumY').AsFloat :=T01;
      T05:=T05+T01;
    end;
    tSqry.Post;

   end;

  end;

  ff1 := FindFirst( GetExecPath + 'Report\Report_3_91.frf', faAnyFile, SearchRec);
  ff2 := FindFirst( GetExecPath + 'Report\Report_3_92.frf', faAnyFile, SearchRec);

  if(ff1 = 0)then begin
    I2:=tSqry.RecordCount;
    I3:=I2-(I2 div 25)*25;

    for I1 := I3 to 25-1 do begin
      tSqry.Append;
      tSqry.Post;
    end;
  end;
end;

procedure TSobo99.Button509Click(Sender: TObject);
var St1,St2,St3,St4,St8,St9: String;
begin

  St1:='S.Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'S.Gdate'+'<='+#39+Edit101.Text+#39+' and '+
       'S.Gubun'+' ='+#39+'출고'+#39+' and '+
       'S.Ocode'+' ='+#39+'B'+#39+' and '+
       'S.Scode'+' ='+#39+'Z'+#39;
  if (Edit104.Text<>'') Then
  St1:=St1+' and '+
       'S.Hcode'+'>='+#39+Edit102.Text+#39+' and '+
       'S.Hcode'+'<='+#39+Edit104.Text+#39;

  if S_Where0<>'' then
  St1:=St1+' and '+S_Where0;

  if RadioButton1.Checked=True Then
  St1:=St1+' and '+'S.Yesno'+'='+#39+'1'+#39;
  if RadioButton2.Checked=True Then
  St1:=St1+' and '+'S.Yesno'+'='+#39+'2'+#39;

  if RadioButton8.Checked=True Then begin
  St1:=St1+' and '+'S.Pubun'+'<>'+#39+'신간'+#39;
  end else
  if RadioButton9.Checked=True Then begin
  St1:=St1+' and '+'S.Pubun'+'= '+#39+'신간'+#39;
  end;

  if D_Select<>'' then
  St1:=St1+' and '+'('+'S.Check is null '+' or '+'S.Check'+'<>'+#39+'D'+#39+')';

  if D_Select<>'' then
  St1:=St1+' and '+'('+'Y.Check is null '+' or '+'Y.Check'+'<>'+#39+'D'+#39+')';

  St1:=St1+' and '+'Y.Grat8'+'> '+'1';

  Sqlen := 'Select S.Hcode,S.Gcode,S.Gjisa,S.Jubun,S.Bcode,Y.Grat8,S.Gsqut From S1_Ssub S, G4_Book Y '+
           'Where S.Hcode=Y.Hcode and S.Bcode=Y.Gcode and '+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(YGrid)
  else ShowMessage(E_Open);

end;

procedure TSobo99.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
end;

procedure TSobo99.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo99.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo99.Edit102KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then DBGrid101.SetFocus;
end;

procedure TSobo99.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then DBGrid101.SetFocus;
end;

procedure TSobo99.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo99.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo99.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo99.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo99.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo99.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo99.Edit114KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo99.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo99.DBGrid101Enter(Sender: TObject);
begin
//
end;

procedure TSobo99.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo99.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo99.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo99.DBGrid201KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid201.SelectedIndex;
  sColumn:=DBGrid201.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=5 Then begin
       nSqry.Edit;
       nSqry.FieldByName('Gqut2').Value:= nSqry.FieldByName('Gqut1').Value*2;
       nSqry.Post;
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end;
end;

procedure TSobo99.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid201.SelectedIndex;
  sColumn:=DBGrid201.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    if SIndexs=5 Then begin
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),0,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),KEYEVENTF_KEYUP,0);
    end;
    if SIndexs=6 Then begin
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),0,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),KEYEVENTF_KEYUP,0);
    end;
    if SIndexs=7 Then begin
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),0,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),KEYEVENTF_KEYUP,0);
    end;
  end;
  end;
end;

procedure TSobo99.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(mSqry,Column);
end;

procedure TSobo99.DBGrid201TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo99.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo99.DataSource2DataChange(Sender: TObject; Field: TField);
var St1: String;
begin
  St1:='';
  St1:=St1+'Hcode'+'='+#39+mSqry.FieldByName('Hcode').AsString+#39;
  nSqry.Filter:=St1;
  nSqry.Filtered:=True;
  nSqry.IndexName := 'IDX'+'GJEJA'+'UP';
  nSqry.IndexName := 'IDX'+'GJEJA'+'DOWN';
  Srart_39_01(Self);
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo99.T3_Sub91AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TSobo99.T3_Sub91BeforePost(DataSet: TDataSet);
begin

    Sqlen :=
    'Select * From T4_Ssub Where '+D_Select+
    'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun'' ';
    Translate(Sqlen, '@Hcode', 'z'+T3_Sub91Hcode.AsString);
    Translate(Sqlen, '@Gcode', T3_Sub91Gcode.AsString);
    Translate(Sqlen, '@Gdate', T3_Sub91Gdate.AsString);
    Translate(Sqlen, '@Gjisa', T3_Sub91Gjisa.AsString);
    Translate(Sqlen, '@Jubun', T3_Sub91Jubun.AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin

      Sqlen := 'UPDATE T4_Ssub SET Gqut1= @Gqut1 ,Gqut2= @Gqut2 ,Gqut3= @Gqut3 WHERE '+
      'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun''';

      Translate(Sqlen, '@Hcode', 'z'+T3_Sub91Hcode.AsString);
      Translate(Sqlen, '@Gcode', T3_Sub91Gcode.AsString);
      Translate(Sqlen, '@Gdate', T3_Sub91Gdate.AsString);
      Translate(Sqlen, '@Gjisa', T3_Sub91Gjisa.AsString);
      Translate(Sqlen, '@Jubun', T3_Sub91Jubun.AsString);
      TransAuto(Sqlen, '@Gqut1', T3_Sub91Gqut1.AsString);
      TransAuto(Sqlen, '@Gqut2', T3_Sub91Gqut2.AsString);
      TransAuto(Sqlen, '@Gqut3', T3_Sub91Gqut3.AsString);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end else begin

      Sqlen := 'INSERT INTO T4_Ssub '+
      '(Hcode, Gcode, Gdate, Gjisa, Jubun, Gqut1, Gqut2, Gqut3) VALUES '+
      '(''@Hcode'',''@Gcode'',''@Gdate'',''@Gjisa'',''@Jubun'', @Gqut1 , @Gqut2 , @Gqut3 )';

      Translate(Sqlen, '@Hcode', 'z'+T3_Sub91Hcode.AsString);
      Translate(Sqlen, '@Gcode', T3_Sub91Gcode.AsString);
      Translate(Sqlen, '@Gdate', T3_Sub91Gdate.AsString);
      Translate(Sqlen, '@Gjisa', T3_Sub91Gjisa.AsString);
      Translate(Sqlen, '@Jubun', T3_Sub91Jubun.AsString);
      TransAuto(Sqlen, '@Gqut1', T3_Sub91Gqut1.AsString);
      TransAuto(Sqlen, '@Gqut2', T3_Sub91Gqut2.AsString);
      TransAuto(Sqlen, '@Gqut3', T3_Sub91Gqut3.AsString);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    //Base10.Update_ID(nSqry,'T4_SSUB91_ID_GEN');

    end;

end;

procedure TSobo99.T3_Sub91BeforeClose(DataSet: TDataSet);
begin
  With T3_Sub91 do
  if(State in dsEditModes)Then Post;
end;

procedure TSobo99.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo99.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo99.Button701Click(Sender: TObject);
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

procedure TSobo99.Button702Click(Sender: TObject);
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

procedure TSobo99.Srart_39_01(Sender: TObject);
begin
  Screen.Cursor:=crHourGlass;
  T01:=0; T02:=0; T03:=0; T04:=0; T05:=0; T06:=0; T07:=0; T08:=0; T09:=0;
  Edit201.Value:=0;
  Edit202.Value:=0;
  Edit203.Value:=0;
  Edit204.Value:=0;
  Edit301.Value:=0;
  Edit302.Value:=0;
  Edit303.Value:=0;
  Edit304.Value:=0;
  Edit401.Value:=0;
  Edit402.Value:=0;
  Edit403.Value:=0;
  Edit404.Value:=0;
  if nSqry.Active=True Then begin
     oSqry:=nSqry; Bmark:=oSqry.GetBookmark; oSqry.DisableControls;
     oSqry.First;
     While oSqry.EOF=False do begin
       if oSqry.FieldByName('Gjeja').AsString='시내' then begin
       T01:=T01+oSqry.FieldByName('Gsqut').AsFloat;
       T02:=T02+oSqry.FieldByName('Gqut1').AsFloat;
       T03:=T03+oSqry.FieldByName('Gqut2').AsFloat;
       T04:=T04+oSqry.FieldByName('Gqut3').AsFloat;
       end else begin
       T05:=T05+oSqry.FieldByName('Gsqut').AsFloat;
       T06:=T06+oSqry.FieldByName('Gqut1').AsFloat;
       T07:=T07+oSqry.FieldByName('Gqut2').AsFloat;
       T08:=T08+oSqry.FieldByName('Gqut3').AsFloat;
       end;
       oSqry.Next;
     end;
     Edit201.Value:=T01;
     Edit202.Value:=T02;
     Edit203.Value:=T03;
     Edit204.Value:=T04;
     Edit301.Value:=T05;
     Edit302.Value:=T06;
     Edit303.Value:=T07;
     Edit304.Value:=T08;
     Edit401.Value:=T01+T05;
     Edit402.Value:=T02+T06;
     Edit403.Value:=T03+T07;
     Edit404.Value:=T04+T08;
     oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  end;
{ Sobo99.StBar201.Panels.Items[2].Text:=FormatFloat('###,###,##0',T01);
  Sobo99.StBar201.Panels.Items[3].Text:=FormatFloat('###,###,##0',T02);
  Sobo99.StBar201.Panels.Items[4].Text:=FormatFloat('###,###,##0',T03);
  Sobo99.StBar201.Panels.Items[5].Text:=FormatFloat('###,###,##0',T04); }
  Screen.Cursor:=crDefault;
end;

procedure TSobo99.DBGrid201DrawColumnCell(Sender: TObject;
  const Rect: TRect; DataCol: Integer; Column: TColumnEh;
  State: TGridDrawState);
begin
  with (Sender as TDBGridEh) do begin
    if(DBGrid201.SelectedRows.CurrentRowSelected = False) then begin
      if(Column.FieldName='GCODE')or(Column.FieldName='GNAME')or
        (Column.FieldName='JUBUN')or(Column.FieldName='GJEJA')then begin
      //(Column.FieldName='CODE2')or(Column.FieldName='CODE3')or
      //(Column.FieldName='CODE4')or(Column.FieldName='CODE1')then begin
        if Column.Grid.Fields[3].AsString='지방'
        then Canvas.Brush.Color := $00F8FFC6
        else Canvas.Brush.Color := clwhite;

        Canvas.Font.Color := Font.Color;
        DBGrid201.DefaultDrawColumnCell(Rect, DataCol, Column, State);
      end;
    end;
  end;
end;

end.
