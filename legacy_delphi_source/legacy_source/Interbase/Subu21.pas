unit Subu21;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, Tong07;

type
  TSobo21 = class(TForm)
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
    DBGrid101: TDBGrid;
    StBar101: TStatusBar;
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
    Button701: TFlatButton;
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
    procedure DBGrid101TitleClick(Column: TColumn);
    procedure DBGrid201TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure Edit301KeyPress(Sender: TObject; var Key: Char);
    procedure Button701Click(Sender: TObject);
    procedure Edit205Click(Sender: TObject);
    procedure Edit205Exit(Sender: TObject);
    procedure StaticText1Click(Sender: TObject);
    procedure StaticText2Click(Sender: TObject);
    procedure StaticText3Click(Sender: TObject);
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
  Sobo21: TSobo21;
  S2101,S2102: Double;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib, Subu20,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo21.FormActivate(Sender: TObject);
begin
  nForm:='21';
  nSqry:=Base10.T2_Sub11;
  mSqry:=Base10.T2_Sub12;
  tSqry:=Base10.T4_Sub81;
end;

procedure TSobo21.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo21.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo21:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Base10.OpenExit(tSqry);
end;

procedure TSobo21.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo21.Button002Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Button015Click(Self);
  end; }
end;

procedure TSobo21.Button003Click(Sender: TObject);
begin
{ if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo21.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo21.Button005Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     Application.CreateForm(TSobo20, Sobo20);
     Sobo20.ShowModal;
  end;
end;

procedure TSobo21.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo21.Button007Click(Sender: TObject);
begin
  if nSqry.Active=True Then
     Button401Click(Self);
end;

procedure TSobo21.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo21.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo21.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo21.Button011Click(Sender: TObject);
begin
{ Tong20.DBGridSaveHtml(DBGrid201, Caption); }
end;

procedure TSobo21.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX0(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo21.Button013Click(Sender: TObject);
begin
{ oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1); }
end;

procedure TSobo21.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('21-01');
end;

procedure TSobo21.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('21-02');
end;

procedure TSobo21.Button016Click(Sender: TObject);
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
  Tong40.print_21_01(Self);
end;

procedure TSobo21.Button017Click(Sender: TObject);
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
  Tong40.PrinTing00('21','2','','','','','','','','');
end;

procedure TSobo21.Button018Click(Sender: TObject);
begin
  Seak60.ShowModal;
end;

procedure TSobo21.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo21.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo21.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont2(DBGrid101,StBar101);
end;

procedure TSobo21.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo21.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo21.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo21.Button101Click(Sender: TObject);
var St1: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Sqlen := 'Select Grat9 From G1_Ggeo Where Hcode=''@Hcode'' and Gcode=''@Gcode'' ';
  Translate(Sqlen, '@Hcode', '');
  Translate(Sqlen, '@Gcode', Edit104.Text);
  if Base10.Seek_Name(Sqlen)='1' then begin
     ShowMessage('출고정지된 거래처입니다. 다시 선택해 주십시오.');
     Edit104.SetFocus;
     Exit;
  end else begin

  Sqlen := 'Select Gbigo From H2_Gbun Where '+
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
  end;

  end;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;

  Sqlen := 'Select * From S1_Ssub Where '+
           'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
           'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
           'Scode=''@Scode'' and Gjisa=''@Gjisa'' and '+
           'Ocode=''@Ocode'' and Hcode=''@Hcode''';

  Translate(Sqlen, '@Gdate', Edit101.Text);
  Translate(Sqlen, '@Gubun', Edit102.Text);
  Translate(Sqlen, '@Jubun', Edit103.Text);
  Translate(Sqlen, '@Gcode', Edit104.Text);
  Translate(Sqlen, '@Ocode', 'B');
  Translate(Sqlen, '@Scode', 'X');
  Translate(Sqlen, '@Gjisa', Edit106.Text);
  Translate(Sqlen, '@Hcode', Edit107.Text);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  S2101:=0; S2102:=0;

  nSqry.First;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    nSqry.Edit;
    nSqry.FieldByName('Gname').Value:=Edit105.Text;

    if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Bcode').AsString]),[loCaseInsensitive])=true then
    nSqry.FieldByName('Bname').AsString:=Base10.G4_Book.FieldByName('Gname').AsString;

    if nSqry.FieldByName('Bname').AsString='' then begin
    Sqlen := 'Select Gname,Gjeja From G4_Book Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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

    S2101:=S2101+nSqry.FieldByName('Gsqut').AsFloat;
    S2102:=S2102+nSqry.FieldByName('Gssum').AsFloat;
    nSqry.Post;
    nSqry.Next;
  end;

  Button301Click(Self);

  nSqry.IndexName := 'IDX'+'ID'+'DOWN';
  nSqry.First;
  Tong20.Srart_21_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=Base10.T2_Sub11BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo21.Button201Click(Sender: TObject);
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

          Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
                   'Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
          Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
                   'Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
                   'Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
                   'Where Gcode=''@Gcode'' and Bcode=''@Bcode'' and Hcode=''@Hcode''';
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

procedure TSobo21.Button301Click(Sender: TObject);
begin
  if Edit203.Visible=True then begin

    Edit203.Text:='';
    Edit204.Text:='';
    Edit205.Text:='';
    Edit206.Text:='';
    Edit207.Text:='';

    Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where '+
             'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
             'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
             'Scode=''@Scode'' and Gjisa=''@Gjisa'' and '+
             'Hcode=''@Hcode''';
    Translate(Sqlen, '@Gdate', Edit101.Text);
    Translate(Sqlen, '@Gubun', Edit102.Text);
    Translate(Sqlen, '@Jubun', Edit103.Text);
    Translate(Sqlen, '@Gcode', Edit104.Text);
    Translate(Sqlen, '@Scode', 'X');
    Translate(Sqlen, '@Gjisa', Edit106.Text);
    Translate(Sqlen, '@Hcode', Edit107.Text);
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

procedure TSobo21.Button401Click(Sender: TObject);
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

procedure TSobo21.Button501Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6: String;
begin
{ Base10.OpenShow(tSqry);

  St1:='Gdate'+' ='+#39+Edit101.Text+#39+' and '+
       'Jubun'+' ='+#39+Edit103.Text+#39+' and '+
       'Gcode'+' ='+#39+Edit104.Text+#39+' and '+
       'Gjisa'+' ='+#39+Edit106.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Scode'+' ='+#39+'X'+#39;

  St2:=' Group By Gcode,Gjisa';

  Sqlen := 'Select Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where '+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  Sqlen := 'Select Gname From G7_Ggeo Where Gcode=''@Gcode'' ';
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

    Sqlen := 'Select Gname From T1_Gbun Where Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa''';
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Gjisa', SGrid.Cells[ 1,List1]);
    St4:=Base10.Seek_Name(Sqlen);

    if St4='' then
    if SGrid.Cells[ 1,List1]<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where '+
               'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname''';
      Translate(Sqlen, '@Hcode', '');
      Translate(Sqlen, '@Scode', 'X');
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gname', SGrid.Cells[ 1,List1]);
      St4:=Base10.Seek_Name(Sqlen);
    end;

    if St4='' then begin
      Sqlen := 'Select Gubun From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Hcode', '');
      if Base10.Seek_Name(Sqlen)='01' then
      St4:='시내';
      if Base10.Seek_Name(Sqlen)='02' then
      St4:='지방';
    end;

    Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', '');
    St5:=Base10.Seek_Name(Sqlen);

    if St5='' then begin
    Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
      'Select Gqut1,Gqut2 From T4_Ssub Where '+
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
      'Select Gqut1,Gqut2 From T4_Ssub Where '+
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

procedure TSobo21.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit103.Focused=True)and(Edit103.SelStart=02)and(Length(Trim(Edit103.Text))=02))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit104.Focused=True)and(Edit104.SelStart=05)and(Length(Trim(Edit104.Text))=05))or
    ((Edit105.Focused=True)and(Edit105.SelStart=24)and(Length(Trim(Edit105.Text))=24))or
    ((Edit107.Focused=True)and(Edit107.SelStart=05)and(Length(Trim(Edit107.Text))=05))or
    ((Edit108.Focused=True)and(Edit108.SelStart=24)and(Length(Trim(Edit108.Text))=24))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo21.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo21.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo21.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo21.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo21.Edit112KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    DGrid: TDBGrid;
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
        DGrid.Columns.Items[0].PickList.Add('반품');
        DGrid.Columns.Items[0].PickList.Add('폐기');
      end;
      Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
    end else
    if Edits.DropDownCount=8 Then begin
      Key:=#0; SendMessage(Hands, cb_ShowDropDown, 1, 0);
    end;
  end;
end;

procedure TSobo21.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit102;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo21.Edit113KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo21.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit106;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo21.Edit114KeyPress(Sender: TObject; var Key: Char);
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
      Seek10.Edit1.Text:=Edit104.Text;
      Seek10.FilterTing(Edit104.Text,Edit107.Text);
      if Seek10.Query1.IsEmpty=True Then Exit;
    end;
    if Edit105.Focused=True Then begin
      Seek10.Edit1.Text:=Edit105.Text;
      Seek10.FilterTing(Edit105.Text,Edit107.Text);
      if Seek10.Query1.IsEmpty=True Then Exit;
    end;
    if Seek10.Query1.RecordCount=1 Then begin
      Edit104.Text:=Seek10.Query1Gcode.AsString;
      Edit105.Text:=Seek10.Query1Gname.AsString;
      Edit202.Text:=Seek10.Query1Gtel1.AsString+'-'+Seek10.Query1Gtel2.AsString;
    //Edit204.Text:=Seek10.Query1Gadd1.AsString+' '+Seek10.Query1Gadd2.AsString;

      Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+
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
      Translate(Sqlen, '@Scode', 'X');
      Str:=Base10.Seek_Name(Sqlen);

      if Str<>'' then begin
        Edit201.Text:=Edit104.Text+'-'+Copy(Edit101.Text,6,2)+Copy(Edit101.Text,9,2)+'-'+IntToStr(StrToIntDef(Str,0));
      end else begin
        Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+
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
           'Scode'+'='+#39+'X'+#39 else
      St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
           'Hcode'+'='+#39+''+#39+' and '+
           'Scode'+'='+#39+'X'+#39;
      Edit106.Items.Clear;
      Sqlen := 'Select Gname,Jubun From H2_Gbun Where '+St1+' Order By Oname,Gname';
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
    if Seek10.ShowModal=mrOK Then begin
      Edit104.Text:=Seek10.Query1Gcode.AsString;
      Edit105.Text:=Seek10.Query1Gname.AsString;
      Edit202.Text:=Seek10.Query1Gtel1.AsString+'-'+Seek10.Query1Gtel2.AsString;
    //Edit204.Text:=Seek10.Query1Gadd1.AsString+' '+Seek10.Query1Gadd2.AsString;

      Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+
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
      Translate(Sqlen, '@Scode', 'X');
      Str:=Base10.Seek_Name(Sqlen);

      if Str<>'' then begin
        Edit201.Text:=Edit104.Text+'-'+Copy(Edit101.Text,6,2)+Copy(Edit101.Text,9,2)+'-'+IntToStr(StrToIntDef(Str,0));
      end else begin
        Sqlen := 'Select Max(Idnum) From S1_Ssub Where '+
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
           'Scode'+'='+#39+'X'+#39 else
      St1:='Gcode'+'='+#39+Edit104.Text+#39+' and '+
           'Hcode'+'='+#39+''+#39+' and '+
           'Scode'+'='+#39+'X'+#39;
      Edit106.Items.Clear;
      Sqlen := 'Select Gname,Jubun From H2_Gbun Where '+St1+' Order By Oname,Gname';
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

procedure TSobo21.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo21.DBGrid101Exit(Sender: TObject);
begin
  Base10.T2_Sub11BeforeClose(Base10.T2_Sub11);
end;

procedure TSobo21.DBGrid101Enter(Sender: TObject);
var DGrid: TDBGrid;
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
    DGrid.Columns.Items[0].PickList.Add('반품');
    DGrid.Columns.Items[0].PickList.Add('폐기');
    DGrid.Columns.Items[0].PickList.Add(' 질 ');
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
  Base10.T2_Sub11AfterScroll(Base10.T2_Sub11);
end;

procedure TSobo21.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=0 Then begin

      Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
               'Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
      Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
               'Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
               'Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
               'Where Gcode=''@Gcode'' and Bcode=''@Bcode'' and Hcode=''@Hcode''';
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

procedure TSobo21.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
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
        nSqry.FieldByName('Pubun').Value:='반품' else
        nSqry.FieldByName('Pubun').Value:='위탁'; end;
      While(Seek40.Query1.EOF=False)and(Code1<>'')do begin
      if nSqry.FieldByName('Gubun').Value='반품' Then
        nSqry.FieldByName('Pubun').Value:='반품' else
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

        Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
                 'Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
        Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
                 'Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
                 'Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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
    if Key=VK_DELETE Then Base10.T2_Sub11AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo21.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo21.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo21.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo21.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo21.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  StBar101.Panels.Items[2].Text:=FormatFloat('###,###,##0',S2101);
  StBar101.Panels.Items[4].Text:=FormatFloat('###,###,##0',S2102);
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo21.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo21.Edit301KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  Button701Click(Self);
end;

procedure TSobo21.Button701Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin

    Sqlen := 'Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where '+
             'Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
             'Jubun=''@Jubun'' and Gcode=''@Gcode'' and '+
             'Scode=''@Scode'' and Gjisa=''@Gjisa'' and '+
             'Hcode=''@Hcode''';
    Translate(Sqlen, '@Gdate', Edit101.Text);
    Translate(Sqlen, '@Gubun', Edit102.Text);
    Translate(Sqlen, '@Jubun', Edit103.Text);
    Translate(Sqlen, '@Gcode', Edit104.Text);
    Translate(Sqlen, '@Scode', 'X');
    Translate(Sqlen, '@Gjisa', Edit106.Text);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin

      Sqlen := 'UPDATE S1_Memo SET Gbigo=''@Gbigo'' ,Sbigo=''@Sbigo'' ,'+
      ' Gtel1=''@Gtel1'' ,Gtel2=''@Gtel2'' ,Gname=''@Gname'' '+
      ' WHERE Gdate=''@Gdate'' and Gubun=''@Gubun'' '+
      '  and  Jubun=''@Jubun'' and Gcode=''@Gcode'' '+
      '  and  Scode=''@Scode'' and Gjisa=''@Gjisa'' '+
      '  and  Hcode=''@Hcode'' ';

      Translate(Sqlen, '@Gdate', Edit101.Text);
      Translate(Sqlen, '@Gubun', Edit102.Text);
      Translate(Sqlen, '@Jubun', Edit103.Text);
      Translate(Sqlen, '@Gcode', Edit104.Text);
      Translate(Sqlen, '@Scode', 'X');
      Translate(Sqlen, '@Gjisa', Edit106.Text);
      Translate(Sqlen, '@Hcode', Edit107.Text);
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

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    end else begin

      Sqlen := 'INSERT INTO S1_Memo '+
      '(Gdate, Gubun, Jubun, Gcode, Scode, Gjisa, Hcode, '+
      ' Gbigo, Sbigo, Gtel1, Gtel2, Gname) VALUES '+
      '(''@Gdate'',''@Gubun'',''@Jubun'',''@Gcode'', '+
      ' ''@Scode'',''@Gjisa'',''@Hcode'',''@Gbigo'', '+
      ' ''@Sbigo'',''@Gtel1'',''@Gtel2'',''@Gname'' )';

      Translate(Sqlen, '@Gdate', Edit101.Text);
      Translate(Sqlen, '@Gubun', Edit102.Text);
      Translate(Sqlen, '@Jubun', Edit103.Text);
      Translate(Sqlen, '@Gcode', Edit104.Text);
      Translate(Sqlen, '@Scode', 'X');
      Translate(Sqlen, '@Gjisa', Edit106.Text);
      Translate(Sqlen, '@Hcode', Edit107.Text);
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

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end;
    DBGrid101.SetFocus;
  end;
end;

procedure TSobo21.Edit205Click(Sender: TObject);
begin
  if Edit205.Focused=True then
  StaticText1.Visible:=False;
  if Edit206.Focused=True then
  StaticText2.Visible:=False;
  if Edit207.Focused=True then
  StaticText3.Visible:=False;
end;

procedure TSobo21.Edit205Exit(Sender: TObject);
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

procedure TSobo21.StaticText1Click(Sender: TObject);
begin
  StaticText1.Visible:=False;
  Edit205.SetFocus;
end;

procedure TSobo21.StaticText2Click(Sender: TObject);
begin
  StaticText2.Visible:=False;
  Edit206.SetFocus;
end;

procedure TSobo21.StaticText3Click(Sender: TObject);
begin
  StaticText3.Visible:=False;
  Edit207.SetFocus;
end;

end.
