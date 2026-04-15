unit Subu32_1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit, ToolEdit, dxCore,
  dxButtons, DBGridEh, CornerButton, DBClient;

type
  TSobo32_1 = class(TForm)
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
    Panel104: TFlatPanel;
    Edit105: TFlatEdit;
    Edit106: TFlatEdit;
    Button201: TFlatButton;
    DateEdit1: TDateEdit;
    Button700: TFlatButton;
    CornerButton1: TCornerButton;
    CornerButton2: TCornerButton;
    CornerButton9: TCornerButton;
    DBGrid101: TDBGridEh;
    dxButton1: TdxButton;
    Label301: TmyLabel3d;
    Label302: TmyLabel3d;
    Label309: TmyLabel3d;
    T3_Sub01: TClientDataSet;
    T3_Sub01GDATE: TStringField;
    T3_Sub01HCODE: TStringField;
    T3_Sub01SCODE: TStringField;
    T3_Sub01GCODE: TStringField;
    T3_Sub01GNAME: TStringField;
    T3_Sub01CHEK1: TStringField;
    T3_Sub01GSUMY: TFloatField;
    T3_Sub01GSSUM: TFloatField;
    Edit107: TFlatEdit;
    Edit108: TFlatEdit;
    Button701: TFlatButton;
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
    procedure Button701Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo32_1: TSobo32_1;

implementation

{$R *.DFM}

uses Chul, Base01, Tong02, Tong04, TcpLib,
   Seak01, Seak02, Seak03, Seak04, Seak05, Seak06, Seak07, Seak08, Seak09,
   Seek01, Seek02, Seek03, Seek04, Seek05, Seek06, Seek07, Seek08, Seek09;

procedure TSobo32_1.FormActivate(Sender: TObject);
begin
  nForm:='32_1';
  nSqry:=T3_Sub01;
//mSqry:=T3_Sub01;
end;

procedure TSobo32_1.FormShow(Sender: TObject);
begin
  T00:=0;
  Edit101.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
//Edit102.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
end;

procedure TSobo32_1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Release;
  Action:=caFree;
  Sobo32_1:=nil;
  Base10.OpenExit(nSqry);
//Base10.OpenExit(mSqry);
end;

procedure TSobo32_1.Button001Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak10.ShowModal;
  end;
end;

procedure TSobo32_1.Button002Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
  if Seak20.ShowModal=mrOK then
  // Tong20.Srart_52_01(Self);
  end;
end;

procedure TSobo32_1.Button003Click(Sender: TObject);
begin
  if nSqry.Active=True Then begin
     oSqry:=nSqry;
     Seak30.ShowModal;
  end;
end;

procedure TSobo32_1.Button004Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button005Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button006Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button007Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button008Click(Sender: TObject);
begin
  Tong20.Zoom_Int_01('52');
end;

procedure TSobo32_1.Button009Click(Sender: TObject);
begin
  Tong20.Zoom_Out_01('52');
end;

procedure TSobo32_1.Button010Click(Sender: TObject);
begin
  Tong20.DBGridSaveHtml(DBGrid101, Caption);
end;

procedure TSobo32_1.Button011Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button012Click(Sender: TObject);
begin
  oSqry:=nSqry;
  Base10.ColumnY1(oSqry,DBGrid101,ProgressBar1);
end;

procedure TSobo32_1.Button013Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button014Click(Sender: TObject);
begin
//Tong20.Print_00_00('52-01');
end;

procedure TSobo32_1.Button015Click(Sender: TObject);
begin
//Tong20.Print_00_00('52-02');
end;

procedure TSobo32_1.Button016Click(Sender: TObject);
begin
//Tong40.print_52_01(Self);
end;

procedure TSobo32_1.Button017Click(Sender: TObject);
begin
{ Tong40.print_52_02(Self); }
end;

procedure TSobo32_1.Button018Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button019Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button020Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button021Click(Sender: TObject);
begin
  Tong20.DBGridFont4(DBGrid101);
end;

procedure TSobo32_1.Button022Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button023Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button024Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Button101Click(Sender: TObject);
var St1,St2,St3,St4: String;
    _S1_Ssub,_Sg_Csum,_Sv_Ghng: String;
begin

  Tong40.Show;
  Tong40.Update;

  Refresh;
  nSqry.BeforePost:=nil;
  Base10.OpenShow(nSqry);
  Screen.Cursor:=crHourGlass;
  DataSource1.Enabled:=False;

  {-G7_Ggeo-}
  Sqlen := 'Select Gcode,Gname,Chek1 From G7_Ggeo Where '+D_Open;

  if (Edit107.Text<>'') Then
  Sqlen:=Sqlen+
         ' and '+'Gcode'+'>='+#39+Edit105.Text+#39+
         ' and '+'Gcode'+'<='+#39+Edit107.Text+#39;

  if S_Where2<>'' then
  Sqlen:=Sqlen+' and '+S_Where2;

  Sqlen:=Sqlen+' Order By Gcode';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(nSqry)
  else ShowMessage(E_Open);

  nSqry.First;
  ProgressBar1.Max:=nSqry.RecordCount;
  While nSqry.EOF=False do begin
  ProgressBar1.Position:=ProgressBar1.Position+1;

    {-Sv_Ghng-}
    Sqlen :='Select Max(Gdate)as Gdate From Sv_Ghng '+
            'Where '+D_Select+
            'Gdate < '+#39+Edit101.Text+'.99'+#39+' and  '+
            'Hcode = '+#39+nSqry.FieldByName('Gcode').AsString+#39;
    St1:=Base10.Seek_Name(Sqlen);

    {-In_Ssub-}
    _S1_Ssub:='Gdate'+'> '+#39+St1+#39+' and '+
              'Gdate'+'<='+#39+Edit101.Text+'.99'+#39+' and '+
              'Ocode'+' ='+#39+'B'+#39+' and '+
              'Hcode'+' ='+#39+nSqry.FieldByName('Gcode').AsString+#39;
    _Sg_Csum:='Gdate'+'> '+#39+St1+#39+' and '+
              'Gdate'+'<='+#39+Edit101.Text+'.99'+#39+' and '+
              'Hcode'+' ='+#39+nSqry.FieldByName('Gcode').AsString+#39+' and '+
             '(Scode'+' ='+#39+'B'+#39+' or '+'Scode'+' ='+#39+'D'+#39+')';
    //        'Scode'+' ='+#39+'B'+#39+' and '+
    _Sv_Ghng:='Gdate'+' ='+#39+St1+#39+' and '+
              'Scode'+' ='+#39+'B'+#39+' and '+
              'Hcode'+' ='+#39+nSqry.FieldByName('Gcode').AsString+#39;
    Tong40._Sv_Ghng_(_S1_Ssub,_Sg_Csum,_Sv_Ghng);


    Sqlen := 'Select Chek3 From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'' ';
    Translate(Sqlen, '@Gcode', nSqry.FieldByName('Gcode').AsString);
    St2:=Base10.Seek_Name(Sqlen);

    T01:=0;
    T03:=0;
    T09:=0;

    sSqry.First;
    While sSqry.EOF=False do begin
      if Base10.G4_Book.Locate('Hcode;Gcode',VarArrayOf([nSqry.FieldByName('Gcode').AsString,sSqry.FieldByName('Gcode').AsString]),[loCaseInsensitive])=true then begin

        if St2='True' then begin
          Sqlen := 'Select Grat8 From G4_Book Where '+D_Select+'Gcode=''@Gcode'' and Hcode=''@Hcode''';
          Translate(Sqlen, '@Gcode', sSqry.FieldByName('Gcode').AsString);
          Translate(Sqlen, '@Hcode', nSqry.FieldByName('Gcode').AsString);
          T08:=StrToIntDef(Base10.Seek_Name(Sqlen),0);
          if T08 > 0 then begin
          T01:=T01+(sSqry.FieldByName('GsumX').AsFloat*T08);
          T03:=T03+(sSqry.FieldByName('Gbqut').AsFloat*T08);
          end else begin
          T01:=T01+sSqry.FieldByName('GsumX').AsFloat;
          T03:=T03+sSqry.FieldByName('Gbqut').AsFloat;
          end;
        end else begin
          T01:=T01+sSqry.FieldByName('GsumX').AsFloat;
          T03:=T03+sSqry.FieldByName('Gbqut').AsFloat;
        end;

        if sSqry.FieldByName('GsumX').AsFloat > 0 then
        T09:=T09+1;

      end;
      sSqry.Next;
    end;

    nSqry.Edit;
    nSqry.FieldByName('GsumY').AsFloat:=T01;

    if nSqry.FieldByName('Chek1').AsString='True' then
    nSqry.FieldByName('Gssum').AsFloat:=T03;

    if nBase='xXx' then
    nSqry.FieldByName('Gssum').AsString:='';

    nSqry.Post;


    nSqry.Next;
  end;

  nSqry.First;
  DBGrid101.SetFocus;
  ProgressBar1.Position:=0;
  DataSource1.Enabled:=True;
  Screen.Cursor:=crDefault;

  Tong40.Hide;
{ Tong40.Free; }
end;

procedure TSobo32_1.Button201Click(Sender: TObject);
begin
//
end;

procedure TSobo32_1.Edit101Change(Sender: TObject);
var St1: Char;
begin
  St1:=#13;
  if((Edit101.Focused=True)and(Edit101.SelStart=10)and(Length(Trim(Edit101.Text))=10))Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
  if((Edit106.Focused=True)and(Edit106.SelStart=50)and(Length(Trim(Edit106.Text))=50))or
    ((Edit108.Focused=True)and(Edit108.SelStart=50)and(Length(Trim(Edit108.Text))=50))Then begin
      Edit114KeyPress(Self,St1);
  end;
end;

procedure TSobo32_1.Edit101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo32_1.Edit102KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
end;

procedure TSobo32_1.Edit111KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Key:=#0; SelectNext(ActiveControl as TWinControl, True, True);
  end;
end;

procedure TSobo32_1.Edit111KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
  if Key=VK_UP   Then PerForm(WM_NEXTDLGCTL,1,0);
  if Key=VK_DOWN Then PerForm(WM_NEXTDLGCTL,0,0);
end;

procedure TSobo32_1.Edit112KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo32_1.Edit112KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo32_1.Edit113KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo32_1.Edit113KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo32_1.Edit114KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
  if Edit106.Focused=True Then begin
       Edit105.Text:='';
    if Edit106.Text<>'' Then begin
    Seak80.Edit1.Text:=Edit106.Text;
    Seak80.FilterTing(Edit106.Text);
    if Seak80.Query1.RecordCount=1 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit105.Text:=Seak80.Query1Gcode.AsString;
      Edit106.Text:=Seak80.Query1Gname.AsString;
    end else
    if Seak80.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit105.Text:=Seak80.Query1Gcode.AsString;
      Edit106.Text:=Seak80.Query1Gname.AsString;
    end;
    end else
      SelectNext(ActiveControl as TWinControl, True, True);
  end else
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

procedure TSobo32_1.Edit114KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo32_1.DBGrid101Exit(Sender: TObject);
begin
//Base10.T5_Sub21BeforeClose(Base10.T5_Sub21);
end;

procedure TSobo32_1.DBGrid201Exit(Sender: TObject);
begin
//
end;

procedure TSobo32_1.DBGrid101Enter(Sender: TObject);
begin
//Base10.T5_Sub21AfterScroll(Base10.T5_Sub21);
end;

procedure TSobo32_1.DBGrid201Enter(Sender: TObject);
begin
//
end;

procedure TSobo32_1.DBGrid101KeyPress(Sender: TObject; var Key: Char);
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

procedure TSobo32_1.DBGrid101KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo32_1.DBGrid201KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSobo32_1.DBGrid201KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSobo32_1.DBGrid101TitleClick(Column: TColumnEh);
begin
  Base10.ColumnS9(nSqry,Column);
end;

procedure TSobo32_1.DBGrid201TitleClick(Column: TColumnEh);
begin
//
end;

procedure TSobo32_1.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Panel009.Caption:=IntToStr(nSqry.RecNo)+'/'+IntToStr(nSqry.RecordCount);
end;

procedure TSobo32_1.DataSource2DataChange(Sender: TObject; Field: TField);
begin
//
end;

procedure TSobo32_1.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit101.Text);
end;

procedure TSobo32_1.DateEdit2ButtonClick(Sender: TObject);
begin
//DateEdit2.Date :=StrToDate(Edit102.Text);
end;

procedure TSobo32_1.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit101.Text :=DateToStr(ADate);
end;

procedure TSobo32_1.DateEdit2AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
//Edit102.Text :=DateToStr(ADate);
end;

procedure TSobo32_1.Button700Click(Sender: TObject);
begin
  Seak80.Edit1.Text:=Edit106.Text;
  if Edit106.Text='' then
  Seak80.FilterTing('') else
  Seak80.FilterTing(Edit106.Text);
  if Seak80.Query1.RecordCount=1 Then begin
    Edit105.Text:=Seak80.Query1Gcode.AsString;
    Edit106.Text:=Seak80.Query1Gname.AsString;
  end else
  if Seak80.ShowModal=mrOK Then begin
    Edit105.Text:=Seak80.Query1Gcode.AsString;
    Edit106.Text:=Seak80.Query1Gname.AsString;
  end;
end;

procedure TSobo32_1.Button701Click(Sender: TObject);
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

end.
