unit Subu51;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit;

type
  TSobo51 = class(TForm)
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
    DBGrid101: TDBGrid;
    StBar101: TStatusBar;
    Label101: TmyLabel3d;
    Edit101: TFlatMaskEdit;
    Edit102: TFlatMaskEdit;
    Panel104: TFlatPanel;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Button201: TFlatButton;
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
    procedure DBGrid101TitleClick(Column: TColumn);
    procedure DBGrid201TitleClick(Column: TColumn);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo51: TSobo51;
  S5101,S5102,S5103,S5104,S5105,S5106: Double;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo51.FormActivate(Sender: TObject);
begin
  nForm:='51';
  nSqry:=Base10.T5_Sub11;
  mSqry:=Base10.T5_Sub12;
end;

procedure TSobo51.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo51.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo51:=nil;
  Base10.OpenExit(nSqry);
  Base10.OpenExit(mSqry);
end;

procedure TSobo51.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo51.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
     Tong20.Srart_51_01(Self);
  end;
end;

procedure TSobo51.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
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
  Tong20.Zoom_Int_01('51');
end;

procedure TSobo51.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('51');
end;

procedure TSobo51.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo51.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnX1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo51.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Button014Click(Sender: TObject);
begin
  Tong20.Print_00_00('51-01');
end;

procedure TSobo51.Button015Click(Sender: TObject);
begin
  Tong20.Print_00_00('51-02');
end;

procedure TSobo51.Button016Click(Sender: TObject);
begin
  Tong40.print_51_01(Self);
end;

procedure TSobo51.Button017Click(Sender: TObject);
begin
{ Tong40.print_51_02(Self); }
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
  Tong20.DBGridFont2(DBGrid101,StBar101);
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

  Scode:='D';
  St1:='Gdate'+'>='+#39+Edit101.Text+#39+' and '+
       'Gdate'+'<='+#39+Edit102.Text+#39+' and '+
       'Hcode'+' ='+#39+Edit107.Text+#39+' and '+
       'Scode'+' ='+#39+Scode+#39;

  St2:=' Order By Gdate,Gcode';

  {-Sg_Csum-}
  Sqlen := 'Select * From Sg_Csum Where '+St1+St2;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  S5101:=0; S5102:=0; S5103:=0;

  nSqry.First;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    nSqry.Edit;

    if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([Edit107.Text,nSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then
    St2:=Base10.G4_Book.FieldByName('Gname').AsString;

    if St2='' then
    St2:=Base10.Seek_Code(nSqry.FieldByName('Gcode').AsString,'B',Edit107.Text);

    nSqry.FieldByName('Gname').Value:=St2;

    S5101:=S5101+nSqry.FieldByName('Gssum').AsFloat;
    S5102:=S5102+nSqry.FieldByName('Gosum').AsFloat;
    S5103:=S5103+nSqry.FieldByName('Gbsum').AsFloat;
    nSqry.Post;
    nSqry.Next;
  end;

  nSqry.First;
  Tong20.Srart_51_01(Self);
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;
  nSqry.BeforePost:=Base10.T5_Sub11BeforePost;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo51.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo51.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))or
    ((Edit102.Focused=True)and(Edit102.SelStart=10)and(Length(Trim(Edit102.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit108.Focused=True)and(Edit108.SelStart=24)and(Length(Trim(Edit108.Text))=24))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo51.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo51.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo51.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo51.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo51.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo51.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo51.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo51.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
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

procedure TSobo51.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo51.DBGrid101Exit(Sender: TObject);
begin
  Base10.T5_Sub11BeforeClose(Base10.T5_Sub21);
end;

procedure TSobo51.DBGrid201Exit(Sender: TObject);
begin
//
end;

procedure TSobo51.DBGrid101Enter(Sender: TObject);
begin
  Base10.T5_Sub11AfterScroll(Base10.T5_Sub21);
end;

procedure TSobo51.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo51.DBGrid101KeyPress(Sender: TObject; var Key: Char);
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
      if(nSqry.FieldByName('Gcode').AsString<>'')and
        (nSqry.FieldByName('Gosum').AsFloat=0   )and
        (nSqry.FieldByName('Gbsum').AsFloat=0   )Then begin

        {-Sv_Ghng-}
        Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
                'Where Gdate < '+#39+nSqry.FieldByName('Gdate').AsString+#39+
                ' and  Hcode = '+#39+Edit107.Text+#39;
        St1:=Base10.Seek_Name(Sqlen);

        {-In_Ssub-}
        _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
                  'Gdate'+'<='+#39+nSqry.FieldByName('Gdate').AsString+#39+' and '+
                  'Bcode'+' ='+#39+nSqry.FieldByName('Gcode').AsString+#39+' and '+
                  'Ocode'+' ='+#39+'B'+#39+' and '+
                  'Hcode'+'='+#39+Edit107.Text+#39;
        _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
                  'Gdate'+'<='+#39+nSqry.FieldByName('Gdate').AsString+#39+' and '+
                  'Gcode'+' ='+#39+nSqry.FieldByName('Gcode').AsString+#39+' and '+
                  'Scode'+' ='+#39+'B'+#39+' and '+
                  'Hcode'+'='+#39+Edit107.Text+#39;
        _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
                  'Gcode'+' ='+#39+nSqry.FieldByName('Gcode').AsString+#39+' and '+
                 '(Scode'+' ='+#39+'B'+#39+' or '+'Scode'+' ='+#39+'D'+#39+')and '+
                  'Hcode'+'='+#39+Edit107.Text+#39;
        Tong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng);

        sSqry.First;
        While sSqry.EOF=False do begin
          nSqry.FieldByName('Gosum').AsFloat:=
          nSqry.FieldByName('Gosum').AsFloat+sSqry.FieldByName('Gbqut').AsFloat;
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

procedure TSobo51.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
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
    if Key=VK_DELETE Then Base10.T5_Sub11AfterDelete(nSqry);
    if Key=VK_ESCAPE Then Edit101.SetFocus;
  end; end;
end;

procedure TSobo51.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo51.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo51.DBGrid101TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(nSqry,Column);
end;

procedure TSobo51.DBGrid201TitleClick(Column: TColumn);
begin
//
end;

procedure TSobo51.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  StBar101.Panels.Items[1].Text:=FormatFloat('###,###,##0',S5101);
  StBar101.Panels.Items[2].Text:=FormatFloat('###,###,##0',S5102);
  StBar101.Panels.Items[3].Text:=FormatFloat('###,###,##0',S5103);
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo51.DataSource2DataChange(Sender: TObject; Field: TField);
begin
//
end;

end.
