unit Seep11;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Qrctrls, Printers, ExtCtrls, StdCtrls, Mylabel, Grids, DBGrids, Db,
  TFlatPanelUnit, TFlatGroupBoxUnit, TFlatButtonUnit, TFlatEditUnit,
  TFlatComboBoxUnit, TFlatSpinEditUnit, TFlatSpeedButtonUnit,
  FR_DSet, FR_DBSet, FR_Class;

type
  TSeen11 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    FontDialog1: TFontDialog;
    ColorDialog1: TColorDialog;
    PrinterSetupDialog1: TPrinterSetupDialog;
    Panel101: TFlatPanel;
    GroupBox1: TFlatGroupBox;
    SpeedButton0: TFlatSpeedButton;
    TitleEdit: TFlatEdit;
    Button1: TFlatButton;
    Button2: TFlatButton;
    Button3: TFlatButton;
    Button4: TFlatButton;
    Panel102: TFlatPanel;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    SpeedButton1: TFlatSpeedButton;
    SpeedButton2: TFlatSpeedButton;
    SpeedButton3: TFlatSpeedButton;
    Panel104: TFlatPanel;
    DBGrid1: TDBGrid;
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
    SpinEdit7: TFlatSpinEditInteger;
    SpinEdit8: TFlatSpinEditInteger;
    SpinEdit3: TFlatSpinEditInteger;
    SpinEdit4: TFlatSpinEditInteger;
    SpinEdit5: TFlatSpinEditInteger;
    SpinEdit6: TFlatSpinEditInteger;
    Panel103: TFlatPanel;
    ListBox: TListBox;
    RadioButton1: TRadioButton;
    RadioButton2: TRadioButton;
    RadioButton3: TRadioButton;
    procedure SaveKey(St0:String);
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure SpeedButton0Click(Sender: TObject);
    procedure SpeedButton1Click(Sender: TObject);
    procedure SpeedButton2Click(Sender: TObject);
    procedure SpeedButton3Click(Sender: TObject);
    procedure SpeedButton4Click(Sender: TObject);
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure Button4Click(Sender: TObject);
    procedure ComboBox1Change(Sender: TObject);
    procedure DBGrid1KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid1KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seen11: TSeen11;
  frReport01_01: TfrReport;
  CoStr: array[0..41] of string;
  SpStr: array[0..41] of Integer;
  PsumX, PsumY: Integer;

implementation

{$R *.DFM}

uses Base01, TcpLib, Tong06;

procedure TSeen11.SaveKey(St0:String);
var St1: String;
begin
  lSqry:=Base10.T1_Sub91;
  Base10.OpenShow(lSqry);

  Sqlen :=
  'Select Gubun,Gname,Gfild,Gnumb From Gg_Megn Where Gubun'+'='+#39+St0+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(lSqry)
  else ShowMessage(E_Open);
end;

procedure TSeen11.FormShow(Sender: TObject);
begin
  SpinEdit1.Value:=1;
  SpinEdit2.Value:=oSqry.RecordCount;
  ListBox.Items.Clear;
  if nPrnt='11' Then begin
    SaveKey(nPrnt);
    ListBox.Items.Add('거래처구분'); ListBox.Items.Add('사업자번호');
    ListBox.Items.Add('코    드'); ListBox.Items.Add('거래처명');
    ListBox.Items.Add('대표자명'); ListBox.Items.Add('지    역');
    ListBox.Items.Add('업    태'); ListBox.Items.Add('종    목');
    ListBox.Items.Add('전화번호'); ListBox.Items.Add('팩스번호');
    ListBox.Items.Add('우편번호'); ListBox.Items.Add('주    소');
    ListBox.Items.Add('담 당 자'); ListBox.Items.Add('위    탁');
    ListBox.Items.Add('현    매'); ListBox.Items.Add('매    절');
    ListBox.Items.Add('특    별'); ListBox.Items.Add('신    간');
    ListBox.Items.Add('비    고');
    CoStr[00]:='Sname'; SpStr[00]:=oSqry.FieldByName('Sname').DisplayWidth*8;
    CoStr[01]:='Gnumb'; SpStr[01]:=oSqry.FieldByName('Gnumb').DisplayWidth*8;
    CoStr[02]:='Gcode'; SpStr[02]:=oSqry.FieldByName('Gcode').DisplayWidth*8;
    CoStr[03]:='Gname'; SpStr[03]:=oSqry.FieldByName('Gname').DisplayWidth*8;
    CoStr[04]:='Gposa'; SpStr[04]:=oSqry.FieldByName('Gposa').DisplayWidth*8;
    CoStr[05]:='Jubun'; SpStr[05]:=oSqry.FieldByName('Jubun').DisplayWidth*8;
    CoStr[06]:='Guper'; SpStr[06]:=oSqry.FieldByName('Guper').DisplayWidth*8;
    CoStr[07]:='Gjomo'; SpStr[07]:=oSqry.FieldByName('Gjomo').DisplayWidth*8;
    CoStr[08]:='Gtels'; SpStr[08]:=oSqry.FieldByName('Gtels').DisplayWidth*8;
    CoStr[09]:='Gfaxs'; SpStr[09]:=oSqry.FieldByName('Gfaxs').DisplayWidth*8;
    CoStr[10]:='Gpost'; SpStr[10]:=oSqry.FieldByName('Gpost').DisplayWidth*8;
    CoStr[11]:='Gadds'; SpStr[11]:=oSqry.FieldByName('Gadds').DisplayWidth*8;
    CoStr[12]:='Gpper'; SpStr[12]:=oSqry.FieldByName('Gpper').DisplayWidth*8;
    CoStr[13]:='Grat1'; SpStr[13]:=oSqry.FieldByName('Grat1').DisplayWidth*8;
    CoStr[14]:='Grat2'; SpStr[14]:=oSqry.FieldByName('Grat2').DisplayWidth*8;
    CoStr[15]:='Grat3'; SpStr[15]:=oSqry.FieldByName('Grat3').DisplayWidth*8;
    CoStr[16]:='Grat4'; SpStr[16]:=oSqry.FieldByName('Grat4').DisplayWidth*8;
    CoStr[17]:='Gqut1'; SpStr[17]:=oSqry.FieldByName('Gqut1').DisplayWidth*8;
    CoStr[18]:='Gbigo'; SpStr[18]:=oSqry.FieldByName('Gbigo').DisplayWidth*8;
  end
  else if nPrnt='12' Then begin
    SaveKey(nPrnt);
    ListBox.Items.Add('입고처구분'); ListBox.Items.Add('사업자번호');
    ListBox.Items.Add('코    드'); ListBox.Items.Add('입고처명');
    ListBox.Items.Add('대표자명'); ListBox.Items.Add('지    역');
    ListBox.Items.Add('업    태'); ListBox.Items.Add('종    목');
    ListBox.Items.Add('전화번호'); ListBox.Items.Add('팩스번호');
    ListBox.Items.Add('우편번호'); ListBox.Items.Add('주    소');
    ListBox.Items.Add('담 당 자'); ListBox.Items.Add('위    탁');
    ListBox.Items.Add('현    매'); ListBox.Items.Add('매    절');
    ListBox.Items.Add('특    별'); ListBox.Items.Add('신    간');
    ListBox.Items.Add('비    고');
    CoStr[00]:='Sname'; SpStr[00]:=oSqry.FieldByName('Sname').DisplayWidth*8;
    CoStr[01]:='Gnumb'; SpStr[01]:=oSqry.FieldByName('Gnumb').DisplayWidth*8;
    CoStr[02]:='Gcode'; SpStr[02]:=oSqry.FieldByName('Gcode').DisplayWidth*8;
    CoStr[03]:='Gname'; SpStr[03]:=oSqry.FieldByName('Gname').DisplayWidth*8;
    CoStr[04]:='Gposa'; SpStr[04]:=oSqry.FieldByName('Gposa').DisplayWidth*8;
    CoStr[05]:='Jubun'; SpStr[05]:=oSqry.FieldByName('Jubun').DisplayWidth*8;
    CoStr[06]:='Guper'; SpStr[06]:=oSqry.FieldByName('Guper').DisplayWidth*8;
    CoStr[07]:='Gjomo'; SpStr[07]:=oSqry.FieldByName('Gjomo').DisplayWidth*8;
    CoStr[08]:='Gtels'; SpStr[08]:=oSqry.FieldByName('Gtels').DisplayWidth*8;
    CoStr[09]:='Gfaxs'; SpStr[09]:=oSqry.FieldByName('Gfaxs').DisplayWidth*8;
    CoStr[10]:='Gpost'; SpStr[10]:=oSqry.FieldByName('Gpost').DisplayWidth*8;
    CoStr[11]:='Gadds'; SpStr[11]:=oSqry.FieldByName('Gadds').DisplayWidth*8;
    CoStr[12]:='Gpper'; SpStr[12]:=oSqry.FieldByName('Gpper').DisplayWidth*8;
    CoStr[13]:='Grat1'; SpStr[13]:=oSqry.FieldByName('Grat1').DisplayWidth*8;
    CoStr[14]:='Grat2'; SpStr[14]:=oSqry.FieldByName('Grat2').DisplayWidth*8;
    CoStr[15]:='Grat3'; SpStr[15]:=oSqry.FieldByName('Grat3').DisplayWidth*8;
    CoStr[16]:='Grat4'; SpStr[16]:=oSqry.FieldByName('Grat4').DisplayWidth*8;
    CoStr[17]:='Gqut1'; SpStr[17]:=oSqry.FieldByName('Gqut1').DisplayWidth*8;
    CoStr[18]:='Gbigo'; SpStr[18]:=oSqry.FieldByName('Gbigo').DisplayWidth*8;
  end
  else if nPrnt='13' Then begin
    SaveKey(nPrnt);
    ListBox.Items.Add('저자구분'); ListBox.Items.Add('등록일자');
    ListBox.Items.Add('저자코드'); ListBox.Items.Add('저 자 명');
    ListBox.Items.Add('직 장 명'); ListBox.Items.Add('직    책');
    ListBox.Items.Add('주민등록'); ListBox.Items.Add('사업자번호');
    ListBox.Items.Add('출신학교'); ListBox.Items.Add('계좌번호');
    ListBox.Items.Add('전화번호'); ListBox.Items.Add('팩스번호');
    ListBox.Items.Add('우편번호'); ListBox.Items.Add('집 주 소');
    ListBox.Items.Add('우편번호'); ListBox.Items.Add('직장주소');
    ListBox.Items.Add('비    고');
    CoStr[00]:='Sname'; SpStr[00]:=oSqry.FieldByName('Sname').DisplayWidth*8;
    CoStr[01]:='Date1'; SpStr[01]:=oSqry.FieldByName('Date1').DisplayWidth*8;
    CoStr[02]:='Gcode'; SpStr[02]:=oSqry.FieldByName('Gcode').DisplayWidth*8;
    CoStr[03]:='Gposa'; SpStr[03]:=oSqry.FieldByName('Gposa').DisplayWidth*8;
    CoStr[04]:='Gname'; SpStr[04]:=oSqry.FieldByName('Gname').DisplayWidth*8;
    CoStr[05]:='Gjice'; SpStr[05]:=oSqry.FieldByName('Gjice').DisplayWidth*8;
    CoStr[06]:='Gnumb'; SpStr[06]:=oSqry.FieldByName('Gnumb').DisplayWidth*8;
    CoStr[07]:='Gnum1'; SpStr[07]:=oSqry.FieldByName('Gnum1').DisplayWidth*8;
    CoStr[08]:='Gscho'; SpStr[08]:=oSqry.FieldByName('Gscho').DisplayWidth*8;
    CoStr[09]:='Gnum2'; SpStr[09]:=oSqry.FieldByName('Gnum2').DisplayWidth*8;
    CoStr[10]:='Gtels'; SpStr[10]:=oSqry.FieldByName('Gtels').DisplayWidth*8;
    CoStr[11]:='Gfaxs'; SpStr[11]:=oSqry.FieldByName('Gfaxs').DisplayWidth*8;
    CoStr[12]:='Gpost'; SpStr[12]:=oSqry.FieldByName('Gpost').DisplayWidth*8;
    CoStr[13]:='Gadds'; SpStr[13]:=oSqry.FieldByName('Gadds').DisplayWidth*8;
    CoStr[14]:='Opost'; SpStr[14]:=oSqry.FieldByName('Opost').DisplayWidth*8;
    CoStr[15]:='Oadds'; SpStr[15]:=oSqry.FieldByName('Oadds').DisplayWidth*8;
    CoStr[16]:='Gbigo'; SpStr[16]:=oSqry.FieldByName('Gbigo').DisplayWidth*8;
  end
  else if nPrnt='14' Then begin
    SaveKey(nPrnt);
    ListBox.Items.Add('도서구분'); ListBox.Items.Add('도서처리');
    ListBox.Items.Add('도서코드'); ListBox.Items.Add('도 서 명');
    ListBox.Items.Add('저 자 명'); ListBox.Items.Add('단    위');
    ListBox.Items.Add('단    가'); ListBox.Items.Add('도 서 질');
    ListBox.Items.Add('ISBN번호'); ListBox.Items.Add('비    고');
    ListBox.Items.Add('위    탁'); ListBox.Items.Add('현    매');
    ListBox.Items.Add('매    절'); ListBox.Items.Add('특    별');
    ListBox.Items.Add('재    고'); ListBox.Items.Add('재고금액');
    ListBox.Items.Add('서가위치');
    CoStr[00]:='Sname'; SpStr[00]:=oSqry.FieldByName('Sname').DisplayWidth*8;
    CoStr[01]:='Jubun'; SpStr[01]:=oSqry.FieldByName('Jubun').DisplayWidth*8;
    CoStr[02]:='Gcode'; SpStr[02]:=oSqry.FieldByName('Gcode').DisplayWidth*8;
    CoStr[03]:='Gname'; SpStr[03]:=oSqry.FieldByName('Gname').DisplayWidth*8;
    CoStr[04]:='Gjeja'; SpStr[04]:=oSqry.FieldByName('Gjeja').DisplayWidth*8;
    CoStr[05]:='Gdabi'; SpStr[05]:=oSqry.FieldByName('Gdabi').DisplayWidth*8;
    CoStr[06]:='Gdang'; SpStr[06]:=oSqry.FieldByName('Gdang').DisplayWidth*8;
    CoStr[07]:='Gbjil'; SpStr[07]:=oSqry.FieldByName('Gbjil').DisplayWidth*8;
    CoStr[08]:='Gisbn'; SpStr[08]:=oSqry.FieldByName('Gisbn').DisplayWidth*8;
    CoStr[09]:='Gbigo'; SpStr[09]:=oSqry.FieldByName('Gbigo').DisplayWidth*8;
    CoStr[10]:='Grat1'; SpStr[10]:=oSqry.FieldByName('Grat1').DisplayWidth*8;
    CoStr[11]:='Grat2'; SpStr[11]:=oSqry.FieldByName('Grat2').DisplayWidth*8;
    CoStr[12]:='Grat3'; SpStr[12]:=oSqry.FieldByName('Grat3').DisplayWidth*8;
    CoStr[13]:='Grat4'; SpStr[13]:=oSqry.FieldByName('Grat4').DisplayWidth*8;
    CoStr[14]:='Gsqut'; SpStr[14]:=oSqry.FieldByName('Gsqut').DisplayWidth*8;
    CoStr[15]:='Gssum'; SpStr[15]:=oSqry.FieldByName('Gssum').DisplayWidth*8;
    CoStr[16]:='Gpost'; SpStr[16]:=oSqry.FieldByName('Gpost').DisplayWidth*8;
  end
  else if nPrnt='15' Then begin
    SaveKey(nPrnt);
    ListBox.Items.Add('거래처구분'); ListBox.Items.Add('사업자번호');
    ListBox.Items.Add('코    드'); ListBox.Items.Add('거래처명');
    ListBox.Items.Add('대표자명'); ListBox.Items.Add('지    역');
    ListBox.Items.Add('업    태'); ListBox.Items.Add('종    목');
    ListBox.Items.Add('전화번호'); ListBox.Items.Add('팩스번호');
    ListBox.Items.Add('우편번호'); ListBox.Items.Add('주    소');
    ListBox.Items.Add('담 당 자'); ListBox.Items.Add('위    탁');
    ListBox.Items.Add('현    매'); ListBox.Items.Add('매    절');
    ListBox.Items.Add('특    별'); ListBox.Items.Add('신    간');
    ListBox.Items.Add('비    고');
    CoStr[00]:='Sname'; SpStr[00]:=oSqry.FieldByName('Sname').DisplayWidth*8;
    CoStr[01]:='Gnumb'; SpStr[01]:=oSqry.FieldByName('Gnumb').DisplayWidth*8;
    CoStr[02]:='Gcode'; SpStr[02]:=oSqry.FieldByName('Gcode').DisplayWidth*8;
    CoStr[03]:='Gname'; SpStr[03]:=oSqry.FieldByName('Gname').DisplayWidth*8;
    CoStr[04]:='Gposa'; SpStr[04]:=oSqry.FieldByName('Gposa').DisplayWidth*8;
    CoStr[05]:='Jubun'; SpStr[05]:=oSqry.FieldByName('Jubun').DisplayWidth*8;
    CoStr[06]:='Guper'; SpStr[06]:=oSqry.FieldByName('Guper').DisplayWidth*8;
    CoStr[07]:='Gjomo'; SpStr[07]:=oSqry.FieldByName('Gjomo').DisplayWidth*8;
    CoStr[08]:='Gtels'; SpStr[08]:=oSqry.FieldByName('Gtels').DisplayWidth*8;
    CoStr[09]:='Gfaxs'; SpStr[09]:=oSqry.FieldByName('Gfaxs').DisplayWidth*8;
    CoStr[10]:='Gpost'; SpStr[10]:=oSqry.FieldByName('Gpost').DisplayWidth*8;
    CoStr[11]:='Gadds'; SpStr[11]:=oSqry.FieldByName('Gadds').DisplayWidth*8;
    CoStr[12]:='Gpper'; SpStr[12]:=oSqry.FieldByName('Gpper').DisplayWidth*8;
    CoStr[13]:='Grat1'; SpStr[13]:=oSqry.FieldByName('Grat1').DisplayWidth*8;
    CoStr[14]:='Grat2'; SpStr[14]:=oSqry.FieldByName('Grat2').DisplayWidth*8;
    CoStr[15]:='Grat3'; SpStr[15]:=oSqry.FieldByName('Grat3').DisplayWidth*8;
    CoStr[16]:='Grat4'; SpStr[16]:=oSqry.FieldByName('Grat4').DisplayWidth*8;
    CoStr[17]:='Gqut1'; SpStr[17]:=oSqry.FieldByName('Gqut1').DisplayWidth*8;
    CoStr[18]:='Gbigo'; SpStr[18]:=oSqry.FieldByName('Gbigo').DisplayWidth*8;
  end
  else if nPrnt='17' Then begin
    SaveKey(nPrnt);
    ListBox.Items.Add('출판사구분'); ListBox.Items.Add('사업자번호');
    ListBox.Items.Add('코    드'); ListBox.Items.Add('출판사명');
    ListBox.Items.Add('대표자명'); ListBox.Items.Add('지    역');
    ListBox.Items.Add('업    태'); ListBox.Items.Add('종    목');
    ListBox.Items.Add('전화번호'); ListBox.Items.Add('팩스번호');
    ListBox.Items.Add('우편번호'); ListBox.Items.Add('주    소');
    ListBox.Items.Add('담 당 자'); ListBox.Items.Add('핸 드 폰');
    ListBox.Items.Add('계약일자'); ListBox.Items.Add('보증금액');
    ListBox.Items.Add('참고내용'); ListBox.Items.Add('비    고');
    CoStr[00]:='Sname'; SpStr[00]:=oSqry.FieldByName('Sname').DisplayWidth*8;
    CoStr[01]:='Gnumb'; SpStr[01]:=oSqry.FieldByName('Gnumb').DisplayWidth*8;
    CoStr[02]:='Gcode'; SpStr[02]:=oSqry.FieldByName('Gcode').DisplayWidth*8;
    CoStr[03]:='Gname'; SpStr[03]:=oSqry.FieldByName('Gname').DisplayWidth*8;
    CoStr[04]:='Gposa'; SpStr[04]:=oSqry.FieldByName('Gposa').DisplayWidth*8;
    CoStr[05]:='Jubun'; SpStr[05]:=oSqry.FieldByName('Jubun').DisplayWidth*8;
    CoStr[06]:='Guper'; SpStr[06]:=oSqry.FieldByName('Guper').DisplayWidth*8;
    CoStr[07]:='Gjomo'; SpStr[07]:=oSqry.FieldByName('Gjomo').DisplayWidth*8;
    CoStr[08]:='Gtels'; SpStr[08]:=oSqry.FieldByName('Gtels').DisplayWidth*8;
    CoStr[09]:='Gfaxs'; SpStr[09]:=oSqry.FieldByName('Gfaxs').DisplayWidth*8;
    CoStr[10]:='Gpost'; SpStr[10]:=oSqry.FieldByName('Gpost').DisplayWidth*8;
    CoStr[11]:='Gadds'; SpStr[11]:=oSqry.FieldByName('Gadds').DisplayWidth*8;
    CoStr[12]:='Gpper'; SpStr[12]:=oSqry.FieldByName('Gpper').DisplayWidth*8;
    CoStr[13]:='Name1'; SpStr[13]:=oSqry.FieldByName('Name1').DisplayWidth*8;
    CoStr[14]:='Gdate'; SpStr[14]:=oSqry.FieldByName('Gdate').DisplayWidth*8;
    CoStr[15]:='Gssum'; SpStr[15]:=oSqry.FieldByName('Gssum').DisplayWidth*8;
    CoStr[16]:='Name2'; SpStr[16]:=oSqry.FieldByName('Name2').DisplayWidth*8;
    CoStr[17]:='Gbigo'; SpStr[17]:=oSqry.FieldByName('Gbigo').DisplayWidth*8;
  end;
  if nPrnt='11' Then TitleEdit.Text:='거래처 현황';
  if nPrnt='12' Then TitleEdit.Text:='입고처 현황';
  if nPrnt='13' Then TitleEdit.Text:='저 자  현황';
  if nPrnt='14' Then TitleEdit.Text:='도 서  현황';
  if nPrnt='15' Then TitleEdit.Text:='거래처 현황';
  if nPrnt='17' Then TitleEdit.Text:='출판사 현황';
  ListBox.MultiSelect:=True;
  ListBox.MultiSelect:=False;
  ComboBox1.ItemIndex:=0;
  ComboBox1Change(Self);
end;

procedure TSeen11.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Base10.DeleteSX(lSqry); lSqry.Close;
end;

procedure TSeen11.ComboBox1Change(Sender: TObject);
begin
  if ComboBox1.ItemIndex=0 Then begin
  SpinEdit7.Text:='2100';
  SpinEdit8.Text:='2970'; end;
  if ComboBox1.ItemIndex=1 Then begin
  SpinEdit7.Text:='2159';
  SpinEdit8.Text:='2794'; end;
end;

procedure TSeen11.SpeedButton0Click(Sender: TObject);
begin
  FontDialog1.Font := SpeedButton0.Font;
  FontDialog1.Execute;
  SpeedButton0.Font := FontDialog1.Font;
end;

procedure TSeen11.SpeedButton1Click(Sender: TObject);
var St1: String;
begin

  Sqlen := 'INSERT INTO Gg_Megn '+
  '(Gubun, Gname, Gfild, Gnumb) VALUES '+
  '(''@Gubun'',''@Gname'',''@Gfild'',''@Gnumb'')';

  Translate(Sqlen, '@Gubun', nPrnt);
  Translate(Sqlen, '@Gname', ListBox.Items[ListBox.ItemIndex]);
  Translate(Sqlen, '@Gfild', CoStr[ListBox.ItemIndex]);
  Translate(Sqlen, '@Gnumb', IntToStr(SpStr[ListBox.ItemIndex]));

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Insert);

  lSqry.Append;
  lSqry.FieldByName('Gubun').Value:=nPrnt;
  lSqry.FieldByName('Gname').Value:=ListBox.Items[ListBox.ItemIndex];
  lSqry.FieldByName('Gfild').Value:=CoStr[ListBox.ItemIndex];
  lSqry.FieldByName('Gnumb').Value:=SpStr[ListBox.ItemIndex];
  lSqry.Post;

end;

procedure TSeen11.SpeedButton2Click(Sender: TObject);
var St1: String;
begin
  if MessageDlg('자료를 삭제하시겠습니까 ?',mtConfirmation,mbOkCancel,0)=mrOK Then begin

  Sqlen := 'DELETE FROM Gg_Megn WHERE Gubun=''@Gubun'' and Gname=''@Gname''';
  Translate(Sqlen, '@Gubun', lSqry.FieldByName('Gubun').AsString);
  Translate(Sqlen, '@Gname', lSqry.FieldByName('Gname').AsString);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

  lSqry.Delete;

  end;
end;

procedure TSeen11.SpeedButton3Click(Sender: TObject);
begin
  FontDialog1.Font := SpeedButton3.Font;
  FontDialog1.Execute;
  SpeedButton3.Font := FontDialog1.Font;
end;

procedure TSeen11.SpeedButton4Click(Sender: TObject);
begin

  Sqlen := 'UPDATE Gg_Megn SET '+
  'Gname=''@Gname'',Gnumb=  @Gnumb '+
  'WHERE Gubun=''@Gubun'' and Gfild=''@Gfild''';

  Translate(Sqlen, '@Gubun', nPrnt);
  Translate(Sqlen, '@Gname', lSqry.FieldByName('Gname').AsString);
  Translate(Sqlen, '@Gfild', lSqry.FieldByName('Gfild').AsString);
  Translate(Sqlen, '@Gnumb', lSqry.FieldByName('Gnumb').Value);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

end;

procedure TSeen11.Button1Click(Sender: TObject);
var
  DBTitle,DBField,St1: String;
begin
  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

  St1:='Gubun'+'='+#39+nPrnt+#39;

  Sqlen := 'Select Gubun,Gname,Gfild,Gnumb From Gg_Megn Where '+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  With Tong60.frReport00_00 do begin
    Clear;
    LoadFromFile(GetExecPath + 'Report\Report_1_11.frf');
    FindObject('Memo11').Visible:=False;
    FindObject('Memo12').Visible:=False;
    FindObject('Memo13').Visible:=False;
    FindObject('Memo14').Visible:=False;
    FindObject('Memo15').Visible:=False;
    FindObject('Memo16').Visible:=False;
    FindObject('Memo17').Visible:=False;
    FindObject('Memo18').Visible:=False;
    FindObject('Memo19').Visible:=False;
    FindObject('Memo21').Visible:=False;
    FindObject('Memo22').Visible:=False;
    FindObject('Memo23').Visible:=False;
    FindObject('Memo24').Visible:=False;
    FindObject('Memo25').Visible:=False;
    FindObject('Memo26').Visible:=False;
    FindObject('Memo27').Visible:=False;
    FindObject('Memo28').Visible:=False;
    FindObject('Memo29').Visible:=False;
  end;

  PSumX := 20;
  PSumY := 1;
  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    case PSumY of
      1: begin
           DBTitle := 'Memo11';
           DBField := 'Memo21';
         end;
      2: begin
           DBTitle := 'Memo12';
           DBField := 'Memo22';
         end;
      3: begin
           DBTitle := 'Memo13';
           DBField := 'Memo23';
         end;
      4: begin
           DBTitle := 'Memo14';
           DBField := 'Memo24';
         end;
      5: begin
           DBTitle := 'Memo15';
           DBField := 'Memo25';
         end;
      6: begin
           DBTitle := 'Memo16';
           DBField := 'Memo26';
         end;
      7: begin
           DBTitle := 'Memo17';
           DBField := 'Memo27';
         end;
      8: begin
           DBTitle := 'Memo18';
           DBField := 'Memo28';
         end;
      9: begin
           DBTitle := 'Memo19';
           DBField := 'Memo29';
         end;
    end;

    With Tong60.frReport00_00 do begin
      FindObject(DBTitle).SetBounds(PSumX,244,StrToIntDef(SGrid.Cells[ 3,List1],0),19);
      FindObject(DBField).SetBounds(PSumX,296,StrToIntDef(SGrid.Cells[ 3,List1],0),19);
      FindObject(DBTitle).Memo.Text:=    SGrid.Cells[ 1,List1];
      FindObject(DBField).Memo.Text:='['+SGrid.Cells[ 2,List1]+']';

      FindObject(DBTitle).Prop['Font.Color']:=SpeedButton3.Font.Color;
      FindObject(DBTitle).Prop['Font.Size']:=SpeedButton3.Font.Size;
      FindObject(DBTitle).Prop['Font.Name']:=SpeedButton3.Font.Name;

      FindObject(DBField).Prop['Font.Color']:=SpeedButton3.Font.Color;
      FindObject(DBField).Prop['Font.Size']:=SpeedButton3.Font.Size;
      FindObject(DBField).Prop['Font.Name']:=SpeedButton3.Font.Name;

      FindObject(DBTitle).Visible:=True;
      FindObject(DBField).Visible:=True;
    end;

    if PSumY=1 Then
    PSumX := StrToIntDef(SGrid.Cells[ 3,List1],0)+30 else
    PSumX := 10+PSumX+StrToIntDef(SGrid.Cells[ 3,List1],0);
    PSumY := PSumY+1;

  end;

  if nPrnt='11' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub11;
  if nPrnt='12' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub21;
  if nPrnt='13' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub31;
  if nPrnt='14' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub41;
  if nPrnt='15' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub51;

  With Tong60.frReport00_00 do begin
    FindObject('Memo91').Memo.Text:=mPrnt;
    FindObject('Memo00').Memo.Text:=TitleEdit.Text;
    FindObject('Memo00').Prop['Font.Color']:=SpeedButton0.Font.Color;
    FindObject('Memo00').Prop['Font.Size']:=SpeedButton0.Font.Size;
    FindObject('Memo00').Prop['Font.Name']:=SpeedButton0.Font.Name;
    if PrepareReport then
    PrintPreparedReport(' ',1,true, frall);
  end;
  oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
end;

procedure TSeen11.Button2Click(Sender: TObject);
var
  DBTitle,DBField,St1: String;
begin
  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;

  St1:='Gubun'+'='+#39+nPrnt+#39;

  Sqlen := 'Select Gubun,Gname,Gfild,Gnumb From Gg_Megn Where '+St1;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  With Tong60.frReport00_00 do begin
    Clear;
    LoadFromFile(GetExecPath + 'Report\Report_1_11.frf');
    FindObject('Memo11').Visible:=False;
    FindObject('Memo12').Visible:=False;
    FindObject('Memo13').Visible:=False;
    FindObject('Memo14').Visible:=False;
    FindObject('Memo15').Visible:=False;
    FindObject('Memo16').Visible:=False;
    FindObject('Memo17').Visible:=False;
    FindObject('Memo18').Visible:=False;
    FindObject('Memo19').Visible:=False;
    FindObject('Memo21').Visible:=False;
    FindObject('Memo22').Visible:=False;
    FindObject('Memo23').Visible:=False;
    FindObject('Memo24').Visible:=False;
    FindObject('Memo25').Visible:=False;
    FindObject('Memo26').Visible:=False;
    FindObject('Memo27').Visible:=False;
    FindObject('Memo28').Visible:=False;
    FindObject('Memo29').Visible:=False;
  end;

  PSumX := 20;
  PSumY := 1;
  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;
    case PSumY of
      1: begin
           DBTitle := 'Memo11';
           DBField := 'Memo21';
         end;
      2: begin
           DBTitle := 'Memo12';
           DBField := 'Memo22';
         end;
      3: begin
           DBTitle := 'Memo13';
           DBField := 'Memo23';
         end;
      4: begin
           DBTitle := 'Memo14';
           DBField := 'Memo24';
         end;
      5: begin
           DBTitle := 'Memo15';
           DBField := 'Memo25';
         end;
      6: begin
           DBTitle := 'Memo16';
           DBField := 'Memo26';
         end;
      7: begin
           DBTitle := 'Memo17';
           DBField := 'Memo27';
         end;
      8: begin
           DBTitle := 'Memo18';
           DBField := 'Memo28';
         end;
      9: begin
           DBTitle := 'Memo19';
           DBField := 'Memo29';
         end;
    end;

    With Tong60.frReport00_00 do begin
      FindObject(DBTitle).SetBounds(PSumX,244,StrToIntDef(SGrid.Cells[ 3,List1],0),19);
      FindObject(DBField).SetBounds(PSumX,296,StrToIntDef(SGrid.Cells[ 3,List1],0),19);
      FindObject(DBTitle).Memo.Text:=    SGrid.Cells[ 1,List1];
      FindObject(DBField).Memo.Text:='['+SGrid.Cells[ 2,List1]+']';

      FindObject(DBTitle).Prop['Font.Color']:=SpeedButton3.Font.Color;
      FindObject(DBTitle).Prop['Font.Size']:=SpeedButton3.Font.Size;
      FindObject(DBTitle).Prop['Font.Name']:=SpeedButton3.Font.Name;

      FindObject(DBField).Prop['Font.Color']:=SpeedButton3.Font.Color;
      FindObject(DBField).Prop['Font.Size']:=SpeedButton3.Font.Size;
      FindObject(DBField).Prop['Font.Name']:=SpeedButton3.Font.Name;

      FindObject(DBTitle).Visible:=True;
      FindObject(DBField).Visible:=True;
    end;

    if PSumY=1 Then
    PSumX := StrToIntDef(SGrid.Cells[ 3,List1],0)+30 else
    PSumX := 10+PSumX+StrToIntDef(SGrid.Cells[ 3,List1],0);
    PSumY := PSumY+1;

  end;

  if nPrnt='11' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub11;
  if nPrnt='12' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub21;
  if nPrnt='13' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub31;
  if nPrnt='14' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub41;
  if nPrnt='15' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub51;
  if nPrnt='17' Then Tong60.frDBDataSet00_00.Dataset:=Base10.T1_Sub71;

  With Tong60.frReport00_00 do begin
    FindObject('Memo91').Memo.Text:=mPrnt;
    FindObject('Memo00').Memo.Text:=TitleEdit.Text;
    FindObject('Memo00').Prop['Font.Color']:=SpeedButton0.Font.Color;
    FindObject('Memo00').Prop['Font.Size']:=SpeedButton0.Font.Size;
    FindObject('Memo00').Prop['Font.Name']:=SpeedButton0.Font.Name;
    ShowReport;
  end;
  oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
end;

procedure TSeen11.Button3Click(Sender: TObject);
begin
  PrinterSetupDialog1.Execute;
end;

procedure TSeen11.Button4Click(Sender: TObject);
begin
  Close;
end;

procedure TSeen11.DBGrid1KeyPress(Sender: TObject; var Key: Char);
begin
  if lSqry.Active=True Then
  if Key=#13 Then SpeedButton4Click(Self);
end;

procedure TSeen11.DBGrid1KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

end.
