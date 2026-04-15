unit Subu29;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, dxCore, dxButtons,
  DBGridEh, ToolEdit, CornerButton;

type
  TSobo29 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel007: TFlatPanel;
    Panel101: TFlatPanel;
    Panel104: TFlatPanel;
    Panel105: TFlatPanel;
    Panel102: TFlatPanel;
    Panel103: TFlatPanel;
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
    Edit106: TFlatComboBox;
    Panel003: TFlatPanel;
    DBGrid102: TDBGrid;
    Label101: TmyLabel3d;
    Panel106: TFlatPanel;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Label100: TmyLabel3d;
    Edit109: TFlatComboBox;
    Panel300: TFlatPanel;
    myLabel3d2: TmyLabel3d;
    Label102: TmyLabel3d;
    Panel301: TFlatPanel;
    Edit203: TFlatEdit;
    Edit204: TFlatEdit;
    Button801: TFlatButton;
    Edit205: TFlatEdit;
    StaticText1: TStaticText;
    Edit206: TFlatEdit;
    StaticText2: TStaticText;
    Edit207: TFlatEdit;
    StaticText3: TStaticText;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    DateEdit1: TDateEdit;
    Button701: TFlatButton;
    Button702: TFlatButton;
    DBGrid101: TDBGridEh;
    myLabel3d1: TmyLabel3d;
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
    procedure DBGrid102DblClick(Sender: TObject);
    procedure Edit301KeyPress(Sender: TObject; var Key: Char);
    procedure Button801Click(Sender: TObject);
    procedure Edit205Click(Sender: TObject);
    procedure Edit205Exit(Sender: TObject);
    procedure StaticText1Click(Sender: TObject);
    procedure StaticText2Click(Sender: TObject);
    procedure StaticText3Click(Sender: TObject);
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
  Sobo29: TSobo29;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo29.FormActivate(Sender: TObject);
begin
  nForm:='29';
  nSqry:=Base10.T2_Sub91;
  mSqry:=Base10.T2_Sub32;
end;

procedure TSobo29.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo29.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo29:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo29.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo29.Button002Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Button015Click(Self);
  end; }
end;

procedure TSobo29.Button003Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo29.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo29.Button011Click(Sender: TObject);
begin
{ Tong20.DBGridSaveHtml(DBGrid201, Caption); }
end;

procedure TSobo29.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY0(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo29.Button013Click(Sender: TObject);
begin
{ oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1); }
end;

procedure TSobo29.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('29-01');
end;

procedure TSobo29.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('29-02');
end;

procedure TSobo29.Button016Click(Sender: TObject);
begin
  nSqry.First;
  While nSqry.EOF=False do begin
    if(nSqry.FieldByName('Yesno').AsString='1')then begin
    nSqry.Edit;
    nSqry.FieldByName('Yesno').AsString:='2';
    nSqry.Post;
    end;
    nSqry.Next;
  end;
  Tong40.print_29_01(Self);
end;

procedure TSobo29.Button017Click(Sender: TObject);
begin
  nSqry.First;
  While nSqry.EOF=False do begin
    if(nSqry.FieldByName('Yesno').AsString='1')then begin
    nSqry.Edit;
    nSqry.FieldByName('Yesno').AsString:='2';
    nSqry.Post;
    end;
    nSqry.Next;
  end;
  Tong40.print_29_02(Self);
end;

procedure TSobo29.Button018Click(Sender: TObject);
begin
  Seak60.ShowModal;
end;

procedure TSobo29.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont4(DBGrid101);
end;

procedure TSobo29.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo29.Button101Click(Sender: TObject);
var St1,St2,St3,St4: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;

  St1:=Edit101.Text;
  St2:=Edit104.Text;
  St3:=Edit103.Text;
  if mSqry.Locate('Gdate;Bcode;Jubun',VarArrayOf([St1,St2,St3]),[loCaseInsensitive])=False then begin
     mSqry.Append;
     mSqry.FieldByName('Gdate').Value:=Edit101.Text;
     mSqry.FieldByName('Bcode').Value:=Edit104.Text;
     mSqry.FieldByName('Bname').Value:=Edit105.Text;
     mSqry.FieldByName('Jubun').Value:=Edit103.Text;
     mSqry.Post;
  end;

  St1:='Gdate'+'='+#39+Edit101.Text+#39+' and '+
       'Gubun'+'='+#39+Edit102.Text+#39+' and '+
       'Jubun'+'='+#39+Edit103.Text+#39+' and '+
       'Pubun'+'='+#39+Edit106.Text+#39+' and '+
       'Hcode'+'='+#39+Edit107.Text+#39+' and '+
       'Bcode'+' Like '+#39+'%'+Edit104.Text+'%'+#39+' and '+
       'Ocode'+'='+#39+'B'+#39+' and '+
       'Scode'+'='+#39+'X'+#39;
  St2:=' Order By Gdate,Gcode,Gubun,Jubun,ID';

  Sqlen := 'Select * From S1_Ssub Where '+D_Select+St1;

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

    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Gname').AsString='' then
    if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

    if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Bcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Bname').AsString:=Base10.G4_Book.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Gjisa').AsString<>'' then
    nSqry.FieldByName('Gname').AsString:=Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'2')+
    nSqry.FieldByName('Gname').AsString+ Base10.Seek_Jisa(nSqry.FieldByName('Gjisa').AsString,'1');

    //------------------------------------------------------------------------//
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

  nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  nSqry.First;
  Tong20.Srart_29_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=Base10.T2_Sub91BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo29.Button201Click(Sender: TObject);
begin
  oSqry:=Seek70.Query1;
  oSqry.First;
  While oSqry.EOF=False do begin
    if(oSqry.FieldByName('Gqut1').AsString<>'')and
      (oSqry.FieldByName('Gqut1').AsInteger<>0)Then begin
      nSqry.Append;
      if Seek70.Edit2.Text<>'' Then
      Jubun:=Seek70.Edit2.Text else
      Jubun:=Edit103.Text;
      Bcode:=Seek70.Edit1.Text;
      Gcode:=oSqry.FieldByName('Gcode').AsString;
      nSqry.FieldByName('Gcode').Value:=Gcode;
      nSqry.FieldByName('Bcode').Value:=Bcode;
      nSqry.FieldByName('Jubun').Value:=Jubun;
      nSqry.FieldByName('Pubun').Value:=Edit106.Text;
      nSqry.FieldByName('Hcode').Value:=Edit107.Text;
      nSqry.FieldByName('Gname').AsString :=oSqry.FieldByName('Gname').AsString;
      nSqry.FieldByName('Gjisa').AsString :=oSqry.FieldByName('Gjisa').AsString;
      nSqry.FieldByName('Gsqut').AsInteger:=oSqry.FieldByName('Gqut1').AsInteger;
      nSqry.FieldByName('Grat1').AsInteger:=oSqry.FieldByName('Grat1').AsInteger;

      if oSqry.FieldByName('Gjisa').AsString<>'' then
      nSqry.FieldByName('Gname').AsString:=Base10.Seek_Jisa(oSqry.FieldByName('Gjisa').AsString,'2')+
      nSqry.FieldByName('Gname').AsString+ Base10.Seek_Jisa(oSqry.FieldByName('Gjisa').AsString,'1');

      Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Gname,Gjeja,Gdang,Scode From G4_Book '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Bcode').AsString);
      Translate(Sqlen, '@Hcode', Edit107.Text );
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        nSqry.FieldByName('Ocode').Value:='B';
        nSqry.FieldByName('Bname').Value:=Base10.Socket.GetData(1, 7);
        nSqry.FieldByName('Gjeja').Value:=Base10.Socket.GetData(1, 8);
        nSqry.FieldByName('Gdang').Value:=StrToIntDef(Base10.Socket.GetData(1, 9),0);
        nSqry.FieldByName('Jeago').AsFloat:=
        Tong20.PrinJing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,Edit107.Text,0);
      end;

      Tong20.PrinYing(Self);
      nSqry.Post;
    end;
    oSqry.Next;
  end;
  nSqry.First; DBGrid101.SetFocus;
end;

procedure TSobo29.Button301Click(Sender: TObject);
var St1,St2: String;
begin
  Base10.OpenShow(mSqry);

  St1:='Gdate'+'='+#39+Edit101.Text+#39+' and '+
       'Gubun'+'='+#39+Edit102.Text+#39+' and '+
       'Pubun'+'='+#39+Edit106.Text+#39+' and '+
       'Scode'+'='+#39+'X'+#39+' and '+
       'Ocode'+'='+#39+'B'+#39+' and '+
       'Hcode'+'='+#39+Edit107.Text+#39;
  St2:=' Group By Gdate,Bcode,Jubun';

  Sqlen := 'Select Gdate,Bcode,Jubun From S1_Ssub Where '+D_Select+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(mSqry)
  else ShowMessage(E_Open);

  mSqry.First;
  While mSqry.EOF=False do begin

    mSqry.Edit;

    Sqlen := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', mSqry.FieldByName('Bcode').AsString);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      mSqry.FieldByName('Bname').Value:=Base10.Socket.GetData(1, 1);
    end;

    mSqry.Post;
    mSqry.Next;
  end;

  mSqry.IndexName := 'IDX'+'BCODE'+'DOWN';
  mSqry.First;
end;

procedure TSobo29.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit103.Focused=True)and(Edit103.SelStart=02)and(Length(Trim(Edit103.Text))=02))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit104.Focused=True)and(Edit104.SelStart=10)and(Length(Trim(Edit104.Text))=10))or
    ((Edit105.Focused=True)and(Edit105.SelStart=40)and(Length(Trim(Edit105.Text))=40))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo29.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo29.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo29.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo29.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo29.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Button301Click(Self);
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo29.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo29.Edit113KeyPress(Sender: TObject; var Key: Char);
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
    end else
    if Edits.DropDownCount=8 Then begin
      Key:=#0; SendMessage(Hands, cb_ShowDropDown, 1, 0);
    end;
  end;
end;

procedure TSobo29.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit106;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo29.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if Edit108.Focused=True Then begin
       Edit107.Text:='';
    if Edit108.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit108.Text;
    Seak80.FilterTing(Edit108.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Button301Click(Self);
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Button301Click(Self);
    end;
    end;
  end else
  if(Edit104.Focused=True)or(Edit105.Focused=True)Then begin
    if Edit104.Focused=True Then begin
    { if Edit104.Text='' Then begin
        Button101Click(Self); Exit;
      end; }
      Seek40.Edit1.Text:=Edit104.Text;
      Seek40.FilterTing(Edit104.Text,Edit107.Text);
      if Seek40.Query1.IsEmpty=True Then Exit;
    end;
    if Edit105.Focused=True Then begin
      Seek40.Edit1.Text:=Edit105.Text;
      Seek40.FilterTing(Edit105.Text,Edit107.Text);
      if Seek40.Query1.IsEmpty=True Then Exit;
    end;
    if Seek40.Query1.RecordCount=1 Then begin
    //SelectNext(ActiveControl as TWinControl, True, True);
      Edit104.Text:=Seek40.Query1Gcode.AsString;
      Edit105.Text:=Seek40.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seek40.ShowModal=mrOK Then begin
    //SelectNext(ActiveControl as TWinControl, True, True);
      Edit104.Text:=Seek40.Query1Gcode.AsString;
      Edit105.Text:=Seek40.Query1Gname.AsString;
      Button101Click(Self);
    end;
  end;
  end;
end;

procedure TSobo29.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo29.DBGrid101Exit(Sender: TObject);
begin
  Base10.T2_Sub91BeforeClose(Base10.T2_Sub91);
end;

procedure TSobo29.DBGrid101Enter(Sender: TObject);
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
    DGrid.Columns.Items[0].PickList.Add('비품');
    DGrid.Columns.Items[0].PickList.Add('정품');
    DGrid.Columns.Items[0].PickList.Add('폐기');
    DGrid.Columns.Items[0].PickList.Add('반품');
    DGrid.Columns.Items[0].PickList.Add(' 질 ');
  end;
  DGrid.SelectedIndex:=0;
  if nSqry.Active=True Then begin
  if(nSqry.FieldByName('Gdate').AsString<>Edit101.Text)or
    (nSqry.FieldByName('Gubun').AsString<>Edit102.Text)or
    (nSqry.FieldByName('Jubun').AsString<>Edit103.Text)or
    (nSqry.FieldByName('Bcode').AsString<>Edit104.Text)or
    (nSqry.FieldByName('Hcode').AsString<>Edit107.Text)Then
     Button101Click(Self);
  end;
  Base10.T2_Sub91AfterScroll(Base10.T2_Sub91);
end;

procedure TSobo29.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=0 Then begin

      Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Gname,Gjeja,Gdang,Ocode From G4_Book '+
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

      Seek40.Edit1.Text:=nSqry.FieldByName('Bcode').AsString;
      Seek40.FilterTing(nSqry.FieldByName('Bcode').AsString,Edit107.Text);
      if Seek40.Query1.RecordCount=1 Then begin
        Code1:=Seek40.Query1Gbjil.AsString;
      //nSqry.FieldByName('Ocode').Value:=Seek40.Query1Scode.Value;
        nSqry.FieldByName('Bcode').Value:=Seek40.Query1Gcode.Value;
        nSqry.FieldByName('Bname').Value:=Seek40.Query1Gname.Value;
        nSqry.FieldByName('Gdang').Value:=Seek40.Query1Gdang.Value;
        nSqry.FieldByName('Jeago').AsFloat:=
        Tong20.PrinJing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,Edit107.Text,0);
      end else
      if Seek40.ShowModal=mrOK Then begin
        Code1:=Seek40.Query1Gbjil.AsString;
      //nSqry.FieldByName('Ocode').Value:=Seek40.Query1Scode.Value;
        nSqry.FieldByName('Bcode').Value:=Seek40.Query1Gcode.Value;
        nSqry.FieldByName('Bname').Value:=Seek40.Query1Gname.Value;
        nSqry.FieldByName('Gdang').Value:=Seek40.Query1Gdang.Value;
        nSqry.FieldByName('Jeago').AsFloat:=
        Tong20.PrinJing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,Edit107.Text,0);
      end;
    //if nSqry.FieldByName('Ocode').AsString='' Then
    //   nSqry.FieldByName('Ocode').AsString:='B';

    end else
    if SIndexs=1 Then begin
      if nSqry.FieldByName('Gcode').AsString='' Then Exit;
      Seek10.Edit1.Text:=nSqry.FieldByName('Gcode').AsString;
      Seek10.FilterTing(nSqry.FieldByName('Gcode').AsString,Edit107.Text);
      if Seek10.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Gcode').Value:=Seek10.Query1Gcode.Value;
        nSqry.FieldByName('Gname').Value:=Seek10.Query1Gname.Value;
        SIndexs:=SIndexs+1;
      end else
      if Seek10.ShowModal=mrOK Then begin
        nSqry.FieldByName('Gcode').Value:=Seek10.Query1Gcode.Value;
        nSqry.FieldByName('Gname').Value:=Seek10.Query1Gname.Value;
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;

      Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Hcode', '');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        Tong20.PrinZing(Self);
        if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
      end else begin
      //--//
      Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
               'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
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

      Tong20.PrinRat1(Edit107.Text,nSqry.FieldByName('Gcode').AsString,nSqry.FieldByName('Bcode').AsString);

      Tong20.PrinYing(Self);
    end else
    if SIndexs=3 Then begin
      Tong20.PrinYing(Self);
      Tong20.PrinSing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,Edit107.Text,nSqry.FieldByName('Gsqut').Value);
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

procedure TSobo29.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
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
      nSqry.Append; DBGrid101.SelectedIndex:=0;
    end;
  end;
  if Key=VK_F2 Then Button016Click(Self);
  if Key=VK_F3 Then Button017Click(Self);
  if Key=VK_F4 Then Seek70.ShowModal;
  if Key=VK_F7 Then Seak70.ShowModal;
  if sColumn=False Then begin
    if nSqry.IsEmpty=False Then
    if Key=VK_DELETE Then Base10.T2_Sub91AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo29.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo29.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo29.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo29.DBGrid201TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(mSqry,Column);
end;

procedure TSobo29.DataSource1DataChange(Sender: TObject; Field: TField);
begin
{ if(nSqry.FieldByName('Bcode').AsString<>'') Then begin
  Edit103.Text:=nSqry.FieldByName('Jubun').AsString;
  Edit104.Text:=nSqry.FieldByName('Bcode').AsString;
  Edit105.Text:=nSqry.FieldByName('Bname').AsString;
  end; }
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo29.DataSource2DataChange(Sender: TObject; Field: TField);
begin
//Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo29.DBGrid102DblClick(Sender: TObject);
begin
  if mSqry.FieldByName('Bcode').Value<>'' then begin
    Edit104.Text:=mSqry.FieldByName('Bcode').Value;
    Edit105.Text:=mSqry.FieldByName('Bname').Value;
    Edit103.Text:=mSqry.FieldByName('Jubun').Value;
    Button101Click(Self);
  end;
end;

procedure TSobo29.Edit301KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  Button801Click(Self);
end;

procedure TSobo29.Button801Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
    nSqry.First;
    While nSqry.EOF=False do begin

    Sqlen := 'Select Gbigo From S1_Memo Where '+D_Select+
             'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
             'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
             'Scode=''@Scode'' and Gjisa=''@Gjisa'' and '+
             'Hcode=''@Hcode'' and '+
             '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';
    Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
    Translate(Sqlen, '@Gubun', nSqry.FieldByName('Gubun').AsString);
    Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
    Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Ocode', 'B');
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin

      Sqlon :=
      'UPDATE S1_Memo SET Gbigo=''@Gbigo'' ,Sbigo=''@Sbigo'' ,'+
      ' Gtel1=''@Gtel1'' ,Gtel2=''@Gtel2'' ,Gname=''@Gname'' ';
      Sqlen :=
      ' WHERE Gdate=''@Gdate'' and Gubun=''@Gubun'' '+
      '  and  Jubun=''@Jubun'' and Gcode=''@Gcode'' '+
      '  and  Scode=''@Scode'' and Gjisa=''@Gjisa'' '+
      '  and  Hcode=''@Hcode'' and '+
      '('+'Ocode is null '+' or '+'Ocode'+'='+#39+'B'+#39+')';

      Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gubun', nSqry.FieldByName('Gubun').AsString);
      Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
      Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
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

      Base10.Socket.RunSQL(Sqlon+Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end else begin

      Sqlon :=
      'INSERT INTO S1_Memo '+
      '(Gdate, Gubun, Jubun, Gcode, Scode, Gjisa, Hcode, '+
      ' Ocode, Gbigo, Sbigo, Gtel1, Gtel2, Gname) VALUES ';
      Sqlen :=
      '(''@Gdate'',''@Gubun'',''@Jubun'',''@Gcode'', '+
      ' ''@Scode'',''@Gjisa'',''@Hcode'',''@Ocode'', '+
      ' ''@Gbigo'',''@Sbigo'',''@Gtel1'',''@Gtel2'',''@Gname'' )';

      Translate(Sqlen, '@Gdate', nSqry.FieldByName('Gdate').AsString);
      Translate(Sqlen, '@Gubun', nSqry.FieldByName('Gubun').AsString);
      Translate(Sqlen, '@Jubun', nSqry.FieldByName('Jubun').AsString);
      Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      Translate(Sqlen, '@Scode', nSqry.FieldByName('Scode').AsString);
      Translate(Sqlen, '@Gjisa', nSqry.FieldByName('Gjisa').AsString);
      Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
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

      Base10.Socket.RunSQL(Sqlon+Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end;

    nSqry.Next;
    end;
    DBGrid101.SetFocus;
    ShowMessage('전체메모 저장완료');
  end;
end;

procedure TSobo29.Edit205Click(Sender: TObject);
begin
  if Edit205.Focused=True then
  StaticText1.Visible:=False;
  if Edit206.Focused=True then
  StaticText2.Visible:=False;
  if Edit207.Focused=True then
  StaticText3.Visible:=False;
end;

procedure TSobo29.Edit205Exit(Sender: TObject);
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

procedure TSobo29.StaticText1Click(Sender: TObject);
begin
  StaticText1.Visible:=False;
  Edit205.SetFocus;
end;

procedure TSobo29.StaticText2Click(Sender: TObject);
begin
  StaticText2.Visible:=False;
  Edit206.SetFocus;
end;

procedure TSobo29.StaticText3Click(Sender: TObject);
begin
  StaticText3.Visible:=False;
  Edit207.SetFocus;
end;

procedure TSobo29.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo29.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo29.Button701Click(Sender: TObject);
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

procedure TSobo29.Button702Click(Sender: TObject);
begin
  Seek40.Edit1.Text:=Edit104.Text;
  if Edit104.Text='' then
  Seek40.FilterTing('',Edit107.Text) else
  Seek40.FilterTing(Edit104.Text,Edit107.Text);
  if Seek40.ShowModal=mrOK Then begin
      Edit104.Text:=Seek40.Query1Gcode.AsString;
      Edit105.Text:=Seek40.Query1Gname.AsString;
      Button101Click(Self);
  end;
end;

end.
