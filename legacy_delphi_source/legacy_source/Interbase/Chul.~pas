unit Chul;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  ImgList, Menus, ExtCtrls, ComCtrls, ToolWin, IniFiles, ShellAPI, Grids,
  Ping, DIMime, Registry, Printers, MDIWallp;

type
  TSubu00 = class(TForm)
    MainMenu1: TMainMenu;
    Menu100: TMenuItem;
    Menu101: TMenuItem;
    Menu102: TMenuItem;
    Menu104: TMenuItem;
    Menu105: TMenuItem;
    Menu106: TMenuItem;
    Menu107: TMenuItem;
    Menu108: TMenuItem;
    Menu109: TMenuItem;
    Menu110: TMenuItem;
    Menu191: TMenuItem;
    Menu192: TMenuItem;
    Menu193: TMenuItem;
    Menu200: TMenuItem;
    Menu201: TMenuItem;
    Menu202: TMenuItem;
    Menu203: TMenuItem;
    Menu506: TMenuItem;
    Menu507: TMenuItem;
    Menu206: TMenuItem;
    Menu508: TMenuItem;
    Menu209: TMenuItem;
    Menu291: TMenuItem;
    Menu292: TMenuItem;
    Menu293: TMenuItem;
    Menu300: TMenuItem;
    Menu302: TMenuItem;
    Menu304: TMenuItem;
    Menu391: TMenuItem;
    Menu392: TMenuItem;
    Menu393: TMenuItem;
    Menu400: TMenuItem;
    Menu401: TMenuItem;
    Menu402: TMenuItem;
    Menu403: TMenuItem;
    Menu404: TMenuItem;
    Menu405: TMenuItem;
    Menu491: TMenuItem;
    Menu492: TMenuItem;
    Menu493: TMenuItem;
    Menu500: TMenuItem;
    Menu505: TMenuItem;
    Menu502: TMenuItem;
    Menu503: TMenuItem;
    Menu504: TMenuItem;
    Menu591: TMenuItem;
    Menu592: TMenuItem;
    Menu593: TMenuItem;
    Menu600: TMenuItem;
    Menu601: TMenuItem;
    Menu602: TMenuItem;
    Menu603: TMenuItem;
    Menu604: TMenuItem;
    Menu605: TMenuItem;
    Menu606: TMenuItem;
    Menu607: TMenuItem;
    Menu608: TMenuItem;
    Menu691: TMenuItem;
    Menu692: TMenuItem;
    Menu693: TMenuItem;
    PopupMenu1: TPopupMenu;
    OpenDialog1: TOpenDialog;
    SaveDialog1: TSaveDialog;
    PrintDialog1: TPrintDialog;
    PrinterSetupDialog1: TPrinterSetupDialog;
    ToolbarImages: TImageList;
    ToolBar: TToolBar;
    ToolButton01: TToolButton;
    ToolButton02: TToolButton;
    ToolButton03: TToolButton;
    ToolButton04: TToolButton;
    ToolButton05: TToolButton;
    ToolButton06: TToolButton;
    ToolButton07: TToolButton;
    ToolButton08: TToolButton;
    ToolButton09: TToolButton;
    ToolButton10: TToolButton;
    ToolButton11: TToolButton;
    ToolButton12: TToolButton;
    ToolButton13: TToolButton;
    ToolButton14: TToolButton;
    ToolButton15: TToolButton;
    ToolButton16: TToolButton;
    ToolButton17: TToolButton;
    ToolButton18: TToolButton;
    ToolButton19: TToolButton;
    ToolButton20: TToolButton;
    ToolButton21: TToolButton;
    ToolButton22: TToolButton;
    ToolButton23: TToolButton;
    ToolButton24: TToolButton;
    ToolButton91: TToolButton;
    ToolButton92: TToolButton;
    ToolButton93: TToolButton;
    ToolButton94: TToolButton;
    ToolButton95: TToolButton;
    ToolButton96: TToolButton;
    ToolButton97: TToolButton;
    ToolButton98: TToolButton;
    ToolButton99: TToolButton;
    Ping1: TPing;
    Timer1: TTimer;
    StringGrid1: TStringGrid;
    StringGrid2: TStringGrid;
    Menu207: TMenuItem;
    Menu103: TMenuItem;
    Menu204: TMenuItem;
    Menu205: TMenuItem;
    Menu301: TMenuItem;
    Menu303: TMenuItem;
    Menu309: TMenuItem;
    Menu308: TMenuItem;
    MDIWallpaper1: TMDIWallpaper;
    Menu208: TMenuItem;
    procedure FormActivate(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure ToolButton01Click(Sender: TObject);
    procedure ToolButton02Click(Sender: TObject);
    procedure ToolButton03Click(Sender: TObject);
    procedure ToolButton04Click(Sender: TObject);
    procedure ToolButton05Click(Sender: TObject);
    procedure ToolButton06Click(Sender: TObject);
    procedure ToolButton07Click(Sender: TObject);
    procedure ToolButton08Click(Sender: TObject);
    procedure ToolButton09Click(Sender: TObject);
    procedure ToolButton10Click(Sender: TObject);
    procedure ToolButton11Click(Sender: TObject);
    procedure ToolButton12Click(Sender: TObject);
    procedure ToolButton13Click(Sender: TObject);
    procedure ToolButton14Click(Sender: TObject);
    procedure ToolButton15Click(Sender: TObject);
    procedure ToolButton16Click(Sender: TObject);
    procedure ToolButton17Click(Sender: TObject);
    procedure ToolButton18Click(Sender: TObject);
    procedure ToolButton19Click(Sender: TObject);
    procedure ToolButton20Click(Sender: TObject);
    procedure ToolButton21Click(Sender: TObject);
    procedure ToolButton22Click(Sender: TObject);
    procedure ToolButton23Click(Sender: TObject);
    procedure ToolButton24Click(Sender: TObject);
    procedure ToolButton25Click(Sender: TObject);
    procedure ToolButton26Click(Sender: TObject);
    procedure ToolButton27Click(Sender: TObject);
    procedure Menu101Click(Sender: TObject);
    procedure Menu102Click(Sender: TObject);
    procedure Menu103Click(Sender: TObject);
    procedure Menu104Click(Sender: TObject);
    procedure Menu105Click(Sender: TObject);
    procedure Menu106Click(Sender: TObject);
    procedure Menu107Click(Sender: TObject);
    procedure Menu108Click(Sender: TObject);
    procedure Menu109Click(Sender: TObject);
    procedure Menu110Click(Sender: TObject);
    procedure Menu201Click(Sender: TObject);
    procedure Menu202Click(Sender: TObject);
    procedure Menu203Click(Sender: TObject);
    procedure Menu204Click(Sender: TObject);
    procedure Menu205Click(Sender: TObject);
    procedure Menu206Click(Sender: TObject);
    procedure Menu207Click(Sender: TObject);
    procedure Menu208Click(Sender: TObject);
    procedure Menu209Click(Sender: TObject);
    procedure Menu210Click(Sender: TObject);
    procedure Menu301Click(Sender: TObject);
    procedure Menu302Click(Sender: TObject);
    procedure Menu303Click(Sender: TObject);
    procedure Menu304Click(Sender: TObject);
    procedure Menu305Click(Sender: TObject);
    procedure Menu306Click(Sender: TObject);
    procedure Menu307Click(Sender: TObject);
    procedure Menu308Click(Sender: TObject);
    procedure Menu309Click(Sender: TObject);
    procedure Menu310Click(Sender: TObject);
    procedure Menu401Click(Sender: TObject);
    procedure Menu402Click(Sender: TObject);
    procedure Menu403Click(Sender: TObject);
    procedure Menu404Click(Sender: TObject);
    procedure Menu405Click(Sender: TObject);
    procedure Menu406Click(Sender: TObject);
    procedure Menu407Click(Sender: TObject);
    procedure Menu408Click(Sender: TObject);
    procedure Menu409Click(Sender: TObject);
    procedure Menu410Click(Sender: TObject);
    procedure Menu501Click(Sender: TObject);
    procedure Menu502Click(Sender: TObject);
    procedure Menu503Click(Sender: TObject);
    procedure Menu504Click(Sender: TObject);
    procedure Menu505Click(Sender: TObject);
    procedure Menu506Click(Sender: TObject);
    procedure Menu507Click(Sender: TObject);
    procedure Menu508Click(Sender: TObject);
    procedure Menu509Click(Sender: TObject);
    procedure Menu510Click(Sender: TObject);
    procedure Menu601Click(Sender: TObject);
    procedure Menu602Click(Sender: TObject);
    procedure Menu603Click(Sender: TObject);
    procedure Menu604Click(Sender: TObject);
    procedure Menu605Click(Sender: TObject);
    procedure Menu606Click(Sender: TObject);
    procedure Menu607Click(Sender: TObject);
    procedure Menu608Click(Sender: TObject);
    procedure Menu609Click(Sender: TObject);
    procedure Menu610Click(Sender: TObject);
    procedure Ping1DnsLookupDone(Sender: TObject; Error: Word);
    procedure Ping1EchoReply(Sender, Icmp: TObject; Error: Integer);
    procedure Ping1EchoRequest(Sender, Icmp: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Subu00: TSubu00;
  iHandle: THandle;
  nBase: String;
  nUse1,nUse2: String;
  nUses,nPcip: String;
  nPort: Integer;
  xMutex: DWORD;

implementation

{$R *.DFM}

uses Base01,Tong02,Tong03,Tong04,TcpLib,Seok03,Subu71,
     Subu11,Subu12,Subu13,Subu14,Subu15,Subu16,Subu17,Subu18,Subu19,Subu10,
     Subu21,Subu22,Subu23,Subu24,Subu25,Subu26,Subu27,Subu28,Subu29,Subu20,
     Subu31,Subu32,Subu33,Subu34,Subu35,Subu36,Subu37,Subu38,Subu39,Subu30,
     Subu41,Subu42,Subu43,Subu44,Subu45,Subu46,Subu47,Subu48,Subu49,Subu40,
     Subu51,Subu52,Subu53,Subu54,Subu55,Subu56,Subu57,Subu58,Subu59,Subu50,
     Subu61,Subu62,Subu63,Subu64,Subu65,Subu66,Subu67,Subu68,Subu69,Subu60;

procedure TSubu00.FormActivate(Sender: TObject);
var I,T:Integer;
begin
  T:=0;
  for I:=0 to MDIChildCount - 1 do
  T:=1;
  if T=0 Then nForm:='00';
end;

procedure TSubu00.FormShow(Sender: TObject);
var SetupIni : TIniFile;
    StrList : TStrings;
    Reg: TRegistry;
    ChulpanKey : String;
begin

  SetupIni := TIniFile.Create(GetExecPath + 'Config.Ini');
  With SetupIni do begin
    nBase:=ReadString('Client', 'Base', '');
    mPrnt:=ReadString('Client', 'Name', '');
    nUses:=ReadString('Client', 'Uses', '');
    nPcip:=ReadString('Client', 'Pcip', '');
    nPort:=ReadInteger('Client','Port', 0 );
    Jeago:=ReadString('Print', 'Jeago', '');
    Lower:=ReadString('Print', 'Lower', '');
  end;
  SetupIni.Free;

  SGrid:=StringGrid1;
  YGrid:=StringGrid2;

{ Base10.Socket.Close;
  Base10.Socket.Address:=nPcip;
  Base10.Socket.Port:=nPort;
  Base10.Socket.Open; }

{ StrList:=Tong20.GetIPs;
  nPcip:=StrList.Strings[0]; }

  if(nPcip<>'')and(Pos('.',nPcip)=0)then begin
  StrList:=Tong20.SetIPs(nPcip);
  nPcip:=StrList.Strings[0]; end;

  if nPcip='' then
  Base10.Database.DatabaseName:=nBase else
  Base10.Database.DatabaseName:=nPcip+':'+nBase;

{ Base10.Database.Host:='211.55.29.154';
  Base10.Database.Login:='test';
  Base10.Database.Password:='test';
  Base10.Database.Database:='test';

  Base10.Database.Host:='210.109.102.86';
  Base10.Database.Login:='test_user';
  Base10.Database.Password:='test_pw';
  Base10.Database.Database:='test_db';

  Base10.Database.Host:='210.109.102.86';
  Base10.Database.Login:='book_js_user';
  Base10.Database.Password:='book_js_pw';
  Base10.Database.Database:='book_js_db';

  Base10.Database.Host:='210.109.102.86';
  Base10.Database.Login:='book_gs_user';
  Base10.Database.Password:='book_gs_pw';
  Base10.Database.Database:='book_gs_db';

  Base10.Database.Host:='210.109.102.86';
  Base10.Database.Login:='book_kb_user';
  Base10.Database.Password:='book_kb_pw';
  Base10.Database.Database:='book_kb_db'; }

  try

    ePrnt:='1'; //Interbase

    Base10.Database.Connected:=True;

  { Timer1.OnTimer:=ToolButton25Click;

    Sqlen :='Select Hcode,Hname,Gpass From Id_Logn '+
            'Where Gcode='+#39+Logn2+#39+
            '  and Gname='+#39+Logn1+#39;

    Base10.Socket.RunSQL(Sqlen);
    Base10.Socket.busyloop;
    if Base10.Socket.Body_Data <> 'NODATA' then begin
      Base10.Socket.MakeData;
      if Logn3=Base10.Socket.GetData(1, 3) then begin
        Hnnnn:=Base10.Socket.GetData(1, 1);
        Subu00.Caption:=Subu00.Caption+'-'+Base10.Socket.GetData(1, 2);
      end else begin
        ShowMessage('비밀번호가 틀립니다.');
        Close;
      end;
    end else begin
        ShowMessage('사용자 또는 아이디가 틀립니다.');
      Close;
    end;

    Reg:=TRegistry.Create;
    try
    //Reg.RootKey:=HKEY_LOCAL_MACHINE;
      if Reg.OpenKey('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce', False) then begin
         ChulpanKey:=MimeDecodeString(Reg.ReadString('ChulpanKey'));
      end;
    finally
      Reg.CloseKey;
      Reg.Free;
      inherited;
    end;
    if Hnnnn<>ChulpanKey then begin
      ShowMessage('Program Key를 등록해 주세요.');
      Close;
    end; }

  except
      ShowMessage('다시 시도해 주십시오.');
      Close;
  end;

  DateSeparator := '.';
  ShortDateFormat := 'YYYY.MM.DD';
  LongDateFormat  := 'YYYY.MM.DD';

  Base10.Init_Show(Self);
end;

procedure TSubu00.FormClose(Sender: TObject; var Action: TCloseAction);
var I:Integer;
begin
  SGrid.Free;
  YGrid.Free;

{ if Base10.Socket.Active=True then begin
    nUse1:='Client-DisConnect'+'Uses:'+nUses+'Pcip:'+nPcip+'Subu:';
    nUse2:=nUse1+'Sub00';
    nUse2:=Base10.Seek_Uses(nUse2);
  end; }

  Base10.Socket.Close;
  for I:=0 to MDIChildCount - 1 do
    MDIChildren[I].Close;

  Base10.Database.Connected:=False;
end;

procedure TSubu00.ToolButton01Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button001Click(Self);
  if nForm='12' Then Sobo12.Button001Click(Self);
  if nForm='13' Then Sobo13.Button001Click(Self);
  if nForm='14' Then Sobo14.Button001Click(Self);
  if nForm='15' Then Sobo15.Button001Click(Self);
  if nForm='16' Then Sobo16.Button001Click(Self);
  if nForm='17' Then Sobo17.Button001Click(Self);
  if nForm='18' Then Sobo18.Button001Click(Self);
  if nForm='19' Then Sobo19.Button001Click(Self);
  if nForm='10' Then Sobo10.Button001Click(Self);

  if nForm='21' Then Sobo21.Button001Click(Self);
  if nForm='22' Then Sobo22.Button001Click(Self);
  if nForm='23' Then Sobo23.Button001Click(Self);
  if nForm='24' Then Sobo24.Button001Click(Self);
  if nForm='25' Then Sobo25.Button001Click(Self);
  if nForm='26' Then Sobo26.Button001Click(Self);
  if nForm='27' Then Sobo27.Button001Click(Self);
  if nForm='28' Then Sobo28.Button001Click(Self);
  if nForm='29' Then Sobo29.Button001Click(Self);
  if nForm='20' Then Sobo20.Button001Click(Self);

  if nForm='31' Then Sobo31.Button001Click(Self);
  if nForm='32' Then Sobo32.Button001Click(Self);
  if nForm='33' Then Sobo33.Button001Click(Self);
  if nForm='34' Then Sobo34.Button001Click(Self);
  if nForm='35' Then Sobo35.Button001Click(Self);
  if nForm='36' Then Sobo36.Button001Click(Self);
  if nForm='37' Then Sobo37.Button001Click(Self);
  if nForm='38' Then Sobo38.Button001Click(Self);
  if nForm='39' Then Sobo39.Button001Click(Self);
  if nForm='30' Then Sobo30.Button001Click(Self);

  if nForm='41' Then Sobo41.Button001Click(Self);
  if nForm='42' Then Sobo42.Button001Click(Self);
  if nForm='43' Then Sobo43.Button001Click(Self);
  if nForm='44' Then Sobo44.Button001Click(Self);
  if nForm='45' Then Sobo45.Button001Click(Self);
  if nForm='46' Then Sobo46.Button001Click(Self);
  if nForm='47' Then Sobo47.Button001Click(Self);
  if nForm='48' Then Sobo48.Button001Click(Self);
  if nForm='49' Then Sobo49.Button001Click(Self);
  if nForm='40' Then Sobo40.Button001Click(Self);

  if nForm='51' Then Sobo51.Button001Click(Self);
  if nForm='52' Then Sobo52.Button001Click(Self);
  if nForm='53' Then Sobo53.Button001Click(Self);
  if nForm='54' Then Sobo54.Button001Click(Self);
  if nForm='55' Then Sobo55.Button001Click(Self);
  if nForm='56' Then Sobo56.Button001Click(Self);
  if nForm='57' Then Sobo57.Button001Click(Self);
  if nForm='58' Then Sobo58.Button001Click(Self);
  if nForm='59' Then Sobo59.Button001Click(Self);
  if nForm='50' Then Sobo50.Button001Click(Self);

  if nForm='61' Then Sobo61.Button001Click(Self);
  if nForm='62' Then Sobo62.Button001Click(Self);
  if nForm='63' Then Sobo63.Button001Click(Self);
  if nForm='64' Then Sobo64.Button001Click(Self);
  if nForm='65' Then Sobo65.Button001Click(Self);
  if nForm='66' Then Sobo66.Button001Click(Self);
  if nForm='67' Then Sobo67.Button001Click(Self);
  if nForm='68' Then Sobo68.Button001Click(Self);
  if nForm='69' Then Sobo69.Button001Click(Self);
  if nForm='60' Then Sobo60.Button001Click(Self);
end;

procedure TSubu00.ToolButton02Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button002Click(Self);
  if nForm='12' Then Sobo12.Button002Click(Self);
  if nForm='13' Then Sobo13.Button002Click(Self);
  if nForm='14' Then Sobo14.Button002Click(Self);
  if nForm='15' Then Sobo15.Button002Click(Self);
  if nForm='16' Then Sobo16.Button002Click(Self);
  if nForm='17' Then Sobo17.Button002Click(Self);
  if nForm='18' Then Sobo18.Button002Click(Self);
  if nForm='19' Then Sobo19.Button002Click(Self);
  if nForm='10' Then Sobo10.Button002Click(Self);

  if nForm='21' Then Sobo21.Button002Click(Self);
  if nForm='22' Then Sobo22.Button002Click(Self);
  if nForm='23' Then Sobo23.Button002Click(Self);
  if nForm='24' Then Sobo24.Button002Click(Self);
  if nForm='25' Then Sobo25.Button002Click(Self);
  if nForm='26' Then Sobo26.Button002Click(Self);
  if nForm='27' Then Sobo27.Button002Click(Self);
  if nForm='28' Then Sobo28.Button002Click(Self);
  if nForm='29' Then Sobo29.Button002Click(Self);
  if nForm='20' Then Sobo20.Button002Click(Self);

  if nForm='31' Then Sobo31.Button002Click(Self);
  if nForm='32' Then Sobo32.Button002Click(Self);
  if nForm='33' Then Sobo33.Button002Click(Self);
  if nForm='34' Then Sobo34.Button002Click(Self);
  if nForm='35' Then Sobo35.Button002Click(Self);
  if nForm='36' Then Sobo36.Button002Click(Self);
  if nForm='37' Then Sobo37.Button002Click(Self);
  if nForm='38' Then Sobo38.Button002Click(Self);
  if nForm='39' Then Sobo39.Button002Click(Self);
  if nForm='30' Then Sobo30.Button002Click(Self);

  if nForm='41' Then Sobo41.Button002Click(Self);
  if nForm='42' Then Sobo42.Button002Click(Self);
  if nForm='43' Then Sobo43.Button002Click(Self);
  if nForm='44' Then Sobo44.Button002Click(Self);
  if nForm='45' Then Sobo45.Button002Click(Self);
  if nForm='46' Then Sobo46.Button002Click(Self);
  if nForm='47' Then Sobo47.Button002Click(Self);
  if nForm='48' Then Sobo48.Button002Click(Self);
  if nForm='49' Then Sobo49.Button002Click(Self);
  if nForm='40' Then Sobo40.Button002Click(Self);

  if nForm='51' Then Sobo51.Button002Click(Self);
  if nForm='52' Then Sobo52.Button002Click(Self);
  if nForm='53' Then Sobo53.Button002Click(Self);
  if nForm='54' Then Sobo54.Button002Click(Self);
  if nForm='55' Then Sobo55.Button002Click(Self);
  if nForm='56' Then Sobo56.Button002Click(Self);
  if nForm='57' Then Sobo57.Button002Click(Self);
  if nForm='58' Then Sobo58.Button002Click(Self);
  if nForm='59' Then Sobo59.Button002Click(Self);
  if nForm='50' Then Sobo50.Button002Click(Self);

  if nForm='61' Then Sobo61.Button002Click(Self);
  if nForm='62' Then Sobo62.Button002Click(Self);
  if nForm='63' Then Sobo63.Button002Click(Self);
  if nForm='64' Then Sobo64.Button002Click(Self);
  if nForm='65' Then Sobo65.Button002Click(Self);
  if nForm='66' Then Sobo66.Button002Click(Self);
  if nForm='67' Then Sobo67.Button002Click(Self);
  if nForm='68' Then Sobo68.Button002Click(Self);
  if nForm='69' Then Sobo69.Button002Click(Self);
  if nForm='60' Then Sobo60.Button002Click(Self);
end;

procedure TSubu00.ToolButton03Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button003Click(Self);
  if nForm='12' Then Sobo12.Button003Click(Self);
  if nForm='13' Then Sobo13.Button003Click(Self);
  if nForm='14' Then Sobo14.Button003Click(Self);
  if nForm='15' Then Sobo15.Button003Click(Self);
  if nForm='16' Then Sobo16.Button003Click(Self);
  if nForm='17' Then Sobo17.Button003Click(Self);
  if nForm='18' Then Sobo18.Button003Click(Self);
  if nForm='19' Then Sobo19.Button003Click(Self);
  if nForm='10' Then Sobo10.Button003Click(Self);

  if nForm='21' Then Sobo21.Button003Click(Self);
  if nForm='22' Then Sobo22.Button003Click(Self);
  if nForm='23' Then Sobo23.Button003Click(Self);
  if nForm='24' Then Sobo24.Button003Click(Self);
  if nForm='25' Then Sobo25.Button003Click(Self);
  if nForm='26' Then Sobo26.Button003Click(Self);
  if nForm='27' Then Sobo27.Button003Click(Self);
  if nForm='28' Then Sobo28.Button003Click(Self);
  if nForm='29' Then Sobo29.Button003Click(Self);
  if nForm='20' Then Sobo20.Button003Click(Self);

  if nForm='31' Then Sobo31.Button003Click(Self);
  if nForm='32' Then Sobo32.Button003Click(Self);
  if nForm='33' Then Sobo33.Button003Click(Self);
  if nForm='34' Then Sobo34.Button003Click(Self);
  if nForm='35' Then Sobo35.Button003Click(Self);
  if nForm='36' Then Sobo36.Button003Click(Self);
  if nForm='37' Then Sobo37.Button003Click(Self);
  if nForm='38' Then Sobo38.Button003Click(Self);
  if nForm='39' Then Sobo39.Button003Click(Self);
  if nForm='30' Then Sobo30.Button003Click(Self);

  if nForm='41' Then Sobo41.Button003Click(Self);
  if nForm='42' Then Sobo42.Button003Click(Self);
  if nForm='43' Then Sobo43.Button003Click(Self);
  if nForm='44' Then Sobo44.Button003Click(Self);
  if nForm='45' Then Sobo45.Button003Click(Self);
  if nForm='46' Then Sobo46.Button003Click(Self);
  if nForm='47' Then Sobo47.Button003Click(Self);
  if nForm='48' Then Sobo48.Button003Click(Self);
  if nForm='49' Then Sobo49.Button003Click(Self);
  if nForm='40' Then Sobo40.Button003Click(Self);

  if nForm='51' Then Sobo51.Button003Click(Self);
  if nForm='52' Then Sobo52.Button003Click(Self);
  if nForm='53' Then Sobo53.Button003Click(Self);
  if nForm='54' Then Sobo54.Button003Click(Self);
  if nForm='55' Then Sobo55.Button003Click(Self);
  if nForm='56' Then Sobo56.Button003Click(Self);
  if nForm='57' Then Sobo57.Button003Click(Self);
  if nForm='58' Then Sobo58.Button003Click(Self);
  if nForm='59' Then Sobo59.Button003Click(Self);
  if nForm='50' Then Sobo50.Button003Click(Self);

  if nForm='61' Then Sobo61.Button003Click(Self);
  if nForm='62' Then Sobo62.Button003Click(Self);
  if nForm='63' Then Sobo63.Button003Click(Self);
  if nForm='64' Then Sobo64.Button003Click(Self);
  if nForm='65' Then Sobo65.Button003Click(Self);
  if nForm='66' Then Sobo66.Button003Click(Self);
  if nForm='67' Then Sobo67.Button003Click(Self);
  if nForm='68' Then Sobo68.Button003Click(Self);
  if nForm='69' Then Sobo69.Button003Click(Self);
  if nForm='60' Then Sobo60.Button003Click(Self);
end;

procedure TSubu00.ToolButton04Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button004Click(Self);
  if nForm='12' Then Sobo12.Button004Click(Self);
  if nForm='13' Then Sobo13.Button004Click(Self);
  if nForm='14' Then Sobo14.Button004Click(Self);
  if nForm='15' Then Sobo15.Button004Click(Self);
  if nForm='16' Then Sobo16.Button004Click(Self);
  if nForm='17' Then Sobo17.Button004Click(Self);
  if nForm='18' Then Sobo18.Button004Click(Self);
  if nForm='19' Then Sobo19.Button004Click(Self);
  if nForm='10' Then Sobo10.Button004Click(Self);

  if nForm='21' Then Sobo21.Button004Click(Self);
  if nForm='22' Then Sobo22.Button004Click(Self);
  if nForm='23' Then Sobo23.Button004Click(Self);
  if nForm='24' Then Sobo24.Button004Click(Self);
  if nForm='25' Then Sobo25.Button004Click(Self);
  if nForm='26' Then Sobo26.Button004Click(Self);
  if nForm='27' Then Sobo27.Button004Click(Self);
  if nForm='28' Then Sobo28.Button004Click(Self);
  if nForm='29' Then Sobo29.Button004Click(Self);
  if nForm='20' Then Sobo20.Button004Click(Self);

{ if nForm='31' Then Sobo31.Button004Click(Self);
  if nForm='32' Then Sobo32.Button004Click(Self);
  if nForm='33' Then Sobo33.Button004Click(Self);
  if nForm='34' Then Sobo34.Button004Click(Self);
  if nForm='35' Then Sobo35.Button004Click(Self);
  if nForm='36' Then Sobo36.Button004Click(Self);
  if nForm='37' Then Sobo37.Button004Click(Self);
  if nForm='38' Then Sobo38.Button004Click(Self);
  if nForm='39' Then Sobo39.Button004Click(Self);
  if nForm='30' Then Sobo30.Button004Click(Self); }

  if nForm='41' Then Sobo41.Button004Click(Self);
  if nForm='42' Then Sobo42.Button004Click(Self);
  if nForm='43' Then Sobo43.Button004Click(Self);
  if nForm='44' Then Sobo44.Button004Click(Self);
  if nForm='45' Then Sobo45.Button004Click(Self);
  if nForm='46' Then Sobo46.Button004Click(Self);
  if nForm='47' Then Sobo47.Button004Click(Self);
  if nForm='48' Then Sobo48.Button004Click(Self);
  if nForm='49' Then Sobo49.Button004Click(Self);
  if nForm='40' Then Sobo40.Button004Click(Self);

  if nForm='51' Then Sobo51.Button004Click(Self);
  if nForm='52' Then Sobo52.Button004Click(Self);
  if nForm='53' Then Sobo53.Button004Click(Self);
  if nForm='54' Then Sobo54.Button004Click(Self);
  if nForm='55' Then Sobo55.Button004Click(Self);
  if nForm='56' Then Sobo56.Button004Click(Self);
  if nForm='57' Then Sobo57.Button004Click(Self);
  if nForm='58' Then Sobo58.Button004Click(Self);
  if nForm='59' Then Sobo59.Button004Click(Self);
  if nForm='50' Then Sobo50.Button004Click(Self);

{ if nForm='61' Then Sobo61.Button004Click(Self);
  if nForm='62' Then Sobo62.Button004Click(Self);
  if nForm='63' Then Sobo63.Button004Click(Self);
  if nForm='64' Then Sobo64.Button004Click(Self);
  if nForm='65' Then Sobo65.Button004Click(Self);
  if nForm='66' Then Sobo66.Button004Click(Self);
  if nForm='67' Then Sobo67.Button004Click(Self);
  if nForm='68' Then Sobo68.Button004Click(Self);
  if nForm='69' Then Sobo69.Button004Click(Self);
  if nForm='60' Then Sobo60.Button004Click(Self); }
end;

procedure TSubu00.ToolButton05Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button005Click(Self);
  if nForm='12' Then Sobo12.Button005Click(Self);
  if nForm='13' Then Sobo13.Button005Click(Self);
  if nForm='14' Then Sobo14.Button005Click(Self);
  if nForm='15' Then Sobo15.Button005Click(Self);
  if nForm='16' Then Sobo16.Button005Click(Self);
  if nForm='17' Then Sobo17.Button005Click(Self);
  if nForm='18' Then Sobo18.Button005Click(Self);
  if nForm='19' Then Sobo19.Button005Click(Self);
  if nForm='10' Then Sobo10.Button005Click(Self);

  if nForm='21' Then Sobo21.Button005Click(Self);
  if nForm='22' Then Sobo22.Button005Click(Self);
  if nForm='23' Then Sobo23.Button005Click(Self);
  if nForm='24' Then Sobo24.Button005Click(Self);
  if nForm='25' Then Sobo25.Button005Click(Self);
  if nForm='26' Then Sobo26.Button005Click(Self);
  if nForm='27' Then Sobo27.Button005Click(Self);
  if nForm='28' Then Sobo28.Button005Click(Self);
  if nForm='29' Then Sobo29.Button005Click(Self);
  if nForm='20' Then Sobo20.Button005Click(Self);

  if nForm='31' Then Sobo31.Button005Click(Self);
  if nForm='32' Then Sobo32.Button005Click(Self);
  if nForm='33' Then Sobo33.Button005Click(Self);
  if nForm='34' Then Sobo34.Button005Click(Self);
  if nForm='35' Then Sobo35.Button005Click(Self);
  if nForm='36' Then Sobo36.Button005Click(Self);
  if nForm='37' Then Sobo37.Button005Click(Self);
  if nForm='38' Then Sobo38.Button005Click(Self);
  if nForm='39' Then Sobo39.Button005Click(Self);
  if nForm='30' Then Sobo30.Button005Click(Self);

  if nForm='41' Then Sobo41.Button005Click(Self);
  if nForm='42' Then Sobo42.Button005Click(Self);
  if nForm='43' Then Sobo43.Button005Click(Self);
  if nForm='44' Then Sobo44.Button005Click(Self);
  if nForm='45' Then Sobo45.Button005Click(Self);
  if nForm='46' Then Sobo46.Button005Click(Self);
  if nForm='47' Then Sobo47.Button005Click(Self);
  if nForm='48' Then Sobo48.Button005Click(Self);
  if nForm='49' Then Sobo49.Button005Click(Self);
  if nForm='40' Then Sobo40.Button005Click(Self);

  if nForm='51' Then Sobo51.Button005Click(Self);
  if nForm='52' Then Sobo52.Button005Click(Self);
  if nForm='53' Then Sobo53.Button005Click(Self);
  if nForm='54' Then Sobo54.Button005Click(Self);
  if nForm='55' Then Sobo55.Button005Click(Self);
  if nForm='56' Then Sobo56.Button005Click(Self);
  if nForm='57' Then Sobo57.Button005Click(Self);
  if nForm='58' Then Sobo58.Button005Click(Self);
  if nForm='59' Then Sobo59.Button005Click(Self);
  if nForm='50' Then Sobo50.Button005Click(Self);

  if nForm='61' Then Sobo61.Button005Click(Self);
  if nForm='62' Then Sobo62.Button005Click(Self);
  if nForm='63' Then Sobo63.Button005Click(Self);
  if nForm='64' Then Sobo64.Button005Click(Self);
  if nForm='65' Then Sobo65.Button005Click(Self);
  if nForm='66' Then Sobo66.Button005Click(Self);
  if nForm='67' Then Sobo67.Button005Click(Self);
  if nForm='68' Then Sobo68.Button005Click(Self);
  if nForm='69' Then Sobo69.Button005Click(Self);
  if nForm='60' Then Sobo60.Button005Click(Self);
end;

procedure TSubu00.ToolButton06Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button006Click(Self);
  if nForm='12' Then Sobo12.Button006Click(Self);
  if nForm='13' Then Sobo13.Button006Click(Self);
  if nForm='14' Then Sobo14.Button006Click(Self);
  if nForm='15' Then Sobo15.Button006Click(Self);
  if nForm='16' Then Sobo16.Button006Click(Self);
  if nForm='17' Then Sobo17.Button006Click(Self);
  if nForm='18' Then Sobo18.Button006Click(Self);
  if nForm='19' Then Sobo19.Button006Click(Self);
  if nForm='10' Then Sobo10.Button006Click(Self);

  if nForm='21' Then Sobo21.Button006Click(Self);
  if nForm='22' Then Sobo22.Button006Click(Self);
  if nForm='23' Then Sobo23.Button006Click(Self);
  if nForm='24' Then Sobo24.Button006Click(Self);
  if nForm='25' Then Sobo25.Button006Click(Self);
  if nForm='26' Then Sobo26.Button006Click(Self);
  if nForm='27' Then Sobo27.Button006Click(Self);
  if nForm='28' Then Sobo28.Button006Click(Self);
  if nForm='29' Then Sobo29.Button006Click(Self);
  if nForm='20' Then Sobo20.Button006Click(Self);

  if nForm='31' Then Sobo31.Button006Click(Self);
  if nForm='32' Then Sobo32.Button006Click(Self);
  if nForm='33' Then Sobo33.Button006Click(Self);
  if nForm='34' Then Sobo34.Button006Click(Self);
  if nForm='35' Then Sobo35.Button006Click(Self);
  if nForm='36' Then Sobo36.Button006Click(Self);
  if nForm='37' Then Sobo37.Button006Click(Self);
  if nForm='38' Then Sobo38.Button006Click(Self);
  if nForm='39' Then Sobo39.Button006Click(Self);
  if nForm='30' Then Sobo30.Button006Click(Self);

  if nForm='41' Then Sobo41.Button006Click(Self);
  if nForm='42' Then Sobo42.Button006Click(Self);
  if nForm='43' Then Sobo43.Button006Click(Self);
  if nForm='44' Then Sobo44.Button006Click(Self);
  if nForm='45' Then Sobo45.Button006Click(Self);
  if nForm='46' Then Sobo46.Button006Click(Self);
  if nForm='47' Then Sobo47.Button006Click(Self);
  if nForm='48' Then Sobo48.Button006Click(Self);
  if nForm='49' Then Sobo49.Button006Click(Self);
  if nForm='40' Then Sobo40.Button006Click(Self);

  if nForm='51' Then Sobo51.Button006Click(Self);
  if nForm='52' Then Sobo52.Button006Click(Self);
  if nForm='53' Then Sobo53.Button006Click(Self);
  if nForm='54' Then Sobo54.Button006Click(Self);
  if nForm='55' Then Sobo55.Button006Click(Self);
  if nForm='56' Then Sobo56.Button006Click(Self);
  if nForm='57' Then Sobo57.Button006Click(Self);
  if nForm='58' Then Sobo58.Button006Click(Self);
  if nForm='59' Then Sobo59.Button006Click(Self);
  if nForm='50' Then Sobo50.Button006Click(Self);

  if nForm='61' Then Sobo61.Button006Click(Self);
  if nForm='62' Then Sobo62.Button006Click(Self);
  if nForm='63' Then Sobo63.Button006Click(Self);
  if nForm='64' Then Sobo64.Button006Click(Self);
  if nForm='65' Then Sobo65.Button006Click(Self);
  if nForm='66' Then Sobo66.Button006Click(Self);
  if nForm='67' Then Sobo67.Button006Click(Self);
  if nForm='68' Then Sobo68.Button006Click(Self);
  if nForm='69' Then Sobo69.Button006Click(Self);
  if nForm='60' Then Sobo60.Button006Click(Self);
end;

procedure TSubu00.ToolButton07Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button007Click(Self);
  if nForm='12' Then Sobo12.Button007Click(Self);
  if nForm='13' Then Sobo13.Button007Click(Self);
  if nForm='14' Then Sobo14.Button007Click(Self);
  if nForm='15' Then Sobo15.Button007Click(Self);
  if nForm='16' Then Sobo16.Button007Click(Self);
  if nForm='17' Then Sobo17.Button007Click(Self);
  if nForm='18' Then Sobo18.Button007Click(Self);
  if nForm='19' Then Sobo19.Button007Click(Self);
  if nForm='10' Then Sobo10.Button007Click(Self);

  if nForm='21' Then Sobo21.Button007Click(Self);
  if nForm='22' Then Sobo22.Button007Click(Self);
  if nForm='23' Then Sobo23.Button007Click(Self);
  if nForm='24' Then Sobo24.Button007Click(Self);
  if nForm='25' Then Sobo25.Button007Click(Self);
  if nForm='26' Then Sobo26.Button007Click(Self);
  if nForm='27' Then Sobo27.Button007Click(Self);
  if nForm='28' Then Sobo28.Button007Click(Self);
  if nForm='29' Then Sobo29.Button007Click(Self);
  if nForm='20' Then Sobo20.Button007Click(Self);

  if nForm='31' Then Sobo31.Button007Click(Self);
  if nForm='32' Then Sobo32.Button007Click(Self);
  if nForm='33' Then Sobo33.Button007Click(Self);
  if nForm='34' Then Sobo34.Button007Click(Self);
  if nForm='35' Then Sobo35.Button007Click(Self);
  if nForm='36' Then Sobo36.Button007Click(Self);
  if nForm='37' Then Sobo37.Button007Click(Self);
  if nForm='38' Then Sobo38.Button007Click(Self);
  if nForm='39' Then Sobo39.Button007Click(Self);
  if nForm='30' Then Sobo30.Button007Click(Self);

  if nForm='41' Then Sobo41.Button007Click(Self);
  if nForm='42' Then Sobo42.Button007Click(Self);
  if nForm='43' Then Sobo43.Button007Click(Self);
  if nForm='44' Then Sobo44.Button007Click(Self);
  if nForm='45' Then Sobo45.Button007Click(Self);
  if nForm='46' Then Sobo46.Button007Click(Self);
  if nForm='47' Then Sobo47.Button007Click(Self);
  if nForm='48' Then Sobo48.Button007Click(Self);
  if nForm='49' Then Sobo49.Button007Click(Self);
  if nForm='40' Then Sobo40.Button007Click(Self);

  if nForm='51' Then Sobo51.Button007Click(Self);
  if nForm='52' Then Sobo52.Button007Click(Self);
  if nForm='53' Then Sobo53.Button007Click(Self);
  if nForm='54' Then Sobo54.Button007Click(Self);
  if nForm='55' Then Sobo55.Button007Click(Self);
  if nForm='56' Then Sobo56.Button007Click(Self);
  if nForm='57' Then Sobo57.Button007Click(Self);
  if nForm='58' Then Sobo58.Button007Click(Self);
  if nForm='59' Then Sobo59.Button007Click(Self);
  if nForm='50' Then Sobo50.Button007Click(Self);

  if nForm='61' Then Sobo61.Button007Click(Self);
  if nForm='62' Then Sobo62.Button007Click(Self);
  if nForm='63' Then Sobo63.Button007Click(Self);
  if nForm='64' Then Sobo64.Button007Click(Self);
  if nForm='65' Then Sobo65.Button007Click(Self);
  if nForm='66' Then Sobo66.Button007Click(Self);
  if nForm='67' Then Sobo67.Button007Click(Self);
  if nForm='68' Then Sobo68.Button007Click(Self);
  if nForm='69' Then Sobo69.Button007Click(Self);
  if nForm='60' Then Sobo60.Button007Click(Self);
end;

procedure TSubu00.ToolButton08Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button008Click(Self);
  if nForm='12' Then Sobo12.Button008Click(Self);
  if nForm='13' Then Sobo13.Button008Click(Self);
  if nForm='14' Then Sobo14.Button008Click(Self);
  if nForm='15' Then Sobo15.Button008Click(Self);
  if nForm='16' Then Sobo16.Button008Click(Self);
  if nForm='17' Then Sobo17.Button008Click(Self);
  if nForm='18' Then Sobo18.Button008Click(Self);
  if nForm='19' Then Sobo19.Button008Click(Self);
  if nForm='10' Then Sobo10.Button008Click(Self);

  if nForm='21' Then Sobo21.Button008Click(Self);
  if nForm='22' Then Sobo22.Button008Click(Self);
  if nForm='23' Then Sobo23.Button008Click(Self);
  if nForm='24' Then Sobo24.Button008Click(Self);
  if nForm='25' Then Sobo25.Button008Click(Self);
  if nForm='26' Then Sobo26.Button008Click(Self);
  if nForm='27' Then Sobo27.Button008Click(Self);
  if nForm='28' Then Sobo28.Button008Click(Self);
  if nForm='29' Then Sobo29.Button008Click(Self);
  if nForm='20' Then Sobo20.Button008Click(Self);

  if nForm='31' Then Sobo31.Button008Click(Self);
  if nForm='32' Then Sobo32.Button008Click(Self);
  if nForm='33' Then Sobo33.Button008Click(Self);
  if nForm='34' Then Sobo34.Button008Click(Self);
  if nForm='35' Then Sobo35.Button008Click(Self);
  if nForm='36' Then Sobo36.Button008Click(Self);
  if nForm='37' Then Sobo37.Button008Click(Self);
  if nForm='38' Then Sobo38.Button008Click(Self);
  if nForm='39' Then Sobo39.Button008Click(Self);
  if nForm='30' Then Sobo30.Button008Click(Self);

  if nForm='41' Then Sobo41.Button008Click(Self);
  if nForm='42' Then Sobo42.Button008Click(Self);
  if nForm='43' Then Sobo43.Button008Click(Self);
  if nForm='44' Then Sobo44.Button008Click(Self);
  if nForm='45' Then Sobo45.Button008Click(Self);
  if nForm='46' Then Sobo46.Button008Click(Self);
  if nForm='47' Then Sobo47.Button008Click(Self);
  if nForm='48' Then Sobo48.Button008Click(Self);
  if nForm='49' Then Sobo49.Button008Click(Self);
  if nForm='40' Then Sobo40.Button008Click(Self);

  if nForm='51' Then Sobo51.Button008Click(Self);
  if nForm='52' Then Sobo52.Button008Click(Self);
  if nForm='53' Then Sobo53.Button008Click(Self);
  if nForm='54' Then Sobo54.Button008Click(Self);
  if nForm='55' Then Sobo55.Button008Click(Self);
  if nForm='56' Then Sobo56.Button008Click(Self);
  if nForm='57' Then Sobo57.Button008Click(Self);
  if nForm='58' Then Sobo58.Button008Click(Self);
  if nForm='59' Then Sobo59.Button008Click(Self);
  if nForm='50' Then Sobo50.Button008Click(Self);

  if nForm='61' Then Sobo61.Button008Click(Self);
  if nForm='62' Then Sobo62.Button008Click(Self);
  if nForm='63' Then Sobo63.Button008Click(Self);
  if nForm='64' Then Sobo64.Button008Click(Self);
  if nForm='65' Then Sobo65.Button008Click(Self);
  if nForm='66' Then Sobo66.Button008Click(Self);
  if nForm='67' Then Sobo67.Button008Click(Self);
  if nForm='68' Then Sobo68.Button008Click(Self);
  if nForm='69' Then Sobo69.Button008Click(Self);
  if nForm='60' Then Sobo60.Button008Click(Self);
end;

procedure TSubu00.ToolButton09Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button009Click(Self);
  if nForm='12' Then Sobo12.Button009Click(Self);
  if nForm='13' Then Sobo13.Button009Click(Self);
  if nForm='14' Then Sobo14.Button009Click(Self);
  if nForm='15' Then Sobo15.Button009Click(Self);
  if nForm='16' Then Sobo16.Button009Click(Self);
  if nForm='17' Then Sobo17.Button009Click(Self);
  if nForm='18' Then Sobo18.Button009Click(Self);
  if nForm='19' Then Sobo19.Button009Click(Self);
  if nForm='10' Then Sobo10.Button009Click(Self);

  if nForm='21' Then Sobo21.Button009Click(Self);
  if nForm='22' Then Sobo22.Button009Click(Self);
  if nForm='23' Then Sobo23.Button009Click(Self);
  if nForm='24' Then Sobo24.Button009Click(Self);
  if nForm='25' Then Sobo25.Button009Click(Self);
  if nForm='26' Then Sobo26.Button009Click(Self);
  if nForm='27' Then Sobo27.Button009Click(Self);
  if nForm='28' Then Sobo28.Button009Click(Self);
  if nForm='29' Then Sobo29.Button009Click(Self);
  if nForm='20' Then Sobo20.Button009Click(Self);

  if nForm='31' Then Sobo31.Button009Click(Self);
  if nForm='32' Then Sobo32.Button009Click(Self);
  if nForm='33' Then Sobo33.Button009Click(Self);
  if nForm='34' Then Sobo34.Button009Click(Self);
  if nForm='35' Then Sobo35.Button009Click(Self);
  if nForm='36' Then Sobo36.Button009Click(Self);
  if nForm='37' Then Sobo37.Button009Click(Self);
  if nForm='38' Then Sobo38.Button009Click(Self);
  if nForm='39' Then Sobo39.Button009Click(Self);
  if nForm='30' Then Sobo30.Button009Click(Self);

  if nForm='41' Then Sobo41.Button009Click(Self);
  if nForm='42' Then Sobo42.Button009Click(Self);
  if nForm='43' Then Sobo43.Button009Click(Self);
  if nForm='44' Then Sobo44.Button009Click(Self);
  if nForm='45' Then Sobo45.Button009Click(Self);
  if nForm='46' Then Sobo46.Button009Click(Self);
  if nForm='47' Then Sobo47.Button009Click(Self);
  if nForm='48' Then Sobo48.Button009Click(Self);
  if nForm='49' Then Sobo49.Button009Click(Self);
  if nForm='40' Then Sobo40.Button009Click(Self);

  if nForm='51' Then Sobo51.Button009Click(Self);
  if nForm='52' Then Sobo52.Button009Click(Self);
  if nForm='53' Then Sobo53.Button009Click(Self);
  if nForm='54' Then Sobo54.Button009Click(Self);
  if nForm='55' Then Sobo55.Button009Click(Self);
  if nForm='56' Then Sobo56.Button009Click(Self);
  if nForm='57' Then Sobo57.Button009Click(Self);
  if nForm='58' Then Sobo58.Button009Click(Self);
  if nForm='59' Then Sobo59.Button009Click(Self);
  if nForm='50' Then Sobo50.Button009Click(Self);

  if nForm='61' Then Sobo61.Button009Click(Self);
  if nForm='62' Then Sobo62.Button009Click(Self);
  if nForm='63' Then Sobo63.Button009Click(Self);
  if nForm='64' Then Sobo64.Button009Click(Self);
  if nForm='65' Then Sobo65.Button009Click(Self);
  if nForm='66' Then Sobo66.Button009Click(Self);
  if nForm='67' Then Sobo67.Button009Click(Self);
  if nForm='68' Then Sobo68.Button009Click(Self);
  if nForm='69' Then Sobo69.Button009Click(Self);
  if nForm='60' Then Sobo60.Button009Click(Self);
end;

procedure TSubu00.ToolButton10Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button010Click(Self);
  if nForm='12' Then Sobo12.Button010Click(Self);
  if nForm='13' Then Sobo13.Button010Click(Self);
  if nForm='14' Then Sobo14.Button010Click(Self);
  if nForm='15' Then Sobo15.Button010Click(Self);
  if nForm='16' Then Sobo16.Button010Click(Self);
  if nForm='17' Then Sobo17.Button010Click(Self);
  if nForm='18' Then Sobo18.Button010Click(Self);
  if nForm='19' Then Sobo19.Button010Click(Self);
  if nForm='10' Then Sobo10.Button010Click(Self);

  if nForm='21' Then Sobo21.Button010Click(Self);
  if nForm='22' Then Sobo22.Button010Click(Self);
  if nForm='23' Then Sobo23.Button010Click(Self);
  if nForm='24' Then Sobo24.Button010Click(Self);
  if nForm='25' Then Sobo25.Button010Click(Self);
  if nForm='26' Then Sobo26.Button010Click(Self);
  if nForm='27' Then Sobo27.Button010Click(Self);
  if nForm='28' Then Sobo28.Button010Click(Self);
  if nForm='29' Then Sobo29.Button010Click(Self);
  if nForm='20' Then Sobo20.Button010Click(Self);

  if nForm='31' Then Sobo31.Button010Click(Self);
  if nForm='32' Then Sobo32.Button010Click(Self);
  if nForm='33' Then Sobo33.Button010Click(Self);
  if nForm='34' Then Sobo34.Button010Click(Self);
  if nForm='35' Then Sobo35.Button010Click(Self);
  if nForm='36' Then Sobo36.Button010Click(Self);
  if nForm='37' Then Sobo37.Button010Click(Self);
  if nForm='38' Then Sobo38.Button010Click(Self);
  if nForm='39' Then Sobo39.Button010Click(Self);
  if nForm='30' Then Sobo30.Button010Click(Self);

  if nForm='41' Then Sobo41.Button010Click(Self);
  if nForm='42' Then Sobo42.Button010Click(Self);
  if nForm='43' Then Sobo43.Button010Click(Self);
  if nForm='44' Then Sobo44.Button010Click(Self);
  if nForm='45' Then Sobo45.Button010Click(Self);
  if nForm='46' Then Sobo46.Button010Click(Self);
  if nForm='47' Then Sobo47.Button010Click(Self);
  if nForm='48' Then Sobo48.Button010Click(Self);
  if nForm='49' Then Sobo49.Button010Click(Self);
  if nForm='40' Then Sobo40.Button010Click(Self);

  if nForm='51' Then Sobo51.Button010Click(Self);
  if nForm='52' Then Sobo52.Button010Click(Self);
  if nForm='53' Then Sobo53.Button010Click(Self);
  if nForm='54' Then Sobo54.Button010Click(Self);
  if nForm='55' Then Sobo55.Button010Click(Self);
  if nForm='56' Then Sobo56.Button010Click(Self);
  if nForm='57' Then Sobo57.Button010Click(Self);
  if nForm='58' Then Sobo58.Button010Click(Self);
  if nForm='59' Then Sobo59.Button010Click(Self);
  if nForm='50' Then Sobo50.Button010Click(Self);

  if nForm='61' Then Sobo61.Button010Click(Self);
  if nForm='62' Then Sobo62.Button010Click(Self);
  if nForm='63' Then Sobo63.Button010Click(Self);
  if nForm='64' Then Sobo64.Button010Click(Self);
  if nForm='65' Then Sobo65.Button010Click(Self);
  if nForm='66' Then Sobo66.Button010Click(Self);
  if nForm='67' Then Sobo67.Button010Click(Self);
  if nForm='68' Then Sobo68.Button010Click(Self);
  if nForm='69' Then Sobo69.Button010Click(Self);
  if nForm='60' Then Sobo60.Button010Click(Self);
end;

procedure TSubu00.ToolButton11Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button011Click(Self);
  if nForm='12' Then Sobo12.Button011Click(Self);
  if nForm='13' Then Sobo13.Button011Click(Self);
  if nForm='14' Then Sobo14.Button011Click(Self);
  if nForm='15' Then Sobo15.Button011Click(Self);
  if nForm='16' Then Sobo16.Button011Click(Self);
  if nForm='17' Then Sobo17.Button011Click(Self);
  if nForm='18' Then Sobo18.Button011Click(Self);
  if nForm='19' Then Sobo19.Button011Click(Self);
  if nForm='10' Then Sobo10.Button011Click(Self);

  if nForm='21' Then Sobo21.Button011Click(Self);
  if nForm='22' Then Sobo22.Button011Click(Self);
  if nForm='23' Then Sobo23.Button011Click(Self);
  if nForm='24' Then Sobo24.Button011Click(Self);
  if nForm='25' Then Sobo25.Button011Click(Self);
  if nForm='26' Then Sobo26.Button011Click(Self);
  if nForm='27' Then Sobo27.Button011Click(Self);
  if nForm='28' Then Sobo28.Button011Click(Self);
  if nForm='29' Then Sobo29.Button011Click(Self);
  if nForm='20' Then Sobo20.Button011Click(Self);

  if nForm='31' Then Sobo31.Button011Click(Self);
  if nForm='32' Then Sobo32.Button011Click(Self);
  if nForm='33' Then Sobo33.Button011Click(Self);
  if nForm='34' Then Sobo34.Button011Click(Self);
  if nForm='35' Then Sobo35.Button011Click(Self);
  if nForm='36' Then Sobo36.Button011Click(Self);
  if nForm='37' Then Sobo37.Button011Click(Self);
  if nForm='38' Then Sobo38.Button011Click(Self);
  if nForm='39' Then Sobo39.Button011Click(Self);
  if nForm='30' Then Sobo30.Button011Click(Self);

  if nForm='41' Then Sobo41.Button011Click(Self);
  if nForm='42' Then Sobo42.Button011Click(Self);
  if nForm='43' Then Sobo43.Button011Click(Self);
  if nForm='44' Then Sobo44.Button011Click(Self);
  if nForm='45' Then Sobo45.Button011Click(Self);
  if nForm='46' Then Sobo46.Button011Click(Self);
  if nForm='47' Then Sobo47.Button011Click(Self);
  if nForm='48' Then Sobo48.Button011Click(Self);
  if nForm='49' Then Sobo49.Button011Click(Self);
  if nForm='40' Then Sobo40.Button011Click(Self);

  if nForm='51' Then Sobo51.Button011Click(Self);
  if nForm='52' Then Sobo52.Button011Click(Self);
  if nForm='53' Then Sobo53.Button011Click(Self);
  if nForm='54' Then Sobo54.Button011Click(Self);
  if nForm='55' Then Sobo55.Button011Click(Self);
  if nForm='56' Then Sobo56.Button011Click(Self);
  if nForm='57' Then Sobo57.Button011Click(Self);
  if nForm='58' Then Sobo58.Button011Click(Self);
  if nForm='59' Then Sobo59.Button011Click(Self);
  if nForm='50' Then Sobo50.Button011Click(Self);

  if nForm='61' Then Sobo61.Button011Click(Self);
  if nForm='62' Then Sobo62.Button011Click(Self);
  if nForm='63' Then Sobo63.Button011Click(Self);
  if nForm='64' Then Sobo64.Button011Click(Self);
  if nForm='65' Then Sobo65.Button011Click(Self);
  if nForm='66' Then Sobo66.Button011Click(Self);
  if nForm='67' Then Sobo67.Button011Click(Self);
  if nForm='68' Then Sobo68.Button011Click(Self);
  if nForm='69' Then Sobo69.Button011Click(Self);
  if nForm='60' Then Sobo60.Button011Click(Self);
end;

procedure TSubu00.ToolButton12Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button012Click(Self);
  if nForm='12' Then Sobo12.Button012Click(Self);
  if nForm='13' Then Sobo13.Button012Click(Self);
  if nForm='14' Then Sobo14.Button012Click(Self);
  if nForm='15' Then Sobo15.Button012Click(Self);
  if nForm='16' Then Sobo16.Button012Click(Self);
  if nForm='17' Then Sobo17.Button012Click(Self);
  if nForm='18' Then Sobo18.Button012Click(Self);
  if nForm='19' Then Sobo19.Button012Click(Self);
  if nForm='10' Then Sobo10.Button012Click(Self);

  if nForm='21' Then Sobo21.Button012Click(Self);
  if nForm='22' Then Sobo22.Button012Click(Self);
  if nForm='23' Then Sobo23.Button012Click(Self);
  if nForm='24' Then Sobo24.Button012Click(Self);
  if nForm='25' Then Sobo25.Button012Click(Self);
  if nForm='26' Then Sobo26.Button012Click(Self);
  if nForm='27' Then Sobo27.Button012Click(Self);
  if nForm='28' Then Sobo28.Button012Click(Self);
  if nForm='29' Then Sobo29.Button012Click(Self);
  if nForm='20' Then Sobo20.Button012Click(Self);

  if nForm='31' Then Sobo31.Button012Click(Self);
  if nForm='32' Then Sobo32.Button012Click(Self);
  if nForm='33' Then Sobo33.Button012Click(Self);
  if nForm='34' Then Sobo34.Button012Click(Self);
  if nForm='35' Then Sobo35.Button012Click(Self);
  if nForm='36' Then Sobo36.Button012Click(Self);
  if nForm='37' Then Sobo37.Button012Click(Self);
  if nForm='38' Then Sobo38.Button012Click(Self);
  if nForm='39' Then Sobo39.Button012Click(Self);
  if nForm='30' Then Sobo30.Button012Click(Self);

  if nForm='41' Then Sobo41.Button012Click(Self);
  if nForm='42' Then Sobo42.Button012Click(Self);
  if nForm='43' Then Sobo43.Button012Click(Self);
  if nForm='44' Then Sobo44.Button012Click(Self);
  if nForm='45' Then Sobo45.Button012Click(Self);
  if nForm='46' Then Sobo46.Button012Click(Self);
  if nForm='47' Then Sobo47.Button012Click(Self);
  if nForm='48' Then Sobo48.Button012Click(Self);
  if nForm='49' Then Sobo49.Button012Click(Self);
  if nForm='40' Then Sobo40.Button012Click(Self);

  if nForm='51' Then Sobo51.Button012Click(Self);
  if nForm='52' Then Sobo52.Button012Click(Self);
  if nForm='53' Then Sobo53.Button012Click(Self);
  if nForm='54' Then Sobo54.Button012Click(Self);
  if nForm='55' Then Sobo55.Button012Click(Self);
  if nForm='56' Then Sobo56.Button012Click(Self);
  if nForm='57' Then Sobo57.Button012Click(Self);
  if nForm='58' Then Sobo58.Button012Click(Self);
  if nForm='59' Then Sobo59.Button012Click(Self);
  if nForm='50' Then Sobo50.Button012Click(Self);

  if nForm='61' Then Sobo61.Button012Click(Self);
  if nForm='62' Then Sobo62.Button012Click(Self);
  if nForm='63' Then Sobo63.Button012Click(Self);
  if nForm='64' Then Sobo64.Button012Click(Self);
  if nForm='65' Then Sobo65.Button012Click(Self);
  if nForm='66' Then Sobo66.Button012Click(Self);
  if nForm='67' Then Sobo67.Button012Click(Self);
  if nForm='68' Then Sobo68.Button012Click(Self);
  if nForm='69' Then Sobo69.Button012Click(Self);
  if nForm='60' Then Sobo60.Button012Click(Self);
end;

procedure TSubu00.ToolButton13Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button013Click(Self);
  if nForm='12' Then Sobo12.Button013Click(Self);
  if nForm='13' Then Sobo13.Button013Click(Self);
  if nForm='14' Then Sobo14.Button013Click(Self);
  if nForm='15' Then Sobo15.Button013Click(Self);
  if nForm='16' Then Sobo16.Button013Click(Self);
  if nForm='17' Then Sobo17.Button013Click(Self);
  if nForm='18' Then Sobo18.Button013Click(Self);
  if nForm='19' Then Sobo19.Button013Click(Self);
  if nForm='10' Then Sobo10.Button013Click(Self);

  if nForm='21' Then Sobo21.Button013Click(Self);
  if nForm='22' Then Sobo22.Button013Click(Self);
  if nForm='23' Then Sobo23.Button013Click(Self);
  if nForm='24' Then Sobo24.Button013Click(Self);
  if nForm='25' Then Sobo25.Button013Click(Self);
  if nForm='26' Then Sobo26.Button013Click(Self);
  if nForm='27' Then Sobo27.Button013Click(Self);
  if nForm='28' Then Sobo28.Button013Click(Self);
  if nForm='29' Then Sobo29.Button013Click(Self);
  if nForm='20' Then Sobo20.Button013Click(Self);

  if nForm='31' Then Sobo31.Button013Click(Self);
  if nForm='32' Then Sobo32.Button013Click(Self);
  if nForm='33' Then Sobo33.Button013Click(Self);
  if nForm='34' Then Sobo34.Button013Click(Self);
  if nForm='35' Then Sobo35.Button013Click(Self);
  if nForm='36' Then Sobo36.Button013Click(Self);
  if nForm='37' Then Sobo37.Button013Click(Self);
  if nForm='38' Then Sobo38.Button013Click(Self);
  if nForm='39' Then Sobo39.Button013Click(Self);
  if nForm='30' Then Sobo30.Button013Click(Self);

  if nForm='41' Then Sobo41.Button013Click(Self);
  if nForm='42' Then Sobo42.Button013Click(Self);
  if nForm='43' Then Sobo43.Button013Click(Self);
  if nForm='44' Then Sobo44.Button013Click(Self);
  if nForm='45' Then Sobo45.Button013Click(Self);
  if nForm='46' Then Sobo46.Button013Click(Self);
  if nForm='47' Then Sobo47.Button013Click(Self);
  if nForm='48' Then Sobo48.Button013Click(Self);
  if nForm='49' Then Sobo49.Button013Click(Self);
  if nForm='40' Then Sobo40.Button013Click(Self);

  if nForm='51' Then Sobo51.Button013Click(Self);
  if nForm='52' Then Sobo52.Button013Click(Self);
  if nForm='53' Then Sobo53.Button013Click(Self);
  if nForm='54' Then Sobo54.Button013Click(Self);
  if nForm='55' Then Sobo55.Button013Click(Self);
  if nForm='56' Then Sobo56.Button013Click(Self);
  if nForm='57' Then Sobo57.Button013Click(Self);
  if nForm='58' Then Sobo58.Button013Click(Self);
  if nForm='59' Then Sobo59.Button013Click(Self);
  if nForm='50' Then Sobo50.Button013Click(Self);

  if nForm='61' Then Sobo61.Button013Click(Self);
  if nForm='62' Then Sobo62.Button013Click(Self);
  if nForm='63' Then Sobo63.Button013Click(Self);
  if nForm='64' Then Sobo64.Button013Click(Self);
  if nForm='65' Then Sobo65.Button013Click(Self);
  if nForm='66' Then Sobo66.Button013Click(Self);
  if nForm='67' Then Sobo67.Button013Click(Self);
  if nForm='68' Then Sobo68.Button013Click(Self);
  if nForm='69' Then Sobo69.Button013Click(Self);
  if nForm='60' Then Sobo60.Button013Click(Self);
end;

procedure TSubu00.ToolButton14Click(Sender: TObject);
begin
{ FormActivate(Self);
  if nForm='11' Then Sobo11.Button014Click(Self);
  if nForm='12' Then Sobo12.Button014Click(Self);
  if nForm='13' Then Sobo13.Button014Click(Self);
  if nForm='14' Then Sobo14.Button014Click(Self);
  if nForm='15' Then Sobo15.Button014Click(Self);
  if nForm='16' Then Sobo16.Button014Click(Self);
  if nForm='17' Then Sobo17.Button014Click(Self);
  if nForm='18' Then Sobo18.Button014Click(Self);
  if nForm='19' Then Sobo19.Button014Click(Self);
  if nForm='10' Then Sobo10.Button014Click(Self);

  if nForm='21' Then Sobo21.Button014Click(Self);
  if nForm='22' Then Sobo22.Button014Click(Self);
  if nForm='23' Then Sobo23.Button014Click(Self);
  if nForm='24' Then Sobo24.Button014Click(Self);
  if nForm='25' Then Sobo25.Button014Click(Self);
  if nForm='26' Then Sobo26.Button014Click(Self);
  if nForm='27' Then Sobo27.Button014Click(Self);
  if nForm='28' Then Sobo28.Button014Click(Self);
  if nForm='29' Then Sobo29.Button014Click(Self);
  if nForm='20' Then Sobo20.Button014Click(Self);

  if nForm='31' Then Sobo31.Button014Click(Self);
  if nForm='32' Then Sobo32.Button014Click(Self);
  if nForm='33' Then Sobo33.Button014Click(Self);
  if nForm='34' Then Sobo34.Button014Click(Self);
  if nForm='35' Then Sobo35.Button014Click(Self);
  if nForm='36' Then Sobo36.Button014Click(Self);
  if nForm='37' Then Sobo37.Button014Click(Self);
  if nForm='38' Then Sobo38.Button014Click(Self);
  if nForm='39' Then Sobo39.Button014Click(Self);
  if nForm='30' Then Sobo30.Button014Click(Self);

  if nForm='41' Then Sobo41.Button014Click(Self);
  if nForm='42' Then Sobo42.Button014Click(Self);
  if nForm='43' Then Sobo43.Button014Click(Self);
  if nForm='44' Then Sobo44.Button014Click(Self);
  if nForm='45' Then Sobo45.Button014Click(Self);
  if nForm='46' Then Sobo46.Button014Click(Self);
  if nForm='47' Then Sobo47.Button014Click(Self);
  if nForm='48' Then Sobo48.Button014Click(Self);
  if nForm='49' Then Sobo49.Button014Click(Self);
  if nForm='40' Then Sobo40.Button014Click(Self);

  if nForm='51' Then Sobo51.Button014Click(Self);
  if nForm='52' Then Sobo52.Button014Click(Self);
  if nForm='53' Then Sobo53.Button014Click(Self);
  if nForm='54' Then Sobo54.Button014Click(Self);
  if nForm='55' Then Sobo55.Button014Click(Self);
  if nForm='56' Then Sobo56.Button014Click(Self);
  if nForm='57' Then Sobo57.Button014Click(Self);
  if nForm='58' Then Sobo58.Button014Click(Self);
  if nForm='59' Then Sobo59.Button014Click(Self);
  if nForm='50' Then Sobo50.Button014Click(Self);

  if nForm='61' Then Sobo61.Button014Click(Self);
  if nForm='62' Then Sobo62.Button014Click(Self);
  if nForm='63' Then Sobo63.Button014Click(Self);
  if nForm='64' Then Sobo64.Button014Click(Self);
  if nForm='65' Then Sobo65.Button014Click(Self);
  if nForm='66' Then Sobo66.Button014Click(Self);
  if nForm='67' Then Sobo67.Button014Click(Self);
  if nForm='68' Then Sobo68.Button014Click(Self);
  if nForm='69' Then Sobo69.Button014Click(Self);
  if nForm='60' Then Sobo60.Button014Click(Self); }
end;

procedure TSubu00.ToolButton15Click(Sender: TObject);
begin
{ FormActivate(Self);
  if nForm='11' Then Sobo11.Button015Click(Self);
  if nForm='12' Then Sobo12.Button015Click(Self);
  if nForm='13' Then Sobo13.Button015Click(Self);
  if nForm='14' Then Sobo14.Button015Click(Self);
  if nForm='15' Then Sobo15.Button015Click(Self);
  if nForm='16' Then Sobo16.Button015Click(Self);
  if nForm='17' Then Sobo17.Button015Click(Self);
  if nForm='18' Then Sobo18.Button015Click(Self);
  if nForm='19' Then Sobo19.Button015Click(Self);
  if nForm='10' Then Sobo10.Button015Click(Self);

  if nForm='21' Then Sobo21.Button015Click(Self);
  if nForm='22' Then Sobo22.Button015Click(Self);
  if nForm='23' Then Sobo23.Button015Click(Self);
  if nForm='24' Then Sobo24.Button015Click(Self);
  if nForm='25' Then Sobo25.Button015Click(Self);
  if nForm='26' Then Sobo26.Button015Click(Self);
  if nForm='27' Then Sobo27.Button015Click(Self);
  if nForm='28' Then Sobo28.Button015Click(Self);
  if nForm='29' Then Sobo29.Button015Click(Self);
  if nForm='20' Then Sobo20.Button015Click(Self);

  if nForm='31' Then Sobo31.Button015Click(Self);
  if nForm='32' Then Sobo32.Button015Click(Self);
  if nForm='33' Then Sobo33.Button015Click(Self);
  if nForm='34' Then Sobo34.Button015Click(Self);
  if nForm='35' Then Sobo35.Button015Click(Self);
  if nForm='36' Then Sobo36.Button015Click(Self);
  if nForm='37' Then Sobo37.Button015Click(Self);
  if nForm='38' Then Sobo38.Button015Click(Self);
  if nForm='39' Then Sobo39.Button015Click(Self);
  if nForm='30' Then Sobo30.Button015Click(Self);

  if nForm='41' Then Sobo41.Button015Click(Self);
  if nForm='42' Then Sobo42.Button015Click(Self);
  if nForm='43' Then Sobo43.Button015Click(Self);
  if nForm='44' Then Sobo44.Button015Click(Self);
  if nForm='45' Then Sobo45.Button015Click(Self);
  if nForm='46' Then Sobo46.Button015Click(Self);
  if nForm='47' Then Sobo47.Button015Click(Self);
  if nForm='48' Then Sobo48.Button015Click(Self);
  if nForm='49' Then Sobo49.Button015Click(Self);
  if nForm='40' Then Sobo40.Button015Click(Self);

  if nForm='51' Then Sobo51.Button015Click(Self);
  if nForm='52' Then Sobo52.Button015Click(Self);
  if nForm='53' Then Sobo53.Button015Click(Self);
  if nForm='54' Then Sobo54.Button015Click(Self);
  if nForm='55' Then Sobo55.Button015Click(Self);
  if nForm='56' Then Sobo56.Button015Click(Self);
  if nForm='57' Then Sobo57.Button015Click(Self);
  if nForm='58' Then Sobo58.Button015Click(Self);
  if nForm='59' Then Sobo59.Button015Click(Self);
  if nForm='50' Then Sobo50.Button015Click(Self);

  if nForm='61' Then Sobo61.Button015Click(Self);
  if nForm='62' Then Sobo62.Button015Click(Self);
  if nForm='63' Then Sobo63.Button015Click(Self);
  if nForm='64' Then Sobo64.Button015Click(Self);
  if nForm='65' Then Sobo65.Button015Click(Self);
  if nForm='66' Then Sobo66.Button015Click(Self);
  if nForm='67' Then Sobo67.Button015Click(Self);
  if nForm='68' Then Sobo68.Button015Click(Self);
  if nForm='69' Then Sobo69.Button015Click(Self);
  if nForm='60' Then Sobo60.Button015Click(Self); }
end;

procedure TSubu00.ToolButton16Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button016Click(Self);
  if nForm='12' Then Sobo12.Button016Click(Self);
  if nForm='13' Then Sobo13.Button016Click(Self);
  if nForm='14' Then Sobo14.Button016Click(Self);
  if nForm='15' Then Sobo15.Button016Click(Self);
  if nForm='16' Then Sobo16.Button016Click(Self);
  if nForm='17' Then Sobo17.Button016Click(Self);
  if nForm='18' Then Sobo18.Button016Click(Self);
  if nForm='19' Then Sobo19.Button016Click(Self);
  if nForm='10' Then Sobo10.Button016Click(Self);

  if nForm='21' Then Sobo21.Button016Click(Self);
  if nForm='22' Then Sobo22.Button016Click(Self);
  if nForm='23' Then Sobo23.Button016Click(Self);
  if nForm='24' Then Sobo24.Button016Click(Self);
  if nForm='25' Then Sobo25.Button016Click(Self);
  if nForm='26' Then Sobo26.Button016Click(Self);
  if nForm='27' Then Sobo27.Button016Click(Self);
  if nForm='28' Then Sobo28.Button016Click(Self);
  if nForm='29' Then Sobo29.Button016Click(Self);
  if nForm='20' Then Sobo20.Button016Click(Self);

  if nForm='31' Then Sobo31.Button016Click(Self);
  if nForm='32' Then Sobo32.Button016Click(Self);
  if nForm='33' Then Sobo33.Button016Click(Self);
  if nForm='34' Then Sobo34.Button016Click(Self);
  if nForm='35' Then Sobo35.Button016Click(Self);
  if nForm='36' Then Sobo36.Button016Click(Self);
  if nForm='37' Then Sobo37.Button016Click(Self);
  if nForm='38' Then Sobo38.Button016Click(Self);
  if nForm='39' Then Sobo39.Button016Click(Self);
  if nForm='30' Then Sobo30.Button016Click(Self);

  if nForm='41' Then Sobo41.Button016Click(Self);
  if nForm='42' Then Sobo42.Button016Click(Self);
  if nForm='43' Then Sobo43.Button016Click(Self);
  if nForm='44' Then Sobo44.Button016Click(Self);
  if nForm='45' Then Sobo45.Button016Click(Self);
  if nForm='46' Then Sobo46.Button016Click(Self);
  if nForm='47' Then Sobo47.Button016Click(Self);
  if nForm='48' Then Sobo48.Button016Click(Self);
  if nForm='49' Then Sobo49.Button016Click(Self);
  if nForm='40' Then Sobo40.Button016Click(Self);

  if nForm='51' Then Sobo51.Button016Click(Self);
  if nForm='52' Then Sobo52.Button016Click(Self);
  if nForm='53' Then Sobo53.Button016Click(Self);
  if nForm='54' Then Sobo54.Button016Click(Self);
  if nForm='55' Then Sobo55.Button016Click(Self);
  if nForm='56' Then Sobo56.Button016Click(Self);
  if nForm='57' Then Sobo57.Button016Click(Self);
  if nForm='58' Then Sobo58.Button016Click(Self);
  if nForm='59' Then Sobo59.Button016Click(Self);
  if nForm='50' Then Sobo50.Button016Click(Self);

  if nForm='61' Then Sobo61.Button016Click(Self);
  if nForm='62' Then Sobo62.Button016Click(Self);
  if nForm='63' Then Sobo63.Button016Click(Self);
  if nForm='64' Then Sobo64.Button016Click(Self);
  if nForm='65' Then Sobo65.Button016Click(Self);
  if nForm='66' Then Sobo66.Button016Click(Self);
  if nForm='67' Then Sobo67.Button016Click(Self);
  if nForm='68' Then Sobo68.Button016Click(Self);
  if nForm='69' Then Sobo69.Button016Click(Self);
  if nForm='60' Then Sobo60.Button016Click(Self);
end;

procedure TSubu00.ToolButton17Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button017Click(Self);
  if nForm='12' Then Sobo12.Button017Click(Self);
  if nForm='13' Then Sobo13.Button017Click(Self);
  if nForm='14' Then Sobo14.Button017Click(Self);
  if nForm='15' Then Sobo15.Button017Click(Self);
  if nForm='16' Then Sobo16.Button017Click(Self);
  if nForm='17' Then Sobo17.Button017Click(Self);
  if nForm='18' Then Sobo18.Button017Click(Self);
  if nForm='19' Then Sobo19.Button017Click(Self);
  if nForm='10' Then Sobo10.Button017Click(Self);

  if nForm='21' Then Sobo21.Button017Click(Self);
  if nForm='22' Then Sobo22.Button017Click(Self);
  if nForm='23' Then Sobo23.Button017Click(Self);
  if nForm='24' Then Sobo24.Button017Click(Self);
  if nForm='25' Then Sobo25.Button017Click(Self);
  if nForm='26' Then Sobo26.Button017Click(Self);
  if nForm='27' Then Sobo27.Button017Click(Self);
  if nForm='28' Then Sobo28.Button017Click(Self);
  if nForm='29' Then Sobo29.Button017Click(Self);
  if nForm='20' Then Sobo20.Button017Click(Self);

  if nForm='31' Then Sobo31.Button017Click(Self);
  if nForm='32' Then Sobo32.Button017Click(Self);
  if nForm='33' Then Sobo33.Button017Click(Self);
  if nForm='34' Then Sobo34.Button017Click(Self);
  if nForm='35' Then Sobo35.Button017Click(Self);
  if nForm='36' Then Sobo36.Button017Click(Self);
  if nForm='37' Then Sobo37.Button017Click(Self);
  if nForm='38' Then Sobo38.Button017Click(Self);
  if nForm='39' Then Sobo39.Button017Click(Self);
  if nForm='30' Then Sobo30.Button017Click(Self);

  if nForm='41' Then Sobo41.Button017Click(Self);
  if nForm='42' Then Sobo42.Button017Click(Self);
  if nForm='43' Then Sobo43.Button017Click(Self);
  if nForm='44' Then Sobo44.Button017Click(Self);
  if nForm='45' Then Sobo45.Button017Click(Self);
  if nForm='46' Then Sobo46.Button017Click(Self);
  if nForm='47' Then Sobo47.Button017Click(Self);
  if nForm='48' Then Sobo48.Button017Click(Self);
  if nForm='49' Then Sobo49.Button017Click(Self);
  if nForm='40' Then Sobo40.Button017Click(Self);

  if nForm='51' Then Sobo51.Button017Click(Self);
  if nForm='52' Then Sobo52.Button017Click(Self);
  if nForm='53' Then Sobo53.Button017Click(Self);
  if nForm='54' Then Sobo54.Button017Click(Self);
  if nForm='55' Then Sobo55.Button017Click(Self);
  if nForm='56' Then Sobo56.Button017Click(Self);
  if nForm='57' Then Sobo57.Button017Click(Self);
  if nForm='58' Then Sobo58.Button017Click(Self);
  if nForm='59' Then Sobo59.Button017Click(Self);
  if nForm='50' Then Sobo50.Button017Click(Self);

  if nForm='61' Then Sobo61.Button017Click(Self);
  if nForm='62' Then Sobo62.Button017Click(Self);
  if nForm='63' Then Sobo63.Button017Click(Self);
  if nForm='64' Then Sobo64.Button017Click(Self);
  if nForm='65' Then Sobo65.Button017Click(Self);
  if nForm='66' Then Sobo66.Button017Click(Self);
  if nForm='67' Then Sobo67.Button017Click(Self);
  if nForm='68' Then Sobo68.Button017Click(Self);
  if nForm='69' Then Sobo69.Button017Click(Self);
  if nForm='60' Then Sobo60.Button017Click(Self);
end;

procedure TSubu00.ToolButton18Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='21' Then Sobo21.Button018Click(Self);
  if nForm='22' Then Sobo22.Button018Click(Self);
  if nForm='23' Then Sobo23.Button018Click(Self);
  if nForm='24' Then Sobo24.Button018Click(Self);
  if nForm='25' Then Sobo25.Button018Click(Self);
  if nForm='26' Then Sobo26.Button018Click(Self);
  if nForm='27' Then Sobo27.Button018Click(Self);
  if nForm='28' Then Sobo28.Button018Click(Self);
  if nForm='29' Then Sobo29.Button018Click(Self);
  if nForm='20' Then Sobo20.Button018Click(Self);
end;

procedure TSubu00.ToolButton19Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Print;
  if nForm='12' Then Sobo12.Print;
  if nForm='13' Then Sobo13.Print;
  if nForm='14' Then Sobo14.Print;
  if nForm='15' Then Sobo15.Print;
  if nForm='16' Then Sobo16.Print;
  if nForm='17' Then Sobo17.Print;
  if nForm='18' Then Sobo18.Print;
  if nForm='19' Then Sobo19.Print;
  if nForm='10' Then Sobo10.Print;

  if nForm='21' Then Sobo21.Print;
  if nForm='22' Then Sobo22.Print;
  if nForm='23' Then Sobo23.Print;
  if nForm='24' Then Sobo24.Print;
  if nForm='25' Then Sobo25.Print;
  if nForm='26' Then Sobo26.Print;
  if nForm='27' Then Sobo27.Print;
  if nForm='28' Then Sobo28.Print;
  if nForm='29' Then Sobo29.Print;
  if nForm='20' Then Sobo20.Print;

  if nForm='31' Then Sobo31.Print;
  if nForm='32' Then Sobo32.Print;
  if nForm='33' Then Sobo33.Print;
  if nForm='34' Then Sobo34.Print;
  if nForm='35' Then Sobo35.Print;
  if nForm='36' Then Sobo36.Print;
  if nForm='37' Then Sobo37.Print;
  if nForm='38' Then Sobo38.Print;
  if nForm='39' Then Sobo39.Print;
  if nForm='30' Then Sobo30.Print;

  if nForm='41' Then Sobo41.Print;
  if nForm='42' Then Sobo42.Print;
  if nForm='43' Then Sobo43.Print;
  if nForm='44' Then Sobo44.Print;
  if nForm='45' Then Sobo45.Print;
  if nForm='46' Then Sobo46.Print;
  if nForm='47' Then Sobo47.Print;
  if nForm='48' Then Sobo48.Print;
  if nForm='49' Then Sobo49.Print;
  if nForm='40' Then Sobo40.Print;

  if nForm='51' Then Sobo51.Print;
  if nForm='52' Then Sobo52.Print;
  if nForm='53' Then Sobo53.Print;
  if nForm='54' Then Sobo54.Print;
  if nForm='55' Then Sobo55.Print;
  if nForm='56' Then Sobo56.Print;
  if nForm='57' Then Sobo57.Print;
  if nForm='58' Then Sobo58.Print;
  if nForm='59' Then Sobo59.Print;
  if nForm='50' Then Sobo50.Print;

  if nForm='61' Then Sobo61.Print;
  if nForm='62' Then Sobo62.Print;
  if nForm='63' Then Sobo63.Print;
  if nForm='64' Then Sobo64.Print;
  if nForm='65' Then Sobo65.Print;
  if nForm='66' Then Sobo66.Print;
  if nForm='67' Then Sobo67.Print;
  if nForm='68' Then Sobo68.Print;
  if nForm='69' Then Sobo69.Print;
  if nForm='60' Then Sobo60.Print;
end;

procedure TSubu00.ToolButton20Click(Sender: TObject);
var
device : array[0..255] of char;
Driver : array[0..255] of char;
Port   : array[0..255] of char;
hDeviceMode : THandle;
begin
  FormActivate(Self);
//PrinterSetupDialog1.Execute;
  if PrinterSetupDialog1.Execute then begin

     Printer.GetPrinter(Device, Driver, Port, hDeviceMode);
     StrCat(Device, ',');
     StrCat(Device, Driver);
     StrCat(Device, ',');
     StrCat(Device, Port);

     WriteProfileString('windows', 'device', Device);
     StrCopy(Device, 'windows');
     SendMessage(HWND_BROADCAST, WM_WININICHANGE,0,LongInt(@Device));
  end;
  ToolButton26Click(Self);
end;

procedure TSubu00.ToolButton21Click(Sender: TObject);
begin
  FormActivate(Self);
  if Tong40.FontDialog.Execute Then begin
  if nForm='11' Then Sobo11.Button021Click(Self);
  if nForm='12' Then Sobo12.Button021Click(Self);
  if nForm='13' Then Sobo13.Button021Click(Self);
  if nForm='14' Then Sobo14.Button021Click(Self);
  if nForm='15' Then Sobo15.Button021Click(Self);
  if nForm='16' Then Sobo16.Button021Click(Self);
  if nForm='17' Then Sobo17.Button021Click(Self);
  if nForm='18' Then Sobo18.Button021Click(Self);
  if nForm='19' Then Sobo19.Button021Click(Self);
  if nForm='10' Then Sobo10.Button021Click(Self);

  if nForm='21' Then Sobo21.Button021Click(Self);
  if nForm='22' Then Sobo22.Button021Click(Self);
  if nForm='23' Then Sobo23.Button021Click(Self);
  if nForm='24' Then Sobo24.Button021Click(Self);
  if nForm='25' Then Sobo25.Button021Click(Self);
  if nForm='26' Then Sobo26.Button021Click(Self);
  if nForm='27' Then Sobo27.Button021Click(Self);
  if nForm='28' Then Sobo28.Button021Click(Self);
  if nForm='29' Then Sobo29.Button021Click(Self);
  if nForm='20' Then Sobo20.Button021Click(Self);

  if nForm='31' Then Sobo31.Button021Click(Self);
  if nForm='32' Then Sobo32.Button021Click(Self);
  if nForm='33' Then Sobo33.Button021Click(Self);
  if nForm='34' Then Sobo34.Button021Click(Self);
  if nForm='35' Then Sobo35.Button021Click(Self);
  if nForm='36' Then Sobo36.Button021Click(Self);
  if nForm='37' Then Sobo37.Button021Click(Self);
  if nForm='38' Then Sobo38.Button021Click(Self);
  if nForm='39' Then Sobo39.Button021Click(Self);
  if nForm='30' Then Sobo30.Button021Click(Self);

  if nForm='41' Then Sobo41.Button021Click(Self);
  if nForm='42' Then Sobo42.Button021Click(Self);
  if nForm='43' Then Sobo43.Button021Click(Self);
  if nForm='44' Then Sobo44.Button021Click(Self);
  if nForm='45' Then Sobo45.Button021Click(Self);
  if nForm='46' Then Sobo46.Button021Click(Self);
  if nForm='47' Then Sobo47.Button021Click(Self);
  if nForm='48' Then Sobo48.Button021Click(Self);
  if nForm='49' Then Sobo49.Button021Click(Self);
  if nForm='40' Then Sobo40.Button021Click(Self);

  if nForm='51' Then Sobo51.Button021Click(Self);
  if nForm='52' Then Sobo52.Button021Click(Self);
  if nForm='53' Then Sobo53.Button021Click(Self);
  if nForm='54' Then Sobo54.Button021Click(Self);
  if nForm='55' Then Sobo55.Button021Click(Self);
  if nForm='56' Then Sobo56.Button021Click(Self);
  if nForm='57' Then Sobo57.Button021Click(Self);
  if nForm='58' Then Sobo58.Button021Click(Self);
  if nForm='59' Then Sobo59.Button021Click(Self);
  if nForm='50' Then Sobo50.Button021Click(Self);

  if nForm='61' Then Sobo61.Button021Click(Self);
  if nForm='62' Then Sobo62.Button021Click(Self);
  if nForm='63' Then Sobo63.Button021Click(Self);
  if nForm='64' Then Sobo64.Button021Click(Self);
  if nForm='65' Then Sobo65.Button021Click(Self);
  if nForm='66' Then Sobo66.Button021Click(Self);
  if nForm='67' Then Sobo67.Button021Click(Self);
  if nForm='68' Then Sobo68.Button021Click(Self);
  if nForm='69' Then Sobo69.Button021Click(Self);
  if nForm='60' Then Sobo60.Button021Click(Self);
  end;
end;

procedure TSubu00.ToolButton22Click(Sender: TObject);
begin
  FormActivate(Self);
  if nForm='11' Then Sobo11.Button022Click(Self);
  if nForm='12' Then Sobo12.Button022Click(Self);
  if nForm='13' Then Sobo13.Button022Click(Self);
  if nForm='14' Then Sobo14.Button022Click(Self);
  if nForm='15' Then Sobo15.Button022Click(Self);
  if nForm='16' Then Sobo16.Button022Click(Self);
  if nForm='17' Then Sobo17.Button022Click(Self);
  if nForm='18' Then Sobo18.Button022Click(Self);
  if nForm='19' Then Sobo19.Button022Click(Self);
  if nForm='10' Then Sobo10.Button022Click(Self);

  if nForm='21' Then Sobo21.Button022Click(Self);
  if nForm='22' Then Sobo22.Button022Click(Self);
  if nForm='23' Then Sobo23.Button022Click(Self);
  if nForm='24' Then Sobo24.Button022Click(Self);
  if nForm='25' Then Sobo25.Button022Click(Self);
  if nForm='26' Then Sobo26.Button022Click(Self);
  if nForm='27' Then Sobo27.Button022Click(Self);
  if nForm='28' Then Sobo28.Button022Click(Self);
  if nForm='29' Then Sobo29.Button022Click(Self);
  if nForm='20' Then Sobo20.Button022Click(Self);

  if nForm='31' Then Sobo31.Button022Click(Self);
  if nForm='32' Then Sobo32.Button022Click(Self);
  if nForm='33' Then Sobo33.Button022Click(Self);
  if nForm='34' Then Sobo34.Button022Click(Self);
  if nForm='35' Then Sobo35.Button022Click(Self);
  if nForm='36' Then Sobo36.Button022Click(Self);
  if nForm='37' Then Sobo37.Button022Click(Self);
  if nForm='38' Then Sobo38.Button022Click(Self);
  if nForm='39' Then Sobo39.Button022Click(Self);
  if nForm='30' Then Sobo30.Button022Click(Self);

  if nForm='41' Then Sobo41.Button022Click(Self);
  if nForm='42' Then Sobo42.Button022Click(Self);
  if nForm='43' Then Sobo43.Button022Click(Self);
  if nForm='44' Then Sobo44.Button022Click(Self);
  if nForm='45' Then Sobo45.Button022Click(Self);
  if nForm='46' Then Sobo46.Button022Click(Self);
  if nForm='47' Then Sobo47.Button022Click(Self);
  if nForm='48' Then Sobo48.Button022Click(Self);
  if nForm='49' Then Sobo49.Button022Click(Self);
  if nForm='40' Then Sobo40.Button022Click(Self);

  if nForm='51' Then Sobo51.Button022Click(Self);
  if nForm='52' Then Sobo52.Button022Click(Self);
  if nForm='53' Then Sobo53.Button022Click(Self);
  if nForm='54' Then Sobo54.Button022Click(Self);
  if nForm='55' Then Sobo55.Button022Click(Self);
  if nForm='56' Then Sobo56.Button022Click(Self);
  if nForm='57' Then Sobo57.Button022Click(Self);
  if nForm='58' Then Sobo58.Button022Click(Self);
  if nForm='59' Then Sobo59.Button022Click(Self);
  if nForm='50' Then Sobo50.Button022Click(Self);

  if nForm='61' Then Sobo61.Button022Click(Self);
  if nForm='62' Then Sobo62.Button022Click(Self);
  if nForm='63' Then Sobo63.Button022Click(Self);
  if nForm='64' Then Sobo64.Button022Click(Self);
  if nForm='65' Then Sobo65.Button022Click(Self);
  if nForm='66' Then Sobo66.Button022Click(Self);
  if nForm='67' Then Sobo67.Button022Click(Self);
  if nForm='68' Then Sobo68.Button022Click(Self);
  if nForm='69' Then Sobo69.Button022Click(Self);
  if nForm='60' Then Sobo60.Button022Click(Self);
end;

procedure TSubu00.ToolButton23Click(Sender: TObject);
var StrList : TStrings;
begin
  FormActivate(Self);
  StrList:=Tong20.GetIPs;
  ShowMessage('IP:'+StrList.Strings[0]);
{ ShowMessage('IP:'+StrList.Strings[1]); }
end;

procedure TSubu00.ToolButton24Click(Sender: TObject);
var
device : array[0..255] of char;
Driver : array[0..255] of char;
Port   : array[0..255] of char;
hDeviceMode : THandle;
begin
  FormActivate(Self);
//PrinterSetupDialog1.Execute;
  if PrinterSetupDialog1.Execute then begin

     Printer.GetPrinter(Device, Driver, Port, hDeviceMode);
     StrCat(Device, ',');
     StrCat(Device, Driver);
     StrCat(Device, ',');
     StrCat(Device, Port);

     WriteProfileString('windows', 'device', Device);
     StrCopy(Device, 'windows');
     SendMessage(HWND_BROADCAST, WM_WININICHANGE,0,LongInt(@Device));
  end;
  ToolButton27Click(Self);
end;

procedure TSubu00.ToolButton25Click(Sender: TObject);
begin

  Timer1.OnTimer:=nil;

{ if Base10.Socket.Active=False then begin
    ShowMessage('서버와 연결실패... '+#13+'프로그램을 종료합니다.');
    Close;
  end;

  if Base10.Socket.Active=True then begin
    nUse1:='Client-Connect-2'+'Uses:'+nUses+'Pcip:'+nPcip+'Subu:';
    nUse2:=nUse1+'Sub00';
    mPrnt:=Base10.Seek_Uses(nUse2);
    nUse1:='Client-Connect-1'+'Uses:'+nUses+'Pcip:'+nPcip+'Subu:';
    nUse2:=nUse1+'Sub00';
    nUse2:=Base10.Seek_Uses(nUse2);
  end;

  if nUse2='X' then begin
    ShowMessage('환경설정 실패... '+#13+'프로그램을 종료합니다.');
    Close;
  end; }

end;

procedure TSubu00.ToolButton26Click(Sender: TObject);
var
  Device : array[0 .. 255] of char;
  Driver : array[0 .. 255] of char;
  Port : array[0 .. 32] of char;
  hDMode : THandle;
  pDMode : PDevMode;
begin
  Sqlen :='Select Top,L11,L61,L62 From Gg_Magn Where '+'Gu'+'='+#39+'0'+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  if StrToIntDef(SGrid.Cells[ 3,1],0)<>0 then begin
  Printer.GetPrinter(Device, Driver, Port, hDMode);
  if hDMode=0 then Exit;
  pDMode:=GlobalLock(hDMode);
  if pDMode=nil then Exit;
  pDMode^.dmFields     :=(pDMode^.dmFields)or(DM_PAPERLENGTH)or(DM_PAPERWIDTH);
  pDMode^.dmPaperSize  :=DMPAPER_USER;
  pDMode^.dmPaperWidth :=StrToIntDef(SGrid.Cells[ 2,1],0);
  pDMode^.dmPaperLength:=StrToIntDef(SGrid.Cells[ 3,1],0);
  GlobalUnlock(hDMode);
  Printer.SetPrinter(Device, Driver, Port, hDMode);
  end;
//FormActivate(Self);
//Tong30.Show;
end;

procedure TSubu00.ToolButton27Click(Sender: TObject);
var
  Device : array[0 .. 255] of char;
  Driver : array[0 .. 255] of char;
  Port : array[0 .. 32] of char;
  hDMode : THandle;
  pDMode : PDevMode;
begin
  Sqlen :='Select Top,L11,L61,L62 From Gg_Magn Where '+'Gu'+'='+#39+'8'+#39;

  Base10.Socket.RunSQL(Sqlen);
  Base10.Socket.busyloop;
  if Base10.Socket.body_data <> 'ERROR' then
     Base10.Socket.MakeGrid(SGrid)
  else ShowMessage(E_Open);

  if StrToIntDef(SGrid.Cells[ 3,1],0)<>0 then begin
  Printer.GetPrinter(Device, Driver, Port, hDMode);
  if hDMode=0 then Exit;
  pDMode:=GlobalLock(hDMode);
  if pDMode=nil then Exit;
  pDMode^.dmFields     :=(pDMode^.dmFields)or(DM_PAPERLENGTH)or(DM_PAPERWIDTH);
  pDMode^.dmPaperSize  :=DMPAPER_USER;
  pDMode^.dmPaperWidth :=StrToIntDef(SGrid.Cells[ 2,1],0);
  pDMode^.dmPaperLength:=StrToIntDef(SGrid.Cells[ 3,1],0);
  GlobalUnlock(hDMode);
  Printer.SetPrinter(Device, Driver, Port, hDMode);
  end;
//FormActivate(Self);
//Tong30.Show;
end;

procedure TSubu00.Menu101Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub11';
  nUse2:=Base10.Seek_Uses('F11');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo11 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo11 := TSobo11.Create( self );

    if nUse2='O' then begin
    Sobo11.Panel002.Enabled:=True;
    Sobo11.Panel004.Enabled:=True;
    Sobo11.DBGrid101.OnKeyDown:=Sobo11.DBGrid101KeyDown;
    Sobo11.DBGrid101.OnKeyPress:=Sobo11.DBGrid101KeyPress;
    Sobo11.DBGrid101.OnDblClick:=Sobo11.DBGrid101DblClick;
    Sobo11.DBGrid201.OnKeyDown:=Sobo11.DBGrid201KeyDown;
    Sobo11.DBGrid201.OnKeyPress:=Sobo11.DBGrid201KeyPress;
    end;
    if nUse2='R' then begin
    Sobo11.Panel002.Enabled:=False;
    Sobo11.Panel004.Enabled:=False;
    Sobo11.DBGrid101.OnKeyDown:=nil;
    Sobo11.DBGrid101.OnKeyPress:=nil;
    Sobo11.DBGrid101.OnDblClick:=nil;
    Sobo11.DBGrid201.OnKeyDown:=nil;
    Sobo11.DBGrid201.OnKeyPress:=nil;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu102Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub12';
  nUse2:=Base10.Seek_Uses('F12');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo12 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo12 := TSobo12.Create( self );

    if nUse2='O' then begin
    Sobo12.Panel002.Enabled:=True;
    Sobo12.Panel004.Enabled:=True;
    Sobo12.DBGrid101.OnKeyDown:=Sobo12.DBGrid101KeyDown;
    Sobo12.DBGrid101.OnKeyPress:=Sobo12.DBGrid101KeyPress;
    Sobo12.DBGrid101.OnDblClick:=Sobo12.DBGrid101DblClick;
    Sobo12.DBGrid201.OnKeyDown:=Sobo12.DBGrid201KeyDown;
    Sobo12.DBGrid201.OnKeyPress:=Sobo12.DBGrid201KeyPress;
    end;
    if nUse2='R' then begin
    Sobo12.Panel002.Enabled:=False;
    Sobo12.Panel004.Enabled:=False;
    Sobo12.DBGrid101.OnKeyDown:=nil;
    Sobo12.DBGrid101.OnKeyPress:=nil;
    Sobo12.DBGrid101.OnDblClick:=nil;
    Sobo12.DBGrid201.OnKeyDown:=nil;
    Sobo12.DBGrid201.OnKeyPress:=nil;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu103Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub13';
  nUse2:=Base10.Seek_Uses('F13');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo13 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo13 := TSobo13.Create( self );

    if nUse2='O' then begin
    Sobo13.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo13.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu104Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub14';
  nUse2:=Base10.Seek_Uses('F14');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo14 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo14 := TSobo14.Create( self );

    if nUse2='O' then begin
    Sobo14.Panel002.Enabled:=True;
    Sobo14.Panel004.Enabled:=True;
    Sobo14.DBGrid101.OnKeyDown:=Sobo14.DBGrid101KeyDown;
    Sobo14.DBGrid101.OnKeyPress:=Sobo14.DBGrid101KeyPress;
    Sobo14.DBGrid101.OnDblClick:=Sobo14.DBGrid101DblClick;
    Sobo14.DBGrid201.OnKeyDown:=Sobo14.DBGrid201KeyDown;
    Sobo14.DBGrid201.OnKeyPress:=Sobo14.DBGrid201KeyPress;
    end;
    if nUse2='R' then begin
    Sobo14.Panel002.Enabled:=False;
    Sobo14.Panel004.Enabled:=False;
    Sobo14.DBGrid101.OnKeyDown:=nil;
    Sobo14.DBGrid101.OnKeyPress:=nil;
    Sobo14.DBGrid101.OnDblClick:=nil;
    Sobo14.DBGrid201.OnKeyDown:=nil;
    Sobo14.DBGrid201.OnKeyPress:=nil;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu105Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub15';
  nUse2:=Base10.Seek_Uses('F15');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo15 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo15 := TSobo15.Create( self );

    if nUse2='O' then begin
    Sobo15.Panel002.Enabled:=True;
    Sobo15.Panel004.Enabled:=True;
    Sobo15.DBGrid101.OnKeyDown:=Sobo15.DBGrid101KeyDown;
    Sobo15.DBGrid101.OnKeyPress:=Sobo15.DBGrid101KeyPress;
    Sobo15.DBGrid101.OnDblClick:=Sobo15.DBGrid101DblClick;
    Sobo15.DBGrid201.OnKeyDown:=Sobo15.DBGrid201KeyDown;
    Sobo15.DBGrid201.OnKeyPress:=Sobo15.DBGrid201KeyPress;
    end;
    if nUse2='R' then begin
    Sobo15.Panel002.Enabled:=False;
    Sobo15.Panel004.Enabled:=False;
    Sobo15.DBGrid101.OnKeyDown:=nil;
    Sobo15.DBGrid101.OnKeyPress:=nil;
    Sobo15.DBGrid101.OnDblClick:=nil;
    Sobo15.DBGrid201.OnKeyDown:=nil;
    Sobo15.DBGrid201.OnKeyPress:=nil;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu106Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub16';
  nUse2:=Base10.Seek_Uses('F16');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo16 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo16 := TSobo16.Create( self );

    if nUse2='O' then begin
    Sobo16.DBGrid101.ReadOnly:=False;
    Sobo16.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo16.DBGrid101.ReadOnly:=True;
    Sobo16.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu107Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub17';
  nUse2:=Base10.Seek_Uses('F17');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo17 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo17 := TSobo17.Create( self );

    if nUse2='O' then begin
    Sobo17.Panel002.Enabled:=True;
    Sobo17.Panel004.Enabled:=True;
    Sobo17.DBGrid101.OnKeyDown:=Sobo17.DBGrid101KeyDown;
    Sobo17.DBGrid101.OnKeyPress:=Sobo17.DBGrid101KeyPress;
    Sobo17.DBGrid101.OnDblClick:=Sobo17.DBGrid101DblClick;
    Sobo17.DBGrid201.OnKeyDown:=Sobo17.DBGrid201KeyDown;
    Sobo17.DBGrid201.OnKeyPress:=Sobo17.DBGrid201KeyPress;
    end;
    if nUse2='R' then begin
    Sobo17.Panel002.Enabled:=False;
    Sobo17.Panel004.Enabled:=False;
    Sobo17.DBGrid101.OnKeyDown:=nil;
    Sobo17.DBGrid101.OnKeyPress:=nil;
    Sobo17.DBGrid101.OnDblClick:=nil;
    Sobo17.DBGrid201.OnKeyDown:=nil;
    Sobo17.DBGrid201.OnKeyPress:=nil;
    end;

  end else
    ShowMessage(E_Connect);
//ToolBar.Visible:=True;
end;

procedure TSubu00.Menu108Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub18';
  nUse2:=Base10.Seek_Uses('F18');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo18 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo18 := TSobo18.Create( self );

  end else
    ShowMessage(E_Connect); }
//ToolBar.Visible:=False;
end;

procedure TSubu00.Menu109Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub19';
  nUse2:=Base10.Seek_Uses('F19');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo19 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo19 := TSobo19.Create( self );

  end else
    ShowMessage(E_Connect); }
  Close;
end;

procedure TSubu00.Menu110Click(Sender: TObject);
var SetupIni : TIniFile;
begin
  nUse2:=nUse1+'Sub19';
  nUse2:=Base10.Seek_Uses('F19');
  if nUse2<>'X' then begin

    Sqlen:='0';

    Sobo10 := TSobo10.Create(Application);
    if Sobo10.ShowModal=mrOK Then begin

      Sqlen :='Select Hcode,Hname,Gpass From Id_Logn '+
              'Where Gcode='+#39+Sobo10.Edit101.Text+#39+
              '  and Gpass='+#39+Sobo10.Edit102.Text+#39;

      Base10.Socket.RunSQL(Sqlen);
      Base10.Socket.busyloop;
      if Base10.Socket.Body_Data <> 'NODATA' then begin
        ShowMessage('사용중인 ID,Password입니다. 다시 등록해주십시오');
      end else begin
        Sqlen := 'UPDATE Id_Logn SET Gcode=''@Gcode'',Gname=''@Gname'',Gpass=''@Gpass'' '+
                 'WHERE Hcode=''@Hcode'' and Gcode=''@Qcode'' and Gname=''@Qname'' and Gpass=''@Qpass'' ';
        Translate(Sqlen, '@Gname', Sobo10.Edit100.Text);
        Translate(Sqlen, '@Gcode', Sobo10.Edit101.Text);
        Translate(Sqlen, '@Gpass', Sobo10.Edit102.Text);
        Translate(Sqlen, '@Qname', Logn1);
        Translate(Sqlen, '@Qcode', Logn2);
        Translate(Sqlen, '@Qpass', Logn3);
        Translate(Sqlen, '@Hcode', Hnnnn);
        Base10.Socket.RunSQL(Sqlen);
        Base10.Socket.BusyLoop;
        if Base10.Socket.Body_Data = 'ERROR' then ShowMessage(E_Update);

        SetupIni := TIniFile.Create(GetExecPath + 'Config.Ini');
        With SetupIni do begin
          WriteString('Client', 'Uses', Sobo10.Edit100.Text);
          WriteString('Client', 'UserName', MimeEncodeString(Sobo10.Edit101.Text));
          WriteString('Client', 'Password', MimeEncodeString(Sobo10.Edit102.Text));
        end;
        SetupIni.Free;

        Logn1:=Sobo10.Edit100.Text;
        Logn2:=Sobo10.Edit101.Text;
        Logn3:=Sobo10.Edit102.Text;

        ShowMessage('수정되었습니다.');
      end;
    end;
    Sobo10.Free;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu201Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub21';
  nUse2:=Base10.Seek_Uses('F21');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo21 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo21 := TSobo21.Create( self );

    if nUse2='O' then begin
    Sobo21.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo21.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu202Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub22';
  nUse2:=Base10.Seek_Uses('F22');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo22 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo22 := TSobo22.Create( self );

    if nUse2='O' then begin
    Sobo22.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo22.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu203Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub23';
  nUse2:=Base10.Seek_Uses('F23');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo23 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo23 := TSobo23.Create( self );

    if nUse2='O' then begin
    Sobo23.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo23.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu204Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub24';
  nUse2:=Base10.Seek_Uses('F24');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo24 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo24 := TSobo24.Create( self );

    if nUse2='O' then begin
    Sobo24.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo24.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu205Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub25';
  nUse2:=Base10.Seek_Uses('F25');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo25 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo25 := TSobo25.Create( self );

    if nUse2='O' then begin
    Sobo25.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo25.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu206Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub26';
  nUse2:=Base10.Seek_Uses('F26');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo26 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo26 := TSobo26.Create( self );

    if nUse2='O' then begin
    Sobo26.DBGrid101.ReadOnly:=False;
    Sobo26.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo26.DBGrid101.ReadOnly:=True;
    Sobo26.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu207Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub27';
  nUse2:=Base10.Seek_Uses('F27');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo27 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo27 := TSobo27.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu208Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub28';
  nUse2:=Base10.Seek_Uses('F28');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo28 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo28 := TSobo28.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu209Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub29';
  nUse2:=Base10.Seek_Uses('F29');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo29 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo29 := TSobo29.Create( self );

    if nUse2='O' then begin
    Sobo29.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo29.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu210Click(Sender: TObject);
begin
//
end;

procedure TSubu00.Menu301Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub31';
  nUse2:=Base10.Seek_Uses('F31');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo31 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo31 := TSobo31.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu302Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub32';
  nUse2:=Base10.Seek_Uses('F32');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo32 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo32 := TSobo32.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu303Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub33';
  nUse2:=Base10.Seek_Uses('F33');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo33 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo33 := TSobo33.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu304Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub34';
  nUse2:=Base10.Seek_Uses('F34');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo34 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo34 := TSobo34.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu305Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub35';
  nUse2:=Base10.Seek_Uses('F35');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo35 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo35 := TSobo35.Create( self );

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu306Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub36';
  nUse2:=Base10.Seek_Uses('F36');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo36 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo36 := TSobo36.Create( self );

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu307Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub37';
  nUse2:=Base10.Seek_Uses('F37');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo37 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo37 := TSobo37.Create( self );

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu308Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub38';
  nUse2:=Base10.Seek_Uses('F38');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSeok30 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Seok30 := TSeok30.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu309Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub39';
  nUse2:=Base10.Seek_Uses('F39');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo39 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo39 := TSobo39.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu310Click(Sender: TObject);
begin
//
end;

procedure TSubu00.Menu401Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub41';
  nUse2:=Base10.Seek_Uses('F41');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo41 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo41 := TSobo41.Create( self );

    if nUse2='O' then begin
    Sobo41.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo41.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu402Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub42';
  nUse2:=Base10.Seek_Uses('F42');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo42 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo42 := TSobo42.Create( self );

    if nUse2='O' then begin
    Sobo42.DBGrid101.ReadOnly:=False;
  //Sobo42.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo42.DBGrid101.ReadOnly:=True;
  //Sobo42.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu403Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub43';
  nUse2:=Base10.Seek_Uses('F43');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo43 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo43 := TSobo43.Create( self );

    if nUse2='O' then begin
    Sobo43.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo43.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu404Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub44';
  nUse2:=Base10.Seek_Uses('F44');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo44 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo44 := TSobo44.Create( self );

    if nUse2='O' then begin
    Sobo44.DBGrid101.ReadOnly:=False;
    Sobo44.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo44.DBGrid101.ReadOnly:=True;
    Sobo44.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu405Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub45';
  nUse2:=Base10.Seek_Uses('F45');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo45 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo45 := TSobo45.Create( self );

    if nUse2='O' then begin
    Sobo45.DBGrid101.ReadOnly:=False;
    Sobo45.DBGrid201.ReadOnly:=False;
    Sobo45.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo45.DBGrid101.ReadOnly:=True;
    Sobo45.DBGrid201.ReadOnly:=True;
    Sobo45.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu406Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub46';
  nUse2:=Base10.Seek_Uses('F46');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo46 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo46 := TSobo46.Create( self );

    if nUse2='O' then begin
    Sobo46.Panel002.Enabled:=True;
    Sobo46.Panel004.Enabled:=True;
    Sobo46.DBGrid101.OnKeyDown:=Sobo46.DBGrid101KeyDown;
    Sobo46.DBGrid101.OnKeyPress:=Sobo46.DBGrid101KeyPress;
    Sobo46.DBGrid101.OnDblClick:=Sobo46.DBGrid101DblClick;
    Sobo46.DBGrid201.OnKeyDown:=Sobo46.DBGrid201KeyDown;
    Sobo46.DBGrid201.OnKeyPress:=Sobo46.DBGrid201KeyPress;
    end;
    if nUse2='R' then begin
    Sobo46.Panel002.Enabled:=False;
    Sobo46.Panel004.Enabled:=False;
    Sobo46.DBGrid101.OnKeyDown:=nil;
    Sobo46.DBGrid101.OnKeyPress:=nil;
    Sobo46.DBGrid101.OnDblClick:=nil;
    Sobo46.DBGrid201.OnKeyDown:=nil;
    Sobo46.DBGrid201.OnKeyPress:=nil;
    end;

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu407Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub47';
  nUse2:=Base10.Seek_Uses('F47');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo47 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo47 := TSobo47.Create( self );

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu408Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub48';
  nUse2:=Base10.Seek_Uses('F48');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo48 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo48 := TSobo48.Create( self );

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu409Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub49';
  nUse2:=Base10.Seek_Uses('F49');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo49 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo49 := TSobo49.Create( self );

    if nUse2='O' then begin
    Sobo49.DBGrid101.ReadOnly:=False;
    Sobo49.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo49.DBGrid101.ReadOnly:=True;
    Sobo49.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu410Click(Sender: TObject);
begin
//
end;

procedure TSubu00.Menu501Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub51';
  nUse2:=Base10.Seek_Uses('F51');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo51 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo51 := TSobo51.Create( self );

    if nUse2='O' then begin
    Sobo51.DBGrid101.ReadOnly:=False;
    Sobo51.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo51.DBGrid101.ReadOnly:=True;
    Sobo51.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu502Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub52';
  nUse2:=Base10.Seek_Uses('F52');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo52 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo52 := TSobo52.Create( self );

    if nUse2='O' then begin
    Sobo52.DBGrid101.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo52.DBGrid101.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu503Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub53';
  nUse2:=Base10.Seek_Uses('F53');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo53 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo53 := TSobo53.Create( self );

    if nUse2='O' then begin
    Sobo53.DBGrid101.ReadOnly:=False;
    Sobo53.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo53.DBGrid101.ReadOnly:=True;
    Sobo53.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu504Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub54';
  nUse2:=Base10.Seek_Uses('F54');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo54 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo54 := TSobo54.Create( self );

    if nUse2='O' then begin
    Sobo54.DBGrid101.ReadOnly:=False;
    Sobo54.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo54.DBGrid101.ReadOnly:=True;
    Sobo54.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu505Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub55';
  nUse2:=Base10.Seek_Uses('F55');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo55 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo55 := TSobo55.Create( self );

    if nUse2='O' then begin
    Sobo55.DBGrid101.ReadOnly:=False;
    Sobo55.DBGrid201.ReadOnly:=False;
    end;
    if nUse2='R' then begin
    Sobo55.DBGrid101.ReadOnly:=True;
    Sobo55.DBGrid201.ReadOnly:=True;
    end;

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu506Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub56';
  nUse2:=Base10.Seek_Uses('F56');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo56 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo56 := TSobo56.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu507Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub57';
  nUse2:=Base10.Seek_Uses('F57');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo57 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo57 := TSobo57.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu508Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub58';
  nUse2:=Base10.Seek_Uses('F58');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo58 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo58 := TSobo58.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu509Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub59';
  nUse2:=Base10.Seek_Uses('F59');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo59 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo59 := TSobo59.Create( self );

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu510Click(Sender: TObject);
begin
//
end;

procedure TSubu00.Menu601Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub61';
  nUse2:=Base10.Seek_Uses('F61');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo61 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo61 := TSobo61.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu602Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub62';
  nUse2:=Base10.Seek_Uses('F62');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo62 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo62 := TSobo62.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu603Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub63';
  nUse2:=Base10.Seek_Uses('F63');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo63 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo63 := TSobo63.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu604Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub64';
  nUse2:=Base10.Seek_Uses('F64');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo64 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo64 := TSobo64.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu605Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub65';
  nUse2:=Base10.Seek_Uses('F65');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo65 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo65 := TSobo65.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu606Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub66';
  nUse2:=Base10.Seek_Uses('F66');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo66 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo66 := TSobo66.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu607Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub67';
  nUse2:=Base10.Seek_Uses('F67');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo67 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo67 := TSobo67.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu608Click(Sender: TObject);
var I:Integer;
begin
  nUse2:=nUse1+'Sub68';
  nUse2:=Base10.Seek_Uses('F68');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo68 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo68 := TSobo68.Create( self );

  end else
    ShowMessage(E_Connect);
end;

procedure TSubu00.Menu609Click(Sender: TObject);
var I:Integer;
begin
{ nUse2:=nUse1+'Sub69';
  nUse2:=Base10.Seek_Uses('F69');
  if nUse2<>'X' then begin

    for I:=0 to MDIChildCount - 1 do
    if MDIChildren[I] is TSobo69 then begin
       MDIChildren[I].Show;
       Exit;
    end;
    Sobo69 := TSobo69.Create( self );

  end else
    ShowMessage(E_Connect); }
end;

procedure TSubu00.Menu610Click(Sender: TObject);
begin
//
end;

procedure TSubu00.Ping1DnsLookupDone(Sender: TObject; Error: Word);
begin
  Ping1.Address := Ping1.DnsResult;
  Ping1.Ping;
end;

procedure TSubu00.Ping1EchoReply(Sender, Icmp: TObject; Error: Integer);
begin
  if Error = 0 then
  ShowMessage('연결 중시! 확인해 주십시오.')
  else
  ShowMessage(Ping1.HostIP);
end;

procedure TSubu00.Ping1EchoRequest(Sender, Icmp: TObject);
begin
  nPcip:=Ping1.HostIP;
end;

initialization
begin
  xMutex := CreateMutex(NIL, FALSE, 'Chulpan.exe');
  if GetLastError() = ERROR_ALREADY_EXISTS then begin
    MessageBox(Application.Handle, 'Program을 다시 시작 하세요.', 'Error', MB_OK);
    Application.Terminate();
  end;
end;

end.
