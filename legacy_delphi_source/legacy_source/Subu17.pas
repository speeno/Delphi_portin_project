unit Subu17;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, TFlatCheckBoxUnit,
  RxRichEd, ToolWin, ImgList, ZQuery, ZMySqlQuery, dxCore, dxButtons,
  CornerButton;

type
  TSobo17 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel003: TFlatPanel;
    Panel004: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    Panel100: TFlatPanel;
    Panel101: TFlatPanel;
    Panel103: TFlatPanel;
    Panel102: TFlatPanel;
    Panel105: TFlatPanel;
    Panel106: TFlatPanel;
    Panel107: TFlatPanel;
    Panel109: TFlatPanel;
    Panel108: TFlatPanel;
    Panel110: TFlatPanel;
    Panel112: TFlatPanel;
    Panel114: TFlatPanel;
    Panel111: TFlatPanel;
    Panel116: TFlatPanel;
    Panel119: TFlatPanel;
    Panel200: TFlatPanel;
    Panel201: TFlatPanel;
    Panel202: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    DBGrid101: TDBGrid;
    DBGrid201: TDBGrid;
    Button104: TFlatButton;
    Button201: TFlatButton;
    Button202: TFlatButton;
    Button203: TFlatButton;
    Label100: TmyLabel3d;
    Label108: TmyLabel3d;
    Label109: TmyLabel3d;
    Label110: TmyLabel3d;
    Label200: TmyLabel3d;
    Edit101: TFlatComboBox;
    Edit102: TFlatEdit;
    Edit103: TFlatEdit;
    Edit104: TFlatEdit;
    Edit105: TFlatEdit;
    Edit106: TFlatEdit;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Edit109: TFlatEdit;
    Edit110: TFlatEdit;
    Edit111: TFlatEdit;
    Edit112: TFlatEdit;
    Edit113: TFlatEdit;
    Edit114: TFlatEdit;
    Edit115: TFlatEdit;
    Edit116: TFlatEdit;
    Edit117: TFlatEdit;
    Edit118: TFlatEdit;
    Edit201: TFlatEdit;
    Edit202: TFlatEdit;
    Panel118: TFlatPanel;
    Edit119: TFlatNumber;
    Label101: TmyLabel3d;
    Label102: TmyLabel3d;
    Edit120: TFlatNumber;
    Label103: TmyLabel3d;
    Edit121: TFlatNumber;
    Label104: TmyLabel3d;
    Edit122: TFlatNumber;
    Panel123: TFlatPanel;
    CheckBox1: TFlatCheckBox;
    Panel124: TFlatPanel;
    Edit124: TFlatComboBox;
    Panel125: TFlatPanel;
    Panel300: TFlatPanel;
    Panel311: TFlatPanel;
    Panel312: TFlatPanel;
    Panel321: TFlatPanel;
    Panel331: TFlatPanel;
    Panel341: TFlatPanel;
    Panel351: TFlatPanel;
    Panel352: TFlatPanel;
    Panel411: TFlatPanel;
    Panel412: TFlatPanel;
    Panel421: TFlatPanel;
    Panel422: TFlatPanel;
    Panel431: TFlatPanel;
    Panel432: TFlatPanel;
    Panel441: TFlatPanel;
    Panel442: TFlatPanel;
    Panel451: TFlatPanel;
    Panel452: TFlatPanel;
    Panel511: TFlatPanel;
    Panel512: TFlatPanel;
    Panel521: TFlatPanel;
    Panel531: TFlatPanel;
    Edit311: TFlatNumber;
    Edit321: TFlatNumber;
    Edit331: TFlatNumber;
    Edit341: TFlatNumber;
    Edit411: TFlatNumber;
    Edit412: TFlatNumber;
    Edit421: TFlatNumber;
    Edit422: TFlatNumber;
    Edit431: TFlatNumber;
    Edit432: TFlatNumber;
    Edit441: TFlatNumber;
    Edit442: TFlatNumber;
    Edit451: TFlatNumber;
    Edit452: TFlatNumber;
    Edit511: TFlatNumber;
    Edit521: TFlatNumber;
    Edit531: TFlatNumber;
    Edit541: TFlatNumber;
    Edit551: TFlatNumber;
    Panel332: TFlatPanel;
    RadioButton331: TRadioButton;
    RadioButton332: TRadioButton;
    Panel342: TFlatPanel;
    RadioButton341: TRadioButton;
    RadioButton342: TRadioButton;
    Panel353: TFlatPanel;
    RadioButton351: TRadioButton;
    RadioButton352: TRadioButton;
    Panel413: TFlatPanel;
    RadioButton411: TRadioButton;
    RadioButton412: TRadioButton;
    Panel423: TFlatPanel;
    RadioButton421: TRadioButton;
    RadioButton422: TRadioButton;
    Panel433: TFlatPanel;
    RadioButton431: TRadioButton;
    RadioButton432: TRadioButton;
    Panel443: TFlatPanel;
    RadioButton441: TRadioButton;
    RadioButton442: TRadioButton;
    Panel453: TFlatPanel;
    RadioButton451: TRadioButton;
    RadioButton452: TRadioButton;
    Panel513: TFlatPanel;
    RadioButton511: TRadioButton;
    RadioButton512: TRadioButton;
    Panel522: TFlatPanel;
    RadioButton521: TRadioButton;
    RadioButton522: TRadioButton;
    Panel532: TFlatPanel;
    RadioButton531: TRadioButton;
    RadioButton532: TRadioButton;
    Panel542: TFlatPanel;
    RadioButton541: TRadioButton;
    RadioButton542: TRadioButton;
    Panel553: TFlatPanel;
    RadioButton551: TRadioButton;
    RadioButton552: TRadioButton;
    StBar101: TStatusBar;
    Panel301: TFlatPanel;
    Label301: TmyLabel3d;
    Panel302: TFlatPanel;
    Label302: TmyLabel3d;
    Edit123: TFlatMaskEdit;
    Panel126: TFlatPanel;
    Edit125: TFlatEdit;
    Edit126: TFlatEdit;
    CheckBox2: TFlatCheckBox;
    CheckBox3: TFlatCheckBox;
    Panel613: TFlatPanel;
    RadioButton611: TRadioButton;
    RadioButton612: TRadioButton;
    Edit611: TFlatNumber;
    Panel612: TFlatPanel;
    Edit612: TFlatNumber;
    Panel621: TFlatPanel;
    Panel622: TFlatPanel;
    Edit621: TFlatNumber;
    Edit622: TFlatNumber;
    Panel623: TFlatPanel;
    RadioButton621: TRadioButton;
    RadioButton622: TRadioButton;
    Panel238: TFlatPanel;
    Edit238: TFlatEdit;
    Edit236: TFlatNumber;
    Panel217: TFlatPanel;
    Edit127_: TFlatEdit;
    Edit127: TFlatComboBox;
    FlatPanel1: TFlatPanel;
    Label304: TmyLabel3d;
    FlatPanel2: TFlatPanel;
    Label303: TmyLabel3d;
    Edit561: TFlatNumber;
    Edit571: TFlatNumber;
    Edit581: TFlatNumber;
    FlatPanel11: TFlatPanel;
    RadioButton561: TRadioButton;
    RadioButton562: TRadioButton;
    FlatPanel13: TFlatPanel;
    RadioButton571: TRadioButton;
    RadioButton572: TRadioButton;
    FlatPanel14: TFlatPanel;
    RadioButton581: TRadioButton;
    RadioButton582: TRadioButton;
    FlatPanel3: TFlatPanel;
    FlatPanel4: TFlatPanel;
    FlatPanel5: TFlatPanel;
    FlatPanel6: TFlatPanel;
    FlatPanel7: TFlatPanel;
    FlatPanel8: TFlatPanel;
    FlatPanel9: TFlatPanel;
    FlatPanel15: TFlatPanel;
    FlatPanel16: TFlatPanel;
    FlatPanel17: TFlatPanel;
    FlatPanel18: TFlatPanel;
    FlatPanel19: TFlatPanel;
    Edit591: TFlatNumber;
    FlatPanel20: TFlatPanel;
    RadioButton591: TRadioButton;
    RadioButton592: TRadioButton;
    FlatPanel21: TFlatPanel;
    FlatPanel10: TFlatPanel;
    FlatPanel12: TFlatPanel;
    Edit491: TFlatNumber;
    FlatPanel22: TFlatPanel;
    RadioButton491: TRadioButton;
    RadioButton492: TRadioButton;
    FlatPanel23: TFlatPanel;
    FlatPanel24: TFlatPanel;
    FlatPanel25: TFlatPanel;
    Edit481: TFlatNumber;
    FlatPanel26: TFlatPanel;
    RadioButton481: TRadioButton;
    RadioButton482: TRadioButton;
    Panel701: TFlatPanel;
    Panel702: TFlatPanel;
    ToolbarImages: TImageList;
    Button302: TFlatButton;
    Button701: TFlatButton;
    Button702: TFlatButton;
    Editor: TRxRichEdit;
    FontDialog1: TFontDialog;
    ToolBar1: TToolBar;
    ToolButton10: TToolButton;
    FontName: TComboBox;
    ToolButton11: TToolButton;
    FontSize: TEdit;
    UpDown1: TUpDown;
    ToolBar2: TToolBar;
    UndoButton: TToolButton;
    ToolButton1: TToolButton;
    BoldButton: TToolButton;
    ItalicButton: TToolButton;
    UnderlineButton: TToolButton;
    ToolButton16: TToolButton;
    StandardToolBar: TToolBar;
    ToolButton3: TToolButton;
    LeftAlign: TToolButton;
    CenterAlign: TToolButton;
    RightAlign: TToolButton;
    ToolButton20: TToolButton;
    BulletsButton: TToolButton;
    Query0: TZMySqlQuery;
    Button301: TFlatButton;
    FlatPanel27: TFlatPanel;
    Label305: TmyLabel3d;
    Edit592: TFlatNumber;
    CornerButton2: TCornerButton;
    CornerButton3: TCornerButton;
    CornerButton4: TCornerButton;
    Label002: TmyLabel3d;
    Label003: TmyLabel3d;
    Label309: TmyLabel3d;
    Button000: TdxButton;
    Button101: TdxButton;
    Button102: TdxButton;
    Button103: TdxButton;
    FlatPanel28: TFlatPanel;
    Label901: TmyLabel3d;
    Label902: TmyLabel3d;
    Edit901: TFlatComboBox;
    Edit902: TFlatComboBox;
    Label903: TmyLabel3d;
    Label107: TmyLabel3d;
    Edit128: TFlatEdit;
    procedure FontNameChange(Sender: TObject);
    procedure FontSizeChange(Sender: TObject);
    procedure BoldButtonClick(Sender: TObject);
    procedure ItalicButtonClick(Sender: TObject);
    procedure UnderlineButtonClick(Sender: TObject);
    procedure LeftAlignClick(Sender: TObject);
    procedure CenterAlignClick(Sender: TObject);
    procedure RightAlignClick(Sender: TObject);
    procedure BulletsButtonClick(Sender: TObject);
    procedure UndoButtonClick(Sender: TObject);
    procedure FormPaint(Sender: TObject);
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
    procedure Button102Click(Sender: TObject);
    procedure Button103Click(Sender: TObject);
    procedure Button104Click(Sender: TObject);
    procedure Button201Click(Sender: TObject);
    procedure Button202Click(Sender: TObject);
    procedure Button203Click(Sender: TObject);
    procedure Edit101Exit(Sender: TObject);
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
    procedure Edit115KeyPress(Sender: TObject; var Key: Char);
    procedure Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101Enter(Sender: TObject);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101Exit(Sender: TObject);
    procedure DBGrid201Exit(Sender: TObject);
    procedure DBGrid101TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure SeachClick(Str1,Str2: String);
    procedure FormCreate(Sender: TObject);
    procedure RadioButtonClick(Sender: TObject);
    procedure Button300Click(Sender: TObject);
    procedure Button301Click(Sender: TObject);
    procedure Button302Click(Sender: TObject);
    procedure Button700Click(Sender: TObject);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure DBGrid101DblClick(Sender: TObject);
  private
    { Private declarations }
    procedure AnyMessage(var Msg: TMsg; var Handled: Boolean);
    function CurrText: TRxTextAttributes;
    procedure GetFontNames;
  public
    procedure SetData2nSql(Sqlen: string);
  end;

var
  Sobo17: TSobo17;

implementation

{$R *.DFM}

uses Chul, Base01, Subu19, Tong02, Tong04, TcpLib, Subu40,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

function TSobo17.CurrText: TRxTextAttributes;
begin
  if Editor.SelLength > 0 then Result := Editor.SelAttributes
  else Result := Editor.WordAttributes;
end;

function EnumFontsProc(var LogFont: TLogFont; var TextMetric: TTextMetric;
  FontType: Integer; Data: Pointer): Integer; stdcall;
begin
  TStrings(Data).Add(LogFont.lfFaceName);
  Result := 1;
end;

procedure TSobo17.GetFontNames;
var
  DC: HDC;
begin
  DC := GetDC(0);
  EnumFonts(DC, nil, @EnumFontsProc, Pointer(FontName.Items));
  ReleaseDC(0, DC);
  FontName.Sorted := True;
end;

procedure TSobo17.FontNameChange(Sender: TObject);
begin
//if FUpdating then Exit;
  CurrText.Name := FontName.Items[FontName.ItemIndex];
end;

procedure TSobo17.FontSizeChange(Sender: TObject);
begin
//if FUpdating then Exit;
  CurrText.Size := StrToInt(FontSize.Text);
end;

procedure TSobo17.BoldButtonClick(Sender: TObject);
begin
//if FUpdating then Exit;
  if BoldButton.Down then
    CurrText.Style := CurrText.Style + [fsBold]
  else
    CurrText.Style := CurrText.Style - [fsBold];
end;

procedure TSobo17.ItalicButtonClick(Sender: TObject);
begin
//if FUpdating then Exit;
  if ItalicButton.Down then
    CurrText.Style := CurrText.Style + [fsItalic]
  else
    CurrText.Style := CurrText.Style - [fsItalic];
end;

procedure TSobo17.UnderlineButtonClick(Sender: TObject);
begin
//if FUpdating then Exit;
  if UnderlineButton.Down then
    CurrText.Style := CurrText.Style + [fsUnderline]
  else
    CurrText.Style := CurrText.Style - [fsUnderline];
end;

procedure TSobo17.LeftAlignClick(Sender: TObject);
begin
//if FUpdating then Exit;
  Editor.Paragraph.Alignment := TParaAlignment(TComponent(Sender).Tag);
end;

procedure TSobo17.CenterAlignClick(Sender: TObject);
begin
//if FUpdating then Exit;
  Editor.Paragraph.Alignment := TParaAlignment(TComponent(Sender).Tag);
end;

procedure TSobo17.RightAlignClick(Sender: TObject);
begin
//if FUpdating then Exit;
  Editor.Paragraph.Alignment := TParaAlignment(TComponent(Sender).Tag);
end;

procedure TSobo17.BulletsButtonClick(Sender: TObject);
begin
//if FUpdating then Exit;
  Editor.Paragraph.Numbering := TRxNumbering(BulletsButton.Down);
end;

procedure TSobo17.UndoButtonClick(Sender: TObject);
begin
  FontDialog1.Font.Assign(Editor.SelAttributes);
  if FontDialog1.Execute then
    CurrText.Assign(FontDialog1.Font);
//SelectionChange(Self);
  Editor.SetFocus;
end;

procedure TSobo17.FormPaint(Sender: TObject);
begin
{ Button023Click(Self);
  Button024Click(Self); }
  Sobo17.OnPaint:=Nil;
  Sobo17.OnShow:=FormShow;
  FormShow(Self);
end;

procedure TSobo17.FormActivate(Sender: TObject);
begin
  nForm:='17';
  nSqry:=Base10.T1_Sub71;
  mSqry:=Base10.T1_Sub72;
end;

procedure TSobo17.FormShow(Sender: TObject);
begin
  GetFontNames;
  FontSize.Text := '10';
//FontSize.Text := IntToStr(Editor.SelAttributes.Size);
  FontName.Text := Editor.SelAttributes.Name;

  Edit311.Height:=35;
  Edit321.Height:=35;
  Edit331.Height:=35;
  Edit341.Height:=35;
  Edit481.Height:=35;
  Edit491.Height:=35;
  Edit511.Height:=35;
  Edit521.Height:=35;
  Edit531.Height:=35;
  Edit541.Height:=35;
  Edit551.Height:=35;
  Edit561.Height:=35;
  Edit571.Height:=35;
  Edit581.Height:=35;
  Edit591.Height:=35;
  Edit622.Height:=35;

  SeachClick('','');
{ Application.CreateForm(TSobo19, Sobo19);
  Sobo19.ShowModal;
  Sobo19.Edit100.ItemIndex:=Sobo19.Edit000.ItemIndex;
  SeachClick(Sobo19.Edit100.Text,Sobo19.Edit101.Text);
  Sobo19.Free; }
end;

procedure TSobo17.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo17:=nil;
  nSqry.AfterScroll:=nil;
  mSqry.AfterScroll:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);

{ Base10.OpenShow(Base10.G7_Ggeo);
  Sqlen := 'Select Hcode,Gcode,Gname,Chek1,Chek2 From G7_Ggeo Where '+D_Open;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Base10.G7_Ggeo)
  else ShowMessage(E_Open); }
end;

procedure TSobo17.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo17.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_11_01(Self);
  end;
end;

procedure TSobo17.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo17.Button004Click(Sender: TObject);
begin
  nSqry.Edit;
  if(nSqry.FieldByName('Ocode').AsString='1')then
     nSqry.FieldByName('Ocode').AsString:=''
  else
  if(nSqry.FieldByName('Ocode').AsString='')then
     nSqry.FieldByName('Ocode').AsString:='1';
  nSqry.Post;

  Edit104.Text:=nSqry.FieldByName('Ocode').AsString;

  Sqlen := 'UPDATE G7_Ggeo SET Ocode=''@Ocode'' '+
           'WHERE Gcode=''@Gcode''';
  Translate(Sqlen, '@Ocode', nSqry.FieldByName('Ocode').AsString);
  Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
end;

procedure TSobo17.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX0(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo17.Button013Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX0(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo17.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('17-01');
end;

procedure TSobo17.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('17-01');
end;

procedure TSobo17.Button016Click(Sender: TObject);
begin
  Tong40.print_17_01(Self);
end;

procedure TSobo17.Button017Click(Sender: TObject);
begin
  Tong40.print_17_02(Self);
end;

procedure TSobo17.Button018Click(Sender: TObject);
begin
  Tong40.print_17_03(Self);
end;

procedure TSobo17.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo17.Button022Click(Sender: TObject);
begin
  nSqry.SaveToFile('.\Data\G7_Ggeo.cds');
end;

procedure TSobo17.Button023Click(Sender: TObject);
begin
  Edit101.Text := nSqry.FieldByName('Sname').AsString;
  Edit102.Text := nSqry.FieldByName('Jubun').AsString;
  Edit103.Text := nSqry.FieldByName('Gcode').AsString;
  Edit104.Text := nSqry.FieldByName('Ocode').AsString;
  Edit105.Text := nSqry.FieldByName('Gname').AsString;
  Edit106.Text := nSqry.FieldByName('Gposa').AsString;
  Edit107.Text := nSqry.FieldByName('Gnumb').AsString;
  Edit108.Text := nSqry.FieldByName('Guper').AsString;
  Edit109.Text := nSqry.FieldByName('Gjomo').AsString;
  Edit110.Text := nSqry.FieldByName('Gpper').AsString;
  Edit111.Text := nSqry.FieldByName('Gpost').AsString;
  Edit112.Text := nSqry.FieldByName('Gtel1').AsString;
  Edit113.Text := nSqry.FieldByName('Gtel2').AsString;
  Edit114.Text := nSqry.FieldByName('Gfax1').AsString;
  Edit115.Text := nSqry.FieldByName('Gfax2').AsString;
  Edit116.Text := nSqry.FieldByName('Gadd1').AsString;
  Edit117.Text := nSqry.FieldByName('Gadd2').AsString;
  Edit127.Text := nSqry.FieldByName('Bigo2').AsString;
  Edit128.Text := nSqry.FieldByName('Gnum1').AsString;
  Edit118.Text := nSqry.FieldByName('Gbigo').AsString;
//Edit119.Value:= nSqry.FieldByName('Giqut').AsFloat;
//Edit120.Value:= nSqry.FieldByName('Gisum').AsFloat;
//Edit124.ItemIndex:= nSqry.FieldByName('Gosum').AsInteger;
  Edit122.Value:= nSqry.FieldByName('Gssum').AsFloat;
  Edit123.Text := nSqry.FieldByName('Gdate').AsString;
  Edit125.Text := nSqry.FieldByName('Name1').AsString;
  Edit126.Text := nSqry.FieldByName('Name2').AsString;
  if nSqry.FieldByName('Jumin').AsString='True' then
  CheckBox1.Checked:=True else
  CheckBox1.Checked:=False;
  if nSqry.FieldByName('Chek1').AsString='True' then
  CheckBox2.Checked:=True else
  CheckBox2.Checked:=False;
  if nSqry.FieldByName('Chek2').AsString='True' then
  CheckBox3.Checked:=True else
  CheckBox3.Checked:=False;
end;

procedure TSobo17.Button024Click(Sender: TObject);
begin
  Edit201.Text := mSqry.FieldByName('Gcode').AsString;
  Edit202.Text := mSqry.FieldByName('Gname').AsString;
end;

procedure TSobo17.Button101Click(Sender: TObject);
begin
  if nSqry.State=dsInsert Then Button102Click(Self);
  nSqry.Insert;
  nSqry.FieldByName('Gcode').AsString := '';
  Edit101.SetFocus;
  Edit103.Enabled:=True;
end;

procedure TSobo17.Button102Click(Sender: TObject);
var MeDlg: Integer;
    St1,St2: String;
    Sq1,Sq2: String;
begin
MeDlg := MessageDlg('저장 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin
  if Edit103.Enabled=True Then
    Edit101Exit(Self);
  if nSqry.State=dsInsert Then
  begin
    Sqlon := 'INSERT INTO G7_Ggeo '+
    '( Gubun, Jubun, Gcode, Ocode, Gname, Gposa, '+
    '  Gnumb, Guper, Gjomo, Gtel1, Gtel2, Gfax1, Bigo2, '+
    '  Gnum1, Gfax2, Gpost, Gadd1, Gadd2, Gpper, Gbigo, '+
    '  Jumin, Gdate, Name1, Name2, Chek1, Chek2, Gssum ) VALUES ';
    Sq1 :=
    '(''@Gubun'',''@Jubun'',''@Gcode'',''@Ocode'',''@Gname'',''@Gposa'', '+
    ' ''@Gnumb'',''@Guper'',''@Gjomo'',''@Gtel1'',''@Gtel2'',''@Gfax1'',''@Bigo2'', ';
    Sq2 :=
    ' ''@Gnum1'',''@Gfax2'',''@Gpost'',''@Gadd1'',''@Gadd2'',''@Gpper'',''@Gbigo'','+
    ' ''@Jumin'',''@Gdate'',''@Name1'',''@Name2'',''@Chek1'',''@Chek2'',  @Gssum   )';

    St1 := 'Select Gcode From G7_Gbun Where '+D_Select+'Gname = ''@Gname''';
    Translate(St1, '@Gname', Edit101.Text);
    St2 := Base10.Seek_Name(St1);

    Translate(Sq1, '@Gubun', St2);
    Translate(Sq1, '@Jubun', Edit102.Text);
    Translate(Sq1, '@Gcode', Edit103.Text);
    Translate(Sq1, '@Ocode', Edit104.Text);
    Translate(Sq1, '@Gname', Edit105.Text);
    Translate(Sq1, '@Gposa', Edit106.Text);
    Translate(Sq1, '@Gnumb', Edit107.Text);
    Translate(Sq1, '@Guper', Edit108.Text);
    Translate(Sq1, '@Gjomo', Edit109.Text);
    Translate(Sq1, '@Gtel1', Edit112.Text);
    Translate(Sq1, '@Gtel2', Edit113.Text);
    Translate(Sq1, '@Gfax1', Edit114.Text);
    Translate(Sq1, '@Bigo2', Edit127.Text);
    Translate(Sq2, '@Gnum1', Edit128.Text);
    Translate(Sq2, '@Gfax2', Edit115.Text);
    Translate(Sq2, '@Gpost', Edit111.Text);
    Translate(Sq2, '@Gadd1', Edit116.Text);
    Translate(Sq2, '@Gadd2', Edit117.Text);
    Translate(Sq2, '@Gpper', Edit110.Text);
    Translate(Sq2, '@Gbigo', Edit118.Text);
  //TransAuto(Sq2, '@Giqut', FloatToStr(Edit119.Value));
  //TransAuto(Sq2, '@Gisum', FloatToStr(Edit120.Value));
  //TransAuto(Sq2, '@Gosum', FloatToStr(Edit124.ItemIndex));
    TransAuto(Sq2, '@Gssum', FloatToStr(Edit122.Value));
    Translate(Sq2, '@Gdate', Edit123.Text);
    Translate(Sq2, '@Name1', Edit125.Text);
    Translate(Sq2, '@Name2', Edit126.Text);

    if CheckBox1.Checked=True then
    Translate(Sq2, '@Jumin', 'True') else
    Translate(Sq2, '@Jumin', 'False');

    if CheckBox2.Checked=True then
    Translate(Sq2, '@Chek1', 'True') else
    Translate(Sq2, '@Chek1', 'False');

    if CheckBox3.Checked=True then
    Translate(Sq2, '@Chek2', 'True') else
    Translate(Sq2, '@Chek2', 'False');

    Sqlen:=Sqlon+Sq1+Sq2;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Insert);
      nSqry.Cancel;
      DBGrid101.SetFocus;
      Edit103.Enabled:=False;
      Exit;
    end;

    Base10.InSert_ID(nSqry,'G7_GGEO_ID_GEN');
  end else begin

    Sqlon := 'UPDATE G7_Ggeo SET '+
    'Gubun=''@Gubun'',Jubun=''@Jubun'',Gcode=''@Gcode'',Ocode=''@Ocode'', '+
    'Gname=''@Gname'',Gposa=''@Gposa'',Gnumb=''@Gnumb'',Guper=''@Guper'', ';
    Sq1 :=
    'Gjomo=''@Gjomo'',Gtel1=''@Gtel1'',Gtel2=''@Gtel2'',Gfax1=''@Gfax1'', '+
    'Gfax2=''@Gfax2'',Gpost=''@Gpost'',Gadd1=''@Gadd1'',Gadd2=''@Gadd2'',Bigo2=''@Bigo2'', ';
    Sq2 :=
    'Gnum1=''@Gnum1'',Gpper=''@Gpper'',Gbigo=''@Gbigo'',Jumin=''@Jumin'',Gdate=''@Gdate'', '+
    'Name1=''@Name1'',Name2=''@Name2'',Chek1=''@Chek1'',Chek2=''@Chek2'',Gssum=  @Gssum    '+
    'WHERE Gcode=''@Gcode''';

    St1 := 'Select Gcode From G7_Gbun Where '+D_Select+'Gname = ''@Gname''';
    Translate(St1, '@Gname', Edit101.Text);
    St2 := Base10.Seek_Name(St1);

    Translate(Sqlon, '@Gubun', St2);
    Translate(Sqlon, '@Jubun', Edit102.Text);
    Translate(Sqlon, '@Gcode', Edit103.Text);
    Translate(Sqlon, '@Ocode', Edit104.Text);
    Translate(Sqlon, '@Gname', Edit105.Text);
    Translate(Sqlon, '@Gposa', Edit106.Text);
    Translate(Sqlon, '@Gnumb', Edit107.Text);
    Translate(Sqlon, '@Guper', Edit108.Text);
    Translate(Sq1, '@Gjomo', Edit109.Text);
    Translate(Sq1, '@Gtel1', Edit112.Text);
    Translate(Sq1, '@Gtel2', Edit113.Text);
    Translate(Sq1, '@Gfax1', Edit114.Text);
    Translate(Sq1, '@Gfax2', Edit115.Text);
    Translate(Sq1, '@Gpost', Edit111.Text);
    Translate(Sq1, '@Gadd1', Edit116.Text);
    Translate(Sq1, '@Gadd2', Edit117.Text);
    Translate(Sq1, '@Bigo2', Edit127.Text);
    Translate(Sq2, '@Gnum1', Edit128.Text);
    Translate(Sq2, '@Gpper', Edit110.Text);
    Translate(Sq2, '@Gbigo', Edit118.Text);
  //TransAuto(Sq2, '@Giqut', FloatToStr(Edit119.Value));
  //TransAuto(Sq2, '@Gisum', FloatToStr(Edit120.Value));
  //TransAuto(Sq2, '@Gosum', FloatToStr(Edit124.ItemIndex));
    TransAuto(Sq2, '@Gssum', FloatToStr(Edit122.Value));
    Translate(Sq2, '@Gdate', Edit123.Text);
    Translate(Sq2, '@Name1', Edit125.Text);
    Translate(Sq2, '@Name2', Edit126.Text);
    Translate(Sq2, '@Gcode', Edit103.Text);

    if CheckBox1.Checked=True then
    Translate(Sq2, '@Jumin', 'True') else
    Translate(Sq2, '@Jumin', 'False');

    if CheckBox2.Checked=True then
    Translate(Sq2, '@Chek1', 'True') else
    Translate(Sq2, '@Chek1', 'False');

    if CheckBox3.Checked=True then
    Translate(Sq2, '@Chek2', 'True') else
    Translate(Sq2, '@Chek2', 'False');

    Sqlen:=Sqlon+Sq1+Sq2;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Update);
      nSqry.Cancel;
      DBGrid101.SetFocus;
      Edit103.Enabled:=False;
      Exit;
    end;

  end;

  St1 := 'Select Gcode From G7_Gbun Where '+D_Select+'Gname = ''@Gname''';
  Translate(St1, '@Gname', Edit101.Text);
  St2 := Base10.Seek_Name(St1);

  nSqry.Edit;
  nSqry.FieldByName('Gubun').AsString := St2;
  nSqry.FieldByName('Sname').AsString := Edit101.Text;
  nSqry.FieldByName('Jubun').AsString := Edit102.Text;
  nSqry.FieldByName('Gcode').AsString := Edit103.Text;
  nSqry.FieldByName('Ocode').AsString := Edit104.Text;
  nSqry.FieldByName('Gname').AsString := Edit105.Text;
  nSqry.FieldByName('Gposa').AsString := Edit106.Text;
  nSqry.FieldByName('Gnumb').AsString := Edit107.Text;
  nSqry.FieldByName('Guper').AsString := Edit108.Text;
  nSqry.FieldByName('Gjomo').AsString := Edit109.Text;
  nSqry.FieldByName('Gpper').AsString := Edit110.Text;
  nSqry.FieldByName('Gpost').AsString := Edit111.Text;
  nSqry.FieldByName('Gtel1').AsString := Edit112.Text;
  nSqry.FieldByName('Gtel2').AsString := Edit113.Text;
  nSqry.FieldByName('Gtels').AsString := Edit112.Text+'-'+Edit113.Text;
  nSqry.FieldByName('Gfax1').AsString := Edit114.Text;
  nSqry.FieldByName('Gfax2').AsString := Edit115.Text;
  nSqry.FieldByName('Gfaxs').AsString := Edit114.Text+'-'+Edit115.Text;
  nSqry.FieldByName('Gadd1').AsString := Edit116.Text;
  nSqry.FieldByName('Gadd2').AsString := Edit117.Text;
  nSqry.FieldByName('Bigo2').AsString := Edit127.Text;
  nSqry.FieldByName('Gnum1').AsString := Edit128.Text;
  nSqry.FieldByName('Gadds').AsString := Edit116.Text+' '+Edit117.Text;
  nSqry.FieldByName('Gbigo').AsString := Edit118.Text;
//nSqry.FieldByName('Giqut').Value    := Edit119.Text;
//nSqry.FieldByName('Gisum').Value    := Edit120.Text;
//nSqry.FieldByName('Gosum').Value    := Edit124.ItemIndex;
  nSqry.FieldByName('Gssum').Value    := Edit122.Text;
  nSqry.FieldByName('Gdate').AsString := Edit123.Text;
  nSqry.FieldByName('Name1').AsString := Edit125.Text;
  nSqry.FieldByName('Name2').AsString := Edit126.Text;
  if CheckBox1.Checked=True then
  nSqry.FieldByName('Jumin').AsString := 'True' else
  nSqry.FieldByName('Jumin').AsString := 'False';
  if CheckBox2.Checked=True then
  nSqry.FieldByName('Chek1').AsString := 'True' else
  nSqry.FieldByName('Chek1').AsString := 'False';
  if CheckBox3.Checked=True then
  nSqry.FieldByName('Chek2').AsString := 'True' else
  nSqry.FieldByName('Chek2').AsString := 'False';
  nSqry.Post;
  DBGrid101.SetFocus;
  Edit103.Enabled:=False;
end;
mrNo: begin
  nSqry.Cancel;
  DBGrid101.SetFocus;
  Edit103.Enabled:=False;
end; end;
end;

procedure TSobo17.Button103Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin

  Sqlen := 'DELETE FROM G7_Ggeo WHERE Gcode=''@Gcode''';
  Translate(Sqlen, '@Gcode', Edit103.Text);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then begin
    ShowMessage(E_Delete);
    DBGrid101.SetFocus;
    Exit;
  end;

  if nSqry.IsEmpty=False Then nSqry.Delete;
  DBGrid101.SetFocus;
  Edit103.Enabled:=False;
end; end;
end;

procedure TSobo17.Button104Click(Sender: TObject);
begin
  Cpost:='17';
  Subu00.Post_Show(Self);
{ if Edit111.Text='' Then begin
  SelectNext(ActiveControl as TWinControl, True, True); Exit; end;
  Seak40.Edit1.Text:=Edit111.Text;
  Seak40.FilterTing(Edit111.Text);
  if Seak40.Query1.IsEmpty=True Then Exit;
  if Seak40.Query1.RecordCount=1 Then begin
     SelectNext(ActiveControl as TWinControl, True, True);
     Edit112.Text:=Seak40.Query1Dddd.Value;
     Edit114.Text:=Seak40.Query1Dddd.Value;
     Edit111.Text:=Seak40.Query1Post.Value;
     Edit116.Text:=Seak40.Query1Addr.Value;
  end else
  if Seak40.ShowModal=mrOK Then begin
     SelectNext(ActiveControl as TWinControl, True, True);
     Edit112.Text:=Seak40.Query1Dddd.Value;
     Edit114.Text:=Seak40.Query1Dddd.Value;
     Edit111.Text:=Seak40.Query1Post.Value;
     Edit116.Text:=Seak40.Query1Addr.Value;
  end; }
end;

procedure TSobo17.Button201Click(Sender: TObject);
begin
  mSqry.Insert;
  mSqry.FieldByName('Gcode').AsString := '';
  Edit201.SetFocus;
end;

procedure TSobo17.Button202Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('저장 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin
  if mSqry.State=dsInsert Then begin

    Sqlen := 'INSERT INTO G7_Gbun ( Gcode, Gname ) VALUES '+
             '(''@Gcode'',''@Gname'')';

    Translate(Sqlen, '@Gcode', Edit201.Text);
    Translate(Sqlen, '@Gname', Edit202.Text);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Insert);
      mSqry.Cancel;
      DBGrid201.SetFocus;
      Exit;
    end;

    Base10.InSert_ID(mSqry,'G7_GBUN_ID_GEN');
  end else begin

    Sqlen := 'UPDATE G7_Gbun SET Gcode=''@Gcode'',Gname=''@Gname'' '+
             'WHERE ID=@ID';

    Translate(Sqlen, '@Gcode', Edit201.Text);
    Translate(Sqlen, '@Gname', Edit202.Text);
    TransAuto(Sqlen, '@ID', mSqry.FieldByName('ID').AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then begin
      ShowMessage(E_Update);
      mSqry.Cancel;
      DBGrid201.SetFocus;
      Exit;
    end;

  end;
  mSqry.Edit;
  mSqry.FieldByName('Gcode').AsString := Edit201.Text;
  mSqry.FieldByName('Gname').AsString := Edit202.Text;
  mSqry.Post;
  DBGrid201.SetFocus;
end;
mrNo: begin
  mSqry.Cancel;
  DBGrid201.SetFocus;
end; end;
end;

procedure TSobo17.Button203Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin

  Sqlen := 'DELETE FROM G7_Gbun WHERE Gcode=''@Gcode''';
  Translate(Sqlen, '@Gcode', Edit201.Text);
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then begin
    ShowMessage(E_Delete);
    DBGrid201.SetFocus;
    Exit;
  end;

  if mSqry.IsEmpty=False Then mSqry.Delete;
  DBGrid201.SetFocus;
end; end;
end;

procedure TSobo17.Edit101Exit(Sender: TObject);
var St1,St2: String;
begin
  if Edit103.Text='' Then begin
    ShowMessage('코드를 입력하세요.');
    Edit103.SetFocus; Exit;
  end else begin
    St1 := 'Select Gcode From G7_Ggeo Where '+D_Select+'Gcode = ''@Gcode''';
    Translate(St1, '@Gcode', Edit103.Text);
    St2 := Base10.Seek_Name(St1);

    if St2<>'' Then begin
    ShowMessage('코드가 이미 등록되어있습니다. 다시 입력하세요.');
    Edit103.SetFocus; Exit;
    end;
  end;
end;

procedure TSobo17.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=06))or
    ((Edit103.Focused=True)and(Edit103.SelStart=05)and(Length(Trim(Edit103.Text))=05))or
    ((Edit104.Focused=True)and(Edit104.SelStart=05)and(Length(Trim(Edit104.Text))=05))or
    ((Edit105.Focused=True)and(Edit105.SelStart=50)and(Length(Trim(Edit105.Text))=50))or
    ((Edit106.Focused=True)and(Edit106.SelStart=30)and(Length(Trim(Edit106.Text))=30))or
    ((Edit107.Focused=True)and(Edit107.SelStart=12)and(Length(Trim(Edit107.Text))=12))or
    ((Edit108.Focused=True)and(Edit108.SelStart=30)and(Length(Trim(Edit108.Text))=30))or
    ((Edit109.Focused=True)and(Edit109.SelStart=30)and(Length(Trim(Edit109.Text))=30))or
    ((Edit110.Focused=True)and(Edit110.SelStart=20)and(Length(Trim(Edit110.Text))=20))or
    ((Edit112.Focused=True)and(Edit112.SelStart=04)and(Length(Trim(Edit112.Text))=04))or
    ((Edit113.Focused=True)and(Edit113.SelStart=20)and(Length(Trim(Edit113.Text))=20))or
    ((Edit114.Focused=True)and(Edit114.SelStart=04)and(Length(Trim(Edit114.Text))=04))or
    ((Edit115.Focused=True)and(Edit115.SelStart=20)and(Length(Trim(Edit115.Text))=20))or
    ((Edit116.Focused=True)and(Edit116.SelStart=90)and(Length(Trim(Edit116.Text))=90))or
    ((Edit117.Focused=True)and(Edit117.SelStart=90)and(Length(Trim(Edit117.Text))=90))or
    ((Edit123.Focused=True)and(Edit123.SelStart=10)and(Length(Trim(Edit123.Text))=10))or
    ((Edit118.Focused=True)and(Edit118.SelStart=50)and(Length(Trim(Edit118.Text))=50))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit111.Focused=True)and(Edit111.SelStart=07)and(Length(Trim(Edit111.Text))=07))Then begin
      Button104Click(Self);
  end;
end;

procedure TSobo17.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo17.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo17.Edit102KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Button102Click(Self);
    DBGrid101.SetFocus;
  end;
end;

procedure TSobo17.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then begin
    Button102Click(Self);
    DBGrid101.SetFocus;
  end;
end;

procedure TSobo17.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo17.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo17.Edit112KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    DGrid: TDBGrid;
    Edits: TFlatComboBox;
begin
  Hands:=Edit101.Handle;
  Edits:=Edit101;
  if Key=#13 Then begin
    if Edits.DropDownCount=9 Then Edits.DropDownCount:=8 else
    if Edits.DropDownCount=8 Then Edits.DropDownCount:=9;
    if Edits.DropDownCount=9 Then begin
      Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
    end else
    if Edits.DropDownCount=8 Then begin
      Key:=#0; SendMessage(Hands, cb_ShowDropDown, 1, 0);
    end;
  end;
end;

procedure TSobo17.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit101;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo17.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Button202Click(Self);
    DBGrid201.SetFocus;
  end;
end;

procedure TSobo17.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then begin
    Button202Click(Self);
    DBGrid201.SetFocus;
  end;
end;

procedure TSobo17.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  if Edit111.Focused=True Then
     Button104Click(Self);
end;

procedure TSobo17.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo17.Edit115KeyPress(Sender: TObject; var Key: Char);
var Hands: THandle;
    DGrid: TDBGrid;
    Edits: TFlatComboBox;
begin
  Hands:=Edit127.Handle;
  Edits:=Edit127;
  if Key=#13 Then begin
    if Edits.DropDownCount=9 Then Edits.DropDownCount:=8 else
    if Edits.DropDownCount=8 Then Edits.DropDownCount:=9;
    if Edits.DropDownCount=9 Then begin
      Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
    end else
    if Edits.DropDownCount=8 Then begin
      Key:=#0; SendMessage(Hands, cb_ShowDropDown, 1, 0);
    end;
  end;
end;

procedure TSobo17.Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var Edits: TFlatComboBox;
begin
  Edits:=Edit127;
  if Edits.DropDownCount=9 Then begin
    if Key=VK_UP   Then begin PerForm(WM_NEXTDLGCTL,1,0); Key:=VK_Cancel; end;
    if Key=VK_DOWN Then begin PerForm(WM_NEXTDLGCTL,0,0); Key:=VK_Cancel; end;
  end;
end;

procedure TSobo17.DBGrid101Enter(Sender: TObject);
begin
  if nSqry.State=dsInsert Then Button102Click(Self);
end;

procedure TSobo17.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo17.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_RETURN Then Edit101.SetFocus;
  if Key=VK_INSERT Then Button101Click(Self);
  if Key=VK_DELETE Then Button103Click(Self);
  end;
end;

procedure TSobo17.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo17.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_RETURN Then Edit201.SetFocus;
  if Key=VK_INSERT Then Button201Click(Self);
  if Key=VK_DELETE Then Button203Click(Self);
  end;
end;

procedure TSobo17.DBGrid101Exit(Sender: TObject);
begin
//
end;

procedure TSobo17.DBGrid201Exit(Sender: TObject);
begin
  Edit101.Items.Clear;
  Sqlen := 'Select * From G7_Gbun Where '+D_Select+' Order By Gcode';
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    List1:=0;
    T00:=Base10.Socket.ClientData('1');
    while List1 < T00-1 do begin
      List1:=List1+1;
      Edit101.Items.Add(Base10.Socket.GetData(List1, 3));
    end;
  end;
end;

procedure TSobo17.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo17.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  if Panel300.Visible=True then
  Button300Click(Self)
  else
  Button700Click(Self);
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo17.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo17.SeachClick(Str1,Str2: String);
var St1: String;
begin
  Tong40.Show;
  Tong40.Update;

  DataSource1.Enabled:=False;

  T00:=0;
  nSqry:=Base10.T1_Sub71;
  mSqry:=Base10.T1_Sub72;

  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);

  St1:=Str1+' Like '+#39+'%'+Str2+'%'+#39;

  if Str2='' then
  St1:=Str1+' = '+#39+''+#39;

  if Str1='' then
  St1:='Gcode'+' Like '+#39+'%'+''+'%'+#39;

  if S_Where2<>'' then
  St1:=S_Where2;

  Sqlen := 'Select * From G7_Ggeo Where '+D_Select+St1+//' Order By Gcode';
           ' Order by field( ocode, '+#39+'x'+#39+'),field( chek5, '+#39+'show1'+#39+'),gcode';
  SetData2nSql(Sqlen);
{
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);
}
  Sqlen := 'Select * From G7_Gbun Where '+D_Open+' Order By Gcode';
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(mSqry)
  else ShowMessage(E_Open);

  mSqry.First;
  Edit101.Items.Clear;
  While mSqry.EOF=False do begin
    Edit101.Items.Add(mSqry.FieldByName('Gname').AsString);
    mSqry.Next;
  end;

  nSqry.First;
  Bmark:=nSqry.GetBookmark; nSqry.DisableControls;
  While nSqry.EOF=False do begin

    St1:=nSqry.FieldByName('Gubun').Value;
    if mSqry.Locate('Gcode',St1,[loCaseInsensitive])=True then
    St1:=mSqry.FieldByName('Gname').Value;

    nSqry.Edit;
    nSqry.FieldByName('Sname').Value:=St1;
    nSqry.FieldByName('Gtels').Value:=nSqry.FieldByName('Gtel1').Value+
                                  '-'+nSqry.FieldByName('Gtel2').Value;
    nSqry.FieldByName('Gfaxs').Value:=nSqry.FieldByName('Gfax1').Value+
                                  '-'+nSqry.FieldByName('Gfax2').Value;
    nSqry.FieldByName('Gadds').Value:=nSqry.FieldByName('Gadd1').Value+
                                  ' '+nSqry.FieldByName('Gadd2').Value;
    nSqry.Post;
    nSqry.Next;
  end;
  nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;

  Edit127.Items.Clear;
  if Hnnnn='000a' then begin
  Sqlen := 'Select distinct Bigo2 From G7_Ggeo '+
           'Where '+D_Select+'Chek5 = ''@Chek5'' '+' and '+'Bigo2 is not null '+
           'Order By Bigo2';
  Translate(Sqlen, '@Chek5', 'show1');
  end else begin
  Sqlen := 'Select distinct Bigo2 From G7_Ggeo '+
           'Where '+D_Select+'( Chek5 is null'+' or '+'Chek5 <>''@Chek5'' )'+' and '+'Bigo2 is not null '+
           'Order By Bigo2';
  Translate(Sqlen, '@Chek5', 'show1');
  end;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    List1:=0;
    T00:=Base10.Socket.ClientData('1');
    while List1 < T00-1 do begin
      List1:=List1+1;
      Edit127.Items.Add(Base10.Socket.GetData(List1, 1));
    end;
  end;

  mSqry.First;
  nSqry.First;
  mSqry.AfterScroll:=Base10.T1_Sub72AfterScroll;
  nSqry.AfterScroll:=Base10.T1_Sub71AfterScroll;
  Button023Click(Self);
  Button024Click(Self);
  ProgressBar1.Position:=0;

  DataSource1.Enabled:=True;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo17.FormCreate(Sender: TObject);
begin
//Application.OnMessage:= AnyMessage;
end;

procedure TSobo17.AnyMessage(var Msg: TMsg; var Handled: Boolean);
begin
  if Msg.Message = WM_MouseWheel then
  if ActiveControl is TDBgrid then begin
    if Msg.wParam > 0 then begin
    keybd_event(VK_UP, VK_UP, 0, 0);
    keybd_event(VK_UP, VK_UP, KEYEVENTF_KEYUP, 0);
    DBGrid101.Invalidate;
    end
    else if Msg.wParam < 0 then begin
    keybd_event(VK_DOWN, VK_DOWN, 0, 0);
    keybd_event(VK_DOWN, VK_DOWN, KEYEVENTF_KEYUP, 0);
    DBGrid101.Invalidate;
    end;
  end;
end;

procedure TSobo17.RadioButtonClick(Sender: TObject);
begin
  if RadioButton331.Checked=True then begin
    Edit331.Enabled:=True;
    Edit331.ColorFlat:=clWhite;
  end else begin
    Edit331.Value:=0;
    Edit331.Enabled:=False;
    Edit331.ColorFlat:=clActiveBorder;
  end;
  if RadioButton341.Checked=True then begin
    Edit341.Enabled:=True;
    Edit341.ColorFlat:=clWhite;
  end else begin
    Edit341.Value:=0;
    Edit341.Enabled:=False;
    Edit341.ColorFlat:=clActiveBorder;
  end;

  if RadioButton411.Checked=True then begin
    Edit411.Enabled:=True;
    Edit411.ColorFlat:=clWhite;
    Edit412.Enabled:=True;
    Edit412.ColorFlat:=$0080FFFF;
  end else begin
    Edit411.Value:=0;
    Edit411.Enabled:=False;
    Edit411.ColorFlat:=clActiveBorder;
    Edit412.Value:=0;
    Edit412.Enabled:=False;
    Edit412.ColorFlat:=clActiveBorder;
  end;
  if RadioButton421.Checked=True then begin
    Edit421.Enabled:=True;
    Edit421.ColorFlat:=clWhite;
    Edit422.Enabled:=True;
    Edit422.ColorFlat:=$0080FFFF;
  end else begin
    Edit421.Value:=0;
    Edit421.Enabled:=False;
    Edit421.ColorFlat:=clActiveBorder;
    Edit422.Value:=0;
    Edit422.Enabled:=False;
    Edit422.ColorFlat:=clActiveBorder;
  end;
  if RadioButton431.Checked=True then begin
    Edit431.Enabled:=True;
    Edit431.ColorFlat:=clWhite;
    Edit432.Enabled:=True;
    Edit432.ColorFlat:=$0080FFFF;
  end else begin
    Edit431.Value:=0;
    Edit431.Enabled:=False;
    Edit431.ColorFlat:=clActiveBorder;
    Edit432.Value:=0;
    Edit432.Enabled:=False;
    Edit432.ColorFlat:=clActiveBorder;
  end;
  if RadioButton441.Checked=True then begin
    Edit441.Enabled:=True;
    Edit441.ColorFlat:=clWhite;
    Edit442.Enabled:=True;
    Edit442.ColorFlat:=$0080FFFF;
  end else begin
    Edit441.Value:=0;
    Edit441.Enabled:=False;
    Edit441.ColorFlat:=clActiveBorder;
    Edit442.Value:=0;
    Edit442.Enabled:=False;
    Edit442.ColorFlat:=clActiveBorder;
  end;
  if RadioButton451.Checked=True then begin
    Edit451.Enabled:=True;
    Edit451.ColorFlat:=clWhite;
    Edit452.Enabled:=True;
    Edit452.ColorFlat:=$0080FFFF;
  end else begin
    Edit451.Value:=0;
    Edit451.Enabled:=False;
    Edit451.ColorFlat:=clActiveBorder;
    Edit452.Value:=0;
    Edit452.Enabled:=False;
    Edit452.ColorFlat:=clActiveBorder;
  end;

  if RadioButton511.Checked=True then begin
    Edit511.Enabled:=True;
    Edit511.ColorFlat:=clWhite;
  end else begin
    Edit511.Value:=0;
    Edit511.Enabled:=False;
    Edit511.ColorFlat:=clActiveBorder;
  end;
  if RadioButton521.Checked=True then begin
    Edit521.Enabled:=True;
    Edit521.ColorFlat:=clWhite;
  end else begin
    Edit521.Value:=0;
    Edit521.Enabled:=False;
    Edit521.ColorFlat:=clActiveBorder;
  end;
  if RadioButton531.Checked=True then begin
    Edit531.Enabled:=True;
    Edit531.ColorFlat:=clWhite;
  end else begin
    Edit531.Value:=0;
    Edit531.Enabled:=False;
    Edit531.ColorFlat:=clActiveBorder;
  end;
  if RadioButton541.Checked=True then begin
    Edit541.Enabled:=True;
    Edit541.ColorFlat:=clWhite;
  end else begin
    Edit541.Value:=0;
    Edit541.Enabled:=False;
    Edit541.ColorFlat:=clActiveBorder;
  end;
  if RadioButton551.Checked=True then begin
    Edit551.Enabled:=True;
    Edit551.ColorFlat:=clWhite;
  end else begin
    Edit551.Value:=0;
    Edit551.Enabled:=False;
    Edit551.ColorFlat:=clActiveBorder;
  end;
  if RadioButton561.Checked=True then begin
    Edit561.Enabled:=True;
    Edit561.ColorFlat:=clWhite;
  end else begin
    Edit561.Value:=0;
    Edit561.Enabled:=False;
    Edit561.ColorFlat:=clActiveBorder;
  end;
  if RadioButton571.Checked=True then begin
    Edit571.Enabled:=True;
    Edit571.ColorFlat:=clWhite;
  end else begin
    Edit571.Value:=0;
    Edit571.Enabled:=False;
    Edit571.ColorFlat:=clActiveBorder;
  end;
  if RadioButton581.Checked=True then begin
    Edit581.Enabled:=True;
    Edit581.ColorFlat:=clWhite;
  end else begin
    Edit581.Value:=0;
    Edit581.Enabled:=False;
    Edit581.ColorFlat:=clActiveBorder;
  end;

  if RadioButton591.Checked=True then begin
    Edit591.Enabled:=True;
    Edit591.ColorFlat:=clWhite;
    Edit592.Enabled:=True;
    Edit592.ColorFlat:=$0080FFFF;
  end else begin
    Edit591.Value:=0;
    Edit591.Enabled:=False;
    Edit591.ColorFlat:=clActiveBorder;
    Edit592.Value:=0;
    Edit592.Enabled:=False;
    Edit592.ColorFlat:=clActiveBorder;
  end;

  if RadioButton481.Checked=True then begin
    Edit481.Enabled:=True;
    Edit481.ColorFlat:=clWhite;
  end else begin
    Edit481.Value:=0;
    Edit481.Enabled:=False;
    Edit481.ColorFlat:=clActiveBorder;
  end;
  if RadioButton491.Checked=True then begin
    Edit491.Enabled:=True;
    Edit491.ColorFlat:=clWhite;
  end else begin
    Edit491.Value:=0;
    Edit491.Enabled:=False;
    Edit491.ColorFlat:=clActiveBorder;
  end;

  if RadioButton611.Checked=True then begin
    Edit611.Enabled:=True;
    Edit611.ColorFlat:=clWhite;
    Edit612.Enabled:=True;
    Edit612.ColorFlat:=$0080FFFF;
  end else begin
    Edit611.Value:=0;
    Edit611.Enabled:=False;
    Edit611.ColorFlat:=clActiveBorder;
    Edit612.Value:=0;
    Edit612.Enabled:=False;
    Edit612.ColorFlat:=clActiveBorder;
  end;
  if RadioButton621.Checked=True then begin
    Edit621.Enabled:=True;
    Edit621.ColorFlat:=clWhite;
    Edit622.Enabled:=True;
    Edit622.ColorFlat:=$0080FFFF;
  end else begin
    Edit621.Value:=0;
    Edit621.Enabled:=False;
    Edit621.ColorFlat:=clActiveBorder;
    Edit622.Value:=0;
    Edit622.Enabled:=False;
    Edit622.ColorFlat:=clActiveBorder;
  end;
end;

procedure TSobo17.Button300Click(Sender: TObject);
begin
  {-G7_Ggeo-}
  Sqlen := 'Select '+
  'Yes33,Yes34,Yes35,Yes41,Yes42,Yes43,Yes44,Yes45,Yes48,Yes49,'+
  'Yes51,Yes52,Yes53,Yes54,Yes55,Yes56,Yes57,Yes58,Yes59,Yes61,Yes62 '+
  'From G7_Ggeo Where '+D_Select+'Gcode'+'='+#39+nSqry.FieldByName('Gcode').AsString+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  if SGrid.Cells[ 0,1]='1' then
  RadioButton331.Checked:=True else
  RadioButton332.Checked:=True;

  if SGrid.Cells[ 1,1]='1' then
  RadioButton341.Checked:=True else
  RadioButton342.Checked:=True;

  if SGrid.Cells[ 2,1]='1' then
  RadioButton351.Checked:=True else
  RadioButton352.Checked:=True;

  if SGrid.Cells[ 3,1]='1' then
  RadioButton411.Checked:=True else
  RadioButton412.Checked:=True;

  if SGrid.Cells[ 4,1]='1' then
  RadioButton421.Checked:=True else
  RadioButton422.Checked:=True;

  if SGrid.Cells[ 5,1]='1' then
  RadioButton431.Checked:=True else
  RadioButton432.Checked:=True;

  if SGrid.Cells[ 6,1]='1' then
  RadioButton441.Checked:=True else
  RadioButton442.Checked:=True;

  if SGrid.Cells[ 7,1]='1' then
  RadioButton451.Checked:=True else
  RadioButton452.Checked:=True;

  if SGrid.Cells[ 8,1]='1' then
  RadioButton481.Checked:=True else
  RadioButton482.Checked:=True;

  if SGrid.Cells[ 9,1]='1' then
  RadioButton491.Checked:=True else
  RadioButton492.Checked:=True;

  if SGrid.Cells[10,1]='1' then
  RadioButton511.Checked:=True else
  RadioButton512.Checked:=True;

  if SGrid.Cells[11,1]='1' then
  RadioButton521.Checked:=True else
  RadioButton522.Checked:=True;

  if SGrid.Cells[12,1]='1' then
  RadioButton531.Checked:=True else
  RadioButton532.Checked:=True;

  if SGrid.Cells[13,1]='1' then
  RadioButton541.Checked:=True else
  RadioButton542.Checked:=True;

  if SGrid.Cells[14,1]='1' then
  RadioButton551.Checked:=True else
  RadioButton552.Checked:=True;

  if SGrid.Cells[15,1]='1' then
  RadioButton561.Checked:=True else
  RadioButton562.Checked:=True;

  if SGrid.Cells[16,1]='1' then
  RadioButton571.Checked:=True else
  RadioButton572.Checked:=True;

  if SGrid.Cells[17,1]='1' then
  RadioButton581.Checked:=True else
  RadioButton582.Checked:=True;

  if SGrid.Cells[18,1]='1' then
  RadioButton591.Checked:=True else
  RadioButton592.Checked:=True;

  if SGrid.Cells[19,1]='1' then
  RadioButton611.Checked:=True else
  RadioButton612.Checked:=True;

  if SGrid.Cells[20,1]='1' then
  RadioButton621.Checked:=True else
  RadioButton622.Checked:=True;

  {-G7_Ggeo-}
  Sqlen := 'Select '+
  'Sum02,Sum04,Sum06,Sum09,Sum12,Sum15,Sum18,Sum19,Sum21,Sum22,Sum25,Sum32,'+
  'Sum33,Sum34,Sum36,Sum38,Sum39,Sum40,Sum41,Sum42,Sum43,Sum44,Sum45,Sum46,'+
  'Sum47,Sum61,Sum62,Sum63,Sum64,Sum68,Sum69,Bigo1 '+
  'From G7_Ggeo Where '+D_Select+'Gcode'+'='+#39+nSqry.FieldByName('Gcode').AsString+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  Edit311.Value:=StrToIntDef(SGrid.Cells[ 0,1],0);
  Edit321.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
  Edit331.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
  Edit341.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);

  Edit411.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
  Edit412.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
  Edit421.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
  Edit422.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);
  Edit431.Value:=StrToIntDef(SGrid.Cells[15,1],0);
  Edit432.Value:=StrToIntDef(SGrid.Cells[16,1],0);
  Edit441.Value:=StrToIntDef(SGrid.Cells[17,1],0);
  Edit442.Value:=StrToIntDef(SGrid.Cells[18,1],0);
  Edit451.Value:=StrToIntDef(SGrid.Cells[12,1],0);
  Edit452.Value:=StrToIntDef(SGrid.Cells[13,1],0);

  Edit511.Value:=StrToIntDef(SGrid.Cells[10,1],0);
  Edit521.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
  Edit531.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
  Edit541.Value:=StrToIntDef(SGrid.Cells[11,1],0);
  Edit551.Value:=StrToIntDef(SGrid.Cells[19,1],0);

  Edit561.Value:=StrToIntDef(SGrid.Cells[20,1],0);
  Edit571.Value:=StrToIntDef(SGrid.Cells[21,1],0);
  Edit581.Value:=StrToIntDef(SGrid.Cells[22,1],0);
  Edit591.Text :=SGrid.Cells[24,1];
  Edit592.Value:=StrToIntDef(SGrid.Cells[23,1],0);

  Edit611.Value:=StrToIntDef(SGrid.Cells[25,1],0);
  Edit612.Value:=StrToIntDef(SGrid.Cells[26,1],0);
  Edit621.Value:=StrToIntDef(SGrid.Cells[27,1],0);
  Edit622.Value:=StrToIntDef(SGrid.Cells[28,1],0);

  Edit481.Value:=StrToIntDef(SGrid.Cells[29,1],0);
  Edit491.Value:=StrToIntDef(SGrid.Cells[30,1],0);

  Edit236.Value:=StrToIntDef(SGrid.Cells[14,1],0);
  Edit238.Text :=SGrid.Cells[31,1];

  RadioButtonClick(Self);
end;

procedure TSobo17.Button301Click(Sender: TObject);
var Sq0,Sq1,Sq2: String;
begin
{
  기본계약부수    :Edit311(sum02)
  기본금액        :Edit321(sum04)
  초과부수        :Edit331(sum06)
  지방부수        :Edit341(sum09)
  입출고기본부수  :Edit411(sum18),Edit412(sum19)
  입출고초과관리비:Edit421(sum21),Edit422(sum22)
  재고기본부수    :Edit431(sum38),Edit432(sum39)
  재고초과관리비  :Edit441(sum40),Edit442(sum41)
  재고관리비      :Edit451(sum33),Edit452(sum34)
  출고종당관리비  :Edit611(sum61),Edit612(sum62)
  반품종당관리비  :Edit621(sum63),Edit622(sum64)
  거래명세서발행비외    : Edit511(sum25)
  책보호대              : Edit521(sum12)
  박스대                : Edit531(sum15)
  반품정리비,월정관리   : Edit541(sum32)
  반품정리비및비품보관비: Edit551(sum42)
  분류해체및입력비      : Edit561(sum43)
  시내수거업무비        : Edit571(sum44)
  지장수거업무비        : Edit581(sum45)
  적재공간운영비        : Edit591(sum46)
}

  Sqlen:='Select Gpass From Id_Logn Where '+D_Select+'Hcode=''@Hcode''';
  Translate(Sqlen, '@Hcode', '0001');
  Logn3:=Base10.Seek_Name(Sqlen);

  Sq0:='NO';
  if Base10.Database.Database='book_kb_db' then begin
    if Sobo40.ShowModal=mrOK Then
    if Sobo40.Edit101.Text=Logn3 then
    Sq0:='OK';
  end else begin
    Sq0:='OK';
  end;

if Sq0='OK' then begin
  Sqlon := 'UPDATE G7_Ggeo SET '+
  'Date1=''@Date1'',Date2=''@Date2'', '+
  'Sum02=  @Sum02  ,Sum04=  @Sum04  ,Sum06=  @Sum06  ,Sum09=  @Sum09  , '+
  'Sum18=  @Sum18  ,Sum19=  @Sum19  ,Sum21=  @Sum21  ,Sum22=  @Sum22  , '+
  'Sum36=  @Sum36  ,Sum38=  @Sum38  ,Sum39=  @Sum39  ,Sum40=  @Sum40  , ';
  Sqlen :=
  'Sum41=  @Sum41  ,Sum33=  @Sum33  ,Sum34=  @Sum34  ,Sum25=  @Sum25  , '+
  'Sum12=  @Sum12  ,Sum15=  @Sum15  ,Sum32=  @Sum32  ,Sum42=  @Sum42  , '+
  'Sum43=  @Sum43  ,Sum44=  @Sum44  ,Sum45=  @Sum45  ,Sum46=  @Sum46  , '+
  'Sum47=  @Sum47  ,Sum61=  @Sum61  ,Sum62=  @Sum62  ,Sum63=  @Sum63  , ';
  Sq1 :=
  'Sum64=  @Sum64  ,Sum68=  @Sum68  ,Sum69=  @Sum69  , '+
  'Yes33=''@Yes33'',Yes34=''@Yes34'',Yes35=''@Yes35'',Yes41=''@Yes41'', '+
  'Yes42=''@Yes42'',Yes43=''@Yes43'',Yes44=''@Yes44'',Yes45=''@Yes45'', '+
  'Yes48=''@Yes48'',Yes49=''@Yes49'',Yes51=''@Yes51'',Yes52=''@Yes52'', '+
  'Yes53=''@Yes53'',Yes54=''@Yes54'',Yes55=''@Yes55'',Yes56=''@Yes56'', ';
  Sq2 :=
  'Yes57=''@Yes57'',Yes58=''@Yes58'',Yes59=''@Yes59'',Yes61=''@Yes61'', '+
  'Yes62=''@Yes62'',Bigo1=''@Bigo1''  '+
  'WHERE Gcode'+'='+#39+nSqry.FieldByName('Gcode').AsString+#39;

  Translate(Sqlon, '@Date1', Edit901.Text);
  Translate(Sqlon, '@Date2', Edit902.Text);
  TransAuto(Sqlon, '@Sum02', FloatToStr(Edit311.Value));
  TransAuto(Sqlon, '@Sum04', FloatToStr(Edit321.Value));
  TransAuto(Sqlon, '@Sum06', FloatToStr(Edit331.Value));
  TransAuto(Sqlon, '@Sum09', FloatToStr(Edit341.Value));
  TransAuto(Sqlon, '@Sum18', FloatToStr(Edit411.Value));
  TransAuto(Sqlon, '@Sum19', FloatToStr(Edit412.Value));
  TransAuto(Sqlon, '@Sum21', FloatToStr(Edit421.Value));
  TransAuto(Sqlon, '@Sum22', FloatToStr(Edit422.Value));
  TransAuto(Sqlon, '@Sum36', FloatToStr(Edit236.Value));
  TransAuto(Sqlon, '@Sum38', FloatToStr(Edit431.Value));
  TransAuto(Sqlon, '@Sum39', FloatToStr(Edit432.Value));
  TransAuto(Sqlon, '@Sum40', FloatToStr(Edit441.Value));
  TransAuto(Sqlen, '@Sum41', FloatToStr(Edit442.Value));
  TransAuto(Sqlen, '@Sum33', FloatToStr(Edit451.Value));
  TransAuto(Sqlen, '@Sum34', FloatToStr(Edit452.Value));
  TransAuto(Sqlen, '@Sum25', FloatToStr(Edit511.Value));
  TransAuto(Sqlen, '@Sum12', FloatToStr(Edit521.Value));
  TransAuto(Sqlen, '@Sum15', FloatToStr(Edit531.Value));
  TransAuto(Sqlen, '@Sum32', FloatToStr(Edit541.Value));
  TransAuto(Sqlen, '@Sum42', FloatToStr(Edit551.Value));
  TransAuto(Sqlen, '@Sum43', FloatToStr(Edit561.Value));
  TransAuto(Sqlen, '@Sum44', FloatToStr(Edit571.Value));
  TransAuto(Sqlen, '@Sum45', FloatToStr(Edit581.Value));
  TransAuto(Sqlen, '@Sum46', FloatToStr(Edit592.Value));
  TransAuto(Sqlen, '@Sum47', FloatToStrF(Edit591.Value,ffNumber,2,1));
  TransAuto(Sqlen, '@Sum61', FloatToStr(Edit611.Value));
  TransAuto(Sqlen, '@Sum62', FloatToStr(Edit612.Value));
  TransAuto(Sqlen, '@Sum63', FloatToStr(Edit621.Value));
  TransAuto(Sq1,   '@Sum64', FloatToStr(Edit622.Value));
  TransAuto(Sq1,   '@Sum68', FloatToStr(Edit481.Value));
  TransAuto(Sq1,   '@Sum69', FloatToStr(Edit491.Value));

  if RadioButton331.Checked=True then
  Translate(Sq1, '@Yes33', '1') else
  Translate(Sq1, '@Yes33', '2');

  if RadioButton341.Checked=True then
  Translate(Sq1, '@Yes34', '1') else
  Translate(Sq1, '@Yes34', '2');

  if RadioButton351.Checked=True then
  Translate(Sq1, '@Yes35', '1') else
  Translate(Sq1, '@Yes35', '2');

  if RadioButton411.Checked=True then
  Translate(Sq1, '@Yes41', '1') else
  Translate(Sq1, '@Yes41', '2');

  if RadioButton421.Checked=True then
  Translate(Sq1, '@Yes42', '1') else
  Translate(Sq1, '@Yes42', '2');

  if RadioButton431.Checked=True then
  Translate(Sq1, '@Yes43', '1') else
  Translate(Sq1, '@Yes43', '2');

  if RadioButton441.Checked=True then
  Translate(Sq1, '@Yes44', '1') else
  Translate(Sq1, '@Yes44', '2');

  if RadioButton451.Checked=True then
  Translate(Sq1, '@Yes45', '1') else
  Translate(Sq1, '@Yes45', '2');

  if RadioButton481.Checked=True then
  Translate(Sq1, '@Yes48', '1') else
  Translate(Sq1, '@Yes48', '2');

  if RadioButton491.Checked=True then
  Translate(Sq1, '@Yes49', '1') else
  Translate(Sq1, '@Yes49', '2');

  if RadioButton511.Checked=True then
  Translate(Sq1, '@Yes51', '1') else
  Translate(Sq1, '@Yes51', '2');

  if RadioButton521.Checked=True then
  Translate(Sq1, '@Yes52', '1') else
  Translate(Sq1, '@Yes52', '2');

  if RadioButton531.Checked=True then
  Translate(Sq1, '@Yes53', '1') else
  Translate(Sq1, '@Yes53', '2');

  if RadioButton541.Checked=True then
  Translate(Sq1, '@Yes54', '1') else
  Translate(Sq1, '@Yes54', '2');

  if RadioButton551.Checked=True then
  Translate(Sq1, '@Yes55', '1') else
  Translate(Sq1, '@Yes55', '2');

  if RadioButton561.Checked=True then
  Translate(Sq1, '@Yes56', '1') else
  Translate(Sq1, '@Yes56', '2');

  if RadioButton571.Checked=True then
  Translate(Sq2, '@Yes57', '1') else
  Translate(Sq2, '@Yes57', '2');

  if RadioButton581.Checked=True then
  Translate(Sq2, '@Yes58', '1') else
  Translate(Sq2, '@Yes58', '2');

  if RadioButton591.Checked=True then
  Translate(Sq2, '@Yes59', '1') else
  Translate(Sq2, '@Yes59', '2');

  if RadioButton611.Checked=True then
  Translate(Sq2, '@Yes61', '1') else
  Translate(Sq2, '@Yes61', '2');

  if RadioButton621.Checked=True then
  Translate(Sq2, '@Yes62', '1') else
  Translate(Sq2, '@Yes62', '2');

  Translate(Sq2, '@Bigo1', Edit238.Text);

  Base10.Socket.RunSQL(Sqlon+Sqlen+Sq1+Sq2);
  Base10.Socket.BusyLoop;
  if Base10.Socket.Body_Data = 'ERROR' then begin
    ShowMessage(E_Update);
    DBGrid101.SetFocus;
    Exit;
  end;

  ShowMessage('저장완료');
end else begin
  ShowMessage('패스워드 확인요망');
end;
end;

procedure TSobo17.Button302Click(Sender: TObject);
begin
  Panel300.Visible:=False;
  Panel701.Visible:=True;
  Panel702.Visible:=True;
  Button700Click(Self)
end;

procedure TSobo17.Button700Click(Sender: TObject);
var Temp1: TStream;
begin
  With Query0 do begin
    Close;
    Sql.Clear;
    Sql.add('Select Memos From G7_Ggeo ');
    Sql.Add('WHERE Gcode = '''+nSqry.FieldByName('Gcode').AsString+''' ');
    Open;
  end;

  Temp1 := TStream.Create;
  Temp1 := Query0.CreateBlobStream(Query0.FieldByName('Memos'), bmRead);
  Editor.Lines.LoadFromStream(Temp1);
  Temp1.Free;
  Query0.Close;
end;

procedure TSobo17.Button701Click(Sender: TObject);
var MemoryStream: TMemoryStream;
    St1: String;
begin
  With Query0 do begin
    Close;
    Sql.Clear;
    Sql.add('UPDATE G7_Ggeo SET ');
    Sql.Add(' Memos = :Memos  ');
    Sql.Add('WHERE Gcode = '''+nSqry.FieldByName('Gcode').AsString+''' ');

    MemoryStream := TMemoryStream.Create;
    Editor.Lines.SaveToStream(MemoryStream);
    ParamByName('Memos').LoadFromStream(MemoryStream,ftBlob);
    MemoryStream.Free;

    ExecSql;
  end;
  ShowMessage('저장 완료.');
end;

procedure TSobo17.Button702Click(Sender: TObject);
begin
  Panel701.Visible:=False;
  Panel702.Visible:=False;
  Panel300.Visible:=True;
  Button300Click(Self)
end;

procedure TSobo17.SetData2nSql(Sqlen: string);
begin
  with Base10.ZMySqlQuery1 do
  begin
    Close;
    Sql.Clear;
    Sql.Text := Sqlen;
    Open;
  end;

  while not Base10.ZMySqlQuery1.Eof do
  begin
    nSqry.Append;
    nSqry.FieldByName('id').Value := Base10.ZMySqlQuery1.FieldByName('id').Value;
    nSqry.FieldByName('chek1').Value := Base10.ZMySqlQuery1.FieldByName('chek1').Value;
    nSqry.FieldByName('chek2').Value := Base10.ZMySqlQuery1.FieldByName('chek2').Value;
    //nSqry.FieldByName('chek4').Value := Base10.ZMySqlQuery1.FieldByName('chek4').Value;
    nSqry.FieldByName('scode').Value := Base10.ZMySqlQuery1.FieldByName('scode').Value;
    nSqry.FieldByName('gubun').Value := Base10.ZMySqlQuery1.FieldByName('gubun').Value;
    nSqry.FieldByName('jubun').Value := Base10.ZMySqlQuery1.FieldByName('jubun').Value;
    nSqry.FieldByName('gcode').Value := Base10.ZMySqlQuery1.FieldByName('gcode').Value;
    nSqry.FieldByName('gname').Value := Base10.ZMySqlQuery1.FieldByName('gname').Value;
    nSqry.FieldByName('ocode').Value := Base10.ZMySqlQuery1.FieldByName('ocode').Value;
    nSqry.FieldByName('name1').Value := Base10.ZMySqlQuery1.FieldByName('name1').Value;
    nSqry.FieldByName('name2').Value := Base10.ZMySqlQuery1.FieldByName('name2').Value;
    nSqry.FieldByName('jumin').Value := Base10.ZMySqlQuery1.FieldByName('jumin').Value;
    nSqry.FieldByName('gpper').Value := Base10.ZMySqlQuery1.FieldByName('gpper').Value;
    nSqry.FieldByName('gpost').Value := Base10.ZMySqlQuery1.FieldByName('gpost').Value;
    nSqry.FieldByName('gadd1').Value := Base10.ZMySqlQuery1.FieldByName('gadd1').Value;
    nSqry.FieldByName('gadd2').Value := Base10.ZMySqlQuery1.FieldByName('gadd2').Value;
    nSqry.FieldByName('gtel1').Value := Base10.ZMySqlQuery1.FieldByName('gtel1').Value;
    nSqry.FieldByName('gtel2').Value := Base10.ZMySqlQuery1.FieldByName('gtel2').Value;
    nSqry.FieldByName('gfax1').Value := Base10.ZMySqlQuery1.FieldByName('gfax1').Value;
    nSqry.FieldByName('gfax2').Value := Base10.ZMySqlQuery1.FieldByName('gfax2').Value;
    nSqry.FieldByName('bigo2').Value := Base10.ZMySqlQuery1.FieldByName('bigo2').Value;
    nSqry.FieldByName('gnum1').Value := Base10.ZMySqlQuery1.FieldByName('gnum1').Value;
    nSqry.FieldByName('gbigo').Value := Base10.ZMySqlQuery1.FieldByName('gbigo').Value;
    nSqry.FieldByName('gposa').Value := Base10.ZMySqlQuery1.FieldByName('gposa').Value;
    nSqry.FieldByName('gnumb').Value := Base10.ZMySqlQuery1.FieldByName('gnumb').Value;
    nSqry.FieldByName('guper').Value := Base10.ZMySqlQuery1.FieldByName('guper').Value;
    nSqry.FieldByName('gjomo').Value := Base10.ZMySqlQuery1.FieldByName('gjomo').Value;
    nSqry.FieldByName('hcode').Value := Base10.ZMySqlQuery1.FieldByName('hcode').Value;
    nSqry.FieldByName('gdate').Value := Base10.ZMySqlQuery1.FieldByName('gdate').Value;
    nSqry.FieldByName('giqut').Value := Base10.ZMySqlQuery1.FieldByName('giqut').Value;
    nSqry.FieldByName('gisum').Value := Base10.ZMySqlQuery1.FieldByName('gisum').Value;
    nSqry.FieldByName('gosum').Value := Base10.ZMySqlQuery1.FieldByName('gosum').Value;
    nSqry.FieldByName('gssum').Value := Base10.ZMySqlQuery1.FieldByName('gssum').Value;

    Base10.ZMySqlQuery1.Next;
  end;
  if nSqry.State in [dsInsert] then
    nSqry.Post;
end;
procedure TSobo17.DBGrid101DblClick(Sender: TObject);
begin
{}
end;

end.
