unit Subu37;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit;

type
  TSobo37 = class(TForm)
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
  Sobo37: TSobo37;
  S3701,S3702,S3703,S3704: Double;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo37.FormActivate(Sender: TObject);
begin
  nForm:='37';
  nSqry:=Base10.T3_Sub71;
  mSqry:=Base10.T3_Sub72;
end;

procedure TSobo37.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo37.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo37:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo37.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo37.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_37_01(Self);
  end;
end;

procedure TSobo37.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo37.Button004Click(Sender: TObject);
begin
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Tong20.Srart_37_01(Self);
  Tong20.Srart_37_02(Self);
  Tong20.Chang_00_01('37');
  Edit101.SetFocus;
end;

procedure TSobo37.Button005Click(Sender: TObject);
begin
  Tong20.Chang_00_02('37');
end;

procedure TSobo37.Button006Click(Sender: TObject);
begin
  T00:=1;
  Button201Click(Self);
end;

procedure TSobo37.Button007Click(Sender: TObject);
begin
  T00:=0;
  Button201Click(Self);
end;

procedure TSobo37.Button008Click(Sender: TObject);
begin
  Tong20.Zoom_Int_01('37');
end;

procedure TSobo37.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('37');
end;

procedure TSobo37.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo37.Button011Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo37.Button012Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX2(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo37.Button013Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX2(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo37.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('37-01');
end;

procedure TSobo37.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('37-02');
end;

procedure TSobo37.Button016Click(Sender: TObject);
begin
  Tong40.print_37_01(Self);
end;

procedure TSobo37.Button017Click(Sender: TObject);
begin
  Tong40.print_37_02(Self);
end;

procedure TSobo37.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo37.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo37.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo37.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo37.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo37.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo37.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo37.Button101Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6: String;
    nSumX,nSumY: Double;
    _S1_Ssub,_H1_Ssub,_Sg_Gsum,_Sv_Chng: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;
  DataSource2.Enabled:=False;

  if Panel102.Caption='거래처명' Then St2:='X';
  if Panel102.Caption='입고처명' Then St2:='Y';
  if Panel102.Caption='거 래 처' Then St2:='Z';

  Button101.Caption:='';

  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Scode'+' ='+#39+St2+#39;
  if Edit105.Text<>'' Then
  St1:=St1+' and '+
       'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
       'Gcode'+'<='+#39+Edit105.Text+#39;

  {-S1_Ssub-}
  Sqlen :=
  'Select Gcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
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
    St4:='';
    St5:='';
    St6:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if St2='X' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Y' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G2_Ggwo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Z' Then
      Sqlen := 'Select Gname,Ocode,Gpper,Gposa From G5_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';

      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', '');

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gpper
        if St2='Z' Then
        St4:=St4+'.'+Base10.Socket.GetData(1, 4);
      end else begin
      //--//
      if St2='X' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Y' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G2_Ggwo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Z' Then
      Sqlen := 'Select Gname,Ocode,Gpper,Gposa From G5_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';

      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gpper
        if St2='Z' Then
        St4:=St4+'.'+Base10.Socket.GetData(1, 4);
      end;
      //--//
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
    end;

    nSqry.Edit;
    St3:=SGrid.Cells[ 2,List1];
    St4:=SGrid.Cells[ 3,List1];
    St5:=SGrid.Cells[ 1,List1];
    if St3='반품' Then begin
      nSqry.FieldByName('Gsqut').AsFloat:=nSqry.FieldByName('Gsqut').AsFloat+T01;
      nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T02;
    end else
    if St4='증정' Then begin
      nSqry.FieldByName('Gjqut').AsFloat:=nSqry.FieldByName('Gjqut').AsFloat+T01;
      nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T02;
    end else
    if St3='출고' Then begin
      nSqry.FieldByName('Gsqut').AsFloat:=nSqry.FieldByName('Gsqut').AsFloat+T01;
      nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T02;
    end else
    if St3='입고' Then begin
      nSqry.FieldByName('Gsqut').AsFloat:=nSqry.FieldByName('Gsqut').AsFloat+T01;
      nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T02;
    end;
    nSqry.Post;
  end;

  if St2='Y' then begin
    St5:='Gubun='+#39+'출금'+#39+' and ';
    St6:='Gubun='+#39+'입금'+#39+' and ';
  end else begin
    St5:='Gubun='+#39+'입금'+#39+' and ';
    St6:='Gubun='+#39+'출금'+#39+' and ';
  end;
  St4:='';
  St4:=St4+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St4:=St4+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St5+St1+' ) as Gosum,';
  St4:=St4+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St6+St1+' ) as Gbsum ';
  St4:=St4+' From H1_Ssub S Where '+St1;

  if ePrnt='2' then begin
  St4:='';
  St4:=St4+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St4:=St4+' Sum(if('+St5+St1+',gssum,0))as Gosum,';
  St4:=St4+' Sum(if('+St6+St1+',gssum,0))as Gbsum ';
  St4:=St4+' From H1_Ssub S Where '+St1;
  end;

  {-H1_Ssub-}
  Sqlen := St4+' Group By Gcode ';

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
    T02:=StrToIntDef(SGrid.Cells[ 3,List1],0);

    St3:=SGrid.Cells[ 0,List1];
    St4:='';
    St5:='';
    St6:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if St2='X' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Y' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G2_Ggwo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Z' Then
      Sqlen := 'Select Gname,Ocode,Gpper,Gposa From G5_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';

      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', '');

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gpper
        if St2='Z' Then
        St4:=St4+'.'+Base10.Socket.GetData(1, 4);
      end else begin
      //--//
      if St2='X' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Y' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G2_Ggwo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Z' Then
      Sqlen := 'Select Gname,Ocode,Gpper,Gposa From G5_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';

      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gpper
        if St2='Z' Then
        St4:=St4+'.'+Base10.Socket.GetData(1, 4);
      end;
      //--//
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
    end;

    nSqry.Edit;
    nSqry.FieldByName('Gsusu').AsFloat:=nSqry.FieldByName('Gsusu').AsFloat+(T01-T02);
    nSqry.Post;
  end;

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

    T01:=StrToIntDef(SGrid.Cells[ 1,List1],0);

    St3:=SGrid.Cells[ 0,List1];
    St4:='';
    St5:='';
    St6:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if St2='X' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Y' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G2_Ggwo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Z' Then
      Sqlen := 'Select Gname,Ocode,Gpper,Gposa From G5_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';

      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', '');

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gpper
        if St2='Z' Then
        St4:=St4+'.'+Base10.Socket.GetData(1, 4);
      end else begin
      //--//
      if St2='X' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Y' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G2_Ggwo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Z' Then
      Sqlen := 'Select Gname,Ocode,Gpper,Gposa From G5_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';

      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gpper
        if St2='Z' Then
        St4:=St4+'.'+Base10.Socket.GetData(1, 4);
      end;
      //--//
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
    end;

    nSqry.Edit;
    nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01;
    nSqry.Post;
  end;

  {-Sv_Chng-}
  Sqlen :='Select Max(Gdate)as Gdate From Sv_Chng '+
          'Where Gdate < '+#39+Edit101.Text+#39+
          ' and  Hcode = '+#39+Edit107.Text+#39;
  St1:=Base10.Seek_Name(Sqlen);

  {-In_Ssub-}
  _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
            'Gdate'+'< '+#39+Edit101.Text+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
            'Scode'+' ='+#39+St2+#39;
  if Edit105.Text<>'' Then
  _S1_Ssub:=_S1_Ssub+' and '+
            'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Gcode'+'<='+#39+Edit105.Text+#39;

  _Sg_Gsum:=_S1_Ssub;
  _Sv_Chng:='Gdate'+' ='+#39+St1+#39+' and '+
            'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
            'Scode'+' ='+#39+St2+#39;
  if Edit105.Text<>'' Then
  _Sv_Chng:=_Sv_Chng+' and '+
            'Gcode'+'>='+#39+Edit103.Text+#39+' and '+
            'Gcode'+'<='+#39+Edit105.Text+#39;

  if St2='Y' then begin
    St5:='Gubun='+#39+'출금'+#39+' and ';
    St6:='Gubun='+#39+'입금'+#39+' and ';
  end else begin
    St5:='Gubun='+#39+'입금'+#39+' and ';
    St6:='Gubun='+#39+'출금'+#39+' and ';
  end;
  St4:='';
  St4:=St4+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St4:=St4+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St5+_S1_Ssub+' ) as Gosum,';
  St4:=St4+'(Select Sum(Gssum) From H1_Ssub Y Where S.Gcode=Y.Gcode and '+St6+_S1_Ssub+' ) as Gbsum ';
  St4:=St4+' From H1_Ssub S Where '+_S1_Ssub;
  _H1_Ssub:= St4;

  if ePrnt='2' then begin
  St4:='';
  St4:=St4+' Select S.Gcode,Sum(S.Gssum)as Gssum,';
  St4:=St4+' Sum(if('+St5+_S1_Ssub+',gssum,0))as Gosum,';
  St4:=St4+' Sum(if('+St6+_S1_Ssub+',gssum,0))as Gbsum ';
  St4:=St4+' From H1_Ssub S Where '+_S1_Ssub;
  _H1_Ssub:= St4;
  end;

  Tong40._Sv_Chng_(_S1_Ssub,_H1_Ssub,_Sg_Gsum,_Sv_Chng);
  sSqry.First;
  While sSqry.EOF=False do begin
    St3:=sSqry.FieldByName('Gcode').AsString;
    St4:='';
    St5:='';
    St6:='';
    if nSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      if St2='X' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Y' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G2_Ggwo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Z' Then
      Sqlen := 'Select Gname,Ocode,Gpper,Gposa From G5_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';

      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', '');

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gpper
        if St2='Z' Then
        St4:=St4+'.'+Base10.Socket.GetData(1, 4);
      end else begin
      //--//
      if St2='X' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Y' Then
      Sqlen := 'Select Gname,Ocode,Gpper From G2_Ggwo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      if St2='Z' Then
      Sqlen := 'Select Gname,Ocode,Gpper,Gposa From G5_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';

      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit107.Text);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St4:=Base10.Socket.GetData(1, 1); //Gname
        St5:=Base10.Socket.GetData(1, 2); //Ocode
        St6:=Base10.Socket.GetData(1, 3); //Gpper
        if St2='Z' Then
        St4:=St4+'.'+Base10.Socket.GetData(1, 4);
      end;
      //--//
      end;

      nSqry.Append;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gdate').AsString:=St5;
      nSqry.FieldByName('Gubun').AsString:=St6;
    end;
    nSqry.Edit;
    nSqry.FieldByName('GsumX').AsFloat:=sSqry.FieldByName('GsumX').AsFloat;
    nSqry.FieldByName('GsumY').AsFloat:=sSqry.FieldByName('GsumX').AsFloat;
    nSqry.Post;
    sSqry.Next;
  end;
  Base10.SpaceDel(nSqry,'Gcode','Gname');

  nSqry.First;
  mSqry.First;
  While nSqry.EOF=False do begin

    nSqry.Edit;
    nSqry.FieldByName('GsumY').AsFloat:=nSqry.FieldByName('GsumY').AsFloat+
    nSqry.FieldByName('Gosum').AsFloat+ nSqry.FieldByName('Gbsum').AsFloat-
    nSqry.FieldByName('Gsusu').AsFloat+ nSqry.FieldByName('Gjsum').AsFloat;
    nSqry.Post;

    St3:=nSqry.FieldByName('Gubun').AsString;
    St4:=nSqry.FieldByName('Gubun').AsString;

    if mSqry.Locate('Gubun',St3,[loCaseInsensitive])=False then begin
      mSqry.Append;
      mSqry.FieldByName('Gubun').AsString:=St3;
      mSqry.FieldByName('Gname').AsString:=St4;
    end;

    mSqry.Edit;
    mSqry.FieldByName('GsumX').AsFloat:=
    mSqry.FieldByName('GsumX').AsFloat+nSqry.FieldByName('GsumX').AsFloat;
    mSqry.FieldByName('Gsqut').AsFloat:=
    mSqry.FieldByName('Gsqut').AsFloat+nSqry.FieldByName('Gsqut').AsFloat;
    mSqry.FieldByName('Giqut').AsFloat:=
    mSqry.FieldByName('Giqut').AsFloat+nSqry.FieldByName('Giqut').AsFloat;
    mSqry.FieldByName('Gisum').AsFloat:=
    mSqry.FieldByName('Gisum').AsFloat+nSqry.FieldByName('Gisum').AsFloat;
    mSqry.FieldByName('Goqut').AsFloat:=
    mSqry.FieldByName('Goqut').AsFloat+nSqry.FieldByName('Goqut').AsFloat;
    mSqry.FieldByName('Gosum').AsFloat:=
    mSqry.FieldByName('Gosum').AsFloat+nSqry.FieldByName('Gosum').AsFloat;
    mSqry.FieldByName('Gbqut').AsFloat:=
    mSqry.FieldByName('Gbqut').AsFloat+nSqry.FieldByName('Gbqut').AsFloat;
    mSqry.FieldByName('Gbsum').AsFloat:=
    mSqry.FieldByName('Gbsum').AsFloat+nSqry.FieldByName('Gbsum').AsFloat;
    mSqry.FieldByName('Gjqut').AsFloat:=
    mSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gjqut').AsFloat;
    mSqry.FieldByName('Gjsum').AsFloat:=
    mSqry.FieldByName('Gjsum').AsFloat+nSqry.FieldByName('Gjsum').AsFloat;
    mSqry.FieldByName('Gsusu').AsFloat:=
    mSqry.FieldByName('Gsusu').AsFloat+nSqry.FieldByName('Gsusu').AsFloat;
    mSqry.FieldByName('GsumY').AsFloat:=
    mSqry.FieldByName('GsumY').AsFloat+nSqry.FieldByName('GsumY').AsFloat;
    mSqry.Post;
    nSqry.Next;
  end;

  nSqry.IndexName := 'IDX'+'GCODE'+'DOWN';
  mSqry.IndexName := 'IDX'+'GUBUN'+'DOWN';
  nSqry.First;
  mSqry.First;
  Tong20.Srart_37_01(Self);
  Tong20.Srart_37_02(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo37.Button201Click(Sender: TObject);
var St1: String;
begin
  Refresh;
  if(T00=0)Then begin
    Button101.Caption:=mSqry.FieldByName('Gname').AsString;
    St1:='Gubun'+'='+#39+mSqry.FieldByName('Gubun').AsString+#39;
    nSqry.Filter:=St1;
    nSqry.Filtered:=True;
  end;
  if(T00=1)Then begin
    Button101.Caption:='';
    nSqry.Filtered:=False;
  end;
  Tong20.Srart_37_02(Self);
end;

procedure TSobo37.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit104.Focused=True)and(Edit104.SelStart=24)and(Length(Trim(Edit104.Text))=24))or
    ((Edit106.Focused=True)and(Edit106.SelStart=24)and(Length(Trim(Edit106.Text))=24))or
    ((Edit108.Focused=True)and(Edit108.SelStart=24)and(Length(Trim(Edit108.Text))=24))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo37.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo37.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo37.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo37.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo37.Edit114KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo37.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo37.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo37.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo37.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo37.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo37.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo37.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo37.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo37.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

end.
