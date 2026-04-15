unit Subu22_1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, DBGridEh, Tong07,
  DBClient, dxCore, dxButtons;

type
  TSobo22_1 = class(TForm)
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
    StBar101: TStatusBar;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatComboBox;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    DBGrid101: TDBGridEh;
    myLabel3d1: TmyLabel3d;
    Panel401: TFlatPanel;
    Label100: TmyLabel3d;
    Edit106: TFlatComboBox;
    Edit109: TFlatEdit;
    Button901: TFlatButton;
    T2_Sub21: TClientDataSet;
    T2_Sub21ID: TFloatField;
    T2_Sub21IDNUM: TFloatField;
    T2_Sub21GDATE: TStringField;
    T2_Sub21SDATE: TStringField;
    T2_Sub21GCODE: TStringField;
    T2_Sub21GNAME: TStringField;
    T2_Sub21HCODE: TStringField;
    T2_Sub21OCODE: TStringField;
    T2_Sub21BCODE: TStringField;
    T2_Sub21BNAME: TStringField;
    T2_Sub21GJEJA: TStringField;
    T2_Sub21GUBUN: TStringField;
    T2_Sub21JUBUN: TStringField;
    T2_Sub21PUBUN: TStringField;
    T2_Sub21GSQUT: TFloatField;
    T2_Sub21QSQUT: TFloatField;
    T2_Sub21GDANG: TFloatField;
    T2_Sub21GRAT1: TSmallintField;
    T2_Sub21GSSUM: TFloatField;
    T2_Sub21JEAGO: TFloatField;
    T2_Sub21GBIGO: TStringField;
    T2_Sub21YESNO: TStringField;
    T2_Sub21GJISA: TStringField;
    T2_Sub22: TClientDataSet;
    T2_Sub22ID: TFloatField;
    T2_Sub22IDNUM: TFloatField;
    T2_Sub22GDATE: TStringField;
    T2_Sub22SCODE: TStringField;
    T2_Sub22GCODE: TStringField;
    T2_Sub22GNAME: TStringField;
    T2_Sub22HCODE: TStringField;
    T2_Sub22OCODE: TStringField;
    T2_Sub22BCODE: TStringField;
    T2_Sub22BNAME: TStringField;
    T2_Sub22GJEJA: TStringField;
    T2_Sub22GUBUN: TStringField;
    T2_Sub22JUBUN: TStringField;
    T2_Sub22PUBUN: TStringField;
    T2_Sub22GSQUT: TFloatField;
    T2_Sub22QSQUT: TFloatField;
    T2_Sub22GDANG: TFloatField;
    T2_Sub22GRAT1: TSmallintField;
    T2_Sub22GSSUM: TFloatField;
    T2_Sub22JEAGO: TFloatField;
    T2_Sub22GBIGO: TStringField;
    T2_Sub22YESNO: TStringField;
    T2_Sub22GJISA: TStringField;
    T2_Sub21MEMO1: TMemoField;
    StBar102: TStatusBar;
    T2_Sub21TIME1: TStringField;
    T2_Sub21TIME3: TStringField;
    T2_Sub21CODE1: TStringField;
    T2_Sub21CODE2: TStringField;
    T2_Sub21CODE3: TStringField;
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
    procedure Button601Click(Sender: TObject);
    procedure Button602Click(Sender: TObject);
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
    procedure DBGrid101TitleClick(Column: TColumn);
    procedure DBGrid201TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure MultiSelect(Sender: TObject);
    procedure Edit301KeyPress(Sender: TObject; var Key: Char);
    procedure Button701Click(Sender: TObject);
    function Idnum(Sender: TObject): Integer;
    procedure Jubun(Sender: TObject);
    procedure Button901Click(Sender: TObject);

    procedure T2_Sub21AfterCancel(DataSet: TDataSet);
    procedure T2_Sub21AfterScroll(DataSet: TDataSet);
    procedure T2_Sub21AfterPost(DataSet: TDataSet);
    procedure T2_Sub21AfterDelete(DataSet: TDataSet);
    procedure T2_Sub21BeforePost(DataSet: TDataSet);
    procedure T2_Sub21BeforeClose(DataSet: TDataSet);
    procedure T2_Sub21NewRecord(DataSet: TDataSet);

  private
    { Private declarations }
  public
    Frame: TFrame;
    FTong07: TTong70;
    { Public declarations }
  end;

var
  Sobo22_1: TSobo22_1;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib, Subu20,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo22_1.FormActivate(Sender: TObject);
begin
  nForm:='22_1';
  nSqry:=T2_Sub21;
  mSqry:=T2_Sub22;
end;

procedure TSobo22_1.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo22_1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo22_1:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo22_1.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo22_1.Button002Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Button015Click(Self);
  end; }
end;

procedure TSobo22_1.Button003Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo22_1.Button004Click(Sender: TObject);
begin
{ if(Base10.Database.Database='book_07_db')or
    (Base10.Database.Database='chul_02_db')then begin
    Base10.OpenExit(nSqry);
    Tong20.Srart_22_01(Self);
    if Sobo22_1.Caption='입고명세서-(온라인)' then
    Sobo22_1.Caption:='입고명세서-(창고)' else
    Sobo22_1.Caption:='입고명세서-(온라인)';
    Edit101.SetFocus;
  end; }
end;

procedure TSobo22_1.Button005Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
    if(nSqry.FieldByName('Yesno').Value='1')or
      (nSqry.FieldByName('Yesno').Value='2')or
      (System_Data > Edit101.Text)then begin
    end else begin
     Application.CreateForm(TSobo20, Sobo20);
     Sobo20.ShowModal;
    end;
  end; }
end;

procedure TSobo22_1.Button006Click(Sender: TObject);
begin
     Button018Click(Self);
end;

procedure TSobo22_1.Button007Click(Sender: TObject);
begin
  if nSqry.Active=True Then
     Button401Click(Self);
end;

procedure TSobo22_1.Button008Click(Sender: TObject);
begin
  if nSqry.Active=True Then
     Button601Click(Self);
end;

procedure TSobo22_1.Button009Click(Sender: TObject);
begin
  if nSqry.Active=True Then
     Button602Click(Self);
end;

procedure TSobo22_1.Button010Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo22_1.Button011Click(Sender: TObject);
begin
{ Tong20.DBGridSaveHtml(DBGrid201, Caption); }
  if nSqry.Active=True Then
     Button501Click(Self);
end;

procedure TSobo22_1.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
//Base10.ColumnX0(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo22_1.Button013Click(Sender: TObject);
begin
  oSqry:=nSqry;
//Base10.ColumnX4(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo22_1.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('22-01');
end;

procedure TSobo22_1.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('22-02');
end;

procedure TSobo22_1.Button016Click(Sender: TObject);
begin
//Tong40.print_22_01(Self);
end;

procedure TSobo22_1.Button017Click(Sender: TObject);
begin
//Tong40.print_22_02(Self);
end;

procedure TSobo22_1.Button018Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
    Sqlen := 'Select Scode From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', Hnnnn);
    if Base10.Seek_Name(Sqlen)<>'' then begin
      ShowMessage(E_Yesno);
      Exit;
    end;

    nSqry.First;
    While nSqry.EOF=False do begin
      if nSqry.FieldByName('Yesno').Value='0' then begin
      nSqry.Edit;
      nSqry.FieldByName('Yesno').Value:='1';
      nSqry.Post;
      end;
      nSqry.Next;
    end;
    Edit104.SetFocus;
  end; }
end;

procedure TSobo22_1.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Button021Click(Sender: TObject);
begin
//Tong20.DBGridFont2(DBGrid101,StBar101);
end;

procedure TSobo22_1.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Button023Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
    Sqlen := 'UPDATE G7_Ggeo SET Scode=''@Scode'' Where Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', 'O');
    Translate(Sqlen, '@Gcode', Hnnnn);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
    ShowMessage('체크완료');
  end; }
end;

procedure TSobo22_1.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Button101Click(Sender: TObject);
var St1,St2: String;
begin

{ if System_Data > Edit101.Text then begin
     ShowMessage('거래일자를 다시 선택해 주십시오.');
     Edit101.SetFocus;
     Exit;
  end; }

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;

  Sqlen := 'Select * From S4_Ssub Where '+D_Select+
           'Code2=''@Code2'' and Code3<>''@Code3'' ';

  if S_Where1<>'' then
  Sqlen:=Sqlen+' and '+S_Where1;

  Translate(Sqlen, '@Gdate', Edit101.Text);
  Translate(Sqlen, '@Code2', 'O');
  Translate(Sqlen, '@Code3', 'O');

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  nSqry.First;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    St2:='';
    if Base10.G7_Ggeo.Locate('Gcode',nSqry.FieldByName('Hcode').AsString,[loCaseInsensitive])=true then
    St2:=Base10.G7_Ggeo.FieldByName('Gname').AsString;

    nSqry.Edit;
    nSqry.FieldByName('Gname').AsString:=St2;
    nSqry.Post;
    nSqry.Next;
  end;

  Button301Click(Self);

  nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  nSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=T2_Sub21BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo22_1.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Button301Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Button401Click(Sender: TObject);
begin
{ if(nSqry.FieldByName('Yesno').Value='1')or
    (nSqry.FieldByName('Yesno').Value='2')or
    (System_Data > Edit101.Text)then begin
  end else begin
  Panel401.Visible:=True;
  if Assigned(Frame) then
     FreeAndNil(Frame);
  FTong07 := TTong70.Create(Self);
  Frame := FTong07;
  Frame.Parent := Panel401;
  FTong07.Edit101.SetFocus;
  FTong07.FormShow(Self);
  end; }
end;

procedure TSobo22_1.Button501Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Button601Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Button602Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Button901Click(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit103.Focused=True)and(Edit103.SelStart=02)and(Length(Trim(Edit103.Text))=02))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit104.Focused=True)and(Edit104.SelStart=05)and(Length(Trim(Edit104.Text))=05))or
    ((Edit105.Focused=True)and(Edit105.SelStart=24)and(Length(Trim(Edit105.Text))=24))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo22_1.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo22_1.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo22_1.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo22_1.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo22_1.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo22_1.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo22_1.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo22_1.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo22_1.Edit114KeyPress(Sender: TObject; var Key: Char);
var St1: String;
begin
  if Key=#13 Then begin
    if Edit104.Focused=True Then begin
      Seek20.Edit1.Text:=Edit104.Text;
    //Seek20.FilterTing(Edit104.Text);
      if Seek20.Query1.IsEmpty=True Then Exit;
    end;
    if Edit105.Focused=True Then begin
      Seek20.Edit1.Text:=Edit105.Text;
    //Seek20.FilterTing(Edit105.Text);
      if Seek20.Query1.IsEmpty=True Then Exit;
    end;
    if Seek20.Query1.RecordCount=1 Then begin
    //SelectNext(ActiveControl as TWinControl, True, True);
      Edit104.Text:=Seek20.Query1Gcode.AsString;
      Edit105.Text:=Seek20.Query1Gname.AsString;
    { Edit201.Text:=Seek20.Query1Gtel1.AsString+'-'+Seek20.Query1Gtel2.AsString;
      Edit202.Text:=Seek20.Query1Gadd1.AsString+' '+Seek20.Query1Gadd2.AsString; }

    { Tong40.SetTring01('Y',Edit101.Text,'',Edit104.Text,'');

      sSqry.First;
      While sSqry.EOF=False do begin
        Edit203.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Goqut').AsFloat )]);
        Edit204.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Gosum').AsFloat )]);
        Edit205.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Gbqut').AsFloat )]);
        Edit206.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Gbsum').AsFloat )]);
        Edit207.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Gsusu').AsFloat )]);
        Edit208.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('GsumX').AsFloat )]);
        sSqry.Next;
      end; }

      if(Base10.Database.Database='book_07_db')or
        (Base10.Database.Database='chul_02_db')then begin
        if Copy(Edit104.Text,1,1)='9' then
        St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
             'Hcode'+'='+#39+Hnnnn+#39+' and '+
             'Scode'+'='+#39+'Y'+#39 else
        St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
             'Hcode'+'='+#39+Hnnnn+#39+' and '+
             'Scode'+'='+#39+'Y'+#39;
      end else begin
        if Copy(Edit104.Text,1,1)='9' then
        St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
             'Hcode'+'='+#39+Hnnnn+#39+' and '+
             'Scode'+'='+#39+'Y'+#39 else
        St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
             'Hcode'+'='+#39+''+#39+' and '+
             'Scode'+'='+#39+'Y'+#39;
      end;

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
        Jubun(Self);
      //Button101Click(Self);
      end;

    end else
    if Seek20.ShowModal=mrOK Then begin
    //SelectNext(ActiveControl as TWinControl, True, True);
      Edit104.Text:=Seek20.Query1Gcode.AsString;
      Edit105.Text:=Seek20.Query1Gname.AsString;
    { Edit201.Text:=Seek20.Query1Gtel1.AsString+'-'+Seek20.Query1Gtel2.AsString;
      Edit202.Text:=Seek20.Query1Gadd1.AsString+' '+Seek20.Query1Gadd2.AsString; }

    { Tong40.SetTring01('Y',Edit101.Text,'',Edit104.Text,'');

      sSqry.First;
      While sSqry.EOF=False do begin
        Edit203.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Goqut').AsFloat )]);
        Edit204.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Gosum').AsFloat )]);
        Edit205.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Gbqut').AsFloat )]);
        Edit206.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Gbsum').AsFloat )]);
        Edit207.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('Gsusu').AsFloat )]);
        Edit208.Text:=Format('%13s',[FormatFloat('#,###,###,##0',sSqry.FieldByName('GsumX').AsFloat )]);
        sSqry.Next;
      end; }

      if(Base10.Database.Database='book_07_db')or
        (Base10.Database.Database='chul_02_db')then begin
        if Copy(Edit104.Text,1,1)='9' then
        St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
             'Hcode'+'='+#39+Hnnnn+#39+' and '+
             'Scode'+'='+#39+'Y'+#39 else
        St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
             'Hcode'+'='+#39+Hnnnn+#39+' and '+
             'Scode'+'='+#39+'Y'+#39;
      end else begin
        if Copy(Edit104.Text,1,1)='9' then
        St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
             'Hcode'+'='+#39+Hnnnn+#39+' and '+
             'Scode'+'='+#39+'Y'+#39 else
        St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
             'Hcode'+'='+#39+''+#39+' and '+
             'Scode'+'='+#39+'Y'+#39;
      end;

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
        Jubun(Self);
      //Button101Click(Self);
      end;

    end;
  end;
end;

procedure TSobo22_1.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo22_1.DBGrid101Exit(Sender: TObject);
begin
  T2_Sub21BeforeClose(T2_Sub21);
end;

procedure TSobo22_1.DBGrid101Enter(Sender: TObject);
var DGrid: TDBGridEh;
begin
  DGrid:=DBGrid101;
  DGrid.SelectedIndex:=0;
  if nSqry.Active=True Then begin
     Button101Click(Self);
  end;
  T2_Sub21AfterScroll(T2_Sub21);
end;

procedure TSobo22_1.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
    i: Integer;
begin
{ if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=0 Then begin
    end else
    if SIndexs=1 Then begin
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end; }
end;

procedure TSobo22_1.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
{ if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    if SIndexs=0 Then begin
    end else
    if SIndexs=7 Then begin
      nSqry.Append; DBGrid101.SelectedIndex:=0;
    end;
  end;
  if sColumn=False Then begin

    if(nSqry.FieldByName('Code2').Value<>'O')then begin
      if nSqry.IsEmpty=False Then
      if Key=VK_DELETE Then T2_Sub21AfterDelete(nSqry);
    end;

    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end; }
end;

procedure TSobo22_1.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo22_1.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo22_1.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo22_1.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo22_1.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  if nSqry.FieldByName('Code3').AsString='O' then
  DBGrid101.ReadOnly:=True
  else
  DBGrid101.ReadOnly:=False;

  StBar101.Panels.Items[1].Text:=nSqry.FieldByName('Time1').AsString;
  StBar102.Panels.Items[1].Text:=nSqry.FieldByName('Time3').AsString;
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo22_1.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo22_1.MultiSelect(Sender: TObject);
begin
//
end;

procedure TSobo22_1.Edit301KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  Button701Click(Self);
end;

procedure TSobo22_1.Button701Click(Sender: TObject);
begin
//
end;

function TSobo22_1.Idnum(Sender: TObject): Integer;
var p_Idnum: Integer;
    Str: String;
begin
  Sqlen := 'Select Max(Idnum) From S4_Ssub Where '+D_Select+
           'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
           'Gubun=''@Gubun'' and Jubun=''@Jubun'' and '+
           'Gcode=''@Gcode'' and Scode=''@Scode'' and Gjisa=''@Gjisa''';

  Translate(Sqlen, '@Hcode', Hnnnn);
  Translate(Sqlen, '@Gdate', Edit101.Text);
  Translate(Sqlen, '@Gubun', Edit102.Text);
  Translate(Sqlen, '@Jubun', Edit103.Text);
  Translate(Sqlen, '@Gcode', Edit104.Text);
  Translate(Sqlen, '@Gjisa', Edit106.Text);
  Translate(Sqlen, '@Scode', 'Y');
  Str:=Base10.Seek_Name(Sqlen);

  if Str<>'' then begin
    p_Idnum := StrToIntDef(Str,0);
    Edit109.Text:=Format('%05s',[FormatFloat('00000',p_Idnum)] );
  end else begin
    Sqlen := 'Select Max(Idnum) From S4_Ssub Where '+D_Select+
             'Hcode=''@Hcode'' and Gdate=''@Gdate'' and '+
             'Gubun=''@Gubun'' and Scode=''@Scode'' ';

    Translate(Sqlen, '@Hcode', Hnnnn);
    Translate(Sqlen, '@Gdate', Edit101.Text);
    Translate(Sqlen, '@Gubun', Edit102.Text);
    Translate(Sqlen, '@Scode', 'Y');
    Str:=Base10.Seek_Name(Sqlen);

    p_Idnum := StrToIntDef(Str,0)+1;
    Edit109.Text:=Format('%05s',[FormatFloat('00000',p_Idnum)] );
  end;
end;

procedure TSobo22_1.Jubun(Sender: TObject);
var MeDlg: Integer;
    p_Jubun: Integer;
begin
  Sqlen := 'Select Max(Jubun),Count(*) From S4_Ssub Where '+D_Select+
           'Hcode=''@Hcode'' and Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
           'Gcode=''@Gcode'' and Scode=''@Scode'' and Gjisa=''@Gjisa''';
  Translate(Sqlen, '@Hcode', Hnnnn);
  Translate(Sqlen, '@Gdate', Edit101.Text);
  Translate(Sqlen, '@Gubun', Edit102.Text);
  Translate(Sqlen, '@Gcode', Edit104.Text);
  Translate(Sqlen, '@Gjisa', Edit106.Text);
  Translate(Sqlen, '@Scode', 'Y');
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    if(Base10.Socket.GetData(1, 1)>'10') and
      (Base10.Socket.GetData(1, 2)<>'0') then begin
      MeDlg := MessageDlg('입력된 자료가 있습니다.'+#10+#13+'새로운 전표를 입력할려면(Yes), 불러와서 수정할려면(No)', mtConfirmation, [mbYes, mbNo], 0);
      case MeDlg of
      mrYes: begin

        p_Jubun:=StrToIntDef(Base10.Socket.GetData(1, 1),0)+1;
        Edit103.Text:=Format('%02s',[FormatFloat('00',p_Jubun)] );

        Idnum(Self);
        Button101Click(Self);

      end;
      mrNo: begin

        Edit103.Text:='';
        p_Jubun:=StrToIntDef(Base10.Socket.GetData(1, 1),0)+0;
        if Base10.Socket.GetData(1, 1)<>'' then
        Edit103.Text:=Format('%02s',[FormatFloat('00',p_Jubun)] );

        Idnum(Self);
        Button101Click(Self);

      end; end;

    end else begin
        Edit103.Text:='';
        p_Jubun:=11;
      //if Base10.Socket.GetData(1, 1)<>'' then
        Edit103.Text:=Format('%02s',[FormatFloat('00',p_Jubun)] );

        Idnum(Self);
        Button101Click(Self);
    end;

  end;
end;

//--입고명세서--//
procedure TSobo22_1.T2_Sub21AfterCancel(DataSet: TDataSet);
begin
  T2_Sub21AfterScroll(T2_Sub21);
end;

procedure TSobo22_1.T2_Sub21AfterScroll(DataSet: TDataSet);
begin
//
end;

procedure TSobo22_1.T2_Sub21AfterPost(DataSet: TDataSet);
begin
//
end;

procedure TSobo22_1.T2_Sub21AfterDelete(DataSet: TDataSet);
var MeDlg: Integer;
begin

  MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
  case MeDlg of
  mrYes: begin

    if D_Select='' then begin
      Sqlen := 'DELETE FROM S4_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub21ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub21Gdate.AsString);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end else begin
      Sqlen := 'UPDATE S4_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
      TransAuto(Sqlen, '@ID',    T2_Sub21ID.AsString);
      Translate(Sqlen, '@Gdate', T2_Sub21Gdate.AsString);
      Translate(Sqlen, '@Scode', '2');
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
    end;

    T2_Sub21.Delete;

  end; end;

end;

procedure TSobo22_1.T2_Sub21BeforePost(DataSet: TDataSet);
begin

  if(T2_Sub21.State=dsInsert)Then begin

    Sqlon := 'INSERT INTO S4_Ssub '+
    '(Gdate, Sdate, Hcode, Bcode, Gsqut, Gdang, '+
    ' Memo1, Gbigo, Code1, Code2, Code3, Time1) VALUES ';
    Sqlen :=
    '(''@Gdate'',''@Sdate'',''@Hcode'',''@Bcode'',  @Gsqut  ,  @Gdang  , '+
    ' ''@Memo1'',''@Gbigo'',''@Code1'',''@Code2'',''@Code3'',  now())    ';

    Translate(Sqlen, '@Gdate', T2_Sub21Gdate.AsString);
    Translate(Sqlen, '@Sdate', T2_Sub21Sdate.AsString);
    Translate(Sqlen, '@Hcode', T2_Sub21Hcode.AsString);
    Translate(Sqlen, '@Bcode', T2_Sub21Bcode.AsString);
    TransAuto(Sqlen, '@Gsqut', T2_Sub21Gsqut.AsString);
    TransAuto(Sqlen, '@Gdang', T2_Sub21Gdang.AsString);
    Translate(Sqlen, '@Memo1', T2_Sub21Memo1.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub21Gbigo.AsString);
    Translate(Sqlen, '@Code1', T2_Sub21Code1.AsString);
    Translate(Sqlen, '@Code2', T2_Sub21Code2.AsString);
    Translate(Sqlen, '@Code3', T2_Sub21Code3.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    Base10.Update_ID(nSqry,'S4_SSUB_ID_GEN');

  end else begin

    Sqlon := 'UPDATE S4_Ssub SET '+
    'Sdate=''@Sdate'',Hcode=''@Hcode'',Bcode=''@Bcode'',Gsqut=  @Gsqut  , '+
    'Gdang=  @Gdang  ,Memo1=''@Memo1'', ';
    Sqlen :=
    'Gbigo=''@Gbigo'',Code1=''@Code1'',Code2=''@Code2'',Code3=''@Code3'', '+
    'Time3=  now() WHERE ID=@ID and Gdate=''@Gdate''';

    Translate(Sqlen, '@Gdate', T2_Sub21Gdate.AsString);
    Translate(Sqlon, '@Sdate', T2_Sub21Sdate.AsString);
    Translate(Sqlon, '@Hcode', T2_Sub21Hcode.AsString);
    Translate(Sqlon, '@Bcode', T2_Sub21Bcode.AsString);
    TransAuto(Sqlon, '@Gsqut', T2_Sub21Gsqut.AsString);
    TransAuto(Sqlon, '@Gdang', T2_Sub21Gdang.AsString);
    Translate(Sqlon, '@Memo1', T2_Sub21Memo1.AsString);
    Translate(Sqlen, '@Gbigo', T2_Sub21Gbigo.AsString);
    Translate(Sqlen, '@Code1', T2_Sub21Code1.AsString);
    Translate(Sqlen, '@Code2', T2_Sub21Code2.AsString);
    Translate(Sqlen, '@Code3', T2_Sub21Code3.AsString);
    TransAuto(Sqlen, '@ID',    T2_Sub21ID.AsString);

    Base10.Socket.RunSQL(Sqlon+Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;

end;

procedure TSobo22_1.T2_Sub21BeforeClose(DataSet: TDataSet);
begin
  With T2_Sub21 do
  if(State in dsEditModes)Then Post;
end;

procedure TSobo22_1.T2_Sub21NewRecord(DataSet: TDataSet);
begin
  T2_Sub21Hcode.Value:=Hnnnn;
  T2_Sub21Gdate.Value:=Sobo22_1.Edit101.Text;
  T2_Sub21Sdate.Value:=Sobo22_1.Edit101.Text;
  T2_Sub21Memo1.Value:='도서명:'+#13+'메모1):'+#13+'메모2):';
  T2_Sub21Gsqut.Value:=0;
  T2_Sub21Gdang.Value:=0;
  T2_Sub21Code1.Value:='N';
  T2_Sub21Code2.Value:='N';
  T2_Sub21Code3.Value:='N';
end;

end.
