unit Seok02;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit, DBGridEh;

type
  TSeok20 = class(TForm)
    Panel100: TFlatPanel;
    Panel201: TFlatPanel;
    Panel101: TFlatPanel;
    Edit1: TFlatEdit;
    Button001: TFlatSpeedButton;
    Button101: TFlatButton;
    Button102: TFlatButton;
    BitBtn101: TBitBtn;
    BitBtn102: TBitBtn;
    DataSource1: TDataSource;
    Query1: TClientDataSet;
    Query1ID: TFloatField;
    Query1HCODE: TStringField;
    Query1HNAME: TStringField;
    Query1GCODE: TStringField;
    Query1GNAME: TStringField;
    Query1NAME1: TStringField;
    Query1NAME2: TStringField;
    Query1GNUMB: TStringField;
    Query1GBIGO: TStringField;
    Query1GSSUM: TFloatField;
    DBGrid101: TDBGridEh;
    Query1CODE5: TStringField;
    procedure FilterTing(Str:String);
    procedure FilterSeek(Str:String);
    procedure Edit1KeyPress(Sender: TObject; var Key: Char);
    procedure Button001Click(Sender: TObject);
    procedure DBGrid101DblClick(Sender: TObject);
    procedure Edit1Enter(Sender: TObject);
    procedure FormShow(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seok20: TSeok20;

implementation

{$R *.DFM}

uses Base01, TcpLib, Subu43;

procedure TSeok20.FilterTing(Str:String);
var St1,St2: String;
begin
  Base10.OpenExit(Query1);
  Base10.OpenShow(Query1);

//if Str='' Then Exit;

//St1:='S.Gdate'+'='+#39+Sobo43.Edit101.Text+#39;
  St1:='S.Gdate'+' ='+#39+Sobo43.Edit101.Text+#39+' and '+
       'S.Gubun'+' ='+#39+'출고'+#39+' and '+
       'S.Yesno'+' ='+#39+'2'+#39+' and '+
       'S.Ocode'+' ='+#39+'B'+#39+' and '+
       'S.Scode'+' ='+#39+'X'+#39;

  St1:=St1+' and '+'('+
       'Y.Gname'+' Like '+#39+'%'+'-택배'+'%'+#39+' or '+
       'Y.Gname'+' Like '+#39+'%'+'-천일'+'%'+#39+')';

  St2:=St1+' and '+'('+
       'Y.Gcode'+' < '+#39+'9'+#39+')';

  Sqlen := 'Select S.Gdate,S.Hcode,S.Gcode,S.Jubun,Y.Gname,Sum(S.Gsqut),Sum(S.Gssum) '+
           'From S1_Ssub S, G1_Ggeo Y '+
           'Where S.Gcode=Y.Gcode and '+St2;

  Sqlen := Sqlen+' Group by S.Gdate,S.Hcode,S.Gcode,S.Jubun,Y.Gname';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    Query1.Append;
    Query1.FieldByName('Code5').AsString:='N';
    Query1.FieldByName('Hcode').AsString:=SGrid.Cells[ 1,List1];
    Query1.FieldByName('Gname').AsString:=SGrid.Cells[ 4,List1];
    Query1.FieldByName('Gssum').AsString:='0';
  //Query1.FieldByName('Gssum').AsString:=SGrid.Cells[ 6,List1];

    Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
    Query1.FieldByName('Hname').Value:=Base10.Seek_Name(Sqlen);

    Query1.Post;
  end;

  St2:=St1+' and '+'('+
       'Y.Gcode'+' >= '+#39+'9'+#39+')';

  Sqlen := 'Select S.Gdate,S.Hcode,S.Gcode,S.Jubun,Y.Gname,Sum(S.Gsqut),Sum(S.Gssum) '+
           'From S1_Ssub S, G1_Ggeo Y '+
           'Where S.Hcode=Y.Hcode and S.Gcode=Y.Gcode and '+St2;

  Sqlen := Sqlen+' Group by S.Gdate,S.Hcode,S.Gcode,S.Jubun,Y.Gname';

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  List1:=0;
  While SGrid.RowCount-1 > List1 do begin
  List1:=List1+1;

    Query1.Append;
    Query1.FieldByName('Code5').AsString:='N';
    Query1.FieldByName('Hcode').AsString:=SGrid.Cells[ 1,List1];
    Query1.FieldByName('Gname').AsString:=SGrid.Cells[ 4,List1];
    Query1.FieldByName('Gssum').AsString:='0';
  //Query1.FieldByName('Gssum').AsString:=SGrid.Cells[ 6,List1];

    Sqlen := 'Select Gname From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', SGrid.Cells[ 1,List1]);
    Query1.FieldByName('Hname').Value:=Base10.Seek_Name(Sqlen);

    Query1.Post;
  end;

  Query1.First;
end;

procedure TSeok20.FilterSeek(Str:String);
begin
//
end;

procedure TSeok20.Edit1KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  FilterTing(Edit1.Text);
end;

procedure TSeok20.Button001Click(Sender: TObject);
begin
  FilterTing(Edit1.Text);
end;

procedure TSeok20.DBGrid101DblClick(Sender: TObject);
begin
  ModalResult:=mrOK;
end;

procedure TSeok20.Edit1Enter(Sender: TObject);
begin
  FilterTing(Edit1.Text);
end;

procedure TSeok20.FormShow(Sender: TObject);
begin
  Sobo43.Button101Click(Self);
  Base10.OpenExit(Query1);
  Base10.OpenShow(Query1);
  DBGrid101.SetFocus;
  FilterTing(Edit1.Text);
end;

end.
