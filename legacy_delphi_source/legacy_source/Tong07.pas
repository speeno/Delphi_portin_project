unit Tong07;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, IniFiles;

type
  TTong70 = class(TFrame)
    Panel100: TFlatPanel;
    Panel101: TFlatPanel;
    Panel102: TFlatPanel;
    Edit101: TFlatEdit;
    Edit102: TFlatNumber;
    RadioButton1: TRadioButton;
    RadioButton2: TRadioButton;
    Button101: TFlatButton;
    Button102: TFlatButton;
    Button103: TFlatButton;
    Button105: TFlatButton;
    procedure FormShow(Sender: TObject);
    procedure Edit101KeyPress(Sender: TObject; var Key: Char);
    procedure Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Button100Click(Sender: TObject);
    procedure Button101Click(Sender: TObject);
    procedure Button102Click(Sender: TObject);
    procedure Button103Click(Sender: TObject);
    procedure Button104Click(nBarcode: String);
    procedure Button105Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  nLen1,nLen2: Integer;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong08, TcpLib, Subu21, Subu22, Subu23, Subu23_1;

procedure TTong70.FormShow(Sender: TObject);
var SetupIni : TIniFile;
    nCode : String;
begin
  SetupIni := TIniFile.Create(GetExecPath + 'Config.Ini');
  With SetupIni do begin
    nCode:=ReadString('Cport', 'nCode', '');
    nLen1:=ReadInteger('Cport','nLen1', 0 );
    nLen2:=ReadInteger('Cport','nLen2', 0 );
  end;
  SetupIni.Free;
  if nCode='1' then RadioButton1.Checked:=True;
  if nCode='2' then RadioButton2.Checked:=True;

  if nCode='2' then
  Tong80.ComPort.Connected:=True;
end;

procedure TTong70.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
  if nSqry.Active=True Then
    if Key=#13 Then
    Button100Click(Self);
end;

procedure TTong70.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TTong70.Button100Click(Sender: TObject);
begin
  Sqlen := 'Select Gcode,Gname,Gjeja,Ocode,Gdang From G4_Book '+
           'Where '+D_Select+'Gisbn=''@Gisbn'' and Hcode=''@Hcode''';
  Translate(Sqlen, '@Gisbn', Edit101.Text);
  if nForm='21' Then
  Translate(Sqlen, '@Hcode', Sobo21.Edit107.Text);
  if nForm='22' Then
  Translate(Sqlen, '@Hcode', Sobo22.Edit107.Text);
  if nForm='23' Then
  Translate(Sqlen, '@Hcode', Sobo23.Edit107.Text);
  if nForm='23_1' Then
  Translate(Sqlen, '@Hcode', tSqry.FieldByName('Hcode').AsString);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;

    if(nSqry.State=dsInsert)Then
    nSqry.Edit else
    nSqry.Append;

    nSqry.FieldByName('Bcode').Value:=Base10.Socket.GetData(1, 1);
    nSqry.FieldByName('Bname').Value:=Base10.Socket.GetData(1, 2);
    nSqry.FieldByName('Gjeja').Value:=Base10.Socket.GetData(1, 3);
    nSqry.FieldByName('Ocode').Value:='B';
    nSqry.FieldByName('Gdang').Value:=StrToIntDef(Base10.Socket.GetData(1, 5),0);
    Tong20.PrinJing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,nSqry.FieldByName('Hcode').Value,0);
  end
  else
  Exit;

  if nSqry.FieldByName('Ocode').AsString='' Then
     nSqry.FieldByName('Ocode').AsString:='B';

  if nSqry.FieldByName('Pubun').Value ='' then
  if nSqry.FieldByName('Gubun').Value ='반품' Then
     nSqry.FieldByName('Pubun').Value:='반품' else
     nSqry.FieldByName('Pubun').Value:='위탁';

  if Edit102.Value=0 then
  nSqry.FieldByName('Gsqut').Value:=1 else
  nSqry.FieldByName('Gsqut').Value:=Edit102.Value;

  if nForm='21' Then begin
    nSqry.FieldByName('Gcode').AsString:=Sobo21.Edit104.Text;
    nSqry.FieldByName('Gname').AsString:=Sobo21.Edit105.Text;

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
      Tong20.PrinYing(Self);
    end else begin
    //--//
    Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
             'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
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
  end;

  if nForm='22' Then begin
    nSqry.FieldByName('Gcode').AsString:=Sobo22.Edit104.Text;
    nSqry.FieldByName('Gname').AsString:=Sobo22.Edit105.Text;

    Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G2_Ggwo '+
             'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
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
    Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G2_Ggwo '+
             'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
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
  end;

  if nForm='23' Then begin
    nSqry.FieldByName('Gcode').AsString:=Sobo23.Edit104.Text;
    nSqry.FieldByName('Gname').AsString:=Sobo23.Edit105.Text;

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
      Tong20.PrinYing(Self);
    end else begin
    //--//
    Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
             'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
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
  end;

  if nForm='23_1' Then begin
  //nSqry.FieldByName('Gcode').AsString:=Sobo23.Edit104.Text;
  //nSqry.FieldByName('Gname').AsString:=Sobo23.Edit105.Text;

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
      Tong20.PrinYing(Self);
    end else begin
    //--//
    Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo '+
             'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
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
  end;

  Sqlen := 'Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G4_Book '+
           'Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
  Translate(Sqlen, '@Gcode', nSqry.FieldByName('Bcode').AsString);
  Translate(Sqlen, '@Hcode', nSqry.FieldByName('Hcode').AsString);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    Tong20.PrinZing(Self);
    if Grat1<>0 Then nSqry.FieldByName('Grat1').Value:=Grat1;
  end;

  Tong20.PrinRat1(nSqry.FieldByName('Hcode').AsString,nSqry.FieldByName('Gcode').AsString,nSqry.FieldByName('Bcode').AsString);

  if nForm='21' Then begin
    Sqlen := 'Select Grat1,Gssum From G6_Ggeo '+
             'Where '+D_Select+'Gcode=''@Gcode'' and Bcode=''@Bcode'' and Hcode=''@Hcode''';
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
  end;

  Tong20.PrinYing(Self);

  Tong20.PrinSing(nSqry.FieldByName('Ocode').Value,nSqry.FieldByName('Bcode').Value,nSqry.FieldByName('Hcode').Value,nSqry.FieldByName('Gsqut').Value);

  nSqry.Append;

  if nForm='21' Then
  Sobo21.DBGrid101.SelectedIndex:=0;

  if nForm='22' Then
  Sobo22.DBGrid101.SelectedIndex:=0;

  if nForm='23' Then
  Sobo23.DBGrid101.SelectedIndex:=0;

  if nForm='23_1' Then
  Sobo23_1.DBGrid101.SelectedIndex:=0;

  Edit101.Text:='';
end;

procedure TTong70.Button101Click(Sender: TObject);
begin
  if nForm='21' Then begin
    if Sobo21.Panel401.Width=410 then
    Sobo21.Panel401.Width := 305 else
    Sobo21.Panel401.Width := 410;
  end;
  if nForm='22' Then begin
    if Sobo22.Panel401.Width=410 then
    Sobo22.Panel401.Width := 305 else
    Sobo22.Panel401.Width := 410;
  end;
  if nForm='23' Then begin
    if Sobo23.Panel401.Width=410 then
    Sobo23.Panel401.Width := 305 else
    Sobo23.Panel401.Width := 410;
  end;
end;

procedure TTong70.Button102Click(Sender: TObject);
begin
  Tong80.ComPort.ShowSetupDialog;
end;

procedure TTong70.Button103Click(Sender: TObject);
begin
  Tong80.ComTerminal.ShowSetupDialog;
end;

procedure TTong70.Button104Click(nBarcode: String);
begin
  if nForm='21' Then begin
    Edit101.Text:=Copy(nBarcode,nLen1,nLen1);
    Button100Click(Self);
  end;
end;

procedure TTong70.Button105Click(Sender: TObject);
begin
  if nForm='21' Then begin
    Sobo21.DBGrid101.SetFocus;
    Sobo21.Panel401.Visible:=False;
  end;
  if nForm='22' Then begin
    Sobo22.DBGrid101.SetFocus;
    Sobo22.Panel401.Visible:=False;
  end;
  if nForm='23' Then begin
    Sobo23.DBGrid101.SetFocus;
    Sobo23.Panel401.Visible:=False;
  end;
end;

end.
