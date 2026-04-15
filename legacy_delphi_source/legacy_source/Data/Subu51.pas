unit Subu51;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, Gauges;

type
  TSobo51 = class(TForm)
    FlatPanel1: TFlatPanel;
    RadioGroup1: TRadioGroup;
    RadioGroup2: TRadioGroup;
    GroupBox1: TGroupBox;
    GroupBox2: TGroupBox;
    Button101: TFlatButton;
    Label100: TmyLabel3d;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    Edit101: TFlatEdit;
    Edit102: TFlatEdit;
    Gauge1: TGauge;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Label103: TmyLabel3d;
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
    procedure Button302Click(Sender: TObject);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo51: TSobo51;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib, Seak08,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo51.FormActivate(Sender: TObject);
begin
  nForm:='56';
end;

procedure TSobo51.FormShow(Sender: TObject);
begin
//
end;

procedure TSobo51.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo56:=nil;
end;

procedure TSobo51.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button012Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button014Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button015Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button016Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button017Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button101Click(Sender: TObject);
begin
  if Edit107.Text<>'' then
  Sobo51.Button302Click(Self)
  else
  Sobo51.Button301Click(Self);
end;

procedure TSobo51.Button201Click(Sender: TObject);
begin
  if(RadioGroup1.ItemIndex=0)or(RadioGroup1.ItemIndex=1)or
    (RadioGroup1.ItemIndex=2)or(RadioGroup1.ItemIndex=3)or
    (RadioGroup1.ItemIndex=4)or(RadioGroup1.ItemIndex=5)or
    (RadioGroup1.ItemIndex=6)Then begin
    Button101.Enabled:=True;
  end;
end;

procedure TSobo51.Button301Click(Sender: TObject);
var Cnt: Double;
    St0,St1,St2,St3: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

{ if Edit101.Text=Edit102.Text Then Exit; }

  St1:=Edit101.Text;
  St2:=Edit102.Text;
  St3:='코드가 이미 등록되어 있습니다. 그래도 변경할까요?';
  if(RadioGroup1.ItemIndex=0)Then begin

    if Base10.Seek_Code(St2,'X',Edit107.Text)<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=1)Then begin

    if Base10.Seek_Code(St2,'Y',Edit107.Text)<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=2)Then begin

    if Base10.Seek_Code(St2,'Z',Edit107.Text)<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=3)Then begin

    Sqlen := 'Select Gcode From G3_Gjeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    if Base10.Seek_Name(Sqlen)<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=4)Then begin

    if Base10.Seek_Code(St2,'B',Edit107.Text)<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=5)Then begin

    if Base10.Seek_Code(St2,'Z',Edit107.Text)<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=6)Then begin

    if Base10.Seek_Code(St2,'X',Edit107.Text)<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  Screen.Cursor:=crHourGlass;
  //-- 0 --//
  if(RadioGroup1.ItemIndex=0)or(RadioGroup1.ItemIndex=1)or(RadioGroup1.ItemIndex=2)Then begin
    if RadioGroup1.ItemIndex=0 Then St0:='X';
    if RadioGroup1.ItemIndex=1 Then St0:='Y';
    if RadioGroup1.ItemIndex=2 Then St0:='Z';

    RadioGroup2.ItemIndex:=0;

    Sqlen := 'UPDATE S1_Ssub SET Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=1;

    Sqlen := 'UPDATE H1_Ssub SET Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=2;

    Sqlen := 'UPDATE Sv_Gsum SET Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=4;

    Sqlen := 'UPDATE Sv_Chng SET Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Gs_Gsum SET Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Sg_Gsum SET Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE In_Gsum SET Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 0 --//
  if RadioGroup1.ItemIndex=0 Then begin
    RadioGroup2.ItemIndex:=0;

    Sqlen := 'UPDATE G6_Ggeo SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE G1_Ggeo SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 1 --//
  if RadioGroup1.ItemIndex=1 Then begin
    RadioGroup2.ItemIndex:=1;

    Sqlen := 'UPDATE S2_Ssub SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE G2_Ggwo SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 2 --//
  if RadioGroup1.ItemIndex=2 Then begin

    Sqlen := 'UPDATE G5_Ggeo SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 3 --//
  if RadioGroup1.ItemIndex=3 Then begin
    RadioGroup2.ItemIndex:=2;

    Sqlen := 'UPDATE S3_Ssub SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE G3_Gjeo SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 4 --//
  if RadioGroup1.ItemIndex=4 Then begin

    RadioGroup2.ItemIndex:=0;

    Sqlen := 'UPDATE S1_Ssub SET Bcode=''@Zcode'''+
             'WHERE Bcode=''@Bcode'' ';
    Translate(Sqlen, '@Bcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=3;

    Sqlen := 'UPDATE Sv_Csum SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=5;

    Sqlen := 'UPDATE Sv_Ghng SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Gs_Csum SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Sg_Csum SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE In_Csum SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=1;

    Sqlen := 'UPDATE G6_Ggeo SET Bcode=''@Zcode'''+
             'WHERE Bcode=''@Bcode'' ';
    Translate(Sqlen, '@Bcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE G4_Book SET Gcode=''@Zcode'''+
             'WHERE Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 5 --//
  if(RadioGroup1.ItemIndex=5)or(RadioGroup1.ItemIndex=6)Then begin
    if RadioGroup1.ItemIndex=5 Then begin St0:='X'; St3:='Z'; end;
    if RadioGroup1.ItemIndex=6 Then begin St0:='Z'; St3:='X'; end;

    RadioGroup2.ItemIndex:=0;

    Sqlen := 'UPDATE S1_Ssub SET Scode=''@Ycode'',Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=1;

    Sqlen := 'UPDATE H1_Ssub SET Scode=''@Ycode'',Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=2;

    Sqlen := 'UPDATE Sv_Gsum SET Scode=''@Ycode'',Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=4;

    Sqlen := 'UPDATE Sv_Chng SET Scode=''@Ycode'',Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Gs_Gsum SET Scode=''@Ycode'',Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Sg_Gsum SET Scode=''@Ycode'',Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE In_Gsum SET Scode=''@Ycode'',Gcode=''@Zcode'''+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  if RadioGroup1.ItemIndex=5 Then begin

    Sqlen := 'DELETE FROM G6_Ggeo WHERE Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', St1);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    Sqlen := 'Select '+
    'Gubun,Jubun,Gcode,Ocode,Gname,Gposa,Gnumb,Guper,Gjomo,'+
    'Gtel1,Gtel2,Gfax1,Gfax2,Gpost,Gadd1,Gadd2,Gpper,Gbigo,'+
    'Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Grat7,Grat8,Grat9,Gqut1 '+
    'From G1_Ggeo Where Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', St1);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then begin
       Base10.Socket.MakeGrid(SGrid);

      Sqlon := 'INSERT INTO G5_Ggeo '+
      '( Gubun, Jubun, Gcode, Ocode, Gname, Gposa, '+
      '  Gnumb, Guper, Gjomo, Gtel1, Gtel2, Gfax1, '+
      '  Gfax2, Gpost, Gadd1, Gadd2, Gpper, Gbigo, '+
      '  Grat1, Grat2, Grat3, Grat4, Grat5, Grat6, '+
      '  Grat7, Grat8, Grat9, Gqut1 ) VALUES ';
      Sqlen :=
      '(''@Gubun'',''@Jubun'',''@Gcode'',''@Ocode'',''@Gname'',''@Gposa'', '+
      ' ''@Gnumb'',''@Guper'',''@Gjomo'',''@Gtel1'',''@Gtel2'',''@Gfax1'', '+
      ' ''@Gfax2'',''@Gpost'',''@Gadd1'',''@Gadd2'',''@Gpper'',''@Gbigo'', '+
      '   @Grat1  ,  @Grat2  ,  @Grat3  ,  @Grat4  ,  @Grat5  ,  @Grat6  , '+
      '   @Grat7  ,  @Grat8  ,  @Grat9  ,  @Gqut1  )';

      Translate(Sqlen, '@Gubun', SGrid.Cells[ 0,1]);
      Translate(Sqlen, '@Jubun', SGrid.Cells[ 1,1]);
      Translate(Sqlen, '@Gcode', St2);
      Translate(Sqlen, '@Ocode', SGrid.Cells[ 3,1]);
      Translate(Sqlen, '@Gname', SGrid.Cells[ 4,1]);
      Translate(Sqlen, '@Gposa', SGrid.Cells[ 5,1]);
      Translate(Sqlen, '@Gnumb', SGrid.Cells[ 6,1]);
      Translate(Sqlen, '@Guper', SGrid.Cells[ 7,1]);
      Translate(Sqlen, '@Gjomo', SGrid.Cells[ 8,1]);
      Translate(Sqlen, '@Gtel1', SGrid.Cells[ 9,1]);
      Translate(Sqlen, '@Gtel2', SGrid.Cells[10,1]);
      Translate(Sqlen, '@Gfax1', SGrid.Cells[11,1]);
      Translate(Sqlen, '@Gfax2', SGrid.Cells[12,1]);
      Translate(Sqlen, '@Gpost', SGrid.Cells[13,1]);
      Translate(Sqlen, '@Gadd1', SGrid.Cells[14,1]);
      Translate(Sqlen, '@Gadd2', SGrid.Cells[15,1]);
      Translate(Sqlen, '@Gpper', SGrid.Cells[16,1]);
      Translate(Sqlen, '@Gbigo', SGrid.Cells[17,1]);
      TransAuto(Sqlen, '@Grat1', SGrid.Cells[18,1]);
      TransAuto(Sqlen, '@Grat2', SGrid.Cells[19,1]);
      TransAuto(Sqlen, '@Grat3', SGrid.Cells[20,1]);
      TransAuto(Sqlen, '@Grat4', SGrid.Cells[21,1]);
      TransAuto(Sqlen, '@Grat5', SGrid.Cells[22,1]);
      TransAuto(Sqlen, '@Grat6', SGrid.Cells[23,1]);
      TransAuto(Sqlen, '@Grat7', SGrid.Cells[24,1]);
      TransAuto(Sqlen, '@Grat8', SGrid.Cells[25,1]);
      TransAuto(Sqlen, '@Grat9', SGrid.Cells[26,1]);
      TransAuto(Sqlen, '@Gqut1', SGrid.Cells[27,1]);

      Sqlen:=Sqlon+Sqlen;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end
    else ShowMessage(E_Open);

    Sqlen := 'DELETE FROM G1_Ggeo WHERE Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', St1);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

  end;
  if RadioGroup1.ItemIndex=6 Then begin

    Sqlen := 'Select '+
    'Gubun,Jubun,Gcode,Ocode,Gname,Gposa,Gnumb,Guper,Gjomo,'+
    'Gtel1,Gtel2,Gfax1,Gfax2,Gpost,Gadd1,Gadd2,Gpper,Gbigo,'+
    'Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Grat7,Grat8,Grat9,Gqut1 '+
    'From G5_Ggeo Where Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', St1);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then begin
       Base10.Socket.MakeGrid(SGrid);

      Sqlon := 'INSERT INTO G1_Ggeo '+
      '( Gubun, Jubun, Gcode, Ocode, Gname, Gposa, '+
      '  Gnumb, Guper, Gjomo, Gtel1, Gtel2, Gfax1, '+
      '  Gfax2, Gpost, Gadd1, Gadd2, Gpper, Gbigo, '+
      '  Grat1, Grat2, Grat3, Grat4, Grat5, Grat6, '+
      '  Grat7, Grat8, Grat9, Gqut1 ) VALUES ';
      Sqlen :=
      '(''@Gubun'',''@Jubun'',''@Gcode'',''@Ocode'',''@Gname'',''@Gposa'', '+
      ' ''@Gnumb'',''@Guper'',''@Gjomo'',''@Gtel1'',''@Gtel2'',''@Gfax1'', '+
      ' ''@Gfax2'',''@Gpost'',''@Gadd1'',''@Gadd2'',''@Gpper'',''@Gbigo'', '+
      '   @Grat1  ,  @Grat2  ,  @Grat3  ,  @Grat4  ,  @Grat5  ,  @Grat6  , '+
      '   @Grat7  ,  @Grat8  ,  @Grat9  ,  @Gqut1  )';

      Translate(Sqlen, '@Gubun', SGrid.Cells[ 0,1]);
      Translate(Sqlen, '@Jubun', SGrid.Cells[ 1,1]);
      Translate(Sqlen, '@Gcode', St2);
      Translate(Sqlen, '@Ocode', SGrid.Cells[ 3,1]);
      Translate(Sqlen, '@Gname', SGrid.Cells[ 4,1]);
      Translate(Sqlen, '@Gposa', SGrid.Cells[ 5,1]);
      Translate(Sqlen, '@Gnumb', SGrid.Cells[ 6,1]);
      Translate(Sqlen, '@Guper', SGrid.Cells[ 7,1]);
      Translate(Sqlen, '@Gjomo', SGrid.Cells[ 8,1]);
      Translate(Sqlen, '@Gtel1', SGrid.Cells[ 9,1]);
      Translate(Sqlen, '@Gtel2', SGrid.Cells[10,1]);
      Translate(Sqlen, '@Gfax1', SGrid.Cells[11,1]);
      Translate(Sqlen, '@Gfax2', SGrid.Cells[12,1]);
      Translate(Sqlen, '@Gpost', SGrid.Cells[13,1]);
      Translate(Sqlen, '@Gadd1', SGrid.Cells[14,1]);
      Translate(Sqlen, '@Gadd2', SGrid.Cells[15,1]);
      Translate(Sqlen, '@Gpper', SGrid.Cells[16,1]);
      Translate(Sqlen, '@Gbigo', SGrid.Cells[17,1]);
      TransAuto(Sqlen, '@Grat1', SGrid.Cells[18,1]);
      TransAuto(Sqlen, '@Grat2', SGrid.Cells[19,1]);
      TransAuto(Sqlen, '@Grat3', SGrid.Cells[20,1]);
      TransAuto(Sqlen, '@Grat4', SGrid.Cells[21,1]);
      TransAuto(Sqlen, '@Grat5', SGrid.Cells[22,1]);
      TransAuto(Sqlen, '@Grat6', SGrid.Cells[23,1]);
      TransAuto(Sqlen, '@Grat7', SGrid.Cells[24,1]);
      TransAuto(Sqlen, '@Grat8', SGrid.Cells[25,1]);
      TransAuto(Sqlen, '@Grat9', SGrid.Cells[26,1]);
      TransAuto(Sqlen, '@Gqut1', SGrid.Cells[27,1]);

      Sqlen:=Sqlon+Sqlen;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end
    else ShowMessage(E_Open);

    Sqlen := 'DELETE FROM G5_Ggeo WHERE Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', St1);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

  end;

  Edit101.Text:='';
  Edit102.Text:='';
  Gauge1.Progress:=0;
  RadioGroup1.ItemIndex:=-1;
  RadioGroup2.ItemIndex:=-1;
  Button101.Enabled:=False;
  Screen.Cursor:=crDefault;
  ShowMessage('완료');
end;

procedure TSobo51.Button302Click(Sender: TObject);
var Cnt: Double;
    St0,St1,St2,St3,St4: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

{ if Edit101.Text=Edit102.Text Then Exit; }

  St1:=Edit101.Text;
  St2:=Edit102.Text;
  St3:='코드가 이미 등록되어 있습니다. 그래도 변경할까요?';
  St4:='Hcode'+' ='+#39+Hnnnn+#39;
  if(RadioGroup1.ItemIndex=0)Then begin

    if Base10.Seek_Code(St2,'X')<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=1)Then begin

    if Base10.Seek_Code(St2,'Y')<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=2)Then begin

    if Base10.Seek_Code(St2,'Z')<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=3)Then begin

    Sqlen := 'Select Gcode From G3_Gjeo Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    if Base10.Seek_Name(Sqlen)<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=4)Then begin

    if Base10.Seek_Code(St2,'B')<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=5)Then begin

    if Base10.Seek_Code(St2,'Z')<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  if(RadioGroup1.ItemIndex=6)Then begin

    if Base10.Seek_Code(St2,'X')<>'' Then
    if MessageDlg(St3,mtConfirmation,[mbYes,mbNo],0)=mrNo then Exit;

  end;
  Screen.Cursor:=crHourGlass;
  //-- 0 --//
  if(RadioGroup1.ItemIndex=0)or(RadioGroup1.ItemIndex=1)or(RadioGroup1.ItemIndex=2)Then begin
    if RadioGroup1.ItemIndex=0 Then St0:='X';
    if RadioGroup1.ItemIndex=1 Then St0:='Y';
    if RadioGroup1.ItemIndex=2 Then St0:='Z';

    RadioGroup2.ItemIndex:=0;

    Sqlen := 'UPDATE S1_Ssub SET Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=1;

    Sqlen := 'UPDATE H1_Ssub SET Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=2;

    Sqlen := 'UPDATE Sv_Gsum SET Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=4;

    Sqlen := 'UPDATE Sv_Chng SET Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Gs_Gsum SET Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Sg_Gsum SET Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE In_Gsum SET Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 0 --//
  if RadioGroup1.ItemIndex=0 Then begin
    RadioGroup2.ItemIndex:=0;

    Sqlen := 'UPDATE G6_Ggeo SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE G1_Ggeo SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 1 --//
  if RadioGroup1.ItemIndex=1 Then begin
    RadioGroup2.ItemIndex:=1;

    Sqlen := 'UPDATE S2_Ssub SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE G2_Ggwo SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 2 --//
  if RadioGroup1.ItemIndex=2 Then begin

    Sqlen := 'UPDATE G5_Ggeo SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 3 --//
  if RadioGroup1.ItemIndex=3 Then begin
    RadioGroup2.ItemIndex:=2;

    Sqlen := 'UPDATE S3_Ssub SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE G3_Gjeo SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 4 --//
  if RadioGroup1.ItemIndex=4 Then begin

    RadioGroup2.ItemIndex:=0;

    Sqlen := 'UPDATE S1_Ssub SET Bcode=''@Zcode'' '+
             'WHERE Bcode=''@Bcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Bcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=3;

    Sqlen := 'UPDATE Sv_Csum SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=5;

    Sqlen := 'UPDATE Sv_Ghng SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Gs_Csum SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Sg_Csum SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE In_Csum SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=1;

    Sqlen := 'UPDATE G6_Ggeo SET Bcode=''@Zcode'' '+
             'WHERE Bcode=''@Bcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Bcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE G4_Book SET Gcode=''@Zcode'' '+
             'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  //-- 5 --//
  if(RadioGroup1.ItemIndex=5)or(RadioGroup1.ItemIndex=6)Then begin
    if RadioGroup1.ItemIndex=5 Then begin St0:='X'; St3:='Z'; end;
    if RadioGroup1.ItemIndex=6 Then begin St0:='Z'; St3:='X'; end;

    RadioGroup2.ItemIndex:=0;

    Sqlen := 'UPDATE S1_Ssub SET Scode=''@Ycode'',Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=1;

    Sqlen := 'UPDATE H1_Ssub SET Scode=''@Ycode'',Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=2;

    Sqlen := 'UPDATE Sv_Gsum SET Scode=''@Ycode'',Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    RadioGroup2.ItemIndex:=4;

    Sqlen := 'UPDATE Sv_Chng SET Scode=''@Ycode'',Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Gs_Gsum SET Scode=''@Ycode'',Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE Sg_Gsum SET Scode=''@Ycode'',Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

    Sqlen := 'UPDATE In_Gsum SET Scode=''@Ycode'',Gcode=''@Zcode'' '+
             'WHERE Scode=''@Scode'' and Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Scode', St0);
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Ycode', St3);
    Translate(Sqlen, '@Zcode', St2);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  end;
  if RadioGroup1.ItemIndex=5 Then begin

    Sqlen := 'DELETE FROM G6_Ggeo WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    Sqlen := 'Select '+
    'Gubun,Jubun,Gcode,Ocode,Gname,Gposa,Gnumb,Guper,Gjomo,'+
    'Gtel1,Gtel2,Gfax1,Gfax2,Gpost,Gadd1,Gadd2,Gpper,Gbigo,'+
    'Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Grat7,Grat8,Grat9,Gqut1 '+
    'From G1_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Hcode', Edit107.Text);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then begin
       Base10.Socket.MakeGrid(SGrid);

      Sqlon := 'INSERT INTO G5_Ggeo '+
      '( Gubun, Jubun, Gcode, Ocode, Gname, Gposa, '+
      '  Gnumb, Guper, Gjomo, Gtel1, Gtel2, Gfax1, '+
      '  Gfax2, Gpost, Gadd1, Gadd2, Gpper, Gbigo, '+
      '  Grat1, Grat2, Grat3, Grat4, Grat5, Grat6, '+
      '  Grat7, Grat8, Grat9, Gqut1, Hcode ) VALUES ';
      Sqlen :=
      '(''@Gubun'',''@Jubun'',''@Gcode'',''@Ocode'',''@Gname'',''@Gposa'', '+
      ' ''@Gnumb'',''@Guper'',''@Gjomo'',''@Gtel1'',''@Gtel2'',''@Gfax1'', '+
      ' ''@Gfax2'',''@Gpost'',''@Gadd1'',''@Gadd2'',''@Gpper'',''@Gbigo'', '+
      '   @Grat1  ,  @Grat2  ,  @Grat3  ,  @Grat4  ,  @Grat5  ,  @Grat6  , '+
      '   @Grat7  ,  @Grat8  ,  @Grat9  ,  @Gqut1  ,''@Hcode'')';

      Translate(Sqlen, '@Gubun', SGrid.Cells[ 0,1]);
      Translate(Sqlen, '@Jubun', SGrid.Cells[ 1,1]);
      Translate(Sqlen, '@Gcode', St2);
      Translate(Sqlen, '@Ocode', SGrid.Cells[ 3,1]);
      Translate(Sqlen, '@Gname', SGrid.Cells[ 4,1]);
      Translate(Sqlen, '@Gposa', SGrid.Cells[ 5,1]);
      Translate(Sqlen, '@Gnumb', SGrid.Cells[ 6,1]);
      Translate(Sqlen, '@Guper', SGrid.Cells[ 7,1]);
      Translate(Sqlen, '@Gjomo', SGrid.Cells[ 8,1]);
      Translate(Sqlen, '@Gtel1', SGrid.Cells[ 9,1]);
      Translate(Sqlen, '@Gtel2', SGrid.Cells[10,1]);
      Translate(Sqlen, '@Gfax1', SGrid.Cells[11,1]);
      Translate(Sqlen, '@Gfax2', SGrid.Cells[12,1]);
      Translate(Sqlen, '@Gpost', SGrid.Cells[13,1]);
      Translate(Sqlen, '@Gadd1', SGrid.Cells[14,1]);
      Translate(Sqlen, '@Gadd2', SGrid.Cells[15,1]);
      Translate(Sqlen, '@Gpper', SGrid.Cells[16,1]);
      Translate(Sqlen, '@Gbigo', SGrid.Cells[17,1]);
      TransAuto(Sqlen, '@Grat1', SGrid.Cells[18,1]);
      TransAuto(Sqlen, '@Grat2', SGrid.Cells[19,1]);
      TransAuto(Sqlen, '@Grat3', SGrid.Cells[20,1]);
      TransAuto(Sqlen, '@Grat4', SGrid.Cells[21,1]);
      TransAuto(Sqlen, '@Grat5', SGrid.Cells[22,1]);
      TransAuto(Sqlen, '@Grat6', SGrid.Cells[23,1]);
      TransAuto(Sqlen, '@Grat7', SGrid.Cells[24,1]);
      TransAuto(Sqlen, '@Grat8', SGrid.Cells[25,1]);
      TransAuto(Sqlen, '@Grat9', SGrid.Cells[26,1]);
      TransAuto(Sqlen, '@Gqut1', SGrid.Cells[27,1]);
      Translate(Sqlen, '@Hcode', Edit107.Text);

      Sqlen:=Sqlon+Sqlen;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end
    else ShowMessage(E_Open);

    Sqlen := 'DELETE FROM G1_Ggeo WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

  end;
  if RadioGroup1.ItemIndex=6 Then begin

    Sqlen := 'Select '+
    'Gubun,Jubun,Gcode,Ocode,Gname,Gposa,Gnumb,Guper,Gjomo,'+
    'Gtel1,Gtel2,Gfax1,Gfax2,Gpost,Gadd1,Gadd2,Gpper,Gbigo,'+
    'Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Grat7,Grat8,Grat9,Gqut1 '+
    'From G5_Ggeo Where Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Hcode', Edit107.Text);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then begin
       Base10.Socket.MakeGrid(SGrid);

      Sqlon := 'INSERT INTO G1_Ggeo '+
      '( Gubun, Jubun, Gcode, Ocode, Gname, Gposa, '+
      '  Gnumb, Guper, Gjomo, Gtel1, Gtel2, Gfax1, '+
      '  Gfax2, Gpost, Gadd1, Gadd2, Gpper, Gbigo, '+
      '  Grat1, Grat2, Grat3, Grat4, Grat5, Grat6, '+
      '  Grat7, Grat8, Grat9, Gqut1, Hcode ) VALUES ';
      Sqlen :=
      '(''@Gubun'',''@Jubun'',''@Gcode'',''@Ocode'',''@Gname'',''@Gposa'', '+
      ' ''@Gnumb'',''@Guper'',''@Gjomo'',''@Gtel1'',''@Gtel2'',''@Gfax1'', '+
      ' ''@Gfax2'',''@Gpost'',''@Gadd1'',''@Gadd2'',''@Gpper'',''@Gbigo'', '+
      '   @Grat1  ,  @Grat2  ,  @Grat3  ,  @Grat4  ,  @Grat5  ,  @Grat6  , '+
      '   @Grat7  ,  @Grat8  ,  @Grat9  ,  @Gqut1  ,''@Hcode'')';

      Translate(Sqlen, '@Gubun', SGrid.Cells[ 0,1]);
      Translate(Sqlen, '@Jubun', SGrid.Cells[ 1,1]);
      Translate(Sqlen, '@Gcode', St2);
      Translate(Sqlen, '@Ocode', SGrid.Cells[ 3,1]);
      Translate(Sqlen, '@Gname', SGrid.Cells[ 4,1]);
      Translate(Sqlen, '@Gposa', SGrid.Cells[ 5,1]);
      Translate(Sqlen, '@Gnumb', SGrid.Cells[ 6,1]);
      Translate(Sqlen, '@Guper', SGrid.Cells[ 7,1]);
      Translate(Sqlen, '@Gjomo', SGrid.Cells[ 8,1]);
      Translate(Sqlen, '@Gtel1', SGrid.Cells[ 9,1]);
      Translate(Sqlen, '@Gtel2', SGrid.Cells[10,1]);
      Translate(Sqlen, '@Gfax1', SGrid.Cells[11,1]);
      Translate(Sqlen, '@Gfax2', SGrid.Cells[12,1]);
      Translate(Sqlen, '@Gpost', SGrid.Cells[13,1]);
      Translate(Sqlen, '@Gadd1', SGrid.Cells[14,1]);
      Translate(Sqlen, '@Gadd2', SGrid.Cells[15,1]);
      Translate(Sqlen, '@Gpper', SGrid.Cells[16,1]);
      Translate(Sqlen, '@Gbigo', SGrid.Cells[17,1]);
      TransAuto(Sqlen, '@Grat1', SGrid.Cells[18,1]);
      TransAuto(Sqlen, '@Grat2', SGrid.Cells[19,1]);
      TransAuto(Sqlen, '@Grat3', SGrid.Cells[20,1]);
      TransAuto(Sqlen, '@Grat4', SGrid.Cells[21,1]);
      TransAuto(Sqlen, '@Grat5', SGrid.Cells[22,1]);
      TransAuto(Sqlen, '@Grat6', SGrid.Cells[23,1]);
      TransAuto(Sqlen, '@Grat7', SGrid.Cells[24,1]);
      TransAuto(Sqlen, '@Grat8', SGrid.Cells[25,1]);
      TransAuto(Sqlen, '@Grat9', SGrid.Cells[26,1]);
      TransAuto(Sqlen, '@Gqut1', SGrid.Cells[27,1]);
      Translate(Sqlen, '@Hcode', Edit107.Text);

      Sqlen:=Sqlon+Sqlen;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

    end
    else ShowMessage(E_Open);

    Sqlen := 'DELETE FROM G5_Ggeo WHERE Gcode=''@Gcode'' and Hcode=''@Hcode'' ';
    Translate(Sqlen, '@Gcode', St1);
    Translate(Sqlen, '@Hcode', Edit107.Text);
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

  end;

  Edit101.Text:='';
  Edit102.Text:='';
  Gauge1.Progress:=0;
  RadioGroup1.ItemIndex:=-1;
  RadioGroup2.ItemIndex:=-1;
  Button101.Enabled:=False;
  Screen.Cursor:=crDefault;
  ShowMessage('완료');
end;

procedure TSobo51.Edit114KeyPress(Sender: TObject; var Key: Char);
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
  if RadioGroup1.ItemIndex=0 Then begin
    if(Edit101.Focused=True)Then begin
      Seek10.Edit1.Text:=Edit101.Text;
      Seek10.FilterTing(Edit101.Text,Edit107.Text);
      if Seek10.Query1.RecordCount=1 Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek10.Query1Gcode.AsString;
      end else
      if Seek10.ShowModal=mrOK Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek10.Query1Gcode.AsString;
      end;
    end else
    if(Edit102.Focused=True)Then begin
      Seek10.Edit1.Text:=Edit102.Text;
      Seek10.FilterTing(Edit102.Text,Edit107.Text);
      if Seek10.Query1.RecordCount=1 Then begin
        Edit102.Text:=Seek10.Query1Gcode.AsString;
      { Button101Click(Self); }
      end else
      if Seek10.ShowModal=mrOK Then begin
        Edit102.Text:=Seek10.Query1Gcode.AsString;
      { Button101Click(Self); }
      end;
    end;
  end;
  if RadioGroup1.ItemIndex=1 Then begin
    if(Edit101.Focused=True)Then begin
      Seek20.Edit1.Text:=Edit101.Text;
      Seek20.FilterTing(Edit101.Text,Edit107.Text);
      if Seek20.Query1.RecordCount=1 Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek20.Query1Gcode.AsString;
      end else
      if Seek20.ShowModal=mrOK Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek20.Query1Gcode.AsString;
      end;
    end else
    if(Edit102.Focused=True)Then begin
      Seek20.Edit1.Text:=Edit102.Text;
      Seek20.FilterTing(Edit102.Text,Edit107.Text);
      if Seek20.Query1.RecordCount=1 Then begin
        Edit102.Text:=Seek20.Query1Gcode.AsString;
      { Button101Click(Self); }
      end else
      if Seek20.ShowModal=mrOK Then begin
        Edit102.Text:=Seek20.Query1Gcode.AsString;
      { Button101Click(Self); }
      end;
    end;
  end;
  if RadioGroup1.ItemIndex=2 Then begin
    if(Edit101.Focused=True)Then begin
      Seek50.Edit1.Text:=Edit101.Text;
      Seek50.FilterTing(Edit101.Text,Edit107.Text);
      if Seek50.Query1.RecordCount=1 Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek50.Query1Gcode.AsString;
      end else
      if Seek50.ShowModal=mrOK Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek50.Query1Gcode.AsString;
      end;
    end else
    if(Edit102.Focused=True)Then begin
      Seek50.Edit1.Text:=Edit102.Text;
      Seek50.FilterTing(Edit102.Text,Edit107.Text);
      if Seek50.Query1.RecordCount=1 Then begin
        Edit102.Text:=Seek50.Query1Gcode.AsString;
      { Button101Click(Self); }
      end else
      if Seek50.ShowModal=mrOK Then begin
        Edit102.Text:=Seek50.Query1Gcode.AsString;
      { Button101Click(Self); }
      end;
    end;
  end;
  if RadioGroup1.ItemIndex=3 Then begin
    if(Edit101.Focused=True)Then begin
      Seek30.Edit1.Text:=Edit101.Text;
      Seek30.FilterTing(Edit101.Text,Edit107.Text);
      if Seek30.Query1.RecordCount=1 Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek30.Query1Gcode.AsString;
      end else
      if Seek30.ShowModal=mrOK Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek30.Query1Gcode.AsString;
      end;
    end else
    if(Edit102.Focused=True)Then begin
      Seek30.Edit1.Text:=Edit102.Text;
      Seek30.FilterTing(Edit102.Text,Edit107.Text);
      if Seek30.Query1.RecordCount=1 Then begin
        Edit102.Text:=Seek30.Query1Gcode.AsString;
      { Button101Click(Self); }
      end else
      if Seek30.ShowModal=mrOK Then begin
        Edit102.Text:=Seek30.Query1Gcode.AsString;
      { Button101Click(Self); }
      end;
    end;
  end;
  if RadioGroup1.ItemIndex=4 Then begin
    if(Edit101.Focused=True)Then begin
      Seek40.Edit1.Text:=Edit101.Text;
      Seek40.FilterTing(Edit101.Text,Edit107.Text);
      if Seek40.Query1.RecordCount=1 Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek40.Query1Gcode.AsString;
      end else
      if Seek40.ShowModal=mrOK Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek40.Query1Gcode.AsString;
      end;
    end else
    if(Edit102.Focused=True)Then begin
      Seek40.Edit1.Text:=Edit102.Text;
      Seek40.FilterTing(Edit102.Text,Edit107.Text);
      if Seek40.Query1.RecordCount=1 Then begin
        Edit102.Text:=Seek40.Query1Gcode.AsString;
      { Button101Click(Self); }
      end else
      if Seek40.ShowModal=mrOK Then begin
        Edit102.Text:=Seek40.Query1Gcode.AsString;
      { Button101Click(Self); }
      end;
    end;
  end;
  if RadioGroup1.ItemIndex=5 Then begin
    if(Edit101.Focused=True)Then begin
      Seek10.Edit1.Text:=Edit101.Text;
      Seek10.FilterTing(Edit101.Text,Edit107.Text);
      if Seek10.Query1.RecordCount=1 Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek10.Query1Gcode.AsString;
      end else
      if Seek10.ShowModal=mrOK Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek10.Query1Gcode.AsString;
      end;
    end else
    if(Edit102.Focused=True)Then begin
      Seek10.Edit1.Text:=Edit102.Text;
      Seek10.FilterTing(Edit102.Text,Edit107.Text);
      if Seek10.Query1.RecordCount=1 Then begin
        Edit102.Text:=Seek10.Query1Gcode.AsString;
      { Button101Click(Self); }
      end else
      if Seek10.ShowModal=mrOK Then begin
        Edit102.Text:=Seek10.Query1Gcode.AsString;
      { Button101Click(Self); }
      end;
    end;
  end;
  if RadioGroup1.ItemIndex=6 Then begin
    if(Edit101.Focused=True)Then begin
      Seek50.Edit1.Text:=Edit101.Text;
      Seek50.FilterTing(Edit101.Text,Edit107.Text);
      if Seek50.Query1.RecordCount=1 Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek50.Query1Gcode.AsString;
      end else
      if Seek50.ShowModal=mrOK Then begin
        SelectNext(ActiveControl as TWinControl, True, True);
        Edit101.Text:=Seek50.Query1Gcode.AsString;
      end;
    end else
    if(Edit102.Focused=True)Then begin
      Seek50.Edit1.Text:=Edit102.Text;
      Seek50.FilterTing(Edit102.Text,Edit107.Text);
      if Seek50.Query1.RecordCount=1 Then begin
        Edit102.Text:=Seek50.Query1Gcode.AsString;
      { Button101Click(Self); }
      end else
      if Seek50.ShowModal=mrOK Then begin
        Edit102.Text:=Seek50.Query1Gcode.AsString;
      { Button101Click(Self); }
      end;
    end;
  end;
  end;
end;

end.
