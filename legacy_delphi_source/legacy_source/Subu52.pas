unit Subu52;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ToolEdit, dxCore,
  dxButtons, DBGridEh, CornerButton;

type
  TSobo52 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel001: TFlatPanel;
    Panel002: TFlatPanel;
    Panel007: TFlatPanel;
    Panel008: TFlatPanel;
    Panel009: TFlatPanel;
    Panel010: TFlatPanel;
    Panel101: TFlatPanel;
    ProgressBar0: TFlatProgressBar;
    ProgressBar1: TProgressBar;
    Button101: TFlatButton;
    Label101: TmyLabel3d;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatMaskEdit;
    Panel104: TFlatPanel;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Button201: TFlatButton;
    DateEdit1: TDateEdit;
    DateEdit2: TDateEdit;
    Button700: TFlatButton;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    DBGrid101: TDBGridEh;
    dxButton1: TdxButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    Button801: TFlatButton;
    Button802: TFlatButton;
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
    procedure Edit112KeyPress(Sender: TObject; var Key: Char);
    procedure Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit113KeyPress(Sender: TObject; var Key: Char);
    procedure Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure Edit114KeyPress(Sender: TObject; var Key: Char);
    procedure Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101Exit(Sender: TObject);
    procedure DBGrid201Exit(Sender: TObject);
    procedure DBGrid101Enter(Sender: TObject);
    procedure DBGrid201Enter(Sender: TObject);
    procedure DBGrid101KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid201KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure DBGrid101TitleClick(Column: TColumnEh);
    procedure DBGrid201TitleClick(Column: TColumnEh);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit2ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
    procedure Button700Click(Sender: TObject);
    procedure Button801Click(Sender: TObject);
    procedure Button802Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo52: TSobo52;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo52.FormActivate(Sender: TObject);
begin
  nForm:='52';
  nSqry:=Base10.T5_Sub21;
  mSqry:=Base10.T5_Sub22;
end;

procedure TSobo52.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo52.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo52:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo52.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo52.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_52_01(Self);
  end;
end;

procedure TSobo52.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo52.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button008Click(Sender: TObject);
begin
  Tong20.Zoom_Int_01('52');
end;

procedure TSobo52.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('52');
end;

procedure TSobo52.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo52.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo52.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('52-01');
end;

procedure TSobo52.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('52-02');
end;

procedure TSobo52.Button016Click(Sender: TObject);
begin
  Tong40.print_52_01(Self);
end;

procedure TSobo52.Button017Click(Sender: TObject);
begin
{ Tong40.print_52_02(Self); }
end;

procedure TSobo52.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont4(DBGrid101);
end;

procedure TSobo52.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Button101Click(Sender: TObject);
var St1,St2: String;
begin
  if Base10.Seek_Ggeo(Edit107.Text)='X' Then Exit;

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;

  Scode:='B';
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Scode'+' ='+#39+Scode+#39;

  St2:=' Order By Gdate,Gcode';

  {-Sg_Csum-}
  Sqlen := 'Select * From Sg_Csum Where '+D_Select+St1+St2;

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

    St2:='';

    if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    St2:=Base10.G4_Book.FieldByName('Gname').AsString;

    if St2='' then
    St2:=Base10.Seek_Code(nSqry.FieldByName('Gcode').AsString,'B',Edit107.Text);

    nSqry.FieldByName('Gname').Value:=St2;

    nSqry.Post;
    nSqry.Next;
  end;

  nSqry.First;
  Tong20.Srart_52_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=Base10.T5_Sub21BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo52.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo52.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit108.Focused=True)and(Edit108.SelStart=50)and(Length(Trim(Edit108.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo52.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo52.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo52.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo52.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo52.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo52.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo52.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo52.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo52.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if Edit108.Focused=True Then begin
       Edit107.Text:='';
    if Edit108.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit108.Text;
    Seak80.FilterTing(Edit108.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end else
    if Seak80.ShowModal=mrOK Then begin
      Edit107.Text:=Seak80.Query1Gcode.AsString;
      Edit108.Text:=Seak80.Query1Gname.AsString;
      Button101Click(Self);
    end;
    end else
      Button101Click(Self);
  end;
  end;
end;

procedure TSobo52.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo52.DBGrid101Exit(Sender: TObject);
begin
  Base10.T5_Sub21BeforeClose(Base10.T5_Sub21);
end;

procedure TSobo52.DBGrid201Exit(Sender: TObject);
begin
//
end;

procedure TSobo52.DBGrid101Enter(Sender: TObject);
begin
  Base10.T5_Sub21AfterScroll(Base10.T5_Sub21);
end;

procedure TSobo52.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo52.DBGrid101KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
    St1,St2,St3,St4: String;
    _S1_Ssub,_Sg_Csum,_Sv_Ghng: String;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=1 Then begin
      if nSqry.FieldByName('Gcode').AsString='' Then Exit;
      Seek40.Edit1.Text:=nSqry.FieldByName('Gcode').AsString;
      Seek40.FilterTing(nSqry.FieldByName('Gcode').AsString,Edit107.Text);
      if Seek40.Query1.RecordCount=1 Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek40.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek40.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
      if Seek40.ShowModal=mrOK Then begin
        nSqry.FieldByName('Gcode').AsString:=Seek40.Query1Gcode.AsString;
        nSqry.FieldByName('Gname').AsString:=Seek40.Query1Gname.AsString;
        SIndexs:=SIndexs+1;
      end else
        SIndexs:=SIndexs-1;
      if SIndexs=2 then
      if(nSqry.FieldByName('Gcode').AsString<>'')and
        (nSqry.FieldByName('Gosum').AsFloat=0   )and
        (nSqry.FieldByName('Gbsum').AsFloat=0   )Then begin

        {-Sv_Ghng-}
        Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
                'Where '+D_Select+
                'Gdate < '+#39+nSqry.FieldByName('Gdate').AsString+#39+' and  '+
                'Hcode = '+#39+Edit107.Text+#39;
        St1:=Base10.Seek_Name(Sqlen);

        {-In_Ssub-}
        _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
                  'Gdate'+'<='+#39+nSqry.FieldByName('Gdate').AsString+#39+' and '+
                  'Bcode'+' ='+#39+nSqry.FieldByName('Gcode').AsString+#39+' and '+
                  'Ocode'+' ='+#39+nSqry.FieldByName('Scode').AsString+#39+' and '+
                  'Hcode'+'='+#39+Edit107.Text+#39;
        _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
                  'Gdate'+'<='+#39+nSqry.FieldByName('Gdate').AsString+#39+' and '+
                  'Gcode'+' ='+#39+nSqry.FieldByName('Gcode').AsString+#39+' and '+
                  'Scode'+' ='+#39+nSqry.FieldByName('Scode').AsString+#39+' and '+
                  'Hcode'+'='+#39+Edit107.Text+#39;
        _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
                  'Gcode'+' ='+#39+nSqry.FieldByName('Gcode').AsString+#39+' and '+
                  'Scode'+' ='+#39+nSqry.FieldByName('Scode').AsString+#39+' and '+
                  'Hcode'+'='+#39+Edit107.Text+#39;
        Tong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng);

        sSqry.First;
        While sSqry.EOF=False do begin
          nSqry.FieldByName('Gosum').AsFloat:=
          nSqry.FieldByName('Gosum').AsFloat+sSqry.FieldByName('GsumX').AsFloat;
          sSqry.Next;
        end;
      end;
    end else
    if SIndexs=3 Then begin
      nSqry.FieldByName('Gbsum').AsFloat:=
      nSqry.FieldByName('Gssum').AsFloat-nSqry.FieldByName('Gosum').AsFloat;
      SIndexs:=SIndexs+1;
    end;
    DBGrid101.SelectedIndex:=SIndexs+1;
    end;
  end;
  end;
end;

procedure TSobo52.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if nSqry.Active=True Then begin
  SIndexs:=DBGrid101.SelectedIndex;
  sColumn:=DBGrid101.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    nSqry.Edit;
    if SIndexs=6 Then begin
      nSqry.Append; DBGrid101.SelectedIndex:=0;
    end;
  end;
  if sColumn=False Then begin
    if nSqry.IsEmpty=False Then
    if Key=VK_DELETE Then Base10.T5_Sub21AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo52.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo52.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo52.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo52.DBGrid201TitleClick(Column: TColumnEh);
begin
//
end;

procedure TSobo52.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo52.DataSource2DataChange(Sender: TObject; Field: TField);
begin
//
end;

procedure TSobo52.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo52.DateEdit2ButtonClick(Sender: TObject);
begin
  DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo52.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo52.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo52.Button700Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit108.Text;
  if Edit108.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit108.Text);
  if Seak80.Query1.RecordCount=1 Then begin
    Edit107.Text:=Seak80.Query1Gcode.AsString;
    Edit108.Text:=Seak80.Query1Gname.AsString;
    Button101Click(Self);
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit107.Text:=Seak80.Query1Gcode.AsString;
    Edit108.Text:=Seak80.Query1Gname.AsString;
    Button101Click(Self);
  end;
end;

procedure TSobo52.Button801Click(Sender: TObject);
var St1,St2,St3,St4,St9: String;
    _S1_Ssub,_Sg_Csum,_Sv_Ghng: String;
begin

  St1:='Hcode'+' ='+#39+Edit107.Text+#39;

  {-G4_Book-}
  Sqlen :=
  'Select Gcode,Gname From G4_Book Where '+D_Select+St1+
  ' Order By Gcode ';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(YGrid)
  else ShowMessage(E_Open);

  Grat1:=0;
  ProgressBar1.Max:=YGrid.RowCount-1;
  While YGrid.RowCount-1 > Grat1 do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  Grat1:=Grat1+1;
  { if Sobo52.Caption='재고변경관리-(본사)' then begin
     St2:='A';
     St9:='C';
    end else begin
     St2:='B';
     St9:='D';
    end; }
     St2:='B';
     St9:='D';
    St3:=YGrid.Cells[ 0,Grat1];
    St4:=YGrid.Cells[ 1,Grat1];

    {-Sv_Ghng-}
    Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
            'Where '+D_Select+
            'Gdate < '+#39+Edit102.Text+#39+' and  '+
            'Hcode = '+#39+Edit107.Text+#39;
    St1:=Base10.Seek_Name(Sqlen);

    {-In_Ssub-}
    _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
              'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
              'Bcode'+' ='+#39+St3+#39+' and '+
              'Ocode'+' ='+#39+St2+#39+' and '+
              'Hcode'+' ='+#39+Edit107.Text+#39;
    _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
              'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
              'Gcode'+' ='+#39+St3+#39+' and '+
              '(Scode'+' ='+#39+St2+#39+' or '+'Scode'+' ='+#39+St9+#39+')'+' and '+
              'Hcode'+' ='+#39+Edit107.Text+#39;
    _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
              'Gcode'+' ='+#39+St3+#39+' and '+
              'Scode'+' ='+#39+St2+#39+' and '+
              'Hcode'+' ='+#39+Edit107.Text+#39;
    Tong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng);

    T01:=0;
    sSqry.First;
    While sSqry.EOF=False do begin
      T01:=T01+sSqry.FieldByName('GsumX').AsFloat;
      sSqry.Next;
    end;

    if T01<>0 then begin
      nSqry.Append;
      nSqry.FieldByName('Gdate').AsString:=Edit102.Text;
      nSqry.FieldByName('Gcode').AsString:=St3;
      nSqry.FieldByName('Scode').AsString:=St2;
      nSqry.FieldByName('Gname').AsString:=St4;
      nSqry.FieldByName('Gssum').AsFloat :=0;
      nSqry.FieldByName('Gosum').AsFloat :=T01;
      nSqry.FieldByName('Gbsum').AsFloat :=
      nSqry.FieldByName('Gssum').AsFloat-nSqry.FieldByName('Gosum').AsFloat;
    //nSqry.FieldByName('Gbigo').AsString:='보명에서 이전';
      nSqry.Post;
    end;

  end;
  ProgressBar1.Position:=0;
end;

procedure TSobo52.Button802Click(Sender: TObject);
var St1,St2,St3,St4,St9: String;
    _S1_Ssub,_Sg_Csum,_Sv_Ghng: String;
begin

  nSqry.First;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;
  { if Sobo52.Caption='재고변경관리-(본사)' then begin
     St2:='A';
     St9:='C';
    end else begin
     St2:='B';
     St9:='D';
    end; }
     St2:='B';
     St9:='D';
    St3:=nSqry.FieldByName('Gcode').AsString;
    St4:=nSqry.FieldByName('Gdate').AsString;

    {-Sv_Ghng-}
    Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
            'Where '+D_Select+
            'Gdate < '+#39+St4+#39+' and  '+
            'Hcode = '+#39+Edit107.Text+#39;
    St1:=Base10.Seek_Name(Sqlen);

    {-In_Ssub-}
    _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
              'Gdate'+'<='+#39+St4+#39+' and '+
              'Bcode'+' ='+#39+St3+#39+' and '+
              'Ocode'+' ='+#39+St2+#39+' and '+
              'Hcode'+' ='+#39+Edit107.Text+#39;
    _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
              'Gdate'+'<='+#39+St4+#39+' and '+
              'Gcode'+' ='+#39+St3+#39+' and '+
              '(Scode'+' ='+#39+St2+#39+' or '+'Scode'+' ='+#39+St9+#39+')'+' and '+
              'Hcode'+' ='+#39+Edit107.Text+#39;
    _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
              'Gcode'+' ='+#39+St3+#39+' and '+
              'Scode'+' ='+#39+St2+#39+' and '+
              'Hcode'+' ='+#39+Edit107.Text+#39;
    Tong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng);

    T01:=0;
    sSqry.First;
    While sSqry.EOF=False do begin
      T01:=T01+sSqry.FieldByName('GsumX').AsFloat;
      sSqry.Next;
    end;

  //if nSqry.Locate('Gcode;Gdate',VarArrayOf([St3,St4]),[loCaseInsensitive])=true then begin
      nSqry.Edit;
      nSqry.FieldByName('Gosum').AsFloat :=T01;
      nSqry.FieldByName('Gbsum').AsFloat :=
      nSqry.FieldByName('Gssum').AsFloat-nSqry.FieldByName('Gosum').AsFloat;
      nSqry.Post;
  //end;

    nSqry.Next;
  end;
  ProgressBar1.Position:=0;
end;

end.
