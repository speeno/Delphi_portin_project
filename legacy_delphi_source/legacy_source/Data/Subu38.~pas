unit Subu38;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, DBClient, DBGridEh,
  FileCtrl, IniFiles, ToolEdit;

type
  TSobo38 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel003: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Panel001: TFlatPanel;
    T3_Sub81: TClientDataSet;
    T3_Sub82: TClientDataSet;
    Button101: TFlatButton;
    Button201: TFlatButton;
    T3_Sub83: TClientDataSet;
    Panel002: TFlatPanel;
    DBGrid101: TDBGridEh;
    DBGrid201: TDBGridEh;
    T3_Sub81GDATE: TStringField;
    T3_Sub81GCODE: TStringField;
    T3_Sub81GNAME: TStringField;
    T3_Sub81BCODE: TStringField;
    T3_Sub81BNAME: TStringField;
    T3_Sub81GUBUN: TStringField;
    T3_Sub81PUBUN: TStringField;
    T3_Sub81JUBUN: TStringField;
    T3_Sub81GRAT1: TFloatField;
    T3_Sub81GSQUT: TFloatField;
    T3_Sub81GDANG: TFloatField;
    T3_Sub82GDATE: TStringField;
    T3_Sub82GCODE: TStringField;
    T3_Sub82GNAME: TStringField;
    T3_Sub82BCODE: TStringField;
    T3_Sub82BNAME: TStringField;
    T3_Sub82GQUT1: TFloatField;
    T3_Sub82GQUT2: TFloatField;
    T3_Sub82MEMO1: TBlobField;
    T3_Sub82MEMO2: TMemoField;
    FlatButton1: TFlatButton;
    Panel004: TFlatPanel;
    Memo1: TMemo;
    myLabel3d1: TmyLabel3d;
    Label101: TmyLabel3d;
    DBGridEh1: TDBGridEh;
    Panel101: TFlatPanel;
    Edit101: TFlatMaskEdit;
    T3_Sub81GSSUM: TFloatField;
    DateEdit1: TDateEdit;
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
    procedure DBGrid101Enter(Sender: TObject);
    procedure DBGrid201Enter(Sender: TObject);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101TitleClick(Column: TColumn);
    procedure DBGrid201TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure ComboBox1Change(Sender: TObject);
    procedure FileListBox1Click(Sender: TObject);
    procedure SeperateStr(Str, SubStr : String; StrList : TStrings);
    function GetSeperateStrByIndex(Str, SubStr : String; Index : LongInt) : String;
    procedure FlatButton1Click(Sender: TObject);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo38: TSobo38;
  nCode: String;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib, Seok09,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo38.FormActivate(Sender: TObject);
begin
  nForm:='38';
  nSqry:=T3_Sub81;
  mSqry:=T3_Sub82;
end;

procedure TSobo38.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  DBGrid101.Align:=alClient;
  DBGrid201.Align:=alClient;
//ComboBox1Change(Self);
end;

procedure TSobo38.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo38:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo38.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button008Click(Sender: TObject);
begin
//Tong20.Zoom_Int_01('39');
end;

procedure TSobo38.Button009Click(Sender: TObject);
begin
//Tong20.Zoom_Out_01('39');
end;

procedure TSobo38.Button010Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo38.Button011Click(Sender: TObject);
begin
//Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo38.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
//Base10.ColumnX1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo38.Button013Click(Sender: TObject);
begin
  oSqry:=mSqry;
//Base10.ColumnX1(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo38.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('39-01');
end;

procedure TSobo38.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('39-02');
end;

procedure TSobo38.Button016Click(Sender: TObject);
begin
  Tong40.print_39_01(Self);
end;

procedure TSobo38.Button017Click(Sender: TObject);
begin
  Tong40.print_39_02(Self);
end;

procedure TSobo38.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button021Click(Sender: TObject);
begin
//Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo38.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo38.Button101Click(Sender: TObject);
begin
  Tong40.Show;
  Tong40.Update;

  Refresh;
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;
  DataSource2.Enabled:=False;
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);

  nSqry.First;
  mSqry.First;
{ Tong20.Srart_39_01(Self); }
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  DataSource2.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo38.Button201Click(Sender: TObject);
begin

  Button101Click(Self);

  DateSeparator := '-';
  ShortDateFormat := 'YYYY-MM-DD';
  LongDateFormat  := 'YYYY-MM-DD';

  Application.CreateForm(TSeok90, Seok90);
  Seok90.ShowModal;
  Seok90.Free;
//ComboBox1Change(Self);

  DateSeparator := '.';
  ShortDateFormat := 'YYYY.MM.DD';
  LongDateFormat  := 'YYYY.MM.DD';
end;

procedure TSobo38.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
end;

procedure TSobo38.Edit101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo38.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo38.Edit102KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then DBGrid101.SetFocus;
end;

procedure TSobo38.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then DBGrid101.SetFocus;
end;

procedure TSobo38.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo38.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo38.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo38.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo38.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo38.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo38.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Button101Click(Self);
  end;
end;

procedure TSobo38.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo38.DBGrid101Enter(Sender: TObject);
begin
//
end;

procedure TSobo38.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo38.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo38.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo38.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo38.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo38.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo38.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo38.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo38.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
  Memo1.Clear;
  Memo1.Lines.Add( T3_Sub82.FieldByName('Memo2').AsString );
end;

procedure TSobo38.ComboBox1Change(Sender: TObject);
var nPath: String;
begin
{ nPath := ExtractFilePath(Application.ExeName);
  //FileListBox1.Directory := nPath+'\Remote\'+nCode+'SR*.*';
  if ComboBox1.ItemIndex=0 then begin
    FileListBox1.Directory := nPath+'\Remote\'+'*SR*.*';
    DBGrid101.Visible:=True;
    DBGrid201.Visible:=False;
  end;
  if ComboBox1.ItemIndex=1 then begin
    FileListBox1.Directory := nPath+'\Remote\'+'*RV*.*';
    DBGrid101.Visible:=True;
    DBGrid201.Visible:=False;
  end;
  if ComboBox1.ItemIndex=4 then begin
    FileListBox1.Directory := nPath+'\Remote\'+'*SO*.*';
    DBGrid101.Visible:=True;
    DBGrid201.Visible:=False;
  end;
  if ComboBox1.ItemIndex=2 then begin
    FileListBox1.Directory := nPath+'\Remote\'+'*RI*.*';
    DBGrid101.Visible:=True;
    DBGrid201.Visible:=False;
  end;
  if ComboBox1.ItemIndex=3 then begin
    FileListBox1.Directory := nPath+'\Remote\'+'*INV*.*';
    DBGrid201.Visible:=True;
    DBGrid101.Visible:=False;
  end;
  FileListBox1.ItemIndex := FileListBox1.Items.Count-1; }
//FileListBox1Click(Self);
end;

procedure TSobo38.FileListBox1Click(Sender: TObject);
var
  TextfileStr : TStringList;
  p_Gname,p_Bname : String;
  X1: String;
  S : String;
  F : Textfile;
  I : Integer;
begin
{ Label101.Caption:=ExtractFileName(FileListBox1.FileName);

  Button101Click(Self);

  if(ComboBox1.ItemIndex=0)or
    (ComboBox1.ItemIndex=4)then begin
    try
      Assignfile(F, FileListBox1.FileName);
      ReSet(F);
      While not Eof(F) do begin
        Readln(F, S);
       if trim(Copy(GetSeperateStrByIndex(S, ';', 0),1,20))=nCode then begin
        nSqry.Append;
        nSqry.FieldByName('Gdate').AsString:=Copy(GetSeperateStrByIndex(S, ';', 1),1,4)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),5,2)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),7,2);

        Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
        Translate(Sqlen, '@Gcode', Copy(GetSeperateStrByIndex(S, ';', 3),1,10));
        p_Gname:=Base10.Seek_Name(Sqlen);
        if p_Gname<>'' then
        nSqry.FieldByName('Gname').AsString:=p_Gname else
        nSqry.FieldByName('Gname').AsString:=Copy(GetSeperateStrByIndex(S, ';', 3),1,10);

        Sqlen := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
        Translate(Sqlen, '@Gcode', Copy(GetSeperateStrByIndex(S, ';', 4),1,10));
        p_Bname:=Base10.Seek_Name(Sqlen);
        if p_Bname<>'' then
        nSqry.FieldByName('Bname').AsString:=p_Bname else
        nSqry.FieldByName('Bname').AsString:=Copy(GetSeperateStrByIndex(S, ';', 4),1,10);

        nSqry.FieldByName('Gsqut').AsString:=Copy(GetSeperateStrByIndex(S, ';', 7),1,09);
        nSqry.FieldByName('Grat1').AsString:=Copy(GetSeperateStrByIndex(S, ';', 8),1,03);
        nSqry.FieldByName('Gdang').AsString:=Copy(GetSeperateStrByIndex(S, ';', 9),1,09);
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='1' then nSqry.FieldByName('Pubun').AsString:='일반' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='2' then nSqry.FieldByName('Pubun').AsString:='납품' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='3' then nSqry.FieldByName('Pubun').AsString:='매절' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='4' then nSqry.FieldByName('Pubun').AsString:='현매' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='5' then nSqry.FieldByName('Pubun').AsString:='증정' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='6' then nSqry.FieldByName('Pubun').AsString:='기타';
        if Copy(GetSeperateStrByIndex(S, ';',11),1,01)='1' then nSqry.FieldByName('Jubun').AsString:='신간' else
        if Copy(GetSeperateStrByIndex(S, ';',11),1,01)='2' then nSqry.FieldByName('Jubun').AsString:='구간';
        nSqry.Post;
       end;
      end;
    finally
      CloseFile(F);
    end;
  end;

  if ComboBox1.ItemIndex=1 then begin
    try
      Assignfile(F, FileListBox1.FileName);
      ReSet(F);
      While not Eof(F) do begin
        Readln(F, S);
       if trim(Copy(GetSeperateStrByIndex(S, ';', 0),1,20))=nCode then begin
        nSqry.Append;
        nSqry.FieldByName('Gdate').AsString:=Copy(GetSeperateStrByIndex(S, ';', 1),1,4)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),5,2)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),7,2);

        Sqlen := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
        Translate(Sqlen, '@Gcode', Copy(GetSeperateStrByIndex(S, ';', 3),1,10));
        p_Bname:=Base10.Seek_Name(Sqlen);
        if p_Bname<>'' then
        nSqry.FieldByName('Bname').AsString:=p_Bname else
        nSqry.FieldByName('Bname').AsString:=Copy(GetSeperateStrByIndex(S, ';', 3),1,10);

        nSqry.FieldByName('Gsqut').AsString:=Copy(GetSeperateStrByIndex(S, ';', 7),1,09);
        nSqry.FieldByName('Grat1').AsString:=Copy(GetSeperateStrByIndex(S, ';', 4),1,03);
        nSqry.FieldByName('Gdang').AsString:=Copy(GetSeperateStrByIndex(S, ';', 5),1,09);
        nSqry.FieldByName('Pubun').AsString:='입고';
        nSqry.Post;
       end;
      end;
    finally
      CloseFile(F);
    end;
  end;

  if ComboBox1.ItemIndex=2 then begin
    try
      Assignfile(F, FileListBox1.FileName);
      ReSet(F);
      While not Eof(F) do begin
        Readln(F, S);
       if trim(Copy(GetSeperateStrByIndex(S, ';', 0),1,20))=nCode then begin
        nSqry.Append;
        nSqry.FieldByName('Gdate').AsString:=Copy(GetSeperateStrByIndex(S, ';', 1),1,4)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),5,2)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),7,2);

        Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
        Translate(Sqlen, '@Gcode', Copy(GetSeperateStrByIndex(S, ';', 3),1,10));
        p_Gname:=Base10.Seek_Name(Sqlen);
        if p_Gname<>'' then
        nSqry.FieldByName('Gname').AsString:=p_Gname else
        nSqry.FieldByName('Gname').AsString:=Copy(GetSeperateStrByIndex(S, ';', 3),1,10);

        Sqlen := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
        Translate(Sqlen, '@Gcode', Copy(GetSeperateStrByIndex(S, ';', 4),1,10));
        p_Bname:=Base10.Seek_Name(Sqlen);
        if p_Bname<>'' then
        nSqry.FieldByName('Bname').AsString:=p_Bname else
        nSqry.FieldByName('Bname').AsString:=Copy(GetSeperateStrByIndex(S, ';', 4),1,10);

        nSqry.FieldByName('Gsqut').AsString:=Copy(GetSeperateStrByIndex(S, ';',10),1,09);
        nSqry.FieldByName('Grat1').AsString:=Copy(GetSeperateStrByIndex(S, ';', 5),1,03);
        nSqry.FieldByName('Gdang').AsString:=Copy(GetSeperateStrByIndex(S, ';', 6),1,09);
        nSqry.FieldByName('Pubun').AsString:='반품';
        nSqry.Post;
       end;
      end;
    finally
      CloseFile(F);
    end;
  end;

  if ComboBox1.ItemIndex=3 then begin
    try
      Assignfile(F, FileListBox1.FileName);
      ReSet(F);
      While not Eof(F) do begin
        Readln(F, S);
       if trim(Copy(GetSeperateStrByIndex(S, ';', 0),1,20))=nCode then begin
        mSqry.Append;
        mSqry.FieldByName('Gdate').AsString:=Copy(GetSeperateStrByIndex(S, ';', 1),1,4)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),5,2)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),7,2);

        Sqlen := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
        Translate(Sqlen, '@Gcode', Copy(GetSeperateStrByIndex(S, ';', 4),1,10));
        p_Bname:=Base10.Seek_Name(Sqlen);
        if p_Bname<>'' then
        mSqry.FieldByName('Bname').AsString:=p_Bname else
        mSqry.FieldByName('Bname').AsString:=Copy(GetSeperateStrByIndex(S, ';', 4),1,10);

        mSqry.FieldByName('Gqut1').AsString:=Copy(GetSeperateStrByIndex(S, ';', 5),1,09);
        mSqry.FieldByName('Gqut2').AsString:=Copy(GetSeperateStrByIndex(S, ';', 6),1,09);
        mSqry.Post;
       end;
      end;
    finally
      CloseFile(F);
    end;
  end;

  nSqry.First;
  mSqry.First; }
end;

procedure TSobo38.SeperateStr(Str, SubStr : String; StrList : TStrings);
var
 Index : Integer;
begin
 Index := Pos(SubStr, Str);
 if Index > 0 then
 begin
   StrList.Add(Copy(Str, 1, Index-1));
   SeperateStr(String(PChar(@Str[Index+1])), SubStr, StrList);
 end else
 begin
   StrList.Add(Str);
 end;
end;

function TSobo38.GetSeperateStrByIndex(Str, SubStr : String; Index : LongInt) : String;
var
 StrList : TStringList;
begin
 StrList := TStringList.Create;
 try
   SeperateStr(Str, SubStr, StrList);
   if Index < StrList.Count then
     Result := StrList[Index]
   else
     Result := '';
 finally
   StrList.Free;
 end;
end;

procedure TSobo38.FlatButton1Click(Sender: TObject);
var
  TextfileStr : TStringList;
  p_Gname,p_Bname : String;
  X1: String;
  S : String;
  F : Textfile;
  I : Integer;
begin
    try
      for I:=0 to Memo1.Lines.Count-1 do begin
        S:=Memo1.Lines.Strings[I];
        nSqry.Append;
        nSqry.FieldByName('Gdate').AsString:=Copy(GetSeperateStrByIndex(S, ';', 1),1,4)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),5,2)+'.'+
                                             Copy(GetSeperateStrByIndex(S, ';', 1),7,2);

        Sqlen := 'Select Gname From G1_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
        Translate(Sqlen, '@Gcode', Copy(GetSeperateStrByIndex(S, ';', 3),1,10));
        p_Gname:=Base10.Seek_Name(Sqlen);
        if p_Gname<>'' then
        nSqry.FieldByName('Gname').AsString:=p_Gname else
        nSqry.FieldByName('Gname').AsString:=Copy(GetSeperateStrByIndex(S, ';', 3),1,10);

        Sqlen := 'Select Gname From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
        Translate(Sqlen, '@Gcode', Copy(GetSeperateStrByIndex(S, ';', 4),1,10));
        p_Bname:=Base10.Seek_Name(Sqlen);
        if p_Bname<>'' then
        nSqry.FieldByName('Bname').AsString:=p_Bname else
        nSqry.FieldByName('Bname').AsString:=Copy(GetSeperateStrByIndex(S, ';', 4),1,10);

        nSqry.FieldByName('Gsqut').AsString:=Copy(GetSeperateStrByIndex(S, ';', 7),1,09);
        nSqry.FieldByName('Grat1').AsString:=Copy(GetSeperateStrByIndex(S, ';', 8),1,03);
        nSqry.FieldByName('Gdang').AsString:=Copy(GetSeperateStrByIndex(S, ';', 9),1,09);
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='1' then nSqry.FieldByName('Pubun').AsString:='일반' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='2' then nSqry.FieldByName('Pubun').AsString:='납품' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='3' then nSqry.FieldByName('Pubun').AsString:='매절' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='4' then nSqry.FieldByName('Pubun').AsString:='현매' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='5' then nSqry.FieldByName('Pubun').AsString:='증정' else
        if Copy(GetSeperateStrByIndex(S, ';',10),1,01)='6' then nSqry.FieldByName('Pubun').AsString:='기타';
        if Copy(GetSeperateStrByIndex(S, ';',11),1,01)='1' then nSqry.FieldByName('Jubun').AsString:='신간' else
        if Copy(GetSeperateStrByIndex(S, ';',11),1,01)='2' then nSqry.FieldByName('Jubun').AsString:='구간';
        nSqry.Post;
      end;
    finally
    end;
end;

procedure TSobo38.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo38.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

end.
