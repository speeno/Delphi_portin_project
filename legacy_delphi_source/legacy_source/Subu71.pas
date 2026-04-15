unit Subu71;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, ExtCtrls, Buttons, Mylabel, Mask, Db, Grids, DBGrids,
  TFlatPanelUnit, TFlatEditUnit, TFlatProgressBarUnit, TFlatMaskEditUnit,
  TFlatButtonUnit, TFlatComboBoxUnit, TFlatNumberUnit;

type
  TSobo71 = class(TForm)
    Panel002: TFlatPanel;
    DBGrid101: TDBGrid;
    Panel003: TFlatPanel;
  private
    { Private declarations }
  public
    { Public declarations }
  protected
  //  procedure WndProc(var Msg: TMessage); override;
  end;

  //const WM_Form_1_MOVE = WM_USER + $1111;

var
  Sobo71: TSobo71;

implementation

{$R *.DFM}

uses Subu21;
{
procedure TSobo71.WndProc(var msg: TMessage);
var
 MovingForm: TForm;
begin
  inherited WndProc(Msg);

  case Msg.Msg of
    WM_FORM_1_MOVE: begin
      MovingForm := TForm(Pointer(Msg.wParam)^);

      Left:=MovingForm.Left+MovingForm.Width;
      Top:=MovingForm.Top;
    end;
  end;
end; }

end.
