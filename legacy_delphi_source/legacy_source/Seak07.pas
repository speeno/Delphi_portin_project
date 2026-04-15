unit Seak07;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Db, DBClient, StdCtrls, ExtCtrls, Buttons, Grids, DBGrids, Mylabel,
  TFlatPanelUnit, SConnect; { BDE, DBTables; }

type
  TSeak70 = class(TForm)
    DataSource1: TDataSource;
    DataSource2: TDataSource;
    Panel1: TFlatPanel;
    Panel2: TFlatPanel;
    Panel3: TFlatPanel;
    DBGrid1: TDBGrid;
    DBGrid2: TDBGrid;
    BitBtn1: TBitBtn;
    BitBtn2: TBitBtn;
    BitBtn3: TBitBtn;
    BitBtn4: TBitBtn;
    BitBtn5: TBitBtn;
    BitBtn6: TBitBtn;
    Label1: TmyLabel3d;
    Label2: TmyLabel3d;
    Label3: TmyLabel3d;
    Label4: TmyLabel3d;
    SaveDialog1: TSaveDialog;
    procedure FormActivate(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure DBGrid2KeyPress(Sender: TObject; var Key: Char);
    procedure DBGrid2KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
    procedure BitBtn1Click(Sender: TObject);
    procedure BitBtn2Click(Sender: TObject);
    procedure BitBtn3Click(Sender: TObject);
    procedure BitBtn4Click(Sender: TObject);
    procedure BitBtn5Click(Sender: TObject);
    procedure BitBtn6Click(Sender: TObject);
    procedure DataSource1DataChange(Sender: TObject; Field: TField);
    procedure DataSource2DataChange(Sender: TObject; Field: TField);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seak70: TSeak70;
  aSqry,bSqry: TClientDataSet;

implementation

{$R *.DFM}

uses Base01, Tong04, Tong05, TcpLib;

procedure TSeak70.FormActivate(Sender: TObject);
begin
//
end;

procedure TSeak70.FormShow(Sender: TObject);
var St1,St2,St3,St4,St5: String;
begin
  DataSource1.Enabled:=False;
  DataSource2.Enabled:=False;
  aSqry:=Base10.T2_Sub12;
  bSqry:=Base10.T2_Sub22;
  Base10.OpenShow(aSqry);
  Base10.OpenShow(bSqry);
  if FileExists(GetExecPath + 'Data\Chulptn.cds') Then
  aSqry.LoadFromFile(GetExecPath + 'Data\Chulptn.cds');
  aSqry.First;
  bSqry.First;
  While aSqry.EOF=False do begin
    St1:=aSqry.FieldByName('Gdate').AsString;
    St2:=aSqry.FieldByName('Gcode').AsString;
    St3:=aSqry.FieldByName('Scode').AsString;
    St4:=aSqry.FieldByName('Gubun').AsString;
    St5:=aSqry.FieldByName('Jubun').AsString;
    if bSqry.Locate('Gdate;Gcode;Scode;Gubun;Jubun',VarArrayOf([St1,St2,St3,St4,St5]),[loCaseInsensitive])=False then begin
      bSqry.Append;
      bSqry.FieldByName('Gdate').AsString:=St1;
      bSqry.FieldByName('Gcode').AsString:=St2;
      bSqry.FieldByName('Scode').AsString:=St3;
      bSqry.FieldByName('Gubun').AsString:=St4;
      bSqry.FieldByName('Jubun').AsString:=St5;
      bSqry.FieldByName('Gname').AsString:=aSqry.FieldByName('Gname').AsString;
      bSqry.Post;
    end;
    aSqry.Next;
  end;
  aSqry.First;
  bSqry.First;
  DataSource1.Enabled:=True;
  DataSource2.Enabled:=True;
end;

procedure TSeak70.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  aSqry.Filtered:=False;
  aSqry.SaveToFile(GetExecPath + 'Data\Chulptn.cds');
  Base10.OpenExit(aSqry);
  Base10.OpenExit(bSqry);
end;

procedure TSeak70.DBGrid2KeyPress(Sender: TObject; var Key: Char);
begin
//
end;

procedure TSeak70.DBGrid2KeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
begin
//
end;

procedure TSeak70.BitBtn1Click(Sender: TObject);
var St1,St2,St3,St4,St5,St6,St7: String;
begin
  Bmark:=nSqry.GetBookmark; nSqry.DisableControls;
  nSqry.First;
  While nSqry.EOF=False do begin
    aSqry.Append;
    aSqry.FieldByName('ID').Value   :=nSqry.FieldByName('ID').Value;
    aSqry.FieldByName('Scode').Value:=nSqry.FieldByName('Scode').Value;
    aSqry.FieldByName('Gcode').Value:=nSqry.FieldByName('Gcode').Value;
    aSqry.FieldByName('Gname').Value:=nSqry.FieldByName('Gname').Value;
    aSqry.FieldByName('Gdate').Value:=nSqry.FieldByName('Gdate').Value;
    aSqry.FieldByName('Gubun').Value:=nSqry.FieldByName('Gubun').Value;
    aSqry.FieldByName('Jubun').Value:=nSqry.FieldByName('Jubun').Value;
    aSqry.FieldByName('Pubun').Value:=nSqry.FieldByName('Pubun').Value;
    aSqry.FieldByName('Bcode').Value:=nSqry.FieldByName('Bcode').Value;
    aSqry.FieldByName('Bname').Value:=nSqry.FieldByName('Bname').Value;

    St6:=nSqry.FieldByName('Bcode').Value;
    St7:='';

    Sqlen := 'Select Gjeja From G4_Book Where '+D_Select+'Gcode=''@Gcode''';
    Translate(Sqlen, '@Gcode', St6);
    St7:=Base10.Seek_Name(Sqlen);

    aSqry.FieldByName('Gjeja').Value:=St7;
    aSqry.FieldByName('Ocode').Value:=nSqry.FieldByName('Ocode').Value;
    aSqry.FieldByName('Gsqut').Value:=nSqry.FieldByName('Gsqut').Value;
    aSqry.FieldByName('Gdang').Value:=nSqry.FieldByName('Gdang').Value;
    aSqry.FieldByName('Grat1').Value:=nSqry.FieldByName('Grat1').Value;
    aSqry.FieldByName('Gssum').Value:=nSqry.FieldByName('Gssum').Value;
    aSqry.FieldByName('Gbigo').Value:=nSqry.FieldByName('Gbigo').Value;
    aSqry.Post;
    St1:=nSqry.FieldByName('Gdate').AsString;
    St2:=nSqry.FieldByName('Gcode').AsString;
    St3:=nSqry.FieldByName('Scode').AsString;
    St4:=nSqry.FieldByName('Gubun').AsString;
    St5:=nSqry.FieldByName('Jubun').AsString;
    if bSqry.Locate('Gdate;Gcode;Scode;Gubun;Jubun',VarArrayOf([St1,St2,St3,St4,St5]),[loCaseInsensitive])=False then begin
      bSqry.Append;
      bSqry.FieldByName('Gdate').AsString:=St1;
      bSqry.FieldByName('Gcode').AsString:=St2;
      bSqry.FieldByName('Scode').AsString:=St3;
      bSqry.FieldByName('Gubun').AsString:=St4;
      bSqry.FieldByName('Jubun').AsString:=St5;
      bSqry.FieldByName('Gname').AsString:=nSqry.FieldByName('Gname').AsString;
      bSqry.Post;
    end;
    nSqry.Next;
  end;
  nSqry.GotoBookmark(Bmark); nSqry.FreeBookmark(Bmark); nSqry.EnableControls;
end;

procedure TSeak70.BitBtn2Click(Sender: TObject);
begin
  bSqry.First;
  While bSqry.EOF=False do begin
    aSqry.First;
    While aSqry.EOF=False do begin
      aSqry.Delete;
    end;
    bSqry.Delete;
  end;
end;

procedure TSeak70.BitBtn3Click(Sender: TObject);
begin
  if aSqry.IsEmpty=False Then
  aSqry.Delete;
end;

procedure TSeak70.BitBtn4Click(Sender: TObject);
begin
  aSqry.SaveToFile(GetExecPath + 'Data\Chulpnt.cds');
{ Table1.DatabaseName:= GetExecPath + 'Data';
  Table1.Exclusive:=True;
  Table1.Open;
  DBIPackTable(Table1.DBHandle,Table1.Handle,nil,nil,True);
  Table1.Close;
  Table1.Exclusive:=False;
  Table1.Open;
  aSqry.First;
  While aSqry.EOF=False do begin
    Table1.Append;
    Table1.FieldByName('ID').Value   :=aSqry.FieldByName('ID').Value;
    Table1.FieldByName('Scode').Value:=aSqry.FieldByName('Scode').Value;
    Table1.FieldByName('Gcode').Value:=aSqry.FieldByName('Gcode').Value;
    Table1.FieldByName('Gname').Value:=aSqry.FieldByName('Gname').Value;
    Table1.FieldByName('Gdate').Value:=aSqry.FieldByName('Gdate').Value;
    Table1.FieldByName('Gubun').Value:=aSqry.FieldByName('Gubun').Value;
    Table1.FieldByName('Jubun').Value:=aSqry.FieldByName('Jubun').Value;
    Table1.FieldByName('Pubun').Value:=aSqry.FieldByName('Pubun').Value;
    Table1.FieldByName('Bcode').Value:=aSqry.FieldByName('Bcode').Value;
    Table1.FieldByName('Bname').Value:=aSqry.FieldByName('Bname').Value;
    Table1.FieldByName('Ocode').Value:=aSqry.FieldByName('Ocode').Value;
    Table1.FieldByName('Gsqut').Value:=aSqry.FieldByName('Gsqut').Value;
    Table1.FieldByName('Gdang').Value:=aSqry.FieldByName('Gdang').Value;
    Table1.FieldByName('Grat1').Value:=aSqry.FieldByName('Grat1').Value;
    Table1.FieldByName('Gssum').Value:=aSqry.FieldByName('Gssum').Value;
    Table1.FieldByName('Gbigo').Value:=aSqry.FieldByName('Gbigo').Value;
    Table1.Post;
    aSqry.Next;
  end;
  FDbiCopyTable(Table1.dbhandle, 'Pt_Prnt.DBF', 'St_Prnt.DBF');
  Table1.Close; }
  ShowMessage('저장 완료.');
end;

procedure TSeak70.BitBtn5Click(Sender: TObject);
begin
  oSqry:=aSqry;
  Bmark:=oSqry.GetBookmark; oSqry.DisableControls;
  oSqry.Filtered:=False;
  oSqry.First;
  Tong40.PrinTing04('1');
  oSqry.GotoBookmark(Bmark); oSqry.FreeBookmark(Bmark); oSqry.EnableControls;
  ShowMessage('전송파일 완료.');

{ Application.CreateForm(TTong50, Tong50);
  Tong50.ShowModal;
  Tong50.Free; }
end;

procedure TSeak70.BitBtn6Click(Sender: TObject);
begin
  SaveDialog1.InitialDir:=GetExecPath + 'Remote';
  
  if SaveDialog1.Execute then begin
    aSqry.SaveToFile(SaveDialog1.FileName);
  end;
end;

procedure TSeak70.DataSource1DataChange(Sender: TObject; Field: TField);
begin
  Label4.Caption:=aSqry.FieldByName('Gdate').AsString;
end;

procedure TSeak70.DataSource2DataChange(Sender: TObject; Field: TField);
var St1: String;
begin
  St1:='';
  St1:=St1+'Gdate'+'='+#39+bSqry.FieldByName('Gdate').AsString+#39+' and ';
  St1:=St1+'Gcode'+'='+#39+bSqry.FieldByName('Gcode').AsString+#39+' and ';
  St1:=St1+'Scode'+'='+#39+bSqry.FieldByName('Scode').AsString+#39+' and ';
  St1:=St1+'Gubun'+'='+#39+bSqry.FieldByName('Gubun').AsString+#39+' and ';
  St1:=St1+'Jubun'+'='+#39+bSqry.FieldByName('Jubun').AsString+#39;
  aSqry.Filter:=St1;
  aSqry.Filtered:=True;
end;

end.
