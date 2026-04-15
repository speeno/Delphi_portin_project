unit Subu35;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit;

type
  TSobo35 = class(TForm)
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
    Panel102: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Button201: TFlatButton;
    DBGrid101: TDBGrid;
    DBGrid201: TDBGrid;
    StBar101: TStatusBar;
    StBar201: TStatusBar;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatMaskEdit;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Edit106: TFlatEdit;
    Label100: TmyLabel3d;
    Panel103: TFlatPanel;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
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
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo35: TSobo35;
  S3501,S3502: Double;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo35.FormActivate(Sender: TObject);
begin
  nForm:='35';
  nSqry:=Base10.T3_Sub51;
  mSqry:=Base10.T3_Sub52;
end;

procedure TSobo35.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"',Date);
end;

procedure TSobo35.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo35:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo35.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo35.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_35_01(Self);
  end;
end;

procedure TSobo35.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo35.Button004Click(Sender: TObject);
begin
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Tong20.Srart_35_01(Self);
  Tong20.Srart_35_02(Self);
  Tong20.Chang_00_01('35');
  Edit101.SetFocus;
end;

procedure TSobo35.Button005Click(Sender: TObject);
begin
  Tong20.Chang_00_02('35');
end;

procedure TSobo35.Button006Click(Sender: TObject);
begin
  T00:=1;
  Button201Click(Self);
end;

procedure TSobo35.Button007Click(Sender: TObject);
begin
  T00:=0;
  Button201Click(Self);
end;

procedure TSobo35.Button008Click(Sender: TObject);
begin
  Tong20.Zoom_Int_01('35');
end;

procedure TSobo35.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('35');
end;

procedure TSobo35.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtm2(DBGrid101, Caption);
end;

procedure TSobo35.Button011Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtm2(DBGrid201, Caption);
end;

procedure TSobo35.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX2(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo35.Button013Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo35.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('35-01');
end;

procedure TSobo35.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('35-02');
end;

procedure TSobo35.Button016Click(Sender: TObject);
begin
  Tong40.print_35_01(Self);
end;

procedure TSobo35.Button017Click(Sender: TObject);
begin
  Tong40.print_35_02(Self);
end;

procedure TSobo35.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo35.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo35.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo35.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo35.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo35.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo35.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo35.Button101Click(Sender: TObject);
var St0,St1,St2,St3,St4,St5: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;
  DataSource2.Enabled:=False;

  if Panel102.Caption='거래처명' Then begin St2:='X'; end;
  if Panel102.Caption='입고처명' Then begin St2:='Y'; end;
  if Panel102.Caption='거 래 처' Then begin St2:='Z'; end;

  {-Sv_Chng-}
  St1:='Hcode'+' ='+#39+Edit107.Text+#39;
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Chng Where '+St1;
  St0:=Base10.Seek_Name(Sqlen);

  St1:='Gdate'+' ='+#39+St0+#39+' and '+
       'Scode'+' ='+#39+St2+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Gcode'+'<='+#39+Edit105.Text+#39;

  {-Sv_Chng-}
  Sqlen :=
  'Select Gcode,Goqut,Gosum,Gjqut,Gjsum,Gbqut,Gbsum,Gsusu,Gssum '+
  'From Sv_Chng Where '+St1+
  'Order By Gcode ';

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

    St3:=SGrid.Cells[ 0,List1];

    St4:=Base10.Seek_Code(St3,St2,Edit107.Text);

    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin
      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
    end;

    nSqry.Edit;
    nSqry.FieldByName('Goqut').AsFloat:=
    nSqry.FieldByName('Goqut').AsFloat+StrToIntDef(SGrid.Cells[ 1,List1],0);
    nSqry.FieldByName('Gosum').AsFloat:=
    nSqry.FieldByName('Gosum').AsFloat+StrToIntDef(SGrid.Cells[ 2,List1],0)+StrToIntDef(SGrid.Cells[ 4,List1],0);
    nSqry.FieldByName('Gjqut').AsFloat:=
    nSqry.FieldByName('Gjqut').AsFloat+StrToIntDef(SGrid.Cells[ 3,List1],0);
    nSqry.FieldByName('Gbqut').AsFloat:=
    nSqry.FieldByName('Gbqut').AsFloat+StrToIntDef(SGrid.Cells[ 5,List1],0);
    nSqry.FieldByName('Gbsum').AsFloat:=
    nSqry.FieldByName('Gbsum').AsFloat+StrToIntDef(SGrid.Cells[ 6,List1],0);
    nSqry.FieldByName('Gsusu').AsFloat:=
    nSqry.FieldByName('Gsusu').AsFloat+StrToIntDef(SGrid.Cells[ 7,List1],0);
    nSqry.FieldByName('GsumY').AsFloat:=
    nSqry.FieldByName('GsumY').AsFloat+StrToIntDef(SGrid.Cells[ 8,List1],0)-+StrToIntDef(SGrid.Cells[ 7,List1],0);
    nSqry.Post;
  end;

  St1:='Gdate'+'<='+#39+St0+#39+' and '+
       'Scode'+' ='+#39+St2+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39;
  if Edit105.Text<>'' Then
  St1:='Gcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Gcode'+'<='+#39+Edit105.Text+#39+' and '+
       'Gdate'+'<='+#39+St0+#39+' and '+
       'Scode'+' ='+#39+St2+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39;

  {-Sg_Gsum-}
  Sqlen :=
  'Select Gcode,Sum(Gbsum)as Gbsum '+
  'From Sg_Gsum Where '+St1+
  'Group By Gcode';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    St3:=SGrid.Cells[ 0,List1];
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=True then begin
      nSqry.Edit;
      nSqry.FieldByName('Gjsum').AsFloat:=StrToIntDef(SGrid.Cells[ 1,List1],0);
      nSqry.Post;
    end;
  end;

  St1:='Gdate'+'> '+#39+St0+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+'.99'+#39+' and '+
       'Scode'+' ='+#39+St2+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39;
  if Edit105.Text<>'' Then
  St1:='Gdate'+'> '+#39+St0+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+'.99'+#39+' and '+
       'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Gcode'+'<='+#39+Edit105.Text+#39+' and '+
       'Scode'+' ='+#39+St2+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39;

  {-S1_Ssub-}
  Sqlen :=
  'Select Gcode,Scode,Gubun,Pubun, '+
  'Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
  'From S1_Ssub Where '+St1+
  'Group By Gcode,Scode,Gubun,Pubun ';

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

    T01:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    T02:=StrToIntDef(SGrid.Cells[ 5,List1],0);

    St3:=SGrid.Cells[ 0,List1];
    St4:=Base10.Seek_Code(St3,St2,Edit107.Text);

    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin
      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
    end;

    nSqry.Edit;
    St3:=SGrid.Cells[ 2,List1];
    St4:=SGrid.Cells[ 3,List1];
    St5:=SGrid.Cells[ 1,List1];
    if St3='반품' Then begin
      nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
      nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T02;
      nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat+T02;
    end else
    if St4='증정' Then begin
      nSqry.FieldByName('Gjqut').AsFloat:=nSqry.FieldByName('Gjqut').AsFloat+T01;
      nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T02;
      nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat+T02;
    end else
    if St3='출고' Then begin
      nSqry.FieldByName('Goqut').AsFloat:=nSqry.FieldByName('Goqut').AsFloat+T01;
      nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T02;
      nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat+T02;
    end else
    if St3='입고' Then begin
      nSqry.FieldByName('Goqut').AsFloat:=nSqry.FieldByName('Goqut').AsFloat+T01;
      nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T02;
      nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat+T02;
    end;
    nSqry.Post;
  end;

  {-H1_Ssub-}
  Sqlen :=
  'Select Gcode,Scode,Gubun,Gssum '+
  'From H1_Ssub Where '+St1;

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

    T01:=StrToIntDef(SGrid.Cells[ 3,List1],0);

    St3:=SGrid.Cells[ 0,List1];
    St4:=Base10.Seek_Code(St3,St2,Edit107.Text);

    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin
      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
    end;

    nSqry.Edit;
    if SGrid.Cells[ 2,List1]='입금' Then begin
    nSqry.FieldByName('Gsusu').AsFloat:=nSqry.FieldByName('Gsusu').AsFloat+T01;
    nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat-T01;
    end;
    if SGrid.Cells[ 2,List1]='출금' Then begin
    nSqry.FieldByName('Gsusu').AsFloat:=nSqry.FieldByName('Gsusu').AsFloat-T01;
    nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat+T01;
    end;
    nSqry.Post;
  end;

  {-Sg_Gsum-}
  Sqlen :=
  'Select Gcode,Sum(Gbsum)as Gbsum '+
  'From Sg_Gsum Where '+St1+
  'Group By Gcode,Gdate ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 1,List1],0);

    St3:=SGrid.Cells[ 0,List1];
    St4:=Base10.Seek_Code(St3,St2,Edit107.Text);

    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin
      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
    end;

    nSqry.Edit;
    nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01;
    nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat+T01;
    nSqry.Post;
  end;
  Base10.SpaceDel(nSqry,'Gcode','Gname');

  nSqry.IndexName := 'IDX'+'GCODE'+'DOWN';
  nSqry.First;
  Tong20.Srart_35_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo35.Button201Click(Sender: TObject);
var St1,St2,St3,St4,St5: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(mSqry);
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;

  if Panel102.Caption='거래처명' Then begin St3:='X'; end;
  if Panel102.Caption='입고처명' Then begin St3:='Y'; end;
  if Panel102.Caption='거 래 처' Then begin St3:='Z'; end;

  St2:=nSqry.FieldByName('Gcode').AsString;
  St4:=nSqry.FieldByName('Gname').AsString;
  if T00=1 Then Button101.Caption:='' else Button101.Caption:=St4;
  St1:='Gdate'+'>='+#39+Edit101.Text+'.00'+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+'.99'+#39+' and '+
       'Gcode'+' ='+#39+St2+#39+' and '+
       'Scode'+' ='+#39+St3+#39;
  if Button101.Caption='' Then
  St1:='Gdate'+'>='+#39+Edit101.Text+'.00'+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+'.99'+#39+' and '+
       'Scode'+' ='+#39+St3+#39;
  if(T00=1)and(Edit105.Text<>'')Then
  St1:='Gdate'+'>='+#39+Edit101.Text+'.00'+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+'.99'+#39+' and '+
       'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Gcode'+'<='+#39+Edit105.Text+#39+' and '+
       'Scode'+' ='+#39+St3+#39;
  if(T00=0)Then
  St1:='Gdate'+'>='+#39+Edit101.Text+'.00'+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+'.99'+#39+' and '+
       'Gcode'+' ='+#39+St2+#39+' and '+
       'Scode'+' ='+#39+St3+#39;

  St1:=St1+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39;

  {-S1_Ssub-}
  Sqlen :=
  'Select Gdate,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
  'From S1_Ssub Where '+St1+
  'Group By Gdate,Scode,Gubun,Pubun ';

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

    T01:=StrToIntDef(SGrid.Cells[ 4,List1],0);
    T02:=StrToIntDef(SGrid.Cells[ 5,List1],0);

    St3:=Copy(SGrid.Cells[ 0,List1],1,7);

    if mSqry.Locate('Gubun',St3,[loCaseInsensitive])=False then begin
      mSqry.Append;
      mSqry.FieldByName('Gubun').AsString:=St3;
    end;

    St3:=SGrid.Cells[ 2,List1];
    St4:=SGrid.Cells[ 3,List1];
    St5:=SGrid.Cells[ 1,List1];
    mSqry.Edit;
    if St3='반품' Then begin
      mSqry.FieldByName('Gbqut').AsFloat:=mSqry.FieldByName('Gbqut').AsFloat+T01;
      mSqry.FieldByName('Gbsum').AsFloat:=mSqry.FieldByName('Gbsum').AsFloat+T02;
      mSqry.FieldByName('GsumY').AsFloat:=mSqry.FieldByName('GsumY').AsFloat+T02;
    end else
    if St4='증정' Then begin
      mSqry.FieldByName('Gjqut').AsFloat:=mSqry.FieldByName('Gjqut').AsFloat+T01;
      mSqry.FieldByName('Gosum').AsFloat:=mSqry.FieldByName('Gosum').AsFloat+T02;
      mSqry.FieldByName('GsumY').AsFloat:=mSqry.FieldByName('GsumY').AsFloat+T02;
    end else
    if St3='출고' Then begin
      mSqry.FieldByName('Goqut').AsFloat:=mSqry.FieldByName('Goqut').AsFloat+T01;
      mSqry.FieldByName('Gosum').AsFloat:=mSqry.FieldByName('Gosum').AsFloat+T02;
      mSqry.FieldByName('GsumY').AsFloat:=mSqry.FieldByName('GsumY').AsFloat+T02;
    end else
    if St3='입고' Then begin
      mSqry.FieldByName('Goqut').AsFloat:=mSqry.FieldByName('Goqut').AsFloat+T01;
      mSqry.FieldByName('Gosum').AsFloat:=mSqry.FieldByName('Gosum').AsFloat+T02;
      mSqry.FieldByName('GsumY').AsFloat:=mSqry.FieldByName('GsumY').AsFloat+T02;
    end;
    mSqry.Post;
  end;

  {-H1_Ssub-}
  Sqlen :=
  'Select Gdate,Gubun,Gssum '+
  'From H1_Ssub Where '+St1+
  'Order By Gdate ';

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

    T01:=StrToIntDef(SGrid.Cells[ 2,List1],0);

    St3:=Copy(SGrid.Cells[ 0,List1],1,7);

    if mSqry.Locate('Gubun',St3,[loCaseInsensitive])=False then begin
      mSqry.Append;
      mSqry.FieldByName('Gubun').AsString:=St3;
    end;

    mSqry.Edit;
    if SGrid.Cells[ 1,List1]='입금' Then
    mSqry.FieldByName('Gsusu').AsFloat:=mSqry.FieldByName('Gsusu').AsFloat+T01;
    if SGrid.Cells[ 1,List1]='출금' Then
    mSqry.FieldByName('Gsusu').AsFloat:=mSqry.FieldByName('Gsusu').AsFloat-T01;
    mSqry.Post;
  end;

  {-Sg_Gsum-}
  Sqlen :=
  'Select Gdate,Gbsum '+
  'From Sg_Gsum Where '+St1+
  'Order By Gdate';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 1,List1],0);

    St3:=Copy(SGrid.Cells[ 0,List1],1,7);

    if mSqry.Locate('Gubun',St3,[loCaseInsensitive])=False then begin
      mSqry.Append;
      mSqry.FieldByName('Gubun').AsString:=St3;
    end;

    mSqry.Edit;
    mSqry.FieldByName('GsumX').AsFloat:=mSqry.FieldByName('GsumX').AsFloat+T01;
    mSqry.Post;
  end;

  mSqry.IndexName := 'IDX'+'GUBUN'+'DOWN';
  mSqry.First;
  Tong20.Srart_35_02(Self);
  DBGrid201.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo35.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=07)and(Length(Trim(Edit101.Text))=07))or
    ((Edit102.Focused=True)and(Edit102.SelStart=07)and(Length(Trim(Edit102.Text))=07))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit104.Focused=True)and(Edit104.SelStart=24)and(Length(Trim(Edit104.Text))=24))or
    ((Edit106.Focused=True)and(Edit106.SelStart=24)and(Length(Trim(Edit106.Text))=24))or
    ((Edit108.Focused=True)and(Edit108.SelStart=24)and(Length(Trim(Edit108.Text))=24))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo35.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo35.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo35.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo35.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo35.Edit114KeyPress(Sender: TObject; var Key: Char);
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
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if(Edit104.Focused=True)and(Panel102.Caption='거래처명')Then begin
       Edit103.Text:='';
    if Edit104.Text<>'' Then begin
    Seek10.Edit1.Text:=Edit104.Text;
    Seek10.FilterTing(Edit104.Text,Edit107.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek10.Query1Gcode.AsString;
      Edit104.Text:=Seek10.Query1Gname.AsString;
    end else
    if Seek10.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek10.Query1Gcode.AsString;
      Edit104.Text:=Seek10.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if(Edit106.Focused=True)and(Panel102.Caption='거래처명')Then begin
       Edit105.Text:='';
    if Edit106.Text<>'' Then begin
    Seek10.Edit1.Text:=Edit106.Text;
    Seek10.FilterTing(Edit106.Text,Edit107.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      Edit105.Text:=Seek10.Query1Gcode.AsString;
      Edit106.Text:=Seek10.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seek10.ShowModal=mrOK Then begin
      Edit105.Text:=Seek10.Query1Gcode.AsString;
      Edit106.Text:=Seek10.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  if(Edit104.Focused=True)and(Panel102.Caption='입고처명')Then begin
       Edit103.Text:='';
    if Edit104.Text<>'' Then begin
    Seek20.Edit1.Text:=Edit104.Text;
    Seek20.FilterTing(Edit104.Text,Edit107.Text);
    if Seek20.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek20.Query1Gcode.AsString;
      Edit104.Text:=Seek20.Query1Gname.AsString;
    end else
    if Seek20.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek20.Query1Gcode.AsString;
      Edit104.Text:=Seek20.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if(Edit106.Focused=True)and(Panel102.Caption='입고처명')Then begin
       Edit105.Text:='';
    if Edit106.Text<>'' Then begin
    Seek20.Edit1.Text:=Edit106.Text;
    Seek20.FilterTing(Edit106.Text,Edit107.Text);
    if Seek20.Query1.RecordCount=1 Then begin
      Edit105.Text:=Seek20.Query1Gcode.AsString;
      Edit106.Text:=Seek20.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seek20.ShowModal=mrOK Then begin
      Edit105.Text:=Seek20.Query1Gcode.AsString;
      Edit106.Text:=Seek20.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  if(Edit104.Focused=True)and(Panel102.Caption='거 래 처')Then begin
       Edit103.Text:='';
    if Edit104.Text<>'' Then begin
    Seek50.Edit1.Text:=Edit104.Text;
    Seek50.FilterTing(Edit104.Text,Edit107.Text);
    if Seek50.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek50.Query1Gcode.AsString;
      Edit104.Text:=Seek50.Query1Gname.AsString;
    end else
    if Seek50.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek50.Query1Gcode.AsString;
      Edit104.Text:=Seek50.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if(Edit106.Focused=True)and(Panel102.Caption='거 래 처')Then begin
       Edit105.Text:='';
    if Edit106.Text<>'' Then begin
    Seek50.Edit1.Text:=Edit106.Text;
    Seek50.FilterTing(Edit106.Text,Edit107.Text);
    if Seek50.Query1.RecordCount=1 Then begin
      Edit105.Text:=Seek50.Query1Gcode.AsString;
      Edit106.Text:=Seek50.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seek50.ShowModal=mrOK Then begin
      Edit105.Text:=Seek50.Query1Gcode.AsString;
      Edit106.Text:=Seek50.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo35.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo35.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo35.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo35.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo35.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo35.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo35.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo35.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo35.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

end.
