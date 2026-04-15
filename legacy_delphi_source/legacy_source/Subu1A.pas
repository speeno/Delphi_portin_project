unit Subu1A;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, TFlatNumberUnit, TFlatCheckBoxUnit, TFlatGroupBoxUnit, dxCore,
  dxButtons, IniFiles;

type
  TSobo1A = class(TForm)
    FlatGroupBox1: TFlatGroupBox;
    FlatCheckBox1: TFlatCheckBox;
    Label1: TLabel;
    Button102: TdxButton;
    Edit_lines: TFlatNumber;
    dxButton1: TdxButton;
    procedure FormShow(Sender: TObject);
    procedure Button102Click(Sender: TObject);
    procedure dxButton1Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Sobo1A: TSobo1A;

implementation

uses globalSystem;

{$R *.DFM}

procedure TSobo1A.FormShow(Sender: TObject);
var
  pFile_name: string;
  pIniFile: TIniFile;
begin
  pFile_name := Get_exe_path + 'Config.Ini';
  pIniFile := TIniFile.Create(pFile_name);

  //sheet_spec : 거래멩세서를 의미
  FlatCheckBox1.Checked := pIniFile.ReadBool('sheet_spec', 'dsply_won', false);//합계금액 앞에 "￦" 표시 여부
  Edit_lines.Value := pIniFile.ReadInteger('Print', 'List1', 12);//거래명세서 세부내용 라인 수

  pIniFile.Free;
end;

procedure TSobo1A.Button102Click(Sender: TObject);
var
  pFile_name: string;
  pIniFile: TIniFile;
begin
  pFile_name := Get_exe_path + 'Config.Ini';
  pIniFile := TIniFile.Create(pFile_name);

  //sheet_spec : 거래멩세서를 의미
  pIniFile.WriteBool('sheet_spec', 'dsply_won', FlatCheckBox1.Checked);//합계금액 앞에 "￦" 표시 여부
  pIniFile.WriteInteger('Print', 'List1', Trunc(Edit_lines.Value));//거래명세서 세부내용 라인 수

  pIniFile.Free;
  Close;
end;

procedure TSobo1A.dxButton1Click(Sender: TObject);
begin
  Close;
end;

end.
