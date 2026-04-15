unit Seak02;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Grids, DBGrids, Db, DBClient, Buttons, TFlatEditUnit,
  TFlatPanelUnit, TFlatSpeedButtonUnit, TFlatButtonUnit, TFlatComboBoxUnit,
  TFlatGroupBoxUnit;

type
  TSeak20 = class(TForm)
    Panel100: TFlatPanel;
    FlatGroupBox1: TFlatGroupBox;
    FlatGroupBox2: TFlatGroupBox;
    FlatGroupBox3: TFlatGroupBox;
    FlatGroupBox4: TFlatGroupBox;
    ComboBox01: TFlatComboBox;
    ComboBox02: TFlatComboBox;
    ComboBox03: TFlatComboBox;
    ComboBox04: TFlatComboBox;
    ComboBox11: TFlatComboBox;
    ComboBox12: TFlatComboBox;
    ComboBox13: TFlatComboBox;
    ComboBox14: TFlatComboBox;
    ComboBox21: TFlatComboBox;
    ComboBox22: TFlatComboBox;
    ComboBox23: TFlatComboBox;
    ComboBox24: TFlatComboBox;
    ComboBox31: TFlatComboBox;
    ComboBox32: TFlatComboBox;
    ComboBox33: TFlatComboBox;
    ComboBox34: TFlatComboBox;
    Edit21: TFlatEdit;
    Edit22: TFlatEdit;
    Edit23: TFlatEdit;
    Edit24: TFlatEdit;
    SpeedButton21: TFlatSpeedButton;
    SpeedButton22: TFlatSpeedButton;
    SpeedButton23: TFlatSpeedButton;
    SpeedButton24: TFlatSpeedButton;
    Label31: TLabel;
    Label32: TLabel;
    Label33: TLabel;
    Label34: TLabel;
    Button101: TFlatButton;
    Button102: TFlatButton;
    BitBtn101: TBitBtn;
    BitBtn102: TBitBtn;
    DBGrid1: TDBGrid;
    G0_GbunD: TDataSource;
    RadioButton11: TRadioButton;
    RadioButton12: TRadioButton;
    RadioButton13: TRadioButton;
    RadioButton14: TRadioButton;
    RadioButton15: TRadioButton;
    RadioButton16: TRadioButton;
    G0_GbunQ: TClientDataSet;
    G0_GbunQID: TFloatField;
    G0_GbunQGCODE: TStringField;
    G0_GbunQGNAME: TStringField;
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure SetSeek01(Str1,Str2:String);
    procedure SetSeek02(Str1,Str2:String);
    procedure SetSeek03(Str1,Str2:String);
    procedure SetSeek04(Str1,Str2:String);
    procedure Edit21Change(Sender: TObject);
    procedure Edit22Change(Sender: TObject);
    procedure Edit23Change(Sender: TObject);
    procedure Edit24Change(Sender: TObject);
    procedure ComboBox11Change(Sender: TObject);
    procedure ComboBox12Change(Sender: TObject);
    procedure ComboBox13Change(Sender: TObject);
    procedure ComboBox14Change(Sender: TObject);
    procedure ComboBox21Change(Sender: TObject);
    procedure ComboBox22Change(Sender: TObject);
    procedure ComboBox23Change(Sender: TObject);
    procedure ComboBox24Change(Sender: TObject);
    procedure SpeedButton21Click(Sender: TObject);
    procedure SpeedButton22Click(Sender: TObject);
    procedure SpeedButton23Click(Sender: TObject);
    procedure SpeedButton24Click(Sender: TObject);
    procedure Edit21KeyPress(Sender: TObject; var Key: Char);
    procedure Edit22KeyPress(Sender: TObject; var Key: Char);
    procedure Edit23KeyPress(Sender: TObject; var Key: Char);
    procedure Edit24KeyPress(Sender: TObject; var Key: Char);
    procedure BitBtn101Click(Sender: TObject);
    procedure BitBtn102Click(Sender: TObject);
    procedure DBGrid1DblClick(Sender: TObject);
    procedure DBGrid1Exit(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Seak20: TSeak20;
  Sos01,Sos02,Sos03: String;
  Sot01,Sot02,Sot03,Sot04: String;

implementation

{$R *.DFM}

uses Base01;

procedure TSeak20.FormShow(Sender: TObject);
var St0,St1:Integer;
    St8:array [0..41] of String;
    St9:array [0..41] of String;
begin
  if nForm='11' Then begin
     St8[00]:='Gubun'; St9[00]:='거래처구분';
     St8[01]:='Jubun'; St9[01]:='거래처지역';
     St8[02]:='Gcode'; St9[02]:='거래처코드';
     St8[03]:='Gname'; St9[03]:='거래처명';
     St8[04]:='Gposa'; St9[04]:='대표자명';
     St8[05]:='Gnumb'; St9[05]:='사업자번호';
     St8[06]:='Guper'; St9[06]:='업    태';
     St8[07]:='Gjomo'; St9[07]:='종    목';
     St8[08]:='Gtel2'; St9[08]:='전화번호';
     St8[09]:='Gfax2'; St9[09]:='팩스번호';
     St8[10]:='Gpost'; St9[10]:='우편번호';
     St8[11]:='Gadd1'; St9[11]:='주    소';
     St8[12]:='Gbigo'; St9[12]:='비    고';
     St1:=13;
  end;
  if nForm='12' Then begin
     St8[00]:='Gubun'; St9[00]:='입고처구분';
     St8[01]:='Jubun'; St9[01]:='입고처지역';
     St8[02]:='Gcode'; St9[02]:='입고처코드';
     St8[03]:='Gname'; St9[03]:='입고처명';
     St8[04]:='Gposa'; St9[04]:='대표자명';
     St8[05]:='Gnumb'; St9[05]:='사업자번호';
     St8[06]:='Guper'; St9[06]:='업    태';
     St8[07]:='Gjomo'; St9[07]:='종    목';
     St8[08]:='Gtel2'; St9[08]:='전화번호';
     St8[09]:='Gfax2'; St9[09]:='팩스번호';
     St8[10]:='Gpost'; St9[10]:='우편번호';
     St8[11]:='Gadd1'; St9[11]:='주    소';
     St8[12]:='Gbigo'; St9[12]:='비    고';
     St1:=13;
  end;
  if nForm='13' Then begin
     St8[00]:='Gubun'; St9[00]:='저자구분';
     St8[01]:='Data1'; St9[01]:='등록일자';
     St8[02]:='Gcode'; St9[02]:='저자코드';
     St8[03]:='Gposa'; St9[03]:='저 자 명';
     St8[04]:='Gname'; St9[04]:='직 장 명';
     St8[05]:='Gjice'; St9[05]:='직    책';
     St8[06]:='Gscho'; St9[06]:='출신학교';
     St8[07]:='Gnumb'; St9[07]:='사업자번호';
     St8[08]:='Gnum1'; St9[08]:='주민등록';
     St8[09]:='Gnum2'; St9[09]:='계좌번호';
     St8[10]:='Gtel2'; St9[10]:='전화번호';
     St8[11]:='Gfax2'; St9[11]:='팩스번호';
     St8[12]:='Gbigo'; St9[12]:='비    고';
     St1:=13;
  end;
  if nForm='14' Then begin
     St8[00]:='Gubun'; St9[00]:='도서분류';
     St8[01]:='Jubun'; St9[01]:='도서처리';
     St8[02]:='Gcode'; St9[02]:='도서코드';
     St8[03]:='Gname'; St9[03]:='도 서 명';
     St8[04]:='Gjeja'; St9[04]:='저 자 명';
     St8[05]:='Gdabi'; St9[05]:='단    위';
     St8[06]:='Gdang'; St9[06]:='단    가';
     St8[07]:='Gisbn'; St9[07]:='ISBN번호';
     St8[08]:='Gbjil'; St9[08]:='도 서 질';
     St8[09]:='Grat8'; St9[09]:='셋    트';
     St8[10]:='Gbigo'; St9[10]:='비    고';
     St1:=11;
  end;
  if nForm='15' Then begin
     St8[00]:='Gubun'; St9[00]:='구    분';
     St8[01]:='Jubun'; St9[01]:='거래처지역';
     St8[02]:='Gcode'; St9[02]:='거래처코드';
     St8[03]:='Gname'; St9[03]:='거래처명';
     St8[04]:='Gposa'; St9[04]:='대표자명';
     St8[05]:='Gnumb'; St9[05]:='사업자번호';
     St8[06]:='Guper'; St9[06]:='업    태';
     St8[07]:='Gjomo'; St9[07]:='종    목';
     St8[08]:='Gtel2'; St9[08]:='전화번호';
     St8[09]:='Gfax2'; St9[09]:='팩스번호';
     St8[10]:='Gpost'; St9[10]:='우편번호';
     St8[11]:='Gadd1'; St9[11]:='주    소';
     St8[12]:='Gbigo'; St9[12]:='비    고';
     St1:=13;
  end;
  if nForm='17' Then begin
     St8[00]:='Gubun'; St9[00]:='출판사구분';
     St8[01]:='Jubun'; St9[01]:='출판사지역';
     St8[02]:='Gcode'; St9[02]:='출판사코드';
     St8[03]:='Gname'; St9[03]:='출판사명';
     St8[04]:='Gposa'; St9[04]:='대표자명';
     St8[05]:='Gnumb'; St9[05]:='사업자번호';
     St8[06]:='Guper'; St9[06]:='업    태';
     St8[07]:='Gjomo'; St9[07]:='종    목';
     St8[08]:='Gtel2'; St9[08]:='전화번호';
     St8[09]:='Gfax2'; St9[09]:='팩스번호';
     St8[10]:='Gpost'; St9[10]:='우편번호';
     St8[11]:='Gadd1'; St9[11]:='주    소';
     St8[12]:='Gbigo'; St9[12]:='비    고';
     St1:=13;
  end;
  if nForm='24' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='Giqut'; St9[02]:='입고수량';
     St8[03]:='Goqut'; St9[03]:='출고수량';
     St8[04]:='Gjqut'; St9[04]:='증정수량';
     St8[05]:='Gbqut'; St9[05]:='반품수량';
     St8[06]:='Gsusu'; St9[06]:='폐기수량';
     St8[07]:='Gosum'; St9[07]:='출고금액';
     St8[08]:='Gbsum'; St9[08]:='반품금액';
     St1:=8;
  end;
  if nForm='25' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='입고처명';
     St8[02]:='Giqut'; St9[02]:='출고수량';
     St8[03]:='Goqut'; St9[03]:='출고금액';
     St8[04]:='Gjqut'; St9[04]:='증정수량';
     St8[05]:='Gbqut'; St9[05]:='반품수량';
     St8[06]:='Gsusu'; St9[06]:='반품금액';
     St8[07]:='Gosum'; St9[07]:='수 금 액';
     St8[08]:='Gbsum'; St9[08]:='판매금액';
     St1:=8;
  end;
  if nForm='26' Then begin
     St8[00]:='Gcode'; St9[00]:='거래일자';
     St8[01]:='Gname'; St9[01]:='코    드';
     St8[02]:='Giqut'; St9[02]:='거래처명';
     St8[03]:='Goqut'; St9[03]:='계정코드';
     St8[04]:='Gjqut'; St9[04]:='계정과목';
     St8[05]:='Gbqut'; St9[05]:='금    액';
     St8[06]:='Gsusu'; St9[06]:='비    고';
     St1:=6;
  end;
  if nForm='27' Then begin
     St8[00]:='Gcode'; St9[00]:='거래일자';
     St8[01]:='Gname'; St9[01]:='코    드';
     St8[02]:='Giqut'; St9[02]:='거래처명';
     St8[03]:='Goqut'; St9[03]:='계정코드';
     St8[04]:='Gjqut'; St9[04]:='계정과목';
     St8[05]:='Gbqut'; St9[05]:='금    액';
     St8[06]:='Gsusu'; St9[06]:='비    고';
     St1:=6;
  end;
  if nForm='28' Then begin
     St8[00]:='Gdate'; St9[00]:='거래일자';
     St8[01]:='Gcode'; St9[01]:='저자코드';
     St8[02]:='Gssum'; St9[02]:='지 급 액';
     St8[03]:='Gisum'; St9[03]:='소 득 세';
     St8[04]:='Gosum'; St9[04]:='주 민 세';
     St8[05]:='Gbsum'; St9[05]:='합    계';
     St8[06]:='Bcode'; St9[06]:='적    요';
     St1:=6;
  end;
  if nForm='32_1' Then begin
     St8[00]:='Gcode'; St9[00]:='코드';
     St8[01]:='Gname'; St9[01]:='출판사명';
     St8[02]:='GsumY'; St9[02]:='정품재고';
     St8[03]:='Gssum'; St9[03]:='비품재고';
     St1:=4;
  end;
  if nForm='33' Then begin
     St8[00]:='Gcode'; St9[00]:='도서코드';
     St8[01]:='Gname'; St9[01]:='도 서 명';
     St8[02]:='GsumX'; St9[02]:='전일재고';
     St8[03]:='Giqut'; St9[03]:='입고수량';
     St8[04]:='Gisum'; St9[04]:='재 입 고';
     St8[05]:='Goqut'; St9[05]:='출고수량';
     St8[06]:='Gjqut'; St9[06]:='증정수량';
     St8[07]:='Gbqut'; St9[07]:='반품수량';
     St8[08]:='Gpqut'; St9[08]:='폐기수량';
     St8[09]:='Gsqut'; St9[09]:='변경수량';
     St8[10]:='GsumY'; St9[10]:='현재재고';
     St8[11]:='Gssum'; St9[11]:='현재고(반)';
     St1:=11;
  end;
  if nForm='34' Then begin
     St8[00]:='Gcode'; St9[00]:='도서코드';
     St8[01]:='Gname'; St9[01]:='도 서 명';
     St8[02]:='GsumX'; St9[02]:='전일재고';
     St8[03]:='Giqut'; St9[03]:='입고수량';
     St8[04]:='Goqut'; St9[04]:='출고수량';
     St8[05]:='Gjqut'; St9[05]:='증정수량';
     St8[06]:='Gbqut'; St9[06]:='반품수량';
     St8[07]:='Gpqut'; St9[07]:='폐기수량';
     St8[08]:='GsumY'; St9[08]:='현재재고';
     St1:=8;
  end;
  if nForm='35' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='Goqut'; St9[02]:='출고수량';
     St8[03]:='Gosum'; St9[03]:='출고금액';
     St8[04]:='Gbqut'; St9[04]:='반품수량';
     St8[05]:='Gbsum'; St9[05]:='반품금액';
     St8[06]:='Gjqut'; St9[06]:='증정수량';
     St8[07]:='Gsusu'; St9[07]:='수 금 액';
     St8[08]:='GsumY'; St9[08]:='미 수 금';
     St1:=8;
  end;
  if nForm='36' Then begin
     St8[00]:='Gcode'; St9[00]:='도서코드';
     St8[01]:='Gname'; St9[01]:='도 서 명';
     St8[02]:='Giqut'; St9[02]:='입고수량';
     St8[03]:='Goqut'; St9[03]:='출고수량';
     St8[04]:='Gjqut'; St9[04]:='증정수량';
     St8[05]:='Gbqut'; St9[05]:='반품수량';
     St8[06]:='Gpqut'; St9[06]:='폐기수량';
     St8[07]:='GsumX'; St9[07]:='판매금액';
     St8[08]:='GsumY'; St9[08]:='현재재고';
     St1:=8;
  end;
  if nForm='37' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='GsumX'; St9[02]:='전일미수';
     St8[03]:='Gosum'; St9[03]:='신간금액';
     St8[04]:='Gjqut'; St9[04]:='주문수량';
     St8[05]:='Gjsum'; St9[05]:='주문금액';
     St8[06]:='Gbsum'; St9[06]:='반품금액';
     St8[07]:='Gsusu'; St9[07]:='수 금 액';
     St8[08]:='GsumY'; St9[08]:='미 수 금';
     St1:=8;
  end;
  if nForm='46' Then begin
     St8[00]:='Gnumb'; St9[00]:='어음번호';
     St8[01]:='Scode'; St9[01]:='처리코드';
     St8[02]:='Gname'; St9[02]:='발 행 처';
     St8[03]:='Gposa'; St9[03]:='발 행 인';
     St8[04]:='Date1'; St9[04]:='발행일자';
     St8[05]:='Date2'; St9[05]:='받은일자';
     St8[06]:='Date3'; St9[06]:='지급일자';
     St8[07]:='Name1'; St9[07]:='지 급 처';
     St8[08]:='Gbang'; St9[08]:='지급은행';
     St8[09]:='Name2'; St9[09]:='지급지점';
     St8[10]:='Date4'; St9[10]:='만기일자';
     St8[11]:='Gssum'; St9[11]:='금    액';
     St8[12]:='Grat1'; St9[12]:='할 인 율';
     St8[13]:='Gosum'; St9[13]:='할인금액';
     St8[14]:='Gbigo'; St9[14]:='비    고';
     St1:=14;
  end;
  if nForm='49' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='Goqut'; St9[02]:='출고수량';
     St8[03]:='Gosum'; St9[03]:='출고금액';
     St8[04]:='Gbqut'; St9[04]:='반품수량';
     St8[05]:='Gbsum'; St9[05]:='반품금액';
     St8[06]:='Gsusu'; St9[06]:='수 금 액';
     St8[07]:='Gssum'; St9[07]:='판매금액';
     St1:=7;
  end;
  if nForm='51' Then begin
     St8[00]:='Gdate'; St9[00]:='거래일자';
     St8[01]:='Gcode'; St9[01]:='코    드';
     St8[02]:='Gssum'; St9[02]:='대조금액';
     St8[03]:='Gosum'; St9[03]:='원장금액';
     St8[04]:='Gbsum'; St9[04]:='장부차액';
     St8[05]:='Gbigo'; St9[05]:='비    고';
     St1:=5;
  end;
  if nForm='52' Then begin
     St8[00]:='Gdate'; St9[00]:='거래일자';
     St8[01]:='Gcode'; St9[01]:='도서코드';
     St8[02]:='Gssum'; St9[02]:='대조재고';
     St8[03]:='Gosum'; St9[03]:='원장재고';
     St8[04]:='Gbsum'; St9[04]:='변경수량';
     St8[05]:='Gbigo'; St9[05]:='비    고';
     St1:=5;
  end;
  if nForm='53' Then begin
     St8[00]:='Gdate'; St9[00]:='초기일자';
     St8[01]:='Gcode'; St9[01]:='코    드';
     St8[02]:='Gssum'; St9[02]:='금    액';
     St1:=2;
  end;
  if nForm='54' Then begin
     St8[00]:='Gdate'; St9[00]:='초기일자';
     St8[01]:='Gcode'; St9[01]:='도서코드';
     St8[02]:='Gssum'; St9[02]:='재    고';
     St1:=2;
  end;
  if nForm='56' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='Bcode'; St9[02]:='도서코드';
     St8[03]:='Bname'; St9[03]:='도 서 명';
     St1:=4;
  end;
  if nForm='57' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='입고처명';
     St8[02]:='Bcode'; St9[02]:='도서코드';
     St8[03]:='Bname'; St9[03]:='도 서 명';
     St1:=4;
  end;
  if nForm='58' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='Bcode'; St9[02]:='도서코드';
     St8[03]:='Bname'; St9[03]:='도 서 명';
     St1:=4;
  end;
  if nForm='58_1' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='Bcode'; St9[02]:='도서코드';
     St8[03]:='Bname'; St9[03]:='도 서 명';
     St1:=4;
  end;
  if nForm='59' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='Bcode'; St9[02]:='도서코드';
     St8[03]:='Bname'; St9[03]:='도 서 명';
     St1:=4;
  end;
  if nForm='61' Then begin
     St8[00]:='Gcode'; St9[00]:='도서코드';
     St8[01]:='Gname'; St9[01]:='도 서 명';
     St8[02]:='Giqut'; St9[02]:='입고수량';
     St8[03]:='Goqut'; St9[03]:='출고수량';
     St8[04]:='Gjqut'; St9[04]:='증정수량';
     St8[05]:='Gbqut'; St9[05]:='반품수량';
     St8[06]:='Gpqut'; St9[06]:='폐기수량';
     St8[07]:='Gosum'; St9[07]:='출고금액';
     St8[08]:='Gbsum'; St9[08]:='반품금액';
     St1:=8;
  end;
  if nForm='62' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='Goqut'; St9[02]:='출고수량';
     St8[03]:='Gosum'; St9[03]:='출고금액';
     St8[04]:='Gjqut'; St9[04]:='증정수량';
     St8[05]:='Gbqut'; St9[05]:='반품수량';
     St8[06]:='Gbsum'; St9[06]:='반품금액';
     St8[07]:='Gsusu'; St9[07]:='수 금 액';
     St8[08]:='Gssum'; St9[08]:='판매금액';
     St1:=8;
  end;
  if nForm='63' Then begin
     St8[00]:='Gcode'; St9[00]:='도서코드';
     St8[01]:='Gname'; St9[01]:='도 서 명';
     St8[02]:='Goqut'; St9[02]:='신    간';
     St8[03]:='Gosum'; St9[03]:='위    탁';
     St8[04]:='Gbqut'; St9[04]:='현    매';
     St8[05]:='Gbsum'; St9[05]:='매    절';
     St8[06]:='Gjqut'; St9[06]:='증    정';
     St8[07]:='GsumX'; St9[07]:='납    품';
     St8[08]:='GsumY'; St9[08]:='특    별';
     St1:=8;
  end;
  if nForm='64' Then begin
     St8[00]:='Gcode'; St9[00]:='도서코드';
     St8[01]:='Gname'; St9[01]:='도 서 명';
     St8[02]:='Goqut'; St9[02]:='신    간';
     St8[03]:='Gosum'; St9[03]:='위    탁';
     St8[04]:='Gbqut'; St9[04]:='현    매';
     St8[05]:='Gbsum'; St9[05]:='매    절';
     St8[06]:='Gjqut'; St9[06]:='증    정';
     St8[07]:='GsumX'; St9[07]:='납    품';
     St8[08]:='GsumY'; St9[08]:='특    별';
     St1:=8;
  end;
  if nForm='65' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St1:=1;
  end;
  if nForm='66' Then begin
     St8[00]:='Gcode'; St9[00]:='도서코드';
     St8[01]:='Gname'; St9[01]:='도 서 명';
     St1:=1;
  end;
  if nForm='67' Then begin
     St8[00]:='Gcode'; St9[00]:='도서코드';
     St8[01]:='Gname'; St9[01]:='도 서 명';
     St8[02]:='Giqut'; St9[02]:='입고수량';
     St8[03]:='Goqut'; St9[03]:='출고수량';
     St8[04]:='Gjqut'; St9[04]:='증정수량';
     St8[05]:='Gbqut'; St9[05]:='반품수량';
     St8[06]:='Gsusu'; St9[06]:='폐기수량';
     St8[07]:='Gosum'; St9[07]:='출고금액';
     St8[08]:='Gbsum'; St9[08]:='반품금액';
     St1:=8;
  end;
  if nForm='68' Then begin
     St8[00]:='Gcode'; St9[00]:='코    드';
     St8[01]:='Gname'; St9[01]:='거래처명';
     St8[02]:='Goqut'; St9[02]:='출고수량';
     St8[03]:='Gosum'; St9[03]:='출고금액';
     St8[04]:='Gjqut'; St9[04]:='증정수량';
     St8[05]:='Gbqut'; St9[05]:='반품수량';
     St8[06]:='Gbsum'; St9[06]:='반품금액';
     St8[07]:='Gsusu'; St9[07]:='수 금 액';
     St8[08]:='Gssum'; St9[08]:='판매금액';
     St1:=8;
  end;
  for St0:=0 to St1 do begin
  Seak20.ComboBox01.Items.Add(St8[St0]);
  Seak20.ComboBox02.Items.Add(St8[St0]);
  Seak20.ComboBox03.Items.Add(St8[St0]);
  Seak20.ComboBox04.Items.Add(St8[St0]);
  Seak20.ComboBox11.Items.Add(St9[St0]);
  Seak20.ComboBox12.Items.Add(St9[St0]);
  Seak20.ComboBox13.Items.Add(St9[St0]);
  Seak20.ComboBox14.Items.Add(St9[St0]);
  end;
  if ComboBox31.ItemIndex = -1 Then ComboBox31.ItemIndex:=0;
  if ComboBox32.ItemIndex = -1 Then ComboBox32.ItemIndex:=0;
  if ComboBox33.ItemIndex = -1 Then ComboBox33.ItemIndex:=0;
  if ComboBox34.ItemIndex = -1 Then ComboBox34.ItemIndex:=0;
end;

procedure TSeak20.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  ComboBox01.Items.Clear; ComboBox11.Items.Clear; Edit21.Text:='';
  ComboBox02.Items.Clear; ComboBox12.Items.Clear; Edit22.Text:='';
  ComboBox03.Items.Clear; ComboBox13.Items.Clear; Edit23.Text:='';
  ComboBox04.Items.Clear; ComboBox14.Items.Clear; Edit24.Text:='';
end;

procedure TSeak20.SetSeek01(Str1,Str2:String);
var St1,St2: String;
begin
  if (Str1='거래처구분') Then begin Sos02:='0';
    if Str2='' Then
    St1:='Gname'+'>'+#39+Str2+#39 else
    St1:='Gname'+'='+#39+Str2+#39;
    St2:=' Order By Gcode';

    Base10.OpenExit(G0_GbunQ);
    Base10.OpenShow(G0_GbunQ);

    Sqlen := 'Select ID, Gcode, Gname From G1_Gbun Where '+D_Select+St1+St2;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(G0_GbunQ)
    else ShowMessage(E_Open);

    DBGrid1.Columns[0].Width:=40;
    DBGrid1.Columns[1].Width:=145;
    DBGrid1.Visible:=True; DBGrid1.SetFocus;
  end else
  if (Str1='입고처구분') Then begin Sos02:='1';
    if Str2='' Then
    St1:='Gname'+'>'+#39+Str2+#39 else
    St1:='Gname'+'='+#39+Str2+#39;
    St2:=' Order By Gcode';

    Sqlen := 'Select ID, Gcode, Gname From G2_Gbun Where '+D_Select+St1+St2;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(G0_GbunQ)
    else ShowMessage(E_Open);

    DBGrid1.Columns[0].Width:=40;
    DBGrid1.Columns[1].Width:=145;
    DBGrid1.Visible:=True; DBGrid1.SetFocus;
  end else
  if (Str1='저자구분') Then begin Sos02:='2';
    if Str2='' Then
    St1:='Gname'+'>'+#39+Str2+#39 else
    St1:='Gname'+'='+#39+Str2+#39;
    St2:=' Order By Gcode';

    Sqlen := 'Select ID, Gcode, Gname From G3_Gbun Where '+D_Select+St1+St2;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(G0_GbunQ)
    else ShowMessage(E_Open);

    DBGrid1.Columns[0].Width:=40;
    DBGrid1.Columns[1].Width:=145;
    DBGrid1.Visible:=True; DBGrid1.SetFocus;
  end else
  if (Str1='도서분류') Then begin Sos02:='3';
    if Str2='' Then
    St1:='Gname'+'>'+#39+Str2+#39 else
    St1:='Gname'+'='+#39+Str2+#39;
    St2:=' Order By Gcode';

    Sqlen := 'Select ID, Gcode, Gname From G4_Gbun Where '+D_Select+St1+St2;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(G0_GbunQ)
    else ShowMessage(E_Open);

    DBGrid1.Columns[0].Width:=40;
    DBGrid1.Columns[1].Width:=145;
    DBGrid1.Visible:=True; DBGrid1.SetFocus;
  end else
  if (Str1='구    분') Then begin Sos02:='4';
    if Str2='' Then
    St1:='Gname'+'>'+#39+Str2+#39 else
    St1:='Gname'+'='+#39+Str2+#39;
    St2:=' Order By Gcode';

    Sqlen := 'Select ID, Gcode, Gname From G5_Gbun Where '+D_Select+St1+St2;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(G0_GbunQ)
    else ShowMessage(E_Open);

    DBGrid1.Columns[0].Width:=40;
    DBGrid1.Columns[1].Width:=145;
    DBGrid1.Visible:=True; DBGrid1.SetFocus;
  end;
  if (Str1='출판사구분') Then begin Sos02:='4';
    if Str2='' Then
    St1:='Gname'+'>'+#39+Str2+#39 else
    St1:='Gname'+'='+#39+Str2+#39;
    St2:=' Order By Gcode';

    Sqlen := 'Select ID, Gcode, Gname From G7_Gbun Where '+D_Select+St1+St2;
    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.body_data <> 'ERROR' then
       Base10.Socket.ClientGrid(G0_GbunQ)
    else ShowMessage(E_Open);

    DBGrid1.Columns[0].Width:=40;
    DBGrid1.Columns[1].Width:=145;
    DBGrid1.Visible:=True; DBGrid1.SetFocus;
  end;
end;

procedure TSeak20.SetSeek02(Str1,Str2:String);
var St0:Integer;
    St9:array [0..15] of String;
begin
  if Str1='지역01' Then begin
    St9[00]:='서울'; St9[01]:='부산'; St9[02]:='대구';
    St9[03]:='인천'; St9[04]:='광주'; St9[05]:='대전';
    St9[06]:='울산'; St9[07]:='경기'; St9[08]:='강원';
    St9[09]:='충북'; St9[10]:='충남'; St9[11]:='전북';
    St9[12]:='전남'; St9[13]:='경북'; St9[14]:='경남'; St9[15]:='제주';
  end else
  if Str1='지역02' Then begin
    St9[00]:='서울'; St9[01]:='부산'; St9[02]:='대구';
    St9[03]:='인천'; St9[04]:='광주'; St9[05]:='대전';
    St9[06]:='울산'; St9[07]:='경기'; St9[08]:='강원';
    St9[09]:='충북'; St9[10]:='충남'; St9[11]:='전북';
    St9[12]:='전남'; St9[13]:='경북'; St9[14]:='경남'; St9[15]:='제주';
  end else
  if Str1='지역03' Then begin
    St9[00]:='서울'; St9[01]:='부산'; St9[02]:='대구';
    St9[03]:='인천'; St9[04]:='광주'; St9[05]:='대전';
    St9[06]:='울산'; St9[07]:='경기'; St9[08]:='강원';
    St9[09]:='충북'; St9[10]:='충남'; St9[11]:='전북';
    St9[12]:='전남'; St9[13]:='경북'; St9[14]:='경남'; St9[15]:='제주';
  end;
  if Str2='1' Then
    ComboBox21.Items.Clear; for St0:=0 to 15 do
    begin ComboBox21.Items.Add(St9[St0]); end;
  if Str2='2' Then
    ComboBox22.Items.Clear; for St0:=0 to 15 do
    begin ComboBox22.Items.Add(St9[St0]); end;
  if Str2='3' Then
    ComboBox23.Items.Clear; for St0:=0 to 15 do
    begin ComboBox23.Items.Add(St9[St0]); end;
  if Str2='4' Then
    ComboBox24.Items.Clear; for St0:=0 to 15 do
    begin ComboBox24.Items.Add(St9[St0]); end;
end;

procedure TSeak20.SetSeek03(Str1,Str2:String);
var St0:String;
begin
  St0:='1'; Sos03:='1';
  if Str1='거래처구분' Then St0:='2';
  if Str1='입고처구분' Then St0:='2';
  if Str1='저자구분'   Then St0:='2';
  if Str1='도서분류'   Then St0:='2';
  if Str1='구    분'   Then St0:='2';
  if Str1='출판사구분' Then St0:='2';
  if Str1='거래처지역' Then St0:='3';
  if Str1='입고처지역' Then St0:='3';
  if Str1='출판사지역' Then St0:='3';
  if Str1='입고수량'   Then St0:='4';
  if Str1='입고금액'   Then St0:='4';
  if Str1='출고수량'   Then St0:='4';
  if Str1='출고금액'   Then St0:='4';
  if Str1='증정수량'   Then St0:='4';
  if Str1='증정금액'   Then St0:='4';
  if Str1='주문수량'   Then St0:='4';
  if Str1='주문금액'   Then St0:='4';
  if Str1='반품수량'   Then St0:='4';
  if Str1='반품금액'   Then St0:='4';
  if Str1='폐기수량'   Then St0:='4';
  if Str1='폐기금액'   Then St0:='4';
  if Str1='판매수량'   Then St0:='4';
  if Str1='판매금액'   Then St0:='4';
  if Str1='전일재고'   Then St0:='4';
  if Str1='현재재고'   Then St0:='4';
  if Str1='전일미수'   Then St0:='4';
  if Str1='미 수 금'   Then St0:='4';
  if Str1='신간금액'   Then St0:='4';
  if Str1='대조금액'   Then St0:='4';
  if Str1='원장금액'   Then St0:='4';
  if Str1='장부차액'   Then St0:='4';
  if Str1='대조재고'   Then St0:='4';
  if Str1='원장재고'   Then St0:='4';
  if Str1='변경수량'   Then St0:='4';
  if Str1='지 급 액'   Then St0:='4';
  if Str1='소 득 세'   Then St0:='4';
  if Str1='주 민 세'   Then St0:='4';
  if Str1='합    계'   Then St0:='4';
  if Str1='전월배본'   Then St0:='4';
  if Str1='판매부수'   Then St0:='4';
  if Str1='점유부수'   Then St0:='4';
  if Str1='전호배본'   Then St0:='4';
  if Str1='당호확정'   Then St0:='4';
  if Str1='조    정'   Then St0:='4';
  if Str1='금    액'   Then St0:='4';
  if Str1='재    고'   Then St0:='4';
  if Str1='수 금 액'   Then St0:='4';
  if Str1='액 면 가'   Then St0:='4';
  if Str1='단    가'   Then St0:='4';
  if Str1='신    간'   Then St0:='4';
  if Str1='위    탁'   Then St0:='4';
  if Str1='현    매'   Then St0:='4';
  if Str1='매    절'   Then St0:='4';
  if Str1='증    정'   Then St0:='4';
  if Str1='납    품'   Then St0:='4';
  if Str1='특    별'   Then St0:='4';
  if Str1='셋    트'   Then St0:='4';
  if Str1='재 입 고'   Then St0:='4';
  if Str1='현재고(반)' Then St0:='4';
  if St0='2' Then Sos03:='2';
  if St0='4' Then Sos03:='4';
  if St0='0' Then begin
     if Str2='1' Then begin
     ComboBox31.ItemIndex:=0; ComboBox31.Enabled:=False; end;
     if Str2='2' Then begin
     ComboBox32.ItemIndex:=0; ComboBox32.Enabled:=False; end;
     if Str2='3' Then begin
     ComboBox33.ItemIndex:=0; ComboBox33.Enabled:=False; end;
     if Str2='4' Then begin
     ComboBox34.ItemIndex:=0; ComboBox34.Enabled:=False; end;
  end
  else begin
     if Str2='1' Then ComboBox31.Enabled:=True;
     if Str2='2' Then ComboBox32.Enabled:=True;
     if Str2='3' Then ComboBox33.Enabled:=True;
     if Str2='4' Then ComboBox34.Enabled:=True;
  end;
  if Str2='1' Then begin
    if (St0='1')or(St0='4') Then begin
    Edit21.Visible:=True;  ComboBox21.VisiBle:=False;
    SpeedButton21.Enabled:=False; end;
    if St0='2' Then begin
    Edit21.Visible:=True;  ComboBox21.VisiBle:=False;
    SpeedButton21.Enabled:=True;  end;
    if St0='3' Then begin
    Edit21.Visible:=False; ComboBox21.VisiBle:=True;
    SpeedButton21.Enabled:=False; end;
    if St0='4' Then Sot01:='1' else Sot01:='2';
  end;
  if Str2='2' Then begin
    if (St0='1')or(St0='4') Then begin
    Edit22.Visible:=True;  ComboBox22.VisiBle:=False;
    SpeedButton22.Enabled:=False; end;
    if St0='2' Then begin
    Edit22.Visible:=True;  ComboBox22.VisiBle:=False;
    SpeedButton22.Enabled:=True;  end;
    if St0='3' Then begin
    Edit22.Visible:=False; ComboBox22.VisiBle:=True;
    SpeedButton22.Enabled:=False; end;
    if St0='4' Then Sot02:='1' else Sot02:='2';
  end;
  if Str2='3' Then begin
    if (St0='1')or(St0='4') Then begin
    Edit23.Visible:=True;  ComboBox23.VisiBle:=False;
    SpeedButton23.Enabled:=False; end;
    if St0='2' Then begin
    Edit23.Visible:=True;  ComboBox23.VisiBle:=False;
    SpeedButton23.Enabled:=True;  end;
    if St0='3' Then begin
    Edit23.Visible:=False; ComboBox23.VisiBle:=True;
    SpeedButton23.Enabled:=False; end;
    if St0='4' Then Sot03:='1' else Sot03:='2';
  end;
  if Str2='4' Then begin
    if (St0='1')or(St0='4') Then begin
    Edit24.Visible:=True;  ComboBox24.VisiBle:=False;
    SpeedButton24.Enabled:=False; end;
    if St0='2' Then begin
    Edit24.Visible:=True;  ComboBox24.VisiBle:=False;
    SpeedButton24.Enabled:=True;  end;
    if St0='3' Then begin
    Edit24.Visible:=False; ComboBox24.VisiBle:=True;
    SpeedButton24.Enabled:=False; end;
    if St0='4' Then Sot04:='1' else Sot04:='2';
  end;
end;

procedure TSeak20.SetSeek04(Str1,Str2:String);
var Sos01,Sos02:String;
begin
  if Str1='0' Then begin
    Sos01:=G0_GbunQGcode.AsString;
    Sos02:=G0_GbunQGname.AsString; end;
  if Str1='1' Then begin
    Sos01:=G0_GbunQGcode.AsString;
    Sos02:=G0_GbunQGname.AsString; end;
  if Str1='2' Then begin
    Sos01:=G0_GbunQGcode.AsString;
    Sos02:=G0_GbunQGname.AsString; end;
  if Str1='3' Then begin
    Sos01:=G0_GbunQGcode.AsString;
    Sos02:=G0_GbunQGname.AsString; end;
  if Str1='4' Then begin
    Sos01:=G0_GbunQGcode.AsString;
    Sos02:=G0_GbunQGname.AsString; end;
  if Str1='5' Then begin
    Sos01:=G0_GbunQGcode.AsString;
    Sos02:=G0_GbunQGname.AsString; end;
  if Str2='1' Then begin
    Edit21.Text:=Sos02; ComboBox21.Text:=Sos01; end;
  if Str2='2' Then begin
    Edit22.Text:=Sos02; ComboBox22.Text:=Sos01; end;
  if Str2='3' Then begin
    Edit23.Text:=Sos02; ComboBox23.Text:=Sos01; end;
  if Str2='4' Then begin
    Edit24.Text:=Sos02; ComboBox24.Text:=Sos01; end;
end;

procedure TSeak20.Edit21Change(Sender: TObject);
var Strs:String; Numb:Integer;
begin
  if ComboBox11.Text='' Then begin
    ComboBox21.Text:=''; Edit21.Text:='';
  end;
  if Sos03='1' Then ComboBox21.Text:=Edit21.Text;
  if Sos03='4' Then begin
    Strs:=Edit21.Text; Numb:=StrToIntDef(Strs, 0);
    ComboBox21.Text:=IntToStr(Numb);
  end;
  ComboBox21.Text:=Edit21.Text;
end;

procedure TSeak20.Edit22Change(Sender: TObject);
var Strs:String; Numb:Integer;
begin
  if ComboBox12.Text='' Then begin
    ComboBox22.Text:=''; Edit22.Text:='';
  end;
  if Sos03='1' Then ComboBox22.Text:=Edit22.Text;
  if Sos03='4' Then begin
    Strs:=Edit22.Text; Numb:=StrToIntDef(Strs, 0);
    ComboBox22.Text:=IntToStr(Numb);
  end;
end;

procedure TSeak20.Edit23Change(Sender: TObject);
var Strs:String; Numb:Integer;
begin
  if ComboBox13.Text='' Then begin
    ComboBox23.Text:=''; Edit23.Text:='';
  end;
  if Sos03='1' Then ComboBox23.Text:=Edit23.Text;
  if Sos03='4' Then begin
    Strs:=Edit23.Text; Numb:=StrToIntDef(Strs, 0);
    ComboBox23.Text:=IntToStr(Numb);
  end;
end;

procedure TSeak20.Edit24Change(Sender: TObject);
var Strs:String; Numb:Integer;
begin
  if ComboBox14.Text='' Then begin
    ComboBox24.Text:=''; Edit24.Text:='';
  end;
  if Sos03='1' Then ComboBox24.Text:=Edit24.Text;
  if Sos03='4' Then begin
    Strs:=Edit24.Text; Numb:=StrToIntDef(Strs, 0);
    ComboBox24.Text:=IntToStr(Numb);
  end;
end;

procedure TSeak20.ComboBox11Change(Sender: TObject);
begin
  Edit21.Text:=''; ComboBox21.Text:='';
  SetSeek02(ComboBox11.Text,'1');
  SetSeek03(ComboBox11.Text,'1');
end;

procedure TSeak20.ComboBox12Change(Sender: TObject);
begin
  Edit22.Text:=''; ComboBox22.Text:='';
  if (Edit21.Text<>'') Then begin
    SetSeek02(ComboBox12.Text,'2');
    SetSeek03(ComboBox12.Text,'2');
    if (RadioButton11.Checked=False) and (RadioButton12.Checked=False) Then
    RadioButton11.Checked:=True; end
  else begin
    ComboBox12.ItemIndex:=-1;
  end;
end;

procedure TSeak20.ComboBox13Change(Sender: TObject);
begin
  Edit23.Text:=''; ComboBox23.Text:='';
  if (Edit22.Text<>'') Then begin
    SetSeek02(ComboBox13.Text,'3');
    SetSeek03(ComboBox13.Text,'3');
    if (RadioButton13.Checked=False) and (RadioButton14.Checked=False) Then
    RadioButton13.Checked:=True; end
  else begin
    ComboBox13.ItemIndex:=-1;
  end;
end;

procedure TSeak20.ComboBox14Change(Sender: TObject);
begin
  Edit24.Text:=''; ComboBox24.Text:='';
  if (Edit23.Text<>'') Then begin
    SetSeek02(ComboBox14.Text,'4');
    SetSeek03(ComboBox14.Text,'4');
    if (RadioButton15.Checked=False) and (RadioButton16.Checked=False) Then
    RadioButton15.Checked:=True; end
  else begin
    ComboBox14.ItemIndex:=-1;
  end;
end;

procedure TSeak20.ComboBox21Change(Sender: TObject);
begin
  if ComboBox11.Text='' Then ComboBox21.ItemIndex:=-1;
  Edit21.Text:=ComboBox21.Text;
end;

procedure TSeak20.ComboBox22Change(Sender: TObject);
begin
  if ComboBox12.Text='' Then ComboBox22.ItemIndex:=-1;
  Edit22.Text:=ComboBox22.Text;
end;

procedure TSeak20.ComboBox23Change(Sender: TObject);
begin
  if ComboBox13.Text='' Then ComboBox23.ItemIndex:=-1;
  Edit23.Text:=ComboBox23.Text;
end;

procedure TSeak20.ComboBox24Change(Sender: TObject);
begin
  if ComboBox14.Text='' Then ComboBox24.ItemIndex:=-1;
  Edit24.Text:=ComboBox24.Text;
end;

procedure TSeak20.SpeedButton21Click(Sender: TObject);
begin
  Sos01:='1'; SetSeek01(ComboBox11.Text,Edit21.Text);
end;

procedure TSeak20.SpeedButton22Click(Sender: TObject);
begin
  Sos01:='2'; SetSeek01(ComboBox12.Text,Edit22.Text);
end;

procedure TSeak20.SpeedButton23Click(Sender: TObject);
begin
  Sos01:='3'; SetSeek01(ComboBox13.Text,Edit23.Text);
end;

procedure TSeak20.SpeedButton24Click(Sender: TObject);
begin
  Sos01:='4'; SetSeek01(ComboBox14.Text,Edit24.Text);
end;

procedure TSeak20.Edit21KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  if SpeedButton21.Enabled=True Then begin
  Sos01:='1'; SetSeek01(ComboBox11.Text,Edit21.Text); end;
end;

procedure TSeak20.Edit22KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  if SpeedButton22.Enabled=True Then begin
  Sos01:='2'; SetSeek01(ComboBox12.Text,Edit22.Text); end;
end;

procedure TSeak20.Edit23KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  if SpeedButton22.Enabled=True Then begin
  Sos01:='3'; SetSeek01(ComboBox13.Text,Edit23.Text); end;
end;

procedure TSeak20.Edit24KeyPress(Sender: TObject; var Key: Char);
begin
  if Key=#13 Then
  if SpeedButton22.Enabled=True Then begin
  Sos01:='4'; SetSeek01(ComboBox14.Text,Edit24.Text); end;
end;

procedure TSeak20.BitBtn101Click(Sender: TObject);
var St1,St2,St3,St4: String;
begin
  Code1:=''; St1:='';
  if (ComboBox11.Text<>'') and (ComboBox21.Text<>'') Then begin
    ComboBox01.ItemIndex:=ComboBox11.ItemIndex;
    St3:=ComboBox01.Text;
    St4:=ComboBox31.Text;
    if (Sot01='1') Then
    St1:=St1+St2+St3+St4+ComboBox21.Text else
    if (Sot01='2') and (ComboBox31.Text='=') Then
    St1:=St1+St2+St3+' like '+#39+'%'+ComboBox21.Text+'%'+#39 else
  { St1:=St1+St2+St3+' like '+#39+'%'+ComboBox21.Text+'%'+#39 else }
    if (Sot01='2') and (ComboBox31.Text='<>') Then
    St1:=St1+St2+' Not'+'('+St3+' like '+#39+'%'+ComboBox21.Text+'%'+#39+')' else
    if (Sot01='2') Then
    St1:=St1+St2+St3+St4+#39+ComboBox21.Text+#39;
    St1:='('+St1+')';
    if RadioButton11.Checked=True Then St2:=' And ';
    if RadioButton12.Checked=True Then St2:=' Or  ';
  end;
  if (ComboBox12.Text<>'') and (ComboBox22.Text<>'') Then begin
    ComboBox02.ItemIndex:=ComboBox12.ItemIndex;
    St3:=ComboBox02.Text;
    St4:=ComboBox32.Text;
    if (Sot02='1') Then
    St1:=St1+St2+St3+St4+ComboBox22.Text else
    if (Sot02='2') and (ComboBox32.Text='=') Then
    St1:=St1+St2+St3+' like '+#39+'%'+ComboBox22.Text+'%'+#39 else
  { St1:=St1+St2+St3+' like '+#39+'%'+ComboBox22.Text+'%'+#39 else }
    if (Sot02='2') and (ComboBox32.Text='<>') Then
    St1:=St1+St2+' Not'+'('+St3+' like '+#39+'%'+ComboBox22.Text+'%'+#39+')' else
    if (Sot02='2') Then
    St1:=St1+St2+St3+St4+#39+ComboBox22.Text+#39;
    St1:='('+St1+')';
    if RadioButton13.Checked=True Then St2:=' And ';
    if RadioButton14.Checked=True Then St2:=' Or  ';
  end;
  if (ComboBox13.Text<>'') and (ComboBox23.Text<>'') Then begin
    ComboBox03.ItemIndex:=ComboBox13.ItemIndex;
    St3:=ComboBox03.Text;
    St4:=ComboBox33.Text;
    if (Sot03='1') Then
    St1:=St1+St2+St3+St4+ComboBox23.Text else
    if (Sot03='2') and (ComboBox33.Text='=') Then
    St1:=St1+St2+St3+' like '+#39+'%'+ComboBox23.Text+'%'+#39 else
  { St1:=St1+St2+St3+' like '+#39+'%'+ComboBox23.Text+'%'+#39 else }
    if (Sot03='2') and (ComboBox33.Text='<>') Then
    St1:=St1+St2+' Not'+'('+St3+' like '+#39+'%'+ComboBox23.Text+'%'+#39+')' else
    if (Sot03='2') Then
    St1:=St1+St2+St3+St4+#39+ComboBox23.Text+#39;
    St1:='('+St1+')';
    if RadioButton15.Checked=True Then St2:=' And ';
    if RadioButton16.Checked=True Then St2:=' Or  ';
  end;
  if (ComboBox14.Text<>'') and (ComboBox24.Text<>'') Then begin
    ComboBox04.ItemIndex:=ComboBox14.ItemIndex;
    St3:=ComboBox04.Text;
    St4:=ComboBox34.Text;
    if (Sot04='1') Then
    St1:=St1+St2+St3+St4+ComboBox24.Text else
    if (Sot04='2') and (ComboBox34.Text='=') Then
    St1:=St1+St2+St3+' like '+#39+'%'+ComboBox24.Text+'%'+#39 else
  { St1:=St1+St2+St3+' like '+#39+'%'+ComboBox24.Text+'%'+#39 else }
    if (Sot04='2') and (ComboBox34.Text='<>') Then
    St1:=St1+St2+' Not'+'('+St3+' like '+#39+'%'+ComboBox24.Text+'%'+#39+')' else
    if (Sot04='2') Then
    St1:=St1+St2+St3+St4+#39+ComboBox24.Text+#39;
    St1:='('+St1+')';
  end;
  if St1<>'' Then Code1:=St1+' And ';
  if St1<>'' Then begin
     oSqry.Filter:=St1;
     oSqry.Filtered:=True;
  end;
end;

procedure TSeak20.BitBtn102Click(Sender: TObject);
begin
  ComboBox11.ItemIndex:=-1; ComboBox12.ItemIndex:=-1;
  ComboBox13.ItemIndex:=-1; ComboBox14.ItemIndex:=-1;
  ComboBox21.ItemIndex:=-1; ComboBox22.ItemIndex:=-1;
  ComboBox23.ItemIndex:=-1; ComboBox24.ItemIndex:=-1;
  RadioButton11.Checked:=False; RadioButton12.Checked:=False;
  RadioButton13.Checked:=False; RadioButton14.Checked:=False;
  RadioButton15.Checked:=False; RadioButton16.Checked:=False;
  Edit21.Text:=''; Edit22.Text:=''; Edit23.Text:=''; Edit24.Text:='';
  Close;
end;

procedure TSeak20.DBGrid1DblClick(Sender: TObject);
begin
  SetSeek04(Sos02,Sos01);
  DBGrid1.Visible:=False;
end;

procedure TSeak20.DBGrid1Exit(Sender: TObject);
begin
  DBGrid1.Visible:=False;
end;

end.
