unit Subu66;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, TFlatCheckBoxUnit,
  ToolEdit;

type
  TSobo66 = class(TForm)
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
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Edit109: TFlatEdit;
    Edit110: TFlatEdit;
    Panel103: TFlatPanel;
    Edit111: TFlatEdit;
    Edit112: TFlatEdit;
    DateEdit1: TDateEdit;
    DateEdit2: TDateEdit;
    Button700: TFlatButton;
    Button701: TFlatButton;
    Button702: TFlatButton;
    Button703: TFlatButton;
    Button704: TFlatButton;
    Button709: TFlatButton;
    CheckBox2: TFlatCheckBox;
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
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit2ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button700Click(Sender: TObject);
    procedure Button701Click(Sender: TObject);
    procedure Button702Click(Sender: TObject);
    procedure Button703Click(Sender: TObject);
    procedure Button704Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo66: TSobo66;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo66.FormActivate(Sender: TObject);
begin
  nForm:='66';
  nSqry:=Base10.T6_Sub61;
  mSqry:=Base10.T6_Sub62;
end;

procedure TSobo66.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo66.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo66:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo66.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo66.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_66_01(Self);
  end;
end;

procedure TSobo66.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo66.Button004Click(Sender: TObject);
begin
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
  Tong20.Srart_66_01(Self);
  Tong20.Srart_66_02(Self);
  Tong20.Chang_00_01('66');
  Edit101.SetFocus;
end;

procedure TSobo66.Button005Click(Sender: TObject);
begin
  Tong20.Chang_00_02('66');
end;

procedure TSobo66.Button006Click(Sender: TObject);
begin
  T00:=1;
  Button201Click(Self);
end;

procedure TSobo66.Button007Click(Sender: TObject);
begin
  T00:=0;
  Button201Click(Self);
end;

procedure TSobo66.Button008Click(Sender: TObject);
begin
  Tong20.Zoom_Int_01('66');
end;

procedure TSobo66.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('66');
end;

procedure TSobo66.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo66.Button011Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid201, Caption);
end;

procedure TSobo66.Button012Click(Sender: TObject);
begin
  oSqry:=mSqry;
  Base10.ColumnX2(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo66.Button013Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX2(oSqry,DBGrid201,ProgressBar1);
end;

procedure TSobo66.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('66-01');
end;

procedure TSobo66.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('66-02');
end;

procedure TSobo66.Button016Click(Sender: TObject);
begin
  Tong40.print_66_01(Self);
end;

procedure TSobo66.Button017Click(Sender: TObject);
begin
  Tong40.print_66_02(Self);
end;

procedure TSobo66.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo66.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo66.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo66.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont1(DBGrid101,DBGrid201,StBar101,StBar201);
end;

procedure TSobo66.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo66.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo66.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo66.Button101Click(Sender: TObject);
var St1,St2,St3,St4: String;
    St9: Integer;
begin
  if Base10.Seek_Ggeo(Edit111.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  Base10.OpenShow(nSqry);
  Base10.OpenShow(mSqry);
  Screen.Cursor:=crHourGlass;
  DataSource2.Enabled:=False;
  DataSource1.Enabled:=False;

  St9:=1;
  St4:=Edit103.Text;
  While St4<>'' do begin
    St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
         'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
         'Pubun'+'<>'+#39+'증정'+#39+' and '+
         'Scode'+' ='+#39+'X'+#39+' and '+
         'Gcode'+' ='+#39+St4+#39;
    if Edit111.Text<>'' Then
    St1:=St1+' and '+
         'Hcode'+' ='+#39+Edit111.Text+#39;

    if(CheckBox2.Checked=True)then
    St1:=St1+' and ((Scode='+#39+'X'+#39+' and Gcode<>'+#39+'00001'+#39+')'+
             ' or (Scode='+#39+'Y'+#39+')'+' or (Scode='+#39+'Z'+#39+'))';

    {-S1_Ssub-}
    Sqlen :=
    'Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum '+
    'From S1_Ssub Where '+St1+
    'Group By Bcode,Scode,Gubun,Pubun ';

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

      St2:=SGrid.Cells[ 0,List1];
      St3:='';
      St4:='';
    //St3:=Base10.Seek_Code(St2,'B',Edit111.Text);

      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit111.Text,St2]),[loCaseInsensitive])=true then begin
        St3:=Base10.G4_Book.FieldByName('Gname').AsString;
        St4:=Base10.G4_Book.FieldByName('Gubun').AsString;
      end;

      if St3='' then begin
      Sqlen := 'Select Gname,Gubun From G4_Book Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St2);
      Translate(Sqlen, '@Hcode', Edit111.Text);
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        Base10.Socket.MakeData;
        St3:=Base10.Socket.GetData(1, 1);
        St4:=Base10.Socket.GetData(1, 2);
      end;
      end;

      if nSqry.Locate('Gcode',St2,[loCaseInsensitive])=False then begin
        nSqry.Append;
        nSqry.FieldByName('Gcode').AsString:=St2;
        nSqry.FieldByName('Gname').AsString:=St3;
        nSqry.FieldByName('Gubun').AsString:=St4;
      end;

      nSqry.Edit;
      St3:=SGrid.Cells[ 2,List1];
      if St3='출고' Then begin
        if St9=1 Then
        nSqry.FieldByName('Giqut').AsFloat:=nSqry.FieldByName('Giqut').AsFloat+T01
        else
        if St9=2 Then
        nSqry.FieldByName('Goqut').AsFloat:=nSqry.FieldByName('Goqut').AsFloat+T01
        else
        if St9=3 Then
        nSqry.FieldByName('Gjqut').AsFloat:=nSqry.FieldByName('Gjqut').AsFloat+T01
        else
        if St9=4 Then
        nSqry.FieldByName('Gbqut').AsFloat:=nSqry.FieldByName('Gbqut').AsFloat+T01;
      end else
      if St3='반품' Then begin
        if St9=1 Then
        nSqry.FieldByName('Gisum').AsFloat:=nSqry.FieldByName('Gisum').AsFloat+T01
        else
        if St9=2 Then
        nSqry.FieldByName('Gosum').AsFloat:=nSqry.FieldByName('Gosum').AsFloat+T01
        else
        if St9=3 Then
        nSqry.FieldByName('Gjsum').AsFloat:=nSqry.FieldByName('Gjsum').AsFloat+T01
        else
        if St9=4 Then
        nSqry.FieldByName('Gbsum').AsFloat:=nSqry.FieldByName('Gbsum').AsFloat+T01;
      end;
      nSqry.Post;
    end;
    ProgressBar1.Position:=0;
    St9:=St9+1;
    if St9=1 Then St4:=Edit103.Text;
    if St9=2 Then St4:=Edit105.Text;
    if St9=3 Then St4:=Edit107.Text;
    if St9=4 Then St4:=Edit109.Text;
    if St9>4 Then St4:='';
  end;

  Base10.SpaceDel(nSqry,'Gcode','Gname');
  nSqry.First;
  While nSqry.EOF=False do begin
    St3:=nSqry.FieldByName('Gubun').AsString;
    St4:=nSqry.FieldByName('Gubun').AsString;

    if mSqry.Locate('Gcode',St3,[loCaseInsensitive])=False then begin

      Sqlen := 'Select Gname From G4_Gbun Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St3);
      Translate(Sqlen, '@Hcode', Edit111.Text);
      St4:=Base10.Seek_Name(Sqlen);

      mSqry.Append;
      mSqry.FieldByName('Gcode').AsString:=St3;
      mSqry.FieldByName('Gname').AsString:=St4;
    end;

    mSqry.Edit;
    mSqry.FieldByName('Giqut').AsFloat:=
    mSqry.FieldByName('Giqut').AsFloat+nSqry.FieldByName('Giqut').AsFloat;
    mSqry.FieldByName('Gisum').AsFloat:=
    mSqry.FieldByName('Gisum').AsFloat+nSqry.FieldByName('Gisum').AsFloat;
    mSqry.FieldByName('Goqut').AsFloat:=
    mSqry.FieldByName('Goqut').AsFloat+nSqry.FieldByName('Goqut').AsFloat;
    mSqry.FieldByName('Gosum').AsFloat:=
    mSqry.FieldByName('Gosum').AsFloat+nSqry.FieldByName('Gosum').AsFloat;
    mSqry.FieldByName('Gjqut').AsFloat:=
    mSqry.FieldByName('Gjqut').AsFloat+nSqry.FieldByName('Gjqut').AsFloat;
    mSqry.FieldByName('Gjsum').AsFloat:=
    mSqry.FieldByName('Gjsum').AsFloat+nSqry.FieldByName('Gjsum').AsFloat;
    mSqry.FieldByName('Gbqut').AsFloat:=
    mSqry.FieldByName('Gbqut').AsFloat+nSqry.FieldByName('Gbqut').AsFloat;
    mSqry.FieldByName('Gbsum').AsFloat:=
    mSqry.FieldByName('Gbsum').AsFloat+nSqry.FieldByName('Gbsum').AsFloat;
    mSqry.Post;
    nSqry.Next;
  end;

  nSqry.IndexName := 'IDX'+'GCODE'+'DOWN';
  mSqry.IndexName := 'IDX'+'GCODE'+'DOWN';
  nSqry.First;
  mSqry.First;
  Tong20.Srart_66_01(Self);
  Tong20.Srart_66_02(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource2.Enabled:=True;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo66.Button201Click(Sender: TObject);
var St1: String;
begin
  Refresh;
  if(T00=0)Then begin
    Button101.Caption:=mSqry.FieldByName('Gname').AsString;
    St1:='Gubun'+' like '+#39+mSqry.FieldByName('Gcode').AsString+'%'+#39;
    nSqry.Filter:=St1;
    nSqry.Filtered:=True;
  end;
  if(T00=1)Then begin
    Button101.Caption:='';
    nSqry.Filtered:=False;
  end;
  Tong20.Srart_66_02(Self);
end;

procedure TSobo66.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit104.Focused=True)and(Edit104.SelStart=24)and(Length(Trim(Edit104.Text))=24))or
    ((Edit106.Focused=True)and(Edit106.SelStart=24)and(Length(Trim(Edit106.Text))=24))or
    ((Edit108.Focused=True)and(Edit108.SelStart=24)and(Length(Trim(Edit108.Text))=24))or
    ((Edit110.Focused=True)and(Edit110.SelStart=24)and(Length(Trim(Edit110.Text))=24))or
    ((Edit112.Focused=True)and(Edit112.SelStart=24)and(Length(Trim(Edit112.Text))=24))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo66.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo66.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo66.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo66.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo66.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if Edit112.Focused=True Then begin
       Edit111.Text:='';
    if Edit112.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit112.Text;
    Seak80.FilterTing(Edit112.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit111.Text:=Seak80.Query1Gcode.AsString;
      Edit112.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit111.Text:=Seak80.Query1Gcode.AsString;
      Edit112.Text:=Seak80.Query1Gname.AsString;
    end;
    end;
  end else
  if Edit104.Focused=True Then begin
       Edit103.Text:='';
    if Edit104.Text<>'' Then begin
    Seek10.Edit1.Text:=Edit104.Text;
    Seek10.FilterTing(Edit104.Text,Edit111.Text);
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
  if Edit106.Focused=True Then begin
       Edit105.Text:='';
    if Edit106.Text<>'' Then begin
    Seek10.Edit1.Text:=Edit106.Text;
    Seek10.FilterTing(Edit106.Text,Edit111.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit105.Text:=Seek10.Query1Gcode.AsString;
      Edit106.Text:=Seek10.Query1Gname.AsString;
    end else
    if Seek10.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit105.Text:=Seek10.Query1Gcode.AsString;
      Edit106.Text:=Seek10.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if Edit108.Focused=True Then begin
       Edit107.Text:='';
    if Edit108.Text<>'' Then begin
    Seek10.Edit1.Text:=Edit108.Text;
    Seek10.FilterTing(Edit108.Text,Edit111.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seek10.Query1Gcode.AsString;
      Edit108.Text:=Seek10.Query1Gname.AsString;
    end else
    if Seek10.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit107.Text:=Seek10.Query1Gcode.AsString;
      Edit108.Text:=Seek10.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if Edit110.Focused=True Then begin
       Edit109.Text:='';
    if Edit110.Text<>'' Then begin
    Seek10.Edit1.Text:=Edit110.Text;
    Seek10.FilterTing(Edit110.Text,Edit111.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      Edit109.Text:=Seek10.Query1Gcode.AsString;
      Edit110.Text:=Seek10.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seek10.ShowModal=mrOK Then begin
      Edit109.Text:=Seek10.Query1Gcode.AsString;
      Edit110.Text:=Seek10.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo66.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo66.DBGrid101KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo66.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if nSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo66.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo66.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if mSqry.Active=True Then begin
  if Key=VK_ESCAPE Then Edit101.SetFocus;
  end;
end;

procedure TSobo66.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(mSqry,Column);
end;

procedure TSobo66.DBGrid201TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo66.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo66.DataSource2DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(mSqry.RecNo)+'/'+IntToStr(mSqry.RecordCount);
end;

procedure TSobo66.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo66.DateEdit2ButtonClick(Sender: TObject);
begin
  DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo66.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo66.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo66.Button700Click(Sender: TObject);
begin
    Seak80.Edit1.Text:='';
    Seak80.FilterTing('');
    if Seak80.Query1.RecordCount=1 Then begin
      Edit111.Text:=Seak80.Query1Gcode.AsString;
      Edit112.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      Edit111.Text:=Seak80.Query1Gcode.AsString;
      Edit112.Text:=Seak80.Query1Gname.AsString;
    end;
end;

procedure TSobo66.Button701Click(Sender: TObject);
begin
    Seek10.Edit1.Text:='';
    Seek10.FilterTing(' ',Edit111.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      Edit103.Text:=Seek10.Query1Gcode.AsString;
      Edit104.Text:=Seek10.Query1Gname.AsString;
    end else
    if Seek10.ShowModal=mrOK Then begin
      Edit103.Text:=Seek10.Query1Gcode.AsString;
      Edit104.Text:=Seek10.Query1Gname.AsString;
    end;
end;

procedure TSobo66.Button702Click(Sender: TObject);
begin
    Seek10.Edit1.Text:='';
    Seek10.FilterTing(' ',Edit111.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      Edit105.Text:=Seek10.Query1Gcode.AsString;
      Edit106.Text:=Seek10.Query1Gname.AsString;
    end else
    if Seek10.ShowModal=mrOK Then begin
      Edit105.Text:=Seek10.Query1Gcode.AsString;
      Edit106.Text:=Seek10.Query1Gname.AsString;
    end;
end;

procedure TSobo66.Button703Click(Sender: TObject);
begin
    Seek10.Edit1.Text:='';
    Seek10.FilterTing(' ',Edit111.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      Edit107.Text:=Seek10.Query1Gcode.AsString;
      Edit108.Text:=Seek10.Query1Gname.AsString;
    end else
    if Seek10.ShowModal=mrOK Then begin
      Edit107.Text:=Seek10.Query1Gcode.AsString;
      Edit108.Text:=Seek10.Query1Gname.AsString;
    end;
end;

procedure TSobo66.Button704Click(Sender: TObject);
begin
    Seek10.Edit1.Text:='';
    Seek10.FilterTing(' ',Edit111.Text);
    if Seek10.Query1.RecordCount=1 Then begin
      Edit109.Text:=Seek10.Query1Gcode.AsString;
      Edit110.Text:=Seek10.Query1Gname.AsString;
    end else
    if Seek10.ShowModal=mrOK Then begin
      Edit109.Text:=Seek10.Query1Gcode.AsString;
      Edit110.Text:=Seek10.Query1Gname.AsString;
    end;
end;

end.
