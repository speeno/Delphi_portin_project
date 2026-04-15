unit Tong01;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  ComCtrls, Menus, OleCtrls, Vcf1, ToolWin, ImgList, AxCtrls;

type
  TTong10 = class(TForm)
    MainMenu1: TMainMenu;
    Menu10: TMenuItem;
    Menu11: TMenuItem;
    Menu12: TMenuItem;
    Menu13: TMenuItem;
    Menu01: TMenuItem;
    Menu14: TMenuItem;
    Menu15: TMenuItem;
    Menu16: TMenuItem;
    Menu02: TMenuItem;
    Menu17: TMenuItem;
    Menu20: TMenuItem;
    Menu21: TMenuItem;
    Menu22: TMenuItem;
    Menu23: TMenuItem;
    Menu03: TMenuItem;
    Menu24: TMenuItem;
    Menu25: TMenuItem;
    Menu04: TMenuItem;
    Menu26: TMenuItem;
    Menu27: TMenuItem;
    Menu05: TMenuItem;
    Menu28: TMenuItem;
    Menu30: TMenuItem;
    Menu31: TMenuItem;
    Menu32: TMenuItem;
    Menu33: TMenuItem;
    Menu34: TMenuItem;
    Menu35: TMenuItem;
    Menu36: TMenuItem;
    Menu37: TMenuItem;
    Menu07: TMenuItem;
    Menu38: TMenuItem;
    Menu40: TMenuItem;
    Menu41: TMenuItem;
    Menu42: TMenuItem;
    Menu43: TMenuItem;
    PopupMenu1: TPopupMenu;
    Sheet2: TMenuItem;
    Add2: TMenuItem;
    Delete2: TMenuItem;
    Name2: TMenuItem;
    Scale2: TMenuItem;
    N752: TMenuItem;
    N1002: TMenuItem;
    N1252: TMenuItem;
    Alignment2: TMenuItem;
    OpenDialog1: TOpenDialog;
    SaveDialog1: TSaveDialog;
    PrintDialog1: TPrintDialog;
    PrinterSetupDialog1: TPrinterSetupDialog;
    ToolbarImages: TImageList;
    F1Book1: TF1Book;
    StatusBar1: TStatusBar;
    ToolBar: TToolBar;
    ToolButton01: TToolButton;
    ToolButton02: TToolButton;
    ToolButton03: TToolButton;
    ToolButton91: TToolButton;
    ToolButton04: TToolButton;
    ToolButton05: TToolButton;
    ToolButton06: TToolButton;
    ToolButton92: TToolButton;
    ToolButton07: TToolButton;
    ToolButton08: TToolButton;
    ToolButton09: TToolButton;
    ToolButton93: TToolButton;
    ToolButton10: TToolButton;
    ToolButton94: TToolButton;
    ToolButton11: TToolButton;
    ToolButton12: TToolButton;
    ToolButton13: TToolButton;
    ToolButton14: TToolButton;
    ToolButton95: TToolButton;
    ToolButton15: TToolButton;
    ToolButton16: TToolButton;
    procedure FormCreate(Sender: TObject);
    procedure ShowHint(Sender: TObject);
    procedure Menu11Click(Sender: TObject);
    procedure Menu12Click(Sender: TObject);
    procedure Menu13Click(Sender: TObject);
    procedure Menu14Click(Sender: TObject);
    procedure Menu15Click(Sender: TObject);
    procedure Menu16Click(Sender: TObject);
    procedure Menu17Click(Sender: TObject);
    procedure Menu21Click(Sender: TObject);
    procedure Menu22Click(Sender: TObject);
    procedure Menu23Click(Sender: TObject);
    procedure Menu24Click(Sender: TObject);
    procedure Menu25Click(Sender: TObject);
    procedure Menu26Click(Sender: TObject);
    procedure Menu27Click(Sender: TObject);
    procedure Menu28Click(Sender: TObject);
    procedure Menu31Click(Sender: TObject);
    procedure Menu32Click(Sender: TObject);
    procedure Menu33Click(Sender: TObject);
    procedure Menu35Click(Sender: TObject);
    procedure Menu36Click(Sender: TObject);
    procedure Menu37Click(Sender: TObject);
    procedure Menu38Click(Sender: TObject);
    procedure Menu41Click(Sender: TObject);
    procedure Menu42Click(Sender: TObject);
    procedure Menu43Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Tong10: TTong10;

implementation

{$R *.DFM}

procedure TTong10.FormCreate(Sender: TObject);
begin
  F1Book1.ShowEditBar := True;
  Application.OnHint := ShowHint;
end;

procedure TTong10.ShowHint(Sender: TObject);
begin
  if Length(Application.Hint) > 0 then
    StatusBar1.SimpleText := Application.Hint;
end;

procedure TTong10.Menu11Click(Sender: TObject);
begin
  F1Book1.InitTable;
end;

procedure TTong10.Menu12Click(Sender: TObject);
var Excel4, Excel5, TabbedText, FormulaOne : SmallInt;
begin
  Excel4 := F1FileExcel4;
  Excel5 := F1FileExcel5;
  TabbedText := F1FileTabbedText;
  FormulaOne := F1FileFormulaOne;
  if OpenDialog1.Execute then begin
    case OpenDialog1.FilterIndex of
    1 : F1Book1.read(Opendialog1.Filename, Excel4);
    2 : F1Book1.read(Opendialog1.Filename, Excel5);
    3 : F1Book1.read(Opendialog1.Filename, TabbedText);
    4 : F1Book1.read(Opendialog1.Filename, FormulaOne);
    end;
  end;
end;

procedure TTong10.Menu13Click(Sender: TObject);
var Excel4, Excel5, TabbedText, FormulaOne : SmallInt;
begin
  Excel4 := F1FileExcel4;
  Excel5 := F1FileExcel5;
  TabbedText := F1FileTabbedText;
  FormulaOne := F1FileFormulaOne;
  SaveDialog1.FileName := OpenDialog1.FileName;
  SaveDialog1.FilterIndex := OpenDialog1.FilterIndex;
  if SaveDialog1.Execute then begin
    case SaveDialog1.FilterIndex of
    1 : F1Book1.Write(Savedialog1.Filename, Excel4);
    2 : F1Book1.Write(Savedialog1.Filename, Excel5);
    3 : F1Book1.Write(SaveDialog1.Filename, TabbedText);
    4 : F1Book1.Write(SaveDialog1.Filename, FormulaOne);
    end;
  end;
end;

procedure TTong10.Menu14Click(Sender: TObject);
begin
  F1Book1.FilePageSetupDlg;
end;

procedure TTong10.Menu15Click(Sender: TObject);
begin
  if PrintDialog1.execute then
     F1Book1.FilePrint(False);
end;

procedure TTong10.Menu16Click(Sender: TObject);
begin
  PrinterSetupDialog1.Execute;
end;

procedure TTong10.Menu17Click(Sender: TObject);
begin
  Close;
end;

procedure TTong10.Menu21Click(Sender: TObject);
begin
  F1Book1.EditCut;
end;

procedure TTong10.Menu22Click(Sender: TObject);
begin
  F1Book1.EditCopy;
end;

procedure TTong10.Menu23Click(Sender: TObject);
begin
  F1Book1.EditPaste;
end;

procedure TTong10.Menu24Click(Sender: TObject);
begin
  F1Book1.EditInsert(F1ShiftRows);
end;

procedure TTong10.Menu25Click(Sender: TObject);
begin
  F1Book1.EditInsert(F1ShiftCols);
end;

procedure TTong10.Menu26Click(Sender: TObject);
begin
  F1Book1.EditDelete(F1ShiftRows);
end;

procedure TTong10.Menu27Click(Sender: TObject);
begin
  F1Book1.EditDelete(F1ShiftCols);
end;

procedure TTong10.Menu28Click(Sender: TObject);
var obj1 : LongInt;
begin
  With F1Book1 do
  ObjNew(F1ObjChart, SelEndCol + 1 , SelStartRow, SelEndCol + 4, SelStartRow + 5, obj1);
end;

procedure TTong10.Menu31Click(Sender: TObject);
begin
  F1Book1.FormatAlignmentDlg;
end;

procedure TTong10.Menu32Click(Sender: TObject);
begin
  F1Book1.FormatFontDlg;
end;

procedure TTong10.Menu33Click(Sender: TObject);
begin
  F1Book1.FormatPatternDlg;
end;

procedure TTong10.Menu35Click(Sender: TObject);
begin
  Menu35.Checked := True;
  F1Book1.ViewScale := 75;
end;

procedure TTong10.Menu36Click(Sender: TObject);
begin
  Menu36.Checked := True;
  F1Book1.ViewScale := 100;
end;

procedure TTong10.Menu37Click(Sender: TObject);
begin
  Menu37.Checked := True;
  F1Book1.ViewScale := 125;
end;

procedure TTong10.Menu38Click(Sender: TObject);
begin
  Menu38.Checked := not Menu38.Checked;
  F1Book1.ShowEditBar := not F1Book1.ShowEditBar;
end;

procedure TTong10.Menu41Click(Sender: TObject);
begin
  F1Book1.InsertSheets(F1Book1.NumSheets + 1, 1);
end;

procedure TTong10.Menu42Click(Sender: TObject);
begin
  if F1Book1.NumSheets = 1 then exit;
     F1Book1.EditDeleteSheets;
end;

procedure TTong10.Menu43Click(Sender: TObject);
var ret : string;
begin
  ret := InputBox('New Sheet Name Dialog', 'New Sheet Name',
                   F1Book1.SheetName[F1Book1.Sheet]);
  F1Book1.SheetName[F1Book1.Sheet] := ret;
end;

end.
