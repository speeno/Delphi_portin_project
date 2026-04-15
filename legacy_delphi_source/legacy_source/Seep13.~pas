unit Seep13;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Qrctrls, Printers, ExtCtrls, StdCtrls, Mylabel, Db, TFlatPanelUnit,
  TFlatEditUnit, TFlatButtonUnit, TFlatComboBoxUnit, TFlatGroupBoxUnit,
  TFlatSpinEditUnit, TFlatSpeedButtonUnit,
  FR_DSet, FR_DBSet, FR_Class;

type
  TSeen13 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    FontDialog1: TFontDialog;
    ColorDialog1: TColorDialog;
    PrinterSetupDialog1: TPrinterSetupDialog;
    FlatPanel1: TFlatPanel;
    ComboBox00: TFlatComboBox;
    Button1: TFlatButton;
    Button2: TFlatButton;
    Button3: TFlatButton;
    Button4: TFlatButton;
    Button5: TFlatButton;
    GroupBox1: TFlatGroupBox;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    Label103: TmyLabel3d;
    Label104: TmyLabel3d;
    Label105: TmyLabel3d;
    Label106: TmyLabel3d;
    Label107: TmyLabel3d;
    Label108: TmyLabel3d;
    Label109: TmyLabel3d;
    Label110: TmyLabel3d;
    Label111: TmyLabel3d;
    Label114: TmyLabel3d;
    Label112: TmyLabel3d;
    Label113: TmyLabel3d;
    SpeedButton1: TFlatSpeedButton;
    SpeedButton2: TFlatSpeedButton;
    SpeedButton3: TFlatSpeedButton;
    SpeedButton4: TFlatSpeedButton;
    SpeedButton5: TFlatSpeedButton;
    Edit21: TFlatEdit;
    Edit22: TFlatEdit;
    Edit23: TFlatEdit;
    Edit24: TFlatEdit;
    Edit25: TFlatEdit;
    SpinEdit21: TFlatSpinEditInteger;
    SpinEdit22: TFlatSpinEditInteger;
    SpinEdit23: TFlatSpinEditInteger;
    SpinEdit25: TFlatSpinEditInteger;
    SpinEdit27: TFlatSpinEditInteger;
    SpinEdit29: TFlatSpinEditInteger;
    SpinEdit72: TFlatSpinEditInteger;
    SpinEdit24: TFlatSpinEditInteger;
    SpinEdit26: TFlatSpinEditInteger;
    SpinEdit28: TFlatSpinEditInteger;
    SpinEdit71: TFlatSpinEditInteger;
    SpinEdit73: TFlatSpinEditInteger;
    SpinEdit74: TFlatSpinEditInteger;
    SpinEdit75: TFlatSpinEditInteger;
    SpinEdit76: TFlatSpinEditInteger;
    SpinEdit77: TFlatSpinEditInteger;
    SpinEdit31: TFlatSpinEditInteger;
    SpinEdit32: TFlatSpinEditInteger;
    SpinEdit33: TFlatSpinEditInteger;
    Edit29: TFlatEdit;
    Edit28: TFlatEdit;
    GroupBox2: TFlatGroupBox;
    Label201: TmyLabel3d;
    Label202: TmyLabel3d;
    SpinEdit1: TFlatSpinEditInteger;
    SpinEdit2: TFlatSpinEditInteger;
    GroupBox3: TFlatGroupBox;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label303: TmyLabel3d;
    Label304: TmyLabel3d;
    Label305: TmyLabel3d;
    Label306: TmyLabel3d;
    Label307: TmyLabel3d;
    ComboBox1: TFlatComboBox;
    SpinEdit61: TFlatSpinEditInteger;
    SpinEdit62: TFlatSpinEditInteger;
    SpinEdit63: TFlatSpinEditInteger;
    SpinEdit64: TFlatSpinEditInteger;
    SpinEdit5: TFlatSpinEditInteger;
    SpinEdit6: TFlatSpinEditInteger;
    RadioButton1: TRadioButton;
    RadioButton2: TRadioButton;
    RadioButton3: TRadioButton;
    procedure SetTing(Str:String);
    procedure PrinTing01(Str:String);
    procedure PrinDing01(Str:String);
    procedure PrinDing02(Str:String);
    procedure PrinDing03(Str:String);
    procedure ComboBox00Change(Sender: TObject);
    procedure SpeedButton1Click(Sender: TObject);
    procedure SpeedButton2Click(Sender: TObject);
    procedure SpeedButton3Click(Sender: TObject);
    procedure SpeedButton4Click(Sender: TObject);
    procedure SpeedButton5Click(Sender: TObject);
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure Button4Click(Sender: TObject);
    procedure Button5Click(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure ComboBox1Change(Sender: TObject);
    procedure frDBDataSet00_01Next(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seen13: TSeen13;
  STPrint00: String;

implementation

{$R *.DFM}

uses Base01, Tong04, Tong06, TcpLib;

procedure TSeen13.FormShow(Sender: TObject);
begin
//Application.CreateForm(TSeen14, Seen14);
  ComboBox00Change(Self);
end;

procedure TSeen13.FormClose(Sender: TObject; var Action: TCloseAction);
begin
//Seen14.Free;
end;

procedure TSeen13.ComboBox00Change(Sender: TObject);
begin
  SpinEdit2.Value:=oSqry.RecordCount;
  if ComboBox00.ItemIndex=0 then begin
    SpinEdit32.Enabled:=False;
    SpinEdit33.Enabled:=False;
  //Seen14.QuickRep1.Page.Columns:=1;
    STPrint00:='1'; SetTing(STPrint00); end
  else if ComboBox00.ItemIndex=1 then begin
    SpinEdit32.Enabled:=False;
    SpinEdit33.Enabled:=False;
  //Seen14.QuickRep1.Page.Columns:=1;
    STPrint00:='2'; SetTing(STPrint00); end
  else if ComboBox00.ItemIndex=2 then begin
    SpinEdit32.Enabled:=False;
    SpinEdit33.Enabled:=False;
  //Seen14.QuickRep1.Page.Columns:=1;
    STPrint00:='3'; SetTing(STPrint00); end
  else if ComboBox00.ItemIndex=3 then begin
    SpinEdit32.Enabled:=True;
    SpinEdit33.Enabled:=True;
  //Seen14.QuickRep1.Page.Columns:=2;
    STPrint00:='4'; SetTing(STPrint00); end
  else if ComboBox00.ItemIndex=4 then begin
    SpinEdit32.Enabled:=True;
    SpinEdit33.Enabled:=True;
  //Seen14.QuickRep1.Page.Columns:=2;
    STPrint00:='5'; SetTing(STPrint00); end
  else begin
    SpinEdit32.Enabled:=False;
    SpinEdit33.Enabled:=False;
  //Seen14.QuickRep1.Page.Columns:=1;
    STPrint00:='1'; SetTing(STPrint00);
    Seen13.ComboBox00.ItemIndex:=0;  end;
end;

procedure TSeen13.ComboBox1Change(Sender: TObject);
begin
  if ComboBox1.ItemIndex=0 Then begin
    SpinEdit61.Text:='2100';
    SpinEdit62.Text:='2970';
  end;
  if ComboBox1.ItemIndex=1 Then begin
    SpinEdit61.Text:='2159';
    SpinEdit62.Text:='2794';
  end;
end;

procedure TSeen13.SetTing(Str:String);
begin
  SpinEdit1.Value:=1;
  SpinEdit2.Value:=oSqry.RecordCount;

  Tong40._Gg_Magn_(Str);

  SpinEdit21.Value:=lSqry.FieldByName('Top').AsInteger;
  SpinEdit22.Value:=lSqry.FieldByName('L11').AsInteger;
  SpinEdit23.Value:=lSqry.FieldByName('L19').AsInteger;
  SpinEdit24.Value:=lSqry.FieldByName('L21').AsInteger;
  SpinEdit25.Value:=lSqry.FieldByName('L29').AsInteger;
  SpinEdit26.Value:=lSqry.FieldByName('L31').AsInteger;
  SpinEdit27.Value:=lSqry.FieldByName('L39').AsInteger;
  SpinEdit28.Value:=lSqry.FieldByName('L41').AsInteger;
  SpinEdit29.Value:=lSqry.FieldByName('L49').AsInteger;
{ SpinEdit30.Value:=lSqry.FieldByName('L51').AsInteger; }
  SpinEdit31.Value:=lSqry.FieldByName('L59').AsInteger;
  SpinEdit32.Value:=lSqry.FieldByName('L58').AsInteger;
  SpinEdit33.Value:=lSqry.FieldByName('L57').AsInteger;
  SpinEdit61.Value:=lSqry.FieldByName('L61').AsInteger;
  SpinEdit62.Value:=lSqry.FieldByName('L62').AsInteger;
  SpinEdit63.Value:=lSqry.FieldByName('L63').AsInteger;
  SpinEdit64.Value:=lSqry.FieldByName('L64').AsInteger;
  ComboBox1.Text  :=lSqry.FieldByName('F61').AsString;
  if lSqry.FieldByName('F61').AsString='A4'     Then ComboBox1.ItemIndex:=0;
  if lSqry.FieldByName('F61').AsString='80Col'  Then ComboBox1.ItemIndex:=1;
  if lSqry.FieldByName('F61').AsString='Custom' Then ComboBox1.ItemIndex:=2;
  // Post
  SpinEdit71.Value:=lSqry.FieldByName('L71').AsInteger;
  SpinEdit72.Value:=lSqry.FieldByName('L72').AsInteger;
  SpinEdit73.Value:=lSqry.FieldByName('L73').AsInteger;
  SpinEdit74.Value:=lSqry.FieldByName('L74').AsInteger;
  SpinEdit75.Value:=lSqry.FieldByName('L75').AsInteger;
  SpinEdit76.Value:=lSqry.FieldByName('L76').AsInteger;
  SpinEdit77.Value:=lSqry.FieldByName('L77').AsInteger;
  // Color
{ Edit21.Font.color:=StringToColor(lSqry.FieldByName('F11').AsString);
  Edit22.Font.color:=StringToColor(lSqry.FieldByName('F21').AsString);
  Edit23.Font.color:=StringToColor(lSqry.FieldByName('F31').AsString);
  Edit24.Font.color:=StringToColor(lSqry.FieldByName('F41').AsString);
  Edit25.Font.color:=StringToColor(lSqry.FieldByName('F51').AsString); }
  // Font
  Edit21.Font.Name:=lSqry.FieldByName('F12').AsString;
  Edit22.Font.Name:=lSqry.FieldByName('F22').AsString;
  Edit23.Font.Name:=lSqry.FieldByName('F32').AsString;
  Edit24.Font.Name:=lSqry.FieldByName('F42').AsString;
  Edit25.Font.Name:=lSqry.FieldByName('F52').AsString;
  // Style
  case lSqry.FieldByName('L14').AsInteger of
    1:Edit21.Font.Style := [];
    2:Edit21.Font.Style := [fsItalic];
    3:Edit21.Font.Style := [fsBold];
    4:Edit21.Font.Style := [fsBold,fsItalic];
    5:Edit21.Font.Style := [fsUnderline];
    6:Edit21.Font.Style := [fsItalic,fsUnderline];
    7:Edit21.Font.Style := [fsBold,fsUnderline];
    8:Edit21.Font.Style := [fsBold,fsItalic,fsUnderline];
  end;
  case lSqry.FieldByName('L24').AsInteger of
    1:Edit22.Font.Style := [];
    2:Edit22.Font.Style := [fsItalic];
    3:Edit22.Font.Style := [fsBold];
    4:Edit22.Font.Style := [fsBold,fsItalic];
    5:Edit22.Font.Style := [fsUnderline];
    6:Edit22.Font.Style := [fsItalic,fsUnderline];
    7:Edit22.Font.Style := [fsBold,fsUnderline];
    8:Edit22.Font.Style := [fsBold,fsItalic,fsUnderline];
  end;
  case lSqry.FieldByName('L34').AsInteger of
    1:Edit23.Font.Style := [];
    2:Edit23.Font.Style := [fsItalic];
    3:Edit23.Font.Style := [fsBold];
    4:Edit23.Font.Style := [fsBold,fsItalic];
    5:Edit23.Font.Style := [fsUnderline];
    6:Edit23.Font.Style := [fsItalic,fsUnderline];
    7:Edit23.Font.Style := [fsBold,fsUnderline];
    8:Edit23.Font.Style := [fsBold,fsItalic,fsUnderline];
  end;
  case lSqry.FieldByName('L44').AsInteger of
    1:Edit24.font.Style := [];
    2:Edit24.font.Style := [fsItalic];
    3:Edit24.font.Style := [fsBold];
    4:Edit24.font.Style := [fsBold,fsItalic];
    5:Edit24.font.Style := [fsUnderline];
    6:Edit24.font.Style := [fsItalic,fsUnderline];
    7:Edit24.Font.Style := [fsBold,fsUnderline];
    8:Edit24.Font.Style := [fsBold,fsItalic,fsUnderline];
  end;
  case lSqry.FieldByName('L54').AsInteger of
    1:Edit25.font.Style := [];
    2:Edit25.font.Style := [fsItalic];
    3:Edit25.font.Style := [fsBold];
    4:Edit25.font.Style := [fsBold,fsItalic];
    5:Edit25.font.Style := [fsUnderline];
    6:Edit25.font.Style := [fsItalic,fsUnderline];
    7:Edit25.Font.Style := [fsBold,fsUnderline];
    8:Edit25.Font.Style := [fsBold,fsItalic,fsUnderline];
  end;
  // Size
  Edit21.Font.Size:=lSqry.FieldByName('L15').AsInteger;
  Edit22.Font.Size:=lSqry.FieldByName('L25').AsInteger;
  Edit23.Font.Size:=lSqry.FieldByName('L35').AsInteger;
  Edit24.Font.Size:=lSqry.FieldByName('L45').AsInteger;
  Edit25.Font.Size:=lSqry.FieldByName('L55').AsInteger;
  // Size
  Edit28.Text:=lSqry.FieldByName('Posa').AsString;
  Edit29.Text:=lSqry.FieldByName('Name').AsString;
end;

procedure TSeen13.SpeedButton1Click(Sender: TObject);
begin
  FontDialog1.Font := Edit21.Font;
  FontDialog1.Execute;
  Edit21.Font := FontDialog1.Font;
end;

procedure TSeen13.SpeedButton2Click(Sender: TObject);
begin
  FontDialog1.Font := Edit22.Font;
  FontDialog1.Execute;
  Edit22.Font := FontDialog1.Font;
end;

procedure TSeen13.SpeedButton3Click(Sender: TObject);
begin
  FontDialog1.Font := Edit23.Font;
  FontDialog1.Execute;
  Edit23.Font := FontDialog1.Font;
end;

procedure TSeen13.SpeedButton4Click(Sender: TObject);
begin
  FontDialog1.Font := Edit24.Font;
  FontDialog1.Execute;
  Edit24.Font := FontDialog1.Font;
end;

procedure TSeen13.SpeedButton5Click(Sender: TObject);
begin
  FontDialog1.Font := Edit25.Font;
  FontDialog1.Execute;
  Edit25.Font := FontDialog1.Font;
end;

procedure TSeen13.Button1Click(Sender: TObject);
var St1,St2,St3,St4,St5: Integer;
    St0: String;
begin
  // Style
  if Edit21.Font.Style = [] then
    St1 := 1
  else if Edit21.Font.Style = [fsItalic] then
    St1 := 2
  else if Edit21.Font.Style = [fsBold] then
    St1 := 3
  else if Edit21.Font.Style = [fsBold,fsItalic] then
    St1 := 4
  else if Edit21.Font.Style = [fsUnderline] then
    St1 := 5
  else if Edit21.Font.Style = [fsItalic,fsUnderline] then
    St1 := 6
  else if Edit21.Font.Style = [fsBold,fsUnderline] then
    St1 := 7
  else if Edit21.Font.Style = [fsBold,fsItalic,fsUnderline] then
    St1 := 8;

  if Edit22.Font.Style = [] then
    St2 := 1
  else if Edit22.Font.Style = [fsItalic] then
    St2 := 2
  else if Edit22.Font.Style = [fsBold] then
    St2 := 3
  else if Edit22.Font.Style = [fsBold,fsItalic] then
    St2 := 4
  else if Edit22.Font.Style = [fsUnderline] then
    St2 := 5
  else if Edit22.Font.Style = [fsItalic,fsUnderline] then
    St2 := 6
  else if Edit22.Font.Style = [fsBold,fsUnderline] then
    St2 := 7
  else if Edit22.Font.Style = [fsBold,fsItalic,fsUnderline] then
    St2 := 8;

  if Edit23.Font.Style = [] then
    St3 := 1
  else if Edit23.Font.Style = [fsItalic] then
    St3 := 2
  else if Edit23.Font.Style = [fsBold] then
    St3 := 3
  else if Edit23.Font.Style = [fsBold,fsItalic] then
    St3 := 4
  else if Edit23.Font.Style = [fsUnderline] then
    St3 := 5
  else if Edit23.Font.Style = [fsItalic,fsUnderline] then
    St3 := 6
  else if Edit23.Font.Style = [fsBold,fsUnderline] then
    St3 := 7
  else if Edit23.Font.Style = [fsBold,fsItalic,fsUnderline] then
    St3 := 8;

  if Edit24.Font.Style = [] then
    St4 := 1
  else if Edit24.Font.Style = [fsItalic] then
    St4 := 2
  else if Edit24.Font.Style = [fsBold] then
    St4 := 3
  else if Edit24.Font.Style = [fsBold,fsItalic] then
    St4 := 4
  else if Edit24.Font.Style = [fsUnderline] then
    St4 := 5
  else if Edit24.Font.Style = [fsItalic,fsUnderline] then
    St4 := 6
  else if Edit24.Font.Style = [fsBold,fsUnderline] then
    St4 := 7
  else if Edit24.Font.Style = [fsBold,fsItalic,fsUnderline] then
    St4 := 8;

  if Edit25.Font.Style = [] then
    St5 := 1
  else if Edit25.Font.Style = [fsItalic] then
    St5 := 2
  else if Edit25.Font.Style = [fsBold] then
    St5 := 3
  else if Edit25.Font.Style = [fsBold,fsItalic] then
    St5 := 4
  else if Edit25.Font.Style = [fsUnderline] then
    St5 := 5
  else if Edit25.Font.Style = [fsItalic,fsUnderline] then
    St5 := 6
  else if Edit25.Font.Style = [fsBold,fsUnderline] then
    St5 := 7
  else if Edit25.Font.Style = [fsBold,fsItalic,fsUnderline] then
    St5 := 8;

  if ComboBox1.ItemIndex=0 Then St0:='A4';
  if ComboBox1.ItemIndex=1 Then St0:='80Col';
  if ComboBox1.ItemIndex=2 Then St0:='Custom';

  {----}
  Sqlen := 'UPDATE Gg_Magn SET '+
  'F11=''@F11'',F12=''@F12'',F21=''@F21'',F22=''@F22'',F31=''@F31'',F32=''@F32'','+
  'F41=''@F41'',F42=''@F42'',F51=''@F51'',F52=''@F52'',F61=''@F61'',F62=''@F62'','+
  'F71=''@F71'',F72=''@F72'',Name=''@Name'',Posa=''@Posa'',Top=@Top '+
  'WHERE Gu=''@Gu''';

  Translate(Sqlen, '@Gu', STPrint00);

  Translate(Sqlen, '@F11', ColorToString(Edit21.Font.color));
  Translate(Sqlen, '@F12', Edit21.Font.Name);
  Translate(Sqlen, '@F21', ColorToString(Edit22.Font.color));
  Translate(Sqlen, '@F22', Edit22.Font.Name);
  Translate(Sqlen, '@F31', ColorToString(Edit23.Font.color));
  Translate(Sqlen, '@F32', Edit23.Font.Name);
  Translate(Sqlen, '@F41', ColorToString(Edit24.Font.color));
  Translate(Sqlen, '@F42', Edit24.Font.Name);
  Translate(Sqlen, '@F51', ColorToString(Edit25.Font.color));

  Translate(Sqlen, '@F52', Edit25.Font.Name);
  Translate(Sqlen, '@F61', St0);
  Translate(Sqlen, '@F62', '');
  Translate(Sqlen, '@F71', '');
  Translate(Sqlen, '@F72', '');
  Translate(Sqlen, '@Name', Edit28.Text);
  Translate(Sqlen, '@Posa', Edit29.Text);
  TransAuto(Sqlen, '@Top', FloatToStr(SpinEdit21.Value));

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  {----}
  Sqlen := 'UPDATE Gg_Magn SET '+
  'L11=@L11,L12=@L12,L13=@L13,L14=@L14,L15=@L15,L16=@L16,L17=@L17,L18=@L18,L19=@L19,'+
  'L21=@L21,L22=@L22,L23=@L23,L24=@L24,L25=@L25,L26=@L26,L27=@L27,L28=@L28,L29=@L29 '+
  'WHERE Gu=''@Gu''';

  Translate(Sqlen, '@Gu', STPrint00);

  TransAuto(Sqlen, '@L11', FloatToStr(SpinEdit22.Value));
  TransAuto(Sqlen, '@L12', '0');
  TransAuto(Sqlen, '@L13', '0');
  TransAuto(Sqlen, '@L14', FloatToStr(St1));
  TransAuto(Sqlen, '@L15', FloatToStr(Edit21.Font.Size));
  TransAuto(Sqlen, '@L16', '0');
  TransAuto(Sqlen, '@L17', '0');
  TransAuto(Sqlen, '@L18', '0');
  TransAuto(Sqlen, '@L19', FloatToStr(SpinEdit23.Value));

  TransAuto(Sqlen, '@L21', FloatToStr(SpinEdit24.Value));
  TransAuto(Sqlen, '@L22', '0');
  TransAuto(Sqlen, '@L23', '0');
  TransAuto(Sqlen, '@L24', FloatToStr(St2));
  TransAuto(Sqlen, '@L25', FloatToStr(Edit22.Font.Size));
  TransAuto(Sqlen, '@L26', '0');
  TransAuto(Sqlen, '@L27', '0');
  TransAuto(Sqlen, '@L28', '0');
  TransAuto(Sqlen, '@L29', FloatToStr(SpinEdit25.Value));

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  {----}
  Sqlen := 'UPDATE Gg_Magn SET '+
  'L31=@L31,L32=@L32,L33=@L33,L34=@L34,L35=@L35,L36=@L36,L37=@L37,L38=@L38,L39=@L39,'+
  'L41=@L41,L42=@L42,L43=@L43,L44=@L44,L45=@L45,L46=@L46,L47=@L47,L48=@L48,L49=@L49 '+
  'WHERE Gu=''@Gu''';

  Translate(Sqlen, '@Gu', STPrint00);

  TransAuto(Sqlen, '@L31', FloatToStr(SpinEdit26.Value));
  TransAuto(Sqlen, '@L32', '0');
  TransAuto(Sqlen, '@L33', '0');
  TransAuto(Sqlen, '@L34', FloatToStr(St3));
  TransAuto(Sqlen, '@L35', FloatToStr(Edit23.Font.Size));
  TransAuto(Sqlen, '@L36', '0');
  TransAuto(Sqlen, '@L37', '0');
  TransAuto(Sqlen, '@L38', '0');
  TransAuto(Sqlen, '@L39', FloatToStr(SpinEdit27.Value));

  TransAuto(Sqlen, '@L41', FloatToStr(SpinEdit28.Value));
  TransAuto(Sqlen, '@L42', '0');
  TransAuto(Sqlen, '@L43', '0');
  TransAuto(Sqlen, '@L44', FloatToStr(St4));
  TransAuto(Sqlen, '@L45', FloatToStr(Edit24.Font.Size));
  TransAuto(Sqlen, '@L46', '0');
  TransAuto(Sqlen, '@L47', '0');
  TransAuto(Sqlen, '@L48', '0');
  TransAuto(Sqlen, '@L49', FloatToStr(SpinEdit29.Value));

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  {----}
  Sqlen := 'UPDATE Gg_Magn SET '+
  'L51=@L51,L52=@L52,L53=@L53,L54=@L54,L55=@L55,L56=@L56,L57=@L57,L58=@L58,L59=@L59,'+
  'L61=@L61,L62=@L62,L63=@L63,L64=@L64,L65=@L65,L66=@L66,L67=@L67,L68=@L68,L69=@L69 '+
  'WHERE Gu=''@Gu''';

  Translate(Sqlen, '@Gu', STPrint00);

  TransAuto(Sqlen, '@L51', '0');
  TransAuto(Sqlen, '@L52', '0');
  TransAuto(Sqlen, '@L53', '0');
  TransAuto(Sqlen, '@L54', FloatToStr(St5));
  TransAuto(Sqlen, '@L55', FloatToStr(Edit25.Font.Size));
  TransAuto(Sqlen, '@L56', '0');
  TransAuto(Sqlen, '@L57', FloatToStr(SpinEdit33.Value));
  TransAuto(Sqlen, '@L58', FloatToStr(SpinEdit32.Value));
  TransAuto(Sqlen, '@L59', FloatToStr(SpinEdit31.Value));

  TransAuto(Sqlen, '@L61', FloatToStr(SpinEdit61.Value));
  TransAuto(Sqlen, '@L62', FloatToStr(SpinEdit62.Value));
  TransAuto(Sqlen, '@L63', FloatToStr(SpinEdit63.Value));
  TransAuto(Sqlen, '@L64', FloatToStr(SpinEdit64.Value));
  TransAuto(Sqlen, '@L65', '0');
  TransAuto(Sqlen, '@L66', '0');
  TransAuto(Sqlen, '@L67', '0');
  TransAuto(Sqlen, '@L68', '0');
  TransAuto(Sqlen, '@L69', '0');

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

  {----}
  Sqlen := 'UPDATE Gg_Magn SET '+
  'L71=@L71,L72=@L72,L73=@L73,L74=@L74,L75=@L75,L76=@L76,L77=@L77,L78=@L78,L79=@L79 '+
  'WHERE Gu=''@Gu''';

  Translate(Sqlen, '@Gu', STPrint00);

  TransAuto(Sqlen, '@L71', FloatToStr(SpinEdit71.Value));
  TransAuto(Sqlen, '@L72', FloatToStr(SpinEdit72.Value));
  TransAuto(Sqlen, '@L73', FloatToStr(SpinEdit73.Value));
  TransAuto(Sqlen, '@L74', FloatToStr(SpinEdit74.Value));
  TransAuto(Sqlen, '@L75', FloatToStr(SpinEdit75.Value));
  TransAuto(Sqlen, '@L76', FloatToStr(SpinEdit76.Value));
  TransAuto(Sqlen, '@L77', FloatToStr(SpinEdit77.Value));
  TransAuto(Sqlen, '@L78', '0');
  TransAuto(Sqlen, '@L79', '0');

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

end;

procedure TSeen13.Button2Click(Sender: TObject);
begin

  oSqry:=nSqry;
  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

  if ComboBox00.ItemIndex=0 then begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_21.frf');
  end;

  if ComboBox00.ItemIndex=1 then begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_22.frf');
  end;

  if ComboBox00.ItemIndex=2 then begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_23.frf');
  end;

  if ComboBox00.ItemIndex=3 then
  begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_24.frf');
  end;

  if ComboBox00.ItemIndex=4 then
  begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_25.frf');
  end;

  Tong60.frDBDataSet00_01.OnFirst:=frDBDataSet00_01Next;
  Tong60.frDBDataSet00_01.OnNext:=frDBDataSet00_01Next;
  Tong60.frDBDataSet00_01.DataSet:=oSqry;

  With Tong60.frReport00_01 do begin
    if PrepareReport then
    PrintPreparedReport(' ',1,true, frall);
  end;

  oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;

end;

procedure TSeen13.Button3Click(Sender: TObject);
begin

  oSqry:=nSqry;
  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

  if ComboBox00.ItemIndex=0 then begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_21.frf');
  end;

  if ComboBox00.ItemIndex=1 then begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_22.frf');
  end;

  if ComboBox00.ItemIndex=2 then begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_23.frf');
  end;

  if ComboBox00.ItemIndex=3 then begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_24.frf');
  end;

  if ComboBox00.ItemIndex=4 then begin
    Tong60.frReport00_01.Clear;
    Tong60.frReport00_01.LoadFromFile(GetExecPath + 'Report\Report_1_25.frf');
  end;

  Tong60.frDBDataSet00_01.OnFirst:=frDBDataSet00_01Next;
  Tong60.frDBDataSet00_01.OnNext:=frDBDataSet00_01Next;
  Tong60.frDBDataSet00_01.DataSet:=oSqry;

  With Tong60.frReport00_01 do begin
    ShowReport;
  end;

  oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;

end;

procedure TSeen13.Button4Click(Sender: TObject);
begin
  PrinterSetupDialog1.Execute;
end;

procedure TSeen13.Button5Click(Sender: TObject);
begin
  Close;
end;

procedure TSeen13.PrinTing01(Str:String);
var
  gpCol, gpRow, gpCnt, gpHeg, gpWth: Integer;
begin
{ Printer.Canvas.Font.Size:=10;
  gpWth:=Printer.Canvas.TextWidth('A');
  gpHeg:=Printer.Canvas.TextHeight('A');
  if SpinEdit64.Value=0 Then
  gpHeg:=gpHeg+(gpHeg div 6) else
  gpHeg:=SpinEdit64.Value;
  gpCol:=0; gpRow:=0; gpCnt:=0;
  // Line 1
  Inc(gpCnt,SpinEdit21.Value); gpRow:=gpHeg*gpCnt;
    gpCol:=gpWth*SpinEdit22.Value;
    Seen14.QRDBText1.Top :=gpRow;
    Seen14.QRDBText1.Left:=gpCol;
  // Line 2
  Inc(gpCnt,SpinEdit23.Value); gpRow:=gpHeg*gpCnt;
    gpCol:=gpWth*SpinEdit24.Value;
    Seen14.QRDBText2.Top :=gpRow;
    Seen14.QRDBText2.Left:=gpCol;
  // Line 3
  Inc(gpCnt,SpinEdit25.Value); gpRow:=gpHeg*gpCnt;
    gpCol:=gpWth*SpinEdit26.Value;
    Seen14.QRDBText3.Top :=gpRow;
    Seen14.QRDBText3.Left:=gpCol;
  // Line 4
  Inc(gpCnt,SpinEdit27.Value); gpRow:=gpHeg*gpCnt;
    gpCol:=gpWth*SpinEdit28.Value;
    Seen14.QRDBText4.Top :=gpRow;
    Seen14.QRDBText4.Left:=gpCol;
  // Line 5
  Inc(gpCnt,SpinEdit29.Value); gpRow:=gpHeg*gpCnt;
    gpCol:=gpWth*SpinEdit71.Value;
    Seen14.QRDBText5.Top :=gpRow;
    Seen14.QRDBText5.Left:=gpCol;
  // Line Bottom
  Inc(gpCnt,SpinEdit31.Value); gpRow:=gpHeg*gpCnt;
    Seen14.QRBand1.Height:=gpRow; }
  // Printers
end;

procedure TSeen13.PrinDing01(Str:String);
var
  Sline: Integer;
  gpCol, gpRow, gpCnt, gpHeg, gpWth: Integer;
  Mname1, Mname2, Mname3, Mname4, Mname5, Magin0, Mpost0: String;
  Mpost1, Mpost2, Mpost3, Mpost4, Mpost5, Mpost6, Mpost7: String;
begin
{ // Line Top
  oSqry.First;
  oSqry.MoveBy(SpinEdit1.Value-1);
  While (not oSqry.EOF) do begin
  Sline:=0;
  Printer.BeginDoc;
  Printer.Canvas.Create;
  Printer.Canvas.Font.Size:=10;
  gpWth:=Printer.Canvas.TextWidth('A');
  gpHeg:=Printer.Canvas.TextHeight('A');
  if SpinEdit64.Value=0 Then
  gpHeg:=gpHeg+(gpHeg div 6) else
  gpHeg:=SpinEdit64.Value;
  gpCol:=0; gpRow:=0; gpCnt:=0;
    // DB Seek
    if RadioButton2.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Scode').Value='O' ) do oSqry.Next;
    if RadioButton3.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Scode').Value<>'O') do oSqry.Next;
    While (not oSqry.EOF) and (oSqry.FieldByName('Gpost').Value=''  ) do oSqry.Next;
    Mname1:=''; Mname2:=''; Mname3:=''; Mname4:=''; Mname5:='';
    Mname1:=oSqry.FieldByName('Gadds').AsString;
    Mpost0:=oSqry.FieldByName('Gpost').AsString;
    Mpost1:=Copy(Mpost0,1,1);
    Mpost2:=Copy(Mpost0,2,1);
    Mpost3:=Copy(Mpost0,3,1);
    if SpinEdit74.Value<>0 Then
    Mpost4:=Copy(Mpost0,4,1) else Mpost4:='';
    Mpost5:=Copy(Mpost0,5,1);
    Mpost6:=Copy(Mpost0,6,1);
    Mpost7:=Copy(Mpost0,7,1);
    if nPrnt='11' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end
    else if nPrnt='12' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end
    else if nPrnt='13' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname3:=oSqry.FieldByName('Gjice').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end
    else if nPrnt='15' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end;
    if Edit29.Text<>'' Then Mname4:=Edit29.Text+'  '+Edit28.Text
    else Mname4:=Mname4+'  '+Edit28.Text;
    Magin0:=Format('%'+IntToStr(SpinEdit71.Value)+'s', [' ']);
    if SpinEdit71.Value=0 Then
    Mname5:=Mname5+Mpost1 else Mname5:=Mname5+Magin0+Mpost1;
    Magin0:=Format('%'+IntToStr(SpinEdit72.Value)+'s', [' ']);
    if SpinEdit72.Value=0 Then
    Mname5:=Mname5+Mpost2 else Mname5:=Mname5+Magin0+Mpost2;
    Magin0:=Format('%'+IntToStr(SpinEdit73.Value)+'s', [' ']);
    if SpinEdit73.Value=0 Then
    Mname5:=Mname5+Mpost3 else Mname5:=Mname5+Magin0+Mpost3;
    Magin0:=Format('%'+IntToStr(SpinEdit74.Value)+'s', [' ']);
    if SpinEdit74.Value=0 Then
    Mname5:=Mname5+Mpost4 else Mname5:=Mname5+Magin0+Mpost4;
    Magin0:=Format('%'+IntToStr(SpinEdit75.Value)+'s', [' ']);
    if SpinEdit75.Value=0 Then
    Mname5:=Mname5+Mpost5 else Mname5:=Mname5+Magin0+Mpost5;
    Magin0:=Format('%'+IntToStr(SpinEdit76.Value)+'s', [' ']);
    if SpinEdit76.Value=0 Then
    Mname5:=Mname5+Mpost6 else Mname5:=Mname5+Magin0+Mpost6;
    Magin0:=Format('%'+IntToStr(SpinEdit77.Value)+'s', [' ']);
    if SpinEdit77.Value=0 Then
    Mname5:=Mname5+Mpost7 else Mname5:=Mname5+Magin0+Mpost7;
    // Space
    if (oSqry.RecNo < SpinEdit1.Value) or (oSqry.RecNo > SpinEdit2.Value) Then begin
    Mname1:=''; Mname2:=''; Mname3:=''; Mname4:=''; Mname5:=''; end;
    oSqry.Next;
    // Line 1
    if Sline=0 Then
    Inc(gpCnt,SpinEdit21.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit21.Font;
      gpCol:=gpWth*SpinEdit22.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname1);
    // Line 2
    Inc(gpCnt,SpinEdit23.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit22.Font;
      gpCol:=gpWth*SpinEdit24.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname2);
    // Line 3
    Inc(gpCnt,SpinEdit25.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit23.Font;
      gpCol:=gpWth*SpinEdit26.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname3);
    // Line 4
    Inc(gpCnt,SpinEdit27.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit24.Font;
      gpCol:=gpWth*SpinEdit28.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname4);
    // Line 5
    Inc(gpCnt,SpinEdit29.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit25.Font;
      gpCol:=gpWth*SpinEdit71.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname5);
    // Line 0
    Inc(gpCnt,SpinEdit31.Value); gpRow:=gpHeg*gpCnt;
      Sline:=2;
    if (oSqry.RecNo > SpinEdit2.Value) Then begin
      oSqry.Last; oSqry.Next;
    end;
  gpRow:=gpHeg*gpCnt;
  Printer.Canvas.TextOut(gpCol, gpRow, '');
  Printer.EndDoc;
  Screen.Cursor:=crDefault;
  end; }
end;

procedure TSeen13.PrinDing02(Str:String);
var
  Sline, Cou: Integer;
  gpCol, gpRow, gpCnt, gpHeg, gpWth: Integer;
  Mname1, Mname2, Mname3, Mname4, Mname5, Magin0, Mpost0: String;
  Mpost1, Mpost2, Mpost3, Mpost4, Mpost5, Mpost6, Mpost7: String;
  Nname1, Nname2, Nname3, Nname4, Nname5, Nagin0, Npost0: String;
  Npost1, Npost2, Npost3, Npost4, Npost5, Npost6, Npost7: String;
begin
{ oSqry.First;
  oSqry.MoveBy(SpinEdit1.Value-1);
  While (not oSqry.EOF) do begin
  Cou:=0; Sline:=0;
  Printer.BeginDoc;
  Printer.Canvas.Create;
  Printer.Canvas.Font.Size:=10;
  gpWth:=Printer.Canvas.TextWidth('A');
  gpHeg:=Printer.Canvas.TextHeight('A');
  if SpinEdit64.Value=0 Then
  gpHeg:=gpHeg+(gpHeg div 6) else
  gpHeg:=SpinEdit64.Value;
  gpCol:=0; gpRow:=0; gpCnt:=0;
  // Line Top
  While (not oSqry.EOF) and (SpinEdit33.Value>Cou) do begin
    // DB Seek
    if RadioButton2.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Scode').Value='O' ) do oSqry.Next;
    if RadioButton3.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Scode').Value<>'O') do oSqry.Next;
    While (not oSqry.EOF) and (oSqry.FieldByName('Gpost').Value=''  ) do oSqry.Next;
    Mname1:=''; Mname2:=''; Mname3:=''; Mname4:=''; Mname5:='';
    Mname1:=oSqry.FieldByName('Gadds').AsString;
    Mpost0:=oSqry.FieldByName('Gpost').AsString;
    Mpost1:=Copy(Mpost0,1,1);
    Mpost2:=Copy(Mpost0,2,1);
    Mpost3:=Copy(Mpost0,3,1);
    Mpost4:=Copy(Mpost0,4,1);
    Mpost5:=Copy(Mpost0,5,1);
    Mpost6:=Copy(Mpost0,6,1);
    Mpost7:=Copy(Mpost0,7,1);
    if nPrnt='11' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='12' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='13' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname3:=oSqry.FieldByName('Gjice').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='15' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end;
    if Edit29.Text<>'' Then Mname4:=Edit29.Text+'  '+Edit28.Text
    else Mname4:=Mname4+'  '+Edit28.Text;
    Magin0:=Format('%'+IntToStr(SpinEdit71.Value)+'s', [' ']);
    if SpinEdit71.Value=0 Then
    Mname5:=Mname5+Mpost1 else Mname5:=Mname5+Magin0+Mpost1;
    Magin0:=Format('%'+IntToStr(SpinEdit72.Value)+'s', [' ']);
    if SpinEdit72.Value=0 Then
    Mname5:=Mname5+Mpost2 else Mname5:=Mname5+Magin0+Mpost2;
    Magin0:=Format('%'+IntToStr(SpinEdit73.Value)+'s', [' ']);
    if SpinEdit73.Value=0 Then
    Mname5:=Mname5+Mpost3 else Mname5:=Mname5+Magin0+Mpost3;
    Magin0:=Format('%'+IntToStr(SpinEdit74.Value)+'s', [' ']);
    if SpinEdit74.Value=0 Then
    Mname5:=Mname5+Mpost4 else Mname5:=Mname5+Magin0+Mpost4;
    Magin0:=Format('%'+IntToStr(SpinEdit75.Value)+'s', [' ']);
    if SpinEdit75.Value=0 Then
    Mname5:=Mname5+Mpost5 else Mname5:=Mname5+Magin0+Mpost5;
    Magin0:=Format('%'+IntToStr(SpinEdit76.Value)+'s', [' ']);
    if SpinEdit71.Value=0 Then
    Mname5:=Mname5+Mpost6 else Mname5:=Mname5+Magin0+Mpost6;
    Magin0:=Format('%'+IntToStr(SpinEdit77.Value)+'s', [' ']);
    if SpinEdit71.Value=0 Then
    Mname5:=Mname5+Mpost7 else Mname5:=Mname5+Magin0+Mpost7;
    // Space
    if (oSqry.RecNo < SpinEdit1.Value) or (oSqry.RecNo > SpinEdit2.Value) Then begin
    Mname1:=''; Mname2:=''; Mname3:=''; Mname4:=''; Mname5:=''; end;
    oSqry.Next;
    // DB Seek
    if RadioButton2.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Scode').Value='O' ) do oSqry.Next;
    if RadioButton3.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Scode').Value<>'O') do oSqry.Next;
    While (not oSqry.EOF) and (oSqry.FieldByName('Gpost').Value=''  ) do oSqry.Next;
    Nname1:=''; Nname2:=''; Nname3:=''; Nname4:=''; Nname5:='';
    Nname1:=oSqry.FieldByName('Gadds').AsString;
    Npost0:=oSqry.FieldByName('Gpost').AsString;
    Npost1:=Copy(Npost0,1,1);
    Npost2:=Copy(Npost0,2,1);
    Npost3:=Copy(Npost0,3,1);
    Npost4:=Copy(Npost0,4,1);
    Npost5:=Copy(Npost0,5,1);
    Npost6:=Copy(Npost0,6,1);
    Npost7:=Copy(Npost0,7,1);
    if nPrnt='11' Then begin
      Nname2:=oSqry.FieldByName('Gname').AsString;
      Nname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='12' Then begin
      Nname2:=oSqry.FieldByName('Gname').AsString;
      Nname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='13' Then begin
      Nname2:=oSqry.FieldByName('Gname').AsString;
      Nname3:=oSqry.FieldByName('Gjice').AsString;
      Nname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='15' Then begin
      Nname2:=oSqry.FieldByName('Gname').AsString;
      Nname4:=oSqry.FieldByName('Gposa').AsString;
    end;
    if Edit29.Text<>'' Then Nname4:=Edit29.Text+'  '+Edit28.Text
    else Nname4:=Nname4+'  '+Edit28.Text;
    Nagin0:=Format('%'+IntToStr(SpinEdit71.Value)+'s', [' ']);
    if SpinEdit71.Value=0 Then
    Nname5:=Nname5+Npost1 else Nname5:=Nname5+Nagin0+Npost1;
    Nagin0:=Format('%'+IntToStr(SpinEdit72.Value)+'s', [' ']);
    if SpinEdit72.Value=0 Then
    Nname5:=Nname5+Npost2 else Nname5:=Nname5+Nagin0+Npost2;
    Nagin0:=Format('%'+IntToStr(SpinEdit73.Value)+'s', [' ']);
    if SpinEdit73.Value=0 Then
    Nname5:=Nname5+Npost3 else Nname5:=Nname5+Nagin0+Npost3;
    Nagin0:=Format('%'+IntToStr(SpinEdit74.Value)+'s', [' ']);
    if SpinEdit74.Value=0 Then
    Nname5:=Nname5+Npost4 else Nname5:=Nname5+Nagin0+Npost4;
    Nagin0:=Format('%'+IntToStr(SpinEdit75.Value)+'s', [' ']);
    if SpinEdit75.Value=0 Then
    Nname5:=Nname5+Npost5 else Nname5:=Nname5+Nagin0+Npost5;
    Nagin0:=Format('%'+IntToStr(SpinEdit76.Value)+'s', [' ']);
    if SpinEdit76.Value=0 Then
    Nname5:=Nname5+Npost6 else Nname5:=Nname5+Nagin0+Npost6;
    Nagin0:=Format('%'+IntToStr(SpinEdit77.Value)+'s', [' ']);
    if SpinEdit77.Value=0 Then
    Nname5:=Nname5+Npost7 else Nname5:=Nname5+Nagin0+Npost7;
    // Space
    if (oSqry.RecNo < SpinEdit1.Value) or (oSqry.RecNo > SpinEdit2.Value) Then begin
    Nname1:=''; Nname2:=''; Nname3:=''; Nname4:=''; Nname5:=''; end;
    oSqry.Next;
    // Line 1
    if Sline=0 Then
    Inc(gpCnt,SpinEdit21.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit21.Font;
      gpCol:=gpWth*SpinEdit22.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname1);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname1);
    // Line 2
    Inc(gpCnt,SpinEdit23.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit22.Font;
      gpCol:=gpWth*SpinEdit24.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname2);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname2);
    // Line 3
    Inc(gpCnt,SpinEdit25.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit23.Font;
      gpCol:=gpWth*SpinEdit26.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname3);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname3);
    // Line 4
    Inc(gpCnt,SpinEdit27.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit24.Font;
      gpCol:=gpWth*SpinEdit28.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname4);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname4);
    // Line 5
    Inc(gpCnt,SpinEdit29.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit25.Font;
      gpCol:=gpWth*SpinEdit71.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname5);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname5);
    // Line Bottom
    Inc(gpCnt,SpinEdit31.Value);
      Sline:=2;
      Cou:=Cou+2;
    if (oSqry.RecNo > SpinEdit2.Value) Then begin
      oSqry.Last; oSqry.Next;
    end;
  end;
  gpRow:=gpHeg*gpCnt;
  Printer.Canvas.TextOut(gpCol, gpRow, '');
  Printer.EndDoc;
  Screen.Cursor:=crDefault;
  end; }
end;

procedure TSeen13.PrinDing03(Str:String);
var
  Sline, Cou: Integer;
  gpCol, gpRow, gpCnt, gpHeg, gpWth: Integer;
  Mname1, Mname2, Mname3, Mname4, Mname5, Magin0, Mpost0: String;
  Mpost1, Mpost2, Mpost3, Mpost4, Mpost5, Mpost6, Mpost7: String;
  Nname1, Nname2, Nname3, Nname4, Nname5, Nagin0, Npost0: String;
  Npost1, Npost2, Npost3, Npost4, Npost5, Npost6, Npost7: String;
begin
{ oSqry.First;
  oSqry.MoveBy(SpinEdit1.Value-1);
  While (not oSqry.EOF) do begin
  Cou:=0; Sline:=0;
  Printer.BeginDoc;
  Printer.Canvas.Create;
  Printer.Canvas.Font.Size:=10;
  gpWth:=Printer.Canvas.TextWidth('A');
  gpHeg:=Printer.Canvas.TextHeight('A');
  if SpinEdit64.Value=0 Then
  gpHeg:=gpHeg+(gpHeg div 6) else
  gpHeg:=SpinEdit64.Value;
  gpCol:=0; gpRow:=0; gpCnt:=0;
  // Line Top
  While (not oSqry.EOF) and (SpinEdit33.Value>Cou) do begin
    // DB Seek
    if RadioButton2.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Gbigo').Value='O' ) do oSqry.Next;
    if RadioButton3.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Gbigo').Value<>'O') do oSqry.Next;
    While (not oSqry.EOF) and (oSqry.FieldByName('Gpost').Value=''  ) do oSqry.Next;
    Mname1:=''; Mname2:=''; Mname3:=''; Mname4:=''; Mname5:='';
    Mname1:=oSqry.FieldByName('Gadds').AsString;
    Mpost0:=oSqry.FieldByName('Gpost').AsString;
    Mpost1:=Copy(Mpost0,1,1);
    Mpost2:=Copy(Mpost0,2,1);
    Mpost3:=Copy(Mpost0,3,1);
    Mpost4:=Copy(Mpost0,4,1);
    Mpost5:=Copy(Mpost0,5,1);
    Mpost6:=Copy(Mpost0,6,1);
    Mpost7:=Copy(Mpost0,7,1);
    if nPrnt='11' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='12' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='13' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname3:=oSqry.FieldByName('Gjice').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='15' Then begin
      Mname2:=oSqry.FieldByName('Gname').AsString;
      Mname4:=oSqry.FieldByName('Gposa').AsString;
    end;
    if Edit29.Text<>'' Then Mname4:=Edit29.Text+'  '+Edit28.Text
    else Mname4:=Mname4+'  '+Edit28.Text;
    Magin0:=Format('%'+IntToStr(SpinEdit71.Value)+'s', [' ']);
    if SpinEdit71.Value=0 Then
    Mname5:=Mname5+Mpost1 else Mname5:=Mname5+Magin0+Mpost1;
    Magin0:=Format('%'+IntToStr(SpinEdit72.Value)+'s', [' ']);
    if SpinEdit72.Value=0 Then
    Mname5:=Mname5+Mpost2 else Mname5:=Mname5+Magin0+Mpost2;
    Magin0:=Format('%'+IntToStr(SpinEdit73.Value)+'s', [' ']);
    if SpinEdit73.Value=0 Then
    Mname5:=Mname5+Mpost3 else Mname5:=Mname5+Magin0+Mpost3;
    Magin0:=Format('%'+IntToStr(SpinEdit74.Value)+'s', [' ']);
    if SpinEdit74.Value=0 Then
    Mname5:=Mname5+Mpost4 else Mname5:=Mname5+Magin0+Mpost4;
    Magin0:=Format('%'+IntToStr(SpinEdit75.Value)+'s', [' ']);
    if SpinEdit75.Value=0 Then
    Mname5:=Mname5+Mpost5 else Mname5:=Mname5+Magin0+Mpost5;
    Magin0:=Format('%'+IntToStr(SpinEdit76.Value)+'s', [' ']);
    if SpinEdit71.Value=0 Then
    Mname5:=Mname5+Mpost6 else Mname5:=Mname5+Magin0+Mpost6;
    Magin0:=Format('%'+IntToStr(SpinEdit77.Value)+'s', [' ']);
    if SpinEdit71.Value=0 Then
    Mname5:=Mname5+Mpost7 else Mname5:=Mname5+Magin0+Mpost7;
    // Space
    if (oSqry.RecNo < SpinEdit1.Value) or (oSqry.RecNo > SpinEdit2.Value) Then begin
    Mname1:=''; Mname2:=''; Mname3:=''; Mname4:=''; Mname5:=''; end;
    oSqry.Next;
    // DB Seek
    if RadioButton2.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Gbigo').Value='O' ) do oSqry.Next;
    if RadioButton3.Checked=True Then
    While (not oSqry.EOF) and (oSqry.FieldByName('Gbigo').Value<>'O') do oSqry.Next;
    While (not oSqry.EOF) and (oSqry.FieldByName('Gpost').Value=''  ) do oSqry.Next;
    Nname1:=''; Nname2:=''; Nname3:=''; Nname4:=''; Nname5:='';
    Nname1:=oSqry.FieldByName('Gadds').AsString;
    Npost0:=oSqry.FieldByName('Gpost').AsString;
    Npost1:=Copy(Npost0,1,1);
    Npost2:=Copy(Npost0,2,1);
    Npost3:=Copy(Npost0,3,1);
    Npost4:=Copy(Npost0,4,1);
    Npost5:=Copy(Npost0,5,1);
    Npost6:=Copy(Npost0,6,1);
    Npost7:=Copy(Npost0,7,1);
    if nPrnt='11' Then begin
      Nname2:=oSqry.FieldByName('Gname').AsString;
      Nname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='12' Then begin
      Nname2:=oSqry.FieldByName('Gname').AsString;
      Nname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='13' Then begin
      Nname2:=oSqry.FieldByName('Gname').AsString;
      Nname3:=oSqry.FieldByName('Gjice').AsString;
      Nname4:=oSqry.FieldByName('Gposa').AsString;
    end else
    if nPrnt='15' Then begin
      Nname2:=oSqry.FieldByName('Gname').AsString;
      Nname4:=oSqry.FieldByName('Gposa').AsString;
    end;
    if Edit29.Text<>'' Then Nname4:=Edit29.Text+'  '+Edit28.Text
    else Nname4:=Nname4+'  '+Edit28.Text;
    Nagin0:=Format('%'+IntToStr(SpinEdit71.Value)+'s', [' ']);
    if SpinEdit71.Value=0 Then
    Nname5:=Nname5+Npost1 else Nname5:=Nname5+Nagin0+Npost1;
    Nagin0:=Format('%'+IntToStr(SpinEdit72.Value)+'s', [' ']);
    if SpinEdit72.Value=0 Then
    Nname5:=Nname5+Npost2 else Nname5:=Nname5+Nagin0+Npost2;
    Nagin0:=Format('%'+IntToStr(SpinEdit73.Value)+'s', [' ']);
    if SpinEdit73.Value=0 Then
    Nname5:=Nname5+Npost3 else Nname5:=Nname5+Nagin0+Npost3;
    Nagin0:=Format('%'+IntToStr(SpinEdit74.Value)+'s', [' ']);
    if SpinEdit74.Value=0 Then
    Nname5:=Nname5+Npost4 else Nname5:=Nname5+Nagin0+Npost4;
    Nagin0:=Format('%'+IntToStr(SpinEdit75.Value)+'s', [' ']);
    if SpinEdit75.Value=0 Then
    Nname5:=Nname5+Npost5 else Nname5:=Nname5+Nagin0+Npost5;
    Nagin0:=Format('%'+IntToStr(SpinEdit76.Value)+'s', [' ']);
    if SpinEdit76.Value=0 Then
    Nname5:=Nname5+Npost6 else Nname5:=Nname5+Nagin0+Npost6;
    Nagin0:=Format('%'+IntToStr(SpinEdit77.Value)+'s', [' ']);
    if SpinEdit77.Value=0 Then
    Nname5:=Nname5+Npost7 else Nname5:=Nname5+Nagin0+Npost7;
    // Space
    if (oSqry.RecNo < SpinEdit1.Value) or (oSqry.RecNo > SpinEdit2.Value) Then begin
    Nname1:=''; Nname2:=''; Nname3:=''; Nname4:=''; Nname5:=''; end;
    oSqry.Next;
    // Line 1
    if Sline=0 Then
    Inc(gpCnt,SpinEdit21.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit21.Font;
      gpCol:=gpWth*SpinEdit22.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname1);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname1);
    // Line 2
    Inc(gpCnt,SpinEdit23.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit22.Font;
      gpCol:=gpWth*SpinEdit24.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname2);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname2);
    // Line 3
    Inc(gpCnt,SpinEdit25.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit23.Font;
      gpCol:=gpWth*SpinEdit26.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname3);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname3);
    // Line 4
    Inc(gpCnt,SpinEdit27.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit24.Font;
      gpCol:=gpWth*SpinEdit28.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname4);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname4);
    // Line 5
    Inc(gpCnt,SpinEdit29.Value); gpRow:=gpHeg*gpCnt;
      Printer.Canvas.Font:=Edit25.Font;
      gpCol:=gpWth*SpinEdit71.Value;
      Printer.Canvas.TextOut(gpCol, gpRow, Mname5);
      gpCol:=gpWth*SpinEdit32.Value+gpCol;
      Printer.Canvas.TextOut(gpCol, gpRow, Nname5);
    // Line Bottom
    Inc(gpCnt,SpinEdit31.Value);
      Sline:=2;
      Cou:=Cou+2;
    if (oSqry.RecNo > SpinEdit2.Value) Then begin
      oSqry.Last; oSqry.Next;
    end;
  end;
  gpRow:=gpHeg*gpCnt;
  Printer.Canvas.TextOut(gpCol, gpRow, '');
  Printer.EndDoc;
  Screen.Cursor:=crDefault;
  end; }
end;

procedure TSeen13.frDBDataSet00_01Next(Sender: TObject);
var p_Gjeja: String;
begin
  if RadioButton2.Checked=True Then
  While (not oSqry.EOF) and (oSqry.FieldByName('Gbigo').Value='O' ) do oSqry.Next;
  if RadioButton3.Checked=True Then
  While (not oSqry.EOF) and (oSqry.FieldByName('Gbigo').Value<>'O') do oSqry.Next;
  While (not oSqry.EOF) and (oSqry.FieldByName('Gpost').Value=''  ) do oSqry.Next;
  While (not oSqry.EOF) and
  ((oSqry.RecNo < SpinEdit1.Value) or (oSqry.RecNo > SpinEdit2.Value)) do oSqry.Next;

  if Edit29.Text<>'' Then
  p_Gjeja:=Edit29.Text+' '+Edit28.Text else
  if oSqry.FieldByName('Gposa').AsString<>'' then
  p_Gjeja:=oSqry.FieldByName('Gposa').AsString+' '+Edit28.Text else
  p_Gjeja:='';
  Tong60.frReport00_01.FindObject('Memo04').Memo.Text:=p_Gjeja;
end;

end.
