unit Subu59_1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ToolEdit,
  TFlatRadioButtonUnit, dxCore, dxButtons, DBGridEh;

type
  TSobo59_1 = class(TForm)
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
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Panel200: TFlatPanel;
    Panel201: TFlatPanel;
    Panel202: TFlatPanel;
    Edit202: TFlatEdit;
    Edit201: TFlatEdit;
    Panel203: TFlatPanel;
    Edit203: TFlatEdit;
    Panel204: TFlatPanel;
    Edit204: TFlatEdit;
    Edit105: TFlatEdit;
    Edit106: TFlatEdit;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    Edit102: TFlatMaskEdit;
    DateEdit1: TDateEdit;
    DateEdit2: TDateEdit;
    Button701: TFlatButton;
    Button702: TFlatButton;
    RadioButton1: TFlatRadioButton;
    RadioButton2: TFlatRadioButton;
    DBGrid101: TDBGridEh;
    DBGrid201: TDBGridEh;
    dxButton1: TdxButton;
    RadioButton3: TFlatRadioButton;
    RadioButton4: TFlatRadioButton;
    RadioButton5: TFlatRadioButton;
    RadioButton6: TFlatRadioButton;
    RadioButton7: TFlatRadioButton;
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
    procedure DBGrid101TitleClick(Column: TColumnEh);
    procedure DBGrid201TitleClick(Column: TColumnEh);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure DBGrid201DblClick(Sender: TObject);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit2ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure DBGrid201Columns8UpdateData(Sender: TObject;
      var Text: String; var Value: Variant; var UseText, Handled: Boolean);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo59_1: TSobo59_1;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib, Subu21,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo59_1.FormActivate(Sender: TObject);
begin
  nForm:='59_1';
  nSqry:=Base10.T5_Sub81;
  mSqry:=Base10.T5_Sub82;
end;

procedure TSobo59_1.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo59_1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo59_1:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo59_1.Button001Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
     Seak10.ShowModal;
  end; }
end;

procedure TSobo59_1.Button002Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_53_02(Self);
  end; }
end;

procedure TSobo59_1.Button003Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo59_1.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button006Click(Sender: TObject);
begin
{ T00:=1;
  Button201Click(Self); }
end;

procedure TSobo59_1.Button007Click(Sender: TObject);
begin
{ T00:=0;
  Button201Click(Self); }
end;

procedure TSobo59_1.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button010Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo59_1.Button011Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo59_1.Button012Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo59_1.Button013Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo59_1.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('53-01');
end;

procedure TSobo59_1.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('53-02');
end;

procedure TSobo59_1.Button016Click(Sender: TObject);
begin
  mSqry.First;
  While mSqry.EOF=False do begin
    if(mSqry.FieldByName('Yesno').AsString='O')then
    Tong40.print_59_12(Self);
    mSqry.Next;
  end;
end;

procedure TSobo59_1.Button017Click(Sender: TObject);
begin
  Tong40.print_59_11(Self);
end;

procedure TSobo59_1.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont3(DBGrid101,DBGrid201);
end;

procedure TSobo59_1.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo59_1.Button101Click(Sender: TObject);
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

  St2:='X';

  if RadioButton7.Checked=True Then
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Gubun'+' ='+#39+'반품'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39
  //   'Scode'+' ='+#39+St2+#39
  else
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Ocode'+' ='+#39+'B'+#39;
  //   'Scode'+' ='+#39+St2+#39;

  if RadioButton1.Checked=True Then
  St1:=St1+' and '+'Yesno'+' ='+#39+'1'+#39
  else
  if RadioButton2.Checked=True Then
  St1:=St1+' and '+'Yesno'+'<='+#39+'0'+#39
  else
  St1:=St1+' and '+'Yesno'+'>='+#39+'1'+#39;

  if RadioButton4.Checked=True Then
  St1:=St1+' and '+'Pubun'+' ='+#39+'신간'+#39
  else
  if RadioButton5.Checked=True Then
  St1:=St1+' and '+'Pubun'+'<>'+#39+'신간'+#39;

  if (Edit105.Text<>'') Then
  St1:=St1+' and '+
       'Hcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Hcode'+'<='+#39+Edit105.Text+#39;

  if S_Where1<>'' then
  St1:=St1+' and '+S_Where1;

{ if Hnnnn='4100' then
  St1:='('+St1+')'+' and '+S_Where1;
  if Hnnnn='8300' then
  St1:='('+St1+')'+' and '+S_Where1; }

  St2:=' Order By Gdate,Hcode,Gcode,Gubun,Jubun,Gjisa,ID';

  {-S1_Ssub-}
  Sqlen :=
  'Select Hcode,Count(Hcode),Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
  'From S1_Ssub Where '+D_Select+St1+' Group by Hcode ';
  Sqlen := Sqlen+' LIMIT 0,10000 ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  T01:=0; T02:=0; T03:=0; T04:=0;

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    T01:=T01+1;
    T02:=T02+StrToIntDef(SGrid.Cells[ 1,List1],0);
    T03:=T03+StrToIntDef(SGrid.Cells[ 2,List1],0);
    T04:=T04+StrToIntDef(SGrid.Cells[ 3,List1],0);
  end;

  Edit201.Text:=FormatFloat('########0',T01);
  Edit202.Text:=FormatFloat('########0',T02);
  Edit203.Text:=FormatFloat('###,###,##0',T03);
  Edit204.Text:=FormatFloat('###,###,##0',T04);

  St3:=' Group By Hcode,Scode,Gdate,Gcode,Idnum,Gubun,Jubun,Gjisa';

  Sqlen := 'Select Hcode,Scode,Gdate,Gcode,Idnum,Gubun,Jubun,Gjisa,Count(*)as Gdang,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
           ' From S1_Ssub Where '+D_Select+St1+St3;
  Sqlen := Sqlen+' LIMIT 0,10000 ';

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

    if nSqry.FieldByName('Scode').AsString='X' then
      if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
      nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;
    if nSqry.FieldByName('Scode').AsString='Z' then
      if Base10.G5_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
      nSqry.FieldByName('Gname').AsString:=Base10.G5_Ggeo.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Scode').AsString='X' then
      if nSqry.FieldByName('Gname').AsString='' then
      if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
      nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;
    if nSqry.FieldByName('Scode').AsString='Z' then
      if nSqry.FieldByName('Gname').AsString='' then
      if Base10.G5_Ggeo.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
      nSqry.FieldByName('Gname').AsString:=Base10.G5_Ggeo.FieldByName('Gname').AsString;

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

    if nSqry.FieldByName('Scode').AsString='X' then
      if nSqry.FieldByName('Gname').AsString='' then begin
      Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Hcode', '');
      nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
      end;
    if nSqry.FieldByName('Scode').AsString='Z' then
      if nSqry.FieldByName('Gname').AsString='' then begin
      Sqlen := 'Select Gname From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Hcode', '');
      nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
      end;

    if nSqry.FieldByName('Scode').AsString='X' then
      if nSqry.FieldByName('Gname').AsString='' then begin
      Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
      end;
    if nSqry.FieldByName('Scode').AsString='Z' then
      if nSqry.FieldByName('Gname').AsString='' then begin
      Sqlen := 'Select Gname From G5_Ggeo Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
      end;

    nSqry.FieldByName('Yesno').AsString:='0';

    Sqlen := 'Select Yesno,Time1 From S1_Chek Where '+D_Select+
             'Hcode=''@Hcode'' and Scode=''@Scode'' and '+
             'Gdate=''@Gdate'' and Gcode=''@Gcode'' and '+
             'Jubun=''@Jubun'' and Gjisa=''@Gjisa'' and '+
             '`Check`<>''@Check'' ';
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Scode', 'X');
    Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
    Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
    Translate(Sqlen, '@Check', 'D');
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      nSqry.FieldByName('Yesno').AsString:=Base10.Socket.GetData(1, 1);
      nSqry.FieldByName('Gbigo').AsString:=Base10.Socket.GetData(1, 2);
    end;

    nSqry.Post;
    nSqry.Next;
  end;

  Button201Click(Self);

  nSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo59_1.Button201Click(Sender: TObject);
var St1,St2,St3,St4,St5: String;
begin
  nSqry.First;
  mSqry.First;
  While nSqry.EOF=False do begin
    St1:=nSqry.FieldByName('Hcode').AsString;
    St3:=nSqry.FieldByName('Scode').AsString;
    St4:=nSqry.FieldByName('Gdate').AsString;
    if mSqry.Locate('Hcode;Scode;Gdate',VarArrayOf([St1,St3,St4]),[loCaseInsensitive])=False then begin
      mSqry.Append;
      mSqry.FieldByName('Hcode').AsString:=St1;
      mSqry.FieldByName('Scode').AsString:=St3;
      mSqry.FieldByName('Gdate').AsString:=St4;
      mSqry.FieldByName('Hname').AsString:=nSqry.FieldByName('Hname').AsString;
      mSqry.FieldByName('Yesno').AsString:='O';
      mSqry.Post;
    end;
    nSqry.Next;
  end;
  nSqry.First;
  mSqry.First;
end;

procedure TSobo59_1.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit104.Focused=True)and(Edit104.SelStart=50)and(Length(Trim(Edit104.Text))=50))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit106.Focused=True)and(Edit106.SelStart=50)and(Length(Trim(Edit106.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo59_1.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo59_1.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo59_1.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo59_1.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo59_1.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo59_1.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo59_1.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo59_1.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo59_1.Edit115KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo59_1.Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo59_1.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if Edit104.Focused=True Then begin
       Edit103.Text:='';
    if Edit104.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit104.Text;
    Seak80.FilterTing(Edit104.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seak80.Query1Gcode.AsString;
      Edit104.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seak80.Query1Gcode.AsString;
      Edit104.Text:=Seak80.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if Edit106.Focused=True Then begin
       Edit105.Text:='';
    if Edit106.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit106.Text;
    Seak80.FilterTing(Edit106.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit105.Text:=Seak80.Query1Gcode.AsString;
      Edit106.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit105.Text:=Seak80.Query1Gcode.AsString;
      Edit106.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo59_1.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo59_1.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo59_1.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo59_1.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo59_1.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo59_1.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(mSqry,Column);
end;

procedure TSobo59_1.DBGrid201TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo59_1.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo59_1.DataSource2DataChange(Sender: TObject; Field: TField);
var St1: String;
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);

  St1:='';
  St1:=St1+'Hcode'+'='+#39+mSqry.FieldByName('Hcode').AsString+#39+' and ';
  St1:=St1+'Scode'+'='+#39+mSqry.FieldByName('Scode').AsString+#39+' and ';
  St1:=St1+'Gdate'+'='+#39+mSqry.FieldByName('Gdate').AsString+#39;
  nSqry.Filter:=St1;
  nSqry.Filtered:=True;
//Srart_59_01(Self);
end;

procedure TSobo59_1.DBGrid201DblClick(Sender: TObject);
begin
{ if(nSqry.RecordCount>0)Then begin
  Subu00.Menu201Click(Self);
  Sobo21.Edit103.Text:=Base10.T5_Sub31.FieldByName('Jubun').AsString;
  Sobo21.Edit101.Text:=Base10.T5_Sub31.FieldByName('Gdate').AsString;
  Sobo21.Edit104.Text:=Base10.T5_Sub31.FieldByName('Gcode').AsString;
  Sobo21.Edit105.Text:=Base10.T5_Sub31.FieldByName('Gname').AsString;
  Sobo21.Edit107.Text:=Base10.T5_Sub32.FieldByName('Hcode').AsString;
  Sobo21.Edit108.Text:=Base10.T5_Sub32.FieldByName('Hname').AsString;
  Sobo21.Label100.Visible:=False;
  Sobo21.Edit106.Visible:=False;
  Sobo21.Edit106.Items.Clear;
  if Base10.T5_Sub31.FieldByName('Gjisa').AsString<>'' then begin
  Sobo21.Label100.Visible:=True;
  Sobo21.Edit106.Visible:=True;
  Sobo21.Edit106.Items.Add(Base10.T5_Sub31.FieldByName('Gjisa').AsString);
  Sobo21.Edit106.ItemIndex:=0;
  end;
  Sobo21.Button101Click(Self);
  end; }
end;

procedure TSobo59_1.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo59_1.DateEdit2ButtonClick(Sender: TObject);
begin
  DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo59_1.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo59_1.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo59_1.Button701Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit104.Text;
  if Edit104.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit104.Text);
  if Seak80.Query1.RecordCount=1 Then begin
    Edit103.Text:=Seak80.Query1Gcode.AsString;
    Edit104.Text:=Seak80.Query1Gname.AsString;
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit103.Text:=Seak80.Query1Gcode.AsString;
    Edit104.Text:=Seak80.Query1Gname.AsString;
  end;
end;

procedure TSobo59_1.Button702Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit106.Text;
  if Edit106.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit106.Text);
  if Seak80.Query1.RecordCount=1 Then begin
    Edit105.Text:=Seak80.Query1Gcode.AsString;
    Edit106.Text:=Seak80.Query1Gname.AsString;
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit105.Text:=Seak80.Query1Gcode.AsString;
    Edit106.Text:=Seak80.Query1Gname.AsString;
  end;
end;

procedure TSobo59_1.DBGrid201Columns8UpdateData(Sender: TObject;
  var Text: String; var Value: Variant; var UseText, Handled: Boolean);
var St2: String;
begin
  if nSqry.Active=True Then begin
    Sqlen := 'Select Time1 From S1_Chek Where '+D_Select+
             'Hcode=''@Hcode'' and Scode=''@Scode'' and '+
             'Gdate=''@Gdate'' and Gcode=''@Gcode'' and '+
             'Jubun=''@Jubun'' and Gjisa=''@Gjisa'' and '+
             'Check<>''@Check'' ';
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Scode', 'X');
    Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
    Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
    Translate(Sqlen, '@Check', 'D');
    if Base10.Seek_Name(Sqlen)='' Then begin

      Sqlen := 'INSERT INTO S1_Chek '+
      '(Hcode, Gdate, Scode, Gcode, '+
      ' Jubun, Gjisa, Gsqut, Yesno, Check, Time1) VALUES '+
      '(''@Hcode'',''@Gdate'',''@Scode'',''@Gcode'', '+
      ' ''@Jubun'',''@Gjisa'',  @Gsqut  ,''@Yesno'',''@Check'', now())';

      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
      Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
      TransAuto(Sqlen, '@Gsqut', nSqry.FieldByName('Gsqut').AsString);
      if nSqry.FieldByName('Yesno').AsString='1' then
      Translate(Sqlen, '@Yesno', '0') else
      Translate(Sqlen, '@Yesno', '1');
      Translate(Sqlen, '@Check', '');

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

      Sqlen := 'Select Time1 From S1_Chek Where '+D_Select+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and '+
               'Gdate=''@Gdate'' and Gcode=''@Gcode'' and '+
               'Jubun=''@Jubun'' and Gjisa=''@Gjisa'' and '+
               'Check<>''@Check'' ';
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Scode', 'X');
      Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
      Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
      Translate(Sqlen, '@Check', 'D');
      St2:=Base10.Seek_Name(Sqlen);

      nSqry.Edit;
      nSqry.FieldByName('Gbigo').AsString:=St2;
    //nSqry.Post;

    end else begin

      Sqlen := 'UPDATE S1_Chek SET '+
      'Yesno=''@Yesno'',Time2=  now() '+'WHERE '+
      'Hcode=''@Hcode'' and Gdate=''@Gdate'' and Scode=''@Scode'' and '+
      'Gcode=''@Gcode'' and Jubun=''@Jubun'' and Gjisa=''@Gjisa'' and Check<>''@Check'' ';

      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
      Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
      if nSqry.FieldByName('Yesno').AsString='1' then
      Translate(Sqlen, '@Yesno', '0') else
      Translate(Sqlen, '@Yesno', '1');
      Translate(Sqlen, '@Check', 'D');

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end;
  end;
end;

end.
