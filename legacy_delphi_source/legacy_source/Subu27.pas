unit Subu27;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, TFlatRadioButtonUnit,
  DBGridEh, ImgList, ToolEdit, dxCore, dxButtons;

type
  TSobo27 = class(TForm)
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
    ImageList1: TImageList;
    ImageList2: TImageList;
    ImageList3: TImageList;
    Panel003: TFlatPanel;
    RadioButton1: TFlatRadioButton;
    RadioButton2: TFlatRadioButton;
    RadioButton3: TFlatRadioButton;
    Panel004: TFlatPanel;
    RadioButton4: TFlatRadioButton;
    RadioButton5: TFlatRadioButton;
    RadioButton6: TFlatRadioButton;
    ImageList4: TImageList;
    Timer1: TTimer;
    RadioButton7: TFlatRadioButton;
    DateEdit1: TDateEdit;
    Button701: TFlatButton;
    Button702: TFlatButton;
    Panel005: TFlatPanel;
    RadioButton8: TFlatRadioButton;
    RadioButton9: TFlatRadioButton;
    RadioButton0: TFlatRadioButton;
    Panel011: TFlatPanel;
    RadioButton12: TFlatRadioButton;
    RadioButton11: TFlatRadioButton;
    RadioButton13: TFlatRadioButton;
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
    procedure Button502Click(Sender: TObject);
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
    procedure Timer1Timer(Sender: TObject);
    procedure DBGrid101DrawColumnCell(Sender: TObject; const Rect: TRect;
      DataCol: Integer; Column: TColumnEh; State: TGridDrawState);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo27: TSobo27;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo27.FormActivate(Sender: TObject);
begin
  nForm:='27';
  nSqry:=Base10.T2_Sub71;
  mSqry:=Base10.T2_Sub72;
  tSqry:=Base10.T4_Sub81;
end;

procedure TSobo27.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit101.SetFocus;
end;

procedure TSobo27.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo27:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Base10.OpenExit(tSqry);
end;

procedure TSobo27.Button001Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end; }
end;

procedure TSobo27.Button002Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_27_01(Self);
  end; }
end;

procedure TSobo27.Button003Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo27.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button008Click(Sender: TObject);
begin
  Tong20.Zoom_Int_01('27');
end;

procedure TSobo27.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('27');
end;

procedure TSobo27.Button010Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo27.Button011Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo27.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX9(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo27.Button013Click(Sender: TObject);
begin
{ oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1); }
end;

procedure TSobo27.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('27-01');
end;

procedure TSobo27.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('27-02');
end;

procedure TSobo27.Button016Click(Sender: TObject);
begin
  mSqry.First;
  While mSqry.EOF=False do begin
  if(mSqry.FieldByName('Code3').AsString='1')and
    (mSqry.FieldByName('Code5').AsString='O')then begin
    Button201Click(Self);
    Button301Click(Self);
    mSqry.Edit;
    mSqry.FieldByName('Gsqut').AsFloat:=mSqry.FieldByName('Gsqut').AsFloat+mSqry.FieldByName('Goqut').AsFloat;
    mSqry.FieldByName('Goqut').AsString:='';
    mSqry.FieldByName('Code3').AsString:='';
    mSqry.FieldByName('Code4').AsString:='2';
    mSqry.Post;
    Tong40.PrinTing00('24','1','','','','','','','','');
    end;
    mSqry.Next;
  end;
end;

procedure TSobo27.Button017Click(Sender: TObject);
begin
  mSqry.First;
  While mSqry.EOF=False do begin
  if(mSqry.FieldByName('Code4').AsString='2')and
    (mSqry.FieldByName('Code5').AsString='O')then begin
      if RadioButton11.Checked=True Then begin
      Button501Click(Self);
      Button502Click(Self);
      end;
      if RadioButton12.Checked=True Then begin
      Button501Click(Self);
      end;
      if RadioButton13.Checked=True Then begin
      Button502Click(Self);
      end;
    end;
    mSqry.Next;
  end;
end;

procedure TSobo27.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button021Click(Sender: TObject);
begin
//Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo27.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo27.Button101Click(Sender: TObject);
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
  Base10.OpenShow(mSqry);

  St1:='';
  if (Edit104.Text<>'') Then
  St1:=' and '+'Gcode'+'>='+#39+Edit102.Text+#39+
       ' and '+'Gcode'+'<='+#39+Edit104.Text+#39;

  St1:=St1+' and '+'Gcode'+'< '+#39+'x'+#39;

  St1:=St1+' and '+' Not ( Gname'+' like '+#39+'%종료%'+#39+' )';

  if S_Where2<>'' then
  St1:=St1+' and '+S_Where2;

  Sqlen := 'Select Gcode,Gname,Gtel1,Gtel2 From G7_Ggeo Where '+D_Open+St1+//' Order By Gcode';
           ' Order by field( ocode, '+#39+'x'+#39+'),field( chek5, '+#39+'show1'+#39+'),gcode';
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
    mSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 0,List1];
    mSqry.FieldByName('Gname').AsString:=SGrid.Cells[ 1,List1];
    mSqry.FieldByName('Code1').AsString:='9';
    mSqry.FieldByName('Code5').AsString:='N';
    mSqry.FieldByName('Gtels').AsString:=SGrid.Cells[ 2,List1]+'-'+SGrid.Cells[ 3,List1];
    mSqry.Post;
  end;

  //--9--//
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit101.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'X'+#39;
  if (Edit104.Text<>'') Then
  St1:=St1+' and '+
       'Hcode'+'>='+#39+Edit102.Text+#39+' and '+
       'Hcode'+'<='+#39+Edit104.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  St2:=' Group By Hcode';

  Sqlen := 'Select Hcode,Count(*) From S1_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    St3:=SGrid.Cells[ 0,List1];
    if mSqry.Locate('Gcode',St3,[loCaseInsensitive])=True then begin
    mSqry.Edit;
    mSqry.FieldByName('Code1').AsString:='';
    mSqry.Post;
    end;
  end;

  //--0--//
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit101.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'X'+#39+' and '+
       'Yesno'+' ='+#39+'0'+#39;
  if (Edit104.Text<>'') Then
  St1:=St1+' and '+
       'Hcode'+'>='+#39+Edit102.Text+#39+' and '+
       'Hcode'+'<='+#39+Edit104.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  St2:=' Group By Hcode';

  Sqlen := 'Select Hcode,Count(*) From S1_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    St3:=SGrid.Cells[ 0,List1];
    if mSqry.Locate('Gcode',St3,[loCaseInsensitive])=True then begin
    mSqry.Edit;
    mSqry.FieldByName('Code2').AsString:='0';
    mSqry.Post;
    end;
  end;

  //--1--//
if RadioButton2.Checked<>True Then begin
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit101.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'X'+#39+' and '+
       'Yesno'+' ='+#39+'1'+#39;
  if (Edit104.Text<>'') Then
  St1:=St1+' and '+
       'Hcode'+'>='+#39+Edit102.Text+#39+' and '+
       'Hcode'+'<='+#39+Edit104.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  St2:=' Group By Hcode,Gcode,Jubun,Gjisa';

  Sqlen := 'Select Hcode,Gcode,Jubun,Gjisa,Count(*) From S1_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    St3:=SGrid.Cells[ 0,List1];
    T01:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    if mSqry.Locate('Gcode',St3,[loCaseInsensitive])=True then begin
    mSqry.Edit;
    mSqry.FieldByName('Code3').AsString:='1';
    mSqry.FieldByName('Goqut').AsFloat :=mSqry.FieldByName('Goqut').AsFloat+1;
    mSqry.Post;
    end;
  end;
end;

  //--2--//
if RadioButton1.Checked<>True Then begin
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit101.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'X'+#39+' and '+
       'Yesno'+' ='+#39+'2'+#39;
  if (Edit104.Text<>'') Then
  St1:=St1+' and '+
       'Hcode'+'>='+#39+Edit102.Text+#39+' and '+
       'Hcode'+'<='+#39+Edit104.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

  St2:=' Group By Hcode,Gcode,Jubun,Gjisa';

  Sqlen := 'Select Hcode,Gcode,Jubun,Gjisa,Count(*) From S1_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    St3:=SGrid.Cells[ 0,List1];
    T01:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    if mSqry.Locate('Gcode',St3,[loCaseInsensitive])=True then begin
    mSqry.Edit;
    mSqry.FieldByName('Code4').AsString:='2';
    mSqry.FieldByName('Gsqut').AsFloat :=mSqry.FieldByName('Gsqut').AsFloat+1;
    mSqry.Post;
    end;
  end;
end;

  mSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }


  if Base10.Database.Database='book_kb_db' then begin
    Sqlen := 'Select Count(*) From S4_Ssub Where '+D_Select+
             'Code2=''@Code2'' and Code3<>''@Code3'' ';

    Translate(Sqlen, '@Gdate', Edit101.Text);
    Translate(Sqlen, '@Code2', 'O');
    Translate(Sqlen, '@Code3', 'O');

    St3:=Base10.Seek_Name(Sqlen);
    if St3>'0' then
    ShowMessage('가입고된 자료가 있습니다.');

  end;

end;

procedure TSobo27.Button201Click(Sender: TObject);
var St1,St2: String;
begin
  Base10.OpenShow(nSqry);
  St1:='Gdate'+'>='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Gdate'+'<='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Gcode').AsString+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'X'+#39;

  if RadioButton1.Checked=True Then
  St1:=St1+' and '+'Yesno'+'='+#39+'1'+#39 else
  if RadioButton2.Checked=True Then
  St1:=St1+' and '+'Yesno'+'='+#39+'2'+#39 else
  if RadioButton3.Checked=True Then
  St1:=St1+' and '+'Yesno'+'>'+#39+'3'+#39 else
  St1:=St1+' and '+'Yesno'+'='+#39+'1'+#39;

  if Base10.Database.Database='book_07_db' then
  St2:=' Order By Gdate,Hcode,Gcode,Gubun,Jubun,Gjisa,ID'
  else
  St2:=' Order By Gdate,Hcode,Gcode,Gubun,Jubun,Gjisa,Bcode,ID';

  Sqlen := 'Select * From S1_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  nSqry.First;
  While nSqry.EOF=False do begin

    nSqry.Edit;

    if Base10.G7_Ggeo.Locate('Gcode',nSqry.FieldByName('Hcode').AsString,[loCaseInsensitive])=true then
    nSqry.FieldByName('Hname').AsString:=Base10.G7_Ggeo.FieldByName('Gname').AsString;

    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Gname').AsString='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Hname').AsString='' then begin
    Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Hcode').AsString);
    nSqry.FieldByName('Hname').Value:=Base10.Seek_Name(Sqlen);
    end;

    if nSqry.FieldByName('Gname').AsString='' then begin
    Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', '');
    nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
    end;

    if nSqry.FieldByName('Gname').AsString='' then begin
    Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
    end;

    if nSqry.FieldByName('Gjisa').AsString<>'' then
    nSqry.FieldByName('Gname').AsString:=Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'2')+
    nSqry.FieldByName('Gname').AsString+ Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'1');

    Sqlen := 'Select Gname,Gjeja From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Bcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      nSqry.FieldByName('Bname').Value:=Base10.Socket.GetData(1, 1);
      nSqry.FieldByName('Gjeja').Value:=Base10.Socket.GetData(1, 2);
    end;

    nSqry.Post;
    nSqry.Next;
  end;
end;

procedure TSobo27.Button301Click(Sender: TObject);
begin
  if RadioButton2.Checked<>True Then begin
    Sqlen := 'UPDATE S1_Ssub SET Yesno=''@Yesno'' ,Time3= now()'+
    ' WHERE '+D_Select+
    ' Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
    ' Scode=''@Scode'' and Yesno=''@Yesoo'' and '+
    ' Ocode=''@Ocode'' and Hcode=''@Hcode'' ';

    Translate(Sqlen, '@Gdate', mSqry.FieldByName('Gdate').AsString);
    Translate(Sqlen, '@Gubun', '출고');
    Translate(Sqlen, '@Scode', 'X'   );
    Translate(Sqlen, '@Yesoo', '1'   );
    Translate(Sqlen, '@Ocode', 'B'   );
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Yesno', '2'   );

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
  end;
end;

procedure TSobo27.Button401Click(Sender: TObject);
begin
  if RadioButton6.Checked=True Then begin
    Timer1.Enabled:=True;
  end else
  if RadioButton7.Checked=True Then begin
    Timer1.Enabled:=False;
  end else begin
    Timer1.Enabled:=False;
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

procedure TSobo27.Button501Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6,St8,St9: String;
begin
  Base10.OpenShow(tSqry);

  Button509Click(Self);

  St1:='Gdate'+' ='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Gcode').AsString+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Yesno'+' ='+#39+'2'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'X'+#39;

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

  if Base10.G7_Ggeo.Locate('Gcode',mSqry.FieldByName('Gcode').AsString,[loCaseInsensitive])=true then
  St6:=Base10.G7_Ggeo.FieldByName('Gname').AsString;

  if St6='' then begin
  Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Gcode', mSqry.FieldByName('Gcode').AsString);
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
      if(YGrid.Cells[ 0,RBand]=mSqry.FieldByName('Gcode').AsString)and
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
    St8:='';
    St9:='';

  { Sqlen := 'Select Gname From T1_Gbun Where '+D_Select+
             'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun''';
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Gjisa', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
    Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
    St4:=Base10.Seek_Name(Sqlen);
    St5:=''; }

    if Base10.G7_Ggeo.Locate('Gcode',mSqry.FieldByName('Gcode').AsString,[loCaseInsensitive])=true then begin
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
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
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

    if SGrid.Cells[ 1,List1]<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
      if Copy(SGrid.Cells[ 0,List1],1,1)<>'9' then
      Translate(Sqlen, '@Hcode', '') else
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', 'X');
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gname', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
      St8:=Base10.Seek_Name(Sqlen);
    end;
    if St8='지방물류' then St9:='2';

    if St9='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end;
    if St9='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Gcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end;

    St9:='';
  { if RadioButton11.Checked=True Then St9:='';
    if RadioButton13.Checked=True Then begin
      if St9='' then
      St9:='2' else
      St9:=''
    end; }

   if St9='' then begin

    if St4='' then
    if SGrid.Cells[ 1,List1]<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
      if Copy(SGrid.Cells[ 0,List1],1,1)<>'9' then
      Translate(Sqlen, '@Hcode', '') else
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', 'X');
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gname', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
      St4:=Base10.Seek_Name(Sqlen);
    end;

    if St4='' then begin
      if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
      end;

      if St4='' then
      if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Gcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
      end;

      if St4='' then begin
      Sqlen := 'Select Gubun From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', '');
      if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
      end;

      if St4='' then begin
      Sqlen := 'Select Gubun From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
      if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
      end;
    end;

    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then
    St5:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if St5='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Gcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then
    St5:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if St5='' then begin
    Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', '');
    St5:=Base10.Seek_Name(Sqlen);
    end;

    if St5='' then begin
    Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
    St5:=Base10.Seek_Name(Sqlen);
    end;

    if SGrid.Cells[ 1,List1]<>'' then
    St5:=Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'2')+
    St5+ Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'1');

    if(St4='시내')or(St4='시내*')then begin
     if(Pos('*',St5) = 0)then begin
      T03:=T03+1;
      St1:=FloatToStr(T03);
     end else begin
      T02:=T02+1;
      St1:=FloatToStr(T02);
     end;
    end;

    if(St4='시내')or(St4='시내*')then begin
    if tSqry.Locate('Gdate',St1,[loCaseInsensitive])=False then begin
      tSqry.Append;
      tSqry.FieldByName('Scode').AsString:=mSqry.FieldByName('Gcode').AsString;
      tSqry.FieldByName('Gdate').AsString:=St1;
      tSqry.FieldByName('Name1').AsString:=St6;
      tSqry.FieldByName('Name2').AsString:=mSqry.FieldByName('Gdate').AsString;
    end;
    end;

    if(St4='시내')or(St4='시내*')then begin
     if(Pos('*',St5) = 0)then begin
      tSqry.Edit;
      Sqlen :=
      'Select Sum(Gqut1)as Gqut1,Sum(Gqut2)as Gqut2,Sum(Gqut3)as Gqut3 From T4_Ssub Where '+D_Select+
      'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' ';
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
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
      tSqry.Post;
      T04:=T04+T01;
     end else begin
      tSqry.Edit;
      Sqlen :=
      'Select Sum(Gqut1)as Gqut1,Sum(Gqut2)as Gqut2,Sum(Gqut3)as Gqut3 From T4_Ssub Where '+D_Select+
      'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' ';
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
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
      tSqry.Post;
      T05:=T05+T01;
     end;
    end;

   end;

  end;
  if tSqry.RecordCount > 0 then
  Tong40.Print_21_02(Self);
end;

procedure TSobo27.Button502Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6,St8,St9: String;
begin
  Base10.OpenShow(tSqry);

  Button509Click(Self);

  St1:='Gdate'+' ='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Gcode').AsString+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Yesno'+' ='+#39+'2'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39+' and '+
       'Scode'+' ='+#39+'X'+#39;

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

  if Base10.G7_Ggeo.Locate('Gcode',mSqry.FieldByName('Gcode').AsString,[loCaseInsensitive])=true then
  St6:=Base10.G7_Ggeo.FieldByName('Gname').AsString;

  if St6='' then begin
  Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Gcode', mSqry.FieldByName('Gcode').AsString);
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
      if(YGrid.Cells[ 0,RBand]=mSqry.FieldByName('Gcode').AsString)and
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
    St8:='';
    St9:='';

  { Sqlen := 'Select Gname From T1_Gbun Where '+D_Select+
             'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun''';
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Gjisa', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
    Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
    St4:=Base10.Seek_Name(Sqlen);
    St5:=''; }

    if Base10.G7_Ggeo.Locate('Gcode',mSqry.FieldByName('Gcode').AsString,[loCaseInsensitive])=true then begin
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
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
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

    if SGrid.Cells[ 1,List1]<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
      if Copy(SGrid.Cells[ 0,List1],1,1)<>'9' then
      Translate(Sqlen, '@Hcode', '') else
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', 'X');
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gname', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
      St8:=Base10.Seek_Name(Sqlen);
    end;
    if St8='지방물류' then St9:='2';

    if St9='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end;
    if St9='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Gcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
      if Base10.G1_Ggeo.FieldByName('Pubun').AsString='03' then St9:='2';
    end;

    St9:='';
  { if RadioButton11.Checked=True Then St9:='';
    if RadioButton13.Checked=True Then begin
      if St9='' then
      St9:='2' else
      St9:=''
    end; }

   if St9='' then begin

    if St4='' then
    if SGrid.Cells[ 1,List1]<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where '+D_Select+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
      if Copy(SGrid.Cells[ 0,List1],1,1)<>'9' then
      Translate(Sqlen, '@Hcode', '') else
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', 'X');
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gname', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'4'));
      St4:=Base10.Seek_Name(Sqlen);
    end;

    if St4='' then begin
      if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
      end;

      if St4='' then
      if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Gcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
        if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
      end;

      if St4='' then begin
      Sqlen := 'Select Gubun From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', '');
      if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
      end;

      if St4='' then begin
      Sqlen := 'Select Gubun From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
      if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
      end;
    end;

    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then
    St5:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if St5='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Gcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then
    St5:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if St5='' then begin
    Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', '');
    St5:=Base10.Seek_Name(Sqlen);
    end;

    if St5='' then begin
    Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
    St5:=Base10.Seek_Name(Sqlen);
    end;

    if SGrid.Cells[ 1,List1]<>'' then
    St5:=Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'2')+
    St5+ Base10.Seek_Jisa(SGrid.Cells[ 1,List1],'1');

   if(St4='시내')or(St4='시내*')then begin
   end else begin
    if(St4<>'시내')and(St4<>'시내*')and(Pos('*',St5) > 0)then begin
      T03:=T03+1;
      St1:=FloatToStr(T03);
    end else begin
      T02:=T02+1;
      St1:=FloatToStr(T02);
    end;
   end;

   if(St4='시내')or(St4='시내*')then begin
   end else begin
    if(St4<>'시내')and(St4<>'시내*')then begin
    if tSqry.Locate('Gdate',St1,[loCaseInsensitive])=False then begin
      tSqry.Append;
      tSqry.FieldByName('Scode').AsString:=mSqry.FieldByName('Gcode').AsString;
      tSqry.FieldByName('Gdate').AsString:=St1;
      tSqry.FieldByName('Name1').AsString:=St6;
      tSqry.FieldByName('Name2').AsString:=mSqry.FieldByName('Gdate').AsString;
    end;
    end;

    if(St4<>'시내')and(St4<>'시내*')and(Pos('*',St5) > 0)then begin
      tSqry.Edit;
      Sqlen :=
      'Select Sum(Gqut1)as Gqut1,Sum(Gqut2)as Gqut2,Sum(Gqut3)as Gqut3 From T4_Ssub Where '+D_Select+
      'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' ';
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
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
      tSqry.Post;
      T04:=T04+T01;
    end else begin
     if(St4<>'시내')and(St4<>'시내*')and( Pos('*',St5) = 0)then begin
      tSqry.Edit;
      Sqlen :=
      'Select Sum(Gqut1)as Gqut1,Sum(Gqut2)as Gqut2,Sum(Gqut3)as Gqut3 From T4_Ssub Where '+D_Select+
      'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gdate=''@Gdate'' and Gjisa=''@Gjisa'' ';
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
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
      tSqry.Post;
      T05:=T05+T01;
     end;
    end;
   end;

   end;

  end;
  if tSqry.RecordCount > 0 then
  Tong40.Print_21_02(Self);
end;

procedure TSobo27.Button509Click(Sender: TObject);
var St1,St2,St3,St4,St8,St9: String;
begin

  St1:='S.Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'S.Gdate'+'<='+#39+Edit101.Text+#39+' and '+
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

  if RadioButton8.Checked=True Then begin
  St1:=St1+' and '+'S.Pubun'+'<>'+#39+'신간'+#39;
  end else
  if RadioButton9.Checked=True Then begin
  St1:=St1+' and '+'S.Pubun'+'= '+#39+'신간'+#39;
  end;

  St1:=St1+' and '+'Y.Grat8'+'> '+'1';

  if D_Select<>'' then
  St1:=St1+' and '+'('+'S.Check is null '+' or '+'S.Check'+'<>'+#39+'D'+#39+')';

  if D_Select<>'' then
  St1:=St1+' and '+'('+'Y.Check is null '+' or '+'Y.Check'+'<>'+#39+'D'+#39+')';

  Sqlen := 'Select S.Hcode,S.Gcode,S.Gjisa,S.Jubun,S.Bcode,Y.Grat8,S.Gsqut From S1_Ssub S, G4_Book Y '+
           'Where S.Hcode=Y.Hcode and S.Bcode=Y.Gcode and '+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(YGrid)
  else ShowMessage(E_Open);

end;

procedure TSobo27.Edit101Change(Sender: TObject);
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

procedure TSobo27.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo27.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo27.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo27.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo27.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo27.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo27.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo27.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo27.Edit114KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo27.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo27.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo27.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_F2 Then begin
    While mSqry.EOF=False do begin
    if(mSqry.FieldByName('Code3').AsString='1')and
      (mSqry.FieldByName('Code5').AsString='O')then begin
      Button201Click(Self);
      Button301Click(Self);
      mSqry.Edit;
      mSqry.FieldByName('Gsqut').AsFloat:=mSqry.FieldByName('Gsqut').AsFloat+mSqry.FieldByName('Goqut').AsFloat;
      mSqry.FieldByName('Goqut').AsString:='';
      mSqry.FieldByName('Code3').AsString:='';
      mSqry.FieldByName('Code4').AsString:='2';
      mSqry.Post;
      Tong40.PrinTing00('24','1','','','','','','','','');
      end;
      mSqry.Next;
    end;
  end;
  if Key=VK_F3 Then begin
    While mSqry.EOF=False do begin
    if(mSqry.FieldByName('Code4').AsString='2')and
      (mSqry.FieldByName('Code5').AsString='O')then begin
      Button501Click(Self);
      end;
      mSqry.Next;
    end;
  end;
  if Key=VK_F4 Then begin
    if(mSqry.FieldByName('Code4').AsString='2')and
      (mSqry.FieldByName('Code5').AsString='O')then begin
      Button201Click(Self);
      Tong40.PrinTing00('24','1','','','','','','','','');
    end;
  end;
  if Key=VK_F5 Then begin
    While mSqry.EOF=False do begin
    if(mSqry.FieldByName('Code4').AsString='2')and
      (mSqry.FieldByName('Code5').AsString='O')then begin
      Button201Click(Self);
      Tong40.PrinTing00('24','1','','','','','','','','');
      end;
      mSqry.Next;
    end;
  end;
{ if Key=VK_F4 Then begin
    if(mSqry.FieldByName('Code3').AsString='1')and
      (mSqry.FieldByName('Code5').AsString='O')then begin
      Button201Click(Self);
      Tong40.PrinTing00('24','2','','','','','','','','');
    end;
  end;
  if Key=VK_F5 Then begin
    While mSqry.EOF=False do begin
    if(mSqry.FieldByName('Code3').AsString='1')and
      (mSqry.FieldByName('Code5').AsString='O')then begin
      Button201Click(Self);
      Tong40.PrinTing00('24','2','','','','','','','','');
      end;
      mSqry.Next;
    end;
  end; }
{ if Key=VK_F7 Then Seak70.ShowModal; }
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo27.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo27.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo27.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(mSqry,Column);
end;

procedure TSobo27.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo27.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo27.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo27.Timer1Timer(Sender: TObject);
begin
  Timer1.Enabled:=False;

  try
    Button101Click(Self);
  except
  { ShowMessage('접속 장애가 발생하여 프로그램을 종료합니다.'+#13+
                '프로그램을 다시 실행해 주십시오');
    Close; }
  end;

  Timer1.Enabled:=True;
end;

procedure TSobo27.DBGrid101DrawColumnCell(Sender: TObject;
  const Rect: TRect; DataCol: Integer; Column: TColumnEh;
  State: TGridDrawState);
begin
  with (Sender as TDBGridEh) do begin
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
  end;
end;

procedure TSobo27.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo27.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo27.Button701Click(Sender: TObject);
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

procedure TSobo27.Button702Click(Sender: TObject);
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

end.
