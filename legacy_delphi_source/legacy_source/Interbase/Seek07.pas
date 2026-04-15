unit Seek07;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit, TFlatNumberUnit;

type
  TSeek70 = class(TForm)
    DataSource1: TDataSource;
    Panel100: TFlatPanel;
    Panel101: TFlatPanel;
    Edit1: TFlatEdit;
    Panel102: TFlatPanel;
    Edit2: TFlatEdit;
    Panel103: TFlatPanel;
    Edit3: TFlatNumber;
    Panel104: TFlatPanel;
    Edit4: TFlatEdit;
    Panel201: TFlatPanel;
    DBGrid1: TDBGrid;
    BitBtn101: TBitBtn;
    Button101: TFlatButton;
    Button102: TFlatButton;
    BitBtn102: TBitBtn;
    Query1: TClientDataSet;
    Query1SNAME: TStringField;
    Query1GUBUN: TStringField;
    Query1JUBUN: TStringField;
    Query1PUBUN: TStringField;
    Query1SCODE: TStringField;
    Query1GCODE: TStringField;
    Query1OCODE: TStringField;
    Query1GNAME: TStringField;
    Query1GPOSA: TStringField;
    Query1GTEL1: TStringField;
    Query1GTEL2: TStringField;
    Query1GADD1: TStringField;
    Query1GADD2: TStringField;
    Query1GQUT1: TFloatField;
    Query1GRAT1: TSmallintField;
    Query1GJISA: TStringField;
    procedure FormActivate(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Edit1KeyPress(Sender: TObject; var Key: Char);
    procedure Edit4KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid1KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid1KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure BitBtn101Click(Sender: TObject);
    procedure DBGrid1TitleClick(Column: TColumn);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seek70: TSeek70;

implementation

{$R *.DFM}

uses Base01, Seek04, Subu29, TcpLib;

procedure TSeek70.FormActivate(Sender: TObject);
begin
{ Query1:=Base30.T2_Sub92; }
end;

procedure TSeek70.FormShow(Sender: TObject);
var St1,St2,St3,p_Sname: String;
    St0,p_Grat1: Integer;
begin
  Base10.OpenExit(Query1);
  Base10.OpenShow(Query1);

  Edit1.Text:=Sobo29.Edit104.Text;
  Edit2.Text:=Sobo29.Edit103.Text;
  Edit4.Text:=Sobo29.Edit105.Text;

  Sqlen := 'Select Grat1 From G4_Book Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
  Translate(Sqlen, '@Gcode', Edit1.Text);
  Translate(Sqlen, '@Hcode', Sobo29.Edit107.Text);
  St3:=Base10.Seek_Name(Sqlen);

  Sqlen := 'Select Gdang From G4_Book Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
  Translate(Sqlen, '@Gcode', Edit1.Text);
  Translate(Sqlen, '@Hcode', Sobo29.Edit107.Text);
  St1:=Base10.Seek_Name(Sqlen);
  if St1<>'' then
  Edit3.Value:=StrToIntDef(St1,0);

  St1:='Gcode'+' like '+#39+''+'%'+#39+' and '+
       'Hcode'+'='+#39+''+#39;
  St2:=' Order By Gcode';
  St1:=St1+St2;

  Sqlen := 'Select Gubun,Jubun,Gcode,Ocode,Gname,Gposa,'+
           'Gtel1,Gtel2,Gqut1,Grat1 From G1_Ggeo Where '+St1;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    p_Sname:='';
    if St3<>'0' then
    p_Grat1:=StrToIntDef(St1,0) else
    p_Grat1:=StrToIntDef(SGrid.Cells[ 9,List1],0);

    Sqlen := 'Select Gname From G1_Gbun Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', Sobo29.Edit107.Text);
    St1:=Base10.Seek_Name(Sqlen);
    p_Sname:=Base10.Seek_Name(Sqlen);

    Sqlen := 'Select Grat1 From G6_Ggeo '+
             'Where Gcode=''@Gcode'' and Bcode=''@Bcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 2,List1]);
    Translate(Sqlen, '@Bcode', '');
    Translate(Sqlen, '@Hcode', Sobo29.Edit107.Text);
    St1:=Base10.Seek_Name(Sqlen);
    if St1<>'' then
    p_Grat1:=StrToIntDef(St1,0);

    Sqlen := 'Select Grat1 From G6_Ggeo '+
             'Where Gcode=''@Gcode'' and Bcode=''@Bcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 2,List1]);
    Translate(Sqlen, '@Bcode', Edit1.Text);
    Translate(Sqlen, '@Hcode', Sobo29.Edit107.Text);
    St1:=Base10.Seek_Name(Sqlen);
    if St1<>'' then
    p_Grat1:=StrToIntDef(St1,0);

    St2:=SGrid.Cells[ 2,List1];
    if Query1.Locate('Gcode',St2,[loCaseInsensitive])=False then begin
      Query1.Append;
      Query1.FieldByName('Gubun').AsString:=SGrid.Cells[ 0,List1];
      Query1.FieldByName('Jubun').AsString:=SGrid.Cells[ 1,List1];
      Query1.FieldByName('Gcode').AsString:=SGrid.Cells[ 2,List1];
      Query1.FieldByName('Ocode').AsString:=SGrid.Cells[ 3,List1];
      Query1.FieldByName('Gname').AsString:=SGrid.Cells[ 4,List1];
      Query1.FieldByName('Gposa').AsString:=SGrid.Cells[ 5,List1];
      Query1.FieldByName('Gtel1').AsString:=SGrid.Cells[ 6,List1];
      Query1.FieldByName('Gtel2').AsString:=SGrid.Cells[ 7,List1];
      Query1.FieldByName('Gqut1').AsString:=SGrid.Cells[ 8,List1];
      Query1.FieldByName('Sname').AsString:=p_Sname;
      Query1.FieldByName('Grat1').AsFloat :=p_Grat1;
      Query1.Post;

      St1:='Scode'+'='+#39+'X'+#39+' and '+
           'Gcode'+'='+#39+SGrid.Cells[ 2,List1]+#39;
      Sqlen := 'Select Gname,Jubun From H2_Gbun Where '+St1+' Order By Oname,Gname';
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.body_data <> 'ERROR' then
         Base10.Socket.MakeGrid(YGrid)
      else ShowMessage(E_Open);

      RBand:=0;
      While YGrid.RowCount-1 > RBand do begin
      RBand:=RBand+1;

      Query1.Append;
      Query1.FieldByName('Gubun').AsString:=SGrid.Cells[ 0,List1];
      Query1.FieldByName('Jubun').AsString:=SGrid.Cells[ 1,List1];
      Query1.FieldByName('Gcode').AsString:=SGrid.Cells[ 2,List1];
      Query1.FieldByName('Ocode').AsString:=SGrid.Cells[ 3,List1];
      Query1.FieldByName('Gname').AsString:=SGrid.Cells[ 4,List1];
      if YGrid.Cells[ 1,RBand]='' then
      Query1.FieldByName('Gjisa').AsString:=YGrid.Cells[ 0,RBand] else
      Query1.FieldByName('Gjisa').AsString:=YGrid.Cells[ 1,RBand]+'|'+YGrid.Cells[ 0,RBand];
      Query1.FieldByName('Gposa').AsString:=SGrid.Cells[ 5,List1];
      Query1.FieldByName('Gtel1').AsString:=SGrid.Cells[ 6,List1];
      Query1.FieldByName('Gtel2').AsString:=SGrid.Cells[ 7,List1];
      Query1.FieldByName('Gqut1').AsString:=SGrid.Cells[ 8,List1];
      Query1.FieldByName('Sname').AsString:=p_Sname;
      Query1.FieldByName('Grat1').Value   :=p_Grat1;
      Query1.Post;

      end;
    end;
  end;

  //-//

  St1:='Gcode'+' like '+#39+''+'%'+#39+' and '+
       'Hcode'+'='+#39+Sobo29.Edit107.Text+#39;

  Sqlen := 'Select Gubun,Jubun,Gcode,Ocode,Gname,Gposa,'+
           'Gtel1,Gtel2,Gqut1,Grat1 From G1_Ggeo Where '+St1;
  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    p_Sname:='';
    if St3<>'0' then
    p_Grat1:=StrToIntDef(St1,0) else
    p_Grat1:=StrToIntDef(SGrid.Cells[ 9,List1],0);

    Sqlen := 'Select Gname From G1_Gbun Where Gcode=''@Gcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 0,List1]);
    Translate(Sqlen, '@Hcode', Sobo29.Edit107.Text);
    St1:=Base10.Seek_Name(Sqlen);
    p_Sname:=Base10.Seek_Name(Sqlen);

    Sqlen := 'Select Grat1 From G6_Ggeo '+
             'Where Gcode=''@Gcode'' and Bcode=''@Bcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 2,List1]);
    Translate(Sqlen, '@Bcode', '');
    Translate(Sqlen, '@Hcode', Sobo29.Edit107.Text);
    St1:=Base10.Seek_Name(Sqlen);
    if St1<>'' then
    p_Grat1:=StrToIntDef(St1,0);

    Sqlen := 'Select Grat1 From G6_Ggeo '+
             'Where Gcode=''@Gcode'' and Bcode=''@Bcode'' and Hcode=''@Hcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 2,List1]);
    Translate(Sqlen, '@Bcode', Edit1.Text);
    Translate(Sqlen, '@Hcode', Sobo29.Edit107.Text);
    St1:=Base10.Seek_Name(Sqlen);
    if St1<>'' then
    p_Grat1:=StrToIntDef(St1,0);

    St2:=SGrid.Cells[ 2,List1];
    if Query1.Locate('Gcode',St2,[loCaseInsensitive])=False then begin
      Query1.Append;
      Query1.FieldByName('Gubun').AsString:=SGrid.Cells[ 0,List1];
      Query1.FieldByName('Jubun').AsString:=SGrid.Cells[ 1,List1];
      Query1.FieldByName('Gcode').AsString:=SGrid.Cells[ 2,List1];
      Query1.FieldByName('Ocode').AsString:=SGrid.Cells[ 3,List1];
      Query1.FieldByName('Gname').AsString:=SGrid.Cells[ 4,List1];
      Query1.FieldByName('Gposa').AsString:=SGrid.Cells[ 5,List1];
      Query1.FieldByName('Gtel1').AsString:=SGrid.Cells[ 6,List1];
      Query1.FieldByName('Gtel2').AsString:=SGrid.Cells[ 7,List1];
      Query1.FieldByName('Gqut1').AsString:=SGrid.Cells[ 8,List1];
      Query1.FieldByName('Sname').AsString:=p_Sname;
      Query1.FieldByName('Grat1').AsFloat :=p_Grat1;
      Query1.Post;

      St1:='Scode'+'='+#39+'X'+#39+' and '+
           'Gcode'+'='+#39+SGrid.Cells[ 2,List1]+#39;
      Sqlen := 'Select Gname,Jubun From H2_Gbun Where '+St1+' Order By Oname,Gname';
      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.body_data <> 'ERROR' then
         Base10.Socket.MakeGrid(YGrid)
      else ShowMessage(E_Open);

      RBand:=0;
      While YGrid.RowCount-1 > RBand do begin
      RBand:=RBand+1;

      Query1.Append;
      Query1.FieldByName('Gubun').AsString:=SGrid.Cells[ 0,List1];
      Query1.FieldByName('Jubun').AsString:=SGrid.Cells[ 1,List1];
      Query1.FieldByName('Gcode').AsString:=SGrid.Cells[ 2,List1];
      Query1.FieldByName('Ocode').AsString:=SGrid.Cells[ 3,List1];
      Query1.FieldByName('Gname').AsString:=SGrid.Cells[ 4,List1];
      if YGrid.Cells[ 1,RBand]='' then
      Query1.FieldByName('Gjisa').AsString:=YGrid.Cells[ 0,RBand] else
      Query1.FieldByName('Gjisa').AsString:=YGrid.Cells[ 1,RBand]+'|'+YGrid.Cells[ 0,RBand];
      Query1.FieldByName('Gposa').AsString:=SGrid.Cells[ 5,List1];
      Query1.FieldByName('Gtel1').AsString:=SGrid.Cells[ 6,List1];
      Query1.FieldByName('Gtel2').AsString:=SGrid.Cells[ 7,List1];
      Query1.FieldByName('Gqut1').AsString:=SGrid.Cells[ 8,List1];
      Query1.FieldByName('Sname').AsString:=p_Sname;
      Query1.FieldByName('Grat1').Value   :=p_Grat1;
      Query1.Post;

      end;
    end;
  end;
  Query1.IndexName := 'IDX'+'GCODE'+'DOWN';
  Query1.First;
end;

procedure TSeek70.FormClose(Sender: TObject; var Action: TCloseAction);
begin
{ Base10.DeleteSX(Query1); Query1.Close; }
end;

procedure TSeek70.Edit1KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Seek40.Edit1.Text:=Edit1.Text;
    Seek40.FilterTing(Edit1.Text,Sobo29.Edit107.Text);
    if Seek40.Query1.RecordCount=0 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit1.Text:=Seek40.Query1Gcode.Value;
      Edit4.Text:=Seek40.Query1Gname.Value; end
    else begin
      if Seek40.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit1.Text:=Seek40.Query1Gcode.Value;
      Edit4.Text:=Seek40.Query1Gname.Value; end;
    end;
  end;
end;

procedure TSeek70.Edit4KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then begin
    Seek40.Edit1.Text:=Edit1.Text;
    Seek40.FilterTing(Edit1.Text,Sobo29.Edit107.Text);
    if Seek40.Query1.RecordCount=0 Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit1.Text:=Seek40.Query1Gcode.Value;
      Edit4.Text:=Seek40.Query1Gname.Value; end
    else begin
      if Seek40.ShowModal=mrOK Then begin
      SelectNext(ActiveControl as TWinControl, True, True);
      Edit1.Text:=Seek40.Query1Gcode.Value;
      Edit4.Text:=Seek40.Query1Gname.Value; end;
    end;
  end;
end;

procedure TSeek70.DBGrid1KeyPress(Sender: TObject; var Key: Char);
var sColumn: Boolean;
    sIndexs: Integer;
    St1,St2: String;
begin
  if Query1.Active=True Then begin
  SIndexs:=DBGrid1.SelectedIndex;
  sColumn:=DBGrid1.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=#13 Then begin
    if sColumn=True Then begin
    if SIndexs=6 Then begin

    { St1:=Query1.FieldByName('Gcode').AsString;
      St2:=Query1.FieldByName('Gqut1').AsString;

      Sqlen := 'UPDATE G1_Ggeo SET Gqut1=@Gqut1 '+'WHERE Gcode=''@Gcode'' and Hcode=''@Hcode''';
      Translate(Sqlen, '@Gcode', St1);
      TransAuto(Sqlen, '@Gqut1', St2);
      Translate(Sqlen, '@Hcode', Sobo29.Edit107.Text);

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.BusyLoop;
      if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update); }

    end;
    end;
  end;
  end;
end;

procedure TSeek70.DBGrid1KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
var sColumn: Boolean;
    sIndexs: Integer;
begin
  if Query1.Active=True Then begin
  SIndexs:=DBGrid1.SelectedIndex;
  sColumn:=DBGrid1.Columns.Items[SIndexs].Grid.EditorMode;
  if Key=VK_RETURN Then begin
    if SIndexs=6 Then begin
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),0,0);
      Keybd_event(VK_DOWN,MapVirtualKey(VK_DOWN,0),KEYEVENTF_KEYUP,0);
    end;
  end;
  end;
end;

procedure TSeek70.BitBtn101Click(Sender: TObject);
begin
  if Edit1.Text='' Then Exit;
  Sobo29.Button201Click(Self)
end;

procedure TSeek70.DBGrid1TitleClick(Column: TColumn);
begin
  Base10.ColumnSX(Query1,Column);
end;

end.
