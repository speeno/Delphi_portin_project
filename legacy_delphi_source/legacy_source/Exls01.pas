unit Exls01;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit, Mask,
  TFlatMaskEditUnit, DBGridEh, dxCore, dxButtons, ToolEdit, ComObj;

type
  TExls10 = class(TForm)
    DataSource1: TDataSource;
    Em_Sub01: TClientDataSet;
    Panel100: TFlatPanel;
    Panel102: TFlatPanel;
    DBGrid101: TDBGridEh;
    Panel101: TFlatPanel;
    Panel103: TFlatPanel;
    Panel300: TFlatPanel;
    Edit300: TFlatMaskEdit;
    Edit301: TFlatEdit;
    Panel301: TFlatPanel;
    Edit302: TFlatEdit;
    Edit304: TFlatEdit;
    Edit303: TFlatEdit;
    Panel302: TFlatPanel;
    Panel303: TFlatPanel;
    Panel201: TFlatPanel;
    Label1: TLabel;
    Edit001: TFlatEdit;
    Edit002: TFlatEdit;
    OpenDialog1: TOpenDialog;
    SaveDialog1: TSaveDialog;
    Button101: TdxButton;
    Button102: TdxButton;
    Button301: TdxButton;
    Edit003: TFlatEdit;
    Edit004: TFlatEdit;
    Button302: TdxButton;
    Button303: TdxButton;
    DateEdit1: TDateEdit;
    Em_Sub01HCODE: TStringField;
    Em_Sub01HNAME: TStringField;
    Em_Sub01NAME0: TStringField;
    Em_Sub01GSQUT: TFloatField;
    Em_Sub01GDANG: TFloatField;
    Em_Sub01GSSUM: TFloatField;
    Em_Sub01GBIGO: TStringField;
    Em_Sub01NAME1: TStringField;
    Em_Sub01NAME2: TStringField;
    Em_Sub01CODE1: TStringField;
    Em_Sub01CODE2: TStringField;
    procedure FormActivate(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Button101Click(Sender: TObject);
    procedure Button102Click(Sender: TObject);
    procedure Button301Click(Sender: TObject);
    procedure Button302Click(Sender: TObject);
    procedure Button303Click(Sender: TObject);
    procedure DateEdit1ButtonClick(Sender: TObject);
    procedure DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Exls10: TExls10;

implementation

{$R *.DFM}

uses Base01, TcpLib, Exls07, Subu43;

procedure TExls10.FormActivate(Sender: TObject);
begin
  nForm:='E1';
  tSqry:=Em_Sub01;
end;

procedure TExls10.FormShow(Sender: TObject);
begin
  Edit300.Text:=FormatDateTime('yyyy"."mm"."dd',Date);
  DBGrid101.SetFocus;
end;

procedure TExls10.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  Base10.OpenExit(tSqry);
end;

procedure TExls10.Button101Click(Sender: TObject);
begin
  if tSqry.Active=True Then begin

    tSqry.First;
    While tSqry.EOF=False do begin

    if(tSqry.FieldByName('Code1').AsString= 'N')and
      (tSqry.FieldByName('Code2').AsString= 'N')then begin
    //(tSqry.FieldByName('Gdate').AsString>=Edit101.Text)then begin
      Base10.T4_Sub31.Append;
      Base10.T4_Sub31.FieldByName('Gdate').AsString:=Edit300.Text;
      Base10.T4_Sub31.FieldByName('Hcode').AsString:=tSqry.FieldByname('Hcode').AsString;
      Base10.T4_Sub31.FieldByName('Hname').AsString:=tSqry.FieldByname('Hname').AsString;
      Base10.T4_Sub31.FieldByName('Gnumb').AsString:=tSqry.FieldByname('Name2').AsString;
      Base10.T4_Sub31.FieldByName('Name1').AsString:='';
      Base10.T4_Sub31.FieldByName('Gname').AsString:=tSqry.FieldByname('Name1').AsString;
      Base10.T4_Sub31.FieldByName('Name2').AsString:='';
      Base10.T4_Sub31.FieldByName('Gbigo').AsString:=tSqry.FieldByname('Gbigo').AsString;
      Base10.T4_Sub31.FieldByName('Gsqut').AsFloat :=tSqry.FieldByname('Gsqut').AsFloat;
      Base10.T4_Sub31.FieldByName('Gdang').AsFloat :=tSqry.FieldByname('Gdang').AsFloat;
      Base10.T4_Sub31.FieldByName('Gssum').AsFloat :=tSqry.FieldByname('Gssum').AsFloat;
      Base10.T4_Sub31.Post;

      tSqry.Edit;
      tSqry.FieldByName('Code2').AsString:= 'O';
      tSqry.Post;
    end;
      tSqry.Next;
    end;
    tSqry.First;

    ShowMessage('저장되었습니다.');
  end;
end;

procedure TExls10.Button102Click(Sender: TObject);
var
  p_Hcode,p_Hname,p_Name0,p_Yesno: String;
  mRow, mCol : Integer; // 순환변수
  XL, XArr, XSheets: Variant;
begin
  if OpenDialog1.Execute then
  begin
    Base10.OpenShow(tSqry);
    XL := CreateOLEObject('Excel.Application');

    XL.Visible := False;
    XL.Displayalerts := False;
    XArr := XL.workbooks.Open(Opendialog1.FileName);
    XArr := XL.workbooks.Item[1];

    XSheets := XArr.worksheets.Item[1];


      For mRow := 1 to XSheets.UsedRange.Rows.Count do   //3
      begin
      if vartostr(XSheets.Cells[mRow, 1])<>'' then begin


        p_Yesno:='';
        p_Hcode:='';
        p_Hname:='';
        p_Name0:=vartostr(XSheets.Cells[mRow, 1]);

        Sqlen := 'Select Hcode From Sm_Ggeo Where '+'Name0=''@Name0'' and Gubun=''@Gubun''  ';
        Translate(Sqlen, '@Name0', p_Name0);
        Translate(Sqlen, '@Gubun', '01');
        p_Hcode:=Base10.Seek_Name(Sqlen);

        if p_Hcode='' then begin
          Sqlen := 'Select Gcode,Gname From G7_Ggeo Where '+'Gname=''@Gname'' ';
          Translate(Sqlen, '@Gname', p_Name0 );
          Base10.Socket.RunSQL(Sqlen);
          Base10.Socket.busyloop;
          if Base10.Socket.Body_Data <> 'NODATA' then begin
             Base10.Socket.MakeData;
             p_Hcode:=Base10.Socket.GetData(1, 1);
             p_Hname:=Base10.Socket.GetData(1, 2);
          end;
        end else begin
             p_Hname:=p_Name0;
        end;

        tSqry.Append;
        tSqry.FieldByname('Hcode').AsString:=p_Hcode;
        tSqry.FieldByname('Hname').AsString:=p_Hname;
        tSqry.FieldByname('Name0').AsString:=p_Name0;
        tSqry.FieldByname('Name1').AsString:=vartostr(XSheets.Cells[mRow, 2]);
        tSqry.FieldByname('Name2').AsString:=vartostr(XSheets.Cells[mRow, 3]);
        tSqry.FieldByname('Gsqut').AsFloat :=0;
        tSqry.FieldByname('Gdang').AsFloat :=0;
        tSqry.FieldByname('Gssum').AsFloat :=StrToIntDef(vartostr(XSheets.Cells[mRow,4]),0);
        tSqry.FieldByname('Gbigo').AsString:='';

        tSqry.FieldByname('Code1').AsString:='N';

        if p_Hname='' then
        tSqry.FieldByname('Code1').AsString:='O';

        if p_Name0='' then
        tSqry.FieldByname('Code1').AsString:='O';

        if p_Yesno='' then
        tSqry.FieldByname('Code2').AsString:='N'
        else
        tSqry.FieldByname('Code2').AsString:='O';

        tSqry.Post;
      end;
      end;
    XL.workbooks.close;
    XL.quit;
    XL := unassigned;

    tSqry.First;
  end;
end;

procedure TExls10.Button301Click(Sender: TObject);
begin
  Exls70.ShowModal;
//Exls70.Show;
end;

procedure TExls10.Button302Click(Sender: TObject);
begin
//
end;

procedure TExls10.Button303Click(Sender: TObject);
begin
//
end;

procedure TExls10.DateEdit1ButtonClick(Sender: TObject);
begin
  DateEdit1.Date :=StrToDate(Edit300.Text);
end;

procedure TExls10.DateEdit1AcceptDate(Sender: TObject; var ADate: TDateTime; var Action: Boolean);
begin
  Edit300.Text :=DateToStr(ADate);
end;

end.
