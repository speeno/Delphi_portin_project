unit Subu39;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, DBClient;

type
  TSobo39 = class(TForm)
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
    DBGrid101: TDBGrid;
    DBGrid201: TDBGrid;
    StBar101: TStatusBar;
    StBar201: TStatusBar;
    Panel001: TFlatPanel;
    Panel102: TFlatPanel;
    Panel103: TFlatPanel;
    Panel101: TFlatPanel;
    Edit101: TFlatMaskEdit;
    T3_Sub91: TClientDataSet;
    T3_Sub91SCODE: TStringField;
    T3_Sub91GDATE: TStringField;
    T3_Sub91GUBUN: TStringField;
    T3_Sub91GCODE: TStringField;
    T3_Sub91GNAME: TStringField;
    T3_Sub91GIQUT: TFloatField;
    T3_Sub91GISUM: TFloatField;
    T3_Sub91GOQUT: TFloatField;
    T3_Sub91GOSUM: TFloatField;
    T3_Sub91GJQUT: TFloatField;
    T3_Sub91GJSUM: TFloatField;
    T3_Sub91GBQUT: TFloatField;
    T3_Sub91GBSUM: TFloatField;
    T3_Sub91GPQUT: TFloatField;
    T3_Sub91GPSUM: TFloatField;
    T3_Sub91GSUSU: TFloatField;
    T3_Sub91GSQUT: TFloatField;
    T3_Sub91GSSUM: TFloatField;
    T3_Sub91GSUMX: TFloatField;
    T3_Sub91GSUMY: TFloatField;
    T3_Sub92: TClientDataSet;
    T3_Sub92SCODE: TStringField;
    T3_Sub92GDATE: TStringField;
    T3_Sub92GUBUN: TStringField;
    T3_Sub92GCODE: TStringField;
    T3_Sub92GNAME: TStringField;
    T3_Sub92GIQUT: TFloatField;
    T3_Sub92GISUM: TFloatField;
    T3_Sub92GOQUT: TFloatField;
    T3_Sub92GOSUM: TFloatField;
    T3_Sub92GJQUT: TFloatField;
    T3_Sub92GJSUM: TFloatField;
    T3_Sub92GBQUT: TFloatField;
    T3_Sub92GBSUM: TFloatField;
    T3_Sub92GPQUT: TFloatField;
    T3_Sub92GPSUM: TFloatField;
    T3_Sub92GSUSU: TFloatField;
    T3_Sub92GSQUT: TFloatField;
    T3_Sub92GSSUM: TFloatField;
    T3_Sub92GSUMX: TFloatField;
    T3_Sub92GSUMY: TFloatField;
    Button101: TFlatButton;
    Button201: TFlatButton;
    Button301: TFlatButton;
    Button401: TFlatButton;
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
    Panel004: TFlatPanel;
    DBGrid301: TDBGrid;
    StatusBar1: TStatusBar;
    Panel105: TFlatPanel;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
    Label101: TmyLabel3d;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    DataSource3: TDataSource;
    T3_Sub90: TClientDataSet;
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
    procedure DBGrid101TitleClick(Column: TColumn);
    procedure DBGrid201TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo39: TSobo39;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo39.FormActivate(Sender: TObject);
begin
  nForm:='39';
  nSqry:=T3_Sub91;
  mSqry:=T3_Sub92;
end;

procedure TSobo39.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo39.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo39:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo39.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('39');
end;

procedure TSobo39.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('39');
end;

procedure TSobo39.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo39.Button011Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo39.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo39.Button013Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo39.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('39-01');
end;

procedure TSobo39.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('39-02');
end;

procedure TSobo39.Button016Click(Sender: TObject);
begin
  Button501Click(Self);
  Tong40.print_39_01(Self);
end;

procedure TSobo39.Button017Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo39.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo39.Button101Click(Sender: TObject);
var St1,St2: String;
begin
  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;
  Base10.OpenShow(nSqry);

  Scode:='A';

  St1:='Gdate'+' ='+#39+Edit101.Text+#39+' and '+
       'Scode'+' ='+#39+Scode+#39;
  St2:=' Order By Gcode';

  {-Sv_Gsum-}
  Sqlen := 'Select Scode,Gdate,Gcode,Goqut,Gbqut From Sv_Csum Where '+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  ProgressBar1.Max:=SGrid.RowCount-1;
  While SGrid.RowCount-1 > List1 do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  List1:=List1+1;

    nSqry.Append;
    nSqry.FieldByName('Scode').AsString:=SGrid.Cells[ 0,List1];
    nSqry.FieldByName('Gdate').AsString:=SGrid.Cells[ 1,List1];
    nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 2,List1];
    nSqry.FieldByName('Goqut').AsString:=SGrid.Cells[ 3,List1];
    nSqry.FieldByName('Gbqut').AsString:=SGrid.Cells[ 4,List1];

    nSqry.Edit;
    Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
    nSqry.Post;
  end;

  nSqry.First;
{ Tong20.Srart_39_01(Self); }
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
//nSqry.BeforePost:=Base10.T3_Sub91BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo39.Button201Click(Sender: TObject);
var St1,St2: String;
begin
  Tong40.Show;
  Tong40.Update;

  Refresh;
  mSqry.BeforePost:=nil;
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  Base10.OpenShow(mSqry);

  Scode:='B';

  St1:='Gdate'+' ='+#39+Edit101.Text+#39+' and '+
       'Scode'+' ='+#39+Scode+#39;
  St2:=' Order By Gcode';

  {-Sv_Gsum-}
  Sqlen := 'Select Scode,Gdate,Gcode,Gosum,Gbsum From Sv_Csum Where '+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  ProgressBar1.Max:=SGrid.RowCount-1;
  While SGrid.RowCount-1 > List1 do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  List1:=List1+1;

    mSqry.Append;
    mSqry.FieldByName('Scode').AsString:=SGrid.Cells[ 0,List1];
    mSqry.FieldByName('Gdate').AsString:=SGrid.Cells[ 1,List1];
    mSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 2,List1];
    mSqry.FieldByName('Gosum').AsString:=SGrid.Cells[ 3,List1];
    mSqry.FieldByName('Gbsum').AsString:=SGrid.Cells[ 4,List1];

    mSqry.Edit;
    Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', mSqry.FieldByName('Gcode').AsString);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    mSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
    mSqry.Post;
  end;

  mSqry.First;
{ Tong20.Srart_39_02(Self); }
  DBGrid201.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  Screen.Cursor:=crDefault;
//mSqry.BeforePost:=Base10.T3_Sub92BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo39.Button301Click(Sender: TObject);
var St1,St2,St3,St4: String;
begin
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);

  St2:='X';
  St1:='Gdate'+' ='+#39+Edit101.Text+#39+' and '+
       'Scode'+' ='+#39+St2+#39;
  {-S1_Ssub-}
  Sqlen :=
  'Select Gcode,Scode,Gjisa,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
  'From S1_Ssub Where '+St1+
  'Group By Gcode,Scode,Gjisa ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  ProgressBar1.Max:=SGrid.RowCount-1;
  While SGrid.RowCount-1 > List1 do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  List1:=List1+1;

    T01:=StrToInt64Def(SGrid.Cells[ 3,List1],0);
    T02:=StrToInt64Def(SGrid.Cells[ 4,List1],0);

    St1:='';
    St2:='';
    St3:='';
    St4:=SGrid.Cells[ 2,List1];

    Sqlen := 'Select Pubun,Gcode,Gname From G1_Ggeo Where Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Base10.Socket.RunSQL(Sqlen);
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      St1:=Base10.Socket.GetData(1, 1);
      St2:=Base10.Socket.GetData(1, 2);
      St3:=Base10.Socket.GetData(1, 3);
    end;

    if St4<>'' then begin
      Sqlen := 'Select Gdate From H2_Gbun Where Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname''';
      Translate(Sqlen, '@Scode', SGrid.Cells[ 1,List1]);
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
      Translate(Sqlen, '@Gname', SGrid.Cells[ 2,List1]);
      Base10.Socket.RunSQL(Sqlen);
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St1:=Base10.Socket.GetData(1, 1);
        St3:=St3+'-'+SGrid.Cells[ 2,List1];
      end;
    end;

    if St1='01' then begin
      if nSqry.Locate('Gcode',St2,[loCaseInsensitive])=False then begin
        nSqry.Append;
        nSqry.FieldByName('Scode').AsString:='A';
        nSqry.FieldByName('Gcode').AsString:=St2;
        nSqry.FieldByName('Gname').AsString:=St3;
        nSqry.FieldByName('Gdate').AsString:=Edit101.Text;
      end;
      nSqry.Edit;
      nSqry.FieldByName('Goqut').AsFloat:=nSqry.FieldByName('Goqut').AsFloat+T01;
      nSqry.Post;
    end else begin
      if mSqry.Locate('Gcode',St2,[loCaseInsensitive])=False then begin
        mSqry.Append;
        mSqry.FieldByName('Scode').AsString:='B';
        mSqry.FieldByName('Gcode').AsString:=St2;
        mSqry.FieldByName('Gname').AsString:=St3;
        mSqry.FieldByName('Gdate').AsString:=Edit101.Text;
      end;
      mSqry.Edit;
      mSqry.FieldByName('Gosum').AsFloat:=mSqry.FieldByName('Gosum').AsFloat+T01;
      mSqry.Post;
    end;
  end;
  nSqry.First;
  mSqry.First;
  ProgressBar1.Position:=0;
end;

procedure TSobo39.Button401Click(Sender: TObject);
var St1,St2: String;
    MeDlg: Integer;
begin
  St1:='('+'Scode'+'='+#39+'A'+#39+' Or '+'Scode'+'='+#39+'B'+#39+')'+' and '+
       'Gdate'+'='+#39+Edit101.Text+#39;

  {-Sv_Csum-}
  Sqlen := 'Select Distinct Gdate From Sv_Csum Where '+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  if SGrid.RowCount > 1 then begin

     MeDlg := MessageDlg('등록된 자료가 있습니다. 삭제하고 등록할까요?', mtConfirmation, [mbYes, mbNo], 0);
     case MeDlg of

     mrYes: begin
       St1:='Gdate'+'='+#39+SGrid.Cells[ 0,1]+#39;

       Sqlen := 'DELETE FROM Sv_Csum Where '+St1;
       Base10.Socket.RunSQL(Sqlen);
       Base10.Socket.BusyLoop;
       if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);
     end;

     mrNo: begin
       Exit;
     end;

     end;

  end;

  nSqry.First;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    St2:=Edit101.Text;

    Sqlen := 'INSERT INTO Sv_Csum '+
    '(Scode, Gcode, Gdate, Goqut, Gbqut, Gosum, Gbsum) VALUES '+
    '(''@Scode'',''@Gcode'',''@Gdate'',@Goqut,@Gbqut,@Gosum,@Gbsum )';

    Translate(Sqlen, '@Scode', 'A');
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Gdate', Edit101.Text);
    TransAuto(Sqlen, '@Goqut', nSqry.FieldByName('Goqut').AsString);
    TransAuto(Sqlen, '@Gbqut', nSqry.FieldByName('Gbqut').AsString);
    TransAuto(Sqlen, '@Gosum', nSqry.FieldByName('Gosum').AsString);
    TransAuto(Sqlen, '@Gbsum', nSqry.FieldByName('Gbsum').AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);
    nSqry.Next;
  end;
  ProgressBar1.Position:=0;

  mSqry.First;
  ProgressBar1.Max:=mSqry.RecordCount;
  While mSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    St2:=Edit101.Text;

    Sqlen := 'INSERT INTO Sv_Csum '+
    '(Scode, Gcode, Gdate, Goqut, Gbqut, Gosum, Gbsum) VALUES '+
    '(''@Scode'',''@Gcode'',''@Gdate'',@Goqut,@Gbqut,@Gosum,@Gbsum )';

    Translate(Sqlen, '@Scode', 'B');
    Translate(Sqlen, '@Gcode', mSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Gdate', Edit101.Text);
    TransAuto(Sqlen, '@Goqut', mSqry.FieldByName('Goqut').AsString);
    TransAuto(Sqlen, '@Gbqut', mSqry.FieldByName('Gbqut').AsString);
    TransAuto(Sqlen, '@Gosum', mSqry.FieldByName('Gosum').AsString);
    TransAuto(Sqlen, '@Gbsum', mSqry.FieldByName('Gbsum').AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);
    mSqry.Next;
  end;
  ProgressBar1.Position:=0;

  ShowMessage('저장되었습니다.')
end;

procedure TSobo39.Button501Click(Sender: TObject);
begin
  Base10.OpenShow(T3_Sub93);

  if nSqry.RecordCount >= mSqry.RecordCount then begin

    nSqry.First;
    While nSqry.EOF=False do begin
      T3_Sub93.Append;
      T3_Sub93.FieldByName('Gcode').AsString:=nSqry.FieldByName('Gcode').AsString;
      T3_Sub93.FieldByName('Gname').AsString:=nSqry.FieldByName('Gname').AsString;
      T3_Sub93.FieldByName('Goqut').AsString:=nSqry.FieldByName('Goqut').AsString;
      T3_Sub93.FieldByName('Gbqut').AsString:=nSqry.FieldByName('Gbqut').AsString;
      T3_Sub93.Post;
      nSqry.Next;
    end;

    T3_Sub93.First;

    mSqry.First;
    While mSqry.EOF=False do begin
      T3_Sub93.Edit;
      T3_Sub93.FieldByName('Bcode').AsString:=mSqry.FieldByName('Gcode').AsString;
      T3_Sub93.FieldByName('Bname').AsString:=mSqry.FieldByName('Gname').AsString;
      T3_Sub93.FieldByName('Gosum').AsString:=mSqry.FieldByName('Gosum').AsString;
      T3_Sub93.FieldByName('Gbsum').AsString:=mSqry.FieldByName('Gbsum').AsString;
      T3_Sub93.Post;
      T3_Sub93.Next;
      mSqry.Next;
    end;

  end else begin

    mSqry.First;
    While mSqry.EOF=False do begin
      T3_Sub93.Append;
      T3_Sub93.FieldByName('Bcode').AsString:=mSqry.FieldByName('Gcode').AsString;
      T3_Sub93.FieldByName('Bname').AsString:=mSqry.FieldByName('Gname').AsString;
      T3_Sub93.FieldByName('Gosum').AsString:=mSqry.FieldByName('Gosum').AsString;
      T3_Sub93.FieldByName('Gbsum').AsString:=mSqry.FieldByName('Gbsum').AsString;
      T3_Sub93.Post;
      mSqry.Next;
    end;

    T3_Sub93.First;

    nSqry.First;
    While nSqry.EOF=False do begin
      T3_Sub93.Edit;
      T3_Sub93.FieldByName('Gcode').AsString:=nSqry.FieldByName('Gcode').AsString;
      T3_Sub93.FieldByName('Gname').AsString:=nSqry.FieldByName('Gname').AsString;
      T3_Sub93.FieldByName('Goqut').AsString:=nSqry.FieldByName('Goqut').AsString;
      T3_Sub93.FieldByName('Gbqut').AsString:=nSqry.FieldByName('Gbqut').AsString;
      T3_Sub93.Post;
      T3_Sub93.Next;
      nSqry.Next;
    end;

  end;
end;

procedure TSobo39.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
end;

procedure TSobo39.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo39.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo39.Edit102KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then DBGrid101.SetFocus;
end;

procedure TSobo39.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then DBGrid101.SetFocus;
end;

procedure TSobo39.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo39.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo39.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo39.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo39.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo39.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo39.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Button201Click(Self);
    Button101Click(Self);
    Button301.Visible:=True;
    Button401.Visible:=True;
  end;
end;

procedure TSobo39.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo39.DBGrid101Enter(Sender: TObject);
begin
//
end;

procedure TSobo39.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo39.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
{ if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=0 Then begin

      if RadioButton101.Checked=True Then begin
      if nSqry.FieldByName('Gcode').AsString='' Then Exit;
      Seek10.Edit1.Text:=nSqry.FieldByName('Gcode').AsString;
      Seek10.FilterTing(nSqry.FieldByName('Gcode').AsString);
      if Seek10.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek10.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek10.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
      if Seek10.ShowModal=mrOK Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek10.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek10.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;
      end;

      if RadioButton102.Checked=True Then begin
      if nSqry.FieldByName('Gcode').AsString='' Then Exit;
      Seek20.Edit1.Text:=nSqry.FieldByName('Gcode').AsString;
      Seek20.FilterTing(nSqry.FieldByName('Gcode').AsString);
      if Seek20.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek20.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek20.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
      if Seek20.ShowModal=mrOK Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek20.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek20.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;
      end;

      if RadioButton103.Checked=True Then begin
      if nSqry.FieldByName('Gcode').AsString='' Then Exit;
      Seek50.Edit1.Text:=nSqry.FieldByName('Gcode').AsString;
      Seek50.FilterTing(nSqry.FieldByName('Gcode').AsString);
      if Seek50.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek50.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek50.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
      if Seek50.ShowModal=mrOK Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek50.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek50.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;
      end;

    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end; }
end;

procedure TSobo39.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
{ if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    if SIndexs=2 Then begin
      nSqry.Append; DBGrid101.SelectedIndex:=0;
    end;
  end;
  if sColumn=False Then begin
    if nSqry.IsEmpty=False Then
    if Key=VK_DELETE Then Base10.T3_Sub81AfterDelete(nSqry);
  //if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end; }
end;

procedure TSobo39.DBGrid201KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
{ if mSqry.Active=True Then begin
  SIndexs:=DBGrid201.SelectedIndex;
  sColumn:=DBGrid201.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=0 Then begin
      if mSqry.FieldByName('Gcode').AsString='' Then Exit;
      Seek40.Edit1.Text:=mSqry.FieldByName('Gcode').AsString;
      Seek40.FilterTing(mSqry.FieldByName('Gcode').AsString);
      if Seek40.Query1.RecordCount=1 Then begin
        mSqry.FieldByName('Gcode').AsString:=Seek40.Query1Gcode.AsString;
        mSqry.FieldByName('Gname').AsString:=Seek40.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
      if Seek40.ShowModal=mrOK Then begin
        mSqry.FieldByName('Gcode').AsString:=Seek40.Query1Gcode.AsString;
        mSqry.FieldByName('Gname').AsString:=Seek40.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;
    end;
    DBGrid201.SelectedIndex:=SIndexs+1;
    end;
  end;
  end; }
end;

procedure TSobo39.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
{ if mSqry.Active=True Then begin
  SIndexs:=DBGrid201.SelectedIndex;
  sColumn:=DBGrid201.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    mSqry.Edit;
    if SIndexs=2 Then begin
      mSqry.Append; DBGrid201.SelectedIndex:=0;
    end;
  end;
  if sColumn=False Then begin
    if mSqry.IsEmpty=False Then
    if Key=VK_DELETE Then Base10.T3_Sub82AfterDelete(mSqry);
  //if Key=VK_ESCAPE Then Edit201.SetFocus;
  end; end; }
end;

procedure TSobo39.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo39.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo39.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo39.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

end.
