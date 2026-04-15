unit Subu45;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, DBGridEh;

type
  TSobo45 = class(TForm)
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
    DBGrid101: TDBGrid;
    StBar101: TStatusBar;
    StBar201: TStatusBar;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
    Panel200: TFlatPanel;
    Panel201: TFlatPanel;
    Panel210: TFlatPanel;
    Panel202: TFlatPanel;
    Panel204: TFlatPanel;
    Panel205: TFlatPanel;
    Panel207: TFlatPanel;
    Panel208: TFlatPanel;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Label101: TmyLabel3d;
    Edit201: TFlatNumber;
    Edit208: TFlatNumber;
    Edit209: TFlatNumber;
    Edit210: TFlatNumber;
    Edit217: TFlatNumber;
    Edit224: TFlatNumber;
    Edit227: TFlatNumber;
    Edit202: TFlatNumber;
    Edit203: TFlatNumber;
    Edit204: TFlatNumber;
    Panel213: TFlatPanel;
    Panel211: TFlatPanel;
    Panel203: TFlatPanel;
    Edit211: TFlatNumber;
    Edit212: TFlatNumber;
    Edit213: TFlatNumber;
    Edit218: TFlatNumber;
    Edit219: TFlatNumber;
    Edit220: TFlatNumber;
    Edit225: TFlatNumber;
    Edit205: TFlatNumber;
    Edit206: TFlatNumber;
    Edit207: TFlatNumber;
    Panel206: TFlatPanel;
    Panel209: TFlatPanel;
    Panel212: TFlatPanel;
    Edit214: TFlatNumber;
    Edit215: TFlatNumber;
    Edit216: TFlatNumber;
    Edit221: TFlatNumber;
    Edit222: TFlatNumber;
    Edit223: TFlatNumber;
    Edit226: TFlatNumber;
    Panel216: TFlatPanel;
    Edit230: TFlatNumber;
    Panel214: TFlatPanel;
    Edit228: TFlatNumber;
    Panel215: TFlatPanel;
    Edit229: TFlatNumber;
    Button301: TFlatButton;
    DBGrid201: TDBGridEh;
    Edit231: TFlatNumber;
    Edit232: TFlatNumber;
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
    procedure Edit201Exit(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo45: TSobo45;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo45.FormActivate(Sender: TObject);
begin
  nForm:='45';
  nSqry:=Base10.T4_Sub51;
  mSqry:=Base10.T4_Sub52;
end;

procedure TSobo45.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"',Date);
end;

procedure TSobo45.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo45:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo45.Button001Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
     Seak10.ShowModal;
  end; }
end;

procedure TSobo45.Button002Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_45_02(Self);
  end; }
end;

procedure TSobo45.Button003Click(Sender: TObject);
begin
{ if mSqry.Active=True Then begin
     oSqry:=mSqry;
     Seak30.ShowModal;
  end; }
end;

procedure TSobo45.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo45.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo45.Button006Click(Sender: TObject);
begin
  Button201Click(Self);
{ T00:=1;
  Button201Click(Self); }
end;

procedure TSobo45.Button007Click(Sender: TObject);
begin
  Button601Click(Self);

  Edit201.Value:=DBGrid201.Columns[1].Footer.SumValue+
                 DBGrid201.Columns[2].Footer.SumValue;
  if Edit201.Value < Edit202.Value then
  Edit205.Value:=0 else
  Edit205.Value:=Edit201.Value - Edit202.Value;
  Edit208.Value:=DBGrid201.Columns[2].Footer.SumValue;
  Edit211.Value:=DBGrid201.Columns[3].Footer.SumValue;
  Edit214.Value:=DBGrid201.Columns[4].Footer.SumValue;
  Edit217.Value:=DBGrid201.Columns[9].Footer.SumValue;
  Edit207.Value:=Edit205.Value * Edit206.Value;
  Edit210.Value:=Edit208.Value * Edit209.Value;
  Edit213.Value:=Edit211.Value * Edit212.Value;
  Edit216.Value:=Edit214.Value * Edit215.Value;
  Edit223.Value:=Edit221.Value * Edit222.Value;
  Edit224.Value:=Edit231.Value * Edit232.Value;
  Edit201Exit(Self);
{ T00:=0;
  Button201Click(Self); }
end;

procedure TSobo45.Button008Click(Sender: TObject);
begin
  Tong20.Zoom_Int_01('24');
end;

procedure TSobo45.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('24');
end;

procedure TSobo45.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo45.Button011Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo45.Button012Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo45.Button013Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX9(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo45.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('45-01');
end;

procedure TSobo45.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('45-02');
end;

procedure TSobo45.Button016Click(Sender: TObject);
begin
  Tong40.print_45_01(Self);
end;

procedure TSobo45.Button017Click(Sender: TObject);
begin
  Tong40.print_45_02(Self);
end;

procedure TSobo45.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo45.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo45.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo45.Button021Click(Sender: TObject);
begin
//Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo45.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo45.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo45.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo45.Button101Click(Sender: TObject);
var St1,St2,St3: String;
    St9: Integer;
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

  Sqlen := 'Select Gcode,Gname,Gtel1,Gtel2 From G7_Ggeo Order By Gcode';

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
  //mSqry.FieldByName('Gtels').AsString:=SGrid.Cells[ 2,List1]+'-'+SGrid.Cells[ 3,List1];
    mSqry.Post;
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
    nSqry.Post;
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

procedure TSobo45.Button201Click(Sender: TObject);
var St1,St2,St3,St4: String;
    St9: Integer;
begin
  Bmark:=nSqry.GetBookmark; nSqry.DisableControls;

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
    if nSqry.Locate('Gdate;Hcode',VarArrayOf([St3,'']),[loCaseInsensitive])=True then begin
    nSqry.Edit;
    nSqry.FieldByName('Gqut1').AsString:='';
    nSqry.FieldByName('Gqut2').AsString:='';
  { nSqry.FieldByName('Gqut3').AsString:='';
    nSqry.FieldByName('Gqut4').AsString:='';
    nSqry.FieldByName('Name1').AsString:='';
    nSqry.FieldByName('Name2').AsString:='';
    nSqry.FieldByName('Gcode').AsString:='';
    nSqry.FieldByName('Gname').AsString:=''; }
    nSqry.FieldByName('Gsqut').AsString:='';
    nSqry.FieldByName('Gssum').AsString:='';
    nSqry.Post;
    end;
  end;

  St1:='Gdate'+'>='+#39+mSqry.FieldByName('Gdate').AsString+'.00'+#39+' and '+
       'Gdate'+'<='+#39+mSqry.FieldByName('Gdate').AsString+'.99'+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39+' and '+
       'Gubun'+' ='+#39+'출고'+#39+' and '+
       'Scode'+' ='+#39+'X'+#39;

  St2:=' Group By Substring(Gdate,9,2),Gcode,Gjisa';

  Sqlen := 'Select Substring(Gdate,9,2),Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where '+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  T02:=0;
  T03:=0;

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 3,List1],0);
    St3:=SGrid.Cells[ 0,List1];
    St4:='';

    if nSqry.Locate('Gdate;Hcode',VarArrayOf([St3,St4]),[loCaseInsensitive])=True then begin

      Sqlen := 'Select Gname From T1_Gbun Where '+
               'Hcode=''@Hcode'' and Gcode=''@Gcode'' and Gjisa=''@Gjisa'' and Jubun=''@Jubun''';
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
      Translate(Sqlen, '@Gjisa', Base10.Seek_Jisa(SGrid.Cells[ 2,List1],'3'));
      Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 2,List1],'4'));
      St4:=Base10.Seek_Name(Sqlen);

      if St4='' then
      if SGrid.Cells[ 2,List1]<>'' then begin
        Sqlen := 'Select Gdate From H2_Gbun Where '+
                 'Hcode=''@Hcode'' and Scode=''@Scode'' and Gcode=''@Gcode'' and Gname=''@Gname'' and Jubun=''@Jubun''';
        Translate(Sqlen, '@Hcode', '');
        Translate(Sqlen, '@Scode', 'X');
        Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
        Translate(Sqlen, '@Gname', Base10.Seek_Jisa(SGrid.Cells[ 2,List1],'3'));
        Translate(Sqlen, '@Jubun', Base10.Seek_Jisa(SGrid.Cells[ 2,List1],'4'));
        St4:=Base10.Seek_Name(Sqlen);
      end;

      if St4='' then begin
        if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 1,List1]]),[loCaseInsensitive])=true then begin
          if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
          if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
        end;

        if St4='' then
        if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Hcode').AsString,SGrid.Cells[ 0,List1]]),[loCaseInsensitive])=true then begin
          if Base10.G1_Ggeo.FieldByName('Gubun').AsString='01' then St4:='시내';
          if Base10.G1_Ggeo.FieldByName('Gubun').AsString='02' then St4:='지방';
        end;

        if St4='' then begin
        Sqlen := 'Select Gubun From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
        Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
        Translate(Sqlen, '@Hcode', '');
        if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
        if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
        end;

        if St4='' then begin
        Sqlen := 'Select Gubun From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
        Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
        Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
        if Base10.Seek_Name(Sqlen)='01' then St4:='시내';
        if Base10.Seek_Name(Sqlen)='02' then St4:='지방';
        end;
      end;

      if St4<>'' then begin
        nSqry.Edit;
        if St4='지방' then begin
        nSqry.FieldByName('Gqut2').AsFloat:=nSqry.FieldByName('Gqut2').AsFloat+T01;
        T03:=T03+T01;
        end else begin
        nSqry.FieldByName('Gqut1').AsFloat:=nSqry.FieldByName('Gqut1').AsFloat+T01;
        T02:=T02+T01;
        end;
        nSqry.Post;
      end;
    end;
  end;

  Edit201.Value:=T02+T03;
  if Edit201.Value < Edit202.Value then
  Edit205.Value:=0 else
  Edit205.Value:=Edit201.Value - Edit202.Value;
  Edit207.Value:=Edit205.Value * Edit206.Value;
  Edit208.Value:=T03;
  Edit210.Value:=Edit208.Value * Edit209.Value;

  St1:='Gdate'+'>='+#39+mSqry.FieldByName('Gdate').AsString+'.00'+#39+' and '+
       'Gdate'+'<='+#39+mSqry.FieldByName('Gdate').AsString+'.99'+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;

  Sqlen := 'Select Gdate,Gcode,Name1,Name2,Gssum From T1_Ssub Where '+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  T02:=0;

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    St3:=Copy(SGrid.Cells[ 0,List1],9,2);
    St4:='';

    if nSqry.Locate('Gdate;Hcode',VarArrayOf([St3,St4]),[loCaseInsensitive])=True then begin

      nSqry.Edit;
      if nSqry.FieldByName('Gname').AsString='' then begin
        if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf(['',SGrid.Cells[ 1,List1]]),[loCaseInsensitive])=true then
        nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

        if nSqry.FieldByName('Gname').AsString='' then
        if Base10.G1_Ggeo.Locate('Hcode;Gcode',VarArrayOf([mSqry.FieldByName('Hcode').AsString,SGrid.Cells[ 1,List1]]),[loCaseInsensitive])=true then
        nSqry.FieldByName('Gname').AsString:=Base10.G1_Ggeo.FieldByName('Gname').AsString;

        if nSqry.FieldByName('Gname').AsString='' then begin
        Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
        Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
        Translate(Sqlen, '@Hcode', '');
        nSqry.FieldByName('Gname').AsString:=Base10.Seek_Name(Sqlen);
        end;

        if nSqry.FieldByName('Gname').AsString='' then begin
        Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
        Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
        Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
        nSqry.FieldByName('Gname').AsString:=Base10.Seek_Name(Sqlen);
        end;

        nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 1,List1];
        nSqry.FieldByName('Name1').AsString:=SGrid.Cells[ 2,List1];
        nSqry.FieldByName('Name2').AsString:=SGrid.Cells[ 3,List1];
      end;
      if nSqry.FieldByName('Gsqut').AsString<>'' then begin
        nSqry.FieldByName('Gsqut').AsFloat :=nSqry.FieldByName('Gsqut').AsFloat+1;
      end else begin
        nSqry.FieldByName('Gsqut').AsFloat :=0;
      end;
      nSqry.FieldByName('Gssum').AsFloat :=nSqry.FieldByName('Gssum').AsFloat+T01;
      nSqry.Post;

      T02:=T02+T01;
    end;
  end;

  Edit217.Value:=T02;

  Button501Click(Self);

  Edit201Exit(Self);

  nSqry.First;
  nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
end;

procedure TSobo45.Button301Click(Sender: TObject);
var Sq1,Sq2,Sq3: String;
begin
  Bmark:=nSqry.GetBookmark; nSqry.DisableControls;

  if nSqry.Active=True Then begin
    Sqlen := 'Select Gdate From T2_Ssub Where Gdate=''@Gdate'' ';
    Translate(Sqlen, '@Gdate', mSqry.FieldByName('Gdate').AsString);
    if Base10.Seek_Name(Sqlen)='' Then begin

      Sqlon := 'INSERT INTO T2_Ssub '+
      '( Gdate, Hcode, Sum01, Sum02, Sum03, Sum04, '+
      '  Sum05, Sum06, Sum07, Sum08, Sum09, Sum10, '+
      '  Sum11, Sum12, Sum13, Sum14, Sum15, Sum16, '+
      '  Sum17, Sum18, Sum19, Sum20, Sum21, Sum22, '+
      '  Sum23, Sum24, Sum25, Sum26, Sum27, Sum28, '+
      '  Sum29, Sum30, Sum31, Sum32 ) VALUES ';
      Sq1 :=
      '(''@Gdate'',''@Hcode'', @Sum01 , @Sum02 , @Sum03 , @Sum04 , '+
      '   @Sum05  ,  @Sum06  , @Sum07 , @Sum08 , @Sum09 , @Sum10 , ';
      Sq2 :=
      '   @Sum11  ,  @Sum12  , @Sum13 , @Sum14 , @Sum15 , @Sum16 , '+
      '   @Sum17  ,  @Sum18  , @Sum19 , @Sum20 , @Sum21 , @Sum22 , ';
      Sq3 :=
      '   @Sum23  ,  @Sum24  , @Sum25 , @Sum26 , @Sum27 , @Sum28 , '+
      '   @Sum29  ,  @Sum30  , @Sum31 , @Sum32  )';

      Translate(Sq1, '@Gdate', mSqry.FieldByName('Gdate').AsString);
      Translate(Sq1, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      TransAuto(Sq1, '@Sum01', FloatToStr(Edit201.Value));
      TransAuto(Sq1, '@Sum02', FloatToStr(Edit202.Value));
      TransAuto(Sq1, '@Sum03', FloatToStr(Edit203.Value));
      TransAuto(Sq1, '@Sum04', FloatToStr(Edit204.Value));
      TransAuto(Sq1, '@Sum05', FloatToStr(Edit205.Value));
      TransAuto(Sq1, '@Sum06', FloatToStr(Edit206.Value));
      TransAuto(Sq1, '@Sum07', FloatToStr(Edit207.Value));
      TransAuto(Sq1, '@Sum08', FloatToStr(Edit208.Value));
      TransAuto(Sq1, '@Sum09', FloatToStr(Edit209.Value));
      TransAuto(Sq1, '@Sum10', FloatToStr(Edit210.Value));

      TransAuto(Sq2, '@Sum11', FloatToStr(Edit211.Value));
      TransAuto(Sq2, '@Sum12', FloatToStr(Edit212.Value));
      TransAuto(Sq2, '@Sum13', FloatToStr(Edit213.Value));
      TransAuto(Sq2, '@Sum14', FloatToStr(Edit214.Value));
      TransAuto(Sq2, '@Sum15', FloatToStr(Edit215.Value));
      TransAuto(Sq2, '@Sum16', FloatToStr(Edit216.Value));
      TransAuto(Sq2, '@Sum17', FloatToStr(Edit217.Value));
      TransAuto(Sq2, '@Sum18', FloatToStr(Edit218.Value));
      TransAuto(Sq2, '@Sum19', FloatToStr(Edit219.Value));
      TransAuto(Sq2, '@Sum20', FloatToStr(Edit220.Value));
      TransAuto(Sq2, '@Sum21', FloatToStr(Edit221.Value));
      TransAuto(Sq2, '@Sum22', FloatToStr(Edit222.Value));

      TransAuto(Sq3, '@Sum23', FloatToStr(Edit223.Value));
      TransAuto(Sq3, '@Sum24', FloatToStr(Edit224.Value));
      TransAuto(Sq3, '@Sum25', FloatToStr(Edit225.Value));
      TransAuto(Sq3, '@Sum26', FloatToStr(Edit226.Value));
      TransAuto(Sq3, '@Sum27', FloatToStr(Edit227.Value));
      TransAuto(Sq3, '@Sum28', FloatToStr(Edit228.Value));
      TransAuto(Sq3, '@Sum29', FloatToStr(Edit229.Value));
      TransAuto(Sq3, '@Sum30', FloatToStr(Edit230.Value));
      TransAuto(Sq3, '@Sum31', FloatToStr(Edit231.Value));
      TransAuto(Sq3, '@Sum32', FloatToStr(Edit232.Value));

      Sqlen:=Sqlon+Sq1+Sq2+Sq3;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then begin
        ShowMessage(E_Insert);
        Exit;
      end;

    end else begin

      Sq1 := 'UPDATE T2_Ssub SET '+
      'Gdate=''@Gdate'',Sum01=  @Sum01  ,Sum02=  @Sum02  ,Sum03=  @Sum03  , '+
      'Sum04=  @Sum04  ,Sum05=  @Sum05  ,Sum06=  @Sum06  ,Sum07=  @Sum07  , '+
      'Sum08=  @Sum08  ,Sum09=  @Sum09  ,Sum10=  @Sum10  ,Sum11=  @Sum11  , ';
      Sq2 :=
      'Sum12=  @Sum12  ,Sum13=  @Sum13  ,Sum14=  @Sum14  ,Sum15=  @Sum15  , '+
      'Sum16=  @Sum16  ,Sum17=  @Sum17  ,Sum18=  @Sum18  ,Sum19=  @Sum19  , '+
      'Sum20=  @Sum20  ,Sum21=  @Sum21  ,Sum22=  @Sum22  ,Sum23=  @Sum23  , ';
      Sq3 :=
      'Sum24=  @Sum24  ,Sum25=  @Sum25  ,Sum26=  @Sum26  ,Sum27=  @Sum27  , '+
      'Sum28=  @Sum28  ,Sum29=  @Sum29  ,Sum30=  @Sum30  ,Sum31=  @Sum31  , '+
      'Sum32=  @Sum32  '+
      'WHERE Gdate=''@Gdate'' and Hcode=''@Hcode'' ';

      Translate(Sq1, '@Gdate', mSqry.FieldByName('Gdate').AsString);
      TransAuto(Sq1, '@Sum01', FloatToStr(Edit201.Value));
      TransAuto(Sq1, '@Sum02', FloatToStr(Edit202.Value));
      TransAuto(Sq1, '@Sum03', FloatToStr(Edit203.Value));
      TransAuto(Sq1, '@Sum04', FloatToStr(Edit204.Value));
      TransAuto(Sq1, '@Sum05', FloatToStr(Edit205.Value));
      TransAuto(Sq1, '@Sum06', FloatToStr(Edit206.Value));
      TransAuto(Sq1, '@Sum07', FloatToStr(Edit207.Value));
      TransAuto(Sq1, '@Sum08', FloatToStr(Edit208.Value));
      TransAuto(Sq1, '@Sum09', FloatToStr(Edit209.Value));
      TransAuto(Sq1, '@Sum10', FloatToStr(Edit210.Value));
      TransAuto(Sq1, '@Sum11', FloatToStr(Edit211.Value));

      TransAuto(Sq2, '@Sum12', FloatToStr(Edit212.Value));
      TransAuto(Sq2, '@Sum13', FloatToStr(Edit213.Value));
      TransAuto(Sq2, '@Sum14', FloatToStr(Edit214.Value));
      TransAuto(Sq2, '@Sum15', FloatToStr(Edit215.Value));
      TransAuto(Sq2, '@Sum16', FloatToStr(Edit216.Value));
      TransAuto(Sq2, '@Sum17', FloatToStr(Edit217.Value));
      TransAuto(Sq2, '@Sum18', FloatToStr(Edit218.Value));
      TransAuto(Sq2, '@Sum19', FloatToStr(Edit219.Value));
      TransAuto(Sq2, '@Sum20', FloatToStr(Edit220.Value));
      TransAuto(Sq2, '@Sum21', FloatToStr(Edit221.Value));
      TransAuto(Sq2, '@Sum22', FloatToStr(Edit222.Value));
      TransAuto(Sq2, '@Sum23', FloatToStr(Edit223.Value));

      TransAuto(Sq3, '@Sum24', FloatToStr(Edit224.Value));
      TransAuto(Sq3, '@Sum25', FloatToStr(Edit225.Value));
      TransAuto(Sq3, '@Sum26', FloatToStr(Edit226.Value));
      TransAuto(Sq3, '@Sum27', FloatToStr(Edit227.Value));
      TransAuto(Sq3, '@Sum28', FloatToStr(Edit228.Value));
      TransAuto(Sq3, '@Sum29', FloatToStr(Edit229.Value));
      TransAuto(Sq3, '@Sum30', FloatToStr(Edit230.Value));
      TransAuto(Sq3, '@Sum31', FloatToStr(Edit231.Value));
      TransAuto(Sq3, '@Sum32', FloatToStr(Edit232.Value));
      Translate(Sq3, '@Gdate', mSqry.FieldByName('Gdate').AsString);
      Translate(Sq3, '@Hcode', mSqry.FieldByName('Hcode').AsString);

      Sqlen:=Sq1+Sq2+Sq3;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then begin
        ShowMessage(E_Update);
        Exit;
      end;

    end;
  end;

  if nSqry.Active=True Then begin
    nSqry.First;
    While nSqry.EOF=False do begin

    Sqlen := 'Select Gdate From T3_Ssub Where Gdate=''@Gdate'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gdate', mSqry.FieldByName('Gdate').AsString+'.'+nSqry.FieldByName('Gdate').AsString);
    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
    if Base10.Seek_Name(Sqlen)='' Then begin

      Sqlon := 'INSERT INTO T3_Ssub '+
      '( Gdate, Hcode, Gqut1, Gqut2, Gqut3, Gqut4, '+
      '  Gname, Name1, Name2, Gcode, Gsqut, Gssum  ) VALUES ';
      Sq1 :=
      '(''@Gdate'',''@Hcode'',  @Gqut1  ,  @Gqut2  , @Gqut3 , @Gqut4 , '+
      ' ''@Gname'',''@Name1'',''@Name2'',''@Gcode'', @Gsqut , @Gssum  )';

      Translate(Sq1, '@Gdate', mSqry.FieldByName('Gdate').AsString+'.'+nSqry.FieldByName('Gdate').AsString);
      Translate(Sq1, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      TransAuto(Sq1, '@Gqut1', nSqry.FieldByName('Gqut1').AsString);
      TransAuto(Sq1, '@Gqut2', nSqry.FieldByName('Gqut2').AsString);
      TransAuto(Sq1, '@Gqut3', nSqry.FieldByName('Gqut3').AsString);
      TransAuto(Sq1, '@Gqut4', nSqry.FieldByName('Gqut4').AsString);
      Translate(Sq1, '@Gname', nSqry.FieldByName('Gname').AsString);
      Translate(Sq1, '@Name1', nSqry.FieldByName('Name1').AsString);
      Translate(Sq1, '@Name2', nSqry.FieldByName('Name2').AsString);
      Translate(Sq1, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      TransAuto(Sq1, '@Gsqut', nSqry.FieldByName('Gsqut').AsString);
      TransAuto(Sq1, '@Gssum', nSqry.FieldByName('Gssum').AsString);

      Sqlen:=Sqlon+Sq1;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then begin
        ShowMessage(E_Insert);
        Exit;
      end;

    end else begin

      Sq1 := 'UPDATE T3_Ssub SET '+
      'Gqut1=  @Gqut1  ,Gqut2=  @Gqut2  ,Gqut3=  @Gqut3  , Gqut4=  @Gqut4  ,'+
      'Gname=''@Gname'',Name1=''@Name1'',Name2=''@Name2'', Gcode=''@Gcode'','+
      'Gsqut=  @Gsqut  ,Gssum=  @Gssum  '+
      'WHERE Gdate=''@Gdate'' and Hcode=''@Hcode'' ';

      Translate(Sq1, '@Gdate', mSqry.FieldByName('Gdate').AsString+'.'+nSqry.FieldByName('Gdate').AsString);
      Translate(Sq1, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      TransAuto(Sq1, '@Gqut1', nSqry.FieldByName('Gqut1').AsString);
      TransAuto(Sq1, '@Gqut2', nSqry.FieldByName('Gqut2').AsString);
      TransAuto(Sq1, '@Gqut3', nSqry.FieldByName('Gqut3').AsString);
      TransAuto(Sq1, '@Gqut4', nSqry.FieldByName('Gqut4').AsString);
      Translate(Sq1, '@Gname', nSqry.FieldByName('Gname').AsString);
      Translate(Sq1, '@Name1', nSqry.FieldByName('Name1').AsString);
      Translate(Sq1, '@Name2', nSqry.FieldByName('Name2').AsString);
      Translate(Sq1, '@Gcode', nSqry.FieldByName('Gcode').AsString);
      TransAuto(Sq1, '@Gsqut', nSqry.FieldByName('Gsqut').AsString);
      TransAuto(Sq1, '@Gssum', nSqry.FieldByName('Gssum').AsString);

      Sqlen:=Sq1;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then begin
        ShowMessage(E_Update);
        Exit;
      end;

    end;

    nSqry.Next;
    end;
  end;

  nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
  ShowMessage('저장완료');
end;

procedure TSobo45.Button401Click(Sender: TObject);
var St1,St2,St3: String;
    St9: Integer;
begin
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

  St1:='Gdate'+'>='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Gdate'+'<='+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;

  Sqlen := 'Select Hcode,'+
           'Sum01,Sum02,Sum03,Sum04,Sum05,Sum06,Sum07,Sum08,Sum09,Sum10,'+
           'Sum11,Sum12,Sum13,Sum14,Sum15,Sum16,Sum17,Sum18,Sum19,Sum20,'+
           'Sum21,Sum22,Sum23,Sum24,Sum25,Sum26,Sum27,Sum28,Sum29,Sum30,'+
           'Sum31,Sum32 '+
           ' From T2_Ssub Where '+St1;

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
    if nSqry.Locate('Gdate;Hcode',VarArrayOf([St3,'']),[loCaseInsensitive])=True then begin
    nSqry.Edit;
    nSqry.FieldByName('Gqut1').AsString:='';
    nSqry.FieldByName('Gqut2').AsString:='';
    nSqry.FieldByName('Gqut3').AsString:='';
    nSqry.FieldByName('Gqut4').AsString:='';
    nSqry.FieldByName('Name1').AsString:='';
    nSqry.FieldByName('Name2').AsString:='';
    nSqry.FieldByName('Gcode').AsString:='';
    nSqry.FieldByName('Gname').AsString:='';
    nSqry.FieldByName('Gsqut').AsString:='';
    nSqry.FieldByName('Gssum').AsString:='';
    nSqry.Post;
    end;
  end;

  St1:='Gdate'+'>='+#39+mSqry.FieldByName('Gdate').AsString+'.00'+#39+' and '+
       'Gdate'+'<='+#39+mSqry.FieldByName('Gdate').AsString+'.99'+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;

  Sqlen := 'Select Hcode,'+
           'Gdate,Gqut1,Gqut2,Gqut3,Gqut4,Name1,Name2,Gname,Gcode,Gsqut,Gssum '+
           ' From T3_Ssub Where '+St1;

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

    { Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 8,List1]);
      Translate(Sqlen, '@Hcode', '');
      nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);

      if nSqry.FieldByName('Gname').Value='' then begin
      Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', SGrid.Cells[ 8,List1]);
      Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
      nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
      end; }

      if SGrid.Cells[ 2,List1]<>'0' then
      nSqry.FieldByName('Gqut1').AsString:=SGrid.Cells[ 2,List1];
      if SGrid.Cells[ 3,List1]<>'0' then
      nSqry.FieldByName('Gqut2').AsString:=SGrid.Cells[ 3,List1];
      if SGrid.Cells[ 4,List1]<>'0' then
      nSqry.FieldByName('Gqut3').AsString:=SGrid.Cells[ 4,List1];
      if SGrid.Cells[ 5,List1]<>'0' then
      nSqry.FieldByName('Gqut4').AsString:=SGrid.Cells[ 5,List1];
      nSqry.FieldByName('Name1').AsString:=SGrid.Cells[ 6,List1];
      nSqry.FieldByName('Name2').AsString:=SGrid.Cells[ 7,List1];
      nSqry.FieldByName('Gname').AsString:=SGrid.Cells[ 8,List1];
      nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 9,List1];
      if SGrid.Cells[10,List1]<>'0' then
      nSqry.FieldByName('Gsqut').AsString:=SGrid.Cells[10,List1];
      if SGrid.Cells[11,List1]<>'0' then
      nSqry.FieldByName('Gssum').AsString:=SGrid.Cells[11,List1];
      nSqry.Post;
    end;
  end;

  nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
end;

procedure TSobo45.Button501Click(Sender: TObject);
var St1,St2: String;
begin
  St1:='Gdate'+'< '+#39+mSqry.FieldByName('Gdate').AsString+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;

  Sqlen := 'Select Max(Gdate) From T2_Ssub Where '+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  St2:='';
  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
     St2:=SGrid.Cells[ 0,List1];
  end;

  St1:='Gdate'+'>='+#39+St2+#39+' and '+
       'Gdate'+'<='+#39+St2+#39+' and '+
       'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;

  Sqlen := 'Select Hcode,'+
           'Sum01,Sum02,Sum03,Sum04,Sum05,Sum06,Sum07,Sum08,Sum09,Sum10,'+
           'Sum11,Sum12,Sum13,Sum14,Sum15,Sum16,Sum17,Sum18,Sum19,Sum20,'+
           'Sum21,Sum22,Sum23,Sum24,Sum25,Sum26,Sum27,Sum28,Sum29,Sum30,'+
           'Sum31,Sum32 '+
           ' From T2_Ssub Where '+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
  //Edit201.Value:=StrToIntDef(SGrid.Cells[ 1,List1],0);
    Edit202.Value:=StrToIntDef(SGrid.Cells[ 2,List1],0);
    Edit203.Value:=StrToIntDef(SGrid.Cells[ 3,List1],0);
    Edit204.Value:=StrToIntDef(SGrid.Cells[ 4,List1],0);
  //Edit205.Value:=StrToIntDef(SGrid.Cells[ 5,List1],0);
    Edit206.Value:=StrToIntDef(SGrid.Cells[ 6,List1],0);
  //Edit207.Value:=StrToIntDef(SGrid.Cells[ 7,List1],0);
  //Edit208.Value:=StrToIntDef(SGrid.Cells[ 8,List1],0);
    Edit209.Value:=StrToIntDef(SGrid.Cells[ 9,List1],0);
  //Edit210.Value:=StrToIntDef(SGrid.Cells[10,List1],0);
  //Edit211.Value:=StrToIntDef(SGrid.Cells[11,List1],0);
    Edit212.Value:=StrToIntDef(SGrid.Cells[12,List1],0);
  //Edit213.Value:=StrToIntDef(SGrid.Cells[13,List1],0);
  //Edit214.Value:=StrToIntDef(SGrid.Cells[14,List1],0);
    Edit215.Value:=StrToIntDef(SGrid.Cells[15,List1],0);
  //Edit216.Value:=StrToIntDef(SGrid.Cells[16,List1],0);
  //Edit217.Value:=StrToIntDef(SGrid.Cells[17,List1],0);
    Edit218.Value:=StrToIntDef(SGrid.Cells[18,List1],0);
    Edit219.Value:=StrToIntDef(SGrid.Cells[19,List1],0);
    Edit220.Value:=StrToIntDef(SGrid.Cells[20,List1],0);
  //Edit221.Value:=StrToIntDef(SGrid.Cells[21,List1],0);
    Edit222.Value:=StrToIntDef(SGrid.Cells[22,List1],0);
  //Edit223.Value:=StrToIntDef(SGrid.Cells[23,List1],0);
  { Edit224.Value:=StrToIntDef(SGrid.Cells[24,List1],0);
    Edit225.Value:=StrToIntDef(SGrid.Cells[25,List1],0);
    Edit226.Value:=StrToIntDef(SGrid.Cells[26,List1],0);
    Edit227.Value:=StrToIntDef(SGrid.Cells[27,List1],0);
    Edit228.Value:=StrToIntDef(SGrid.Cells[28,List1],0);
    Edit229.Value:=StrToIntDef(SGrid.Cells[29,List1],0);
    Edit230.Value:=StrToIntDef(SGrid.Cells[30,List1],0); }
  //Edit231.Value:=StrToIntDef(SGrid.Cells[31,List1],0);
    Edit232.Value:=StrToIntDef(SGrid.Cells[32,List1],0);
  end;
end;

procedure TSobo45.Button601Click(Sender: TObject);
var St1,St2,St3,St4: String;
    _S1_Ssub,_Sg_Csum,_Sv_Ghng: String;
begin
  {-Sv_Ghng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
          'Where Gdate < '+#39+mSqry.FieldByName('Gdate').AsString+'.99'+#39+
          ' and  Hcode = '+#39+mSqry.FieldByName('Hcode').AsString+#39;
  St1:=Base10.Seek_Name(Sqlen);

  {-In_Ssub-}
  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'<='+#39+mSqry.FieldByName('Gdate').AsString+'.99'+#39+' and '+
            'Ocode'+' ='+#39+'B'+#39+' and '+
            'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;
  _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'<='+#39+mSqry.FieldByName('Gdate').AsString+'.99'+#39+' and '+
            'Scode'+' ='+#39+'B'+#39+' and '+
            'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;
  _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Scode'+' ='+#39+'B'+#39+' and '+
            'Hcode'+' ='+#39+mSqry.FieldByName('Hcode').AsString+#39;
  Tong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng);

  T01:=0;
  T02:=Edit218.Value;
  T03:=0;

  sSqry.First;
  While sSqry.EOF=False do begin
    T01:=T01+sSqry.FieldByName('GsumX').AsFloat;
    T03:=T03+sSqry.FieldByName('Gbqut').AsFloat;
    sSqry.Next;
  end;

  if T01 > T02 then
  Edit221.Value:=T01-T02;
  Edit223.Value:=Edit221.Value * Edit222.Value;
  Edit231.Value:=T03;
end;

procedure TSobo45.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit103.Focused=True)and(Edit103.SelStart=24)and(Length(Trim(Edit103.Text))=24))or
    ((Edit105.Focused=True)and(Edit105.SelStart=24)and(Length(Trim(Edit105.Text))=24))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo45.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo45.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo45.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo45.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo45.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo45.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo45.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo45.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo45.Edit115KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo45.Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo45.Edit114KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo45.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo45.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo45.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo45.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo45.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo45.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo45.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo45.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo45.DataSource2DataChange(Sender: TObject; Field: TField);
var St1: String;
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
  Button401Click(Self);
end;

procedure TSobo45.Edit201Exit(Sender: TObject);
begin
  if(Edit202.Focused=True)or(Edit203.Focused=True)Then begin
  //Edit204.Value:=Edit202.Value * Edit203.Value;
  end else
  if(Edit205.Focused=True)or(Edit206.Focused=True)Then begin
    Edit207.Value:=Edit205.Value * Edit206.Value;
  end else
  if(Edit208.Focused=True)or(Edit209.Focused=True)Then begin
    Edit210.Value:=Edit208.Value * Edit209.Value;
  end else
  if(Edit211.Focused=True)or(Edit212.Focused=True)Then begin
    Edit213.Value:=Edit211.Value * Edit212.Value;
  end else
  if(Edit214.Focused=True)or(Edit215.Focused=True)Then begin
    Edit216.Value:=Edit214.Value * Edit215.Value;
  end else
  if(Edit218.Focused=True)or(Edit219.Focused=True)Then begin
  //Edit220.Value:=Edit218.Value * Edit219.Value;
  end else
  if(Edit221.Focused=True)or(Edit222.Focused=True)Then begin
    Edit223.Value:=Edit221.Value * Edit222.Value;
  end else
  if(Edit231.Focused=True)or(Edit232.Focused=True)Then begin
    Edit224.Value:=Edit231.Value * Edit232.Value;
  end;

    Edit227.Value:=Edit204.Value + Edit207.Value + Edit210.Value +
                   Edit213.Value + Edit216.Value + Edit217.Value +
                   Edit220.Value + Edit223.Value + Edit224.Value +
                   Edit225.Value + Edit226.Value;
    Edit228.Value:=Edit227.Value / 10;
    Edit230.Value:=Edit227.Value + Edit228.Value;
end;

end.
