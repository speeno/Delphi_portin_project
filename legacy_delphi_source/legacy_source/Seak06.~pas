unit Seak06;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ComCtrls, DBClient, IBQuery, TFlatTabControlUnit, TFlatEditUnit,
  TFlatGroupBoxUnit, TFlatButtonUnit, TFlatSpinEditUnit;

type
  TSeak60 = class(TForm)
    PageControl1: TPageControl;
    TabSheet1: TTabSheet;
    TabSheet2: TTabSheet;
    TabSheet3: TTabSheet;
    GroupBox11: TFlatGroupBox;
    GroupBox12: TFlatGroupBox;
    Button101: TFlatButton;
    Button102: TFlatButton;
    Label101: TLabel;
    Label102: TLabel;
    Label103: TLabel;
    Label104: TLabel;
    Label111: TLabel;
    Label112: TLabel;
    Label113: TLabel;
    Label114: TLabel;
    Label115: TLabel;
    Label116: TLabel;
    Label117: TLabel;
    Label118: TLabel;
    Label119: TLabel;
    Label120: TLabel;
    Label121: TLabel;
    Edit111: TFlatEdit;
    Edit112: TFlatEdit;
    Edit113: TFlatEdit;
    Edit121: TFlatEdit;
    Edit122: TFlatEdit;
    Edit123: TFlatEdit;
    Edit124: TFlatEdit;
    Edit131: TFlatEdit;
    Edit132: TFlatEdit;
    Edit133: TFlatEdit;
    Edit141: TFlatEdit;
    Edit142: TFlatEdit;
    Edit143: TFlatEdit;
    Edit151: TFlatEdit;
    Edit152: TFlatEdit;
    Edit153: TFlatEdit;
    SpinEdit101: TFlatSpinEditFloat;
    SpinEdit103: TFlatSpinEditFloat;
    SpinEdit102: TFlatSpinEditFloat;
    SpinEdit104: TFlatSpinEditFloat;
    SpinEdit111: TFlatSpinEditFloat;
    SpinEdit112: TFlatSpinEditFloat;
    SpinEdit113: TFlatSpinEditFloat;
    SpinEdit121: TFlatSpinEditFloat;
    SpinEdit122: TFlatSpinEditFloat;
    SpinEdit123: TFlatSpinEditFloat;
    SpinEdit124: TFlatSpinEditFloat;
    SpinEdit131: TFlatSpinEditFloat;
    SpinEdit132: TFlatSpinEditFloat;
    SpinEdit133: TFlatSpinEditFloat;
    SpinEdit141: TFlatSpinEditFloat;
    SpinEdit142: TFlatSpinEditFloat;
    SpinEdit143: TFlatSpinEditFloat;
    SpinEdit151: TFlatSpinEditFloat;
    SpinEdit152: TFlatSpinEditFloat;
    SpinEdit153: TFlatSpinEditFloat;
    SpinEdit154: TFlatSpinEditFloat;
    SpinEdit155: TFlatSpinEditFloat;
    SpinEdit156: TFlatSpinEditFloat;
    SpinEdit157: TFlatSpinEditFloat;
    SpinEdit158: TFlatSpinEditFloat;
    SpinEdit159: TFlatSpinEditFloat;
    SpinEdit190: TFlatSpinEditFloat;
    SpinEdit191: TFlatSpinEditFloat;
    SpinEdit192: TFlatSpinEditFloat;
    SpinEdit193: TFlatSpinEditFloat;
    SpinEdit194: TFlatSpinEditFloat;
    SpinEdit195: TFlatSpinEditFloat;
    SpinEdit196: TFlatSpinEditFloat;
    SpinEdit197: TFlatSpinEditFloat;
    SpinEdit198: TFlatSpinEditFloat;
    SpinEdit199: TFlatSpinEditFloat;
    GroupBox21: TFlatGroupBox;
    GroupBox22: TFlatGroupBox;
    Button201: TFlatButton;
    Button202: TFlatButton;
    Label201: TLabel;
    Label202: TLabel;
    Label203: TLabel;
    Label204: TLabel;
    Label211: TLabel;
    Label212: TLabel;
    Label213: TLabel;
    Label214: TLabel;
    Label215: TLabel;
    Label216: TLabel;
    Label217: TLabel;
    Label218: TLabel;
    Label219: TLabel;
    Label220: TLabel;
    Label221: TLabel;
    Label222: TLabel;
    Edit211: TFlatEdit;
    Edit221: TFlatEdit;
    Edit222: TFlatEdit;
    Edit223: TFlatEdit;
    Edit231: TFlatEdit;
    Edit232: TFlatEdit;
    Edit241: TFlatEdit;
    Edit251: TFlatEdit;
    Edit252: TFlatEdit;
    SpinEdit201: TFlatSpinEditFloat;
    SpinEdit202: TFlatSpinEditFloat;
    SpinEdit203: TFlatSpinEditFloat;
    SpinEdit204: TFlatSpinEditFloat;
    SpinEdit211: TFlatSpinEditFloat;
    SpinEdit212: TFlatSpinEditFloat;
    SpinEdit213: TFlatSpinEditFloat;
    SpinEdit214: TFlatSpinEditFloat;
    SpinEdit215: TFlatSpinEditFloat;
    SpinEdit216: TFlatSpinEditFloat;
    SpinEdit217: TFlatSpinEditFloat;
    SpinEdit218: TFlatSpinEditFloat;
    SpinEdit219: TFlatSpinEditFloat;
    SpinEdit221: TFlatSpinEditFloat;
    SpinEdit222: TFlatSpinEditFloat;
    SpinEdit223: TFlatSpinEditFloat;
    SpinEdit226: TFlatSpinEditFloat;
    SpinEdit227: TFlatSpinEditFloat;
    SpinEdit228: TFlatSpinEditFloat;
    SpinEdit229: TFlatSpinEditFloat;
    SpinEdit231: TFlatSpinEditFloat;
    SpinEdit232: TFlatSpinEditFloat;
    SpinEdit241: TFlatSpinEditFloat;
    SpinEdit242: TFlatSpinEditFloat;
    SpinEdit243: TFlatSpinEditFloat;
    SpinEdit244: TFlatSpinEditFloat;
    SpinEdit245: TFlatSpinEditFloat;
    SpinEdit246: TFlatSpinEditFloat;
    SpinEdit251: TFlatSpinEditFloat;
    SpinEdit252: TFlatSpinEditFloat;
    SpinEdit253: TFlatSpinEditFloat;
    SpinEdit254: TFlatSpinEditFloat;
    SpinEdit255: TFlatSpinEditFloat;
    SpinEdit256: TFlatSpinEditFloat;
    SpinEdit257: TFlatSpinEditFloat;
    SpinEdit258: TFlatSpinEditFloat;
    SpinEdit259: TFlatSpinEditFloat;
    SpinEdit271: TFlatSpinEditFloat;
    SpinEdit272: TFlatSpinEditFloat;
    SpinEdit273: TFlatSpinEditFloat;
    SpinEdit274: TFlatSpinEditFloat;
    SpinEdit275: TFlatSpinEditFloat;
    SpinEdit276: TFlatSpinEditFloat;
    SpinEdit277: TFlatSpinEditFloat;
    SpinEdit278: TFlatSpinEditFloat;
    SpinEdit279: TFlatSpinEditFloat;
    SpinEdit290: TFlatSpinEditFloat;
    SpinEdit291: TFlatSpinEditFloat;
    SpinEdit292: TFlatSpinEditFloat;
    SpinEdit293: TFlatSpinEditFloat;
    SpinEdit294: TFlatSpinEditFloat;
    SpinEdit295: TFlatSpinEditFloat;
    SpinEdit296: TFlatSpinEditFloat;
    SpinEdit297: TFlatSpinEditFloat;
    SpinEdit298: TFlatSpinEditFloat;
    SpinEdit299: TFlatSpinEditFloat;
    GroupBox31: TFlatGroupBox;
    GroupBox32: TFlatGroupBox;
    Button301: TFlatButton;
    Button302: TFlatButton;
    Label301: TLabel;
    Label302: TLabel;
    Label303: TLabel;
    Label304: TLabel;
    Label311: TLabel;
    Label312: TLabel;
    Label313: TLabel;
    Label314: TLabel;
    Label315: TLabel;
    Label316: TLabel;
    Label317: TLabel;
    Label318: TLabel;
    Label319: TLabel;
    Label320: TLabel;
    Label321: TLabel;
    Label322: TLabel;
    Label323: TLabel;
    Label324: TLabel;
    Label325: TLabel;
    Edit311: TFlatEdit;
    Edit312: TFlatEdit;
    Edit321: TFlatEdit;
    Edit322: TFlatEdit;
    Edit323: TFlatEdit;
    Edit331: TFlatEdit;
    Edit341: TFlatEdit;
    Edit342: TFlatEdit;
    Edit343: TFlatEdit;
    Edit351: TFlatEdit;
    Edit352: TFlatEdit;
    Edit353: TFlatEdit;
    SpinEdit301: TFlatSpinEditFloat;
    SpinEdit302: TFlatSpinEditFloat;
    SpinEdit303: TFlatSpinEditFloat;
    SpinEdit304: TFlatSpinEditFloat;
    SpinEdit311: TFlatSpinEditFloat;
    SpinEdit312: TFlatSpinEditFloat;
    SpinEdit313: TFlatSpinEditFloat;
    SpinEdit314: TFlatSpinEditFloat;
    SpinEdit315: TFlatSpinEditFloat;
    SpinEdit316: TFlatSpinEditFloat;
    SpinEdit317: TFlatSpinEditFloat;
    SpinEdit318: TFlatSpinEditFloat;
    SpinEdit319: TFlatSpinEditFloat;
    SpinEdit321: TFlatSpinEditFloat;
    SpinEdit322: TFlatSpinEditFloat;
    SpinEdit323: TFlatSpinEditFloat;
    SpinEdit331: TFlatSpinEditFloat;
    SpinEdit332: TFlatSpinEditFloat;
    SpinEdit333: TFlatSpinEditFloat;
    SpinEdit334: TFlatSpinEditFloat;
    SpinEdit335: TFlatSpinEditFloat;
    SpinEdit336: TFlatSpinEditFloat;
    SpinEdit337: TFlatSpinEditFloat;
    SpinEdit338: TFlatSpinEditFloat;
    SpinEdit339: TFlatSpinEditFloat;
    SpinEdit341: TFlatSpinEditFloat;
    SpinEdit342: TFlatSpinEditFloat;
    SpinEdit343: TFlatSpinEditFloat;
    SpinEdit344: TFlatSpinEditFloat;
    SpinEdit345: TFlatSpinEditFloat;
    SpinEdit346: TFlatSpinEditFloat;
    SpinEdit347: TFlatSpinEditFloat;
    SpinEdit348: TFlatSpinEditFloat;
    SpinEdit349: TFlatSpinEditFloat;
    SpinEdit351: TFlatSpinEditFloat;
    SpinEdit352: TFlatSpinEditFloat;
    SpinEdit353: TFlatSpinEditFloat;
    SpinEdit354: TFlatSpinEditFloat;
    SpinEdit355: TFlatSpinEditFloat;
    SpinEdit356: TFlatSpinEditFloat;
    SpinEdit357: TFlatSpinEditFloat;
    SpinEdit358: TFlatSpinEditFloat;
    SpinEdit359: TFlatSpinEditFloat;
    SpinEdit390: TFlatSpinEditFloat;
    SpinEdit391: TFlatSpinEditFloat;
    SpinEdit392: TFlatSpinEditFloat;
    SpinEdit393: TFlatSpinEditFloat;
    SpinEdit394: TFlatSpinEditFloat;
    SpinEdit395: TFlatSpinEditFloat;
    SpinEdit396: TFlatSpinEditFloat;
    SpinEdit397: TFlatSpinEditFloat;
    SpinEdit398: TFlatSpinEditFloat;
    SpinEdit399: TFlatSpinEditFloat;
    Button100: TFlatButton;
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure PageControl1Change(Sender: TObject);
    procedure Button101Click(Sender: TObject);
    procedure Button201Click(Sender: TObject);
    procedure Button301Click(Sender: TObject);
    procedure Button100Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seak60: TSeak60;
  wSqry: TClientDataSet;

implementation

{$R *.DFM}

uses Base01, TcpLib;

procedure TSeak60.FormShow(Sender: TObject);
begin
  PageControl1Change(Self);
end;

procedure TSeak60.FormClose(Sender: TObject; var Action: TCloseAction);
begin
//
end;

procedure TSeak60.PageControl1Change(Sender: TObject);
begin
  if PageControl1.ActivePage=TabSheet1 Then begin

    Sqlen := 'Select Top,L91,L92,L93,L94,L95,L96,L97,L98,L99 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '7');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // Top,Bottom
    SpinEdit190.Value:=StrToIntDef(SGrid.Cells[ 0,1],0);
    SpinEdit191.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit192.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit193.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit194.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit195.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit196.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit197.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit198.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit199.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L11,L12,L13,L14,L15,L16,L17,L18,L19 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '7');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 1
    SpinEdit111.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit112.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit113.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);

    Sqlen := 'Select Top,L21,L22,L23,L24,L25,L26,L27,L28,L29 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '7');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 2
    SpinEdit121.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit122.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit123.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit124.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);

    Sqlen := 'Select Top,L31,L32,L33,L34,L35,L36,L37,L38,L39 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '7');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 3
    SpinEdit131.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit132.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit133.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);

    Sqlen := 'Select Top,L41,L42,L43,L44,L45,L46,L47,L48,L49 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '7');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 4
    SpinEdit141.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit142.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit143.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);

    Sqlen := 'Select Top,L51,L52,L53,L54,L55,L56,L57,L58,L59 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '7');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 5
    SpinEdit151.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit152.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit153.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit154.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit155.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit156.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit157.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit158.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit159.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L61,L62,L63,L64,L65,L66,L67,L68,L69 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '7');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // Page
    SpinEdit101.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit102.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit103.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit104.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);

  end;
  if PageControl1.ActivePage=TabSheet2 Then begin

    Sqlen := 'Select Top,L91,L92,L93,L94,L95,L96,L97,L98,L99 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '8');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // Top,Bottom
    SpinEdit290.Value:=StrToIntDef(SGrid.Cells[ 0,1],0);
    SpinEdit291.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit292.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit293.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit294.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit295.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit296.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit297.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit298.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit299.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L11,L12,L13,L14,L15,L16,L17,L18,L19 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '8');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 1
    SpinEdit211.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit212.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit213.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit214.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit215.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit216.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit217.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit218.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit219.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L21,L22,L23,L24,L25,L26,L27,L28,L29 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '8');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 2
    SpinEdit221.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit222.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit223.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit226.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit227.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit228.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit229.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L31,L32,L33,L34,L35,L36,L37,L38,L39 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '8');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 3
    SpinEdit231.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit232.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);

    Sqlen := 'Select Top,L41,L42,L43,L44,L45,L46,L47,L48,L49 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '8');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 4
    SpinEdit241.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit242.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit243.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit244.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit245.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit246.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);

    Sqlen := 'Select Top,L51,L52,L53,L54,L55,L56,L57,L58,L59 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '8');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 5
    SpinEdit251.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit252.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit253.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit254.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit255.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit256.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit257.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit258.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit259.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L61,L62,L63,L64,L65,L66,L67,L68,L69 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '8');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // Page
    SpinEdit201.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit202.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit203.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit204.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);

    Sqlen := 'Select Top,L71,L72,L73,L74,L75,L76,L77,L78,L79 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '8');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 7
    SpinEdit271.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit272.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit273.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit274.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit275.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit276.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit277.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit278.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit279.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

  end;
  if PageControl1.ActivePage=TabSheet3 Then begin

    Sqlen := 'Select Top,L91,L92,L93,L94,L95,L96,L97,L98,L99 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '9');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // Top,Bottom
    SpinEdit390.Value:=StrToIntDef(SGrid.Cells[ 0,1],0);
    SpinEdit391.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit392.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit393.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit394.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit395.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit396.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit397.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit398.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit399.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L11,L12,L13,L14,L15,L16,L17,L18,L19 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '9');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 1
    SpinEdit311.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit312.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit313.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit314.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit315.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit316.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit317.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit318.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit319.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L21,L22,L23,L24,L25,L26,L27,L28,L29 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '9');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 2
    SpinEdit321.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit322.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit323.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);

    Sqlen := 'Select Top,L31,L32,L33,L34,L35,L36,L37,L38,L39 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '9');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 3
    SpinEdit331.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit332.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit333.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit334.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit335.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit336.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit337.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit338.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit339.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L41,L42,L43,L44,L45,L46,L47,L48,L49 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '9');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 4
    SpinEdit341.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit342.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit343.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit344.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit345.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit346.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit347.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit348.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit349.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L51,L52,L53,L54,L55,L56,L57,L58,L59 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '9');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // line 5
    SpinEdit351.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit352.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit353.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit354.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);
    SpinEdit355.Value:=StrToIntDef(SGrid.Cells[ 5,1],0);
    SpinEdit356.Value:=StrToIntDef(SGrid.Cells[ 6,1],0);
    SpinEdit357.Value:=StrToIntDef(SGrid.Cells[ 7,1],0);
    SpinEdit358.Value:=StrToIntDef(SGrid.Cells[ 8,1],0);
    SpinEdit359.Value:=StrToIntDef(SGrid.Cells[ 9,1],0);

    Sqlen := 'Select Top,L61,L62,L63,L64,L65,L66,L67,L68,L69 '+
             'From Gg_Magn Where Gu=''@Gu''';

    Translate(Sqlen, '@Gu', '9');

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.MakeGrid(SGrid)
    else ShowMessage(E_Open);

    // Page
    SpinEdit301.Value:=StrToIntDef(SGrid.Cells[ 1,1],0);
    SpinEdit302.Value:=StrToIntDef(SGrid.Cells[ 2,1],0);
    SpinEdit303.Value:=StrToIntDef(SGrid.Cells[ 3,1],0);
    SpinEdit304.Value:=StrToIntDef(SGrid.Cells[ 4,1],0);

  end;
end;

procedure TSeak60.Button101Click(Sender: TObject);
begin

    Sqlen :=
    'UPDATE Gg_Magn SET '+
    'Top=@Top,L91=@L91,L92=@L92,L93=@L93,L94=@L94,L95=@L95, '+
    'L96=@L96,L97=@L97,L98=@L98,L99=@L99,L11=@L11,L12=@L12, '+
    'L13=@L13,L21=@L21,L22=@L22,L23=@L23,L24=@L24,L31=@L31, ';
    Sqlon :=
    'L32=@L32,L33=@L33,L41=@L41,L42=@L42,L43=@L43,L51=@L51, '+
    'L52=@L52,L53=@L53,L54=@L54,L55=@L55,L56=@L56,L57=@L57, '+
    'L58=@L58,L59=@L59,L61=@L61,L62=@L62,L63=@L63,L64=@L64  '+
    'WHERE Gu=''@Gu''';

    TransAuto(Sqlen, '@Top', FloatToStr(SpinEdit190.Value));
    TransAuto(Sqlen, '@L91', FloatToStr(SpinEdit191.Value));
    TransAuto(Sqlen, '@L92', FloatToStr(SpinEdit192.Value));
    TransAuto(Sqlen, '@L93', FloatToStr(SpinEdit193.Value));
    TransAuto(Sqlen, '@L94', FloatToStr(SpinEdit194.Value));
    TransAuto(Sqlen, '@L95', FloatToStr(SpinEdit195.Value));
    TransAuto(Sqlen, '@L96', FloatToStr(SpinEdit196.Value));
    TransAuto(Sqlen, '@L97', FloatToStr(SpinEdit197.Value));
    TransAuto(Sqlen, '@L98', FloatToStr(SpinEdit198.Value));
    TransAuto(Sqlen, '@L99', FloatToStr(SpinEdit199.Value));
    TransAuto(Sqlen, '@L11', FloatToStr(SpinEdit111.Value));
    TransAuto(Sqlen, '@L12', FloatToStr(SpinEdit112.Value));
    TransAuto(Sqlen, '@L13', FloatToStr(SpinEdit113.Value));
    TransAuto(Sqlen, '@L21', FloatToStr(SpinEdit121.Value));
    TransAuto(Sqlen, '@L22', FloatToStr(SpinEdit122.Value));
    TransAuto(Sqlen, '@L23', FloatToStr(SpinEdit123.Value));
    TransAuto(Sqlen, '@L24', FloatToStr(SpinEdit124.Value));
    TransAuto(Sqlen, '@L31', FloatToStr(SpinEdit131.Value));
    TransAuto(Sqlon, '@L32', FloatToStr(SpinEdit132.Value));
    TransAuto(Sqlon, '@L33', FloatToStr(SpinEdit133.Value));
    TransAuto(Sqlon, '@L41', FloatToStr(SpinEdit141.Value));
    TransAuto(Sqlon, '@L42', FloatToStr(SpinEdit142.Value));
    TransAuto(Sqlon, '@L43', FloatToStr(SpinEdit143.Value));
    TransAuto(Sqlon, '@L51', FloatToStr(SpinEdit151.Value));
    TransAuto(Sqlon, '@L52', FloatToStr(SpinEdit152.Value));
    TransAuto(Sqlon, '@L53', FloatToStr(SpinEdit153.Value));
    TransAuto(Sqlon, '@L54', FloatToStr(SpinEdit154.Value));
    TransAuto(Sqlon, '@L55', FloatToStr(SpinEdit155.Value));
    TransAuto(Sqlon, '@L56', FloatToStr(SpinEdit156.Value));
    TransAuto(Sqlon, '@L57', FloatToStr(SpinEdit157.Value));
    TransAuto(Sqlon, '@L58', FloatToStr(SpinEdit158.Value));
    TransAuto(Sqlon, '@L59', FloatToStr(SpinEdit159.Value));
    TransAuto(Sqlon, '@L61', FloatToStr(SpinEdit101.Value));
    TransAuto(Sqlon, '@L62', FloatToStr(SpinEdit102.Value));
    TransAuto(Sqlon, '@L63', FloatToStr(SpinEdit103.Value));
    TransAuto(Sqlon, '@L64', FloatToStr(SpinEdit104.Value));
    Translate(Sqlon, '@Gu',  '7');

    Sqlen:=Sqlen+Sqlon;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

end;

procedure TSeak60.Button201Click(Sender: TObject);
begin

    Sqlen :=
    'UPDATE Gg_Magn SET '+
    'Top=@Top,L91=@L91,L92=@L92,L93=@L93,L94=@L94,L95=@L95, '+
    'L96=@L96,L97=@L97,L98=@L98,L99=@L99,L11=@L11,L12=@L12, '+
    'L13=@L13,L14=@L14,L15=@L15,L16=@L16,L17=@L17,L18=@L18, '+
    'L19=@L19,L21=@L21,L22=@L22,L23=@L23,L26=@L26,L27=@L27, '+
    'L28=@L28,L29=@L29,L31=@L31,L32=@L32,L41=@L41,L42=@L42, ';
    Sqlon :=
    'L43=@L43,L44=@L44,L45=@L45,L46=@L46,L51=@L51,L52=@L52, '+
    'L53=@L53,L54=@L54,L55=@L55,L56=@L56,L57=@L57,L58=@L58, '+
    'L59=@L59,L61=@L61,L62=@L62,L63=@L63,L64=@L64,L71=@L71, '+
    'L72=@L72,L73=@L73,L74=@L74,L75=@L75,L76=@L76,L77=@L77, '+
    'L78=@L78,L79=@L79 '+
    'WHERE Gu=''@Gu''';

    TransAuto(Sqlen, '@Top', FloatToStr(SpinEdit290.Value));
    TransAuto(Sqlen, '@L91', FloatToStr(SpinEdit291.Value));
    TransAuto(Sqlen, '@L92', FloatToStr(SpinEdit292.Value));
    TransAuto(Sqlen, '@L93', FloatToStr(SpinEdit293.Value));
    TransAuto(Sqlen, '@L94', FloatToStr(SpinEdit294.Value));
    TransAuto(Sqlen, '@L95', FloatToStr(SpinEdit295.Value));
    TransAuto(Sqlen, '@L96', FloatToStr(SpinEdit296.Value));
    TransAuto(Sqlen, '@L97', FloatToStr(SpinEdit297.Value));
    TransAuto(Sqlen, '@L98', FloatToStr(SpinEdit298.Value));
    TransAuto(Sqlen, '@L99', FloatToStr(SpinEdit299.Value));
    TransAuto(Sqlen, '@L11', FloatToStr(SpinEdit211.Value));
    TransAuto(Sqlen, '@L12', FloatToStr(SpinEdit212.Value));
    TransAuto(Sqlen, '@L13', FloatToStr(SpinEdit213.Value));
    TransAuto(Sqlen, '@L14', FloatToStr(SpinEdit214.Value));
    TransAuto(Sqlen, '@L15', FloatToStr(SpinEdit215.Value));
    TransAuto(Sqlen, '@L16', FloatToStr(SpinEdit216.Value));
    TransAuto(Sqlen, '@L17', FloatToStr(SpinEdit217.Value));
    TransAuto(Sqlen, '@L18', FloatToStr(SpinEdit218.Value));
    TransAuto(Sqlen, '@L19', FloatToStr(SpinEdit219.Value));
    TransAuto(Sqlen, '@L21', FloatToStr(SpinEdit221.Value));
    TransAuto(Sqlen, '@L22', FloatToStr(SpinEdit222.Value));
    TransAuto(Sqlen, '@L23', FloatToStr(SpinEdit223.Value));
    TransAuto(Sqlen, '@L26', FloatToStr(SpinEdit226.Value));
    TransAuto(Sqlen, '@L27', FloatToStr(SpinEdit227.Value));
    TransAuto(Sqlen, '@L28', FloatToStr(SpinEdit228.Value));
    TransAuto(Sqlen, '@L29', FloatToStr(SpinEdit229.Value));
    TransAuto(Sqlen, '@L31', FloatToStr(SpinEdit231.Value));
    TransAuto(Sqlen, '@L32', FloatToStr(SpinEdit232.Value));
    TransAuto(Sqlen, '@L41', FloatToStr(SpinEdit241.Value));
    TransAuto(Sqlen, '@L42', FloatToStr(SpinEdit242.Value));
    TransAuto(Sqlon, '@L43', FloatToStr(SpinEdit243.Value));
    TransAuto(Sqlon, '@L44', FloatToStr(SpinEdit244.Value));
    TransAuto(Sqlon, '@L45', FloatToStr(SpinEdit245.Value));
    TransAuto(Sqlon, '@L46', FloatToStr(SpinEdit246.Value));
    TransAuto(Sqlon, '@L51', FloatToStr(SpinEdit251.Value));
    TransAuto(Sqlon, '@L52', FloatToStr(SpinEdit252.Value));
    TransAuto(Sqlon, '@L53', FloatToStr(SpinEdit253.Value));
    TransAuto(Sqlon, '@L54', FloatToStr(SpinEdit254.Value));
    TransAuto(Sqlon, '@L55', FloatToStr(SpinEdit255.Value));
    TransAuto(Sqlon, '@L56', FloatToStr(SpinEdit256.Value));
    TransAuto(Sqlon, '@L57', FloatToStr(SpinEdit257.Value));
    TransAuto(Sqlon, '@L58', FloatToStr(SpinEdit258.Value));
    TransAuto(Sqlon, '@L59', FloatToStr(SpinEdit259.Value));
    TransAuto(Sqlon, '@L61', FloatToStr(SpinEdit201.Value));
    TransAuto(Sqlon, '@L62', FloatToStr(SpinEdit202.Value));
    TransAuto(Sqlon, '@L63', FloatToStr(SpinEdit203.Value));
    TransAuto(Sqlon, '@L64', FloatToStr(SpinEdit204.Value));
    TransAuto(Sqlon, '@L71', FloatToStr(SpinEdit271.Value));
    TransAuto(Sqlon, '@L72', FloatToStr(SpinEdit272.Value));
    TransAuto(Sqlon, '@L73', FloatToStr(SpinEdit273.Value));
    TransAuto(Sqlon, '@L74', FloatToStr(SpinEdit274.Value));
    TransAuto(Sqlon, '@L75', FloatToStr(SpinEdit275.Value));
    TransAuto(Sqlon, '@L76', FloatToStr(SpinEdit276.Value));
    TransAuto(Sqlon, '@L77', FloatToStr(SpinEdit277.Value));
    TransAuto(Sqlon, '@L78', FloatToStr(SpinEdit278.Value));
    TransAuto(Sqlon, '@L79', FloatToStr(SpinEdit279.Value));
    Translate(Sqlon, '@Gu',  '8');

    Sqlen:=Sqlen+Sqlon;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

end;

procedure TSeak60.Button301Click(Sender: TObject);
begin

    Sqlen :=
    'UPDATE Gg_Magn SET '+
    'Top=@Top,L91=@L91,L92=@L92,L93=@L93,L94=@L94,L95=@L95, '+
    'L96=@L96,L97=@L97,L98=@L98,L99=@L99,L11=@L11,L12=@L12, '+
    'L13=@L13,L14=@L14,L15=@L15,L16=@L16,L17=@L17,L18=@L18, '+
    'L19=@L19,L21=@L21,L22=@L22,L23=@L23,L31=@L31,L32=@L32, '+
    'L33=@L33,L34=@L34,L35=@L35,L36=@L36,L37=@L37,L38=@L38, ';
    Sqlon :=
    'L39=@L39,L41=@L41,L42=@L42,L43=@L43,L45=@L45,L46=@L46, '+
    'L47=@L47,L48=@L48,L49=@L49,L51=@L51,L52=@L52,L53=@L53, '+
    'L54=@L54,L55=@L55,L56=@L56,L57=@L57,L58=@L58,L59=@L59, '+
    'L61=@L61,L62=@L62,L63=@L63,L64=@L64 '+
    'WHERE Gu=''@Gu''';

    TransAuto(Sqlen, '@Top', FloatToStr(SpinEdit390.Value));
    TransAuto(Sqlen, '@L91', FloatToStr(SpinEdit391.Value));
    TransAuto(Sqlen, '@L92', FloatToStr(SpinEdit392.Value));
    TransAuto(Sqlen, '@L93', FloatToStr(SpinEdit393.Value));
    TransAuto(Sqlen, '@L94', FloatToStr(SpinEdit394.Value));
    TransAuto(Sqlen, '@L95', FloatToStr(SpinEdit395.Value));
    TransAuto(Sqlen, '@L96', FloatToStr(SpinEdit396.Value));
    TransAuto(Sqlen, '@L97', FloatToStr(SpinEdit397.Value));
    TransAuto(Sqlen, '@L98', FloatToStr(SpinEdit398.Value));
    TransAuto(Sqlen, '@L99', FloatToStr(SpinEdit399.Value));
    TransAuto(Sqlen, '@L11', FloatToStr(SpinEdit311.Value));
    TransAuto(Sqlen, '@L12', FloatToStr(SpinEdit312.Value));
    TransAuto(Sqlen, '@L13', FloatToStr(SpinEdit313.Value));
    TransAuto(Sqlen, '@L14', FloatToStr(SpinEdit314.Value));
    TransAuto(Sqlen, '@L15', FloatToStr(SpinEdit315.Value));
    TransAuto(Sqlen, '@L16', FloatToStr(SpinEdit316.Value));
    TransAuto(Sqlen, '@L17', FloatToStr(SpinEdit317.Value));
    TransAuto(Sqlen, '@L18', FloatToStr(SpinEdit318.Value));
    TransAuto(Sqlen, '@L19', FloatToStr(SpinEdit319.Value));
    TransAuto(Sqlen, '@L21', FloatToStr(SpinEdit321.Value));
    TransAuto(Sqlen, '@L22', FloatToStr(SpinEdit322.Value));
    TransAuto(Sqlen, '@L23', FloatToStr(SpinEdit323.Value));
    TransAuto(Sqlen, '@L31', FloatToStr(SpinEdit331.Value));
    TransAuto(Sqlen, '@L32', FloatToStr(SpinEdit332.Value));
    TransAuto(Sqlen, '@L33', FloatToStr(SpinEdit333.Value));
    TransAuto(Sqlen, '@L34', FloatToStr(SpinEdit334.Value));
    TransAuto(Sqlen, '@L35', FloatToStr(SpinEdit335.Value));
    TransAuto(Sqlen, '@L36', FloatToStr(SpinEdit336.Value));
    TransAuto(Sqlen, '@L37', FloatToStr(SpinEdit337.Value));
    TransAuto(Sqlen, '@L38', FloatToStr(SpinEdit338.Value));
    TransAuto(Sqlon, '@L39', FloatToStr(SpinEdit339.Value));
    TransAuto(Sqlon, '@L41', FloatToStr(SpinEdit341.Value));
    TransAuto(Sqlon, '@L42', FloatToStr(SpinEdit342.Value));
    TransAuto(Sqlon, '@L43', FloatToStr(SpinEdit343.Value));
    TransAuto(Sqlon, '@L44', FloatToStr(SpinEdit344.Value));
    TransAuto(Sqlon, '@L45', FloatToStr(SpinEdit345.Value));
    TransAuto(Sqlon, '@L46', FloatToStr(SpinEdit346.Value));
    TransAuto(Sqlon, '@L47', FloatToStr(SpinEdit347.Value));
    TransAuto(Sqlon, '@L48', FloatToStr(SpinEdit348.Value));
    TransAuto(Sqlon, '@L49', FloatToStr(SpinEdit349.Value));
    TransAuto(Sqlon, '@L51', FloatToStr(SpinEdit351.Value));
    TransAuto(Sqlon, '@L52', FloatToStr(SpinEdit352.Value));
    TransAuto(Sqlon, '@L53', FloatToStr(SpinEdit353.Value));
    TransAuto(Sqlon, '@L54', FloatToStr(SpinEdit354.Value));
    TransAuto(Sqlon, '@L55', FloatToStr(SpinEdit355.Value));
    TransAuto(Sqlon, '@L56', FloatToStr(SpinEdit356.Value));
    TransAuto(Sqlon, '@L57', FloatToStr(SpinEdit357.Value));
    TransAuto(Sqlon, '@L58', FloatToStr(SpinEdit358.Value));
    TransAuto(Sqlon, '@L59', FloatToStr(SpinEdit359.Value));
    TransAuto(Sqlon, '@L61', FloatToStr(SpinEdit301.Value));
    TransAuto(Sqlon, '@L62', FloatToStr(SpinEdit302.Value));
    TransAuto(Sqlon, '@L63', FloatToStr(SpinEdit303.Value));
    TransAuto(Sqlon, '@L64', FloatToStr(SpinEdit304.Value));
    Translate(Sqlon, '@Gu',  '9');

    Sqlen:=Sqlen+Sqlon;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.BusyLoop;
    if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

end;

procedure TSeak60.Button100Click(Sender: TObject);
begin

  wSqry:=Base10.T1_Sub92;
  Base10.OpenData(wSqry);

  Sqlen := 'Select * From Gg_Magn Where Gu'+'>='+#39+'1'+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.ClientGrid(wSqry)
  else ShowMessage(E_Open);

  wSqry.SaveToFile(GetExecPath + 'Data\Magin.cds');
  Base10.OpenExit(Base10.T1_Sub92);
  
end;

end.
