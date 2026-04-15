unit Subu32;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit;

type
  TSobo32 = class(TForm)
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
    Panel103: TFlatPanel;
    Panel104: TFlatPanel;
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
    Panel105: TFlatPanel;
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
  Sobo32: TSobo32;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo32.FormActivate(Sender: TObject);
begin
  nForm:='32';
  nSqry:=Base10.T3_Sub21;
  mSqry:=Base10.T3_Sub22;
end;

procedure TSobo32.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo32.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo32:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo32.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo32.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo32.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo32.Button004Click(Sender: TObject);
begin
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Tong20.Srart_32_01(Self);
  Tong20.Srart_32_02(Self);
  Tong20.Chang_00_01('32');
  Edit101.SetFocus;
end;

procedure TSobo32.Button005Click(Sender: TObject);
begin
  Tong20.Chang_00_02('32');
end;

procedure TSobo32.Button006Click(Sender: TObject);
begin
  T00:=1;
  Button201Click(Self);
end;

procedure TSobo32.Button007Click(Sender: TObject);
begin
  T00:=0;
  Button201Click(Self);
end;

procedure TSobo32.Button008Click(Sender: TObject);
begin
  Tong20.Zoom_Int_01('32');
end;

procedure TSobo32.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('32');
end;

procedure TSobo32.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtm2(DBGrid101, Caption);
end;

procedure TSobo32.Button011Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtm2(DBGrid201, Caption);
end;

procedure TSobo32.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo32.Button013Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo32.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('32-01');
end;

procedure TSobo32.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('32-02');
end;

procedure TSobo32.Button016Click(Sender: TObject);
begin
  Tong40.print_32_01(Self);
end;

procedure TSobo32.Button017Click(Sender: TObject);
begin
  Tong40.print_32_02(Self);
end;

procedure TSobo32.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo32.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo32.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo32.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo32.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo32.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo32.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo32.Button101Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6,St7: String;
    nSumX,nSumY: Double;
    _S1_Ssub,_Sg_Csum,_Sv_Ghng: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;
  DataSource2.Enabled:=False;

  if Panel103.Caption='도 서 명' Then St2:='B';
  if Panel103.Caption='본사도서' Then St2:='A';
  if Panel103.Caption='창고도서' Then St2:='B';

  St3:=''; St4:='';
  St5:=''; St6:='';
  if Edit103.Text=Edit105.Text Then begin
    Seek40.FilterSing(Edit105.Text,Edit107.Text);
    While Seek40.Query1.EOF=False do begin
      St3:=St3+St4+'Bcode'+' = '+#39+Seek40.Query1Gcode.AsString+#39;
      St4:=' Or ';
      St5:=St5+St6+'Gcode'+' = '+#39+Seek40.Query1Gcode.AsString+#39;
      St6:=' Or ';
      Seek40.Query1.Next;
    end;
  end else begin
    St3:='Bcode'+' ='+#39+Edit103.Text+#39;
    St5:='Gcode'+' ='+#39+Edit103.Text+#39;
  end;
  St4:=St5;

  if Edit107.Text<>'' Then
  St3:=St3+' and '+
       'Hcode'+'='+#39+Edit107.Text+#39;
  if Edit107.Text<>'' Then
  St4:=St4+' and '+
       'Hcode'+'='+#39+Edit107.Text+#39;

  {-Sv_Ghng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
          'Where Gdate < '+#39+Edit101.Text+#39+
          ' and  Hcode = '+#39+Edit107.Text+#39;
  St1:=Base10.Seek_Name(Sqlen);

  {-In_Ssub-}
  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Edit101.Text+#39+' and '+
            '('+St3+')'+' and '+
            'Ocode'+' Like '+#39+'%'+St2+'%'+#39;
  _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Edit101.Text+#39+' and '+
            '('+St4+')'+' and '+
            'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
            '('+St4+')'+' and '+
            'Scode'+' Like '+#39+'%'+St2+'%'+#39;
  Tong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng);

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       '('+St3+')'+' and '+
       'Ocode'+' Like '+#39+'%'+St2+'%'+#39;

  {-S1_Ssub-}
  Sqlen :='Select Gdate,Scode,Gubun,Pubun,Bcode,Gbigo,Gsqut,Gssum '+
          'From S1_Ssub Where '+St1+' Order By Gdate,Jubun,Id ';

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

    T01:=StrToIntDef(SGrid.Cells[ 6,List1],0);
    T02:=StrToIntDef(SGrid.Cells[ 7,List1],0);

    St6:=SGrid.Cells[ 0,List1];

    if nSqry.Locate('Gdate',VarArrayOf([St6]),[loCaseInsensitive])=False then begin
      nSqry.Append;
      nSqry.FieldByName('Gdate').AsString:=St6;
      nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 4,List1];
    end;

    nSqry.Edit;
    St6:=SGrid.Cells[ 2,List1];
    St7:=SGrid.Cells[ 3,List1];
    St5:=SGrid.Cells[ 1,List1];
    if St5='Y' Then begin
      if St6='입고' Then begin
        nSqry.FieldByName('Giqut').AsFloat:=nSqry.FieldByName('Giqut').AsFloat+T01;
      end else
      if St6='반품' Then begin
        nSqry.FieldByName('Giqut').AsFloat:=nSqry.FieldByName('Giqut').AsFloat+T01;
      end;
    end else begin
      if St7='증정' Then begin
        nSqry.FieldByName('Gjqut').AsFloat:=nSqry.FieldByName('Gjqut').AsFloat+T01;
        nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T02;
      end else
      if St7='반품' Then begin
        nSqry.FieldByName('Gpsum').AsFloat:=nSqry.FieldByName('Gpsum').AsFloat-T01;
        nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
        nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T02;
      end else
      if St7='폐기' Then begin
        if St5='X' Then begin
          nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
          nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T02;
        end else begin
          if St5='Z' Then
          nSqry.FieldByName('Gpsum').AsFloat:=nSqry.FieldByName('Gpsum').AsFloat+T01;
          nSqry.FieldByName('Gpqut').AsFloat:=nSqry.FieldByName('Gpqut').AsFloat+T01;
          nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T02;
        end;
      end else
      if St6='출고' Then begin
        nSqry.FieldByName('Goqut').AsFloat:=nSqry.FieldByName('Goqut').AsFloat+T01;
        nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T02;
      end;
    end;
    nSqry.Post;
  end;

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       '('+St4+')'+' and '+
       'Scode'+' Like '+#39+'%'+St2+'%'+#39;

  {-Sg_Csum-}
  Sqlen :='Select Gdate,Gcode,Gbigo,Gbsum '+
          'From Sg_Csum Where '+St1+' Order By Gdate ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    T01:=StrToIntDef(SGrid.Cells[ 3,List1],0);

    St6:=SGrid.Cells[ 0,List1];
    St7:='YY';
    if nSqry.Locate('Gdate;Jubun',VarArrayOf([St6,St7]),[loCaseInsensitive])=False then begin
      if SGrid.Cells[ 2,List1]='' Then
      St7:='---변경수량---' else
      St7:='---'+SGrid.Cells[ 2,List1]+'---';
      nSqry.Append;
      nSqry.FieldByName('Gdate').AsString:=St6;
      nSqry.FieldByName('Gname').AsString:=St7;
      nSqry.FieldByName('Gcode').AsString:=SGrid.Cells[ 1,List1];
      nSqry.FieldByName('Jubun').AsString:='YY';
    end;
    nSqry.Edit;
    nSqry.FieldByName('Gsqut').AsFloat:=nSqry.FieldByName('Gsqut').AsFloat+T01;
    nSqry.Post;
  end;

  nSumX:=0;
  nSumY:=0;
  sSqry.First;
  While sSqry.EOF=False do begin
    nSumX:=nSumX+sSqry.FieldByName('GsumX').AsFloat;
    sSqry.Next;
  end;

  nSqry.Append;
  nSqry.FieldByName('Gdate').AsString:=' 전일재고 ';
  nSqry.FieldByName('GsumX').AsFloat :=nSumX;
  nSqry.FieldByName('GsumY').AsFloat :=nSumX;
  nSqry.Post;

  nSqry.IndexName := 'IDX'+'GDATE'+'DOWN';
  nSqry.First;
  nSqry.Next;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
    nSqry.Edit;
    nSqry.FieldByName('GsumX').AsFloat:=nSumX;
    nSumX:=nSumX+
  //nSqry.FieldByName('Gjqut').AsFloat-nSqry.FieldByName('Gbqut').AsFloat+
    nSqry.FieldByName('Giqut').AsFloat-nSqry.FieldByName('Goqut').AsFloat-
    nSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gsqut').AsFloat;
  //nSqry.FieldByName('Gpsum').AsFloat+nSqry.FieldByName('Gsqut').AsFloat;
    nSqry.FieldByName('GsumY').AsFloat:=nSumX;
    nSqry.Post;
    nSqry.Next;
  end;

  nSqry.First;
  Tong20.Srart_32_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo32.Button201Click(Sender: TObject);
var St1,St2,St3,St4: String;
    St5,St6,St7,St8,St9,nSumX: Double;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(mSqry);
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;

  if Panel103.Caption='도 서 명' Then St2:='B';
  if Panel103.Caption='본사도서' Then St2:='A';
  if Panel103.Caption='창고도서' Then St2:='B';

  if T00=1 Then Button101.Caption:='' else Button101.Caption:=nSqry.FieldByName('Gdate').AsString;
  Bmark:=nSqry.GetBookmark; nSqry.DisableControls;
  if T00=1 Then nSqry.First;
  nSumX:=nSqry.FieldByName('GsumX').AsFloat;

  mSqry.Append;
  mSqry.FieldByName('Gdate').AsString:=' 전일재고 ';
  mSqry.FieldByName('GsumY').AsFloat :=nSumX;
  mSqry.Post;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    if(nSqry.FieldByName('Jubun').AsString<>'YY')Then begin

    St1:='Gdate'+'='+#39+nSqry.FieldByName('Gdate').AsString+#39+' and '+
         'Bcode'+'='+#39+nSqry.FieldByName('Gcode').AsString+#39+' and '+
         'Hcode'+'='+#39+Edit107.Text+#39+' and '+
         'Ocode'+' Like '+#39+'%'+St2+'%'+#39;

    {-S1_Ssub-}
    Sqlen :='Select Gdate,Scode,Gubun,Pubun,Gcode,Gbigo,Grat1,Gsqut,Gssum,Gjisa '+
            'From S1_Ssub Where '+St1+' Order By Gdate,Jubun,Gubun,Gjisa DESC,Id ';

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    List1:=0;
    While SGrid.RowCount-1 > List1 do begin
    List1:=List1+1;

      T01:=StrToIntDef(SGrid.Cells[ 7,List1],0);
      T02:=StrToIntDef(SGrid.Cells[ 8,List1],0);

      St5:=0; St6:=0; St7:=0; St8:=0; St9:=0;
      St3:=SGrid.Cells[ 1,List1];
      St4:=SGrid.Cells[ 4,List1];

      St3:=Base10.Seek_Code(St4,St3,Edit107.Text);

      if SGrid.Cells[ 2,List1]='입고' Then begin
        St3:='입고('+SGrid.Cells[ 3,List1]+')'+St3;
        St5:=T01;
      { St8:=T02; }
        nSumX:=nSumX+T01;
      end else
      if SGrid.Cells[ 2,List1]='출고' Then begin
        St6:=T01;
        St8:=T02;
        nSumX:=nSumX-T01;
      end else
      if SGrid.Cells[ 3,List1]='반품' Then begin
        St7:=T01;
        St9:=T02;
        if SGrid.Cells[ 1,List1]='X' Then nSumX:=nSumX-T01;
        if SGrid.Cells[ 1,List1]='Y' Then nSumX:=nSumX+T01;
        if SGrid.Cells[ 1,List1]='Z' Then nSumX:=nSumX-T01;

        if SGrid.Cells[ 1,List1]='Y' Then begin
        St3:='입고(반품)';
        St5:=T01;
        St7:=0;
        St9:=0;
        end;
      end else
      if SGrid.Cells[ 3,List1]='폐기' Then begin
        St7:=T01;
        St9:=T02;
        if SGrid.Cells[ 1,List1]='X' Then nSumX:=nSumX;
        if SGrid.Cells[ 1,List1]='Y' Then nSumX:=nSumX-T01;
        if SGrid.Cells[ 1,List1]='Z' Then nSumX:=nSumX;

        if SGrid.Cells[ 1,List1]='Z' Then begin
        St3:='반품(폐기)';
        end;

        if SGrid.Cells[ 1,List1]='Y' Then begin
        St5:=T01;
        St7:=0;
        St9:=0;
        end;
      end;

      if SGrid.Cells[ 9,List1]<>'' then
      St3:=St3+'-'+SGrid.Cells[ 9,List1];

      mSqry.Append;
      mSqry.FieldByName('Gdate').AsString:=SGrid.Cells[ 0,List1];
      mSqry.FieldByName('Gname').AsString:=St3;
    //mSqry.FieldByName('Jubun').AsString:=lSqry.FieldByName('Jubun').AsString;
      mSqry.FieldByName('Gsqut').AsFloat :=StrToIntDef(SGrid.Cells[ 6,List1],0);
      mSqry.FieldByName('Giqut').AsFloat :=St5;
      mSqry.FieldByName('Goqut').AsFloat :=St6;
      mSqry.FieldByName('Gbqut').AsFloat :=St7;
      mSqry.FieldByName('Gosum').AsFloat :=St8;
      mSqry.FieldByName('Gbsum').AsFloat :=St9;
      mSqry.FieldByName('GsumY').AsFloat :=nSumX;
      mSqry.Post;
    end;

    end else
    if(nSqry.FieldByName('Jubun').AsString='YY')Then begin

    St1:='Gdate'+'='+#39+nSqry.FieldByName('Gdate').AsString+#39+' and '+
         'Gcode'+'='+#39+nSqry.FieldByName('Gcode').AsString+#39+' and '+
         'Hcode'+'='+#39+Edit107.Text+#39+' and '+
         'Scode'+' Like '+#39+'%'+St2+'%'+#39;

    {-Sg_Csum-}
    Sqlen :='Select Gdate,Gcode,Gbigo,Gbsum '+
            'From Sg_Csum Where '+St1+' Order By Gdate ';

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    List1:=0;
    While SGrid.RowCount-1 > List1 do begin
    List1:=List1+1;

      T01:=StrToIntDef(SGrid.Cells[ 3,List1],0);

      St9:=0;
      if SGrid.Cells[ 2,List1]='' Then
      St4:='---변경수량---' else
      St4:='---'+SGrid.Cells[ 2,List1]+'---';
      St9:=T01;
      nSumX:=nSumX+T01;
      mSqry.Append;
      mSqry.FieldByName('Gdate').AsString:=SGrid.Cells[ 0,List1];
      mSqry.FieldByName('Gname').AsString:=St4;
      mSqry.FieldByName('Gbqut').AsFloat :=St9;
      mSqry.FieldByName('GsumY').AsFloat :=nSumX;
      mSqry.Post;
    end;

    end;

    if T00<>1 Then
    nSqry.Last;
    nSqry.Next;
  end;

  nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
  mSqry.First;
  Tong20.Srart_32_02(Self);
  DBGrid201.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo32.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit103.Focused=True)and(Edit103.SelStart=10)and(Length(Trim(Edit103.Text))=10))or
    ((Edit104.Focused=True)and(Edit104.SelStart=40)and(Length(Trim(Edit104.Text))=40))or
    ((Edit108.Focused=True)and(Edit108.SelStart=24)and(Length(Trim(Edit108.Text))=24))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo32.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo32.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo32.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo32.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo32.Edit114KeyPress(Sender: TObject; var Key: Char);
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
    end;
  end else
  if(Edit103.Focused=True)or(Edit104.Focused=True)Then begin
    if(Edit103.Text='')and(Edit104.Text='') Then Exit;
    if Edit103.Focused=True Then begin
      Seek40.Edit1.Text:=Edit103.Text;
      Seek40.FilterTing(Edit103.Text,Edit107.Text);
      if Seek40.Query1.IsEmpty=True Then Exit;
    end;
    if Edit104.Focused=True Then begin
      Seek40.Edit1.Text:=Edit104.Text;
      Seek40.FilterTing(Edit104.Text,Edit107.Text);
      if Seek40.Query1.IsEmpty=True Then Exit;
    end;
    if Seek40.Query1.RecordCount=1 Then begin
      Edit103.Text:=Seek40.Query1Gcode.AsString;
      Edit104.Text:=Seek40.Query1Gname.AsString;
      Edit105.Text:=Seek40.Query1Ocode.AsString;
      Edit106.Text:=FloatToStr(Seek40.Query1Gdang.AsFloat);
      Button101Click(Self);
    end else
    if Seek40.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit103.Text:=Seek40.Query1Gcode.AsString;
      Edit104.Text:=Seek40.Query1Gname.AsString;
      Edit105.Text:=Seek40.Query1Ocode.AsString;
      Edit106.Text:=FloatToStr(Seek40.Query1Gdang.AsFloat);
      Button101Click(Self);
    end;
  end;
  end;
end;

procedure TSobo32.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo32.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo32.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo32.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo32.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo32.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo32.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo32.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo32.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

end.
