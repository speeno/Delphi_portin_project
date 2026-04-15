unit Subu14_1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  TFlatRadioButtonUnit, Grids, DBGridEh, ExtCtrls, TFlatPanelUnit,
  TFlatButtonUnit, StdCtrls, TFlatComboBoxUnit, Db, DBClient, Mylabel,
  TFlatEditUnit, dxCore, dxButtons, ComCtrls, TFlatProgressBarUnit,
  CornerButton, ToolEdit, Mask, TFlatMaskEditUnit, TFlatCheckBoxUnit;

type
  TSobo14_1 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    T1_Sub81: TClientDataSet;
    T1_Sub81ID: TFloatField;
    T1_Sub81HCODE: TStringField;
    T1_Sub81GCODE: TStringField;
    T1_Sub81GNAME: TStringField;
    T1_Sub81GISBN: TStringField;
    T1_Sub81GPOST: TStringField;
    T1_Sub81OPOST: TStringField;
    T1_Sub81GSQUT: TFloatField;
    Panel001: TFlatPanel;
    Panel101: TFlatPanel;
    Edit201: TFlatComboBox;
    Panel002: TFlatPanel;
    Label100: TmyLabel3d;
    Edit101: TFlatEdit;
    Edit102: TFlatEdit;
    Button701: TFlatButton;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    Panel007: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    ProgressBar1: TProgressBar;
    dxButton1: TdxButton;
    Edit202: TFlatEdit;
    dxButton2: TdxButton;
    DBGrid101: TDBGridEh;
    FlatPanel1: TFlatPanel;
    Edit103: TFlatMaskEdit;
    DateEdit1: TDateEdit;
    CheckBox1: TFlatCheckBox;
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
    procedure Button709Click(Sender: TObject);
    procedure Button200Click(Sender: TObject);
    procedure Button300Click(Sender: TObject);
    procedure Button701Click(Sender: TObject);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
    procedure Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit115KeyPress(Sender: TObject; var Key: Char);
    procedure Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DBGrid101TitleClick(Column: TColumnEh);
    procedure T1_Sub81BeforePost(DataSet: TDataSet);
    procedure T1_Sub81BeforeClose(DataSet: TDataSet);
    procedure DBGrid101DrawColumnCell(Sender: TObject; const Rect: TRect;
      DataCol: Integer; Column: TColumnEh; State: TGridDrawState);
    procedure CheckBox1Click(Sender: TObject);
  private
    { Private declarations }
  public
    //fCp_Code:출판사코드, fBK_Name: 사용자가 입력한 도서명
    function Get_Book_Code(fCp_Code, fBk_Name: string): string;
  end;

var
  Sobo14_1: TSobo14_1;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo14_1.FormActivate(Sender: TObject);
begin
  nForm:='14_1';
  nSqry:=T1_Sub81;
end;

procedure TSobo14_1.FormShow(Sender: TObject);
begin
{ Base10.G7_Ggeo.First;
  While Base10.G7_Ggeo.EOF=False do begin
    Edit101.Items.Add(Base10.G7_Ggeo.FieldByName('Gname').AsString);
    Base10.G7_Ggeo.Next;
  end;
  Edit101.ItemIndex:=0; }
//Button709Click(Self);
  Edit103.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo14_1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo14_1:=nil;
  Base10.OpenExit(nSqry);
end;

procedure TSobo14_1.Button001Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button002Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button003Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button008Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button009Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button010Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo14_1.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button014Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button015Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button016Click(Sender: TObject);
begin
  Tong40.print_14_11(Self);
end;

procedure TSobo14_1.Button017Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button021Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button101Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button709Click(Sender: TObject);
var St1,St2: String;
begin
  if Base10.Seek_Ggeo(Edit101.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;

  Sqlen := 'Select Gcode From G7_Ggeo Where '+D_Select+'Gname=''@Gname'' ';
  Translate(Sqlen, '@Gname', Edit102.Text);
  Label100.Caption:=Base10.Seek_Name(Sqlen);

  //2024.04.06
  //Sqlen := 'Select Id,Gcode,Gname,Gisbn,Gpost,Opost From G4_Book Where '+D_Select;
  //           'Hcode=''@Hcode'' Order by Gcode,Id ' ;
  //Translate(Sqlen, '@Hcode', Label100.Caption);

  Sqlen := 'Select Id,Gcode,Gname,Gisbn,Gpost,Opost From G4_Book Where '+D_Select +
           'Hcode=''@Hcode''  ' ;

  if Edit201.ItemIndex <> -1 then
  begin
    if Edit201.ItemIndex = 0 then     //ISBN
    begin
       if Edit202.Text <> '' then
       begin
         if Length(Edit202.Text) = 4 then
         //Sqlen := Sqlen + ' And  RIGHT(Gisbn, 4) = '+#39+Edit202.Text+#39
         Sqlen := Sqlen + ' And  Gisbn like '+ QuotedStr('%' + Edit202.Text)
         else
         Sqlen := Sqlen + ' And Gisbn like '+#39+'%'+Edit202.Text+'%'+#39;
       end;
    end
    else if Edit201.ItemIndex = 1 then  //도서명
    begin
       if Edit202.Text <> '' then
       Sqlen := Sqlen + ' And Gname like '+#39+'%'+Edit202.Text+'%'+#39;
    end
    else if Edit201.ItemIndex = 2 then  //도서코드
    begin
       if Edit202.Text <> '' then
       Sqlen := Sqlen + ' And Gcode like '+#39+'%'+Edit202.Text+'%'+#39;
    end;
  end;

  Sqlen := Sqlen +
           ' Order by Gcode,Id ' ;
  Translate(Sqlen, '@Hcode', Label100.Caption);

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  Tong40.SetTring02('','Edit103.Text','','','',Label100.Caption);
//Tong40.SetTring02('','9999.99.99','','','',Label100.Caption);
  sSqry.First;
  While sSqry.EOF=False do begin
    if nSqry.Locate('Gcode',sSqry.FieldByName('Gcode').Value,[loCaseInsensitive])=true then begin
    nSqry.Edit;
    nSqry.FieldByName('Gsqut').AsFloat:=sSqry.FieldByName('GsumY').AsFloat;
    nSqry.Post;
    end;
    sSqry.Next;
  end;

  nSqry.First;

  Edit202.SetFocus;
//DBGrid101.SetFocus;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=T1_Sub81BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo14_1.Button200Click(Sender: TObject);
begin
//
end;

procedure TSobo14_1.Button300Click(Sender: TObject);
var St1,St2:integer;
    St0:String;
begin
  //--도서코드 중복자료 보기--//
{ select distinct Gcode from G4_Book
  where hcode='122'
  group by Gcode
  having Count(*) > 1 }

  //--도서코드 중복자료 코드변경하기--//
  nSqry.First;
  While nSqry.EOF=False do begin
    Sqlen := 'Select count(*) From G4_Book Where '+'Hcode=''@Hcode'' and Gcode=''@Gcode''';
    Translate(Sqlen, '@Hcode', Label100.Caption);
    Translate(Sqlen, '@Gcode', T1_Sub81Gcode.AsString);
    St1:=StrToInt(Base10.Seek_Name(Sqlen));

    if St1 > 1 then begin
       St0:=T1_Sub81Gcode.AsString+'-1';

       Sqlen := 'Select count(*) From G4_Book Where '+'Hcode=''@Hcode'' and Gcode=''@Gcode''';
       Translate(Sqlen, '@Hcode', Label100.Caption);
       Translate(Sqlen, '@Gcode', St0);
       St2:=StrToInt(Base10.Seek_Name(Sqlen));
       if St2 > 1 then begin
         //
       end else begin
         Sqlen := 'UPDATE G4_Book SET '+
         'Gcode=''@Gcode'' '+
         'WHERE Hcode=''@Hcode'' and Id=@Id ';

         Translate(Sqlen, '@Hcode', Label100.Caption);
         Translate(Sqlen, '@Gcode', St0);
         Translate(Sqlen, '@Id', T1_Sub81Id.AsString);

         Base10.Socket.RunSQL(Sqlen);
         Base10.Socket.BusyLoop;
         if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);
       end;
    end;
    nSqry.Next;
  end;
end;

procedure TSobo14_1.Button701Click(Sender: TObject);
begin
    Seak80.Edit1.Text:='';
    Seak80.FilterTing('');
    if Seak80.Query1.RecordCount=1 Then begin
      Edit101.Text:=Seak80.Query1Gcode.AsString;
      Edit102.Text:=Seak80.Query1Gname.AsString;
      Button709Click(Self);
    end else
    if Seak80.ShowModal=mrOK Then begin
      Edit101.Text:=Seak80.Query1Gcode.AsString;
      Edit102.Text:=Seak80.Query1Gname.AsString;
      Button709Click(Self);
    end;
end;

procedure TSobo14_1.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
       Edit101.Text:='';
    if Edit102.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit102.Text;
    Seak80.FilterTing(Edit102.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit101.Text:=Seak80.Query1Gcode.AsString;
      Edit102.Text:=Seak80.Query1Gname.AsString;
      Button709Click(Self);
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit101.Text:=Seak80.Query1Gcode.AsString;
      Edit102.Text:=Seak80.Query1Gname.AsString;
      Button709Click(Self);
    end;
    end;
  end;
end;

procedure TSobo14_1.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

//fCp_Code:출판사코드, fBK_Name: 사용자가 입력한 도서명
function TSobo14_1.Get_Book_Code(fCp_Code, fBk_Name: string): string;
begin
  with Base10.ZMySqlQuery1 do
  begin
    Close;
    with Sql do
    begin
      Clear;
      Add('select gcode from G4_Book');
      Add(' where hcode = :hcode');
      Add('   and gname like :gname');
    end;
    ParamByName('hcode').AsString := fCp_Code;
    ParamByName('gname').AsString := '%' + fBk_Name + '%';
    Open;
    Result := FieldByName('gcode').AsString;
  end;
end;

procedure TSobo14_1.Edit115KeyPress(Sender: TObject; var Key: Char);
var
  pBk_Code: string;
begin
  if Key=#13 Then
  begin
    if Edit201.Text='ISBN' then
    begin
      //nSqry.Locate('Gisbn',Edit202.Text,[loPartialKey])
      if Length(Edit202.Text) = 4 then
      begin
        nSqry.Filtered := False;
        nSqry.Filter :=  'Gisbn like ' + QuotedStr('%' + Edit202.Text);
        nSqry.Filtered := True;
      end
      else
      begin
        nSqry.Filtered := False;
        nSqry.Filter :=  'Gisbn like ' + QuotedStr('%' + Edit202.Text + '%');
        nSqry.Filtered := True;
      end;
    end
    else if Edit201.Text='도서명' then
    begin
      pBk_Code := Get_Book_Code(Label100.Caption, Edit202.Text);
      if pBk_Code = '' then
      begin
        ShowMessage('출판사코드, 도서명을 확인하시기 바랍니다');
        Exit;
      end;
      nSqry.Locate('gcode', pBk_Code, [loPartialKey]);
//      nSqry.Locate('Gname',Edit202.Text,[loPartialKey]);
    end
    else if Edit201.Text='도서코드' then
      nSqry.Locate('Gcode',Edit202.Text,[loPartialKey]);

    Edit202.Text:='';
    if nSqry.FieldByName('Gpost').AsString='' then
    begin
      DBGrid101.SetFocus;
      DBGrid101.SelectedIndex:=4;
      DBGrid101.Columns.Items[4].Grid.EditorMode:=True;
    end;
  end;
end;

procedure TSobo14_1.Edit115KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo14_1.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
begin
{ if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=0 Then begin
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end; }
end;

procedure TSobo14_1.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    nSqry.Post;
    Edit202.SetFocus;
  end;
  if sColumn=False Then begin
    if nSqry.IsEmpty=False Then
    if Key=VK_ESCAPE Then Edit202.SetFocus;
  end; end;
end;

procedure TSobo14_1.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo14_1.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit103.Text);
end;

procedure TSobo14_1.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit103.Text :=DateToStr(ADate);
end;

procedure TSobo14_1.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo14_1.T1_Sub81BeforePost(DataSet: TDataSet);
begin

    Sqlen := 'UPDATE G4_Book SET '+
    'Gisbn=''@Gisbn'',Gpost=''@Gpost'',Opost=''@Opost'' '+
    'WHERE Hcode=''@Hcode'' and Gcode=''@Gcode'' ';

    Translate(Sqlen, '@Hcode', Label100.Caption);
    Translate(Sqlen, '@Gcode', T1_Sub81Gcode.AsString);
    Translate(Sqlen, '@Gpost', T1_Sub81Gpost.AsString);
    Translate(Sqlen, '@Gisbn', T1_Sub81Gisbn.AsString);
    Translate(Sqlen, '@Opost', T1_Sub81Opost.AsString);

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

end;

procedure TSobo14_1.T1_Sub81BeforeClose(DataSet: TDataSet);
begin
  With T1_Sub81 do
  if(State in dsEditModes)Then Post;
end;

procedure TSobo14_1.DBGrid101DrawColumnCell(Sender: TObject;
  const Rect: TRect; DataCol: Integer; Column: TColumnEh;
  State: TGridDrawState);
begin
  if (Rect.Top = DBGrid101.CellRect(DBGrid101.Col,DBGrid101.Row).Top) and (not (gdFocused in State) or not DBGrid101.Focused) then
    DBGrid101.Canvas.Brush.Color := clAqua;
  DBGrid101.DefaultDrawColumnCell(Rect,DataCol,Column,State);
end;

procedure TSobo14_1.CheckBox1Click(Sender: TObject);
begin
  if CheckBox1.Checked=True then
  DBGrid101.Columns.Items[3].ReadOnly:=False
  else
  DBGrid101.Columns.Items[3].ReadOnly:=True;
end;

end.
