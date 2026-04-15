unit Subu28;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, TFlatRadioButtonUnit,
  DBGridEh, ToolEdit, DBClient, dxCore, dxButtons, ComObj;

type
  TSobo28 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    Panel101: TFlatPanel;
    Panel102: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Button201: TFlatButton;
    StBar101: TStatusBar;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    DBGrid101: TDBGridEh;
    Label101: TmyLabel3d;
    Panel003: TFlatPanel;
    RadioButton1: TFlatRadioButton;
    RadioButton2: TFlatRadioButton;
    RadioButton3: TFlatRadioButton;
    Panel004: TFlatPanel;
    RadioButton4: TFlatRadioButton;
    RadioButton5: TFlatRadioButton;
    RadioButton6: TFlatRadioButton;
    RadioButton7: TFlatRadioButton;
    DateEdit1: TDateEdit;
    Button701: TFlatButton;
    Button702: TFlatButton;
    Panel005: TFlatPanel;
    RadioButton8: TFlatRadioButton;
    RadioButton9: TFlatRadioButton;
    RadioButton0: TFlatRadioButton;
    FlatPanel1: TFlatPanel;
    Edit203: TFlatEdit;
    Edit204: TFlatEdit;
    Panel203: TFlatPanel;
    T2_Sub81: TClientDataSet;
    T2_Sub81ID: TFloatField;
    T2_Sub81GCODE: TStringField;
    T2_Sub81GNAME: TStringField;
    T2_Sub81HCODE: TStringField;
    T2_Sub81HNAME: TStringField;
    T2_Sub81GTELS: TStringField;
    T2_Sub81GQUT1: TFloatField;
    T2_Sub81GQUT2: TFloatField;
    T2_Sub81CODE5: TStringField;
    T2_Sub82: TClientDataSet;
    T2_Sub81JUBUN: TStringField;
    Edit205: TFlatEdit;
    Edit206: TFlatEdit;
    Edit207: TFlatEdit;
    StaticText1: TStaticText;
    StaticText2: TStaticText;
    StaticText3: TStaticText;
    T2_Sub81GJISA: TStringField;
    dxButton1: TdxButton;
    T2_Sub81GPOSA: TStringField;
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
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101TitleClick(Column: TColumnEh);
    procedure DBGrid201TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure DBGrid101DblClick(Sender: TObject);
    procedure DBGrid101DrawColumnCell(Sender: TObject; const Rect: TRect;
      DataCol: Integer; Column: TColumnEh; State: TGridDrawState);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure Edit205Click(Sender: TObject);
    procedure Edit205Exit(Sender: TObject);
    procedure StaticText1Click(Sender: TObject);
    procedure StaticText2Click(Sender: TObject);
    procedure StaticText3Click(Sender: TObject);
    procedure ColumnX1(TableX: TClientDataSet);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo28: TSobo28;

implementation

{$R *.DFM}

uses Chul, Base01, Tong01, Tong02, Tong04, TcpLib, Subu21,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo28.FormActivate(Sender: TObject);
begin
  nForm:='28';
  nSqry:=T2_Sub81;
  mSqry:=T2_Sub82;
end;

procedure TSobo28.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit101.SetFocus;
end;

procedure TSobo28.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo28:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo28.Button001Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end; }
end;

procedure TSobo28.Button002Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_27_01(Self);
  end; }
end;

procedure TSobo28.Button003Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo28.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button008Click(Sender: TObject);
begin
  Tong20.Zoom_Int_01('27');
end;

procedure TSobo28.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('27');
end;

procedure TSobo28.Button010Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo28.Button011Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo28.Button012Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    oSqry:=nSqry;
    ColumnX1(oSqry);
  end;
end;

procedure TSobo28.Button013Click(Sender: TObject);
begin
{ oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1); }
end;

procedure TSobo28.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('27-01');
end;

procedure TSobo28.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('27-02');
end;

procedure TSobo28.Button016Click(Sender: TObject);
begin
  nSqry.First;
  While nSqry.EOF=False do begin
    if(nSqry.FieldByName('Code5').AsString='O')then
    Tong40.PrinTing00('32','2','','','','','','','','');
    nSqry.Next;
  end;
end;

procedure TSobo28.Button017Click(Sender: TObject);
begin
  nSqry.First;
  While nSqry.EOF=False do begin
    if(nSqry.FieldByName('Code5').AsString='O')then
    Tong40.PrinTing00('32','1','','','','','','','','');
    nSqry.Next;
  end;
end;

procedure TSobo28.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button021Click(Sender: TObject);
begin
//Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo28.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button101Click(Sender: TObject);
var St1,St2,St3: String;
begin
//if Base10.Seek_Ggeo(Edit108.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;
  Base10.OpenShow(nSqry);
//Base10.OpenShow(mSqry);

  St1:='';
  St1:='S.Gdate'+' ='+#39+Edit101.Text+#39+' and '+
       'S.Gubun'+' ='+#39+'출고'+#39+' and '+
       'S.Yesno'+' ='+#39+'2'+#39+' and '+
       'S.Ocode'+' ='+#39+'B'+#39+' and '+
       'S.Scode'+' ='+#39+'X'+#39;

  if (Edit104.Text<>'') Then
  St1:=St1+' and '+
       'S.Hcode'+'>='+#39+Edit102.Text+#39+' and '+
       'S.Hcode'+'<='+#39+Edit104.Text+#39;

  if S_Where0<>'' then
  St1:=St1+' and '+S_Where0;

  if Base10.G7_Ggeo.Locate('Gcode;Hcode',VarArrayOf([Edit104.Text,'pintx']),[loCaseInsensitive])=false then begin
//if(Base10.Database.Database='book_02_db')or
  if(Base10.Database.Database='chul_03_db')then
  St1:=St1+' and '+'('+
       'Y.Gname'+' Like '+#39+'%'+'택배'+'%'+#39+' or '+
       'Y.Gname'+' Like '+#39+'%'+'택배'+'%'+#39+')'
  else
  St1:=St1+' and '+'('+
       'Y.Gname'+' Like '+#39+'%'+'-택배'+'%'+#39+' or '+
       'Y.Gname'+' Like '+#39+'%'+'-택배'+'%'+#39+')';
  end;     

  St2:=St1+' and '+'('+'Y.Gcode'+' < '+#39+'9'+#39+')';

  if D_Select<>'' then
  St2:=St2+' and '+'('+'S.Check is null '+' or '+'S.Check'+'<>'+#39+'D'+#39+')';

  if D_Select<>'' then
  St2:=St2+' and '+'('+'Y.Check is null '+' or '+'Y.Check'+'<>'+#39+'D'+#39+')';

  Sqlen := 'Select S.Gdate,S.Hcode,S.Gcode,S.Jubun,S.Gjisa,Y.Gname,Y.Gtel1,Y.Gtel2,Sum(S.Gsqut),Sum(S.Gssum) '+
           'From S1_Ssub S, G1_Ggeo Y '+
           'Where S.Gcode=Y.Gcode and '+St2;

  Sqlen := Sqlen+' Group by S.Gdate,S.Hcode,S.Gcode,S.Jubun,S.Gjisa,Y.Gname,Y.Gtel1,Y.Gtel2';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    nSqry.Append;
    nSqry.FieldByName('Code5').AsString:='N';
    nSqry.FieldByName('Hcode').AsString:=SGrid.Cells[ 1,List1];
    nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 2,List1];
    nSqry.FieldByName('Jubun').AsString:=SGrid.Cells[ 3,List1];
    nSqry.FieldByName('Gjisa').AsString:=SGrid.Cells[ 4,List1];
    nSqry.FieldByName('Gname').AsString:=SGrid.Cells[ 5,List1];
    nSqry.FieldByName('Gtels').AsString:=SGrid.Cells[ 6,List1]+'-'+SGrid.Cells[ 7,List1];
    nSqry.FieldByName('Gqut1').AsString:=SGrid.Cells[ 8,List1];
    nSqry.FieldByName('Gqut2').AsString:='1';

    if SGrid.Cells[ 4,List1]<>'' then
    nSqry.FieldByName('Gname').AsString:=Base10.Seek_Jisa(SGrid.Cells[ 4,List1],'2')+
    nSqry.FieldByName('Gname').AsString+ Base10.Seek_Jisa(SGrid.Cells[ 4,List1],'1');

    Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
    nSqry.FieldByName('Hname').Value:=Base10.Seek_Name(Sqlen);

    Button301Click(Self);
    if Edit207.Text<>'' then
    nSqry.FieldByName('Gposa').AsString:=Edit207.Text;
    if Edit206.Text<>'' then
    nSqry.FieldByName('Gtels').AsString:=Edit206.Text;
    if(Edit206.Text='')and(Edit205.Text<>'')then
    nSqry.FieldByName('Gtels').AsString:=Edit205.Text;

    nSqry.Post;
  end;

  St2:=St1+' and '+'('+'Y.Gcode'+' >= '+#39+'9'+#39+')';

  if D_Select<>'' then
  St2:=St2+' and '+'('+'S.Check is null '+' or '+'S.Check'+'<>'+#39+'D'+#39+')';

  if D_Select<>'' then
  St2:=St2+' and '+'('+'Y.Check is null '+' or '+'Y.Check'+'<>'+#39+'D'+#39+')';

  Sqlen := 'Select S.Gdate,S.Hcode,S.Gcode,S.Jubun,S.Gjisa,Y.Gname,Y.Gtel1,Y.Gtel2,Sum(S.Gsqut),Sum(S.Gssum) '+
           'From S1_Ssub S, G1_Ggeo Y '+
           'Where S.Hcode=Y.Hcode and S.Gcode=Y.Gcode and '+St2;

  Sqlen := Sqlen+' Group by S.Gdate,S.Hcode,S.Gcode,S.Jubun,S.Gjisa,Y.Gname,Y.Gtel1,Y.Gtel2';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    nSqry.Append;
    nSqry.FieldByName('Code5').AsString:='N';
    nSqry.FieldByName('Hcode').AsString:=SGrid.Cells[ 1,List1];
    nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 2,List1];
    nSqry.FieldByName('Jubun').AsString:=SGrid.Cells[ 3,List1];
    nSqry.FieldByName('Gjisa').AsString:=SGrid.Cells[ 4,List1];
    nSqry.FieldByName('Gname').AsString:=SGrid.Cells[ 5,List1];
    nSqry.FieldByName('Gtels').AsString:=SGrid.Cells[ 6,List1]+'-'+SGrid.Cells[ 7,List1];
    nSqry.FieldByName('Gqut1').AsString:=SGrid.Cells[ 8,List1];
    nSqry.FieldByName('Gqut2').AsString:='1';

    if SGrid.Cells[ 4,List1]<>'' then
    nSqry.FieldByName('Gname').AsString:=Base10.Seek_Jisa(SGrid.Cells[ 4,List1],'2')+
    nSqry.FieldByName('Gname').AsString+ Base10.Seek_Jisa(SGrid.Cells[ 4,List1],'1');

    Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
    nSqry.FieldByName('Hname').Value:=Base10.Seek_Name(Sqlen);

    Button301Click(Self);
    if Edit207.Text<>'' then
    nSqry.FieldByName('Gposa').AsString:=Edit207.Text;
    if Edit206.Text<>'' then
    nSqry.FieldByName('Gtels').AsString:=Edit206.Text;
    if(Edit206.Text='')and(Edit205.Text<>'')then
    nSqry.FieldByName('Gtels').AsString:=Edit205.Text;

    nSqry.Post;
  end;

  nSqry.IndexName := 'IDX'+'HCODE'+'DOWN';
  nSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo28.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button301Click(Sender: TObject);
begin
  if Edit203.Visible=True then begin

    Edit203.Text:='';
    Edit204.Text:='';
    Edit205.Text:='';
    Edit206.Text:='';
    Edit207.Text:='';

    Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where '+D_Select+
             'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
             'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
             'Scode=''@Scode'' and Hcode=''@Hcode'' and '+
             'Gjisa=''@Gjisa'' and '+
             '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';
    Translate(Sqlen, '@Gdate', Edit101.Text);
    Translate(Sqlen, '@Gubun', '출고');
    Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Scode', 'X');
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
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
    end;

    Edit205Exit(Self);
  end;
end;

procedure TSobo28.Button401Click(Sender: TObject);
begin
    if nSqry.Active=True Then begin
      Bmark:=nSqry.GetBookmark; nSqry.DisableControls;
      nSqry.First;
      While nSqry.EOF=False do begin
        nSqry.Edit;
        if RadioButton4.Checked=True Then
        nSqry.FieldByName('Code5').AsString:='O';
        if RadioButton5.Checked=True Then
        nSqry.FieldByName('Code5').AsString:='N';
        nSqry.Post;
        nSqry.Next;
      end;
      nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
      nSqry.First;
    end;
end;

procedure TSobo28.Button501Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Button509Click(Sender: TObject);
begin
//
end;

procedure TSobo28.Edit101Change(Sender: TObject);
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

procedure TSobo28.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo28.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo28.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo28.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo28.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo28.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo28.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo28.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo28.Edit114KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo28.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo28.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo28.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo28.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo28.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo28.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo28.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo28.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
  Button301Click(Self);
end;

procedure TSobo28.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo28.DBGrid101DblClick(Sender: TObject);
begin
  if(nSqry.RecordCount>0)Then begin
  Subu00.Menu201Click(Self);
  Sobo21.Edit103.Text:=T2_Sub81.FieldByName('Jubun').AsString;
  Sobo21.Edit101.Text:=Edit101.Text;
  Sobo21.Edit104.Text:=T2_Sub81.FieldByName('Gcode').AsString;
  Sobo21.Edit105.Text:=T2_Sub81.FieldByName('Gname').AsString;
  Sobo21.Edit107.Text:=T2_Sub81.FieldByName('Hcode').AsString;
  Sobo21.Edit108.Text:=T2_Sub81.FieldByName('Hname').AsString;
  Sobo21.Edit109.Text:='';
  Sobo21.Label100.Visible:=False;
  Sobo21.Edit106.Visible:=False;
  Sobo21.Edit106.Items.Clear;
  if T2_Sub81.FieldByName('Gjisa').AsString<>'' then begin
  Sobo21.Label100.Visible:=True;
  Sobo21.Edit106.Visible:=True;
  Sobo21.Edit106.Items.Add(T2_Sub81.FieldByName('Gjisa').AsString);
  Sobo21.Edit106.ItemIndex:=0;
  end;
  Sobo21.Button101Click(Self);
  end;
end;

procedure TSobo28.DBGrid101DrawColumnCell(Sender: TObject;
  const Rect: TRect; DataCol: Integer; Column: TColumnEh;
  State: TGridDrawState);
begin
{ with (Sender as TDBGridEh) do begin
    if(DBGrid101.SelectedRows.CurrentRowSelected = False) then begin
      if(Column.FieldName='GCODE')or(Column.FieldName='GNAME')or
        (Column.FieldName='GTELS')or(Column.FieldName='CODE5')then begin
      //(Column.FieldName='CODE2')or(Column.FieldName='CODE3')or
      //(Column.FieldName='CODE4')or(Column.FieldName='CODE1')then begin
        if DataSource.DataSet.RecNo mod 2 = 0
        then Canvas.Brush.Color := $00F8FFC6
        else Canvas.Brush.Color := clwhite;

        Canvas.Font.Color := Font.Color;
        DBGrid101.DefaultDrawColumnCell(Rect, DataCol, Column, State);
      end;
    end;
  end; }
end;

procedure TSobo28.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo28.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo28.Button701Click(Sender: TObject);
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

procedure TSobo28.Button702Click(Sender: TObject);
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

procedure TSobo28.Edit205Click(Sender: TObject);
begin
  if Edit205.Focused=True then
  StaticText1.Visible:=False;
  if Edit206.Focused=True then
  StaticText2.Visible:=False;
  if Edit207.Focused=True then
  StaticText3.Visible:=False;
end;

procedure TSobo28.Edit205Exit(Sender: TObject);
begin
  StaticText1.Visible:=False;
  StaticText2.Visible:=False;
  StaticText3.Visible:=False;
  if Edit205.Text='' then
  StaticText1.Visible:=True;
  if Edit206.Text='' then
  StaticText2.Visible:=True;
  if Edit207.Text='' then
  StaticText3.Visible:=True;
end;

procedure TSobo28.StaticText1Click(Sender: TObject);
begin
  StaticText1.Visible:=False;
  Edit205.SetFocus;
end;

procedure TSobo28.StaticText2Click(Sender: TObject);
begin
  StaticText2.Visible:=False;
  Edit206.SetFocus;
end;

procedure TSobo28.StaticText3Click(Sender: TObject);
begin
  StaticText3.Visible:=False;
  Edit207.SetFocus;
end;

procedure TSobo28.ColumnX1(TableX: TClientDataSet);
var I,K: Integer;
  St1: Integer;
cFieldname: string;
  St8:array [0..21] of String;
  St9:array [0..21] of String;
  St0,St2,p_Idnum: Integer;
  p_Scode,p_Gdate,p_Gcode,p_Gubun,p_Jubun,p_Gjisa: String;
XL, XArr, XTitle: Variant;
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
  if Base10.Database.Database='chul_04_db' then begin
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
             Tong10.F1Book1.TextRC[St1,I+1]  :='031-921-8628';
           end else
           if I = 2 then begin
             Tong10.F1Book1.TextRC[St1,I+1]  :='경기도 고양시 일산서구 산율길 59-25';
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
    St8[01]:='Hname'; St9[01]:='송화인연락처';
    St8[02]:='Hcode'; St9[02]:='송화인주소';
    St8[03]:='Hcode'; St9[03]:='주소';
    St8[04]:='Hcode'; St9[04]:='핸드폰번호';
    St8[05]:='Hcode'; St9[05]:='전화번호';
    St8[06]:='Hcode'; St9[06]:='받는사람';
    St8[07]:='Gqut1'; St9[07]:='수량';
    St8[08]:='Gqut2'; St9[08]:='건수';

    if nList<>'3' then
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

    if nList='3' then
    if TableX.Active=True Then begin
    // Bmark:=TableX.GetBookmark; TableX.DisableControls;

       try
         //엑셀을 실행
         XL := CreateOLEObject('Excel.Application');
       except
         MessageDlg('Excel이 설치되어 있지 않습니다.',MtWarning, [mbok], 0);
         Exit;
       end;

       XL.WorkBooks.Add; //새로운 페이지 생성
       XL.Visible := True;
       I := 1;
       K := 1;

       //타이틀 처리변수
       XTitle := VarArrayCreate([1, St0], VarVariant);
       TableX.First;
       while I <= St0 do begin
         cFieldname:=St8[I-1];
         if TableX.FieldByName(cFieldname).DataType=ftString Then begin
         XL.Workbooks[XL.Workbooks.Count].WorkSheets['Sheet1'].Columns[I].Select;
         XL.Selection.NumberFormatLocal := '@';
         end;
         XTitle[I] := St9[I-1];
         Inc(I);
       end;
       //타이틀처리
       XL.Range['A1', CHR(64 + St0) + '1'].Value := XTitle;

       //데이타 처리변수
       XArr := VarArrayCreate([1, St0], VarVariant);

     //PBar.Max:=TableX.RecordCount;
       While TableX.EOF=False do begin
       //PBar.Position:=PBar.Position+1;
         I := 1;
         while I <= St0 do begin
           cFieldname:=St8[I-1];
           if I = 2 then begin
             XArr[I]   :='031-111-2222';
           end else
           if I = 3 then begin
             XArr[I]   :='경기도 ???(주소)';
           end else
           if I = 4 then begin
             XArr[I]   :=Edit203.Text+' '+Edit204.Text;
           end else
           if I = 5 then begin
             XArr[I]   :=Edit205.Text;
           end else
           if I = 6 then begin
             XArr[I]   :=Edit206.Text;
           end else
           if I = 7 then begin
             XArr[I]   :=Edit207.Text;
           end else begin
             XArr[I]   :=TableX.FieldByName(cFieldname).Value;
           end;
           Inc(I);
         end;
         //셀에 값을 넣는다.
         XL.Range['A' + IntToStr(K+1), CHR(64 + St0) + IntToStr(K+1)].Value := XArr;
         TableX.Next;
         Inc(K);
       end;
       //셀 크기 조정
       XL.Range['A1', CHR(64 + St0) + IntToStr(K)].Select;
       XL.Selection.Columns.AutoFit;
       XL.Range['A1', 'A1'].Select;
     //PBar.Position:=0;

    // TableX.GotoBookmark(Bmark); TableX.FreeBookmark(Bmark); TableX.EnableControls;
    end;
  end;
end;

end.
