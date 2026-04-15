unit Seok03;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit, ComCtrls, ToolWin,
  ImgList, Mylabel, Mask, TFlatMaskEditUnit, ZQuery, ZMySqlQuery, ToolEdit,
  Printers, RichEdit, RxRichEd, TFlatCheckBoxUnit, TFlatRadioButtonUnit;

type
  TSeok30 = class(TForm)
    Panel100: TFlatPanel;
    Panel201: TFlatPanel;
    Button101: TFlatButton;
    Button102: TFlatButton;
    BitBtn101: TBitBtn;
    BitBtn102: TBitBtn;
    DBGrid101: TDBGrid;
    DataSource1: TDataSource;
    Query1: TClientDataSet;
    Query1ID: TFloatField;
    Query1GCODE: TStringField;
    Query1GNAME: TStringField;
    Query1GTELS: TStringField;
    Query1HTELS: TStringField;
    Query1GBIGO: TStringField;
    Panel301: TFlatPanel;
    DBGrid201: TDBGrid;
    Panel401: TFlatPanel;
    Editor_1: TRichEdit;
    ToolbarImages: TImageList;
    FontDialog1: TFontDialog;
    Panel501: TFlatPanel;
    Edit103: TFlatMaskEdit;
    Panel502: TFlatPanel;
    Edit101: TFlatMaskEdit;
    Label101: TmyLabel3d;
    Edit102: TFlatMaskEdit;
    DataSource2: TDataSource;
    Query2: TClientDataSet;
    Query2GDATE: TStringField;
    Query0: TZMySqlQuery;
    StandardToolBar: TToolBar;
    UndoButton: TToolButton;
    ToolButton10: TToolButton;
    FontName: TComboBox;
    ToolButton11: TToolButton;
    FontSize: TEdit;
    UpDown1: TUpDown;
    ToolButton2: TToolButton;
    BoldButton: TToolButton;
    ItalicButton: TToolButton;
    UnderlineButton: TToolButton;
    ToolButton16: TToolButton;
    LeftAlign: TToolButton;
    CenterAlign: TToolButton;
    RightAlign: TToolButton;
    ToolButton20: TToolButton;
    BulletsButton: TToolButton;
    BitBtn103: TBitBtn;
    DateEdit1: TDateEdit;
    DateEdit2: TDateEdit;
    DateEdit3: TDateEdit;
    Editor: TRxRichEdit;
    CheckBox1: TFlatCheckBox;
    Button3: TFlatButton;
    procedure MemoPrint(aCaption: String);
    procedure mPrintClick(Sender: TObject);
    procedure Button016Click(Sender: TObject);
    procedure FontNameChange(Sender: TObject);
    procedure FontSizeChange(Sender: TObject);
    procedure BoldButtonClick(Sender: TObject);
    procedure ItalicButtonClick(Sender: TObject);
    procedure UnderlineButtonClick(Sender: TObject);
    procedure LeftAlignClick(Sender: TObject);
    procedure CenterAlignClick(Sender: TObject);
    procedure RightAlignClick(Sender: TObject);
    procedure BulletsButtonClick(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormPaint(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Button101Click(Sender: TObject);
    procedure Button201Click(Sender: TObject);
    procedure Button301Click(Sender: TObject);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure BitBtn101Click(Sender: TObject);
    procedure BitBtn102Click(Sender: TObject);
    procedure UndoButtonClick(Sender: TObject);
    procedure BitBtn103Click(Sender: TObject);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit2ButtonClick(Sender: TObject);
    procedure DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit3ButtonClick(Sender: TObject);
    procedure DateEdit3AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button3Click(Sender: TObject);
  private
    function CurrText: TRxTextAttributes;
    procedure GetFontNames;
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seok30: TSeok30;

implementation

{$R *.DFM}

uses Base01, TcpLib, Tong04;

procedure TSeok30.MemoPrint(aCaption: String);
var
 Range: TFormatRange;
 LastChar, MaxLen, LogX, LogY, OldMap: Integer;
 SaveRect: TRect;
begin
 FillChar(Range, SizeOf(TFormatRange), 0);
 with Printer, Range do
 begin
   Title := aCaption;
   BeginDoc;
   hdc := Handle;
   hdcTarget := hdc;
   LogX := GetDeviceCaps(Handle, LOGPIXELSX);
   LogY := GetDeviceCaps(Handle, LOGPIXELSY);
   if IsRectEmpty(Editor.PageRect) then
   begin
     rc.right := PageWidth * 1440 div LogX;
     rc.bottom := PageHeight * 1440 div LogY;
   end
   else begin
     rc.left := Editor.PageRect.Left * 1440 div LogX;
     rc.top := Editor.PageRect.Top * 1440 div LogY;
     rc.right := Editor.PageRect.Right * 1440 div LogX;
     rc.bottom := Editor.PageRect.Bottom * 1440 div LogY;
   end;


   //----------------------------------------------------------
   // 이부분만 추가 했습니다. 여백주기 위,아래,왼쪽,오른쪽 여백 -_-;
   rc.Left := rc.Left + (500 * 1440 div LogX);
   rc.Right := rc.Right - (500 * 1440 div LogX);
   rc.Top := rc.Top + (80 * 1440 div LogY);
   rc.Bottom := rc.Bottom - (80 * 1440 div LogY);
   //----------------------------------------------------------

   rcPage := rc;
   SaveRect := rc;
   LastChar := 0;
   MaxLen := Editor.GetTextLen;
   chrg.cpMax := -1;
   // ensure printer DC is in text map mode
   OldMap := SetMapMode(hdc, MM_TEXT);
   SendMessage(Editor.Handle, EM_FORMATRANGE, 0, 0);    // flush buffer
   try
     repeat
       rc := SaveRect;
       chrg.cpMin := LastChar;
       LastChar := SendMessage(Editor.Handle, EM_FORMATRANGE, 1, Longint(@Range));
       if (LastChar < MaxLen) and (LastChar <> -1) then NewPage;
     until (LastChar >= MaxLen) or (LastChar = -1);
     EndDoc;
   finally
     SendMessage(Editor.Handle, EM_FORMATRANGE, 0, 0);  // flush buffer
     SetMapMode(hdc, OldMap);       // restore previous map mode
   end;
 end;
end;

//위의 메서드 호출.. (메뉴 아이템 클릭)
procedure TSeok30.mPrintClick(Sender: TObject);
begin
  with TPrintDialog.Create(nil) do
  try
    if Execute then
    MemoPrint(Application.Title);
  finally
    Free;
  end;
end;

procedure TSeok30.Button016Click(Sender: TObject);
begin
  mPrintClick(Self);
//Tong40.print_38_01(Self);
end;

function TSeok30.CurrText: TRxTextAttributes;
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

procedure TSeok30.GetFontNames;
var
  DC: HDC;
begin
  DC := GetDC(0);
  EnumFonts(DC, nil, @EnumFontsProc, Pointer(FontName.Items));
  ReleaseDC(0, DC);
  FontName.Sorted := True;
end;

procedure TSeok30.FontNameChange(Sender: TObject);
begin
//if FUpdating then Exit;
  CurrText.Name := FontName.Items[FontName.ItemIndex];
end;

procedure TSeok30.FontSizeChange(Sender: TObject);
begin
//if FUpdating then Exit;
  CurrText.Size := StrToInt(FontSize.Text);
end;

procedure TSeok30.BoldButtonClick(Sender: TObject);
begin
//if FUpdating then Exit;
  if BoldButton.Down then
    CurrText.Style := CurrText.Style + [fsBold]
  else
    CurrText.Style := CurrText.Style - [fsBold];
end;

procedure TSeok30.ItalicButtonClick(Sender: TObject);
begin
//if FUpdating then Exit;
  if ItalicButton.Down then
    CurrText.Style := CurrText.Style + [fsItalic]
  else
    CurrText.Style := CurrText.Style - [fsItalic];
end;

procedure TSeok30.UnderlineButtonClick(Sender: TObject);
begin
//if FUpdating then Exit;
  if UnderlineButton.Down then
    CurrText.Style := CurrText.Style + [fsUnderline]
  else
    CurrText.Style := CurrText.Style - [fsUnderline];
end;

procedure TSeok30.LeftAlignClick(Sender: TObject);
begin
//if FUpdating then Exit;
  Editor.Paragraph.Alignment := TParaAlignment(TComponent(Sender).Tag);
end;

procedure TSeok30.CenterAlignClick(Sender: TObject);
begin
//if FUpdating then Exit;
  Editor.Paragraph.Alignment := TParaAlignment(TComponent(Sender).Tag);
end;

procedure TSeok30.RightAlignClick(Sender: TObject);
begin
//if FUpdating then Exit;
  Editor.Paragraph.Alignment := TParaAlignment(TComponent(Sender).Tag);
end;

procedure TSeok30.BulletsButtonClick(Sender: TObject);
begin
//if FUpdating then Exit;
  Editor.Paragraph.Numbering := TRxNumbering(BulletsButton.Down);
end;

procedure TSeok30.UndoButtonClick(Sender: TObject);
begin
  FontDialog1.Font.Assign(Editor.SelAttributes);
  if FontDialog1.Execute then
    CurrText.Assign(FontDialog1.Font);
//SelectionChange(Self);
  Editor.SetFocus;
end;

procedure TSeok30.FormPaint(Sender: TObject);
begin
  Seok30.OnPaint:=Nil;
  Seok30.OnShow:=FormShow;
  FormShow(Self);
end;

procedure TSeok30.FormActivate(Sender: TObject);
begin
  nForm:='38';
//nSqry:=Base10.T1_Sub11;
//mSqry:=Base10.T1_Sub12;
end;

procedure TSeok30.FormShow(Sender: TObject);
begin
  GetFontNames;
  FontSize.Text := IntToStr(Editor.SelAttributes.Size);
  FontName.Text := Editor.SelAttributes.Name;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit103.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Button101Click(Self);
  DBGrid101.SetFocus;
end;

procedure TSeok30.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Seok30:=nil;
//nSqry.AfterScroll:=nil;
//mSqry.AfterScroll:=nil;
  Base10.OpenExit(Query1);
  Base10.OpenExit(Query2);
end;

procedure TSeok30.Button101Click(Sender: TObject);
var St1: String;
begin
  Tong40.Show;
  Tong40.Update;

  Refresh;
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;
  Base10.OpenShow(Query1);

  Query1.Append;
  Query1.FieldByName('Gcode').AsString:='';
  Query1.FieldByName('Gname').AsString:='-전체-';
  Query1.Post;

  St1:='';
  if S_Where2<>'' then
  St1:=' and '+S_Where2;

  Sqlen := 'Select Gcode,Gname From G7_Ggeo Where '+D_Open+St1+' Order By Gcode';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Query1)
  else ShowMessage(E_Open);


  if CheckBox1.Checked=True then
  Sqlen := 'Select Hcode,Count(*) From Me_Sage '+' Group by Hcode'
  else
  Sqlen := 'Select Hcode,Count(*) From Me_Sage Where '+D_Open+' Group by Hcode';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    if Query1.Locate('Gcode',SGrid.Cells[ 0,List1],[loCaseInsensitive])=True then begin
      Query1.Edit;
      Query1.FieldByName('Gbigo').AsString:=SGrid.Cells[ 1,List1];
      Query1.Post;
    end;
  end;

  Query1.First;
  DBGrid101.SetFocus;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSeok30.Button201Click(Sender: TObject);
begin

  Refresh;
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  Base10.OpenShow(Query2);

  if CheckBox1.Checked=True then
  Sqlen := 'Select Gdate From Me_Sage Where '+D_Select+'Hcode=''@Hcode'' Order By Gdate DESC'
  else
  Sqlen := 'Select Gdate From Me_Sage Where '+D_Open+' and '+D_Select+'Hcode=''@Hcode'' Order By Gdate DESC';
  Translate(Sqlen, '@Hcode', Query1.FieldByName('Gcode').AsString);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(Query2)
  else ShowMessage(E_Open);

  Query2.First;
//DBGrid201.SetFocus;
  DataSource2.Enabled:=True;
  Screen.Cursor:=crDefault;

end;

procedure TSeok30.Button301Click(Sender: TObject);
var Temp1: TStream;
begin

  With Query0 do begin
    Close;
    Sql.Clear;
    Sql.add('Select Date1,Date2,Gbigo From Me_Sage ');
    Sql.Add('WHERE Hcode = '''+Query1.FieldByName('Gcode').AsString+''' ');
    Sql.Add('  AND Gdate = '''+Query2.FieldByName('Gdate').AsString+'''  ');
    Open;
  end;
  Edit103.Text:=Query2.FieldByName('Gdate').AsString;
  Edit101.Text:=Query0.FieldByName('Date1').AsString;
  Edit102.Text:=Query0.FieldByName('Date2').AsString;

  Temp1 := TStream.Create;
  Temp1 := Query0.CreateBlobStream(Query0.FieldByName('Gbigo'), bmRead);
  Editor.Lines.LoadFromStream(Temp1);
  Temp1.Free;
  Query0.Close;

{ Sqlen := 'Select Date1,Date2,Gbigo From Me_Sage Where '+D_Select+'Hcode=''@Hcode'' and Gdate=''@Gdate'' ';
  Translate(Sqlen, '@Hcode', Query1.FieldByName('Gcode').AsString);
  Translate(Sqlen, '@Gdate', Query2.FieldByName('Gdate').AsString);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.Body_Data <> 'NODATA' then begin
    Base10.Socket.MakeData;
    Edit103.Text:=Query2.FieldByName('Gdate').AsString;
    Edit101.Text:=Base10.Socket.GetData(1, 1);
    Edit102.Text:=Base10.Socket.GetData(1, 2);
    Editor.Lines.Text:=Base10.Socket.GetData(1, 3);
  end else begin
    Editor.Lines.Clear;
  end; }

end;

procedure TSeok30.BitBtn101Click(Sender: TObject);
var MemoryStream: TMemoryStream;
    St1: String;
begin

  if CheckBox1.Checked=True then begin

    Sqlen := 'Select Gdate From Me_Sage Where '+D_Select+'Hcode=''@Hcode'' and Gdate=''@Gdate'' and `Check`=''@Check'' ';
    Translate(Sqlen, '@Hcode', Query1.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Gdate', Edit103.Text);
    Translate(Sqlen, '@Check', 'D');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin

      With Query0 do begin
        Close;
        Sql.Clear;
        Sql.add('UPDATE Me_Sage SET ');
        Sql.Add(' Date1 = :Date1 ,');
        Sql.Add(' Date2 = :Date2 ,');
        Sql.Add(' Gbigo = :Gbigo  ');
        Sql.Add('WHERE Hcode = '''+Query1.FieldByName('Gcode').AsString+''' ');
        Sql.Add('  AND Gdate = '''+Edit103.Text+'''  ');
        Sql.Add('  AND `Check` = :Check ');
        ParamByName('Date1').AsString := Edit101.Text;
        ParamByName('Date2').AsString := Edit102.Text;
        ParamByName('Check').AsString := 'D';

        MemoryStream := TMemoryStream.Create;
        Editor.Lines.SaveToStream(MemoryStream);
        ParamByName('Gbigo').LoadFromStream(MemoryStream,ftBlob);
        MemoryStream.Free;

        ExecSql;
      end;

    end else begin

      With Query0 do begin
        Close;
        Sql.Clear;
        Sql.add('INSERT INTO Me_Sage ');
        Sql.Add('(Hcode, Gdate, Date1, Date2, Gbigo, `Check`) VALUES ');
        Sql.Add('(:Hcode,:Gdate,:Date1,:Date2,:Gbigo,:Check)');
        ParamByName('Hcode').AsString := Query1.FieldByName('Gcode').AsString;
        ParamByName('Gdate').AsString := Edit103.Text;
        ParamByName('Date1').AsString := Edit101.Text;
        ParamByName('Date2').AsString := Edit102.Text;
        ParamByName('Check').AsString := 'D';

        MemoryStream := TMemoryStream.Create;
        Editor.Lines.SaveToStream(MemoryStream);
        ParamByName('Gbigo').LoadFromStream(MemoryStream,ftBlob);
        MemoryStream.Free;

        ExecSql;
      end;

      St1:=Edit103.Text;

      Query2.Append;
      Query2.FieldByName('Gdate').AsString:=St1;
      Query2.Post;

    end;

  end else begin

    Sqlen := 'Select Gdate From Me_Sage Where '+D_Select+'Hcode=''@Hcode'' and Gdate=''@Gdate'' ';
    Translate(Sqlen, '@Hcode', Query1.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Gdate', Edit103.Text);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin

      With Query0 do begin
        Close;
        Sql.Clear;
        Sql.add('UPDATE Me_Sage SET ');
        Sql.Add(' Date1 = :Date1 ,');
        Sql.Add(' Date2 = :Date2 ,');
        Sql.Add(' Gbigo = :Gbigo  ');
        Sql.Add('WHERE Hcode = '''+Query1.FieldByName('Gcode').AsString+''' ');
        Sql.Add('  AND Gdate = '''+Edit103.Text+'''  ');
        ParamByName('Date1').AsString := Edit101.Text;
        ParamByName('Date2').AsString := Edit102.Text;

        MemoryStream := TMemoryStream.Create;
        Editor.Lines.SaveToStream(MemoryStream);
        ParamByName('Gbigo').LoadFromStream(MemoryStream,ftBlob);
        MemoryStream.Free;

        ExecSql;
      end;

    end else begin

      With Query0 do begin
        Close;
        Sql.Clear;
        Sql.add('INSERT INTO Me_Sage ');
        Sql.Add('(Hcode, Gdate, Date1, Date2, Gbigo) VALUES ');
        Sql.Add('(:Hcode,:Gdate,:Date1,:Date2,:Gbigo)');
        ParamByName('Hcode').AsString := Query1.FieldByName('Gcode').AsString;
        ParamByName('Gdate').AsString := Edit103.Text;
        ParamByName('Date1').AsString := Edit101.Text;
        ParamByName('Date2').AsString := Edit102.Text;

        MemoryStream := TMemoryStream.Create;
        Editor.Lines.SaveToStream(MemoryStream);
        ParamByName('Gbigo').LoadFromStream(MemoryStream,ftBlob);
        MemoryStream.Free;

        ExecSql;
      end;

      St1:=Edit103.Text;

      Query2.Append;
      Query2.FieldByName('Gdate').AsString:=St1;
      Query2.Post;

    end;

  end;
end;

procedure TSeok30.BitBtn102Click(Sender: TObject);
var MeDlg: Integer;
begin
MeDlg := MessageDlg('삭제 하시겠습니까?', mtConfirmation, [mbYes, mbNo], 0);
case MeDlg of
mrYes: begin

    Sqlen := 'DELETE From Me_Sage '+
    'WHERE Hcode=''@Hcode'' and Gdate=''@Gdate'' ';

    Translate(Sqlen, '@Hcode', Query1.FieldByName('Gcode').AsString);
    Translate(Sqlen, '@Gdate', Query2.FieldByName('Gdate').AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Delete);

    Query2.Delete;

end; end;
end;

procedure TSeok30.BitBtn103Click(Sender: TObject);
begin
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit103.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Editor.Lines.Clear;
  Editor.SetFocus;
end;

procedure TSeok30.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Button201Click(Self);
end;

procedure TSeok30.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Button301Click(Self);
end;

procedure TSeok30.DateEdit1ButtonClick(Sender: TObject);
begin
  if Edit101.Text > '2000.01.01' then
  DateEdit1.Date :=StrToDate(Edit101.Text) else
  DateEdit1.Date :=StrToDate(FormatDateTime('yyyy"."mm"."dd',Date));
end;

procedure TSeok30.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSeok30.DateEdit2ButtonClick(Sender: TObject);
begin
  if Edit102.Text > '2000.01.01' then
  DateEdit2.Date :=StrToDate(Edit102.Text) else
  DateEdit2.Date :=StrToDate(FormatDateTime('yyyy"."mm"."dd',Date));
end;

procedure TSeok30.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSeok30.DateEdit3ButtonClick(Sender: TObject);
begin
  if Edit103.Text > '2000.01.01' then
  DateEdit3.Date :=StrToDate(Edit103.Text) else
  DateEdit3.Date :=StrToDate(FormatDateTime('yyyy"."mm"."dd',Date));
end;

procedure TSeok30.DateEdit3AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit103.Text :=DateToStr(ADate);
end;

procedure TSeok30.Button3Click(Sender: TObject);
begin
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit103.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Button101Click(Self);
  DBGrid101.SetFocus;
end;

end.
