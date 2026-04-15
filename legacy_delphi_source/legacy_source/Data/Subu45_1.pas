unit Subu45;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit;

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
    DBGrid201: TDBGrid;
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
    Panel004: TFlatPanel;
    DBGrid301: TDBGrid;
    StBar301: TStatusBar;
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
    DataSource3: TDataSource;
    Button301: TFlatButton;
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
  tSqry:=Base10.T4_Sub71;
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
  Base10.OpenExit(tSqry);
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
{ T00:=1;
  Button201Click(Self); }
end;

procedure TSobo45.Button007Click(Sender: TObject);
begin
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
  Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo45.Button012Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo45.Button013Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1);
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
  Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
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
begin
//if Base10.Seek_Ggeo(Edit108.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Screen.Cursor:=crHourGlass;
  DataSource3.Enabled:=False;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);
  Base10.OpenShow(tSqry);

  St2:='X';

  St1:='Gdate'+'>='+#39+Edit101.Text+'.00'+#39+' and '+
       'Gdate'+'<='+#39+Edit101.Text+'.99'+#39+' and '+
       'Gubun'+' ='+#39+'Ãâ°í'+#39+' and '+
       'Scode'+' ='+#39+St2+#39;
  if (Edit104.Text<>'') Then
  St1:=St1+' and '+
       'Hcode'+'>='+#39+Edit102.Text+#39+' and '+
       'Hcode'+'<='+#39+Edit104.Text+#39;

  St2:=' Order By Gdate,Hcode,Gcode,Gubun,Jubun,ID';

  Sqlen := 'Select * From S1_Ssub Where '+St1+St2;

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

    Sqlen := 'Select Gname From G7_Ggeo Where Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Hcode').AsString);
    nSqry.FieldByName('Hname').Value:=Base10.Seek_Name(Sqlen);

    Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', '');
    nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);

    if nSqry.FieldByName('Gname').Value='' then begin
    Sqlen := 'Select Gname From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
    nSqry.FieldByName('Gname').Value:=Base10.Seek_Name(Sqlen);
    end;

    Sqlen := 'Select Gname,Gjeja From G4_Book Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
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

  St1:='Gdate'+'>='+#39+Edit101.Text+'.00'+#39+' and '+
       'Gdate'+'<='+#39+Edit101.Text+'.99'+#39;
  if (Edit104.Text<>'') Then
  St1:=St1+' and '+'Hcode'+'>='+#39+Edit102.Text+#39+
           ' and '+'Hcode'+'<='+#39+Edit102.Text+#39;

  St2:=' Order By Gdate,Hcode,Gcode';

  Sqlen := 'Select * From T1_Ssub Where '+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(tSqry)
  else ShowMessage(E_Open);

  tSqry.First;
  While tSqry.EOF=False do begin

    tSqry.Edit;

    Sqlen := 'Select Gname From G7_Ggeo Where Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', tSqry.FieldByName('Hcode').AsString);
    tSqry.FieldByName('Hname').Value:=Base10.Seek_Name(Sqlen);

    tSqry.FieldByName('Gname').Value:=Base10.Seek_Hname(tSqry.FieldByName('Gcode').AsString,tSqry.FieldByName('Hcode').AsString);

    tSqry.Post;
    tSqry.Next;
  end;

  Button201Click(Self);

  nSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource3.Enabled:=True;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo45.Button201Click(Sender: TObject);
var St1,St2,St3,St4,St5: String;
begin
  nSqry.First;
  mSqry.First;
  While nSqry.EOF=False do begin
    St1:=nSqry.FieldByName('Hcode').AsString;
    St3:=nSqry.FieldByName('Scode').AsString;
    if mSqry.Locate('Hcode;Scode',VarArrayOf([St1,St3]),[loCaseInsensitive])=False then begin
      mSqry.Append;
      mSqry.FieldByName('Hcode').AsString:=St1;
      mSqry.FieldByName('Scode').AsString:=St3;
      mSqry.FieldByName('Hname').AsString:=nSqry.FieldByName('Hname').AsString;
      mSqry.Post;
    end;
    nSqry.Next;
  end;
  nSqry.First;
  mSqry.First;
end;

procedure TSobo45.Button301Click(Sender: TObject);
var Sq1,Sq2,Sq3: String;
begin
  if nSqry.Active=True Then begin
    Sqlen := 'Select Gdate From T2_Ssub Where Gdate=''@Gdate'' ';
    Translate(Sqlen, '@Gdate', Edit101.Text);
    if Base10.Seek_Name(Sqlen)='' Then begin

      Sqlon := 'INSERT INTO T2_Ssub '+
      '( Gdate, Hcode, Sum01, Sum02, Sum03, Sum04, '+
      '  Sum05, Sum06, Sum07, Sum08, Sum09, Sum10, '+
      '  Sum11, Sum12, Sum13, Sum14, Sum15, Sum16, '+
      '  Sum17, Sum18, Sum19, Sum20, Sum21, Sum22, '+
      '  Sum23, Sum24, Sum25, Sum26, Sum27, Sum28, '+
      '  Sum29, Sum30 ) VALUES ';
      Sq1 :=
      '(''@Gdate'',''@Hcode'', @Sum01 , @Sum02 , @Sum03 , @Sum04 , '+
      '   @Sum05  ,  @Sum06  , @Sum07 , @Sum08 , @Sum09 , @Sum10 , ';
      Sq2 :=
      '   @Sum11  ,  @Sum12  , @Sum13 , @Sum14 , @Sum15 , @Sum16 , '+
      '   @Sum17  ,  @Sum18  , @Sum19 , @Sum20 , @Sum21 , @Sum22 , ';
      Sq3 :=
      '   @Sum23  ,  @Sum24  , @Sum25 , @Sum26 , @Sum27 , @Sum28 , '+
      '   @Sum29  ,  @Sum30  )';

      Translate(Sq1, '@Gdate', Edit101.Text);
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

      Sqlen:=Sqlon+Sq1+Sq2+Sq3;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then begin
        ShowMessage(E_Insert);
        Exit;
      end;

    end else begin

      Sq1 := 'UPDATE T2_Ssub SET '+
      'Gdate=''@Gdate'',Sum01=''@Sum01'',Sum02=''@Sum02'',Sum03=''@Sum03'', '+
      'Sum04=''@Sum04'',Sum05=''@Sum05'',Sum06=''@Sum06'',Sum07=''@Sum07'', '+
      'Sum08=''@Sum08'',Sum09=''@Sum09'',Sum10=''@Sum10'',Sum11=''@Sum11'', ';
      Sq2 :=
      'Sum12=''@Sum12'',Sum13=''@Sum13'',Sum14=''@Sum14'',Sum15=''@Sum15'', '+
      'Sum16=''@Sum16'',Sum17=''@Sum17'',Sum18=''@Sum18'',Sum19=''@Sum19'', '+
      'Sum20=''@Sum20'',Sum21=''@Sum21'',Sum22=''@Sum22'',Sum23=''@Sum23'', ';
      Sq3 :=
      'Sum24=''@Sum24'',Sum25=''@Sum25'',Sum26=''@Sum26'',Sum27=''@Sum27'', '+
      'Sum28=''@Sum28'',Sum29=''@Sum29'',Sum30=''@Sum30 '+
      'WHERE Gdate=''@Gdate'' and Hcode=''@Hcode'' ';

      Translate(Sq1, '@Gdate', Edit101.Text);
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
      Translate(Sq3, '@Gdate', Edit101.Text);
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
  if nSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo45.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo45.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
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

  St1:='';
  St1:=St1+'Hcode'+'='+#39+mSqry.FieldByName('Hcode').AsString+#39+' and ';
  St1:=St1+'Scode'+'='+#39+mSqry.FieldByName('Scode').AsString+#39;
  nSqry.Filter:=St1;
  nSqry.Filtered:=True;

  St1:='';
  St1:=St1+'Hcode'+'='+#39+mSqry.FieldByName('Hcode').AsString+#39;
  tSqry.Filter:=St1;
  tSqry.Filtered:=True;

  Tong20.Srart_45_01(Self);
  Tong20.Srart_45_02(Self);

  Sqlen := 'Select Gdate From T2_Ssub Where Gdate=''@Gdate'' and Hcode=''@Hcode'' ';
  Translate(Sqlen, '@Gdate', Edit101.Text);
  Translate(Sqlen, '@Hcode', mSqry.FieldByName('Hcode').AsString);
  if Base10.Seek_Name(Sqlen)='' Then begin
    Edit201.Value:=T01;
    Edit217.Value:=T02;
  end;
end;

end.
